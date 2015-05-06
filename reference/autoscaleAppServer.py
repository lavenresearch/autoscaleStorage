import sys
import os
import glob
import re
import time
class appServer():
    clusterName = "ssdCluster"
    mountPoint = ""
    masterName = ""
    masterIP = ""
    baseDevices = []
    deviceInUse = []
    hostName = ""
    appServerConf = {}
    remoteDiskAmount = 0
    # stepSize = 100 # MB
    initialCmds = ["yum install iscsi-initiator-utils.x86_64 reiserfs-utils sysstat -y --nogpgcheck",
                    "service iptables stop",
                    "setenforce 0",
                    "service NetworkManager stop",
                    "chkconfig NetworkManager off",
                    "lvmconf --disable-cluster"]
    def __init__(self,masterName,masterIP,mountPoint,clusterName):
        self.masterName = masterName
        self.masterIP = masterIP
        self.mountPoint = mountPoint
        self.clusterName = clusterName
        for cmd in self.initialCmds:
            self.executeCmd(cmd)
        # modify /etc/hosts by hand
        self.hostName = os.popen("hostname").read()[:-1]
        self.loadConf(self.clusterName,"nodelist")
        self.remoteDiskAmount = 0
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
                self.appServerConf["localdevicepath"] = l[3]
                self.appServerConf["inittid"] = int(l[4])
                self.appServerConf["vgname"] = l[5]
                self.appServerConf["lvname"] = l[6]
                self.appServerConf["lvpath"] = "/dev/"+self.appServerConf["vgname"]+"/"+self.appServerConf["lvname"]
        conffile.close()

    def getDeviceSize(self,devicepathDev):
        devicepathSys = "/sys/block/"+devicepathDev.split("/")[-1]
        nr_sectors = open(devicepathSys+'/size').read().rstrip('\n')
        sect_size = open(devicepathSys+'/queue/hw_sector_size').read().rstrip('\n')
        # The sect_size is in bytes, so we convert it to MiB and then send it back
        return int((float(nr_sectors)*float(sect_size))/(1024.0*1024.0)) # in MB

    def mountLocalDevice(self):
        self.executeCmd("pvcreate "+self.appServerConf["localdevicepath"])
        self.executeCmd("vgcreate "+self.appServerConf["vgname"]+" "+self.appServerConf["localdevicepath"])
        self.executeCmd("lvcreate -L "+str(self.getDeviceSize(self.appServerConf["localdevicepath"])-100)+"M -n "+self.appServerConf["lvname"]+" "+self.appServerConf["vgname"])
        self.executeCmd("mkdir "+self.mountPoint)
        self.executeCmd("mkreiserfs -f "+self.appServerConf["lvpath"])
        self.executeCmd("mount -t reiserfs "+self.appServerConf["lvpath"]+" "+self.mountPoint)

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

    def remoteCmd(self,rcmd,remoteip):
        cmd = "ssh -t root@"+remoteip+" \""+rcmd+"\""
        return self.executeCmd(cmd)

    def createRemoteStorage(self,stepSize):
        self.remoteDiskAmount += 1
        lvname = self.appServerConf["lvname"]+str(self.remoteDiskAmount)
        self.remoteCmd("lvcreate -L "+str(stepSize+10)+"M -n "+lvname+" "+self.appServerConf["vgname"] , self.masterIP)
        status = self.remoteCmd("service tgtd status" , self.masterIP)
        if status.find("tgtd is stopped") != -1:
            self.remoteCmd("service tgtd start" , self.masterIP)
        tid = str(self.appServerConf['inittid']+self.remoteDiskAmount)
        iqn = self.appServerConf["deviceiqn"]+str(self.remoteDiskAmount)
        lvpath = self.appServerConf["lvpath"]+str(self.remoteDiskAmount)
        self.remoteCmd("tgtadm --lld iscsi --op new --mode target --tid "+tid+" -T "+iqn , self.masterIP)
        self.remoteCmd("setenforce 0;tgtadm --lld iscsi --op new --mode logicalunit --tid "+tid+" --lun 1 -b "+lvpath , self.masterIP)
        self.remoteCmd("tgtadm --lld iscsi --op bind --mode target --tid "+tid+" -I ALL" , self.masterIP)

    def loadRemoteStorage(self):
        self.baseDevices = self.getDevicesInfo()
        cmdDiscovery = "iscsiadm -m discovery -t sendtargets -p " + self.masterIP
        self.executeCmd(cmdDiscovery)
        cmdLogin = "iscsiadm -m node -T "+self.appServerConf["deviceiqn"]+str(self.remoteDiskAmount)+" --login"
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

    def extendMountPoint(self,newDevices,newSizeMB):
        for newD in newDevices:
            self.executeCmd("pvcreate "+newD)
            self.executeCmd("vgextend "+self.appServerConf["vgname"]+" "+newD)
        self.executeCmd("lvextend -L "+newSizeMB+"M "+self.appServerConf["lvpath"])
        self.executeCmd("resize_reiserfs -s "+newSizeMB+"M "+self.appServerConf["lvpath"])

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

    def diskUsage(self,mountPoint):
        hd={}
        disk = os.statvfs(mountPoint)
        hd['available'] = float(disk.f_bsize * disk.f_bavail)/(1024*1024)
        hd['capacity'] = float(disk.f_bsize * disk.f_blocks)/(1024*1024)
        hd['used'] = float((disk.f_blocks - disk.f_bfree) * disk.f_frsize)/(1024*1024)
        for k in hd.keys():
            hd[k] = int(round(hd[k]))
        print hd
        # return hd['used']/hd['capacity']
        return hd

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
                self.createRemoteStorage(stepSize)
                time.sleep(5)
                newD = self.loadRemoteStorage()
                ioStat = self.monitorIostat(self.deviceInUse[-1])
                while ioStat == "device busy":
                    ioStat = self.monitorIostat(self.deviceInUse[-1])
                self.executeCmd("sync")
                newSizeMB = str(storageInfo["capacity"]+stepSize)
                self.extendMountPoint(newD,newSizeMB)


if __name__ == '__main__':
    mountPoint = ""
    masterName = ""
    masterIP = ""
    clusterName = ""
    if len(sys.argv) == 5:
        clusterName = sys.argv[4]
        mountPoint = sys.argv[3]
        masterName = sys.argv[2]
        masterIP = sys.argv[1]
    elif len(sys.argv) == 4:
        clusterName = sys.argv[3]
        mountPoint = "/autoscale"
        masterName = sys.argv[2]
        masterIP = sys.argv[1]
    elif len(sys.argv) == 2:
        clusterName = sys.argv[1]
        mountPoint = "/autoscale"
        masterName = "de01"
        masterIP = "192.168.3.121"
    else:
        clusterName = "ssdCluster"
        mountPoint = "/autoscale"
        masterName = "de01"
        masterIP = "192.168.3.121"
    appserver = appServer(masterName, masterIP, mountPoint, clusterName)
    appserver.mountLocalDevice()
    appserver.autoscale(30,700,100)# (interval in seconds,threshold in MB,stepSize in MB)