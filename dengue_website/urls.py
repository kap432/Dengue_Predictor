"""
URL configuration for dengue_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from predictions import views

urlpatterns = [
    path('', views.landing_page, name='index'),
    path('predict/', views.predict_dengue, name='predict_dengue'),
    path('dengue-symptoms/', views.dengue_symptoms, name='dengue_symptoms'),
    path('dengue-preventions/', views.dengue_preventions, name='dengue_preventions'),
]
