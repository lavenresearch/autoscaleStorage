from autoScaleLog import autoscaleLog
from confingHelper import configHelper
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
    ipInfoC = "127.0.0.1"
    portInfoC = 6379
    cHelper = configHelper( ipInfoC, portInfoC)
    consumersConf = cHelper.getConsumerConf()
    providersConf = cHelper.getProviderConf()
    allConf = {}
    allConf["dev"] = providersConf
    allConf["appserver"] = consumersConf
    logger.writeLog(allConf)
    print json.dumps(allConf)
    logger.shutdownLog()