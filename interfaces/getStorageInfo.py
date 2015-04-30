from autoScaleLog import autoscaleLog
import sys
import json

class storageInfo():
    storInfoExample = {"ssdCluster":[{"deviceName":"/dev/sdb","deviceLocation":"192.168.3.62","deviceIQN":"iqn.2222.ca01:storage.disk2","deviceSize":"10GB","deviceType":"fcoe"},]}
    storInfo = {}
    def __init__(self):
        pass

logger = autoscaleLog(__file__)
logger.writeLog(str(sys.argv))
logger.shutdownLog()
