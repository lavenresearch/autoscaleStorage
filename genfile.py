import os

cmd1 = "dd if=/dev/zero of=/autoscale/test1g"
cmd2 = "  bs=1M count=10"
count = 50
while True:
    for i in range(count):
        os.popen(cmd1+str(i)+cmd2)
        os.popen("sync")
        print "10MB writen"

print "1GB writen"
