import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Device, Record
from DataAccess import DBA, DAO


def index(request):
    devices = Device.get_all()

    test = Device('123', 'test', 'temp, hum')
    print("test")
    print(test.provided_func)

    response = {'msg': 'Records',
                'devices': devices,
                }
    return render(request, "main/index.html", response)


def device_detail(request, device_id):
    device = Device.get(device_id)
    records = Record.get_all(device_id, limit=10)

    response = {'device': device,
                'values': records
                }
    return render(request, 'main/device_detail.html', response)


def waiting_devices_api(request):
    db = DBA.Dba("test.db")
    devices = db.get_waiting_devices()
    print(len(devices))

    response = json.dumps([device.__dict__ for device in devices])
    return HttpResponse(response)