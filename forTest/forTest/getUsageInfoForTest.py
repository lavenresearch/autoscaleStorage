from autoScaleLog import autoscaleLog
from configHelper import configHelper
from generalConfig import generalConfig
import sys,os
import json

def executeCmd(cmd,logger):
    print cmd
    logger.writeLog(cmd)
    tmp = os.popen(cmd).read()
    print tmp
    logger.writeLog(tmp)
    return tmp

if __name__ == '__main__':
    logger = autoscaleLog(__file__)
    logger.writeLog(sys.argv)
    consumersConf = {"/home/suyi/consumer1192.168.1.162": {"remoteLV": "consumer1ca02RemoteLV", "localLV": "consumer1LocalLV", "consumerLocation": "192.168.1.162", "remoteDiskAmount": 5, "localDeviceSize": 1000, "localDevice": "/dev/loop3", "consumerID": "/home/suyi/consumer1192.168.1.162", "remoteIQN": "iqn.consumer1.ca02:dsal.disk", "localVG": "consumer1LocalVG", "mountPoint": "/home/suyi/consumer1", "localLVPath": "/dev/consumer1LocalVG/consumer1LocalLV", "extraDevicesList": [{"remoteLV": "consumer1ca02RemoteLV1", "localDeviceMap": "/dev/sdb", "remoteSize": "100", "remoteTid": 501, "groupName": "highSpeedGroup", "remoteIQN": "iqn.consumer1.ca02:dsal.disk1", "remoteLVPath": "/dev/highSpeedGroupVG/consumer1ca02RemoteLV1", "remoteVG": "highSpeedGroupVG"}, {"remoteLV": "consumer1ca02RemoteLV2", "localDeviceMap": "/dev/sdc", "remoteSize": "100", "remoteTid": 502, "groupName": "highSpeedGroup", "remoteIQN": "iqn.consumer1.ca02:dsal.disk2", "remoteLVPath": "/dev/highSpeedGroupVG/consumer1ca02RemoteLV2", "remoteVG": "highSpeedGroupVG"}, {"remoteLV": "consumer1ca02RemoteLV3", "localDeviceMap": "/dev/sdd", "remoteSize": "500", "remoteTid": 503, "groupName": "highSpeedGroup", "remoteIQN": "iqn.consumer1.ca02:dsal.disk3", "remoteLVPath": "/dev/highSpeedGroupVG/consumer1ca02RemoteLV3", "remoteVG": "highSpeedGroupVG"}, {"remoteLV": "consumer1ca02RemoteLV4", "localDeviceMap": "/dev/sde", "remoteSize": "500", "remoteTid": 504, "groupName": "highSpeedGroup", "remoteIQN": "iqn.consumer1.ca02:dsal.disk4", "remoteLVPath": "/dev/highSpeedGroupVG/consumer1ca02RemoteLV4", "remoteVG": "highSpeedGroupVG"}, {"remoteLV": "consumer1ca02RemoteLV5", "localDeviceMap": "/dev/sdf", "remoteSize": "150", "remoteTid": 505, "groupName": "highSpeedGroup", "remoteIQN": "iqn.consumer1.ca02:dsal.disk5", "remoteLVPath": "/dev/highSpeedGroupVG/consumer1ca02RemoteLV5", "remoteVG": "highSpeedGroupVG"}]}}
    providersConf = {"lowSpeedGroup": {"/dev/loop0192.168.1.162": {"deviceName": "/dev/loop0", "deviceGroup": "lowSpeedGroup", "deviceSize": 1000, "deviceType": "FCoE", "tid": "100", "deviceLocation": "192.168.1.162", "deviceIQN": "iqn.dsal.ca02:storage.disk0"}}, "highSpeedGroup": {"/dev/loop1192.168.1.162": {"deviceName": "/dev/loop1", "deviceGroup": "highSpeedGroup", "deviceSize": 1500, "deviceType": "iSCSI", "tid": "101", "deviceLocation": "192.168.1.162", "deviceIQN": "iqn.dsal.ca02:storage.disk1"}, "/dev/loop0192.168.1.131": {"deviceName": "/dev/loop0", "deviceGroup": "highSpeedGroup", "deviceSize": 1000, "deviceType": "Local SSD", "tid": "100", "deviceLocation": "192.168.1.131", "deviceIQN": "iqn.dsal.de11:storage.disk0"}}}
    usageInfo = {}
    for groupName in providersConf.keys():
        groupSize = 0
        for providerConf in providersConf[groupName].values():
            deviceSize = int(providerConf["deviceSize"])
            groupSize += deviceSize
        usageInfo[groupName] = {"groupSize": groupSize, "usedSize":0}
    for consumerConf in consumersConf.values():
        for remoteDevice in consumerConf["extraDevicesList"]:
            groupName = remoteDevice["groupName"]
            usedSize = remoteDevice["remoteSize"]
            usageInfo[groupName]["usedSize"] += int(usedSize)
    logger.writeLog(usageInfo)
    print json.dumps(usageInfo)
    logger.shutdownLog()