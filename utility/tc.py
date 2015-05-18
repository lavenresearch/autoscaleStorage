import os,sys

def executeCmd(cmd):
    print cmd
    r = os.popen(cmd).read()
    print r

def trafficControl(device, ip, maxbw, minbw):
    cmd = "tc qdisc add dev "+device+" root handle 1: htb default 10"
    executeCmd(cmd)
    cmd = "tc class add dev "+device+" parent 1: classid 1:1 htb rate "+minbw+"kbps ceil "+maxbw+"kbps"
    executeCmd(cmd)
    cmd = ""
