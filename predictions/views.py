from django.shortcuts import render
import joblib
import numpy as np
from django.http import JsonResponse

def landing_page(request):
    return render(request, 'predictions/index.html')

def dengue_symptoms(request):
    return render(request, 'predictions/dengue_symptoms.html')

def predict_view(request):
    return render(request, 'predictions/index.html')

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


