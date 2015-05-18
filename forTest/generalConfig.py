from autoScaleLog import autoscaleLog

class generalConfig():
    generalConf = {}
    logger = None
    def __init__(self):
        self.generalConf["infoCLocation"] = {"ipInfoC":"192.168.3.137",
                            "portInfoC":6379}
        self.generalConf["path"] = "/usr/local/src/suyiAutoscale/src/"
        self.logger = autoscaleLog(__file__)
        self.logger.writeLog(self.generalConf)
        self.shutdownLog()

    def getInfoCLocation(self):
        return self.generalConf["infoCLocation"]

    def getPath(self):
        return self.generalConf["path"]