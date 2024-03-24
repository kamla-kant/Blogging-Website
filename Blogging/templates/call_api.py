"""
This is how we get data from REST API
inside the program
"""

import requests

my_rest_api_endpoint = "http://127.0.0.1:6060/postdata"

my_api_response = requests.get(my_rest_api_endpoint)
my_api_response = my_api_response.json()
print("my_api_response : ", my_api_response)