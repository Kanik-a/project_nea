"""
Importing required libraries for functioning of this site
"""

from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpRequest, response
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import HttpResponseRedirect
from .forms import CustomUserCreationForm
from django.views import View
from django.db import connection
from django.db.models import Sum,F,Count
from django.http import HttpResponse
from app.models import hotel_details, room_d, amenities, booking, cancel_booking, udetails, flightudetails, flightbooking,cancel_flightbooking, booking
from django.template import loader
import hashlib
import pandas as pd
from tabulate import tabulate
from django_pivot.pivot import pivot
import re
from django.views.generic import TemplateView
import numpy as np
from decimal import Decimal
from django.contrib.sessions.backends.db import SessionStore
import requests

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(request,'app\index.html')



class signup(View):
    """Renders the Signup Page"""
    def get(self, request):
            return render(request, 'app\signup.html')
    
    def is_authenticated(self, request):
        return redirect('app\login.html')


    def post(self, request):
        signup_form = CustomUserCreationForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            username = signup_form.cleaned_data.get('username')
            password = signup_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
           
            return render(request, 'app\index.html')
        else:
            return render(request, 'app\signup.html', {'form': signup_form})

    def notpost(View):
        signup_form = CustomUserCreationForm()
        return render(request, 'app\signup.html', {'form': signup_form})



