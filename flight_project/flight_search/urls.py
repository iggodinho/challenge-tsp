# flight_search/urls.py
from django.urls import path
from .views import flight_selection_view, flight_results_view

urlpatterns = [
    path('', flight_selection_view, name='flight_selection'),
    path('results/', flight_results_view, name='flight_results'),
]
