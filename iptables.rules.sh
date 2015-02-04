#!/bin/sh

# Enable IPV4 Port Forwarding
sudo sysctl -w net.ipv4.ip_forward=1

# Activate it permanantly
# sudo sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/g' /etc/sysctl.conf

# Activate the changes
sudo sysctl -p

# Flush rules
sudo iptables -F
sudo iptables -t nat -F

# Delete all chains
sudo iptables -X

# PREROUTING isn't used by the loopback interface, you need to also add an OUTPUT rule:
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 9191
sudo iptables -t nat -A OUTPUT -p tcp -o lo --dport 80 -j REDIRECT --to-ports 9191

sudo iptables -t nat -L
