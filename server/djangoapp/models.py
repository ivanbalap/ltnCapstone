from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    car_make_name = models.CharField(null=False, max_length=100)
    car_make_desc = models.CharField(null=True, max_length=1000)
    def __str__(self):
        return f"Car Make: {self.car_make_name}"


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    OTHER='other'
    SEDAN='sedan'
    SUV='SUV'
    WAGON='WAGON'
    CAR_TYPE_CHOICES=[
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'WAGON'),
        (OTHER,'Other')]
    car_model_name = models.CharField(null=False, max_length=100)
    car_make = models.ForeignKey(CarMake, null=False, on_delete=models.CASCADE)
    car_model_dealer_id = models.IntegerField(null=False)
    car_model_type = models.CharField(null=False, max_length=100,choices=CAR_TYPE_CHOICES,default=OTHER)
    car_model_year = models.DateField(null=True)
    def __str__(self):
        return "Car model name: " + self.car_model_name + ", " + \
                "Car model dealer id: " + str(self.car_model_dealer_id) + ", " + \
                "Car model type: " + self.car_model_type + ", " + \
                "Car model year: " + str(self.car_model_year)
    
# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, state, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer state
        self.state = state
        # Dealer zip
        self.zip = zip
    
    def __str__(self):
        return f"Dealer name: {self.full_name}"


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, id, sentiment=None):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return f"Review for {self.car_make} - {self.car_model}: {self.review} with sentiment {self.sentiment}"