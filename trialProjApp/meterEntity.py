from .models import Meter, MeterData
import datetime


class MeterEntity:

    def __init__(self, name, resource="", unit=""):
        self.name = name
        self.resource = resource
        self.unit = unit

    def create_meter(self):
        Meter.objects.create(name=self.name, resource_type=self.resource, unit=self.unit)

    def delete_all_data(self):
        meter = MeterData.objects.filter(meter_id=self.name)
        meter.delete()

    def load_data(self, dat):
        dat2 = []
        for x in dat:
            x = x.rstrip()
            x = x.split(',')
            dat2.append(x)
        dat2.pop(0)
        for x in dat2:
            x[0] = datetime.datetime.strptime(x[0], '%Y-%m-%d').date()
        self.add_data(sorted(dat2, key=lambda date: date[0]))

    def add_data(self, dat):
        MeterData.objects.all().filter(meter_id=self.name, date__gte=dat[0][0], date__lte=dat[-1][0]).delete()
        for_save = []
        for row in dat:
            for_save.append(MeterData(date=row[0], value=row[1], meter_id=self.name))
        MeterData.objects.bulk_create(for_save)
