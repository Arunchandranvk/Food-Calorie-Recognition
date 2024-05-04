from django.urls import path
from .views import *


urlpatterns = [
    path("signup/",UserCreationView.as_view(),name="signup"),
    path('login/',CustomAuthToken.as_view(),name="log"),
    path('checkcalorie/',CaloriesAdvisorAPI,name='cal')
]
