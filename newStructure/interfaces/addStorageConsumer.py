from utils.configHelper import configHelper
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog
import sys,os

# python addStorageConsumer.py consumerLocation

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
    consumerLocation = arg[0]
    sConf = staticConfig()
    path = sConf.getPath()
    cmd = "ssh -t root@"+consumerLocation+" \"python "+path+"main.py startConsumer\""
    executeCmd(cmd)

if __name__ == '__main__':
    consumerLocation = sys.argv[1]
    run([consumerLocation])