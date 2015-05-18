import os,time,sys,json

path = "/mnt/test"

fileIDs = ["2","3","4"]

fhs = []

datafh = open("./data.hotfile","rb")

data = datafh.read()

datafh.close()

for fid in fileIDs:
    hotfile = path+fid
    fh = open(hotfile,"wb")
    fhs.append(fh)

def writeFile(fhs):
    timeSequence = []
    beginTime = time.time()
    for i in xrange(1000):
        for fh in fhs:
            fh.seek(0)
            fh.write(data)
            timeSequence.append(time.time())
    endTime = time.time()
    return {"bt":beginTime,"et":endTime,"ts":timeSequence}

beforeMigration = writeFile(fhs)
print beforeMigration
time.sleep(10)

afterMigration = writeFile(fhs)
print afterMigration

for fh in fhs:
    fh.close()

result = {}
result["beforeMigration"] = beforeMigration
result["afterMigration"] = afterMigration
f = open("migrationEffect","w")
f.write(json.dumps(result))
f.close()
