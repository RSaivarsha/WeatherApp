import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv
import io
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'YOUR SECRET KEY'  # Replace with a secure key
db = SQLAlchemy(app)

# Replace with your actual WeatherAPI key
WEATHER_API_KEY = 'YOUR WEATHER_API_KEY'
BASE_URL = "http://api.weatherapi.com/v1"

# Database model for storing weather requests
class WeatherRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    # We'll store a JSON structure with daily forecast details
    weather_info = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<WeatherRequest {self.location} from {self.start_date} to {self.end_date}>"

def get_weather_data(location, start_date, end_date):
    """
    Calls WeatherAPI's forecast endpoint for the specified date range.
    The free plan typically allows up to 3 days of forecast.
    We've added "&aqi=yes" so air quality data is returned if available.
    """
    days_diff = (end_date - start_date).days + 1
    url = f"{BASE_URL}/forecast.json?key={WEATHER_API_KEY}&q={location}&days={days_diff}&aqi=yes"
    try:
        response = requests.get(url)
        data = response.json()
        if "error" in data:
            return f"Error from WeatherAPI: {data['error'].get('message', 'Unknown error')}"
        return json.dumps(data)
    except Exception as e:
        return f"Error retrieving weather data: {str(e)}"

# --- Default Route: Create Request Form ("/") ---
@app.route('/', methods=['GET', 'POST'])
def create():
    """Display the create form and process POST to create a new weather request."""
    if request.method == 'POST':
        location = request.form.get('location')
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')

        # Validate input
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.", "danger")
            return redirect(url_for('create'))
        if start_date > end_date:
            flash("Start date must be on or before end date.", "danger")
            return redirect(url_for('create'))
        if not location or location.strip() == "":
            flash("Location cannot be empty.", "danger")
            return redirect(url_for('create'))

        # Fetch weather data from WeatherAPI
        full_json_str = get_weather_data(location, start_date, end_date)
        if full_json_str.startswith("Error"):
            flash(full_json_str, "danger")
            return redirect(url_for('create'))
        try:
            full_json = json.loads(full_json_str)
            forecast_list = []
            # Extract details for each forecast day
            for forecast_day in full_json['forecast']['forecastday']:
                day_data = forecast_day['day']
                forecast_list.append({
                    "date": forecast_day.get("date"),
                    "maxtemp_c": day_data.get("maxtemp_c"),
                    "mintemp_c": day_data.get("mintemp_c"),
                    "condition": day_data.get("condition", {}).get("text"),
                    "avghumidity": day_data.get("avghumidity"),
                    "maxwind_kph": day_data.get("maxwind_kph"),
                    
                })
        except Exception as e:
            flash("Error extracting forecast details from weather data.", "danger")
            return redirect(url_for('create'))

        simplified_info = json.dumps({"forecast": forecast_list})

        new_request = WeatherRequest(
            location=location,
            start_date=start_date,
            end_date=end_date,
            weather_info=simplified_info
        )
        db.session.add(new_request)
        db.session.commit()

        flash("Weather request created successfully!", "success")
        # Redirect to update page for the new record.
        return redirect(url_for('requestinfo', request_id=new_request.id))
    else:
        return render_template('create.html', name = "Saivarsha Raju")

@app.route('/requestinfo')
def requestinfo():
    """Display a table of all saved weather requests."""
    requests_list = WeatherRequest.query.all()[::-1]
    return render_template('index.html', requests=requests_list, name="Saivarsha Raju")

@app.route('/weather', methods=['GET'])
def get_weather():
    """
    Example endpoint to fetch weather data via GET parameters.
    Not strictly required for the create/update flow.
    """
    location = request.args.get('location')
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    if not location or not start_date_str or not end_date_str:
        return jsonify({"error": "location, start_date, and end_date parameters are required."}), 400
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD."}), 400
    if start_date > end_date:
        return jsonify({"error": "start_date must be on or before end_date."}), 400
    weather_info = get_weather_data(location, start_date, end_date)
    if weather_info.startswith("Error"):
        return jsonify({"error": weather_info}), 400
    try:
        weather_json = json.loads(weather_info)
    except json.JSONDecodeError:
        return jsonify({"error": "Unable to parse weather data."}), 500
    return jsonify(weather_json), 200

