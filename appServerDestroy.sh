#!/bin/sh
umount /autoscale
rmdir /autoscale
vgremove shareStorageVG -ff
pvremove /dev/sd${1} -ff
iscsiadm -m node -T iqn.2222.de01:storage.disk2 -p 192.168.3.121 -u