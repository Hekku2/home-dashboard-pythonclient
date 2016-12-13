#import os
#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')

from w1thermsensor import W1ThermSensor
import requests
import datetime
import ConfigParser

def ConfigSectionMap(config, section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

print("Reading config...")
config = ConfigParser.ConfigParser()
config.read('config.ini')

login = {
    'identifier': ConfigSectionMap(config, 'Server')['username'],
    'password': ConfigSectionMap(config, 'Server')['password']
}
r = requests.post(ConfigSectionMap(config, 'Server')['host'] + '/login', data = login)
token = r.json()['token']
for sensor in W1ThermSensor.get_available_sensors():
    id = ConfigSectionMap(config, 'Sensors')[sensor.id]
    payload = {
        'token': token, 
        'timestamp': datetime.datetime.now().isoformat(),
        'sensor': id,
        'value': sensor.get_temperature()
    }
    result = requests.post(ConfigSectionMap(config, 'Server')['host'] + '/measurement', data = payload)
    print(result)
    print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))
print("Reading ended")
