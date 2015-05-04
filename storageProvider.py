from confingHelper import configHelper
import os
# deviceName == devicePath

class storageProvider():
    ipInfoC = ""
    portInfoC = 6379
    cHelper = None
    confPath = "./conf/devices.list"
    confList = []
    hostName = ""
    def __init__(self, ipInfoC,portInfoC):
        self.ipInfoC = ipInfoC
        self.portInfoC = portInfoC
        self.cHelper = configHelper(self.ipInfoC, self.portInfoC)
        self.hostName = os.popen("hostname").read()[:-1]
        self.loadConf()

    def getDeviceSize(self,devicepathDev):
        devicepathSys = "/sys/block/"+devicepathDev.split("/")[-1]
        nr_sectors = open(devicepathSys+'/size').read().rstrip('\n')
        sect_size = open(devicepathSys+'/queue/hw_sector_size').read().rstrip('\n')
        # The sect_size is in bytes, so we convert it to MiB and then send it back
        return int((float(nr_sectors)*float(sect_size))/(1024.0*1024.0*1024.0)) # in GB

    def loadConf(self):
        f = open(self.consumerConfPath)
        self.confList = []
        for l in f.readlines():
            conf = {}
            ll = l.split(";")
            conf["deviceName"] = ll[0]
            conf["deviceLocation"] = ll[1]
            conf["deviceIQN"] = ll[2]
            conf["deviceType"] = ll[3]
            conf["deviceGroup"] = ll[4]
            conf["hostName"] = ll[5]
            conf["tid"] = ll[6]
            if conf["hostName"] == self.hostName:
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
        confRemote = self.cHelper.getProviderConf()
        confGroupRemote = confRemote[conf["deviceGroup"]]
        deviceID = conf["deviceName"]+conf["deviceLocation"]
        confGroupRemote[deviceID] = conf
        confRemote[conf["deviceGroup"]] = confGroupRemote
        self.cHelper.setProviderConf(confRemote)

if __name__ == '__main__':
    ipInfoC = "127.0.0.1"
    portInfoC = 6379
    sProvider = storageProvider(ipInfoC, portInfoC)