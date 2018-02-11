#!/bin/sh
sysctl -w net.ipv4.ip_forward=0
killall dnsmasq
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X
iptables -F
iptables -X
ufw enable
ufw default deny
systemctl start NetworkManager
