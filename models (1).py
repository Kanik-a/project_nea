"""
Definition of models.
"""

from django.db import models
from django.db.models import Sum


# Model created for presenting hotel details
class hotel_details(models.Model):
    hotel_id = models.IntegerField(primary_key=True,null=False, editable=False)
    hotel_name = models.CharField(max_length = 200)
    city = models.CharField(max_length = 200)
    country = models.CharField(max_length = 200)
    guest_rating = models.IntegerField(200)
    total_room = models.IntegerField(6000)
    price = models.IntegerField(2000)
    
    def __str__(self):
        return self.city
  
# Model created for presenting rooms    
class room_d(models.Model):
    room_id = models.IntegerField(primary_key=True,null=False, editable=False)
    Sleeps = models.IntegerField(200)
    hotel = models.ForeignKey(to=hotel_details, on_delete=models.CASCADE)
    bedtype = models.CharField(max_length = 200)
    classtype = models.CharField(max_length = 200)
    sqft = models.CharField(max_length = 200)
    room_price = models.IntegerField(200)

    def __int__(self):
        return self.hotel

# Model created for presenting amenities
class amenities(models.Model):
    amenity_id = models.IntegerField(primary_key=True,null=False, editable=False)
    roomtype = models.CharField(max_length = 200)
    amen = models.CharField(max_length = 200)
   
    def __str__(self):
        return self.amen

# Model created for presenting meal & parking
class extra(models.Model):
    extra_id = models.IntegerField(primary_key=True,null=False, editable=False)
    meals = models.IntegerField(200)
    hotel = models.ForeignKey(to=hotel_details, on_delete=models.CASCADE)
    parking = models.IntegerField(200)

    def __int__(self):
        return self.hotel

# Model created for presenting tax
class tax(models.Model):
    tax_id = models.IntegerField(primary_key=True,null=False, editable=False)
    tax_rate = models.IntegerField(200)
    city = models.CharField(max_length = 200)
    
    def __str__(self):
        return self.city

# Model created for presenting user details while making bookings
class udetails(models.Model):
    user_id = models.AutoField(primary_key=True,null=False, editable=False)
    uname = models.CharField(max_length = 200)
    fullname = models.CharField(max_length = 200)
    address = models.CharField(max_length = 200)
    city = models.CharField(max_length = 200)
    state = models.CharField(max_length = 200)
    zip = models.CharField(max_length = 200)
    name_on_card = models.CharField(max_length = 200)
    cc_number = models.CharField(max_length = 200)
    exp_month = models.CharField(max_length = 200)
    exp_yr = models.IntegerField(200)
    cvv = models.IntegerField(200)

    def __str__(self):
        return self.uname

# Model created for presenting booking done by users
class booking(models.Model):
    booking_id = models.AutoField(primary_key=True,null=False, editable=False)
    user_id = models.ForeignKey(to=udetails,unique=True, null=True, on_delete=models.CASCADE)
    uname = models.CharField(max_length = 200)
    fullname = models.CharField(max_length = 200)
    email_id = models.CharField(max_length = 200)
    meal = models.IntegerField(200)
    parking = models.IntegerField(200)
    taxcharge = models.IntegerField(200)
    total = models.IntegerField(200)
    roomprice = models.IntegerField(200)
    hotelname = models.CharField(max_length = 200)
    checkin_date = models.DateField(null=True)
    checkout_date = models.DateField(null=True)
    def __str__(self):
        return self.uname

# Model created for presenting flight details
class flight_details(models.Model):
    
    flight_id = models.AutoField(primary_key=True,null=False, editable=False)
    flight_number = models.IntegerField(200)
    airline = models.CharField(max_length = 200)
    depart_city = models.CharField(max_length = 200)
    arrival_city = models.CharField(max_length = 200)
    depart_time = models.DateField(null=True)
    arrival_time = models.DateField(null=True)
    price = models.IntegerField(2000)


