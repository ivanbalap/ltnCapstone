from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarMake, CarModel, CarDealer, DealerReview
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_by_id, get_dealers_by_state
from .restapis import get_dealer_reviews_from_cf, post_request
from django.views import generic
import uuid
# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {}
    return render(request, 'djangoapp/contact_us.html', context)

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)


# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context={}
    context["dealerships"]=[]
    if request.method == "GET":
        url = "http://localhost:3000/api/dealership"
        dealers = get_dealers_from_cf(url)
        if dealers:
            for dealer in dealers:
                context["dealerships"].append(dealer)
        
        # dealers = get_dealer_by_id(url,dealerId=10)
        # if dealers:
        #     for dealer in dealers:
        #         context["dealerships"].append(dealer)
        
        # dealers = get_dealers_by_state(url,state="Texas")
        # if dealers:
        #     for dealer in dealers:
        #         context["dealerships"].append(dealer)
        
        return render(request, 'djangoapp/index.html', context=context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context={}
    context["dealer"]=get_dealer_by_id("http://localhost:3000/api/dealership",dealerId=dealer_id)
    if (context["dealer"]) and (len(context["dealer"]) > 0):
        context["dealer"]=context["dealer"][0]
        context["dealerDetails"]=[]
        if request.method == "GET":
            url = "http://localhost:5000/api/review"
            dealerDetails = get_dealer_reviews_from_cf(url, dealer_id)
            if dealerDetails:
                for dealerDetail in dealerDetails:
                    context["dealerDetails"].append(dealerDetail)
    return render(request, 'djangoapp/dealer_details.html', context=context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
# ...
    user = request.user

    if user.is_authenticated:
        context = {}
        context["dealer"]=get_dealer_by_id("http://localhost:3000/api/dealership",dealerId=dealer_id)
        if (context["dealer"]) and (len(context["dealer"]) > 0):
            context["dealer"]=context["dealer"][0]
            context["cars"]=[]
            cars=CarModel.objects.filter(car_model_dealer_id=dealer_id)
            for car in cars:
                context["cars"].append(car)
            # print(context["cars"])
            if request.method == 'GET':
                return render(request, 'djangoapp/add_review.html', context)
            elif request.method == 'POST':
                review = dict()
                # json_payload = dict()
                review["id"] = str(uuid.uuid4())
                review["time"] = datetime.utcnow().isoformat()
                review["dealership"] = dealer_id
                review["review"] = request.POST['review_content']
                review["name"] = f"{request.user.first_name} {request.user.last_name}"
                # print(request.POST)
                if 'purchasecheck' in request.POST:
                    review["purchase"] = "True"
                    review["purchase_date"] = request.POST['purchasedate']
                    # print(CarModel.objects.filter(id=request.POST['car']))
                    car=CarModel.objects.filter(id=request.POST['car'])[0]
                    review["car_make"] = car.car_make.car_make_name
                    review["car_model"] = car.car_model_name
                    review["car_year"] = car.car_model_year.strftime("%Y")
                else:
                    review["purchase"] = "False"
                    review["purchase_date"] = ""
                    review["car_make"] = ""
                    review["car_model"] = ""
                    review["car_year"] = ""
                # review["another"] = "field"
                url="http://localhost:5000/api/review"
                # json_payload["review"]=review
                post_request(url=url,json_payload=review, dealerId=dealer_id)
                # print(review)
                # return get_dealer_details(request, dealer_id)
                return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            return get_dealerships(request)
    else:
        return render(request, 'djangoapp/login.html', context={'message':"please login to add review"})
