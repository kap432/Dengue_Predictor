from django.shortcuts import render
import pickle
import numpy as np

def landing_page(request):
    return render(request, 'predictions/index.html')

def dengue_symptoms(request):
    return render(request, 'predictions/dengue_symptoms.html')

def predict_view(request):
    return render(request, 'predictions/index.html')

# Load the trained model (ensure the path is correct)
with open('predictions/models/dengue_model.pkl', 'rb') as file:
    model = pickle.load(file)

def predict_dengue(request):
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

        # Make the prediction using the loaded model
        prediction = model.predict(input_features)
        prediction = "Dengue Positive" if prediction[0] == 1 else "Dengue Negative"

    # Render the form with the prediction result (if any)
    return render(request, 'predictions/index.html', {'prediction': prediction})

