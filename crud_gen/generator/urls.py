from django.urls import path, include
from .views import *
app_name = 'generator'
urlpatterns = [
    # Define your app's URLs here
    path('', home, name='home'),
    path('add_field/', add_field, name='add_field'),
    path('add_model/', add_model, name='add_model'),
    path('add_app/', add_app, name='add_app'),

        ]