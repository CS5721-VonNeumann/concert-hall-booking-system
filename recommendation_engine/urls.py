from django.urls import path
from . import views


'''
1. add urls here
2. see how params can be passed and print it
'''

urlpatterns = [
    path("", views.get_recommendations),
    path("set-strategy", views.set_recommendation_strategy),
]
