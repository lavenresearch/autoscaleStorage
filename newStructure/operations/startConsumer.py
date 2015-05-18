from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
import os,glob,re,time,sys
import socket
import fcntl
import struct

class startConsumer():
    ipInfoC = ""
    portInfoC = 6379
    cHelper = None
    conf = {}
    hostIP = ""
    logger = None
    def __init__(self,arg):
        sConf = staticConfig()
        self.logger = autoscaleLog(__file__)
        self.ipInfoC = sConf.getInfoCLocation()["ipInfoC"]
        self.portInfoC = sConf.getInfoCLocation()["portInfoC"]
        self.cHelper = configHelper(self.ipInfoC,self.portInfoC)
        hostName = self.executeCmd("hostname")
        iframe = sConf.getHostInterface(hostName)
        self.hostIP = self.getLocalIP(iframe)

    def executeCmd(self,cmd):
        print cmd
        self.logger.writeLog(cmd)
        tmp = os.popen(cmd).read()
        print tmp
        self.logger.writeLog(tmp)
        return tmp

    def getLocalIP(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

    def run(self):
        consumerID = self.hostIP
        remoteConf = self.cHelper.getConsumerConf()
        remoteConsumerConf = remoteConf.get(consumerID)
        if remoteConsumerConf == None:
            hostName = self.executeCmd("hostname").split("\n")[0]
            remoteIQN = "iqn.dsal.consumer:"+hostName+"."+"disk"
            remoteLV = "consumer"+hostName+"remoteLV"
            remoteDiskAmount = 0
            consumerLocation = self.hostIP
            self.conf["remoteIQN"] = remoteIQN
            self.conf["remoteLV"] = remoteLV
            self.conf["remoteDiskAmount"] = remoteDiskAmount
            self.conf["consumerLocation"] = consumerLocation
            self.conf["consumerID"] = consumerID
            self.conf["extraDevicesList"] = []
            remoteConf[consumerID] = self.conf
            self.cHelper.setConsumerConf(remoteConf)
