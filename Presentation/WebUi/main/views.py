import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Device, Record
from DataAccess import DBA, DAO
from DeviceCom import DataSender

def index(request):
    devices = Device.get_all()

    test = Device('123', 'test', 'temp, hum')

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


def waiting_devices(request):
    db = DBA.Dba("test.db")
    devices = db.get_waiting_devices()

    response = {'title': 'Waiting devices',
                'devices': devices}
    return render(request, 'main/waiting_devices.html', response)


def verify_device(request, device_id):
    db = DBA.Dba("test.db")
    device = db.get_waiting_device(device_id)  # get waiting device for transfer to permanent devices table
    db.remove_waiting_device(device_id)  # remove device from waiting devices table
    # TODO send message to device
    sender = DataSender.DataSender()
    sender.verify_device(device_id)

    print(device_id)
    print(device)
    device.name = request.POST['device-name']
    db.insert_device(device)

    return HttpResponseRedirect(reverse('main:waiting_devices'))

def waiting_devices_api(request):
    db = DBA.Dba("test.db")
    devices = db.get_waiting_devices()

    response = json.dumps([device.__dict__ for device in devices])
    return HttpResponse(response)
