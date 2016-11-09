#import os
#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')

from w1thermsensor import W1ThermSensor

print("Printing")
for sensor in W1ThermSensor.get_available_sensors():
    print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))
print("Printing ended")
