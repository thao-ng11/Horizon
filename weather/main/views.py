from django.shortcuts import render
from .models import City, WeatherEntry
from .forms import ConditionsForm
import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from django.http import HttpResponse
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

def index(request):
    cities = City.objects.all()  # return all the cities in the database

    weather_input = None
    if request.method == 'POST':  # only true if form is submitted
        condition_form = ConditionsForm(request.POST)
        print("POST")
        print(request.POST)

        if condition_form.is_valid():
            weather_input = condition_form.cleaned_data['selector']
    else:
        condition_form = ConditionsForm()

    weather_data = []

    if weather_input:
        pool = ThreadPoolExecutor()
        results = pool.map(WeatherEntry.get_weather_condition, cities)

        for city_weather_data in results:
            if city_weather_data and city_weather_data.condition == weather_input:
                weather_data.append(city_weather_data)

    context = {'weather_data': weather_data, 'condition_form': condition_form}
    return render(request, 'main/index.html', context)

def data(request):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]

    google_sheets_api_key_path = os.getenv("GOOGLE_SHEETS_API_KEY_PATH")

    creds = ServiceAccountCredentials.from_json_keyfile_name(google_sheets_api_key_path, scope)

    client = gspread.authorize(creds)

    sheet = client.open("US Cities").sheet1

    data = sheet.get_all_values()

    for i in range(1, len(data)):
        c = City(name=data[i][0], state=data[i][1])
        c.save()

    cities = City.objects.all()

    for city in cities:
        print(city.name, city.state)

    return HttpResponse("APIs tested successfully")

