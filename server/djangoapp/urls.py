"""
This module defines the URL patterns for the Django application.

It includes routes for login, logout, registration,
dealer details, reviews, and adding reviews.
"""

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

APP_NAME = 'djangoapp'

urlpatterns = [
    path(route='login', view=views.login_user, name='login'),
    path('logout/', view=views.logout_request, name='logout'),
    path('register', views.registration, name='register'),
    #path('get_cars/', views.get_cars, name='get_cars'),
    path(route='get_cars', view=views.get_cars, name ='getcars'),
    path('get_dealers/', views.get_dealerships,
         name='get_dealers'),
    path('get_dealers/<str:state>/', views.get_dealerships,
         name='get_dealers_by_state'),
    path('dealer/<int:dealer_id>/', views.get_dealer_details,
         name='dealer_details'),
    path('reviews/dealer/<int:dealer_id>/',
         views.get_dealer_reviews, name='dealer_reviews'),
    path('add_review/', views.add_review, name='add_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
