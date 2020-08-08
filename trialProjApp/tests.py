from django.test import TestCase, Client
from django.urls import reverse
from datetime import date
from .models import Meter, MeterData
from .utils import validation


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

    @classmethod
    def set_up_test_data(cls):
        cls.tested_meter = Meter.objects.create(name='Meter_1', resource_type='G', unit='Unit 1')
        cls.test_meter_data_one = MeterData.objects.create(date=date(2015, 11, 2), value=10135.0, meter_id=cls.tested_meter)
        cls.test_meter_data_two = MeterData.objects.create(date=date(2015, 10, 5), value=10072.0, meter_id=cls.tested_meter)
        cls.test_meter_data_three = MeterData.objects.create(date=date(2015, 9, 3), value=10059.0, meter_id=cls.tested_meter)
        cls.test_meter_data_four = MeterData.objects.create(date=date(2015, 8, 2), value=10049.0, meter_id=cls.tested_meter)

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
