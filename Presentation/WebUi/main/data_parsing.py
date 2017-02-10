import json

from DataAccess import DBA, DAO
from DeviceCom import DataSender


def get_actual_device_values(device_id):
    db = DBA.Dba("test.db")
    device = db.get_device(device_id)

    device_values = []
    if device:  # if device exists
        print(device.provided_func)
        for func in device.provided_func:
            print(func)
            records = db.get_record_from_device(device_id, value_type=func, limit=1)  # get newest record from db
            if len(records) > 0:
                record_dict = records[0].__dict__  # select first from 1 length list and make dictionary
                record_dict['time'] = records[0].time
                device_values.append(record_dict)

    return device_values
