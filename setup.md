information center : de17
storage provider low : ca02
storage provider high : ca02 de11
group manager : de17

procedure:

@ALL

    yum install iscsi-initiator-utils.x86_64 reiserfs-utils sysstat scsi-target-utils.x86_64 -y --nogpgcheck

@de17

    /home/suyi/virtualization/packages/redis-stable/src/redis-server

@ca02

    python storageProvider.py

@de17C:\Program Files\Common Files\Tencent\QQPhoneManager

    python createGroup.py highSpeedGroup
    python createGroup.py lowSpeedGroup

@de11

    python storageProvider.py

@de17

    python extendGroup.py highSpeedGroup

@ca02

    python storageConsumer.py
    <!-- python consumerExtend.py -->

@de17

    python requestExtraStorage.py 192.168.1.162 /home/suyi/consumer1 highSpeedGroup 100

@ca02

    python consumerAutoscale.py
    python genfile.py


NOTE:

1. deviceSize error. the reason for this is in storageProvider.py the getDeviceSize method return device size in GB and round down it to an integer. So the 0.9GB results in 0GB. I have changed it to return device size in MB.