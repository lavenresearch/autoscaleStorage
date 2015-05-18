import sys
from operations.startProvider import startProvider
from operations.extendGroup import extendGroup
from operations.requestStorage import requestStorage
from operations.releaseStorage import releaseStorage
from operations.startConsumer import startConsumer
from test.testAll import testAll

from interfaces import createGroup, addDeviceToGroup, addStorageConsumer, requestExtraStorage, releaseExtraStorage, getInfo, getUsageInfo

ops = ["startProvider","extendGroup","releaseStorage","requestStorage","startConsumer","testAll"]
ifs = ["createGroup", "addDeviceToGroup", "addStorageConsumer", "requestExtraStorage", "releaseExtraStorage", "getInfo", "getUsageInfo"]

if __name__ == '__main__':
    prefix = "operations."
    moduleName = sys.argv[1]
    if moduleName in ops:
        operation = globals()[moduleName]
        op = operation(sys.argv[2:])
        # op = operationa(*args, **kwargs)
        op.run()
    if moduleName in ifs:
        interface = globals()[moduleName]
        interface.run(sys.argv[2:])