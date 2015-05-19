import os

def executeCmd(cmd):
    print cmd
    output = os.popen(cmd).read()
    print output
    return output

def run():
    iplist = ["192.168.3.192","192.168.3.161","192.168.3.167","192.168.3.130","192.168.3.62","192.168.3.161"]
    cmd = "ssh-copy-id -i "
    executeCmd("ssh-keygen -t rsa")
    for ip in iplist:
        executeCmd(cmd+ip)