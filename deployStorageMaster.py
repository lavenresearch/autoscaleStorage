# from __future__ import print_function
import glob
import re
import os
import time

class Node(object):
    nodename = ""
    nodeip = ""
    deviceiqn = ""
    devicepath = ""
    tid = ""
    def __init__(self, nodename,nodeip,deviceiqn,devicepath,tid):
        self.nodename = nodename
        self.nodeip = nodeip
        self.deviceiqn = deviceiqn
        self.devicepath = devicepath
        self.tid = tid
    def iscsiLogin(self):
        cmdDiscovery = "iscsiadm -m discovery -t sendtargets -p " + self.nodeip
        cmdLogin = "iscsiadm -m node -T " + self.deviceiqn + " -p " + self.nodeip + " -l"
        print cmdDiscovery
        tmp = os.popen(cmdDiscovery).read()
        print tmp
        print cmdLogin
        tmp = os.popen(cmdLogin).read()
        print tmp

class Cluster():
    clusterName = "ssd"
    nodes = {}
    devicesPath = []
    devicesTotalSize = 0
    lvInitialSize = 5 #GB
    vgname = "masterVG2"
    lvname = "masterLV"
    cmdDeploayStorage = "./deployStorage.sh"
    confpath = "./conf/"+clusterName+"Cluster"
    def __init__(self, clusterName):
        self.clusterName = clusterName
        self.vgname = clusterName+"masterVG3"
        self.lvname = clusterName+"masterLV"
        self.cmdDeploayStorage = "./deployStorage.sh"
        self.confpath = "./conf/"+self.clusterName+"Cluster"
        self.loadConf("disklist")
        self.executeCmd("lvmconf --disable-cluster")

    def loadConf(self,confType):
        '''confType include disklist(for storage list) and nodelist(for appserver list)'''
        self.nodes[confType] = []
        conffile = open(self.confpath+"."+confType)
        for line in conffile.xreadlines():
            l = line.split(";")
            nodename = l[0]
            nodeip = l[1]
            deviceiqn = l[2]
            devicepath = l[3]
            tid = l[4]
            n = Node(nodename, nodeip, deviceiqn, devicepath,tid)
            self.nodes[confType].append(n)

    def loadStorage(self):
        for n in self.nodes["disklist"]:
            n.iscsiLogin()

    def getDevicesInfo(self):
        self.devicesPath = []
        devicesPathSys = []
        self.devicesTotalSize = 0
        dev_pattern = ['sd.*']
        for device in glob.glob('/sys/block/*'):
            for pattern in dev_pattern:
                if re.compile(pattern).match(os.path.basename(device)):
                    devicesPathSys.append(device)
        if '/sys/block/sda' in devicesPathSys:
            devicesPathSys.remove('/sys/block/sda')
        if len(devicesPathSys) != len(self.nodes["disklist"]):
            print "WRONG NODES AMOUNT"+str(devicesPathSys)+"vs"+str(self.nodes["disklist"])
        for d in devicesPathSys:
            # dname = d.split("/")[-1][0:-1]
            nr_sectors = open(d+'/size').read().rstrip('\n')
            sect_size = open(d+'/queue/hw_sector_size').read().rstrip('\n')
            dsize = (float(nr_sectors)*float(sect_size))/(1024.0*1024.0*1024.0)
            self.devicesTotalSize += dsize
        for d in devicesPathSys:
            dpathdev = "/dev/"+d.split("/")[-1]
            self.devicesPath.append(dpathdev)

    def executeCmd(self,cmd):
        print cmd
        tmp = os.popen(cmd).read()
        print tmp

    def integrateStorage(self):
        cmdPV = "pvcreate "
        for dp in self.devicesPath:
            self.executeCmd(cmdPV+dp)
            # cmd = cmdPV + dp
            # print cmd
            # tmp = os.popen(cmd).read()
            # print tmp
        cmdVG1 = "vgcreate "+self.vgname+" "
        cmdVG2 = "vgextend "+self.vgname+" "
        self.executeCmd( cmdVG1+self.devicesPath[0] )
        # cmd = cmdVG1+self.devicesPath[0]
        # print cmd
        # tmp = os.popen(cmd).read()
        # print tmp
        for i in xrange(1,len(self.devicesPath)):
            self.executeCmd(cmdVG2+self.devicesPath[i])
            # cmd = cmdVG2+self.devicesPath[i]
            # print cmd
            # tmp = os.popen(cmd).read()
            # print tmp
        self.loadConf("nodelist")
        for node in self.nodes["nodelist"]:
            cmdLV = "lvcreate -L "+str(self.lvInitialSize)+"GB -n "+self.lvname+node.nodename+" "+self.vgname
            self.executeCmd(cmdLV)
    def iscsiTargetStart(self):
        # masterHostname = os.popen("hostname").read()[:-1]
        for node in self.nodes["nodelist"]:
            # iqn = "iqn.2222."+masterHostname+node.nodename+":storage.disk2"
            path = "/dev/"+self.vgname+"/"+self.lvname+node.nodename
            iqn = node.deviceiqn
            tid = node.tid
            # path = node.devicepath
            self.executeCmd("chmod +x "+self.cmdDeploayStorage)
            self.executeCmd(self.cmdDeploayStorage+" "+iqn+" "+path+" "+tid)


if __name__ == '__main__':
    cluster = Cluster("ssd")
    cluster.loadStorage()
    time.sleep(5)
    cluster.getDevicesInfo()
    cluster.integrateStorage()
    cluster.iscsiTargetStart()
