from django import forms
from .models import Meter


class CreateForm(forms.ModelForm):
    ELECTRICITY = 'E'
    GAS = 'G'
    WATER = 'W'
    RESOURCE_TYPE_CHOICES = [
        (ELECTRICITY, 'Electricity'),
        (GAS, 'Gas'),
        (WATER, 'Water'),
    ]

    class Meta:
        model = Meter
        fields = ('name', 'unit', 'resource_type')

    name = forms.CharField(label='Enter name')
    resource_type = forms.ChoiceField(choices=RESOURCE_TYPE_CHOICES, required=True)
    unit = forms.CharField(label='Enter unit')
    name.widget.attrs.update({'class': 'form-control'})
    resource_type.widget.attrs.update({'class': 'form-control'})
    unit.widget.attrs.update({'class': 'form-control'})
