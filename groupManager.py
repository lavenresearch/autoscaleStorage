from confingHelper import configHelper
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
    groupName = ""
    vgName = ""
    cHelper = None
    devicesList =[]
    groupManagerConf = {}

    def __init__(self, ipInfoC, portInfoC, groupName):
        self.ipInfoC = ipInfoC
        self.portInfoC = portInfoC
        self.groupName = groupName
        self.vgName = self.groupName + "VG"
        self.cHelper = configHelper(self.ipInfoC, self.portInfoC)
        self.loadConf()

    def loadConf(self):
        confRemote = self.cHelper.getProviderConf()
        confGroupRemote = confRemote[self.groupName]
        for conf in confGroupRemote.values():
            deviceID = conf["deviceName"]+conf["deviceLocation"]
            device = remoteDevice(deviceID, conf["deviceLocation"], conf["deviceIQN"])
            self.devicesList.append(device)

    def getLocalIP(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

    def setGroupManagerConf(self):
        conf = {}
        conf["gmIP"] = self.getLocalIP("eth0")
        conf["currentTid"] = 500
        conf["devicesLoaded"] = []
        for d in self.devicesList:
            conf["devicesLoaded"].append(d.deviceID)
        confRemote = self.cHelper.getGroupMConf()
        confRemote[self.groupName] = conf
        self.cHelper.setGroupMConf(confRemote)

    def executeCmd(self,cmd):
        print cmd
        tmp = os.popen(cmd).read()
        print tmp
        return tmp

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
        print "baseDevice"+str(self.baseDevices)
        print "allDevice"+str(devices)
        print "newDevice"+str(newDevices)
        if newDevices != []:
            self.baseDevices = devices
            self.deviceInUse = newDevices
        else:
            print "Storage Load Failed"
            sys.exit()
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
        devicesLoaded = confGroupRemote["devicesLoaded"]
        devicesAdded = []
        for d in self.devicesList:
            if d.deviceID not in devicesLoaded:
                devicesAdded.append(d)
        return devicesAdded

    def extendIntegrateStorage(self):
        devicesAdded = self.getAddedDevicesInfo()
        newDevices = self.loadRemoteStorage(devicesAdded)
        cmdPV = "pvcreate "
        for newDev in newDevices:
            self.executeCmd(cmdPV+newDev)
        cmdVG = "vgextend "+self.vgName+" "
        for i in xrange(0,len(newDevices)):
            self.executeCmd(cmdVG+self.newDevices[i])
        confRemote = self.cHelper.getGroupMConf()
        confGroupRemote = confRemote[self.groupName]
        confGroupRemote["devicesLoaded"].extend(devicesAdded)
        self.cHelper.setGroupMConf(confRemote)


if __name__ == '__main__':
    ipInfoC = "127.0.0.1"
    portInfoC = 6379
    groupName = "lowSpeedGroup"
    sProvider = groupManager(ipInfoC, portInfoC, groupName)
    sProvider.integrateStorageInit()
    # add some devices
    sProvider.extendIntegrateStorage()
