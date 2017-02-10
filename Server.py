# import datetime
# from Presentation.WebUi.DataAccess import DAO
import json
import time

from Presentation.WebUi.DeviceCom import DataCollector as Collector
from Presentation.WebUi.DeviceCom import EspDiscovery as Discovery

Collector.DataCollector('test.db', 'config')

msg = json.dumps({"name": "testServer", "ip": "192.168.1.1", "port": 1883})

esp_discovery = Discovery.EspDiscovery('192.168.1.255', 11114, msg, 5)
esp_discovery.start()


# tel = DAO.Telemetry('123', datetime.datetime.now(), '0', '0', '0', '0', '0', '0')
# print(tel._time)
# print(tel.time)

try:
    while True:
        time.sleep(0.2)
except KeyboardInterrupt:
    exit(0)