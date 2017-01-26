from django.shortcuts import render, get_object_or_404
# from DataAccess import DBA, DAO
import importlib.util
from .models import Device, Record


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

    response = {'device': device,
                'values': [[1, 'emp', 23], [2, 'temp', 24], [3, 'temp', 23]]
                }
    return render(request, 'main/device_detail.html', response)