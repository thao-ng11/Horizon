from django.contrib import admin
from .models import City, WeatherEntry

admin.site.register(City)
@admin.register(WeatherEntry)
class WeatherEntryAdmin(admin.ModelAdmin):
    pass