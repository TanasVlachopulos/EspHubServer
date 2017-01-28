from .MessageHandler import MessageHandler
import json


class DataSender(object):
    def __init__(self):
        self.mqtt = MessageHandler('192.168.1.1')  # TODO replace with config

    def verify_device(self, device_id):
        reply = {"ip": "192.168.1.1", "port": 1883} # TODO replace with config
        self.mqtt.publish(str.format("esp_hub/device/{}/accept", device_id), json.dumps(reply), qos=1)