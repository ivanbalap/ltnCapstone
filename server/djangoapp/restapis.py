import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print(f"GET from {url}")
    try:
        print(url, kwargs)
        response = requests.get(
            url,
            headers=(),
            params=kwargs)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print(f"With staus {status_code}")
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    # - Call get_request() with specified arguments
    # - Parse JSON results into a CarDealer object list
    results = []
    json_result = get_request(url)
    if json_result:
        # dealers = json_result["rows"]
        # for dealer in dealers:
        for dealer in json_result:
            # dealer_doc = dealer["doc"]
            # dealer_doc = dealer
            dealer_obj = CarDealer(
                address = dealer["address"],
                city = dealer["city"],
                full_name = dealer["full_name"],
                id = dealer["id"],
                lat = dealer["lat"],
                long = dealer["long"],
                short_name = dealer["short_name"],
                st = dealer["st"],
                state = dealer["state"],
                zip = dealer["zip"]
            )
            results.append(dealer_obj)
    return results


def get_dealer_by_id(url, dealerId):
    results = []
    json_result = get_request(url,id=dealerId)
    if json_result:
        for dealer in json_result:
            dealer_obj = CarDealer(
                address = dealer["address"],
                city = dealer["city"],
                full_name = dealer["full_name"],
                id = dealer["id"],
                lat = dealer["lat"],
                long = dealer["long"],
                short_name = dealer["short_name"],
                st = dealer["st"],
                state = dealer["state"],
                zip = dealer["zip"]
            )
            results.append(dealer_obj)
    return results

def get_dealers_by_state(url, state):
    results = []
    json_result = get_request(url,state=state)
    if json_result:
        for dealer in json_result:
            dealer_obj = CarDealer(
                address = dealer["address"],
                city = dealer["city"],
                full_name = dealer["full_name"],
                id = dealer["id"],
                lat = dealer["lat"],
                long = dealer["long"],
                short_name = dealer["short_name"],
                st = dealer["st"],
                state = dealer["state"],
                zip = dealer["zip"]
            )
            results.append(dealer_obj)
    return results

def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url,id=dealerId)
    if json_result:
        for review in json_result:
            dealer_review_obj = DealerReview(
                dealership = review["dealership"],
                purchase = review["purchase"],
                name = review["name"],
                id = review["id"],
                review = review["review"],
                purchase_date = review["purchase_date"],
                car_make = review["car_make"],
                car_model = review["car_model"],
                car_year = review["car_year"],
                # sentiment = review["sentiment"]
            )
            results.append(dealer_review_obj)
    return results
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



