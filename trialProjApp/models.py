from django.db import models

# Create your models here.


class Meter(models.Model):
    ELECTRICITY = 'E'
    GAS = 'G'
    WATER = 'W'
    RESOURCE_TYPE_CHOICES = [
        (ELECTRICITY, 'Electricity'),
        (GAS, 'Gas'),
        (WATER, 'Water'),
    ]
    name = models.CharField(primary_key=True, max_length=255, blank=False, null=False)
    resource_type = models.CharField(max_length=3, choices=RESOURCE_TYPE_CHOICES, default=ELECTRICITY)
    unit = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return str(self.name)


class MeterData(models.Model):
    date = models.DateField()
    value = models.FloatField()
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date)


