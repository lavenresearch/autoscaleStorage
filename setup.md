information center : de17
storage provider low : ca02
storage provider high : ca02 de11
group manager : de17

procedure:

@de17

    /home/suyi/virtualization/packages/redis-stable/src/redis-server

@ca02

    python storageProvider.py

@de17

    python createGroup.py highSpeedGroup
    python createGroup.py lowSpeedGroup

@de11

    python storageProvider.py

@de17

    python extendGroup.py highSpeedGroup


NOTE:

1. deviceSize error. the reason for this is in storageProvider.py the getDeviceSize method return device size in GB and round down it to an integer. So the 0.9GB results in 0GB. I have changed it to return device size in MB.