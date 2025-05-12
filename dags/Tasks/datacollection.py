import requests
import pandas as pd


def data_collection():
# Set your API key and city
    API_KEY = 'aa678ab5719073097f21e6ffecc8aae1'
    CITY = 'Lahore'
    BASE_URL = 'https://api.openweathermap.org/data/2.5/forecast'
    
    # Set up request parameters
    params = {
        'q': CITY,
        'appid': API_KEY,
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }
    
    # Make the API request
    response = requests.get(BASE_URL, params=params)
    
    # Check for successful response
    if response.status_code == 200:
        data = response.json()
        
        # Create a list to store extracted data
        weather_data = []
    
        for entry in data['list']:
            dt_txt = entry['dt_txt']
            temp = entry['main']['temp']
            humidity = entry['main']['humidity']
            wind_speed = entry['wind']['speed']
            weather_condition = entry['weather'][0]['description']
    
            weather_data.append({
                'DateTime': dt_txt,
                'Temperature (°C)': temp,
                'Humidity (%)': humidity,
                'Wind Speed (m/s)': wind_speed,
                'Weather Condition': weather_condition
            })
        
        # Convert to DataFrame
        df = pd.DataFrame(weather_data)
        
        # Save to CSV
        filename = "WeatherData/Lahore_Forecast.csv"
        df.to_csv(filename, index=False)
        
        print(f"✅ Data saved to {filename}")
    
    else:
        print(f"❌ Failed to fetch data. Status code: {response.status_code}")
        print(response.text)
    