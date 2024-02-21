# main.py

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.core.wsgi import get_wsgi_application
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Skysearch.settings")
import django
django.setup()
from django.core.management import call_command
from fastapi import FastAPI, Request
from app.models import flight_details


# Created API - While searching for flight this API will be called with parameters and will return JSON for processing

django_app = get_wsgi_application()
app = FastAPI()

@app.get("/flight")
def flight(request: Request):
    destination = request.query_params.get('depart_city',default=None)
    arrival = request.query_params.get('arrival_city', default=None)
    checkin = request.query_params.get('check_in', default=None)
    checkout = request.query_params.get('checkout', default=None)
    dataflight = flight_details.objects.filter(depart_city=destination,arrival_city=arrival,depart_time__gt=checkin,arrival_time__lt=checkout)
    return {'data':list(dataflight)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


