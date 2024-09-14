"""
This module contains views for user authentication, registration,
dealerships, dealer reviews, and review submission in the Django application.
"""

import json
import logging
from django.shortcuts import render
#from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review
from datetime import datetime
from django.contrib import messages

# Get an instance of a logger
logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    """
    Handle user login requests.
    """
    data = json.loads(request.body)
    username = data.get('userName')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    response_data = {"userName": username}
    if user:
        login(request, user)
        response_data["status"] = "Authenticated"
    return JsonResponse(response_data)
"""
@csrf_exempt
def logout_request(request):
    
    Handle user logout requests.
  
    user = request.user
    logout(request)
    return JsonResponse({"userName": user.username})
"""
@csrf_exempt
def logout_request(request):
    """
    Handle user logout requests.
    """
    if request.user.is_authenticated:
        # Log out the user
        logout(request)
        response_data = {"userName": "", "status": "Logged out"}
    else:
        response_data = {"userName": "", "status": "Not logged in"}
    
    return JsonResponse(response_data)

@csrf_exempt
def registration(request):
    """
    Handle user registration requests.
    """
    data = json.loads(request.body)
    username = data.get('userName')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')
    if User.objects.filter(username=username).exists():
        return JsonResponse({"userName": username,
                             "error": "Already Registered"})
    # Create new user
    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
        email=email
    )
    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


#Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})


def get_dealer_details(request, dealer_id):
    """
    Get details of a specific dealer.
    """
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_reviews(request, dealer_id):
    """
    Get reviews for a specific dealer and analyze sentiment.
    """
    # if dealer id has been provided
    if(dealer_id):
        endpoint = "/fetchReviews/dealer/"+str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status":200,"reviews":reviews})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})


  
def get_cars(request):
    """
    Get a list of car models and makes.
    """
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})


def add_review(request):
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})

    return JsonResponse({"status": 403, "message": "Unauthorized"})
