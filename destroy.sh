# destroy consumer

umount ../consumer1
lvchange -a n /dev/consumer1LocalVG/consumer1LocalLV
lvremove /dev/consumer1LocalVG/consumer1LocalLV
vgremove consumer1LocalVG
pvremove /dev/loop3
pvremove /dev/sdb
iscsiadm -m node -U all

# destroy group manager

service tgtd stop
lvremove /dev/highSpeedGroupVG/consumer1ca02RemoteLV4
vgremove highSpeedGroupVG
pvremove /dev/sdb
iscsiadm -m node -U all
