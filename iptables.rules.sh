#!/bin/sh

sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 9191

sudo iptables -t nat -L
