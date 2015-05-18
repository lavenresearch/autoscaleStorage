import sys
from operations.extendGroup import extendGroup
from operations.requestStorage import requestStorage
from operations.releaseStorage import releaseStorage
from operations.startConsumer import startConsumer
from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog

from interfaces import createGroup, addDeviceToGroup, addStorageConsumer, requestExtraStorage, releaseExtraStorage, getInfo, getUsageInfo

# PROCEDURE:
#
# createGroup: add group information to providerConf and groupMConf
# addStorageConsumer
# getInfo
# getUsageInfo
#
# addDeviceToGroup
# addDeviceToGroup
# getInfo
# getUsageInfo
#
# requestExtraStorage
# requestExtraStorage
# getInfo
# getUsageInfo
#
# releaseExtraStorage
# getInfo
# getUsageInfo
#
# ARRANGEMENT:
#
# de62: call web interface here
# de10: information center, groupManager
# ca01, de62: storage consumers
# ca32, ca07: storage providers(/dev/loop0, /dev/loop1)

class testAll():
    cgARG1 = ["highSpeedGroup"]
    cgARG2 = ["lowSpeedGroup"]

    ascARG1 = ["192.168.3.161"]
    ascARG2 = ["192.168.3.62"]

    adtgARG1 = ["192.168.3.192","/dev/loop0","highSpeedGroup"]
    adtgARG2 = ["192.168.3.192","/dev/loop1","highSpeedGroup"]
    adtgARG3 = ["192.168.3.167","/dev/loop0","highSpeedGroup"]
    adtgARG4 = ["192.168.3.167","/dev/loop1","lowSpeedGroup"]

    rqesARG1 = ["192.168.3.161","highSpeedGroup",150]
    rqesARG2 = ["192.168.3.161","highSpeedGroup",250]
    rqesARG3 = ["192.168.3.161","lowSpeedGroup",350]
    rqesARG4 = ["192.168.3.62","highSpeedGroup",400]
    rqesARG5 = ["192.168.3.62","lowSpeedGroup",500]

    # rlesARG1
    def __init__(self):
        print "Test Program Begins"

    def viewResult(self):
        getInfo.run([])
        getUsageInfo.run([])
        raw_input("press enter to continue:")

    def run(self):
        print "Enter Test Procedure!\n"
        print "########################"
        print "createGroup"
        print "########################"
        createGroup.run(self.cgARG1)
        createGroup.run(self.cgARG2)
        self.viewResult()
        print "########################"
        print "addStorageConsumer"
        print "########################"
        addStorageConsumer.run(self.ascARG1)
        addStorageConsumer.run(self.ascARG2)
        self.viewResult()
        print "########################"
        print "addDeviceToGroup"
        print "########################"
        addDeviceToGroup.run(self.adtgARG1)
        addDeviceToGroup.run(self.adtgARG2)
        addDeviceToGroup.run(self.adtgARG3)
        addDeviceToGroup.run(self.adtgARG4)
        self.viewResult()
        print "########################"
        print "requestExtraStorage"
        print "########################"
        requestExtraStorage.run(self.rqesARG1)
        requestExtraStorage.run(self.rqesARG2)
        requestExtraStorage.run(self.rqesARG3)
        requestExtraStorage.run(self.rqesARG4)
        requestExtraStorage.run(self.rqesARG5)
        self.viewResult()
        print "########################"
        print "releaseExtraStorage"
        print "########################"
        for i in xrange(2):
            rlesARGcl = input("consumerLocation:")
            rlesARGldm = input("localDeviceMap:")
            releaseExtraStorage.run([rlesARGcl,rlesARGldm])
            self.viewResult()
