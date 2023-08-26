import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview

with open("./../functions/.creds.json") as creds:
    param_dict=json.load(creds)

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    # print(kwargs)
    # print(f"GET from {url}")
    # response=requests.get(url)
    # json_data=""
    try:
        # print(url, kwargs)
        if 'api_key' in kwargs:
            # print(kwargs['params'])
            # print(kwargs['api_key'])
            response =  requests.get(
                        url,
                        params=kwargs['params'],
                        headers={'Content-Type': 'application/json'},
                        auth=HTTPBasicAuth('apikey', kwargs['api_key']))
            # status_code = response.status_code
            # print(f"With staus {status_code}")
            # json_data = json.loads(response.text)
        else:
            response = requests.get(
                        url, 
                        headers={'Content-Type': 'application/json'}, 
                        params=kwargs)
            # status_code = response.status_code
            # print(f"With staus {status_code}")
            # json_data = json.loads(response.text)
    except Exception as e:
        print(f"Network exception occurred: {e}")
    status_code = response.status_code
    # print(f"With staus {status_code}")
    json_data = json.loads(response.text)
    # print(f"Reponse: {response.text}")
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    # print("from post request: ")
    # print(kwargs)
    # print(json_payload)
    # print("===================")
    requests.post(url, params=kwargs, json=json_payload)


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
        try:
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
        except Exception as e:
            print(json_result)
            return None
        
def get_dealers_by_state(url, state):
    results = []
    json_result = get_request(url,state=state)
    if json_result:
        try:
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
        except Exception as e:
            print(json_result)
            return None

def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url,id=dealerId)
    # print(f"get dealer reviews: {json_result}")
    if json_result:
        try:
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
                )
                dealer_review_obj.sentiment = analyze_review_sentiments(dealer_review_obj.review)
                results.append(dealer_review_obj)
            return results
        except Exception as e:
            print(json_result)
            return None

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
    params = dict()
    params["text"] = text
    params["version"] = "2022-04-07"
    params["features"] = "sentiment"
    params["return_analyzed_text"] = ""
    json_result = get_request("{}/v1/analyze".format(param_dict["IBM_NLU_URL"]),params=params,api_key=param_dict["IBM_NLU_API_KEY"])
    return json_result["sentiment"]["document"]["label"]


