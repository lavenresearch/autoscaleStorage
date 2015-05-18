import os, json

class remoteProcess():
    processName = ""
    processLocation = ""
    path = './'
    def __init__(self, processName, processLocation):
        self.processName = processName
        self.processLocation = processLocation
        self.path = self.path+self.processName+self.processLocation

    def getPID(self):
        pids = []
        # cmd = "ssh -t root@"+self.processLocation+" \"ps -ef|grep "+self.processName+"\""
        # print cmd
        # output = os.popen(cmd).read()
        # print output
        cmd = "ps -ef|grep "+self.processName
        res = self.remoteCmd(cmd,self.processLocation)
        print "&&&&&&&&&&&&&&&&&&&&&&&&&"
        for line in res.split("\n"):
            line =  line.split()
            if len(line) > 0:
                processNum = line[1]
                pids.append(processNum)
        f = open(self.path,"w")
        f.write(json.dumps(pids))
        f.close()

    def killProcess(self):
        f = open(self.path,"r")
        pids = json.loads(f.read())
        f.close()
        for pid in pids:
            cmd = "kill "+str(pid)
            self.remoteCmd(cmd, self.processLocation)
        self.executeCmd("rm -f "+self.path)

    def executeCmd(self,cmd):
        print cmd
        tmp = os.popen(cmd).read()
        print tmp
        return tmp

    def remoteCmd(self,rcmd,remoteip):
        cmd = "ssh -t root@"+remoteip+" \""+rcmd+"\""
        return self.executeCmd(cmd)
