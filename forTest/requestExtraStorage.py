from autoScaleLog import autoscaleLog
from generalConfig import generalConfig
import sys,os

# Needed arguments including:
#
# consumerIP : 192.168.1.162
# consumerMountPoint : /home/suyi/consumer1
# groupName : highSpeedGroup
# stepSize : 100 (in MB)
#
# the program will add $extendSize storage from $deviceGroup for apppserver $appserverIP
#
# after operation, update the information on configuration server.


# For example:
#
# python requestExtraStorage.py 192.168.1.162 /home/suyi/consumer1 highSpeedGroup 100
#
# in which the "100" means 100MB

if __name__ == '__main__':
    logger = autoscaleLog(__file__)
    logger.writeLog(str(sys.argv))
    gConf = generalConfig()
    path = gConf.getPath()
    consumerIP = sys.argv[1]
    consumerMountPoint = sys.argv[2]
    groupName = sys.argv[3]
    stepSize = sys.argv[4]
    cmd = "ssh -t root@"+consumerIP+" \"python "+path+"consumerExtend.py "+groupName+" "+stepSize+" "+consumerMountPoint+consumerIP+"\""
    print cmd
    logger.writeLog(cmd)
    result = os.popen(cmd).read()
    print result
    logger.writeLog(result)
    logger.shutdownLog()