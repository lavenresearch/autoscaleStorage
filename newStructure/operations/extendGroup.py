from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
from core.groupManager import groupManager
import sys

class extendGroup():
    groupName = ""
    groupManager = None
    cHelper = None
    logger = None
    def __init__(self,args):
        print args
        self.groupName = args[0]
        self.groupManager = groupManager(self.groupName)
        sConf = staticConfig()
        infoCLocation = sConf.getInfoCLocation()
        self.cHelper = configHelper(infoCLocation["ipInfoC"],infoCLocation["portInfoC"])
        self.logger = autoscaleLog(__file__)
    def run(self):
        gmConf = self.cHelper.getGroupMConf().get(self.groupName)
        if gmConf == None:
            print "Group do not exist!"
            self.logger.writeLog("Group do not exist!")
            self.logger.shutdownLog()
            sys.exit(1)
        devicesLoaded = gmConf.get("devicesLoaded")
        if devicesLoaded == None:
            devicesLoaded == []
        if devicesLoaded == []:
            self.groupManager.integrateStorageInit()
        else:
            self.groupManager.extendIntegrateStorage()


