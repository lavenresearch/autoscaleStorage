from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
import sys,os
import json

def executeCmd(cmd):
    logger = autoscaleLog(__file__)
    print cmd
    logger.writeLog(cmd)
    output = os.popen(cmd).read()
    print output
    logger.writeLog(output)
    logger.shutdownLog()
    return output

def run(arg):
    logger = autoscaleLog(__file__)
    sConf = staticConfig()
    infoCLocation = sConf.getInfoCLocation()
    cHelper = configHelper(infoCLocation["ipInfoC"],infoCLocation["portInfoC"])
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

if __name__ == '__main__':
    run([])