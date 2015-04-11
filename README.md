# Orion IDS #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

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


Redis in Mac
brew install redis

Refer to http://superuser.com/questions/504892/how-do-i-restart-redis-that-i-installed-with-brew

/usr/local/Cellar/redis//homebrew.mxcl.redis.plist will contain details about the conf (/usr/local/etc/redis.conf)

sudo redis-server /usr/local/etc/redis.conf

dump.rdb on /usr/local/var/db/redis/
