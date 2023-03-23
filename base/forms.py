from django.forms import ModelForm
from .models import Car,Part

class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
        
class PartForm(ModelForm):
    class Meta:
        model = Part
        fields = '__all__'