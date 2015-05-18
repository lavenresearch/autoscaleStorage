import os
for i in xrange(10):
    cmd = "dd if=/dev/zero of=/mnt/test"+str(i)+" bs=1M count=100"
    os.popen(cmd)
os.popen("cp /mnt/test0 ./data.hotfile")