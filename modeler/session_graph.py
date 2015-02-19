__author__ = 'grainier'

import graph_tool.all as gt
from modeler import SingletonGraph
from util import config
import redis


class SessionGraph(object):
    __metaclass__ = SingletonGraph

    def __init__(self, session, temp=True):
        self.session = session
        self.temp = temp
        self.redis = redis.StrictRedis(
            config.redis.get('host', '127.0.0.1'),
            config.redis.get('port', '6379')
        )
        try:
            self.graph = gt.load_graph("{0}_c_g.xml.gz".format(self.session))
            pass
        except Exception:
            self.graph = gt.Graph()
            # add graph properties
            self.graph.graph_properties["session"] = self.graph.new_graph_property("string", self.session)
            
            # add edge properties
            # self.graph.edge_properties["referer"] = self.graph.new_edge_property("string")  # this is shouldn't be an edge property
            
            # add vertex properties
            self.graph.vertex_properties["vertex_id"] = self.graph.new_vertex_property("string")  # do not remove this
            self.graph.vertex_properties["original_index"] = self.graph.new_vertex_property("int")  # do not remove this
            self.graph.vertex_properties["url"] = self.graph.new_vertex_property("string")  # do not remove this

            # self.graph.vertex_properties["data_length"] = self.graph.new_vertex_property("int")
            # self.graph.vertex_properties["content_length"] = self.graph.new_vertex_property("int")
            # self.graph.vertex_properties["content_size"] = self.graph.new_vertex_property("double")  # in kb
            pass
        pass

    def is_same_session(self, session):
        return session == self.session
        pass

    def save(self):
        self.graph.save("{0}_c_g.xml.gz".format(self.session))
        pass

    def add_edge(self, source_vertex, target_vertex, edge_properties=None):
        # get vertex ids
        sv_id = source_vertex['vertex_id']
        tv_id = target_vertex['vertex_id']

        # get vertex property descriptors
        s = self.get_vertex(sv_id)
        t = self.get_vertex(tv_id)

        # TODO : need a find_vertex method
        # if none there should be a find_vertex method to find
        # whether the indexes have changed (this calls the re-index too)

        # if there's no existing vertex, create new ones
        s = self.add_vertex(sv_id) if s is None else s
        t = self.add_vertex(tv_id) if t is None else t

        e = self.graph.add_edge(s, t)
        # TODO : add edge properties here, if there's any
        return e
        pass

    def add_vertex(self, vertex_id, properties=None):
        # create new vertex
        v = self.graph.add_vertex()
        v_index = int(v)

        # add properties
        self.graph.vertex_properties["vertex_id"][v] = vertex_id
        self.graph.vertex_properties["original_index"][v] = v_index

        #  TODO : This is bad, DO it right
        self.graph.vertex_properties["url"][v] = self.redis.get('session:any.url.{0}'.format(vertex_id))
        # TODO : add other properties here, if there's any

        # add index to redis
        self.redis.set('session:{0}.vertex.{1}'.format(self.session, vertex_id), v_index)
        return v
        pass

    def get_vertex(self, vertex_id):
        try:
            v_index = self.redis.get('session:{0}.vertex.{1}'.format(self.session, vertex_id))
            v = self.graph.vertex(v_index)
            v = v if v.is_valid() else None
        except TypeError as e:
            v = None
            pass
        return v
        pass

    def re_index(self):
        # re-index redis
        # {vertex_id : vertex_index}
        # get vertex using vertex_index, and check whether it's vertex_id
        # equivalent to redis key used to retrieve vertex_index. If it's
        # different, reindex the hole redis index

        for vertex in self.graph.vertices():
            print self.graph.vertex_properties["vertex_id"][vertex]
        pass

    def print_graph(self):
        gt.graph_draw(
            self.graph,
            vertex_text=self.graph.vertex_properties["url"],
            vertex_font_size=8,
            edge_pen_width=1,
            output_size=(2048, 2048),
            output="{0}_c_g.png".format(self.session)
        )
        pass

    pass