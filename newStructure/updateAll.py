import os
from utils.staticConfig import staticConfig
from utils.autoScaleLog import autoscaleLog

class updateAll():
    destinationIP = ""
    path = ""
    def __init__(self, arg):
        self.destinationIP = arg
        sConf = staticConfig()
        self.path = sConf.getPath()
        # self.executeCmd("ssh-copy-id -i "+self.destinationIP)

    def executeCmd(self, cmd):
        logger = autoscaleLog(__file__)
        print cmd
        logger.writeLog(cmd)
        output = os.popen(cmd).read()
        print output
        logger.writeLog(output)
        logger.shutdownLog()
        return output

    def executeRemoteCmd(self, rcmd , remoteip):
        cmd = "ssh -t root@"+remoteip+" \""+rcmd+"\""
        self.executeCmd(cmd)

    def run(self):
        rcmd = "rm -rf "+self.path
        self.executeRemoteCmd(rcmd, self.destinationIP)
        rcmd = "mkdir -p "+self.path
        self.executeRemoteCmd(rcmd, self.destinationIP)
        cmd = "scp -r "+self.path+"* root@"+self.destinationIP+":"+self.path
        self.executeCmd(cmd)
        rcmd = "dos2unix "+self.path+"*/*.sh"
        self.executeRemoteCmd(rcmd, self.destinationIP)
        rcmd = "chmod +x "+self.path+"*/*.sh"
        self.executeRemoteCmd(rcmd, self.destinationIP)


if __name__ == '__main__':
    iplist = ["192.168.3.192","192.168.3.161","192.168.3.167","192.168.3.130","192.168.3.121"]
    for ip in iplist:
        ua = updateAll(ip)
        ua.run()
