from django.forms import ModelForm, TextInput
from .models import City, Conditions
from django import forms

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'class' : 'input', 'placeholder' : 'City Name'}),
        } #updates the input class to have the correct Bulma class and placeholder



class ConditionsForm(ModelForm):
    class Meta:
        model = Conditions
        fields = ['selector']

        
