#!/bin/sh

# Enable IPV4 Port Forwarding
sudo sysctl -w net.ipv4.ip_forward=1

# Flush rules
sudo iptables -F

# Delete all chains
sudo iptables -X

# Add port Forwarding
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 9191

sudo iptables -t nat -L
