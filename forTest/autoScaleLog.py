import logging

class autoscaleLog():
    """docstring for autoscaleLog"""
    logSource = ""

    def __init__(self, source):
        self.logSource = source
        self.logPath = "./suyiAutoscale.log"
        # logging.basicConfig(filename=self.flogPath,filemode='a',level=logging.DEBUG,format='%(asctime)s - %(filename)s[func:%(funcName)s ; line:%(lineno)d] %(levelname)s\t: %(message)s')
        # self.fLogger = logging.getLogger("root.fullLog")
        logging.basicConfig(filename=self.logPath,filemode='a',level=logging.DEBUG,format='%(asctime)s - '+self.logSource+'\t: %(message)s')

    def writeLog(self,msg):
        msg = str(msg)
        logging.debug(msg)

    def shutdownLog(self):
        logging.shutdown()


if __name__ == '__main__':
    al = autoscaleLog("test")
    al.writeLog("skljdfklajsdf")
    al.writeLog("sdjijskdfjsakldj")
    al.shutdownLog()