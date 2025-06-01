from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = 'bd4534efdd9cd75710704ea6bfda1f7c'  

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    forecast_data = None
    error = None
    if request.method == 'POST':
        city = request.form.get('city')
        if city:

            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon']
                }
                # Forecast API call
                forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
                forecast_response = requests.get(forecast_url)
                if forecast_response.status_code == 200:
                    forecast_json = forecast_response.json()
                    
                    forecast_data = []
                    for item in forecast_json['list'][:5]:
                        forecast_data.append({
                            'datetime': item['dt_txt'],
                            'temperature': item['main']['temp'],
                            'description': item['weather'][0]['description'],
                            'icon': item['weather'][0]['icon']
                        })
                else:
                    error = "Could not retrieve forecast data."
            else:
                error = "City not found. Please try again."
        else:
            error = "Please enter a city name."
    return render_template('index.html', weather=weather_data, forecast=forecast_data, error=error)

if __name__ == '__main__':
    app.run(debug=True)
