from django.shortcuts import render
import joblib
import numpy as np
from django.http import JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import pandas as pd

# Load the model and scaler
model1 = joblib.load('predictions/models/best_rf_model.joblib')
scaler1 = joblib.load('predictions/models/scaler.joblib')

def landing_page(request):
    return render(request, 'predictions/index.html')

def dengue_symptoms(request):
    return render(request, 'predictions/dengue_symptoms.html')

def predict_view(request):
    return render(request, 'predictions/index.html')

def dengue_preventions(request):
    return render(request, 'predictions/dengue_prevention.html')

def dengue_chatbot(request):
    return render(request, 'predictions/dengue_chatbot.html')

# Load the trained model and scaler (ensure paths are correct)
model = joblib.load('predictions/models/random_forest_model.pkl')
scaler = joblib.load('predictions/models/scaler.pkl')

def predict_dengue(request):
    probability = None
    prediction = None

    if request.method == 'POST':
        # Get the form data
        heart_rate = float(request.POST.get('heart_rate', 0))
        blood_pressure_systolic = float(request.POST.get('blood_pressure1', 0))
        blood_pressure_diastolic = float(request.POST.get('blood_pressure2', 0))
        haemoglobin = float(request.POST.get('haemoglobin', 0))
        platelet_count = float(request.POST.get('platelet_count', 0))
        wbc_count = float(request.POST.get('wbc_count', 0))
        urea = float(request.POST.get('urea', 0))
        sodium = float(request.POST.get('sodium', 0))
        potassium = float(request.POST.get('potassium', 0))

        # Create the feature array for prediction
        input_features = np.array([[heart_rate, blood_pressure_systolic, blood_pressure_diastolic, haemoglobin, platelet_count, wbc_count, urea, sodium, potassium]])

       # Standardize the features using the same scaler
        input_features = scaler.transform(input_features)

        # Make the prediction using the loaded model
        prediction_proba = model.predict_proba(input_features)
        probability = prediction_proba[0][1]  # Probability of class 1 (Dengue Positive)
        probability_percentage = probability * 100  # Convert probability to percentage
        print(probability_percentage)
        prediction = "Dengue Positive" if probability > 0.5 else "Dengue Negative"

     # Convert probability to percentage
        probability_percentage = round(probability * 100, 2)

        # Return JSON response
        return JsonResponse({
            'prediction': prediction,
            'probability_percentage': probability_percentage
        })
    
    # Render the form if not POST request
    return render(request, 'predictions/index.html')

def dengue_dashboard(request):
    # Render the dengue dashboard page
    return render(request, 'predictions/dengue_dashboard.html')

def dengue_news(request):
    api_key = settings.NEWS_API_KEY  # Make sure to add this key in your settings
    url = f'https://newsapi.org/v2/everything?q=dengue&sources=the-times-of-india&apiKey={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        news_data = response.json()
        
        # Filter articles from Times of India
        articles = [
            {
                'title': article.get('title', 'No title available'),
                'urlToImage': article.get('urlToImage', 'default_image_url'),  # Provide a default image URL if needed
                'publishedAt': article.get('publishedAt', 'No date available'),
                'source': article.get('source', {}).get('name', 'No source available'),
                'description': article.get('description', 'No description available'),
                'url': article.get('url', '#')
            }
            for article in news_data.get('articles', [])
            if article.get('source', {}).get('name') == 'The Times of India' and 'dengue' in article.get('title', '').lower()
        ]
    
    except requests.RequestException as e:
        # Handle errors from the request
        print(f"Error fetching news: {e}")
        articles = []  # Set to empty list or handle as appropriate

    except ValueError as e:
        # Handle errors in decoding JSON
        print(f"Error decoding JSON: {e}")
        articles = []

    context = {
        'articles': articles
    }
    return render(request, 'predictions/dengue_news.html', context)

@csrf_exempt
def weather_data_view(request):
    if request.method == 'POST':
        try:
            # Load the JSON data from the request
            data = json.loads(request.body)
            
            # Prepare the data for prediction
            sample_data = pd.DataFrame({
                'precipitation_amt_mm': [data.get('precipitationAmtMm', 0)],
                'reanalysis_avg_temp_k': [data.get('avgTempK', 0)],
                'reanalysis_dew_point_temp_k': [data.get('dewPointTempK', 0)],
                'reanalysis_max_air_temp_k': [data.get('maxTempK', 0)],
                'reanalysis_min_air_temp_k': [data.get('minTempK', 0)],
                'reanalysis_relative_humidity_percent': [data.get('relativeHumidityPercent', 0)]
            })

            # Scale the sample data
            sample_data_scaled = scaler1.transform(sample_data)
            
            # Make a prediction
            prediction = model1.predict(sample_data_scaled)

            # Print the prediction to the terminal
            print("Predicted total_cases:", prediction[0])
            
            # Return the prediction as JSON
            return JsonResponse({'status': 'success', 'predicted_total_cases': prediction[0]}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f'Error: {e}')
            return JsonResponse({'status': 'error', 'message': 'An error occurred'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
