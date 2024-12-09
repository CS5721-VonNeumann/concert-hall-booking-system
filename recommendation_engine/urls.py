from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_recommendations, name="get_recommendations"),
    path("set-strategy", views.set_recommendation_strategy, name="set_recommendation_strategy"),
]
