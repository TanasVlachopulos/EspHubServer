"""
========= DATABASE ACCESS ===========
    - Singleton class
    - handle database connection
    - provides methods for access to database like Insert and Select which returns Database objects
"""

import sqlite3 as sql
import DataAccess.DAO as DAO


class _Dba(object):
    """ Save path to DB file and create tables if not exists """
    def __init__(self, path):
        self._path = path
        con = self._get_connection()

        self._waiting_devices = []  # list of devices waiting for authorization

        try:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Devices(Id TEXT PRIMARY KEY, Name TEXT, Provided_func TEXT)")
            cur.execute("CREATE TABLE IF NOT EXISTS Records(Id INTEGER PRIMARY KEY, Device_id TEXT, Time NUMERIC, Type TEXT, Value TEXT)")
            cur.execute("CREATE TABLE IF NOT EXISTS WaitingDevices(Device_id TEXT PRIMARY KEY, Name TEXT, provided_func TEXT)")
        except sql.Error as e:
            if con:
                con.rollback()
                con.close()
            print("DB error: ", e.args[0])

    def add_waiting_device(self, device):
        """
        add new device to waiting queue
        primary for Data collector which collect data from new devices
        :param device: DAO device object
        """
        con = self._get_connection()
        try:
            cur = con.cursor()
            cur.execute("INSERT INTO WaitingDevices(Device_id, Name, Provided_func) VALUES (:Device_id, :Name, :Provided_func)",
                        {'Device_id': device.id, 'Name': device.name, 'Provided_func': ','.join(device.provided_func)})
            con.commit()
        except sql.Error as e:
            print(e.args[0])
        finally:
            con.close()

    def remove_waiting_device(self, device):
        """
        remove device from waiting list
        :param device: DAO device object
        """
        con = self._get_connection()
        try:
            cur = con.cursor()
            cur.execute("DELETE FROM WaitingDevices WHERE Device_id=:Device_id",
                        {'Device_id': device.id})
            con.commit()
        except sql.Error as e:
            print(e.args[0])
        finally:
            con.close()

    def get_waiting_devices(self):
        """
        :return: list of DAO device objects - waiting devices
        """
        con = self._get_connection()
        try:
            cur = con.cursor()
            cur.row_factory = sql.Row  # return data from cursor as dictionary
            cur.execute("SELECT * FROM WaitingDevices")
            rows = cur.fetchall()
            return [DAO.Device(x['Device_id'], x['Name'], x['Provided_func']) for x in rows]
        except sql.Error as e:
            print(e.args[0])
            return None
        finally:
            con.close()


    """ Get connection object """
    def _get_connection(self):
        return sql.connect(self._path)

    """ Get list of all devices """
    def get_devices(self):
        con = self._get_connection()
        try:
            cur = con.cursor()
            cur.row_factory = sql.Row  # return data from cursor as dictionary
            cur.execute("SELECT * FROM Devices")
            rows = cur.fetchall()
            return [DAO.Device(x['Id'], x['Name'], x['Provided_func']) for x in rows]
        except sql.Error as e:
            print(e.args[0])
            return None
        finally:
            con.close()

    """ Get single device by id """
    def get_device(self, device_id):
        con = self._get_connection()
        try:
            cur = con.cursor()
            cur.row_factory = sql.Row
            cur.execute("SELECT * FROM Devices WHERE Id=:Id", {'Id': device_id})
            row = (cur.fetchall())[0]  # get first record
            return DAO.Device(row['Id'], row['Name'], row['Provided_func'])
        except sql.Error as e:
            print(e.args[0])
            return None
        except IndexError:  # when does not exist any record with given id
            return None
        finally:
            con.close()

    """ Insert singe device to DB """
    def insert_device(self, device):
        con = self._get_connection()
        try:
            cur = con.cursor()
            cur.execute("INSERT INTO Devices(Id, Name, Provided_func) VALUES (:Id, :Name, :Provided_func)",
                        {'Id': device.id, 'Name': device.name, 'Provided_func': ','.join(device.provided_func)})
            con.commit()
        except sql.Error as e:
            print(e.args[0])
        finally:
            con.close()

    # def remove_device(self, device_id):
    #     con = self._get_connection()
    #     try:
    #         cur = con.cursor()
    #         cur.execute("")

    """ Update list of provided function for one device """
    def update_provided_func(self, id, function):
        con = self._get_connection()
        try:
            cur = con.cursor()
            cur.execute("UPDATE Devices SET Provided_func=:provided_func WHERE Id=:id",
                        {'provided_func': ';'.join(function), 'id': id})
            con.commit()
        except sql.Error as e:
            print(e.args[0])
        finally:
            con.close()

    """ Get all record from single device """
    def get_record_from_device(self, device_id, order='desc', limit=600):
        con = self._get_connection()
        try:
            cur = con.cursor()
            cur.row_factory = sql.Row  # return data from cursor as dictionary
            cur.execute(str.format("SELECT * FROM Records WHERE Device_id=:Device_id ORDER BY Time {} LIMIT {}", order, limit),
                        {"Device_id": device_id})
            rows = cur.fetchall()
            return [DAO.Record(x['Device_id'], sql.datetime.datetime.fromtimestamp(x['Time']), x['Type'], x['Value']) for x in rows]
        except sql.Error as e:
            print(e.args[0])
            return None
        finally:
            con.close()

    """ Insert device record """
    def insert_record(self, record):
        con = self._get_connection()
        try:
            cur = con.cursor()
            cur.execute("INSERT INTO Records(Device_id, Time, Type, Value) VALUES(:Device_id, :Time, :Type, :Value)",
                        {'Device_id': record.id, 'Time': record.time, 'Type': record.type, 'Value': record.value})
            con.commit()
        except sql.Error as e:
            print(e.args[0])
        finally:
            con.close()


class Singleton(type):
    """ Singleton meta class """
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


class Dba(_Dba, metaclass=Singleton):
    """ Empty class inherit from _Dba class with meta property Singleton """
    pass
