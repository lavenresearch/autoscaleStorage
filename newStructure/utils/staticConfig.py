from utils.autoScaleLog import autoscaleLog
import random

class staticConfig():
    staticConf = {}
    logger = None
    def __init__(self):
        self.staticConf["infoCLocation"] = {"ipInfoC":"192.168.3.137", "portInfoC":6379}
        self.staticConf["path"] = "/usr/local/src/suyiAutoscale/src/"
        self.staticConf["gmCandidates"] = ["192.168.3.137"]
        self.logger = autoscaleLog(__file__)
        self.logger.writeLog(self.staticConf)
        self.shutdownLog()

    def getInfoCLocation(self):
        return self.staticConf["infoCLocation"]

    def getPath(self):
        return self.staticConf["path"]

    def getGroupMIP(self):
        gmip = random.choice(self.staticConf.get("gmCandidates"))
        return gmip