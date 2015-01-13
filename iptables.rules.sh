iptables -t nat -A PREROUTING -s $CLIENT_IP -p tcp --dport 80 -j REDIRECT --to-port 8080

iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-port 1024
