from autoScaleLog import autoscaleLog
from configHelper import configHelper
from generalConfig import generalConfig
import sys,os
import json

def executeCmd(cmd,logger):
    print cmd
    logger.writeLog(cmd)
    tmp = os.popen(cmd).read()
    print tmp
    logger.writeLog(tmp)
    return tmp

if __name__ == '__main__':
    logger = autoscaleLog(__file__)
    logger.writeLog(sys.argv)
    gConf = generalConfig()
    infoCLocation = gConf.getInfoCLocation()
    cHelper = configHelper( infoCLocation.get("ipInfoC"), infoCLocation.get("portInfoC"))
    consumersConf = cHelper.getConsumerConf()
    providersConf = cHelper.getProviderConf()
    allConf = {}
    allConf["dev"] = providersConf
    allConf["appserver"] = consumersConf
    logger.writeLog(allConf)
    print json.dumps(allConf)
    logger.shutdownLog()