# import datetime
# from Presentation.WebUi.DataAccess import DAO

import time

from Presentation.WebUi.DeviceCom import DataCollector as collector

collector.DataCollector('test.db', 'config')

# tel = DAO.Telemetry('123', datetime.datetime.now(), '0', '0', '0', '0', '0', '0')
# print(tel._time)
# print(tel.time)

try:
    while True:
        time.sleep(0.2)
except KeyboardInterrupt:
    exit(0)