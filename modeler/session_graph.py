__author__ = 'grainier'

import graph_tool.all as gt
from modeler import SingletonGraph
from util import config, current_time_milliseconds
from exception import VertexDoesNotExists, PropertyDoesNotExists, EdgeDoesNotExists
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
            self.graph = gt.load_graph("{0}_c_g.gt".format(self.session))
            self.session_start = self.graph.graph_properties["session_start"]
            pass
        except Exception:
            self.graph = gt.Graph()
            self.session_start = current_time_milliseconds()

            # add mandatory graph properties
            self.graph.graph_properties["session"] = self.graph.new_graph_property("string", self.session)
            self.graph.graph_properties["session_start"] = self.graph.new_graph_property("long", self.session_start)
            self.graph.graph_properties["traffic_records"] = self.graph.new_graph_property("int", 0)
            self.graph.graph_properties["user_agents"] = self.graph.new_graph_property("object", {})
            self.graph.graph_properties["response_codes"] = self.graph.new_graph_property("object", {})

            # add edge properties
            # self.graph.edge_properties["referer"] = self.graph.new_edge_property("string")  # this is shouldn't be an edge property

            # add vertex properties
            self.graph.vertex_properties["vertex_id"] = self.graph.new_vertex_property("string")  # do not remove this
            self.graph.vertex_properties["original_index"] = self.graph.new_vertex_property("int")  # do not remove this
            self.graph.vertex_properties["url"] = self.graph.new_vertex_property("string")  # do not remove this
            pass
        pass

    def is_same_session(self, session):
        return session == self.session
        pass

    def save(self):
        self.graph.save("{0}_c_g.gt".format(self.session))
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

        # TODO : This is bad, DO it right
        self.graph.vertex_properties["url"][v] = self.redis.get('session::any||type::url||hash::{0}'.format(vertex_id))
        # TODO : add other properties here, if there's any

        # add index to redis
        self.redis.set('session::{0}||type::vertex||hash::{1}'.format(self.session, vertex_id), v_index)
        return v
        pass

    def add_graph_property(self, property_key, property_type, property_value):
        """
        This method will add a graph property to this session graph and save it.
        :param property_key: property key to identify property
        :param property_type: property type (int, double, ...)
        :param property_value: value of the property
        :return: -
        """
        try:
            self.graph.graph_properties[property_key] = property_value
            pass
        except KeyError, e:
            prop = self.graph.new_graph_property(property_type)
            self.graph.graph_properties[property_key] = prop
            self.graph.graph_properties[property_key] = property_value
            pass
        self.save()
        pass

    def get_graph_property(self, property_key):
        try:
            return self.graph.graph_properties[property_key]
            pass
        except KeyError, e:
            return None
            pass
        pass

    def add_vertex_property(self, property_key, property_type, property_value, vertex=None, vertex_id=None):
        # get the vertex
        if vertex:
            v = vertex
        elif vertex_id:
            v = self.get_vertex(vertex_id)
        else:
            v = None

        # check the validity
        v = v if v is not None and v.is_valid() else None

        # add vertex property
        if v:
            self.graph.vertex_properties[property_key] = self.graph.new_vertex_property(property_type)
            self.graph.vertex_properties[property_key][v] = property_value
            self.save()
        else:
            raise VertexDoesNotExists()
        pass

    def get_vertex_property(self, property_key, vertex=None, vertex_id=None):
        # get the vertex
        v = None
        if vertex:
            v = vertex
        elif vertex_id:
            v = self.get_vertex(vertex_id)

        # check the validity
        v = v if v is not None and v.is_valid() else None

        # return vertex property
        if v:
            try:
                return self.graph.vertex_properties[property_key][v]
            except KeyError, e:
                raise PropertyDoesNotExists()
            pass
        else:
            raise VertexDoesNotExists()
        pass

    def add_edge_property(
            self, property_key, property_type, property_value,
            edge=None, source_vertex=None, destination_vertex=None,
            source_vertex_id=None, destination_vertex_id=None):

        # get the edge
        try:
            if edge:
                e = edge
                pass
            elif source_vertex and destination_vertex:
                e = self.graph.edge(int(source_vertex), int(destination_vertex))
                pass
            elif source_vertex_id and destination_vertex_id:
                sv = self.get_vertex(source_vertex_id)
                dv = self.get_vertex(destination_vertex_id)
                if sv and dv:
                    e = self.graph.edge(int(sv), int(dv))
                    pass
                else:
                    e = None
                    pass
                pass
            else:
                e = None
        except ValueError, e:
            e = None
            pass

        # add edge property
        if e:
            self.graph.edge_properties[property_key] = self.graph.new_edge_property(property_type)
            self.graph.edge_properties[property_key][e] = property_value
            self.save()
            pass
        else:
            raise EdgeDoesNotExists()
        pass

    def get_edge_property(
            self, property_key, edge=None, source_vertex=None, destination_vertex=None,
            source_vertex_id=None, destination_vertex_id=None):
        # TODO : Implement this
        pass

    def get_vertex(self, vertex_id):
        try:
            v_index = self.redis.get('session::{0}||type::vertex||hash::{1}'.format(self.session, vertex_id))
            v = self.graph.vertex(v_index)
            v = v if v.is_valid() else None
        except TypeError as e:
            v = None
            pass
        return v
        pass

    def increment_records_count(self):
        self.graph.graph_properties["traffic_records"] += 1
        pass

    def update_response_code_usage(self, response_code):
        rcu = self.graph.graph_properties["response_codes"]
        if response_code in rcu:
            rcu[response_code] += 1
        else:
            rcu[response_code] = 1
        self.graph.graph_properties["response_codes"] = rcu
        pass

    def update_user_agent_usage(self, user_agent):
        uau = self.graph.graph_properties["user_agents"]
        if user_agent in uau:
            uau[user_agent] += 1
        else:
            uau[user_agent] = 1
        self.graph.graph_properties["user_agents"] = uau
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