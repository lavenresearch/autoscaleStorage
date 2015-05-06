from confingHelper import configHelper
from autoScaleLog import autoscaleLog
import os,glob,re,time,sys
import socket
import fcntl
import struct

class storageConsumer():
    ipInfoC = ""
    portInfoC = 6379
    cHelper = None
    confPath = "./conf/consumers.list"
    confList = []
    hostIP = ""
    logger = None
    initialCmds = ["dos2unix *","chmod +x *","service iptable stop","setenforce 0","lvmconf --disable-cluster"]
    def __init__(self, ipInfoC, portInfoC):
        self.ipInfoC = ipInfoC
        self.portInfoC = portInfoC
        self.cHelper = configHelper(self.ipInfoC, self.portInfoC)
        self.hostIP = self.getLocalIP("eth3")
        self.logger = autoscaleLog(__file__)
        self.loadConf()
        if self.confList == []:
            print "consumer conf load error"
            self.logger.writeLog("consumer conf load error")
            sys.exit(1)
        for cmd in self.initialCmds:
            self.executeCmd(cmd)

    def getLocalIP(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

    def loadConf(self):
        f = open(self.confPath)
        self.confList = []
        for l in f.readlines():
            conf = {}
            ll = l.split(";")
            conf["mountPoint"] = ll[0]
            conf["consumerLocation"] = ll[1]
            conf["localVG"] = ll[2]
            conf["localLV"] = ll[3]
            conf["remoteIQN"] = ll[4]
            conf["remoteLV"] = ll[5]
            conf["localDevice"] = ll[6]
            conf["remoteDiskAmount"] = 0
            if conf["consumerLocation"] == self.hostIP:
                conf["consumerID"] = conf["mountPoint"]+conf["consumerLocation"]
                conf["localLVPath"] = "/dev/"+conf["localVG"]+"/"+conf["localLV"]
                conf["localDeviceSize"] = self.getDeviceSize(conf["localDevice"])
                self.confList.append(conf)
        f.close()

    def executeCmd(self,cmd):
        print cmd
        self.logger.writeLog(cmd)
        tmp = os.popen(cmd).read()
        print tmp
        self.logger.writeLog(tmp)
        return tmp

    def remoteCmd(self,rcmd,remoteip):
        cmd = "ssh -t root@"+remoteip+" \""+rcmd+"\""
        return self.executeCmd(cmd)

    def getDeviceSize(self,devicepathDev):
        devicepathSys = "/sys/block/"+devicepathDev.split("/")[-1]
        nr_sectors = open(devicepathSys+'/size').read().rstrip('\n')
        sect_size = open(devicepathSys+'/queue/hw_sector_size').read().rstrip('\n')
        # The sect_size is in bytes, so we convert it to MiB and then send it back
        return int((float(nr_sectors)*float(sect_size))/(1024.0*1024.0)) # in MB

    def initAllConsumers(self):
        for conf in self.confList:
            self.initConsumer(conf["consumerID"])

    def initConsumer(self,consumerID):
        for conf in self.confList:
            if conf["consumerID"] == consumerID:
                mkdirCMD = "mkdir -p "+conf["mountPoint"]
                self.executeCmd(mkdirCMD)
                pvcreateCMD = "pvcreate "+conf["localDevice"]
                self.executeCmd(pvcreateCMD)
                vgcreateCMD = "vgcreate "+conf["localVG"]+" "+conf["localDevice"]
                self.executeCmd(vgcreateCMD)
                lvcreateCMD = "lvcreate -L "+str(conf["localDeviceSize"]-100)+"M -n "+conf["localLV"]+" "+conf["localVG"]
                self.executeCmd(lvcreateCMD)
                mkfsCMD = "mkreiserfs -f "+conf["localLVPath"]
                self.executeCmd(mkfsCMD)
                mountCMD = "mount -t reiserfs "+conf["localLVPath"]+" "+conf["mountPoint"]
                self.executeCmd(mountCMD)
                remoteConf = {}
                conf["extraDevicesList"] = []
                remoteConf[conf["consumerID"]] = conf
                self.cHelper.setConsumerConf(remoteConf)

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

    def extendMountPoint(self,groupName,stepSize,consumerID):#in MB
        extraDeviceConf = {}
        remoteConsumersConf = self.cHelper.getConsumerConf()
        remoteConsumerConf = remoteConsumersConf[consumerID]
        remoteGroupManagersConf = self.cHelper.getGroupMConf()
        remoteGroupManagerConf = remoteGroupManagersConf[groupName]
        remoteConsumerConf["remoteDiskAmount"] += 1
        extraDeviceConf["remoteLV"] = remoteConsumerConf["remoteLV"]+str(remoteConsumerConf["remoteDiskAmount"])
        extraDeviceConf["remoteVG"] = groupName+"VG"
        extraDeviceConf["remoteLVPath"] = "/dev/"+extraDeviceConf["remoteVG"]+"/"+extraDeviceConf["remoteLV"]
        extraDeviceConf["remoteIQN"] = remoteConsumerConf["remoteIQN"]+str(remoteConsumerConf["remoteDiskAmount"])
        extraDeviceConf["groupName"] = groupName
        extraDeviceConf["remoteSize"] = stepSize
        remoteGroupManagerConf["currentTid"] += 1
        extraDeviceConf["remoteTid"] = remoteGroupManagerConf["currentTid"]
        groupManagerIP = remoteGroupManagerConf["gmIP"]

        # createRemoteStorage

        self.remoteCmd("lvcreate -L "+str(extraDeviceConf["remoteSize"])+"M -n "+extraDeviceConf["remoteLV"]+" "+extraDeviceConf["remoteVG"], groupManagerIP)
        status = self.remoteCmd("service tgtd status" , groupManagerIP)
        if status.find("tgtd is stopped") != -1:
            self.remoteCmd("service tgtd start" , groupManagerIP)
        self.remoteCmd("tgtadm --lld iscsi --op new --mode target --tid "+str(extraDeviceConf["remoteTid"])+" -T "+extraDeviceConf["remoteIQN"] , groupManagerIP)
        self.remoteCmd("setenforce 0;tgtadm --lld iscsi --op new --mode logicalunit --tid "+str(extraDeviceConf["remoteTid"])+" --lun 1 -b "+extraDeviceConf["remoteLVPath"] , groupManagerIP)
        self.remoteCmd("tgtadm --lld iscsi --op bind --mode target --tid "+str(extraDeviceConf["remoteTid"])+" -I ALL" , groupManagerIP)

        # loadRemoteStorage

        baseDevices = self.getDevicesInfo()
        cmdDiscovery = "iscsiadm -m discovery -t sendtargets -p " + groupManagerIP
        self.executeCmd(cmdDiscovery)
        cmdLogin = "iscsiadm -m node -T "+extraDeviceConf["remoteIQN"]+" --login"
        self.executeCmd(cmdLogin)
        time.sleep(5)
        devices = self.getDevicesInfo()
        newDevices = list(set(devices).difference(set(baseDevices)))
        print "baseDevice"+str(baseDevices)
        self.logger.writeLog("baseDevice"+str(baseDevices))
        print "allDevice"+str(devices)
        self.logger.writeLog("allDevice"+str(devices))
        print "newDevice"+str(newDevices)
        self.logger.writeLog("newDevice"+str(newDevices))
        if newDevices == []:
            print "Storage Load Failed"
            self.logger.writeLog("Storage Load Failed")
            sys.exit()

        # extendMountPoint

        for newD in newDevices:
            self.executeCmd("pvcreate "+newD)
            self.executeCmd("vgextend "+remoteConsumerConf["localVG"]+" "+newD)
            extraDeviceConf["localDeviceMap"] = newD
        newSizeMB = remoteConsumerConf["localDeviceSize"]
        for edConf in remoteConsumerConf["extraDevicesList"]:
            newSizeMB += edConf["remoteSize"]
        newSizeMB = str(newSizeMB)
        self.executeCmd("lvextend -L "+newSizeMB+"M "+remoteConsumerConf["localLVPath"])
        self.executeCmd("resize_reiserfs -s "+newSizeMB+"M "+remoteConsumerConf["localLVPath"])

        # update Information center

        self.cHelper.setGroupMConf(remoteGroupManagersConf)
        remoteConsumerConf["extraDevicesList"].append(extraDeviceConf)
        self.cHelper.setConsumerConf(remoteConsumersConf)

    def diskUsage(self,mountPoint):
        hd={}
        disk = os.statvfs(mountPoint)
        hd['available'] = float(disk.f_bsize * disk.f_bavail)/(1024*1024)
        hd['capacity'] = float(disk.f_bsize * disk.f_blocks)/(1024*1024)
        hd['used'] = float((disk.f_blocks - disk.f_bfree) * disk.f_frsize)/(1024*1024)
        for k in hd.keys():
            hd[k] = int(round(hd[k]))
        print hd
        self.logger.writeLog(hd)
        # return hd['used']/hd['capacity']
        return hd

    def autoscale(self,interval,threshold,stepSize,groupName,consumerID):
        for conf in self.confList:
            if consumerID == conf["consumerID"]:
                mountPoint = conf["mountPoint"]
        while True:
            print "sleep for"+str(interval)+"seconds"
            self.logger.writeLog("sleep for"+str(interval)+"seconds")
            time.sleep(interval)
            storageInfo = self.diskUsage(mountPoint)
            availDisk = storageInfo["available"]
            if availDisk < threshold:
                self.executeCmd("sync")
                self.extendMountPoint( groupName, stepSize, consumerID)

if __name__ == '__main__':
    ipInfoC = "192.168.1.137"
    portInfoC = 6379
    groupName = "lowSpeedGroup"
    sConsumer = storageConsumer(ipInfoC, portInfoC)
    sConsumer.initAllConsumers()




