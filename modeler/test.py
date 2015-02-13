__author__ = 'grainier'

import graph_tool.all as gt

g = gt.complete_graph(30)
sub = gt.complete_graph(10)
vm = gt.subgraph_isomorphism(sub, g, max_n=100)
print(len(vm))

for i in range(len(vm)):
    g.set_vertex_filter(None)
    g.set_edge_filter(None)
    vmask, emask = gt.mark_subgraph(g, sub, vm[i])
    g.set_vertex_filter(vmask)
    g.set_edge_filter(emask)
    assert gt.isomorphism(g, sub)
g.set_vertex_filter(None)
g.set_edge_filter(None)
ewidth = g.copy_property(emask, value_type="double")
ewidth.a += 0.5
ewidth.a *= 2
gt.graph_draw(g, vertex_fill_color=vmask, edge_color=emask,
              edge_pen_width=ewidth, output_size=(200, 200),
              output="subgraph-iso-embed.pdf")
gt.graph_draw(sub, output_size=(200, 200), output="subgraph-iso.pdf")


# initialize graph
graph = gt.Graph()

# add graph properties
graph.graph_properties["ip"] = graph.new_graph_property("string", "192.168.1.100")

# add edge properties
graph.edge_properties["referer"] = graph.new_edge_property("string")

# add vertex properties
graph.vertex_properties["accept"] = graph.new_vertex_property("string")
graph.vertex_properties["accept_language"] = graph.new_vertex_property("string")
graph.vertex_properties["accept_encoding"] = graph.new_vertex_property("string")
graph.vertex_properties["dnt"] = graph.new_vertex_property("string")
graph.vertex_properties["connection"] = graph.new_vertex_property("string")
graph.vertex_properties["cache_control"] = graph.new_vertex_property("string")
graph.vertex_properties["data_length"] = graph.new_vertex_property("int")
graph.vertex_properties["content_length"] = graph.new_vertex_property("int")
graph.vertex_properties["content_size"] = graph.new_vertex_property("double")  # in kb
graph.vertex_properties["content"] = graph.new_vertex_property("string")  # TODO :should I track this????

# print "Host:", request.headers.get('Host')
# print "User-Agent:", request.headers.get('User-Agent')

graph.save("graph.xml.gz")
g2 = gt.load_graph("graph.xml.gz")
# g and g2 should be copies of each other
