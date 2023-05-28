from django.db import models
from datetime import timedelta
import requests
import os
from django.utils.timezone import now

WEATHER_CONDITIONS = (
    ("Thunderstorm", "Thunderstorm"),
    ("Drizzle", "Drizzle"),
    ("Rain", "Rain"),
    ("Snow", "Snow"),
    ("Atmosphere", "Atmosphere"),
    ("Clear", "Clear"),
    ("Clouds", "Clouds"),
)

class Conditions(models.Model):
    selector = models.CharField(max_length=12, choices=WEATHER_CONDITIONS, default="thunderstorm")

    def __str__(self):
        return self.selector


class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    conditions = models.ManyToManyField(Conditions)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'cities'

city_name_mappings = {
    'Nashville-Davidson': 'Nashville',
    'Louisville/Jefferson County': 'Louisville',
    'Augusta-Richmond County': 'Augusta',
    'Macon-Bibb County': 'Macon County',
    'Athens-Clarke County': 'Athens County',
}

class WeatherEntry(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.FloatField()
    wind = models.FloatField()
    condition = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    last_updated = models.DateTimeField(default=now)

    @classmethod
    def get_weather_condition(cls, city):
        # Get weather entries matching city name
        entry = cls.objects.filter(city=city).first()
        if entry == None or now() - entry.last_updated >= timedelta(minutes=15):
            # Update the weather entry from the OpenWeather API
            updated_weather = cls._fetch_city_weather_data(city)
            if entry == None:
                print(f"{city.name} data doesn't exist, fetching from openweather")
                entry = WeatherEntry(
                    city=city,
                    temperature=updated_weather['main']['temp'],
                    wind=updated_weather['wind']['speed'],
                    condition=id_to_condition(updated_weather['weather'][0]['id']),
                    icon=updated_weather['weather'][0]['icon'],
                    last_updated=now())
            else:
                print(f"{city.name} outdated (fetching), last updated:", now() - entry.last_updated)
                entry.temperature = updated_weather['main']['temp']
                entry.wind=updated_weather['wind']['speed']
                entry.condition=id_to_condition(updated_weather['weather'][0]['id'])
                entry.icon=updated_weather['weather'][0]['icon']
                entry.last_updated=now()
            entry.save()
        else:
            print(f"{city.name} data up-to-date, displaying from database")
            
        return entry

    @classmethod
    def _fetch_city_weather_data(cls, city):
        city_clean_name = city_name_mappings.get(city.name, city.name)
        openweathermap_api_key = os.environ.get('OPENWEATHERMAP_API_KEY')
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_clean_name},{city.state}&units=imperial&appid={openweathermap_api_key}'
        response = requests.get(url)
        return response.json()
    
def id_to_condition(id):
    if id >= 200 and id <= 232:
        return "Thunderstorm"
    if id >= 300 and id <= 321:
        return "Drizzle"
    if id >= 500 and id <= 531:
        return "Rain"
    if id >= 600 and id <= 622:
        return "Snow"
    if id >= 701 and id <= 781:
        return "Atmosphere"
    if id == 800:
        return "Clear"
    if id >= 801 and id <= 804:
        return "Clouds"