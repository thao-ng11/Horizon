from django.forms import ModelForm
from .models import Conditions

class ConditionsForm(ModelForm):
    class Meta:
        model = Conditions
        fields = ['selector']

        
