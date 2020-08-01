from .models import Meter, MeterData
import datetime

class MeterEntity:

    def __init__(self, name, resource="", unit=""):
        self.name = name
        self.resource = resource
        self.unit = unit

    def createMeter(self):
        Meter.objects.create(name=self.name, resource_type=self.resource, unit=self.unit)

    def deleteAllData(self):
        meter = MeterData.objects.filter(meter_id=self.name)
        meter.delete()

    def loadData(self, dat):
        dat2=[]
        for x in dat:
            x=x.rstrip()
            x=x.split(',')
            dat2.append(x)
        dat2.pop(0)
        for x in dat2:
            x[0] = datetime.datetime.strptime(x[0], '%Y-%m-%d').date()
        self.addData(dat2)



    def addData(self, dat):
        meter = MeterData.objects.all().filter(meter_id=self.name, date__lte=dat[0][0], date__gte=dat[-1][0]).delete()
        forSave = []
        for row in dat:
            forSave.append(MeterData(date=row[0], value=row[1], meter_id=self.name))
        for row in forSave:
            row.save()
