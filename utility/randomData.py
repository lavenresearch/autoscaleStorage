import sys
import os
def oneWrite():
    f = open("randomData.dat","a")
    data = 0
    for i in xrange(200000000):
        strData = str(data)
        data+=i
        f.write(strData)
        os.popen("sync")
    f.close()

while True:
    tmp = os.popen("rm -f randomData.dat").read()
    oneWrite()