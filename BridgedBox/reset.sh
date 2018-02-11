#!/bin/sh
sysctl -w net.ipv4.ip_forward=0
ifconfig br0 down
brctl delif br0 eno1
brctl delif br0 enp0s20u2 
brctl delbr br0
killall dnsmasq
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X
iptables -F
iptables -X
ebtables -t broute -F
ebtables -t broute -X
ebtables -F
ebtables -X
ufw enable
ufw default deny
systemctl start NetworkManager
