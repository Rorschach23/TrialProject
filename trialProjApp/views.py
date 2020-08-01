from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import json
import datetime, time
from .models import Meter, MeterData
from .meterEntity import MeterEntity
from .forms import CreateForm

# Create your views here.

def index(request):
    meters_list = Meter.objects.all()
    form = CreateForm()
    context = {'meters_list': meters_list, 'form': form}
    return render(request, 'trialProjApp/index.html', context)

def detail(request, meter_id):
    meter = get_object_or_404(Meter, pk=meter_id)
    meterDataList = meter.meterdata_set.all()
    rangeSet = [list((m.value, m.date.strftime('%Y-%m-%d'))) for m in meterDataList]
    dump = json.dumps(rangeSet)
    yRangeSet = [time.mktime(y.date.timetuple())*1000 for y in meterDataList]
    xRangeSet = [x.value for x in meterDataList]
    xRangeSet.reverse()
    xValues = []
    if len(xRangeSet) >0:
        xValues.append(xRangeSet[0])
        for v in range(1,len(xRangeSet)):
            xValues.append(xRangeSet[v]-xRangeSet[v-1])
    return render(request, 'trialProjApp/detail.html', {'meter': meter,
                                                        'meterDataList': meterDataList,
                                                        'dump': dump,
                                                        'xRangeSet':xRangeSet,
                                                        'yRangeSet':yRangeSet,
                                                        'xValues':xValues})

def create(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            entity = MeterEntity(form.cleaned_data['name'],
                                 form.cleaned_data['resource_type'],
                                 form.cleaned_data['unit'])
            try:
                entity.createMeter()
            except (KeyError, Meter.DoesNotExist):
                return render(request, 'trialProjApp/index.html', {'response':'Oops, something went wrong!'})
            else:
                return HttpResponseRedirect(reverse('trial_app:index'))

def deleteAll(request, meter_id):
    try:
        m = MeterEntity(meter_id)
        m.deleteAllData()
        print('success')
    except (KeyError, MeterData.DoesNotExist):
        return render(request, 'trialProjApp/index.html', {'response':'Failure'})
    else:
        return HttpResponseRedirect(reverse('trial_app:detail', args=(meter_id,)))

def uploadData(request, meter_id):
    try:
        if request.method == 'POST' and request.FILES['file']:
            dat=[]
            str_text=''
            for line in request.FILES['file']:
                str_text = line.decode()
                dat.append(str_text)

            m = MeterEntity(name=meter_id)
            m.loadData(dat)
    except Exception as e:
        return render(request, 'trialProjApp/index.html', {'response':'Failure : %s'%e})
    else:
        return HttpResponseRedirect(reverse('trial_app:detail', args=(meter_id,)))

