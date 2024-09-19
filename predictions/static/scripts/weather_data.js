// API details
const API_KEY = 'f40d6e15bfbc85ea2a3bb4de9b55267e';
const LATITUDE = 18.465540;
const LONGITUDE = -66.105736;

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
        avgTempK += main.temp + 273.15;
        dewPointTempK += calculateDewPoint(main.temp, humidity) + 273.15;
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
