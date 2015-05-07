from remoteProcess import remoteProcess
import sys

if __name__ == '__main__':
    consumerIP = sys[1]
    remoteAS = remoteProcess("consumerAutoscale.py", consumerIP)
    remoteAS.killProcess()