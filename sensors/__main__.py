import sys

sys.path.append('/app')

from sensors import Sensor


if __name__ == '__main__':
    sensor = Sensor()
    sensor.start()
