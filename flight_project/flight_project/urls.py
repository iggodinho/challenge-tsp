# flight_project/urls.py
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from django.shortcuts import redirect

def home(request):
    return redirect('flight_selection')  # Redireciona para a URL de seleção de voos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('flights/', include('flight_search.urls')),
    path('', home),  # Adiciona uma página inicial
]
