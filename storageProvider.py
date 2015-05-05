from confingHelper import configHelper
import os
import socket
import fcntl
import struct
# deviceName == devicePath

class storageProvider():
    ipInfoC = ""
    portInfoC = 6379
    cHelper = None
    confPath = "./conf/devices.list"
    confList = []
    hostIP = ""
    initialCmds = ["dos2unix *","chmod +x *","service iptable stop","setenforce 0","lvmconf --disable-cluster"]
    def __init__(self, ipInfoC,portInfoC):
        self.ipInfoC = ipInfoC
        self.portInfoC = portInfoC
        self.cHelper = configHelper(self.ipInfoC, self.portInfoC)
        self.hostIP = self.getLocalIP("eth3")
        self.loadConf()
        for cmd in self.initialCmds:
            self.executeCmd(cmd)

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

    def loadConf(self):
        f = open(self.confPath)
        self.confList = []
        for l in f.readlines():
            conf = {}
            ll = l.split(";")
            conf["deviceName"] = ll[0]
            conf["deviceLocation"] = ll[1]
            conf["deviceIQN"] = ll[2]
            conf["deviceType"] = ll[3]
            conf["deviceGroup"] = ll[4]
            conf["tid"] = ll[5]
            if conf["deviceLocation"] == self.hostIP:
                conf["deviceSize"] = str(self.getDeviceSize(conf["deviceName"]))+" GB"
                self.confList.append(conf)
        f.close()

    def executeCmd(self,cmd):
        print cmd
        tmp = os.popen(cmd).read()
        print tmp
        return tmp

    def exportStorage(self):
        for conf in self.confList:
            cmd = "./deployStorage.sh "+conf["deviceIQN"]+" "+conf["deviceName"]+" "+conf["tid"]
            self.executeCmd(cmd)
            self.updateInfoCenter(conf)

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
    ipInfoC = "192.168.1.137"
    portInfoC = 6379
    sProvider = storageProvider(ipInfoC, portInfoC)
    sProvider.exportStorage()