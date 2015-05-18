from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
import sys,os

# Needed arguments including:
#
# consumerIP : 192.168.1.162
# groupName : highSpeedGroup
# stepSize : 100 (in MB)
#
# the program will add $extendSize storage from $deviceGroup for apppserver $appserverIP
#
# after operation, update the information on configuration server.


# For example:
#
# python requestExtraStorage.py 192.168.1.162 highSpeedGroup 100
#
# in which the "100" means 100MB

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
    sConf = staticConfig()
    path = sConf.getPath()
    consumerLocation = arg[0]
    groupName = arg[1]
    stepSize = arg[2]
    requestStorageCmd = "ssh -t root@"+consumerLocation+" \"python "+path+"main.py requestStorage "+groupName+" "+str(stepSize)+"\""
    executeCmd(requestStorageCmd)

if __name__ == '__main__':
    consumerLocation = sys.argv[1]
    groupName = sys.argv[2]
    stepSize = sys.argv[3]
    run([consumerLocation, groupName, stepSize])