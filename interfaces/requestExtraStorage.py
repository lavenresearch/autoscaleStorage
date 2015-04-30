from autoScaleLog import autoscaleLog
import sys

# Needed arguments including:
# appserverIP: "192.168.3.62"
# extendSize: 1000M
# deviceGroup: "ssdCluster"
#
# the program will add $extendSize storage from $deviceGroup for apppserver $appserverIP
#
# after operation, update the information on configuration server.

logger = autoscaleLog(__file__)
logger.writeLog(str(sys.argv))
logger.shutdownLog()