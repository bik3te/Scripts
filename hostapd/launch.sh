#!/bin/sh
echo "Stopping network manager..."
systemctl stop NetworkManager

echo "Stopping dnsmasq..."
killall dnsmasq

echo "Configuring wireless interface..."
ifconfig wlp2s0 10.0.0.1 netmask 255.255.255.0

echo "Starting dnsmasq..."
sleep 2
if [ -z "$(ps -e | grep dnsmasq)" ]
then
 dnsmasq -C ./dnsmasq.conf
fi

echo "Enabling NAT..."
ufw disable
iptables --flush
iptables --delete-chain
iptables --table nat --flush
iptables --table nat --delete-chain
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT
iptables --table nat --append POSTROUTING --out-interface eno1 -j MASQUERADE
iptables --append FORWARD --in-interface eno1 -j ACCEPT

echo "Enabling IP forwarding..."
sysctl -w net.ipv4.ip_forward=1

echo "Starting hostapd..."
hostapd ./hostapd.conf
