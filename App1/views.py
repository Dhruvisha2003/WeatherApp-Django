import requests
from datetime import datetime

from django.shortcuts import *

def index(request):
    data = {}
    if request.method == 'POST':
        city = request.POST.get('city')
        api_key = '7c0390401c2c7a8243c01c653c5b929e'
        
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}'  
        list_of_data = requests.get(url).json()
        current_time = datetime.now()
        time = current_time.strftime("%A, %B %d %Y, %H:%M:%S %p")
    
        data = {
                    'city': city,
                    'temperature': f'Temperature: {list_of_data["main"]["temp"]} °C',
                    'min_temp': f' {list_of_data["main"]["temp_min"]} °C',
                    'max_temp': f' {list_of_data["main"]["temp_max"]} °C',
                    'real_feel': f' {list_of_data["main"]["feels_like"]} °C',  
                    'wind': f' {list_of_data["wind"]["speed"]} km/h',
                    'humidity': f' {list_of_data["main"]["humidity"]} %',
                    'pressure': f' {list_of_data["main"]["pressure"]} hPa', 
                    'time': time
        }
        return redirect('home')
    return render(request, 'index.html', {'data': data})
