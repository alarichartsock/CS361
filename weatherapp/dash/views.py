from django.shortcuts import render
import requests
from django.http import JsonResponse
import plotly.offline as opy
import plotly.graph_objs as go
from django.views.generic.base import TemplateView


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
        'feels_like': r['main']['feels_like'],
        'temp_min': r['main']['temp_min'],
        'temp_max': r['main']['temp_max'],
        'pressure': r['main']['pressure'],
        'humidity': r['main']['humidity'],
        'windspeed': r['wind']['speed'],
        'icon': r['weather'][0]['icon']
    }

    beachUrl = 'https://fast-ravine-54409.herokuapp.com/api/spot?beachQuery={}'

    r2 = requests.get(beachUrl.format(city))
    waves = []
    if r2.status_code == 404:
        pass
    else:
        r2 = r2.json()
        try:
            for i in r2:
                requestCoords = (round(r['coord']['lat'], 1), round(r['coord']['lon'], 1))
                beachCoords = (round(float(i['Lat']), 1), round(float(i['Lon']), 1))

                if requestCoords == beachCoords:
                    wavesUrl = 'https://fast-ravine-54409.herokuapp.com/api/wave?spotId={}&intervalHours=3&days=5'
                    r3 = requests.get(wavesUrl.format(i['SpotId']))
                    if r3.status_code == 404:
                        pass
                    r3 = r3.json()
                    waves = r3['WaveMinArray']
                    break
        except:
            pass

    context = {'city_weather': city_weather}

    if len(waves) > 0:
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=waves))
        fig.update_layout(title='Wave Forecast', xaxis_title='Hours From Now', yaxis_title='Wave Height (feet)')
        graph = fig.to_html(full_html=False, default_height=500, default_width=700)
        context = {'city_weather': city_weather, 'graph': graph}
    return render(request, '../templates/report.html', context)


def search(request):
    return render(request, '../templates/search.html')