# Model created for capturing cancellation done by users
class cancel_booking(models.Model):
    cancel_id = models.AutoField(primary_key=True,null=False, editable=False)
    booking_id = models.IntegerField(200) 
    hotel_bookin_id = models.ForeignKey(to=booking,unique=True, null=True, on_delete=models.CASCADE)
    user_id = models.IntegerField(200)
    uname = models.CharField(max_length = 200)
    fullname = models.CharField(max_length = 200)
    email_id = models.CharField(max_length = 200)
    address = models.CharField(max_length = 200)
    city = models.CharField(max_length = 200)
    state = models.CharField(max_length = 200)
    zip = models.CharField(max_length = 200)
    name_on_card = models.CharField(max_length = 200)
    cc_number = models.CharField(max_length = 200)
    exp_month = models.CharField(max_length = 200)
    exp_yr = models.IntegerField(200)
    cvv = models.IntegerField(200)
    meal = models.IntegerField(200)
    parking = models.IntegerField(200)
    taxcharge = models.IntegerField(200)
    total = models.IntegerField(200)
    roomprice = models.IntegerField(200)
    hotelname = models.CharField(max_length = 200)
    checkin_date = models.DateField(null=True)
    checkout_date = models.DateField(null=True)
    def __str__(self):
        return self.uname

# Model created for capturing cancellation done by users
class cancel_flightbooking(models.Model):
    cancel_id = models.AutoField(primary_key=True,null=False, editable=False)
    booking_id = models.IntegerField(200)
    flight_booking_id = models.ForeignKey(to=booking,unique=True, null=True, on_delete=models.CASCADE)
    user_id = models.IntegerField(200)
    uname = models.CharField(max_length = 200)
    fullname = models.CharField(max_length = 200)
    email_id = models.CharField(max_length = 200)
    address = models.CharField(max_length = 200)
    city = models.CharField(max_length = 200)
    state = models.CharField(max_length = 200)
    zip = models.CharField(max_length = 200)
    name_on_card = models.CharField(max_length = 200)
    cc_number = models.CharField(max_length = 200)
    exp_month = models.CharField(max_length = 200)
    exp_yr = models.IntegerField(200)
    cvv = models.IntegerField(200)
    destcity = models.CharField(max_length = 200)
    arrivalcity = models.CharField(max_length = 200)
    flightprice = models.IntegerField(200)
    airline = models.CharField(max_length = 200)
    destdate = models.DateField(null=True)
    arrivaldate = models.DateField(null=True)
    def __str__(self):
        return self.uname

# Model created for presenting user details while making bookings
class flightudetails(models.Model):
    user_id = models.AutoField(primary_key=True,null=False, editable=False)
    uname = models.CharField(max_length = 200)
    fullname = models.CharField(max_length = 200)
    address = models.CharField(max_length = 200)
    city = models.CharField(max_length = 200)
    state = models.CharField(max_length = 200)
    zip = models.CharField(max_length = 200)
    name_on_card = models.CharField(max_length = 200)
    cc_number = models.CharField(max_length = 200)
    exp_month = models.CharField(max_length = 200)
    exp_yr = models.IntegerField(200)
    cvv = models.IntegerField(200)

    def __str__(self):
        return self.uname

# Model created for presenting booking done by users
class flightbooking(models.Model):
    booking_id = models.AutoField(primary_key=True,null=False, editable=False)
    user_id = models.ForeignKey(to=flightudetails,unique=True, null=True, on_delete=models.CASCADE)
    uname = models.CharField(max_length = 200)
    fullname = models.CharField(max_length = 200)
    email_id = models.CharField(max_length = 200)
    destcity = models.CharField(max_length = 200)
    arrivalcity = models.CharField(max_length = 200)
    flightprice = models.IntegerField(200)
    airline = models.CharField(max_length = 200)
    destdate = models.DateField(null=True)
    arrivaldate = models.DateField(null=True)
    def __str__(self):
        return self.uname