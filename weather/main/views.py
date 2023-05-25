from django.shortcuts import render
import requests
from .models import City, Conditions
from .forms import CityForm, ConditionsForm
from django.views.generic.edit import CreateView
import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from django.http import HttpResponse

load_dotenv()

def index(request):
    openweathermap_api_key = os.environ.get('OPENWEATHERMAP_API_KEY')

    # url = f'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={openweathermap_api_key}'
    # weather_response = requests.get(url)
    # logging.info(weather_response.json())
    # cities = City.objects.filter(conditions__selector=request.POST.get('selector')) if request.method == 'POST' else City.objects.all()

    # form = CityForm(request.POST) if request.method == 'POST' else CityForm()
    # condition_form = ConditionsForm(request.POST) if request.method == 'POST' else ConditionsForm()

    cities = City.objects.all()  # return all the cities in the database

    weather_input = None     
    if request.method == 'POST':  # only true if form is submitted
        form = CityForm(request.POST)  # add actual request data to form for processing
        condition_form = ConditionsForm(request.POST)
        print("POST")
        print(request.POST)

        if condition_form.is_valid():
            weather_input = condition_form.cleaned_data['selector']
    else:
        condition_form = ConditionsForm()

    weather_data = []
    context = {'weather_data' : weather_data, 'condition_form': condition_form}
    print("user input", weather_input)
    if weather_input:
        city_name_mappings = {
            'Nashville-Davidson': 'Nashville',
            'Louisville/Jefferson County': 'Louisville',
            'Augusta-Richmond County': 'Augusta',
            'Macon-Bibb County': 'Macon County',
            'Athens-Clarke County': 'Athens County',
        }

        for city in cities:
            try:
                city_clean_name = city_name_mappings.get(city.name, city.name)
                url = f'http://api.openweathermap.org/data/2.5/weather?q={city_clean_name}&units=imperial&appid={openweathermap_api_key}'
                city_weather = requests.get(url.format(city_clean_name)).json() #request the API data and convert the JSON to Python data types
                # pprint(city_weather)
                city_state = city.state
                weather = {
                    'city' : city,
                    'state' : city_state,
                    'temperature' : city_weather['main']['temp'],
                    'wind' : city_weather['wind']['speed'],
                    'condition' : id_to_condition(city_weather['weather'][0]['id']),
                    'icon' : city_weather['weather'][0]['icon']   
                }

                if weather['condition'].lower() == weather_input.lower():
                    weather_data.append(weather) #add the data for the current city into our list
                else:
                    print(f"weather data does not match {city} {weather['condition']}")
            except KeyError:
                print(f"KeyError occurred while processing data for {city.name} {city_name_mappings.get(city.name, None)}. Skipping...")
            continue
        context = {'weather_data' : weather_data, 'condition_form': condition_form}

    return render(request, 'main/index.html', context) #returns the index.html template


def id_to_condition(id: int):
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

def data(request):

    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

    google_sheets_api_key_path = os.getenv("GOOGLE_SHEETS_API_KEY_PATH")

    creds = ServiceAccountCredentials.from_json_keyfile_name(google_sheets_api_key_path, scope)

    client = gspread.authorize(creds)

    sheet = client.open("US Cities").sheet1

    data = sheet.get_all_values()

    for i in range(1,len(data)):
        c = City(name=data[i][0], state=data[i][1])
        c.save()

    cities = City.objects.all() 
    
    for city in cities:
        print(city.name, city.state)

    return HttpResponse("APIs tested successfully")