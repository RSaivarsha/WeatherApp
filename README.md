# Weather App

A Flask-based weather application that allows users to:

- **Retrieve real-time or forecasted weather data** for any location (using [WeatherAPI.com](https://www.weatherapi.com/)).
- **Store user requests** (location + date range) in a SQLite database.
- **Perform CRUD operations** on stored weather requests (Create, Read, Update, Delete).
- Optionally, **export data** as JSON or CSV, and integrate additional APIs (e.g., YouTube links, Google Maps).
- Access an **info page** with details about PM Accelerator and a link to their [LinkedIn page](https://www.linkedin.com/company/product-manager-accelerator/).

---

## Table of Contents

- [Demo](#demo)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [License](#license)
- [Credits](#credits)

---

## Demo

- **Video Demo:** [Link to your demo video here](https://drive.google.com/file/d/1FE7r7UyP81YjAomk-r8VfVbhxdMxdVDC/view?usp=sharing)
- **You can test the app here:** [My Weather App](https://myapp.pythonanywhere.com/)

---

## Features

1. **User Input for Location and Date Range**  
   - Accepts city, zip code, or other location formats.
   - Users enter a start date and end date for which they want weather data.

2. **Weather Display**  
   - Shows current weather details such as temperature, conditions, etc.
   - (Optional) Displays a 5-day forecast.
   - (Optional) Uses icons/images for weather conditions.
  
3. **CRUD Operations**  
   - **Create:** Enter a location and date range to fetch and store weather data.
   - **Read:** View all stored weather requests.
   - **Update:** Edit existing weather requests.
   - **Delete:** Remove a weather request from the database.

4. **Additional API Integrations**  
   - Provides YouTube travel video links for the location.
   - Provides a Google Maps link to view the location.
  
5. **Data Export**  
   - Export stored data as JSON or CSV.

6. **Error Handling**  
   - Validates date range (start date must be on or before end date).
   - Handles API errors (e.g., invalid location).

7. **PM Accelerator Info**  
   - The app includes an info button that links to PM Accelerator’s [LinkedIn page](https://www.linkedin.com/company/product-manager-accelerator/).

---

## Tech Stack

- **Backend:** Python, Flask, SQLAlchemy
- **Database:** SQLite
- **Weather API:** [WeatherAPI.com](https://www.weatherapi.com/)
- **Frontend:** Basic HTML/CSS (Bootstrap 4 for styling)

---

## Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/RSaivarsha/WeatherApp.git
   cd WeatherApp
2. **Create a Virtual Environment (recommended)**
    ```bash
    python -m venv venv
3. **Activate the Environment**
   - On Linux/Mac:
      ```bash
      source venv/bin/activate
   - On Windows:
      ```bash
      venv\Scripts\activate
4. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
5. **Set Your WeatherAPI Key**
    **Option A:**
    Edit `app.py` and replace `YOUR_WEATHERAPI_KEY` with your actual key.

    **Option B:**
    Set an environment variable:
   - **On Linux/Mac:**
      ```bash
      export WEATHER_API_KEY="YOUR_REAL_KEY"
    - **On Windows (Command Prompt):**
      ```bash
      set WEATHER_API_KEY="YOUR_REAL_KEY"
6. **Initialize Database**
    The database tables are created automatically when you run the app for the first time.

 
## Usage

### Run the Flask App

    
    python app.py

By default, the app runs on port 8000 (or another port if you specify).

### Open Your Browser
Navigate to http://127.0.0.1:8000.

### Interact with the App
- Create a Weather Request: *Enter a location and date range.*
- View Requests: *See all stored weather requests on the home page.*
- Update/Delete: *Edit or remove existing requests.*
- Additional APIs: *Use provided YouTube and Google Maps links on the detail page.*
- Data Export: *Use the export options to download data as JSON or CSV.*

## Project Structure 
    
    WeatherApp/
    │
    ├── app.py               # Main Flask application
    ├── requirements.txt     # Dependencies
    ├── README.md            # This file
    ├── templates/           # HTML templates
    │   ├── layout.html      # Base layout template
    │   ├── index.html       # Home page (lists weather requests)
    │   ├── create.html      # Form to create a new weather request
    │   ├── update.html      # Form to update an existing request
    │   ├── detail.html      # Detailed view for a weather request
    │   └── info.html        # Info page about PM Accelerator
    └── weather.db           # SQLite database (auto-created)

## How It Works

### Flask Routes
- `GET /`: Displays all stored weather requests.
- `GET/POST /create`: Form to create a new weather request.
- `GET/POST /update/<id>`: Form to update a specific request.
- `POST /delete/<id>`: Deletes a request.
- `GET /detail/<id>`: Detailed view of a weather request, including external links.
- `GET /export/json`: Exports data as JSON.
- `GET /export/csv`: Exports data as CSV.
- `GET /info`: Displays info about PM Accelerator.

### Weather Data Handling
- The app uses a function (`get_weather_data`) to call WeatherAPI and fetch weather data based on user inputs.
- Retrieved data is stored as JSON in the database.

### Database Persistence
- SQLAlchemy is used to manage a SQLite database, ensuring data persists between sessions.

## License
This project is licensed under the [MIT License](LICENSE).

## Credits
- **Weather API:** [WeatherAPI.com](https://www.weatherapi.com/)
- **Bootstrap:** [Bootstrap 4](https://getbootstrap.com/)
- **Flask & SQLAlchemy:** [Flask](https://flask.palletsprojects.com/) & [SQLAlchemy](https://www.sqlalchemy.org/)
- **PM Accelerator:** [LinkedIn](https://www.linkedin.com/company/product-manager-accelerator/)

---

**Thank you for checking out this Weather App!**  
Feel free to open issues or submit pull requests if you have suggestions or improvements.




