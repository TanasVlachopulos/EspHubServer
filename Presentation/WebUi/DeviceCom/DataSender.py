from .MessageHandler import MessageHandler
import json


class _DataSender(object):
    def __init__(self):
        self.mqtt = MessageHandler('192.168.1.1')  # TODO replace with config

    def verify_device(self, device_id):
        reply = {"ip": "192.168.1.1", "port": 1883} # TODO replace with config
        self.mqtt.publish(str.format("esp_hub/device/{}/accept", device_id), json.dumps(reply), qos=1)

    def send_data_to_device(self, device_id, value_type, value, default_value=0):
        reply = {"type": value_type, "value": value, "dvalue": default_value}
        self.mqtt.publish(str.format("esp_hub/device/{}/data", device_id), json.dumps(reply), qos=1)


class Singleton(type):
    """ Singleton meta class """
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


class DataSender(_DataSender, metaclass=Singleton):
    """ Empty class inherit from _Dba class with meta property Singleton """
    pass