#Once user is authenticated redirects to the page else throws an error
def signin(request):
    
    if request.user.is_authenticated:
        return render(request, 'app\index.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
             login(request, user)
             return render(request, 'app\layout.html')
        
        else:
            msg = 'Error Login'
            form = AuthenticationForm(request.POST)
            return render(request, 'app\login.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
        return render(request, 'app\login.html', {'form': form})

# Logs out the user from site
def logout_request(request):
	logout(request)
	
	return render(request, 'app\index.html')


class booking_details:

    def book_details(self, current_user):
        booking_data = booking.objects.filter(user_id__uname=current_user).values('booking_id', 'fullname', 'email_id', 'meal', 'parking', 'total', 
                                                                                  'hotelname', 'checkin_date', 'checkout_date')

        booking_data = [{
            'booking_id': row['booking_id'],
            'full_name': row['fullname'],
            'email_id': row['email_id'],
            'meal': row['meal'],
            'parking': row['parking'],
            'total_charge': row['total'],
            'hotel_name': row['hotelname'],
            'checkin_date': row['checkin_date'],
            'checkout_date': row['checkout_date'],}
            for row in booking_data]

        row_count = len(booking_data)

        flight_booking_data = flightbooking.objects.filter(user_id__uname=current_user).values('booking_id', 'fullname', 'email_id', 'destcity', 'arrivalcity', 'flightprice', 
                                                                                  'airline', 'destdate', 'arrivaldate')

        flight_booking_data = [{
            'booking_id': row['booking_id'],
            'full_name': row['fullname'],
            'email_id': row['email_id'],
            'destcity': row['destcity'],
            'arrivalcity': row['arrivalcity'],
            'flightprice': row['flightprice'],
            'airline': row['airline'],
            'destdate': row['destdate'],
            'arrivaldate': row['arrivaldate'],}
            for row in flight_booking_data]

        flight_row_count = len(flight_booking_data)

        return current_user, row_count, booking_data, flight_row_count, flight_booking_data



class cancel_booking:

    def cancelbooking(self, booking_id):
        try:
            # Get the booking and user details objects
            booking_obj = booking.objects.get(booking_id=booking_id)
            udetails_obj = udetails.objects.get(user_id=booking_id)

            
            # Delete the original booking and user details objects
            booking_obj.delete()
            udetails_obj.delete()

            # Return the cancelled booking ID and the ID of the cancel_booking object
            return booking_id

        except booking.DoesNotExist:
            # Handle the case where the booking object does not exist
            no_booking = "No booking exist for the user"
            return no_booking

        except udetails.DoesNotExist:
            # Handle the case where the user details object does not exist
            no_booking = "No booking exist for the user"
            return no_booking

class cancel_flight_booking:

    def cancel_f_booking(self, flight_booking_id):
        try:
            # Get the booking and user details objects
            booking_obj = flightbooking.objects.get(booking_id=flight_booking_id)
            udetails_obj = flightudetails.objects.get(user_id=flight_booking_id)

            
            # Delete the original booking and user details objects
            booking_obj.delete()
            udetails_obj.delete()

            # Return the cancelled booking ID and the ID of the cancel_booking object
            return flight_booking_id

        except booking.DoesNotExist:
            # Handle the case where the booking object does not exist
            no_booking = "No booking exist for the user"
            return no_booking

        except udetails.DoesNotExist:
            # Handle the case where the user details object does not exist
            no_booking = "TNo booking exist for the user"
            return no_booking

# Class created for user to view their bookings
class MyBookingsView(TemplateView,booking_details,cancel_booking,cancel_flight_booking):
    
    # This function calls the booking_details function to view bookings done by the current logged user
    def get(self, request, *args, **kwargs):
        current_user = request.user
        data = booking_details()
        current_user,row_count,booking_data,flight_row_count, flight_booking_data = data.book_details(current_user) 
        return render(request, 'app/mybookings.html', {'current_user': current_user, 'row_count': row_count, 'booking_data': booking_data,
                                                       'flight_row_count':flight_row_count,'flight_booking_data':flight_booking_data})

    # This function calls the cancel_booking function to cancel the booking selected by the current logged user
    def post(self, request, *args, **kwargs):
        booking_id = request.POST.get('cancel')
        flight_booking_id = request.POST.get('cancelflight')
        new_book_id = 0
        cancel_booking_id = 0
        if booking_id:
            data = cancel_booking()
            new_book_id = data.cancelbooking(booking_id)

        if flight_booking_id:
            data = cancel_flight_booking()
            new_book_id = data.cancel_f_booking(flight_booking_id)

        return render(request, 'app/cancel.html', {'new_book_id': new_book_id})



class hotel_options:

    def h_options(self,c_name):
        
        c_name = c_name
        mydata = hotel_details.objects.filter(city=c_name)
        
        return mydata, c_name


class hotel_options_sort:

    def h_options_sort(self,c_name):
        c_name = c_name
        
        
        hotel_id = []
        hotel_name = []
        city = []
        country = []
        guest_rating = []
        total_room = []
        price = []
        sort_dict = {}
        mydata = hotel_details.objects.filter(city=c_name)
        for row in mydata:
            hotel_id.append(row.hotel_id)
            hotel_name.append(row.hotel_name)
            city.append(row.city)
            country.append(row.country)
            guest_rating.append(row.guest_rating)
            total_room.append(row.total_room)
            price.append(int(row.price))
            sort_dict[row.hotel_id] = {
            "hotel_name": row.hotel_name,
            "city": row.city,
            "country": row.country,
            "guest_rating": row.guest_rating,
            "total_room": row.total_room,
            "price": int(row.price)
            }
        callmergefunc = callmergesort()
        result = callmergefunc.merge_sort(price)
        sorted_keys = [k for k, v in sorted(sort_dict.items(), key=lambda x: result.index(x[1]['price']))]
        new_dict = {k: sort_dict[k] for k in sorted_keys}
        
        return mydata,c_name,new_dict

# Class is defined to list hotels based on location entered by user and run MERGESORT algorithm to sort the hotels by Price     
class hoteloptions(TemplateView,hotel_options,hotel_options_sort):

    # This function calls the hotel_options_Sort function to sort the hotel list by price
    def get(self, request, *args, **kwargs):
        sortcity = request.GET.get('sortcity')
        c_name = request.POST.get('location')
        sorting =  request.POST.get('sorting')
        checkin_user = request.GET.get('checkin_user')
        checkout_user = request.GET.get('checkout_user')
        searchhotel = request.POST.get('searchhotel')
        mydata = []
        
        d_name = ""
        data = hotel_options_sort()
        mydata1,d_name1,new_dict = data.h_options_sort(sortcity)
        template = loader.get_template('app\hotel_options.html')
        context = {'mymembers1': mydata1,'checkout_user':checkout_user,'checkin_user':checkin_user,'d_name1':d_name1,'new_dict':new_dict}
        return HttpResponse(template.render(context, request))

    # This function calls the hotel_options to return the list of hotels based on location entered by user
    def post(self, request, *args, **kwargs):
        sortcity = request.POST.get('sortcity')
        c_name = request.POST.get('location')
        sorting =  request.POST.get('sorting')
        checkin_user = request.POST.get('checkin')
        checkout_user = request.POST.get('checkout')
        searchhotel = request.POST.get('searchhotel')
        mydata = []
       
        d_name = ""
        data = hotel_options()
        mydata,d_name = data.h_options(c_name)
        
        template = loader.get_template('app\hotel_options.html')
        context = {'mymembers': mydata,'checkout_user':checkout_user,'checkin_user':checkin_user,'sortcity':sortcity}
        return HttpResponse(template.render(context, request))

        
# This function returns the type of room based on hotel selection done as per the location
def room(request):
    c_name = request.POST.get('roomd')
    checkin_user = request.POST.get('checkin')
    checkout_user = request.POST.get('checkout')

    # Define room types and their corresponding indices
    room_types = ['suproom', 'deluxroom', 'execroom', 'doubledeluxroom', 'execsuite', 'supsuite', 'presroom', 'pressuite']
    room_indices = [10, 10, 10, 10, 10, 10, 10, 10]

    # Define amenity names and their corresponding indices
    amenity_names = ['amen_1', 'amen_2', 'amen_3', 'amen_4', 'amen_5']
    amenity_indices = [2, 2, 2, 2, 2]

    # Define a list to store the fetched room details
    room_details = []

    # Fetch room details using a single cursor object and parameterized queries
    with connection.cursor() as cursor:
        query = "SELECT * FROM app_hotel_details LEFT JOIN app_room_d ON app_hotel_details.hotel_id = app_room_d.hotel_id where app_hotel_details.hotel_id = %s"
        cursor.execute(query, [c_name])
        rows = cursor.fetchall()

        for i in range(len(room_types)):
            room_type = rows[i][room_indices[i]]
            room_price = rows[i][12]

            # Fetch amenity details for the current room type
            query = "select * from app_amenities where roomtype like %s"
            cursor.execute(query, ['%' + room_type + '%'])
            amenities = cursor.fetchall()

            # Store the fetched amenity details in a dictionary
            amenity_details = {}
            for j in range(len(amenity_names)):
                amenity_name = amenities[j][amenity_indices[j]]
                amenity_details[amenity_names[j]] = amenity_name

            # Append the room details and amenity details to the room_details list
            room_details.append({
                'room_type': room_type,
                'room_price': room_price,
                'amenities': amenity_details
                
            })
    mydata = room_d.objects.filter(hotel=c_name)
    mydata_list = list(mydata)
    mydatahotel = hotel_details.objects.filter(hotel_id=c_name)
    # Render the response with the room details
    return render(request, 'app/room.html', {'mydata_list':mydata_list,'room_details': room_details,'myroom': mydata,'myhotel': mydatahotel,
                                             'checkout_user':checkout_user,'checkin_user':checkin_user})



# This functions returns the selected room type for confirmation
def roomconfirmed(request):
    class_id = request.POST.get('roomclass')
    hot_id = request.POST.get('hot_name')
    city_id = request.POST.get('city_name')
    sleep_id = request.POST.get('roomsleep')
    bedtype_id = request.POST.get('bedtype')
    sqft_id = request.POST.get('sqft')
    checkin_user = request.POST.get('checkin')
    checkout_user = request.POST.get('checkout')
    template = loader.get_template('app/roomconfirmed.html')
    context = {'hotel_id_name':hot_id,'city_id_name':city_id,'class_id_name':class_id,'sleep_id_name':sleep_id,'bedtype_id_name':bedtype_id,
               'sqft_id_name':sqft_id,'checkout_user':checkout_user,'checkin_user':checkin_user}
    return HttpResponse(template.render(context, request))
    

# This function returns the page for selecting meals and parking for selected room
def roomselect(request):
    hotel_name = request.POST.get('hot_name')
    room_class = request.POST.get('roomclass')
    meal_yes_no = request.POST.get('meals')
    parking_yes_no = request.POST.get('parking')
    city_n = request.POST.get('city_name')
    checkin_user = request.POST.get('checkin')
    checkout_user = request.POST.get('checkout')
    total_amount = 0
   
    f = 'any value'
    g = 'any value'
    meal_value = 0
    parking_value = 0
    que2 = 'any value'
    que3 = 'any value'
    que1 = "SELECT * FROM app_hotel_details LEFT JOIN app_room_d ON app_hotel_details.hotel_id = app_room_d.hotel_id where app_hotel_details.hotel_name='" + hotel_name + "'" + " and app_room_d.classtype='" + room_class + "'" ;
    cursor = connection.cursor()
    cursor.execute(que1)
    r = cursor.fetchall()
    room_price = r [0][12]
    if meal_yes_no == 'Yes':
        que2 = "SELECT * FROM app_hotel_details LEFT JOIN app_extra ON app_hotel_details.hotel_id = app_extra.hotel_id where app_hotel_details.hotel_name='" + hotel_name + "'" ;
        cursor1 = connection.cursor()
        cursor1.execute(que2)
        f = cursor1.fetchall()
        meal_value = f [0][8]
    elif meal_yes_no == 'No':
        meal_value = 0
    if parking_yes_no == 'Yes':
        que3 = "SELECT * FROM app_hotel_details LEFT JOIN app_extra ON app_hotel_details.hotel_id = app_extra.hotel_id where app_hotel_details.hotel_name='" + hotel_name + "'" ;
        cursor2 = connection.cursor()
        cursor2.execute(que3)
        g = cursor2.fetchall()
        parking_value = g [0][9]
    elif parking_yes_no == 'No':
        parking_value = 0
    que4 = "SELECT * FROM app_tax where city='" + city_n + "'" ;
    cursor3 = connection.cursor()
    cursor3.execute(que4)
    h = cursor3.fetchall()
    tax_r = h[0][1]
    tax_charges = (room_price * tax_r) / 100
    tax_charges = int(tax_charges)
    total_amount = room_price + tax_charges + meal_value + parking_value
    template = loader.get_template('app/roomselect.html')
    context = {'myroomselect': room_price,'meal_selection':meal_value,'parking_selection':parking_value,'tax_rate':tax_charges,'final_amount':total_amount,
               'hotel_name':hotel_name,'checkout_user':checkout_user,'checkin_user':checkin_user
              }
    return HttpResponse(template.render(context, request))


# Class is created to submit the checkout form filled by user, also does validation of Credit Card number and Email based on PATTERN MATCHING algorithm
class CheckoutView(TemplateView):
    template_name = 'app/checkout.html'

    def post(self, request, *args, **kwargs):
        u_name = request.POST.get('uname')
        f_name = request.POST.get('fname')
        email_id = request.POST.get('email')
        addr = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        nameoncard = request.POST.get('nameoncard')
        cardnumber = request.POST.get('cardnumber')
        expmonth = request.POST.get('expmonth')
        expyear = request.POST.get('expyear')
        cvv = request.POST.get('cvv')
        meal_select= request.POST.get('mealselect')
        parking_select = request.POST.get('parkingselect')
        tax_rate = request.POST.get('taxrate')
        total = request.POST.get('total')
        roomprice = request.POST.get('price')
        hotelname = request.POST.get('hotelname')
        checkin_user = request.POST.get('checkin')
        checkout_user = request.POST.get('checkout')
        # email validation algorithm using pattern matching
        
        email = str(email_id)
        email_valid = self.email_valid(email)
        if email_valid != 'valid email':
            context = {'email_valid':email_valid}
            return render(request, 'app/roomselect.html', context)

        # Credit card validation whether user input has 16 digits with no alphabets and starts with ("visa":4,"master":5,"amex":3,"discover":6)
        card_num = str(cardnumber)
        cc_msg = self.cc_valid(card_num)
        cc_number_message = cc_msg[0]
        cc_issuer_message = cc_msg[1]
        if cc_number_message == 'Card number valid' and cc_issuer_message == 'Valid issuer':
            que4 = "SELECT * FROM app_hotel_details where app_hotel_details.hotel_name='" + hotelname + "'" ;
            cursor3 = connection.cursor()
            cursor3.execute(que4)
            h = cursor3.fetchall()
            hotel_id = h[0][0]
            context = {'uname': u_name,'room_price':roomprice,'f_name':f_name,'email_id':email_id,'addr':addr,'city':city,'state':state,'zip':zip,
            'nameoncard':nameoncard,'cardnumber':cardnumber,'expmonth':expmonth,'expyear':expyear,'cvv':cvv,'meal_select':meal_select,
            'parking_select':parking_select,'tax_rate':tax_rate,'total':total,'hotelname':hotelname,'hotel_id':hotel_id,'checkout_user':checkout_user,'checkin_user':checkin_user}
            return self.render_to_response(context)
        else:
            context = {'cc_number_message':cc_number_message,'cc_issuer_message':cc_issuer_message}
            return render(request, 'app/roomselect.html', context)

    # Credit card validation based on provider using custom PATTERN MATCHING algorithm
    def cc_valid(self, cc_num):
        cc_issuer = {"visa": 4, "master": 5, "amex": 3, "discover": 6}
        cc_issuer_message = ""
        cc_number_message = ""
        if cc_num.isdigit() and len(cc_num) == 16:
            cc_number_message = "Card number valid"
        else:
            cc_number_message = "Card number not valid"

        for x in cc_issuer:
            if int(cc_num[0]) == cc_issuer[x]:
                cc_issuer_message = "Valid issuer"
                break
            else:
                cc_issuer_message = "Invalid issuer"

        return cc_number_message,cc_issuer_message

    # Email validation using regex
    def email_valid(self,email):
        regex = r'^[a-zA-Z0-9]+@[a-zA-Z.]+\.[a-zA-Z]{2,}$'
        valid = "valid email"
        invalid = "invalid email"
        if re.match(regex, email):
            return valid
        else:
            return invalid
        return valid,invalid

# This function renders to the final page for hoetl room selection
def final(request):

    u_name = request.POST.get('uname')
    f_name = request.POST.get('f_name')
    email_id = request.POST.get('email_id')
    addr = request.POST.get('addr')
    city = request.POST.get('city')
    state = request.POST.get('state')
    zip = request.POST.get('zip')
    nameoncard = request.POST.get('nameoncard')
    cardnumber = request.POST.get('cardnumber')
    expmonth = request.POST.get('expmonth')
    expyear = request.POST.get('expyear')
    cvv = request.POST.get('cvv')
    meal_select= request.POST.get('meal_select')
    parking_select = request.POST.get('parking_select')
    tax_rate = request.POST.get('tax_rate')
    total = request.POST.get('total')
    roomprice = request.POST.get('room_price')
    hotelname = request.POST.get('hotelname')
    checkin_user = request.POST.get('checkin')
    checkout_user = request.POST.get('checkout')

    # hashing credit card numbers
    hash_card = str(cardnumber)
    result = hashlib.md5(hash_card.encode())
    hash_result = result.hexdigest()

    # inserting user details in udetails model
    insert_udetails = udetails(uname=u_name,fullname=f_name,address=addr,city=city,state=state,zip=zip,name_on_card=nameoncard,
                               cc_number=cardnumber,exp_month=expmonth,exp_yr=expyear,cvv=cvv)
    insert_udetails.save()
    user_book_id = insert_udetails.user_id
    
    if meal_select == 'NA' or parking_select == 'NA':
        meal_select = 0
        parking_select = 0
    else:
        meal_select == meal_select
        parking_select == parking_select

    # inserting booking into booking model for referencing booking done by user
    insert_booking = booking(uname=u_name,fullname=f_name,email_id=email_id,meal=meal_select,parking=parking_select,taxcharge=tax_rate,total=total,
                             roomprice=roomprice,hotelname=hotelname,checkin_date=checkin_user,checkout_date=checkout_user,user_id_id=user_book_id)
    insert_booking.save()
    book_id = insert_booking.booking_id
    template = loader.get_template('app/final.html')
    context = {'uname': u_name,'room_price':roomprice,'f_name':f_name,'email_id':email_id,'addr':addr,'city':city,'state':state,'zip':zip,
               'nameoncard':nameoncard,'cardnumber':cardnumber,'expmonth':expmonth,'expyear':expyear,'cvv':cvv,'book_id':book_id,'result':hash_result,'cardnumber':cardnumber}
    return HttpResponse(template.render(context, request))


# This function renders the analytics page for site analytics
def analytics(request):
    template = loader.get_template('app/analytics.html')
    u_name = "pradeep"
    context = {'uname': u_name}
    return HttpResponse(template.render(context, request))

# Class is created to present analytics based on different requirements
class callanalyticsView(TemplateView):
    template_name = 'app/analytics.html'

    def post(self, request, *args, **kwargs):
        u_name = request.POST.get('uname')
        roomprice_analytics = None
        room_analytics = None
        booking_analytics = None
        user_register_analytics = None
        user_login_analytics = None
        booking = None
        roomavailable = None
        find_room = request.POST.get('find_room')
        find_room_price = request.POST.get('find_room_price')
        user_booking = request.POST.get('user_booking')
        user_login = request.POST.get('user_login')
        user_register = request.POST.get('user_register')
        booking = request.POST.get('booking')
        roomavailable = request.POST.get('roomavailable')
        hotelrevenue = request.POST.get('hotelrevenue')
        total_r = []
        if find_room:
            cities, total_r,room_analytics,sort_dict,result,new_dict = self.f_room_analytics()
            return render(request, 'app/analytics.html', {'new_dict':new_dict,'result':result,'sort_dict':sort_dict,'total_r':total_r,'total_room_citywise':room_analytics,
                                                          'roomprice_analytics':roomprice_analytics,'booking_analytics':booking_analytics,
                                                      'user_register_analytics':user_register_analytics,'user_login_analytics':user_login_analytics})
        if find_room_price:
            roomprice_analytics = self.f_roomprice_analytics()
            return render(request, 'app/analytics.html', {'roomprice_analytics':roomprice_analytics})
        if user_booking:
            booking_analytics = self.f_booking_analytics()
            return render(request, 'app/analytics.html', {'booking_analytics':booking_analytics})
        if user_register:
            user_register_analytics = self.f_register_analytics()
            return render(request, 'app/analytics.html', {'user_register_analytics':user_register_analytics})
        if user_login:
            user_login_analytics = self.f_login_analytics()
            return render(request, 'app/analytics.html', {'user_login_analytics':user_login_analytics})
        if booking:
            user_booking_analytics = self.f_booking_analytics()
            return render(request, 'app/analytics.html', {'user_booking_analytics':user_booking_analytics})
        if roomavailable:
            user_available_analytics = self.f_available_analytics()
            return render(request, 'app/analytics.html', {'user_available_analytics':user_available_analytics})
        if hotelrevenue:
            user_available_analytics = self.hotel_revenue()
            return render(request, 'app/analytics.html', {'hotel_revenue_analytics':user_available_analytics})
    
    # This function present the total no. of rooms available as per city
    def f_room_analytics(self):
        total_room_citywise = "SELECT city, SUM(total_room) from app_hotel_details group by city"
        cursor = connection.cursor()
        cursor.execute(total_room_citywise)
        pivot_room_citywise = cursor.fetchall()
        cities = []
        total_r = []
        sort_dict = {}
        for row in pivot_room_citywise:
            cities.append(row[0])
            total_r.append(int(row[1]))
            sort_dict[row[0]] = int(row[1])

        callmergefunc = callmergesort()
        result = callmergefunc.merge_sort(total_r)
        sorted_keys = [k for k, v in sorted(sort_dict.items(), key=lambda x: result.index(x[1]))]
        new_dict = {k: sort_dict[k] for k in sorted_keys}
        return cities, total_r, pivot_room_citywise,sort_dict,result,new_dict

    # This function returns the total price based on location
    def f_roomprice_analytics(self):
        total_price_citywise = "SELECT city, SUM(price) from app_hotel_details group by city"
        cursor1 = connection.cursor()
        cursor1.execute(total_price_citywise)
        pivot_price_citywise = cursor1.fetchall()
        return pivot_price_citywise

    # This function returns the no. of booking for each month
    def f_booking_analytics(self):
        total_price_citywise = "select city,count(city) from app_udetails group by city"
        cursor1 = connection.cursor()
        cursor1.execute(total_price_citywise)
        booking_citywise = cursor1.fetchall()
        return booking_citywise

    # This function returns the no. of users registered on site monthwise
    def f_register_analytics(self):
        total_price_citywise = "select MONTHNAME(date_joined) as Month_Joined,  count(date_joined) as Count from auth_user group by Month_Joined"
        cursor1 = connection.cursor()
        cursor1.execute(total_price_citywise)
        user_login = cursor1.fetchall()
        return user_login

    # This function returns the no. of users logged monthwise
    def f_login_analytics(self):
        total_price_citywise = "select MONTHNAME(last_login) as Login_Joined,  count(last_login) as Count from auth_user group by Login_Joined"
        cursor1 = connection.cursor()
        cursor1.execute(total_price_citywise)
        user_register = cursor1.fetchall()
        return user_register

    # This function returns the monthwise booking
    def f_booking_analytics(self):
        total_price_citywise = "select MONTHNAME(checkin_date) as Month_Joined,  count(checkin_date) as Count from app_booking group by Month_Joined;"
        cursor1 = connection.cursor()
        cursor1.execute(total_price_citywise)
        month_booking = cursor1.fetchall()
        return month_booking

    # This function returns the monthwise booking
    def f_available_analytics(self):
        total_price_citywise = (
        "SELECT hotel_name AS hname, hotelname AS hotel, "
        "SUM(total_room) AS Total_Room, "
        "SUM(total_room) - COUNT(hotelname) AS Room_Available, "
        "COUNT(hotelname) AS Room_Booked "
        "FROM app_hotel_details "
        "LEFT JOIN app_booking "
        "ON app_hotel_details.hotel_name = app_booking.hotelname "
        "GROUP BY hname;" )
        cursor1 = connection.cursor()
        cursor1.execute(total_price_citywise)
        month_booking = cursor1.fetchall()
        return month_booking


    def hotel_revenue(self):
        total_price_citywise = (
        "SELECT Hotelname, "
        "COALESCE(SUM(CASE WHEN monthname(checkin_date) = 'January' THEN roomprice END), '') AS January, "
        "COALESCE(SUM(CASE WHEN monthname(checkin_date) = 'February' THEN roomprice END), '') AS February, "
        "COALESCE(SUM(CASE WHEN monthname(checkin_date) = 'March' THEN roomprice END), '') AS March, "
        "COALESCE(SUM(CASE WHEN monthname(checkin_date) = 'April' THEN roomprice END), '') AS April, "
        "COALESCE(SUM(CASE WHEN monthname(checkin_date) = 'May' THEN roomprice END), '') AS May, "
        "COALESCE(SUM(CASE WHEN monthname(checkin_date) = 'June' THEN roomprice END), '') AS June, "
        "COALESCE(SUM(CASE WHEN monthname(checkin_date) = 'July' THEN roomprice END), '') AS July, "
        "COALESCE(SUM(CASE WHEN monthname(checkin_date) = 'August' THEN roomprice END), '') AS August, "
        "COALESCE(SUM(CASE WHEN monthname(checkin_date) = 'September' THEN roomprice END), '') AS September, "
        "COALESCE(SUM(CASE WHEN monthname(checkin_date) = 'October' THEN roomprice END), '') AS October, "
        "COALESCE(SUM(CASE WHEN monthname(checkin_date) = 'November' THEN roomprice END), '') AS November, "
        "COALESCE(SUM(CASE WHEN monthname(checkin_date) = 'December' THEN roomprice END), '') AS December, "
        "COALESCE(SUM(roomprice), '') AS total_price "
        "FROM app_booking "
        "GROUP BY Hotelname;" )
        cursor1 = connection.cursor()
        cursor1.execute(total_price_citywise)
        month_booking = cursor1.fetchall()
        return month_booking


# This class is created for MERGESORT algorithm
class callmergesort(TemplateView):
    template_name = 'app/analytics.html'

    def post(self, request, *args, **kwargs):
        arr = request.POST.get('arr')
        arr_list = [int(d) for d in str(arr)]
        resultarr = self.merge_sort(arr_list)
        return render(request, 'app/analytics.html', {'resultarr':resultarr})

    def merge_sort(self,arr):
        l = 0
        h = len(arr) - 1
        unsorted_arr1 = []
        unsorted_arr2 = []
        if l < h:
            midpoint = len(arr)//2
            for item in arr:
                if arr.index(item) < midpoint:
                    unsorted_arr1.append(item)
                elif arr.index(item) >= midpoint:
                    unsorted_arr2.append(item)
       

            self.merge_sort(unsorted_arr1)
            self.merge_sort(unsorted_arr2)

            p = q = r = 0

            while p < len(unsorted_arr1) and q < len(unsorted_arr2):
                if unsorted_arr1[p] < unsorted_arr2[q]:
                    arr[r] = unsorted_arr1[p]
                    p += 1
                else:
                    arr[r] = unsorted_arr2[q]
                    q += 1
                r += 1

            while p < len(unsorted_arr1):
                arr[r] = unsorted_arr1[p]
                p += 1
                r += 1

            while q < len(unsorted_arr2):
                arr[r] = unsorted_arr2[q]
                q += 1
                r += 1

        return arr


class flightdetails:

    def flightapi(self,destination,arrival,checkin,checkout):
        
        response = requests.get('http://globetrotter:8000/flight?depart_city={}&arrival_city={}&check_in={}&checkout={}'.format(destination, arrival, checkin, checkout))
        data = response.json().get('data')
        return data

class flightcall(TemplateView,flightdetails):
    template_name = 'app/flight.html'

    def post(self, request, *args, **kwargs):
        searchflight = request.POST.get('searchflight')
        destination = request.POST.get('destination')
        arrival = request.POST.get('arrival')
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')

        if searchflight:
            data = flightdetails()
            data = data.flightapi(destination,arrival,checkin,checkout)

        return render(request, 'app/flightdetails.html',{'data':data})

class flightfinal:

    def finalbooking(self, u_name,fname,address,city,state,zip,nameoncard,cardnumber,expmonth,expyear,cvv,user_id,email_id,departurecity,arrivalcity,flightprice,airline,departime,arrivaltime):

        # inserting user details in flightudetails model
        insert_udetails = flightudetails(uname=u_name,fullname=fname,address=address,city=city,state=state,zip=zip,name_on_card=nameoncard,
                               cc_number=cardnumber,exp_month=expmonth,exp_yr=expyear,cvv=cvv)
        insert_udetails.save()
        insert_udetails_id = insert_udetails.user_id

        # inserting user details in flightudetails model
        insert_bookingdetails = flightbooking(user_id_id=insert_udetails_id,uname=u_name,fullname=fname,email_id=email_id,destcity=departurecity,arrivalcity=arrivalcity,flightprice=flightprice,
                                          airline=airline,destdate=departime,arrivaldate=arrivaltime)
        insert_bookingdetails.save()
        insert_bookingdetails_id = insert_bookingdetails.booking_id

        return insert_bookingdetails_id   

class flightcheckout(TemplateView,flightfinal):
    template_name = 'app/flightbooking.html'

    def post(self, request, *args, **kwargs):
        u_name = request.POST.get('u_name')
        fname = request.POST.get('fname')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        nameoncard = request.POST.get('nameoncard')
        cardnumber = request.POST.get('cardnumber')
        expmonth = request.POST.get('expmonth')
        expyear = request.POST.get('expyear')
        cvv = request.POST.get('cvv')
        user_id = request.POST.get('')
        email_id = request.POST.get('email')
        departurecity = request.POST.get('departurecity')
        arrivalcity = request.POST.get('arrivalcity')
        flightprice = request.POST.get('flightprice')
        airline = request.POST.get('airline')
        departime = request.POST.get('departime')
        arrivaltime = request.POST.get('arrivaltime')
        finalflight = request.POST.get('finalflight')

        if finalflight:

            callfinal = flightfinal()
            insert_bookingdetails_id = callfinal.finalbooking(u_name,fname,address,city,state,zip,nameoncard,cardnumber,expmonth,expyear,cvv,user_id,email_id,departurecity,arrivalcity,flightprice,airline,departime,arrivaltime)

        return render(request, 'app/flightfinal.html', {'insert_bookingdetails_id':insert_bookingdetails_id })


class flightbookingdetails(TemplateView):
    template_name = 'app/flightbooking.html'

    def post(self, request, *args, **kwargs):
        u_name = request.POST.get('u_name')
        flightnumber = request.POST.get('flightnumber')
        airline = request.POST.get('airline')
        departcity = request.POST.get('departcity')
        arrivalcity = request.POST.get('arrivalcity')
        departtime = request.POST.get('departtime')
        arrivaltime = request.POST.get('arrivaltime')
        price = request.POST.get('price')
        return render(request, 'app/flightbooking.html', {'flightnumber':flightnumber,'airline':airline,'departcity':departcity,'arrivalcity':arrivalcity,
                                                      'departtime':departtime,'arrivaltime':arrivaltime,'price':price,'u_name':u_name}) 