@app.route('/update/<int:request_id>', methods=['GET', 'POST'])
def update(request_id):
    """Update an existing weather request (storing forecast details)."""
    weather_req = WeatherRequest.query.get_or_404(request_id)
    if request.method == 'POST':
        location = request.form.get('location')
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.", "danger")
            return redirect(url_for('update', request_id=request_id))
        if start_date > end_date:
            flash("Start date must be on or before end date.", "danger")
            return redirect(url_for('update', request_id=request_id))
        if not location or location.strip() == "":
            flash("Location cannot be empty.", "danger")
            return redirect(url_for('update', request_id=request_id))

        full_json_str = get_weather_data(location, start_date, end_date)
        if full_json_str.startswith("Error"):
            flash(full_json_str, "danger")
            return redirect(url_for('update', request_id=request_id))
        try:
            full_json = json.loads(full_json_str)
            forecast_list = []
            for forecast_day in full_json['forecast']['forecastday']:
                day_data = forecast_day['day']
                forecast_list.append({
                    "date": forecast_day.get("date"),
                    "maxtemp_c": day_data.get("maxtemp_c"),
                    "mintemp_c": day_data.get("mintemp_c"),
                    "condition": day_data.get("condition", {}).get("text"),
                    "avghumidity": day_data.get("avghumidity"),
                    "maxwind_kph": day_data.get("maxwind_kph"),
                    "air_quality": day_data.get("air_quality", "N/A")
                })
        except Exception as e:
            flash("Error extracting forecast details from weather data.", "danger")
            return redirect(url_for('update', request_id=request_id))

        simplified_info = json.dumps({"forecast": forecast_list})

        weather_req.location = location
        weather_req.start_date = start_date
        weather_req.end_date = end_date
        weather_req.weather_info = simplified_info

        db.session.commit()
        flash("Weather request updated successfully!", "success")
        return redirect(url_for('requestinfo'))
    return render_template('update.html', weather_req=weather_req)

@app.route('/delete/<int:request_id>', methods=['POST'])
def delete(request_id):
    """Delete a weather request."""
    weather_req = WeatherRequest.query.get_or_404(request_id)
    db.session.delete(weather_req)
    db.session.commit()
    flash("Weather request deleted successfully!", "success")
    return redirect(url_for('requestinfo'))

@app.route('/detail/<int:request_id>')
def detail(request_id):
    """
    Display detailed info for a weather request.
    Iterates over the forecast data and displays max/min temperatures,
    condition, humidity, wind, and air quality.
    """
    weather_req = WeatherRequest.query.get_or_404(request_id)
    youtube_search_url = f"https://www.youtube.com/results?search_query={weather_req.location.replace(' ', '+')}+travel"
    google_maps_url = f"https://www.google.com/maps/search/{weather_req.location.replace(' ', '+')}"
    try:
        forecast_data = json.loads(weather_req.weather_info).get("forecast", [])
    except:
        forecast_data = []
    return render_template('detail.html',
                           weather_req=weather_req,
                           forecast_data=forecast_data,
                           youtube_search_url=youtube_search_url,
                           google_maps_url=google_maps_url)

@app.route('/export/json')
def export_json():
    weather_requests = WeatherRequest.query.all()
    data = []
    for req in weather_requests:
        data.append({
            'id': req.id,
            'location': req.location,
            'start_date': req.start_date.strftime('%Y-%m-%d'),
            'end_date': req.end_date.strftime('%Y-%m-%d'),
            'weather_info': req.weather_info,
            'created_at': req.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(data)

@app.route('/export/csv')
def export_csv():
    weather_requests = WeatherRequest.query.all()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Location', 'Start Date', 'End Date', 'Weather Info', 'Created At'])
    for req in weather_requests:
        cw.writerow([
            req.id, 
            req.location, 
            req.start_date, 
            req.end_date, 
            req.weather_info, 
            req.created_at
        ])
    output = si.getvalue()
    return output, 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename="weather_data.csv"'
    }

@app.route('/info')
def info():
    """PM Accelerator Info Page."""
    pm_info = "Product Manager Accelerator is dedicated to empowering product managers."
    linkedin_url = "https://www.linkedin.com/school/pmaccelerator/"
    return render_template('info.html', pm_info=pm_info, linkedin_url=linkedin_url, name= "Saivarsha Raju")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
