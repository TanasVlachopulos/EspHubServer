import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Device
from datetime import datetime
from .data_parsing import *
from DataAccess import DBA, DAO
from DeviceCom import DataSender


# TODO handle 404 page not found error
# TODO replace test.db with config class
# TODO maximalizovat predavani hodnot do templatu - snizit pocet leteraru v templatech

def index(request):
    devices = Device.get_all()

    devices_id_lst = [device.id for device in devices]

    response = {'msg': 'Devices',
                'devices': devices,
                'devices_json': json.dumps(devices_id_lst),
                'time_to_live': 30,
                }
    return render(request, "main/index.html", response)


def device_detail(request, device_id):
    db = DBA.Dba("test.db")
    device = db.get_device(device_id)
    # device = Device.get(device_id)
    records = db.get_record_from_device(device_id, limit=10)
    # records = Record.get_all(device_id, limit=10)

    actual_values = get_actual_device_values(device_id)

    response = {'device': device,
                'values': records,
                'actual_values': actual_values,
                'device_status_interval': 30000,  # status refresh interval in seconds
                'device_values_interval': 5000,  # values refresh interval in seconds
                }
    return render(request, 'main/device_detail.html', response)


def waiting_devices(request):
    db = DBA.Dba("test.db")
    devices = db.get_waiting_devices()

    response = {'title': 'Waiting devices',
                'devices': devices,
                'input_abilities': ['sensor'],
                'output_abilities': ['display', 'switch']}
    return render(request, 'main/waiting_devices.html', response)


""" FORMS """
def verify_device(request, device_id):
    db = DBA.Dba("test.db")
    device = db.get_waiting_device(device_id)  # get waiting device for transfer to permanent devices table
    db.remove_waiting_device(device_id)  # remove device from waiting devices table

    # if hidden remove input is set to false
    if request.POST['remove-device'] == 'false':
        # sending MQTT message to device
        sender = DataSender.DataSender()
        sender.verify_device(device_id)

        # add device to database
        device.name = request.POST['device-name']
        db.insert_device(device)

    return HttpResponseRedirect(reverse('main:waiting_devices'))


def remove_device(request, device_id):
    db = DBA.Dba("test.db")
    if request.POST['remove-device'] == 'true':
        print('true')
        db.remove_device(device_id)

    return HttpResponseRedirect(reverse('main:index'))


""" API """
def waiting_devices_api(request):
    db = DBA.Dba("test.db")
    devices = db.get_waiting_devices()

    response = json.dumps([device.__dict__ for device in devices])
    return HttpResponse(response)


def telemetry_api(request, device_id):
    db = DBA.Dba('test.db')
    telemetry = db.get_telemetry(device_id)

    if telemetry:
        response = json.dumps(telemetry.__dict__)
        return HttpResponse(response)
    else:
        return HttpResponse('{}')


def device_actual_values_api(request, device_id):
    device_values = get_actual_device_values(device_id)

    # handle not serializable datetime objects in device_values
    for value in device_values:
        value['time'] = value['time'].isoformat()

    return HttpResponse(json.dumps(device_values))
