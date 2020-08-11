from .models import Meter, MeterData
import datetime
from .utils import validation


class MeterEntity:

    errors = ''

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
        query = MeterData.objects.all()
        dat_for_delete = query.filter(meter_id=self.name, date__gte=dat[0][0], date__lte=dat[-1][0])
        for_check_start = query.filter(meter_id=self.name, date__lte=dat[0][0])
        for_check_end = query.filter(meter_id=self.name, date__gte=dat[-1][0])
        if not for_check_start and not for_check_end:
            dat_for_delete.delete()
            for_save = []
            for row in dat:
                for_save.append(MeterData(date=row[0], value=row[1], meter_id=self.name))
            MeterData.objects.bulk_create(for_save)
        elif for_check_start or for_check_end:
            check = []
            range_set_start = [list((m.value, m.date.strftime('%Y-%m-%d'))) for m in for_check_start]
            if range_set_start:
                range_set_start = range_set_start[-1]
                check.append(range_set_start[0])
            check.extend([float(dat[0][1]), float(dat[-1][1])])
            range_set_end = [list((m.value, m.date.strftime('%Y-%m-%d'))) for m in for_check_end]
            if range_set_end:
                range_set_end = range_set_end[0]
                check.append(range_set_end[0])
            for x in range(1, len(check)):
                if check[x]-check[x-1] < 0:
                    self.errors = 'Integrity check failed with values %.2f (older) > %.2f (newer) (negative difference error)' % (check[x-1], check[x])
            if not self.errors:
                dat_for_delete.delete()
                for_save = []
                for row in dat:
                    for_save.append(MeterData(date=row[0], value=row[1], meter_id=self.name))
                MeterData.objects.bulk_create(for_save)
        else:
            self.errors = 'Integrity check failed'
