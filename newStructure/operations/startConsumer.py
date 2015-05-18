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
    initialCmds = ["dos2unix *","service iptable stop","setenforce 0","lvmconf --disable-cluster"]
    def __init__(self):
        infoCConf = staticConfig()
        self.ipInfoC = infoCConf.getInfoCLocation()["ipInfoC"]
        self.portInfoC = infoCConf.getInfoCLocation()["portInfoC"]
        self.cHelper = configHelper(self.ipInfoC,self.portInfoC)
        self.hostIP = self.getLocalIP("eth3")
        for cmd in self.initialCmds:
            self.executeCmd(cmd)
        self.logger = autoscaleLog(__file__)

    def getLocalIP(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

    def run(self):
        consumerID = self.hostIP
        remoteConf = self.cHelper.getConsumerConf().get(consumerID)
        if remoteConf == None:
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
