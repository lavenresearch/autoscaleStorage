from autoScaleLog import autoscaleLog
from configHelper import configHelper
from generalConfig import generalConfig
import sys
import json

# Needed arguments including:
#
# groupName : highSpeedGroup

# For example:
#
# python createGroup.py highSpeedGroup

if __name__ == '__main__':
    logger = autoscaleLog(__file__)
    logger.writeLog(sys.argv)
    groupName = sys.argv[1]
    gConf = generalConfig()
    infoCLocation = gConf.getInfoCLocation()
    cHelper = configHelper( infoCLocation.get("ipInfoC"), infoCLocation.get("portInfoC"))
    providersConf = cHelper.getProviderConf()
    if providersConf.get(groupName) == None:
        providersConf[groupName] = {}
        cHelper.setProviderConf(providersConf)
    logger.writeLog(providersConf)
    print json.dumps(providersConf)
    logger.shutdownLog()