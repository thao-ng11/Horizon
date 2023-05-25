from django.db import models

WEATHER_CONDITIONS = (
    ("thunderstorm", "Thunderstorm"),
    ("drizzle", "Drizzle"),
    ("rain", "Rain"),
    ("snow", "Snow"),
    ("atmosphere", "Atmosphere"),
    ("clear", "Clear"),
    ("clouds", "Clouds"),
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


# class Weather(models.Model):
#     city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='weather')
#     temperature = models.DecimalField(max_digits=12, decimal_places=2)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Weather in {self.city.name} at {self.timestamp}"
    