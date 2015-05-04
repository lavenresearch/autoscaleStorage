import redis,json

class configHelper():
    ipInfoC = ""
    portInfoC = 6379
    r = None
    groupManagerConfKey = "groupckey"
    providerConfKey = "pckey"
    comsumerConfKey = "cckey"
    def __init__(self, ipInfoC, portInfoC):
        self.ipInfoC = ipInfoC
        self.portInfoC = portInfoC
        self.r = redis.StrictRedis( host=self.ipInfoC, port=self.portInfoC, db=0)

    def setConfig(self,key,value):
        print "\nSET:\n"+value
        self.r.set(key,value)
    def getConfig(self,key):
        value = self.r.get(key)
        print "\nGET:\n"+value
        return value

    def setGroupMConf(self,conf):
        self.setConfig(self.groupManagerConfKey,json.dumps(conf))
    def getGroupMConf(self):
        confJson = self.getConfig(self.groupManagerConfKey)
        conf = json.loads(confJson)
        # print conf
        return conf

    def setProviderConf(self,conf):
        self.setConfig(self.providerConfKey,json.dumps(conf))
    def getProviderConf(self):
        confJson = self.getConfig(self.providerConfKey)
        conf = json.loads(confJson)
        # print conf
        return conf

    def setConsumerConf(self,conf):
        self.setConfig(self.comsumerConfKey,json.dumps(conf))
    def getConsumerConf(self):
        confJson = self.getConfig(self.comsumerConfKey)
        conf = json.loads(confJson)
        # print conf
        return conf


if __name__ == '__main__':
    ipInfoC = "127.0.0.1"
    portInfoC = 6379
    cHelper = configHelper(ipInfoC, portInfoC)
    redis.c
