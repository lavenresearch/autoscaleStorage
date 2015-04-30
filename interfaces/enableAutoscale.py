from autoScaleLog import autoscaleLog
import sys

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

logger = autoscaleLog(__file__)
logger.writeLog(str(sys.argv))
logger.shutdownLog()