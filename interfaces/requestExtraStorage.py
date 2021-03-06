from autoScaleLog import autoscaleLog
import sys,os

# Needed arguments including:
# appserverIP: "192.168.3.62"
# extendSize: 1000M
# deviceGroup: "ssdCluster"
#
# the program will add $extendSize storage from $deviceGroup for apppserver $appserverIP
#
# after operation, update the information on configuration server.

if __name__ == '__main__':
    logger = autoscaleLog(__file__)
    logger.writeLog(str(sys.argv))
    path = "/usr/local/src/suyiAotuscale/src/"
    consumerIP = sys.argv[1]
    consumerMountPoint = sys.argv[2]
    groupName = sys.argv[3]
    stepSize = sys.argv[4]
    cmd = "ssh -t root@"+consumerIP+" \"python "+path+"consumerExtend.py "+groupName+" "+stepSize+" "+consumerMountPoint+consumerIP+"\""
    print cmd
    logger.writeLog(cmd)
    result = os.popen().read()
    print result
    logger.writeLog(result)
    logger.shutdownLog()