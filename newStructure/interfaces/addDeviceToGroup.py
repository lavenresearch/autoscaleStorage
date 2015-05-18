from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
import sys,os

# python addDeviceToGroup.py 192.168.1.137 /dev/loop0 highSpeedGroup

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
    deviceLocation = arg[0]
    deviceName = arg[1]
    groupName = arg[2]
    sConf = staticConfig()
    path = sConf.getPath()
    infoCLocation = sConf.getInfoCLocation()
    cHelper = configHelper(infoCLocation["ipInfoC"],infoCLocation["portInfoC"])
    startProviderCmd = "ssh -t root@"+deviceLocation+" \"python "+path+"main.py startProvider "+deviceName+" "+groupName+"\""
    executeCmd(startProviderCmd)
    gmConf = cHelper.getGroupMConf().get(groupName)
    if gmConf == None:
        print "Group do not exist"
        sys.exit(1)
    gmIP = gmConf.get("gmIP")
    extendGroupCmd = "ssh -t root@"+gmIP+" \"python "+path+"main.py extendGroup "+groupName+"\""
    executeCmd(extendGroupCmd)

if __name__ == '__main__':
    deviceLocation = sys.argv[1]
    deviceName = sys.argv[2]
    groupName = sys.argv[3]
    run([deviceLocation, deviceName, groupName])