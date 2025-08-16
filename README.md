[README.md](https://github.com/user-attachments/files/21813633/README.md)
# 🦟 Dengue Predictor

A **Django-based web application** that predicts the likelihood of a patient having **Dengue Fever** using a trained machine learning model.  
In addition to predictions, the platform provides essential information such as **symptoms, prevention tips, chatbot (prototype), news section, and dashboard (future expansion)**.  

---

## 📑 Table of Contents
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Running the Application](#-running-the-application)
- [Usage](#-usage)
- [Future Roadmap](#-future-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Features
- 🔮 **Dengue Prediction** – Predicts "Positive" or "Negative" using patient vitals.  
- 🩺 **Symptoms Information** – Static page listing dengue symptoms.  
- 🛡️ **Prevention Tips** – Guidance on avoiding dengue infection.  
- 💬 **Chatbot (prototype)** – Simple informational chatbot (planned for expansion).  
- 📰 **News Section (prototype)** – Dengue-related articles (planned for integration).  
- 📊 **Dashboard (prototype)** – Placeholder for future dengue data visualization.  

---

## 🛠️ Tech Stack
- **Backend**: Python, Django  
- **Frontend**: HTML, CSS, JavaScript  
- **Machine Learning**: `scikit-learn`, `joblib`, `numpy`  
- **Database**: SQLite3  
- **Architecture**: Django’s **Model-View-Template (MVT)**  

---

## 📂 Project Structure
```
Dengue_Predictor/
├── db.sqlite3
├── manage.py
├── dengue_website/                # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── predictions/                   # Core app
    ├── views.py                   # Views (prediction, info pages)
    ├── models.py                  # DB models (minimal for MVP)
    ├── models/                    # ML models & scalers
    │   ├── random_forest_model.pkl
    │   ├── best_rf_model.joblib
    │   ├── scaler.pkl
    │   └── scaler.joblib
    ├── templates/predictions/     # HTML templates
    │   ├── index.html             # Landing + prediction form
    │   ├── dengue_symptoms.html
    │   ├── dengue_prevention.html
    │   ├── dengue_chatbot.html
    │   ├── dengue_news.html
    │   └── dengue_dashboard.html
    ├── static/                    # CSS, JS, images
    │   ├── styles/                # Styling for pages
    │   ├── scripts/               # JavaScript utilities
    │   └── images/                # Assets
    └── tests.py
```

---

## ⚡ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/kap432/Dengue_Predictor.git
   cd Dengue_Predictor
   ```

2. **Create a virtual environment & activate it**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

---

## 🚀 Running the Application
Start the Django development server:
```bash
python manage.py runserver
```
Visit the app at: **http://127.0.0.1:8000/**  

---

## 📖 Usage
1. Open the homepage.  
2. Fill out the prediction form with parameters like:  
   - Heart Rate  
   - Blood Pressure (Systolic & Diastolic)  
   - Hemoglobin, Platelet Count, WBC Count  
   - Urea, Sodium, Potassium  
3. Submit to see prediction results (Positive/Negative + probability).  
4. Explore **Symptoms** and **Prevention** pages for health info.  

---

## 🔮 Future Roadmap
- 🤖 **Chatbot Expansion** – AI-driven chatbot for dengue Q&A.  
- 📰 **Live News Feed** – Auto-fetch dengue-related articles.  
- 📊 **Interactive Dashboard** – Visualize cases, trends, and hotspots.  
- 🔐 **User Authentication** – Secure login and patient record history.  
- ☁️ **Deployment** – Host on Heroku / PythonAnywhere for public use.  

---

## 🤝 Contributing
Contributions are welcome!  
1. Fork this repo  
2. Create a new branch (`feature/xyz`)  
3. Commit your changes  
4. Push to your fork & submit a PR  

---

## 📜 License
This project is licensed under the **MIT License** – feel free to use and modify.  
  
