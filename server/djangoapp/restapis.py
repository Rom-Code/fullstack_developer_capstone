"""
This module provides functions for interacting with external APIs related
to car reviews and sentiment analysis.

Functions:
 - get_request(endpoint, **kwargs): Sends a GET request to
the specified endpoint with optional query parameters.
 - analyze_review_sentiments(text): Analyzes the sentiment of
the provided text using the sentiment analyzer service.
 - post_review(data_dict): Posts a review to the backend service.

The module utilizes the `requests` library for HTTP operations and `dotenv`
to manage environment variables.
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve backend and sentiment analyzer URLs from environment variables
backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/"
)


def get_request(endpoint, **kwargs):
    """
    Perform a GET request to the specified endpoint with optional parameters.

    Args:
    endpoint (str): The endpoint to send the GET request to.
    **kwargs: Optional query parameters to include in the request.

    Returns:
        dict: The JSON response from the server.

    Raises:
    requests.RequestException: If the request fails or
    the response cannot be parsed.
    """
    params = ""
    if(kwargs):
        for key,value in kwargs.items():
            params=params+key+"="+value+"&"

    request_url = backend_url+endpoint+"?"+params

    print("GET from {} ".format(request_url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except:
        # If any error occurs
        print("Network exception occurred")


def analyze_review_sentiments(text):
    """
    Analyze the sentiment of the given text using
    the sentiment analyzer service.

    Args:
        text (str): The review text to analyze.

    Returns:
        dict: The sentiment analysis result.

    Raises:
    requests.RequestException: If the request fails or
    the response cannot be parsed.
    """
    request_url = sentiment_analyzer_url+"analyze/"+text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")


def post_review(data_dict):
    request_url = backend_url+"/insert_review"
    try:
        response = requests.post(request_url,json=data_dict)
        print(response.json())
        return response.json()
    except:
        print("Network exception occurred")
