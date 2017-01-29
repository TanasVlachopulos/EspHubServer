"""
============= DATABASE ACCESS OBJECTS ===============
    -   maps database entities to object representation
"""
import time


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
    def __init__(self, id, time, type, value):
        self.id = id
        self.time = time
        self.type = type
        self.value = value

    def __str__(self):
        return '| ' + self.id + ' | ' + time.asctime(time.localtime(self.time)) + ' | ' + self.type + ' | ' + self.value + '|'


class Telemetry(object):
    def __init__(self, device_id, time, rssi, heap, cycles, voltage, ip, mac):
        self.device_id = device_id
        self.time = time
        self.rssi = rssi
        self.heap = heap
        self.cycles = cycles
        self.voltage = voltage
        self.ip = ip
        self.mac = mac

    def __str__(self):
        return str.format("{} | {} | {} | {} | {} | {}",
                          self.device_id, self.time, self.rssi, self.heap, self.cycles, self.voltage, self.ip, self.mac)