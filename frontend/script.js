const cityInput = document.getElementById("cityInput");
const searchBtn = document.getElementById("searchBtn");

const weatherCard = document.getElementById("weatherCard");
const welcomeMessage = document.getElementById("welcomeMessage");

const loading = document.getElementById("loading");
const errorMessage = document.getElementById("errorMessage");


// Search button
searchBtn.addEventListener("click", searchWeather);


// Press Enter to search
cityInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        searchWeather();
    }
});


// Search weather
async function searchWeather() {

    const city = cityInput.value.trim();

    // Empty input
    if (city === "") {
        errorMessage.textContent = "Please enter a city name.";
        weatherCard.style.display = "none";
        return;
    }

    // Reset messages
    errorMessage.textContent = "";
    loading.style.display = "block";
    weatherCard.style.display = "none";

    // Disable button while loading
    searchBtn.disabled = true;
    searchBtn.textContent = "Searching...";

    try {

        // Use the deployed FastAPI backend
        const response = await fetch(
            `/weather/${encodeURIComponent(city)}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "City not found. Please try another city."
            );
        }


        // Update city
        document.getElementById("cityName").textContent = data.city;

        document.getElementById("country").textContent = data.country;


        // Update temperature
        document.getElementById("temperature").textContent =
            Number(data.temperature).toFixed(1);

        document.getElementById("temperatureDetail").textContent =
            Number(data.temperature).toFixed(1);


        // Update humidity
        document.getElementById("humidity").textContent =
            data.humidity;


        // Update wind speed
        document.getElementById("windSpeed").textContent =
            Number(data.wind_speed).toFixed(1);


        // Update description
        document.getElementById("description").textContent =
            data.description;


        // Update weather icon
        const weatherIcon = document.getElementById("weatherIcon");

        if (weatherIcon) {
            weatherIcon.textContent =
                getWeatherIcon(data.description);
        }


        // Show weather card
        welcomeMessage.style.display = "none";
        weatherCard.style.display = "block";


        // Refresh history
        // Load forecast
await loadForecast(city);

// Refresh history
await loadHistory();
    }

    catch (error) {

        weatherCard.style.display = "none";

        errorMessage.textContent =
            error.message || "Unable to get weather information.";

    }

    finally {

        loading.style.display = "none";

        // Enable button again
        searchBtn.disabled = false;
        searchBtn.textContent = "Search";
    }
}


// Weather icon based on description
function getWeatherIcon(description) {

    const weather = description.toLowerCase();


    if (weather.includes("thunderstorm")) {
        return "⛈️";
    }


    if (
        weather.includes("rain") ||
        weather.includes("drizzle")
    ) {
        return "🌧️";
    }


    if (weather.includes("snow")) {
        return "❄️";
    }


    if (
        weather.includes("mist") ||
        weather.includes("fog") ||
        weather.includes("haze")
    ) {
        return "🌫️";
    }


    if (weather.includes("cloud")) {
        return "☁️";
    }


    if (weather.includes("clear")) {
        return "☀️";
    }


    return "🌤️";
}


// Load weather search history
async function loadHistory() {

    const historyList =
        document.getElementById("historyList");

    try {

        const response =
            await fetch("/weather/history/all");


        if (!response.ok) {
            throw new Error("Could not load history");
        }


        const history = await response.json();


        if (history.length === 0) {

            historyList.innerHTML =
                '<p class="history-empty">No searches yet.</p>';

            return;
        }


        historyList.innerHTML = "";


        history.forEach(item => {

            const historyItem =
                document.createElement("div");

            historyItem.className = "history-item";


            historyItem.innerHTML = `
                <div>
                    <div class="history-city">
                        ${item.city}
                    </div>

                    <div class="history-country">
                        ${item.country}
                    </div>
                </div>

                <div class="history-weather">
                    <div class="history-temperature">
                        ${Number(item.temperature).toFixed(1)}°C
                    </div>

                    <div class="history-description">
                        ${item.description}
                    </div>
                </div>
            `;


            historyList.appendChild(historyItem);
        });

    }

    catch (error) {

        console.error("History error:", error);

        historyList.innerHTML =
            '<p class="history-empty">Unable to load history.</p>';
    }
}


// Clear all weather history
document
    .getElementById("clearHistoryBtn")
    .addEventListener("click", async () => {

        const confirmed = confirm(
            "Are you sure you want to clear all search history?"
        );


        if (!confirmed) {
            return;
        }


        try {

            const response =
                await fetch(
                    "/weather/history/clear",
                    {
                        method: "DELETE"
                    }
                );


            if (!response.ok) {
                throw new Error(
                    "Failed to clear history"
                );
            }


            // Reload history from database
            await loadHistory();

        }

        catch (error) {

            console.error(
                "Clear history error:",
                error
            );

            alert(
                "Unable to clear history. Please try again."
            );
        }
    });


// Load history when page opens
loadHistory();

async function loadForecast(city) {

    const forecastSection =
        document.getElementById("forecastSection");

    const forecastContainer =
        document.getElementById("forecastContainer");

    try {

        const response = await fetch(
            `/weather/forecast/${encodeURIComponent(city)}`
        );

        if (!response.ok) {
            throw new Error("Unable to load forecast.");
        }

        const data = await response.json();
        console.log(data);

        forecastContainer.innerHTML = "";

        data.forecast.forEach(day => {

            const card = document.createElement("div");

            card.className = "forecast-card";

            card.innerHTML = `
                <h3>${day.date}</h3>

                <div class="forecast-temp">
                    ${Number(day.temperature).toFixed(1)}°C
                </div>

                <div>
                    💧 ${day.humidity}%
                </div>

                <div>
                    💨 ${Number(day.wind_speed).toFixed(1)} m/s
                </div>

                <div class="forecast-desc">
                    ${day.description}
                </div>
            `;

            forecastContainer.appendChild(card);
        });

        forecastSection.style.display = "block";

    }

    catch (error) {

        console.error(error);

        forecastSection.style.display = "none";
    }
}