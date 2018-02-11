#!/bin/bash

#redirect HTTP to burp
iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 10.0.0.1:8080
iptables -t nat -A POSTROUTING -p tcp --dport 80 -j MASQUERADE

#redirect other SSL to burp
iptables -t nat -A PREROUTING -p tcp --dport 443 -j DNAT --to-destination 10.0.0.1:8080
iptables -t nat -A POSTROUTING -p tcp --dport 443 -j MASQUERADE

#redirect 8080 to burp
iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to-destination 10.0.0.1:8080
iptables -t nat -A POSTROUTING -p tcp --dport 8080 -j MASQUERADE
