import sys
import os
import glob
import re
import random
import string
import time

class appServer():
    mountPoint = ""
    masterName = ""
    deviceiqn = ""
    baseDevices = []
    hostName = ""
    vgname = ""
    lvname = ""
    initSize = 5
    initialCmds = ["yum install iscsi-initiator-utils.x86_64 -y",
                    "service iptables stop",
                    "setenforce 0",
                    "service NetworkManager stop",
                    "chkconfig NetworkManager off",
                    "lvmconf --enable-cluster"]
    def __init__(self,masterName,mountpoint):
        self.masterName = masterName
        self.mountPoint = mountPoint
        self.deviceiqn = "iqn.2222."+self.masterName+":storage.disk2"
        for cmd in self.initialCmds:
            self.executeCmd(cmd)
        # modify /etc/hosts by hand
        self.baseDevices = self.getDevicesInfo()
        self.hostName = os.popen("hostname").read().split("\n")[0]
        sessionid = string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a','0','2','3','4','5','6','7','8','9'], 10)).replace(' ','')
        self.vgname = self.hostName+"VG"+sessionid
        self.vgname = "shareStorageVG"
        self.lvname = self.hostName+"LV"+sessionid

    def executeCmd(self,cmd):
        print cmd
        tmp = os.popen(cmd).read()
        print tmp

    def getDevicesInfo(self):
        devices = []
        devicesDev = []
        dev_pattern = ['sd.*']
        for device in glob.glob('/sys/block/*'):
            for pattern in dev_pattern:
                if re.compile(pattern).match(os.path.basename(device)):
                    devices.append(device)
        for d in devices:
            dpathdev = "/dev/"+d.split("/")[-1]
            devicesDev.append(dpathdev)
        return devicesDev
        # if '/dev/sda1' in devices:
        #     devices.remove('/dev/sda1')

    def integrateDevices(self,devices):
        # cmdPV = "pvcreate "
        # for dp in devices:
        #     self.executeCmd(cmdPV+dp)
        #     # cmd = cmdPV + dp
        #     # print cmd
        #     # tmp = os.popen(cmd).read()
        #     # print tmp
        # cmdVG1 = "vgcreate "+self.vgname+" "
        # cmdVG2 = "vgextend "+self.vgname+" "
        # self.executeCmd( cmdVG1+devices[0] )
        # # cmd = cmdVG1+devices[0]
        # # print cmd
        # # tmp = os.popen(cmd).read()
        # # print tmp
        # for i in xrange(1,len(devices)):
        #     self.executeCmd(cmdVG2+devices[i])
            # cmd = cmdVG2+devices[i]
            # print cmd
            # tmp = os.popen(cmd).read()
            # print tmp
        cmdLV = "lvcreate -L "+str(self.initSize)+"GB -n "+self.lvname+" "+self.vgname
        self.executeCmd(cmdLV)

    def loadShareStorage(self):
        cmdDiscovery = "iscsiadm -m discovery -t sendtargets -p " + self.masterName
        self.executeCmd(cmdDiscovery)
        cmdLogin = "iscsiadm -m node -T "+self.deviceiqn+" --login"
        self.executeCmd(cmdLogin)
        time.sleep(5)
        devices = self.getDevicesInfo()
        newDevices = list(set(devices).difference(set(self.baseDevices)))
        print "baseDevice"+str(self.baseDevices)
        print "allDevice"+str(devices)
        print "newDevice"+str(newDevices)
        if newDevices != []:
            self.baseDevices = devices
            self.integrateDevices(newDevices)
        else:
            print "Storage Load Failed"

    def mountDevices(self):
        devicePath = "/dev/"+self.vgname+"/"+self.lvname
        self.executeCmd("mkdir "+self.mountPoint)
        self.executeCmd("mkreiserfs -f "+devicePath)
        self.executeCmd("mount -t reiserfs "+devicePath+" "+self.mountPoint)

if __name__ == '__main__':
    mountPoint = ""
    masterName = ""
    if len(sys.argv) == 3:
        mountPoint = sys.argv[2]
        masterName = sys.argv[1]
    elif len(sys.argv) == 2:
        mountPoint = "/autoscale"
        masterName = sys.argv[1]
    else:
        mountPoint = "/authscale"
        masterName = "de01"
    appserver = appServer(masterName, mountPoint)
    appserver.loadShareStorage()
    appserver.mountDevices()



