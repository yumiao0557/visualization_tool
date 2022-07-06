from django import forms
from .models import CheckboxData, CountryData, Summarized_Dataset


class CountryDataForm(forms.ModelForm):
    class Meta:
        model = CountryData
        fields = '__all__'


class Summarized_DatasetForm(forms.ModelForm):
    class Meta:
        model = Summarized_Dataset
        fields = '__all__'

class CheckboxDataForm(forms.ModelForm):
    class Meta:
        model = CheckboxData
        fields = '__all__'
