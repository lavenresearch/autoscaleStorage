from utils.autoScaleLog import autoscaleLog
import random

class staticConfig():
    staticConf = {}
    logger = None
    def __init__(self):
        self.staticConf["infoCLocation"] = {"ipInfoC":"192.168.3.130", "portInfoC":6379}
        self.staticConf["path"] = "/usr/local/src/suyiAutoscale/src/"
        self.staticConf["gmCandidates"] = ["192.168.3.130"]
        self.staticConf["hostInterfaceMap"] = {"ca01":"eth0",
                                               "ca32":"eth0",
                                               "ca07":"eth0",
                                               "de10":"eth0",
                                               "de62":"eth0",
                                               "de01":"eth0"}
        self.logger = autoscaleLog(__file__)
        self.logger.writeLog(self.staticConf)
        self.logger.shutdownLog()

    def getInfoCLocation(self):
        return self.staticConf["infoCLocation"]

    def getPath(self):
        return self.staticConf["path"]

    def getGroupMIP(self):
        gmip = random.choice(self.staticConf.get("gmCandidates"))
        return gmip
    def getHostInterface(self, hostname):
        hostnameShort = hostname.split("\n")[0].split(".")[0]
        hostInterfaceMap = self.staticConf["hostInterfaceMap"]
        return hostInterfaceMap[hostnameShort]