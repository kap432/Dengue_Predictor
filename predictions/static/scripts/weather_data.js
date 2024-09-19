// API details
const API_KEY = 'f40d6e15bfbc85ea2a3bb4de9b55267e';
const LATITUDE = 18.465540; // San Juan coordinates
const LONGITUDE = -66.105736;

// Initialize map with default location (Mumbai)
var map = L.map('map').setView([19.0760, 72.8777], 10); // Mumbai coordinates

// Add OpenStreetMap tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

// Function to calculate dew point temperature
function calculateDewPoint(tempC, humidity) {
    return tempC - (100 - humidity) / 5;
}

// Fetch weather data from OpenWeatherMap
async function getWeatherData() {
    try {
        const response = await fetch(`https://api.openweathermap.org/data/2.5/forecast?lat=${LATITUDE}&lon=${LONGITUDE}&appid=${API_KEY}&units=metric`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching weather data:', error);
    }
}

// Calculate weekly averages and other data
function calculateWeeklyAverages(data) {
    const weatherList = data.list;
    let precipitationAmtMm = 0;
    let avgTempK = 0;
    let dewPointTempK = 0;
    let maxTempK = Number.MIN_VALUE;
    let minTempK = Number.MAX_VALUE;
    let relativeHumidityPercent = 0;
    let count = 0;

    weatherList.forEach(item => {
        const main = item.main;
        const rain = item.rain || {};
        const humidity = main.humidity || 0;

        precipitationAmtMm += rain["3h"] || 0;
        avgTempK += main.temp + 273.15; // Convert Celsius to Kelvin
        dewPointTempK += calculateDewPoint(main.temp, humidity) + 273.15; // Convert dew point to Kelvin
        maxTempK = Math.max(maxTempK, (main.temp_max || Number.MIN_VALUE) + 273.15);
        minTempK = Math.min(minTempK, (main.temp_min || Number.MAX_VALUE) + 273.15);
        relativeHumidityPercent += humidity;

        count++;
    });

    // Calculate averages
    avgTempK /= count;
    dewPointTempK /= count;
    relativeHumidityPercent /= count;

    return {
        precipitationAmtMm,
        avgTempK,
        dewPointTempK,
        maxTempK,
        minTempK,
        relativeHumidityPercent
    };
}

// Handle button click to fetch and send weather data to backend
document.getElementById('fetch-weather-data').addEventListener('click', async () => {
    const useSanJuan = document.getElementById('san-juan-checkbox').checked;
    
    // Set map view based on checkbox status
    if (useSanJuan) {
        map.setView([LATITUDE, LONGITUDE], 10); // Set view to San Juan
    } else {
        map.setView([19.0760, 72.8777], 10); // Reset view to Mumbai
    }

    const data = await getWeatherData();
    if (data) {
        const weeklyData = calculateWeeklyAverages(data);

        // Send the data to Django backend
        try {
            const response = await fetch('/your-django-endpoint/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')  // CSRF token
                },
                body: JSON.stringify(weeklyData)
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            // Display prediction result
            const result = await response.json();
            if (result.status === 'success') {
                document.getElementById('prediction_result').textContent = `Predicted total cases: ${result.predicted_total_cases}`;

                // Add a red circle marker for predicted cases
                const predictedCases = result.predicted_total_cases;
                const radius = Math.max(predictedCases * 5, 50); // Scale radius based on cases
                const circle = L.circle([LATITUDE, LONGITUDE], {
                    color: 'red',
                    fillColor: '#f03',
                    fillOpacity: 0.5,
                    radius: radius // Set radius based on cases
                }).addTo(map);

                // Bind popup to circle
                circle.bindPopup(`Predicted cases: ${predictedCases}`).openPopup();
            } else {
                console.error('Error in prediction:', result.message);
            }
        } catch (error) {
            console.error('Error sending data to backend:', error);
        }
    }
});

// Function to get the CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
