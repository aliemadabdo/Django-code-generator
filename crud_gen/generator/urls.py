from django.urls import path, include
from .views import *
app_name = 'generator'
urlpatterns = [
    # Define your app's URLs here
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('add_model/', add_model, name='add_model'),
    path('add_model_field/', add_model_field, name='add_model_field'),
]