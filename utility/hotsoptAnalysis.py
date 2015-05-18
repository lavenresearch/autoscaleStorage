from pylab import *
import seaborn as sns
import json

# load data

migrationEffect1 = {}
migrationEffect2 = {}
# f = open("migrationEffect","r")
# migrationEffect1 = json.loads(f.read())
# f.close()
f = open("migrationEffect4","r")
migrationEffect2 = json.loads(f.read())
f.close()

# show data

# sns.set_palette("Paired",2)

figure(1)

title(u"small file do not know whether migration")

# colors = sns.color_palette('Paired',2)
colors = ["yellow","blue"]

keys = ["beforeMigration","afterMigration"]
for key in keys:
    data = migrationEffect2[key]
    beginTime = data["bt"]
    timeSequence = data["ts"]
    print len(timeSequence)
    figx = []
    figy = []
    foret = beginTime
    for i in xrange(len(timeSequence)):
        v = timeSequence[i] - foret
        figx.append(i+len(timeSequence)*keys.index(key))
        figy.append(v)
        foret = timeSequence[i]
    # if key == "beforeMigration":
    # bar(figx,figy,1,color=colors[keys.index(key)],label=key)
    # else:
    plot(figx,figy,color=colors[keys.index(key)],label=key)

# draw x y axis

# ticks_pos_x = []
# for i in xrange(10):
#     ticks_pos_x.append(i*100)
# xticks(ticks_pos_x,ticks_pos_x)
xlabel("times")

# ticks_y = range(10)
# ticks_pos_y = range(10)
# yticks(ticks_pos_y,ticks_y)
ylabel("latency")

legend(loc='upper right')

# figure(2)

# title(u"3vs3, 4 process, Without data security")

# t = [u"  Initial write ",u"        Rewrite ",u"           Read ",u"        Re-read ",u"    Random read ",u"   Random write ",]

# for x in xrange(len(t)):
#     k = t[x]
#     figx = []
#     figy = []
#     for i in xrange(len(blockSize)):
#         v = results[blockSize[i]][k]
#         figx.append(i*8)
#         if v != None:
#             figy.append(v)
#         else:
#             figy.append(0)
#     plot(figx,figy,label=t[x])

# # draw x y axis

# ticks_pos_x = []
# for i in range(len(blockSize)):
#     ticks_pos_x.append(i*8)
# xticks(ticks_pos_x,blockSize)
# xlabel("Block Size")

# # ticks_y = ["100M","200M","300M","400M","500M","600M","700M","800M","900M","1G"]
# ticks_y = ["1GB","2GB","3GB"]
# gb =1048576 #KB
# ticks_pos_y = [1*gb,2*gb,3*gb]
# yticks(ticks_pos_y,ticks_y)
# ylabel("Throughput")

# legend(loc='upper left')

show()




