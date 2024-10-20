from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from . import models


# Create your views here.
def getShows(request):
    shows = serializers.serialize('json', models.Shows.objects.all())
    return HttpResponse(shows, content_type='application/json')

def getSeats(request):
    seats = serializers.serialize('json', models.Seats.objects.all())
    return HttpResponse(seats, content_type='application/json')

