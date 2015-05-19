from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
import sys
import json

# Needed arguments including:
#
# groupName : highSpeedGroup

# For example:
#
# python createGroup.py highSpeedGroup

def run(arg):
    logger = autoscaleLog(__file__)
    logger.writeLog(sys.argv)
    groupName = arg[0]
    sConf = staticConfig()
    infoCLocation = sConf.getInfoCLocation()
    cHelper = configHelper( infoCLocation.get("ipInfoC"), infoCLocation.get("portInfoC"))
    providersConf = cHelper.getProviderConf()
    if providersConf.get(groupName) == None:
        providersConf[groupName] = {}
        cHelper.setProviderConf(providersConf)
    logger.writeLog(providersConf)
    print json.dumps(providersConf)
    gmConf = cHelper.getGroupMConf()
    groupAmount = len(gmConf)
    if gmConf.get(groupName) == None:
        gmConf[groupName] = {}
        gmConf[groupName]["currentTid"] = 500+200*groupAmount
        gmConf[groupName]["gmIP"] = sConf.getGroupMIP()
        gmConf[groupName]["devicesLoaded"] = []
        cHelper.setGroupMConf(gmConf)
    logger.writeLog(gmConf)
    print json.dumps(gmConf)
    logger.shutdownLog()

if __name__ == '__main__':
    groupName = sys.argv[1]
    run(groupName)