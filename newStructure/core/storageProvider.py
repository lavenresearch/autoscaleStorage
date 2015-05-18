from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
import os,sys
import socket
import fcntl
import struct

class storageProvider():
    ipInfoC = ""
    portInfoC = 6379
    cHelper = None
    hostIP = ""
    conf = {}
    # initialCmds = ["dos2unix *","chmod +x *","service iptable stop","setenforce 0","lvmconf --disable-cluster"]
    initialCmds = []
    logger = None
    path = "/usr/local/src/suyiAutoscale/src/"
    def __init__(self,deviceName,groupName):
        sConf = staticConfig()
        self.ipInfoC = sConf.getInfoCLocation()["ipInfoC"]
        self.portInfoC = sConf.getInfoCLocation()["portInfoC"]
        self.cHelper = configHelper(self.ipInfoC,self.portInfoC)
        hostName = self.executeCmd("hostname")
        iframe = sConf.getHostInterface(hostName)
        self.hostIP = self.getLocalIP(iframe)
        self.conf["deviceName"] = deviceName
        self.conf["deviceGroup"] = groupName
        self.loadConf()
        for cmd in self.initialCmds:
            self.executeCmd(cmd)
        self.logger = autoscaleLog(__file__)
        sConf = staticConfig()
        self.path = sConf.getPath()+"core/"

    def getLocalIP(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

    def getDeviceSize(self,devicepathDev):
        devicepathSys = "/sys/block/"+devicepathDev.split("/")[-1]
        nr_sectors = open(devicepathSys+'/size').read().rstrip('\n')
        sect_size = open(devicepathSys+'/queue/hw_sector_size').read().rstrip('\n')
        # The sect_size is in bytes, so we convert it to MiB and then send it back
        return int((float(nr_sectors)*float(sect_size))/(1024.0*1024.0)) # in MB

    def executeCmd(self,cmd):
        print cmd
        tmp = os.popen(cmd).read()
        print tmp
        return tmp

    def loadConf(self):
        hostName = self.executeCmd("hostname").split("\n")[0]
        deviceNameShort = self.conf["deviceName"].split("/")[-1]
        self.conf["deviceLocation"] = self.hostIP
        self.conf["deviceIQN"] = "iqn.dsal.storage:"+hostName+"."+deviceNameShort
        self.conf["deviceType"] = "localDisk"
        self.conf["deviceSize"] = self.getDeviceSize(self.conf["deviceName"])
        atid = self.cHelper.getAvailTid()
        tid = atid.get(self.hostIP)
        if tid == None:
            tid = 100
        self.conf["tid"] = str(tid)
        atid[self.hostIP] = tid+1
        self.cHelper.setAvailTid(atid)
        gmsConf = self.cHelper.getGroupMConf()
        gmConf = gmsConf.get(self.conf["deviceGroup"])
        if gmConf == None:
            print "Storage group do not exist!"
            self.writeLog("Storage group do not exist!")
            self.shutdownLog()
            sys.exit(1)
        self.conf["groupManagerIP"] = gmConf.get("gmIP")

    def exportStorage(self):
        cmd = self.path+"deployStorage.sh "+self.conf["deviceIQN"]+" "+self.conf["deviceName"]+" "+self.conf["tid"]+" "+self.conf["groupManagerIP"]
        self.executeCmd(cmd)
        self.updateInfoCenter(self.conf)
        self.logger.shutdownLog()

    def updateInfoCenter(self,conf):
        '''
        conf in remote.
        {
            groupname1:{deviceID1:conf1,deviceID2:conf2,},
            groupname2:{},
        }
        '''
        confRemote = self.cHelper.getProviderConf()
        confGroupRemote = confRemote.get(conf["deviceGroup"])
        if confGroupRemote == None:
            confGroupRemote = {}
        deviceID = conf["deviceName"]+conf["deviceLocation"]
        confGroupRemote[deviceID] = conf
        confRemote[conf["deviceGroup"]] = confGroupRemote
        self.cHelper.setProviderConf(confRemote)

if __name__ == '__main__':
    deviceName = "/dev/loop0"
    groupName = "newHighSpeedGroup"
    sProvider = storageProvider( deviceName, groupName)
    sProvider.exportStorage()