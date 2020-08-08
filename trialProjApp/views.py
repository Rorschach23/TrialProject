from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import json
import mimetypes
import os
import time
import pandas as pd
from .models import Meter, MeterData
from .meterEntity import MeterEntity
from .forms import CreateForm
from .utils import validation

# Create your views here.


def index(request):
    meters_list = Meter.objects.all()
    form = CreateForm()
    context = {'meters_list': meters_list, 'form': form}
    return render(request, 'trialProjApp/index.html', context)


def detail(request, meter_id):
    meter = get_object_or_404(Meter, pk=meter_id)
    meter_data_list = meter.meterdata_set.all().order_by('date')
    range_set = [list((m.value, m.date.strftime('%Y-%m-%d'))) for m in meter_data_list]
    dump = json.dumps(range_set)
    df = pd.DataFrame(range_set, columns=['ABSOLUTE VALUE', 'DATE'])
    y_range_set = [time.mktime(y.date.timetuple())*1000 for y in meter_data_list]
    x_range_set = [x.value for x in meter_data_list]
    x_values = []
    if len(x_range_set) > 0:
        x_values.append(x_range_set[0])
        for v in range(1, len(x_range_set)):
            x_values.append(abs(x_range_set[v]-x_range_set[v-1]))
    df['RELATIVE VALUE'] = x_values
    df.to_csv('trialProjApp/downloads/currentCSV.csv', columns=['ABSOLUTE VALUE', 'DATE', 'RELATIVE VALUE'], index=False)
    return render(request, 'trialProjApp/detail.html', {'meter': meter,
                                                        'meterDataList': meter_data_list,
                                                        'dump': dump,
                                                        'xRangeSet': x_range_set,
                                                        'yRangeSet': y_range_set[1:],
                                                        'xValues': x_values[1:]})


def create(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            entity = MeterEntity(form.cleaned_data['name'],
                                 form.cleaned_data['resource_type'],
                                 form.cleaned_data['unit'])
            try:
                entity.create_meter()
            except (KeyError, Meter.DoesNotExist):
                return render(request, 'trialProjApp/index.html', {'response': 'Oops, something went wrong!'})
            else:
                return HttpResponseRedirect(reverse('trial_app:index'))


def delete_all(request, meter_id):
    try:
        m = MeterEntity(meter_id)
        m.delete_all_data()
    except (KeyError, MeterData.DoesNotExist):
        return render(request, 'trialProjApp/index.html', {'response': 'Failure'})
    else:
        return HttpResponseRedirect(reverse('trial_app:detail', args=(meter_id,)))


def upload_data(request, meter_id):
    try:
        if request.method == 'POST' and request.FILES['file']:
            csv_file = pd.read_csv(request.FILES['file'])
            valid_response = validation(csv_file)
            if valid_response:
                return render(request, 'trialProjApp/index.html', {'response': valid_response})
            dat = []
            for line in request.FILES['file']:
                str_text = line.decode()
                dat.append(str_text)
            m = MeterEntity(name=meter_id)
            m.load_data(dat)
    except Exception as e:
        return render(request, 'trialProjApp/index.html', {'response': 'Failure : %s' % e})
    else:
        return HttpResponseRedirect(reverse('trial_app:detail', args=(meter_id,)))


def download_csv(request):
    fl_path = 'trialProjApp/downloads/currentCSV.csv'
    fp = open(fl_path, "rb")
    response = HttpResponse(fp.read())
    fp.close()
    file_type = mimetypes.guess_type(fl_path)
    if file_type is None:
        file_type = 'application/octet-stream'
    response['Content-Type'] = file_type
    response['Content-Length'] = str(os.stat(fl_path).st_size)
    response['Content-Disposition'] = "attachment; filename=currentCSV.csv"
    return response
