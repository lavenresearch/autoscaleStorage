import sys
import os
import glob
import re
import time

class appServer():
    mountPoint = ""
    masterName = ""
    masterIP = ""
    baseDevices = []
    deviceInUse = []
    hostName = ""
    appServerConf = {}

    initialCmds = ["yum install iscsi-initiator-utils.x86_64 -y",
                    "service iptables stop",
                    "setenforce 0",
                    "service NetworkManager stop",
                    "chkconfig NetworkManager off",
                    "lvmconf --disable-cluster"]
    def __init__(self,masterName,masterIP,mountPoint):
        self.masterName = masterName
        self.masterIP = masterIP
        self.mountPoint = mountPoint
        for cmd in self.initialCmds:
            self.executeCmd(cmd)
        # modify /etc/hosts by hand
        self.hostName = os.popen("hostname").read()[:-1]
        self.loadConf("ssdCluster","nodelist")
        if self.appServerConf == {}:
            print "appserver Conf load error"
            sys.exit()

    def executeCmd(self,cmd):
        print cmd
        tmp = os.popen(cmd).read()
        print tmp
        return tmp

    def loadConf(self,clusterName,confType):
        '''confType include disklist(for storage list) and nodelist(for appserver list)'''
        self.appServerConf = {}
        conffile = open("./conf/"+clusterName+"."+confType)
        for line in conffile.xreadlines():
            l = line.split(";")
            nodename = l[0]
            if nodename == self.hostName:
                self.appServerConf["nodename"] = l[0]
                self.appServerConf["nodeip"] = l[1]
                self.appServerConf["deviceiqn"] = l[2]
                self.appServerConf["devicepath"] = l[3]
                self.appServerConf["tid"] = l[4]
                self.appServerConf["vgname"] = l[5]
                self.appServerConf["lvname"] = l[6]
                self.appServerConf["devicepath"] = "/dev/"+self.appServerConf["vgname"]+"/"+self.appServerConf["lvname"]
        conffile.close()

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

    def mountDeviceInit(self,devicePath):
        self.executeCmd("mkdir "+self.mountPoint)
        self.executeCmd("echo \"y\"|mkreiserfs -f "+devicePath)
        self.executeCmd("mount -t reiserfs "+devicePath+" "+self.mountPoint)

    def loadShareStorage(self):
        self.baseDevices = self.getDevicesInfo()
        cmdDiscovery = "iscsiadm -m discovery -t sendtargets -p " + self.masterIP
        self.executeCmd(cmdDiscovery)
        cmdLogin = "iscsiadm -m node -T "+self.appServerConf["deviceiqn"]+" --login"
        self.executeCmd(cmdLogin)
        time.sleep(5)
        devices = self.getDevicesInfo()
        newDevices = list(set(devices).difference(set(self.baseDevices)))
        print "baseDevice"+str(self.baseDevices)
        print "allDevice"+str(devices)
        print "newDevice"+str(newDevices)
        if newDevices != []:
            self.baseDevices = devices
            self.deviceInUse = newDevices
        else:
            print "Storage Load Failed"
            sys.exit()
        return newDevices

    def diskUsage(self,mountPoint):
        hd={}
        disk = os.statvfs(mountPoint)
        hd['available'] = float(disk.f_bsize * disk.f_bavail)/(1024*1024)
        hd['capacity'] = float(disk.f_bsize * disk.f_blocks)/(1024*1024)
        hd['used'] = float((disk.f_blocks - disk.f_bfree) * disk.f_frsize)/(1024*1024)
        print hd
        # return hd['used']/hd['capacity']
        return hd

    def remoteCmd(self,rcmd,remoteip):
        cmd = "ssh -t root@"+remoteip+" \""+rcmd+"\""
        self.executeCmd(cmd)

    def monitorIostat(self,device):
        cmdIostat = "iostat -d "+self.deviceInUse[-1]+" 15 2"
        outIostat = os.popen(cmdIostat).read().split("\n")[-3]
        print outIostat
        outIostat = " ".join(outIostat.split())
        outIostat = outIostat.split(" ")[1:]
        print outIostat
        for o in outIostat:
            i = o.split(".")[0]
            if i != "0":
                print "device busy"
                return "device busy"
        print "device available"
        return "device available"

    def autoscale(self,interval,threshold,stepSize):
        while True:
            print "sleep for "+str(interval)+"seconds"
            time.sleep(interval)
            storageInfo = self.diskUsage(self.mountPoint)
            availDisk = storageInfo["available"]
            if availDisk < threshold:
                # out = "busy"
                # while out.find("busy") != -1:
                #     # self.executeCmd("sync")
                #     time.sleep(5)
                #     out = self.executeCmd("umount "+self.mountPoint)
                ioStat = self.monitorIostat(self.deviceInUse[-1])
                while ioStat == "device busy":
                    ioStat = self.monitorIostat(self.deviceInUse[-1])
                self.executeCmd("sync")
                self.executeCmd("umount "+self.mountPoint)
                self.executeCmd("iscsiadm -m node -T "+self.appServerConf["deviceiqn"]+" -p "+self.masterIP+" -u")
                self.remoteCmd("lvextend -L "+ str(storageInfo["capacity"]+stepSize) +"M /dev/"+self.appServerConf["vgname"]+"/"+self.appServerConf["lvname"] , self.masterIP)
                self.remoteCmd("resize_reiserfs -s "+str(storageInfo["capacity"]+stepSize)+"M /dev/"+self.appServerConf["vgname"]+"/"+self.appServerConf["lvname"] , self.masterIP)
                self.remoteCmd("tgtadm --lld iscsi --op delete --mode target --tid "+self.appServerConf["tid"] , self.masterIP)
                self.remoteCmd("tgtadm --lld iscsi --op new --mode target --tid "+self.appServerConf["tid"]+" -T "+self.appServerConf["deviceiqn"] , self.masterIP)
                self.remoteCmd("tgtadm --lld iscsi --op new --mode logicalunit --tid "+self.appServerConf["tid"]+" --lun 1 -b "+self.appServerConf["devicepath"] , self.masterIP)
                self.remoteCmd("tgtadm --lld iscsi --op bind --mode target --tid "+self.appServerConf["tid"]+" -I ALL" , self.masterIP)
                newDevices = self.loadShareStorage()
                for d in newDevices:
                    self.executeCmd("mount -t reiserfs "+d+" "+self.mountPoint)

if __name__ == '__main__':
    mountPoint = ""
    masterName = ""
    if len(sys.argv) == 4:
        mountPoint = sys.argv[3]
        masterName = sys.argv[2]
        masterIP = sys.argv[1]
    elif len(sys.argv) == 3:
        mountPoint = "/autoscale"
        masterName = sys.argv[2]
        masterIP = sys.argv[1]
    else:
        mountPoint = "/autoscale"
        masterName = "de01"
        masterIP = "192.168.3.121"
    appserver = appServer(masterName, masterIP, mountPoint)
    newDevices = appserver.loadShareStorage()
    for d in newDevices:
        appserver.mountDeviceInit(d)
    appserver.autoscale(30,100,100)# seconds , MB