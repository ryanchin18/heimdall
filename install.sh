sudo apt-get install python-setuptools python-dev
easy_install pip
pip install -r requirements.txt

check ip_forward is enabled
cat /proc/sys/net/ipv4/ip_forward
if it is 0 enable it
sudo sysctl -w net.ipv4.ip_forward=1

how to make it permanent [http://www.fclose.com/1372/setting-up-gateway-using-iptables-and-route-on-linux/]



Add PYTHONPATH
export PYTHONPATH=$PYTHONPATH:/path/to/orion-ids