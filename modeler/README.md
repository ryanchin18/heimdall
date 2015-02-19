HOW TO ADD PROPERTIES FOR EDGES AND VERTICES

http://graph-tool.skewed.de/static/doc/graph_tool.html
new_vertex_property
new_edge_property
new_graph_property


WAYS TO HAVE REFERER
1. Meta Refrer - http://smerity.com/articles/2013/where_did_all_the_http_referrers_go.html
2. Use Cookies - meh
3. JavaScript (May Be) - Add refer parameter to each query - http://stackoverflow.com/questions/9406954/jquery-replace-all-href-with-onclick-window-location
3. Do the same thing on server side - Add refer parameter to each query - http://stackoverflow.com/questions/9406954/jquery-replace-all-href-with-onclick-window-location


redis key patterns

storing vertex index
session:{ip}.vertex.{hash}

storing real url for hash (for any session url hash will be the same)
session:any.url.{hash}

storing session key for expiration
session:{ip}