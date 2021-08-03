from django.shortcuts import render
import re 
import requests
from django.http import JsonResponse


def dash(request):
    return render(request, '../templates/dash.html')


def settings(request):
    return render(request, '../templates/settings.html')


def forecast(request, city="Bend"):
    # city = 'Bend'
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=e9f5eeaa457c2534493eff2db78e840b'

    r = requests.get(url.format(city)).json()
    print(r)

    city_weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon']
    }

    return JsonResponse(city_weather, safe=False)

def report(request, city="Bend"):
    # city = 'Bend'
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=e9f5eeaa457c2534493eff2db78e840b'

    r = requests.get(url.format(city))
    if r.status_code == 404:
        return render(request, '../templates/error.html')
    r = r.json()
    

    city_weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon']
    }

    context = {'city_weather': city_weather}

    print(city_weather)
    return render(request, '../templates/report.html', context)


def search(request):
    return render(request, '../templates/search.html')