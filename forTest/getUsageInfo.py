from autoScaleLog import autoscaleLog
from configHelper import configHelper
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
    ipInfoC = "192.168.1.137"
    portInfoC = 6379
    cHelper = configHelper( ipInfoC, portInfoC)
    consumersConf = cHelper.getConsumerConf()
    providersConf = cHelper.getProviderConf()
    usageInfo = {}
    for groupName in providersConf.keys():
        groupSize = 0
        for providerConf in providersConf[groupName].values():
            deviceSize = int(providerConf["deviceSize"])
            groupSize += deviceSize
        usageInfo[groupName] = {"groupSize": groupSize, "usedSize":0}
    for consumerConf in consumersConf.values():
        for remoteDevice in consumerConf["extraDevicesList"]:
            groupName = remoteDevice["groupName"]
            usedSize = remoteDevice["remoteSize"]
            usageInfo[groupName]["usedSize"] += int(usedSize)
    logger.writeLog(usageInfo)
    print json.dumps(usageInfo)
    logger.shutdownLog()