import os

cmd = "dd if=/dev/zero of=/autoscale/test1g bs=1M count=10"
count = 100

for i in range(100):
    os.popen(cmd)
    os.popen("sync")
    print "10MB writen"

print "1GB writen"