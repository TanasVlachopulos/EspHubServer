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
