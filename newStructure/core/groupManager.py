from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
import os,glob,re,time,sys
import socket
import fcntl
import struct

class remoteDevice():
    deviceID = ""
    deviceLocation = ""
    deviceIQN = ""
    def __init__(self, deviceID, deviceLocation, deviceIQN):
        self.deviceID = deviceID
        self.deviceLocation = deviceLocation
        self.deviceIQN = deviceIQN
    def executeCmd(self,cmd):
        print cmd
        tmp = os.popen(cmd).read()
        print tmp
        return tmp
    def iscsiLogin(self):
        cmdDiscovery = "iscsiadm -m discovery -t sendtargets -p " + self.deviceLocation
        cmdLogin = "iscsiadm -m node -T " + self.deviceIQN + " -p " + self.deviceLocation + " -l"
        self.executeCmd(cmdDiscovery)
        self.executeCmd(cmdLogin)
    def printDevice(self):
        print "DEVICE INFO"
        print self.deviceID
        print self.deviceLocation
        print self.deviceIQN

class groupManager():
    ipInfoC = ""
    portInfoC = 6379
    cHelper = None
    hostIP = ""
    groupName = ""
    vgName = ""
    devicesList =[]
    groupManagerConf = {}
    initialCmds = []
    logger = None
    def __init__(self, groupName):
        sConf = staticConfig()
        self.ipInfoC = sConf.getInfoCLocation()["ipInfoC"]
        self.portInfoC = sConf.getInfoCLocation()["portInfoC"]
        self.cHelper = configHelper(self.ipInfoC,self.portInfoC)
        hostName = self.executeCmd("hostname")
        iframe = sConf.getHostInterface(hostName)
        self.hostIP = self.getLocalIP(iframe)
        self.groupName = groupName
        self.vgName = self.groupName + "VG"
        self.loadConf()
        for cmd in self.initialCmds:
            self.executeCmd(cmd)
        self.logger = autoscaleLog(__file__)

    def executeCmd(self,cmd):
        print cmd
        tmp = os.popen(cmd).read()
        print tmp
        return tmp

    def getLocalIP(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

    def loadConf(self):
        confRemote = self.cHelper.getProviderConf()
        confGroupRemote = confRemote[self.groupName]
        for conf in confGroupRemote.values():
            deviceID = conf["deviceName"]+conf["deviceLocation"]
            device = remoteDevice(deviceID, conf["deviceLocation"], conf["deviceIQN"])
            self.devicesList.append(device)

    def setGroupManagerConf(self):
        confRemote = self.cHelper.getGroupMConf()
        conf = confRemote.get(self.groupName)
        # gmip and currentTid are determined during group creation.
        #
        # conf["gmIP"] = self.hostIP
        # conf["currentTid"] = 500
        conf["devicesLoaded"] = []
        for d in self.devicesList:
            conf["devicesLoaded"].append(d.deviceID)
        confRemote[self.groupName] = conf
        self.cHelper.setGroupMConf(confRemote)

    def getDevicesInfo(self):
        devices = []
        devicesDev = []
        dev_pattern = ['sd.*']
        for device in glob.glob('/sys/block/*'):
            for pattern in dev_pattern:
                if re.compile(pattern).match(os.path.basename(device)):
                    devices.append(device)
        for d in devices:
            dpathdev = "/dev/"+d.split("/")[-1]
            devicesDev.append(dpathdev)
        return devicesDev

    def loadRemoteStorage(self, devList):
        baseDevices = self.getDevicesInfo()
        for d in devList:
            d.iscsiLogin()
        time.sleep(10)
        devices = self.getDevicesInfo()
        newDevices = list(set(devices).difference(set(baseDevices)))
        print "baseDevices"+str(baseDevices)
        self.logger.writeLog("baseDevices"+str(baseDevices))
        print "allDevices"+str(devices)
        self.logger.writeLog("allDevices"+str(devices))
        print "newDevices"+str(newDevices)
        self.logger.writeLog("newDevices"+str(newDevices))
        if newDevices == []:
            print "Storage Load Failed"
            self.logger.writeLog("Storage Load Failed")
            self.logger.shutdownLog()
            sys.exit(1)
        return newDevices

    def integrateStorageInit(self):
        newDevices = self.loadRemoteStorage(self.devicesList)
        cmdPV = "pvcreate "
        for newDev in newDevices:
            self.executeCmd(cmdPV+newDev)
        cmdVG1 = "vgcreate "+self.vgName+" "
        cmdVG2 = "vgextend "+self.vgName+" "
        self.executeCmd(cmdVG1+newDevices[0])
        for i in xrange(1,len(newDevices)):
            self.executeCmd(cmdVG2+self.newDevices[i])
        self.setGroupManagerConf()

    def getAddedDevicesInfo(self):
        confRemote = self.cHelper.getGroupMConf()
        confGroupRemote = confRemote[self.groupName]
        devicesLoadedID = confGroupRemote["devicesLoaded"]
        devicesAdded = []
        for d in self.devicesList:
            if d.deviceID not in devicesLoadedID:
                devicesAdded.append(d)
        return devicesAdded

    def extendIntegrateStorage(self):
        devicesAdded = self.getAddedDevicesInfo()
        print devicesAdded
        newDevices = self.loadRemoteStorage(devicesAdded)
        # print newDevices
        cmdPV = "pvcreate "
        for newDev in newDevices:
            self.executeCmd(cmdPV+newDev)
        cmdVG = "vgextend "+self.vgName+" "
        for i in xrange(0,len(newDevices)):
            self.executeCmd(cmdVG+newDevices[i])
        confRemote = self.cHelper.getGroupMConf()
        # print confRemote
        confGroupRemote = confRemote[self.groupName]
        # print confGroupRemote
        for d in devicesAdded:
            confGroupRemote["devicesLoaded"].append(d.deviceID)
        # print confRemote
        self.cHelper.setGroupMConf(confRemote)

if __name__ == '__main__':
    groupName = "lowSpeedGroup"
    sProvider = groupManager(groupName)
    sProvider.integrateStorageInit()
    # add some devices
    sProvider.extendIntegrateStorage()