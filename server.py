from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

# Initialize Flask app
app = Flask(__name__)

# Routes
@app.route('/')
@app.route('/index')
def index():
    """Render the homepage with a search form."""
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    """
    Handle weather search requests.
    If city is valid, show weather data. Otherwise, show an error page.
    """
    city = request.args.get('city')

    # Handle empty or invalid input
    if not city or not city.strip():
        city = "Kansas City"

    weather_data = get_current_weather(city)

    # Debug: Log API response
    print("API Response:", weather_data)

    # Check for API errors or invalid data
    if not weather_data or 'cod' not in weather_data or weather_data['cod'] != 200:
        return render_template('city-not-found.html')

    # Extract icon or use fallback
    icon = weather_data['weather'][0]['icon'] if 'weather' in weather_data and weather_data['weather'][0].get('icon') else '01d'

    # Pass data to the template
    return render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}",
        icon=icon
    )

# Run the app using Waitress
if __name__ == "__main__":
    print("Starting Flask server...")
    serve(app, host="0.0.0.0", port=8000)
