# Weather App

A Django-based web application that displays weather information for cities.

## Features

- Fetches weather data from the OpenWeatherMap API.
- Allows users to filter weather conditions for cities.
- Displays weather information for selected cities.
- Supports Docker for easy deployment.

## Requirements

- Python 3.10 or higher
- Docker (optional)

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/thao-ng11/Horizon/weather-app.git
   cd weather-app
 
2. Create a virtual environment (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   
4. Create a .env file in the project root directory and define the following environment variables:

   ```bash
   OPENWEATHERMAP_API_KEY=your-api-key
   GOOGLE_SHEETS_API_KEY_PATH=path-to-creds.json
   
 - OPENWEATHERMAP_API_KEY: Your OpenWeatherMap API key.
 - GOOGLE_SHEETS_API_KEY_PATH: Path to the creds.json file for Google Sheets API access.
 
5. Run the initial database migration:

   ```bash
   python manage.py migrate
   
6. Load city data from Google Sheets:

   ```bash
   python manage.py data
 
 - This command fetches city data from the configured Google Sheets document and saves it to the database.
 
7. Start the development server:

   ```bash
   python manage.py data

- The application should now be running at http://localhost:8000.

8. Docker Deployment:

If you prefer running the application using Docker and docker-compose, follow these steps:

 1. Modify the docker-compose.yml file:
  - Replace user-name, password, and db-name in the DATABASE_URL environment variable with your PostgreSQL credentials.
  - Optionally, adjust the port mapping if desired.
 2. Build and run the Docker containers:


    ```bash
    docker-compose up -d

- The application should now be running at http://localhost:8000.
