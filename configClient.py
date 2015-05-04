# FOR storage provider
# [deviceName,deviceLocation(ip),deviceIQN,deviceSize,deviceGroup,deviceType]

storInfoExample = {"ssdCluster":[{"deviceName":"/dev/sdb","deviceLocation":"192.168.3.62","deviceIQN":"iqn.2222.ca01:storage.disk2","deviceSize":"10GB","deviceType":"fcoe","deviceGroup":"ssdCluster"},]}

from confingHelper import configHelper
# json.dumps(), json.loads()

class confingClient():
    consumerConfPath = ""
    consumerConf = {}
    providerConfPath = ""
    providerConf = {}
    ipInfoC = ""
    portInfoC = 6379
    cHelper = None
    def __init__(self, path, ipInfoC, portInfoC):
        self.consumerConfPath = path+"consumer.list"
        self.providerConfPath = path+"provider.list"
        self.ipInfoC = ipInfoC
        self.portInfoC = portInfoC
        self.cHelper = configHelper(self.ipInfoC, self.portInfoC)


    def loadProviderConf(self):
        f = open(self.consumerConfPath)
        for l in f.readlines():
            ll = l.split(";")
            conf = {}
            conf["deviceName"] = ll[0]
            conf["deviceLocation"] = ll[1]
            conf["deviceIQN"] = ll[2]
            conf["deviceType"] = ll[3]
            conf["deviceGroup"] = ll[4]
            conf["deviceSize"] = ll[5]
        f.close()

    def loadConsumerConf(self):
        f = open(self.providerConfPath)
        for l in f.readline():
            ll = l.split(";")
        f.close()

if __name__ == '__main__':
    path = "./conf/"
    confCenterIP = "127.0.0.1"
    port = 6379
    conf = confingClient(path, confCenterIP, port)