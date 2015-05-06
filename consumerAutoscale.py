from storageConsumer import storageConsumer
import sys
if __name__ == '__main__':
    ipInfoC = "192.168.1.137"
    portInfoC = 6379
    # interval = sys.argv[1] # in seconds
    # threshold = sys.argv[2] # in MBs
    # groupName = sys.argv[3]
    # stepSize = sys.argv[4] # in MBs
    # consumerID = sys.argv[5]
    interval = 30 # in seconds
    threshold = 300 # in MBs
    groupName = "highSpeedGroup"
    stepSize = 100 # in MBs
    consumerID = "/home/suyi/consumer1192.168.1.162"
    sConsumer = storageConsumer(ipInfoC, portInfoC)
    sConsumer.autoscale( interval, threshold, stepSize, groupName, consumerID)