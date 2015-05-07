from autoScaleLog import autoscaleLog
import sys,os

# Needed arguments including:
#
# interval : 30 (in seconds)
# threshold : 300 (in MB)
# groupName : highSpeedGroup
# stepSize : 100 (in MB)
# consumerIP : 192.168.1.162
# consumerMountPoint : /home/suyi/consumer1
#
# the program will add $stepSize storage from $groupName for apppserver $consumerIP automatically.
#
# after operation, update the information on configuration server.


# For example:
#
# python enableAutoscale.py 30 300 highSpeedGroup 100 192.168.1.162 /home/suyi/consumer1

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
    result = os.popen(cmd).read()
    print result
    logger.writeLog(result)
    logger.shutdownLog()