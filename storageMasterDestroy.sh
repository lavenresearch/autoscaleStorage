#!/bin/sh
service tgtd stop
yes | vgremove ssdmasterVG6
pvremove /dev/sdb
pvremove /dev/sdc
iscsiadm -m node -U all