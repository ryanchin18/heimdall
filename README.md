# Heimdall DDoS Detection #

### What is Heimdall DDoS Detection? ###

Version 0.0.1

### How to set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact

____

HOW TO ADD PROPERTIES FOR EDGES AND VERTICES

http://graph-tool.skewed.de/static/doc/graph_tool.html
new_vertex_property
new_edge_property
new_graph_property


WAYS TO HAVE REFERER
1. Meta Refrer - http://smerity.com/articles/2013/where_did_all_the_http_referrers_go.html
2. Do the same thing on server side - Add refer parameter to each query - http://stackoverflow.com/questions/9406954/jquery-replace-all-href-with-onclick-window-location


redis key patterns

storing vertex index
session::{ip}||type::vertex||hash::{hash}

storing real url for hash (for any session url hash will be the same)
session::any||type::url||hash::{hash}

storing session key for expiration
session::{ip}||type::session||hash::{some_hash}

storing http transport (hash part is the hash of the transport)
session::{ip}||type::transport||hash::{hash}

storing severity record
session::{ip}||type::severity||hash::{hash}

storing factors value map
session::{ip}||type::factors||hash::{hash}


Load redis.rdb dump to the redis server

ps -ef|grep "redis"
redis-cli SHUTDOWN
sudo stop redis-server
sudo rm -f /var/lib/redis/redis.rdb
sudo cp ~/Desktop/redis.rdb /var/lib/redis/
sudo redis-server /etc/redis/redis.conf


Redis in Mac
brew install redis

Refer to http://superuser.com/questions/504892/how-do-i-restart-redis-that-i-installed-with-brew

/usr/local/Cellar/redis//homebrew.mxcl.redis.plist will contain details about the conf (/usr/local/etc/redis.conf)

sudo redis-server /usr/local/etc/redis.conf

dump.rdb on /usr/local/var/db/redis/


Start The Orion
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 9191
cd /opt/lampp/
sudo ./xampp startmysql
sudo ./xampp startapache
