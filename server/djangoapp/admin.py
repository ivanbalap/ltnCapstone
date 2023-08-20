from django.contrib import admin
from .models import CarMake, CarModel, CarDealer, DealerReview

# Register your models here.
# admin.site.register(CarMake)
# admin.site.register(CarModel)

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = [
        'car_model_name',
        'car_model_dealer_id',
        'car_model_type',
        'car_model_year'
    ]
    # list_filter = ['pub_date']
    # search_fields = ['name', 'description']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines=[CarModelInline]
    list_display = ['car_make_name','car_make_desc']

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)