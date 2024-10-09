import requests
from datetime import datetime
from django.contrib import messages
import os

from django.shortcuts import *

def home(request,city=None):
    if request.method == 'POST':
        city = request.POST.get('city')
        return redirect('getcity', city=city)
    return render(request,'index.html')

def index(request, city):
    data = {}
    if request.method == 'POST':
        city = request.POST.get('city')
        return redirect('getcity', city=city)

    api_key = os.getenv('weather_key')
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}'

    response = requests.get(url)
    
    if response.status_code == 200:
        weather_data = response.json()
        # print(weather_data)
        current_time = datetime.now().strftime("%A, %B %d %Y, %H:%M:%S %p")
        
        data = {
            'city': city,
            'temperature': f'Temperature: {weather_data["main"]["temp"]} °C',
            'min_temp': f'{weather_data["main"]["temp_min"]} °C',
            'max_temp': f'{weather_data["main"]["temp_max"]} °C',
            'real_feel': f'{weather_data["main"]["feels_like"]} °C',
            'wind': f'{weather_data["wind"]["speed"]} km/h',
            'humidity': f'{weather_data["main"]["humidity"]} %',
            'pressure': f'{weather_data["main"]["pressure"]} hPa',
            'time': current_time
        }
        
        return render(request, 'index.html', {'data': data, 'city': city})
    
    elif response.status_code == 404:
        messages.warning(request, 'Location not Found.') # city name/location
    elif response.status_code == 401:
        messages.warning(request, 'Please check your API_KEY.') # api_key error
    elif response.status_code == 400:
        messages.warning(request, 'Bad request. Please check your URL.') # url error
    else: 
        messages.warning(request, f'API error: {response.status_code}')

    return render(request, 'index.html', {'data': data, 'city': city})
