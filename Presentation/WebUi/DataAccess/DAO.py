"""
============= DATABASE ACCESS OBJECTS ===============
    -   maps database entities to object representation
"""
import time

import datetime


class Device(object):
    def __init__(self, id, name, provided_func):
        self.id = id
        self.name = name

        # parse provided_function parameter if it is not a list
        # devices can send data in simple string format
        if not isinstance(provided_func, list):
            provided_func = provided_func.replace('[', '')
            provided_func = provided_func.replace(']', '')
            provided_func = provided_func.replace(';', ',')
            provided_func = provided_func.replace(' ', '')
            provided_func = provided_func.split(',')

        self.provided_func = provided_func

    def __str__(self):
        return '| ' + self.id + ' | ' + self.name + ' | ' + ';'.join(self.provided_func) + ' |'

    def to_list(self):
        return [self.id, self.name, self.provided_func]


class Record(object):
    def __init__(self, id, time, value_type, value):
        """

        :param id: unique device id - string value
        :param time: primarily in Datetime format but accept also UNIX timestamp in float and int format
        :param value_type:
        :param value:
        """
        self.id = id
        if type(time) is float or type(time) is int:
            self._time = time
        else:
            self._time = time.timestamp()
        self.value_type = value_type
        self.value = value

    @property
    def timestamp(self):
        return self._time

    @property
    def time(self):
        return datetime.datetime.fromtimestamp(self._time)

    @time.setter
    def time(self, value):
        self._time = value.timestamp()

    def __str__(self):
        return '| ' + self.id + ' | ' + time.asctime(time.localtime(self.time)) + ' | ' + self.value_type + ' | ' + self.value + '|'


class Telemetry(object):
    def __init__(self, device_id, time, rssi='0', heap='0', cycles='0', voltage='0', ip='0', mac='0', ssid='0'):
        """
        Holder of device telemetry
        :param device_id: unique device id - string value
        :param time: primarily in Datetime format but accept also UNIX timestamp in float and int format
        :param rssi: Recieved signa code power to wifi AP
        :param heap: Amount of memory on heap
        :param cycles:
        :param voltage: Device input voltage
        :param ip: Device IP address
        :param mac: Device MAC address
        """
        self.device_id = device_id
        if type(time) is float or type(time) is int:
            self._time = time
        else:
            self._time = time.timestamp()
        self.rssi = rssi
        self.heap = heap
        self.cycles = cycles
        self.voltage = voltage
        self.ip = ip
        self.mac = mac
        self.ssid = ssid

    @property
    def timestamp(self):
        return self._time

    @property
    def time(self):
        return datetime.datetime.fromtimestamp(self._time)

    @time.setter
    def time(self, value):
        self._time = value.timestamp()

    def __str__(self):
        return str.format("{} | {} | {} | {} | {} | {} | {}",
                          self.device_id, self.time, self.rssi, self.heap, self.cycles, self.voltage, self.ip, self.mac, self.ssid)