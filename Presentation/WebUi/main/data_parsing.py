import json

from DataAccess import DBA, DAO
from DeviceCom import DataSender


def get_actual_device_values(device_id, io_type='all'):
    db = DBA.Dba("test.db")
    device = db.get_device(device_id)

    device_values = []
    if device:
        try:
            abilities = json.loads(device.provided_func)
        except json.JSONDecodeError as e:
            print("Json decode error")  # TODO replace with log
            abilities = []

        for ability in abilities:
            # get newest record from db
            records = db.get_record_from_device(device_id, value_type=ability['name'], limit=1)

            # select type of ability
            if ability['io'] == io_type or io_type == 'all':
                # select first item from record list or create empty dictionary if record list is empty
                if len(records) > 0:
                    record_dict = records[0].__dict__
                    record_dict['time'] = records[0].time
                else:
                    record_dict = {}

                record_dict['value_type'] = ability['user_name']
                record_dict['unit'] = ability['unit']
                record_dict['category'] = ability['category']
                record_dict['io'] = ability['io']
                record_dict['desc'] = ability['desc']
                record_dict['user_name'] = ability['user_name']
                record_dict['name'] = ability['name']
                device_values.append(record_dict)

    return device_values
