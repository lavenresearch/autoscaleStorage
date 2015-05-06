from groupManager import groupManager
import sys

if __name__ == '__main__':
    ipInfoC = "192.168.1.137"
    portInfoC = 6379
    groupName = sys.argv[1]
    sProvider = groupManager(ipInfoC, portInfoC, groupName)
    sProvider.integrateStorageInit()
    # add some devices
    # sProvider.extendIntegrateStorage()
