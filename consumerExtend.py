from storageConsumer import storageConsumer
import socket
import fcntl
import struct
import sys
if __name__ == '__main__':
    ipInfoC = "192.168.1.137"
    portInfoC = 6379
    # groupName = sys.argv[1]
    # stepSize = sys.argv[2]
    # consumerID = sys.argv[3]
    def getLocalIP(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])
    groupName = "highSpeedGroup"
    stepSize = 100
    consumerID = "/home/suyi/consumer1"+getLocalIP("eth3")
    sConsumer = storageConsumer(ipInfoC, portInfoC)
    sConsumer.extendMountPoint(groupName, stepSize, consumerID)