# flight_search/forms.py
from django import forms

class FlightSearchForm(forms.Form):
    CITIES = [
        ("Madrid", "Madrid"),
        ("Oslo", "Oslo"),
        ("Roma", "Roma"),
        ("Paris", "Paris"),
        ("Berlin", "Berlin"),
    ]
    
    origem = forms.ChoiceField(choices=CITIES, label="Cidade de Origem")
    destinos = forms.MultipleChoiceField(choices=CITIES, widget=forms.CheckboxSelectMultiple, label="Destinos Intermediários")
    data_partida = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Data de Partida")
