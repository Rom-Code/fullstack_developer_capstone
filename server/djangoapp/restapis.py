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
        requests.RequestException: If the request fails or the response cannot be parsed.
    """
    params = "&".join(f"{key}={value}" for key, value in kwargs.items())
    request_url = f"{backend_url}{endpoint}?{params}"

    print(f"GET from {request_url}")
    try:
        response = requests.get(request_url, timeout=10)  # Added timeout
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        return response.json()
    except requests.RequestException as e:
        print(f"Error during GET request: {e}")
        raise  # Re-raise the exception for higher-level handling

def analyze_review_sentiments(text):
    """
    Analyze the sentiment of the given text using the sentiment analyzer service.

    Args:
        text (str): The review text to analyze.

    Returns:
        dict: The sentiment analysis result.

    Raises:
        requests.RequestException: If the request fails or the response cannot be parsed.
    """
    request_url = f"{sentiment_analyzer_url}analyze/{text}"
    try:
        response = requests.get(request_url, timeout=10)  # Added timeout
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        return response.json()
    except requests.RequestException as e:
        print(f"Error during sentiment analysis: {e}")
        return {"error": str(e)}  # Return an error message

def post_review(data_dict):
    """
    Post a review to the backend service.

    Args:
        data_dict (dict): The review data to post.

    Returns:
        dict: The server's response.

    Raises:
        requests.RequestException: If the request fails or the response cannot be parsed.
    """
    request_url = f"{backend_url}/insert_review"
    try:
        response = requests.post(
            request_url,
            json=data_dict,
            timeout=10  # Added timeout
        )
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        print(response.json())
        return response.json()
    except requests.RequestException as e:
        print(f"Error during POST request: {e}")
        return {"error": str(e)}  # Return an error message
