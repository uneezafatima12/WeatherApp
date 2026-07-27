# 🌤️ Weather App

A full-stack weather application that allows users to search for the current weather of any city and view their weather search history.

## ✨ Features

- Search weather by city name
- Current temperature
- Humidity
- Wind speed
- Weather description
- Dynamic weather icons
- Country information
- Weather search history
- Clear search history
- Loading indicator
- Error handling
- Responsive design
- MySQL database integration

## 🛠️ Technologies Used

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- PyMySQL
- HTTPX
- python-dotenv

### Database
- MySQL
- XAMPP

### API
- OpenWeather API

## 📁 Project Structure

```text
WeatherApp/
│
├── backend/
│   ├── routers/
│   │   └── weather.py
│   ├── database.py
│   ├── models.py
│   ├── main.py
│   └── .env
│
├── frontend/
│   ├── images/
│   │   └── weather-bg.jpg
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── .gitignore
├── requirements.txt
└── README.md



```

Then paste this:

````markdown
## ⚙️ Setup

### 1. Create the Database

Start **Apache** and **MySQL** in XAMPP.

Open phpMyAdmin and create a database named:

```text
weather_app
```

The `weather_history` table will be created automatically when the application starts.

### 2. Create Environment Variables

Create:

```text
backend/.env
```

Add:

```env
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
DB_NAME=weather_app

OPENWEATHER_API_KEY=YOUR_API_KEY
```

Replace `YOUR_API_KEY` with your own OpenWeather API key.

**Never upload your `.env` file or API key to GitHub.**

### 3. Install Dependencies

Create a virtual environment:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

Install the required packages:

```powershell
pip install -r requirements.txt
```

### 4. Run the Application

From the WeatherApp folder, run:

```powershell
uvicorn backend.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## 🔌 API Endpoints

### Current Weather

```text
GET /weather/{city}
```

Example:

```text
GET /weather/Lahore
```

### Weather History

```text
GET /weather/history/all
```

### Clear History

```text
DELETE /weather/history/clear
```

## 🗄️ Database

Weather searches are stored in the MySQL `weather_history` table.

The table stores:

- City
- Country
- Temperature
- Humidity
- Wind speed
- Weather description
- Search date and time

## 🔐 Security

Sensitive information such as the OpenWeather API key and database credentials are stored in environment variables.

The `.env` file is excluded from GitHub using `.gitignore`.

## 👩‍💻 Author

**Uneeza Fatima**

Full-Stack Weather Application