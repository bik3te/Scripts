#!/bin/sh
echo "Stopping network manager..."
systemctl stop NetworkManager

echo "Stopping dnsmasq..."
killall dnsmasq

echo "Configuring interfaces..."
ifconfig eno1 0.0.0.0 promisc up
ifconfig enp0s20u2 0.0.0.0 promisc up

echo "Creating bridge..."
brctl addbr br0
brctl addif br0 eno1
brctl addif br0 enp0s20u2 

echo "Configuring bridge..."
ifconfig br0 192.168.1.64 netmask 255.255.255.0 up
route add default gw 192.168.1.1 dev br0 # (IP de la box)

echo "Proxifying HTTP though Burp..."
ufw disable
iptables --flush
iptables --delete-chain
iptables --table nat --flush
iptables --table nat --delete-chain
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT
ebtables -t broute -A BROUTING -p IPv4 --ip-protocol 6 --ip-destination-port 80 -j redirect --redirect-target ACCEPT
iptables -t nat -A PREROUTING -i br0 -p tcp --dport 80 -j REDIRECT --to-port 8080
iptables --table nat --append POSTROUTING --out-interface enp0s20u2 -j MASQUERADE
iptables --append FORWARD --in-interface enp0s20u2 -j ACCEPT

echo "Enabling IP forwarding..."
sysctl -w net.ipv4.ip_forward=1
