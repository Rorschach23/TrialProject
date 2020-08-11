from django.test import TestCase, Client
from django.shortcuts import get_object_or_404
from django.urls import reverse
from datetime import date
from .models import Meter, MeterData
from .utils import validation, prepare_detail
from .meterEntity import *


# Create your tests here.


class TestViews(TestCase):

    def test_getIndex(self):
        client = Client()
        response = client.get(reverse('trial_app:index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'trialProjApp/index.html')

    def test_delete(self):
        client = Client()
        response = client.get(reverse('trial_app:deleteAll', args='a'))
        self.assertEquals(response.status_code, 302)


class TestRW(TestCase):

    error = ''

    @classmethod
    def setUpTestData(cls):
        cls.tested_meter = Meter.objects.create(name='Meter_1', resource_type='G', unit='Unit 1')
        cls.test_meter_data_one = MeterData.objects.create(date=date(2015, 11, 2), value=200.0, meter_id=cls.tested_meter.name)
        cls.test_meter_data_two = MeterData.objects.create(date=date(2015, 10, 5), value=170.0, meter_id=cls.tested_meter.name)
        cls.test_meter_data_three = MeterData.objects.create(date=date(2015, 9, 3), value=153.0, meter_id=cls.tested_meter.name)
        cls.test_meter_data_four = MeterData.objects.create(date=date(2015, 8, 2), value=100.0, meter_id=cls.tested_meter.name)

    def test_create(self):
        self.assertTrue(isinstance(self.tested_meter, Meter))
        self.assertTrue(isinstance(self.test_meter_data_one, MeterData))
        self.assertTrue(isinstance(self.test_meter_data_two, MeterData))
        self.assertTrue(isinstance(self.test_meter_data_three, MeterData))
        self.assertTrue(isinstance(self.test_meter_data_four, MeterData))

    def test_import(self):
        data = {
            'DATE': ['2015-11-13', '2015-10-05', '2015-09-03', '2015-08-02'],
            'VALUE': [10135.0, 10072.0, 10059.0, 10049.0]
        }
        valid_response = validation(data)
        self.assertTrue(type(valid_response) is not str)

    def test_check_integrity_values(self):
        data_csv = open('trialProjApp/for_test.csv', 'r')
        dat = []
        for line in data_csv:
            str_text = line
            dat.append(str_text)
        m = MeterEntity(name=self.tested_meter.name)
        m.load_data(dat)
        print(m.errors)
        meter = get_object_or_404(Meter, pk=self.tested_meter.name)
        meter_data_list = meter.meterdata_set.all().order_by('date')
        ready_data = prepare_detail(meter_data_list)
        graph_values = ready_data['xValues']
        for dif in graph_values:
            if dif < 0:
                self.error = 'Data in graph contains negative difference'
        self.assertEquals(self.error, '')
