from autoScaleLog import autoscaleLog
import sys

logger = autoscaleLog(__file__)
logger.writeLog(str(sys.argv))
logger.shutdownLog()