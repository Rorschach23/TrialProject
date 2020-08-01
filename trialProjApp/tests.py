from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.utils import setup_test_environment
from django.urls import reverse
import os
import json
import datetime
from .views import detail, deleteAll, create, index, uploadData

# Create your tests here.
class TestViews(TestCase):

    def test_getIndex(self):
        client = Client()
        response = client.get(reverse('trial_app:index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'trialTaskApp/index.html')

    def test_create(self):
        client = Client()
        response = client.post(reverse('trial_app:create'), {'name':'name1', 'resource':'resource1','unit':'unit1'})
        self.assertEquals(response.status_code, 302)

    def test_upload(self):
        client = Client()
        csvFile = SimpleUploadedFile('pdd_test_task_absolute_readings.csv', b"""DATE,VALUE
                                                                                2020-08-01,10900.0
                                                                                2015-11-02,10135.0
                                                                                2015-10-05,10072.0
                                                                                2015-09-03,10059.0
                                                                                2015-08-03,10049.0
                                                                                2015-07-01,10036.0
                                                                                2015-06-01,10027.0
                                                                                2015-04-30,10016.0""")
        response = client.post(reverse('trial_app:uploadData', args=['a6',]), {'file':csvFile})
        self.assertEquals(response.status_code, 200)

    def test_delete(self):
        client = Client()
        response = client.get(reverse('trial_app:deleteAll', args='a'))
        self.assertEquals(response.status_code, 302)