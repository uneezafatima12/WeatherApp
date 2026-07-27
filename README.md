# 🌦️ Weather App

A full-stack Weather Application built with **FastAPI**, **MySQL**, **HTML**, **CSS**, and **JavaScript**. The application allows users to search for real-time weather information, view a 5-day forecast, manage search history, and export weather history as a CSV file.

---

## 🚀 Features

- 🌤️ Search current weather by city
- 📅 View 5-day weather forecast
- 🗄️ Store weather search history in MySQL
- 📖 View previous weather searches
- ✏️ Update weather history records
- 🗑️ Delete individual weather history records
- 🧹 Clear all weather history
- 📄 Export weather history as CSV
- ⚡ FastAPI REST API
- 🎨 Responsive frontend using HTML, CSS, and JavaScript

---

## 🛠️ Technologies Used

### Backend
- FastAPI
- SQLAlchemy
- MySQL
- PyMySQL
- HTTPX
- Python
- Uvicorn

### Frontend
- HTML5
- CSS3
- JavaScript

### Deployment
- Railway (Backend)
- Aiven MySQL (Database)

### External API
- OpenWeather API

---

## 📂 Project Structure

```
WeatherApp/
│
├── backend/
│   ├── routes/
│   ├── database.py
│   ├── models.py
│   ├── main.py
│   └── .env
│
├── static/
│   ├── style.css
│   └── script.js
│
├── templates/
│   └── index.html
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/your-username/WeatherApp.git
cd WeatherApp
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create a `.env` file

```env
OPENWEATHER_API_KEY=your_api_key
DATABASE_URL=your_database_url
```

### Run the application

```bash
uvicorn backend.main:app --reload
```

Open your browser:

```
http://127.0.0.1:8000
```

API Documentation:

```
http://127.0.0.1:8000/docs
```

---

## 📌 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/weather/{city}` | Get current weather |
| GET | `/weather/forecast/{city}` | Get 5-day forecast |
| GET | `/weather/history/all` | Get weather history |
| PUT | `/weather/history/{history_id}` | Update weather history |
| DELETE | `/weather/history/{history_id}` | Delete weather history record |
| DELETE | `/weather/history/clear` | Clear all history |
| GET | `/weather/history/export/csv` | Export history as CSV |

---

## 📸 Screenshots

Add screenshots of your application here.

Example:

```
screenshots/
├── home.png
├── search.png
├── history.png
└── forecast.png
```

---

## 📈 Future Improvements

- User authentication
- Weather icons from OpenWeather
- Search by current location
- Charts for temperature trends
- Dark mode
- Favourite cities
- Pagination for history

---

## 👩‍💻 Author

**Uneeza Fatima**

GitHub: https://github.com/uneenzafatima12

---

## 📄 License

This project is for educational and portfolio purposes.