from autoScaleLog import autoscaleLog
import sys,os

# Needed arguments including:
# appserverIP: "192.168.3.62"
# stepSize: 1000M
# deviceGroup: "ssdCluster"
# threshold: "1000M"
# interval: "30s"
#
# the program will add $stepSize storage from $deviceGroup for apppserver $appserverIP automatically.
#
# after operation, update the information on configuration server.

if __name__ == '__main__':
    logger = autoscaleLog(__file__)
    logger.writeLog(sys.argv)
    path = "/usr/local/src/suyiAotuscale/src/"
    interval = sys.argv[1]
    threshold = sys.argv[2]
    groupName = sys.argv[3]
    stepSize = sys.argv[4]
    consumerIP = sys.argv[5]
    consumerMountPoint = sys.argv[6]
    cmd = "ssh -t root@"+consumerIP+" \"python "+path+"consumerAutoscale.py "+interval+" "+threshold+" "+groupName+" "+stepSize+" "+consumerMountPoint+consumerIP+"\""
    print cmd
    logger.writeLog(cmd)
    result = os.popen().read()
    print result
    logger.writeLog(result)
    logger.shutdownLog()