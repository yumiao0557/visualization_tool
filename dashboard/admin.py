from django.contrib import admin
from .models import CountryData, Summarized_Dataset, CheckboxData
# Register your models here.

admin.site.register(CountryData)
admin.site.register(Summarized_Dataset)
admin.site.register(CheckboxData)

