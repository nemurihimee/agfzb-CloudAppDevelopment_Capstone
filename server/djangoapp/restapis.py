from urllib import response
import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                    auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, api_key =None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if api_key: 
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)

    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    response = requests.post(url, params=kwargs, json=json_payload)
    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        for _ in json_result:
            print(_)
        dealers = json_result['body']["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function

def get_dealer_reviews_from_cf (url, dealer_id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,id= dealer_id)
    if json_result:
        # Get the row list in JSON as dealers
        for _ in json_result:
            print(_)
        reviews = json_result['body']['data']['docs']
        # For each dealer object
        for review in reviews:            
            review_obj = DealerReview( id=review['_id'], dealership = review['dealership'], name=review.get('name') ,purchase= review['purchase'],
            review=review['review'],purchase_date = review.get('purchase_date'), car_make = review.get('car_make'),car_model = review.get('car_model'),
            car_year = review.get('car_year'),sentiment = analyze_review_sentiments(review['review']))   
            results.append(review_obj)        

    return results       

# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_by_id_from_cf(url, dealerId):
     
    dealer_obj =None
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId = dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        for _ in json_result:
            print(_)
        dealers = json_result['body']["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
             

    return dealer_obj

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(text):
    
    url ="https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/69ae9b45-ba31-4a16-bb7d-ce0e7a9def30"
    api_key="w-LI3PoSO6ZlgrAjGR-ojLdNaiovkmqbcPcYt0GHZ517"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=authenticator
    )
    natural_language_understanding.set_service_url(url)

    response = natural_language_understanding.analyze(text= text, language='en',
         features=Features( sentiment=SentimentOptions())).get_result()       
   
    
    return response["sentiment"]["document"]['label']


