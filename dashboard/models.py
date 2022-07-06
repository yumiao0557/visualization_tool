from django.db import models



## TODO: Create each model for each of the dataset
## EG: class ADNI(models.Model) and class UCSD(models.Model)


# Create your models here.
class CountryData(models.Model):
    country = models.CharField(max_length=100)
    population = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Country Population Data'

    def __str__(self):
        return f'{self.country}-{self.population}'

class Summarized_Dataset(models.Model):
    number_female = models.IntegerField()
    number_male = models.IntegerField()
    number_total = models.IntegerField()
    name_dataset = models.CharField(max_length=100)
    no_female = models.CharField(max_length=100)
    no_male = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Summarized Dataset'

    def __str__(self):
        return f'{self.number_female}-{self.number_male}-{self.number_total}-{self.name_dataset}-{self.no_female}-{self.no_male}'


    

class CheckboxData(models.Model):
    sort_by_name = models.CharField(max_length=100)
    approved = models.BooleanField(default=True)


    class Meta:
        verbose_name_plural = 'Check Box Data'

    def __str__(self):
        return f'{self.sort_by_name}-{self.approved}'

