from storageConsumer import storageConsumer
import sys
if __name__ == '__main__':
    ipInfoC = "192.168.1.137"
    portInfoC = 6379
    # groupName = sys.argv[1]
    # stepSize = sys.argv[2]
    # consumerID = sys.argv[3]
    groupName = "lowSpeedGroup"
    stepSize = 100
    consumerID = "/home/suyi/consumer1192.168.1.131"
    sConsumer = storageConsumer(ipInfoC, portInfoC)
    sConsumer.extendMountPoint(groupName, stepSize, consumerID)