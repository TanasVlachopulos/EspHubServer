# import datetime
# from Presentation.WebUi.DataAccess import DAO

from Presentation.WebUi.DeviceCom import  DataCollector as collector

collector.DataCollector('test.db', 'config')

# tel = DAO.Telemetry('123', datetime.datetime.now(), '0', '0', '0', '0', '0', '0')
# print(tel._time)
# print(tel.time)

while True:
    pass
