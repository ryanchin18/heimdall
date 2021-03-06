__author__ = 'grainier'

import graph_tool.all as gt

import os
import redis
from common import REDIS_POOL, current_time_milliseconds, redis_key_template, root_dir
from common.exceptions import VertexDoesNotExists, PropertyDoesNotExists, EdgeDoesNotExists
from common.graphs import GraphReference, SingletonGraph


class SessionGraph(GraphReference):
    __metaclass__ = SingletonGraph

    def __init__(self, session):
        super(SessionGraph, self).__init__()
        self.session = session
        self.redis = redis.Redis(connection_pool=REDIS_POOL)
        self.path = os.path.join(root_dir, "generated", "graphs")
        try:
            self.graph = gt.load_graph(os.path.join(self.path, "{0}_c_g.gt".format(self.session)))
            self.session_start = self.graph.graph_properties["session_start"]
            pass
        except Exception:
            self.graph = gt.Graph()
            self.session_start = current_time_milliseconds()

            # add mandatory graph properties
            self.graph.graph_properties["session"] = self.graph.new_graph_property("string", self.session)
            self.graph.graph_properties["last_request"] = self.graph.new_graph_property("string", '')
            self.graph.graph_properties["session_start"] = self.graph.new_graph_property("long", self.session_start)
            self.graph.graph_properties["consecutive_requests"] = self.graph.new_graph_property("int", 0)
            self.graph.graph_properties["last_request_time"] = self.graph.new_graph_property("long", self.session_start)
            self.graph.graph_properties["user_agents"] = self.graph.new_graph_property("object", {})
            self.graph.graph_properties["response_codes"] = self.graph.new_graph_property("object", {})
            self.graph.graph_properties["resource_types"] = self.graph.new_graph_property("object", {})
            self.graph.graph_properties["request_intervals"] = self.graph.new_graph_property("object", {})
            self.graph.graph_properties["request_sequence"] = self.graph.new_graph_property("vector<int>", [])

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
        self.graph.save(os.path.join(self.path, "{0}_c_g.gt".format(self.session)))
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
        self.graph.vertex_properties["url"][v] = self.redis.get(redis_key_template.format("any", "url", vertex_id))
        # TODO : add other properties here, if there's any

        # add index to redis
        self.redis.set(redis_key_template.format(self.session, "vertex", vertex_id), v_index)
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
        except (KeyError, ValueError) as e:
            prop = self.graph.new_graph_property(property_type)
            self.graph.graph_properties[property_key] = prop
            self.graph.graph_properties[property_key] = property_value
            pass
        # self.save()   # do not save here, it will add i/o overhead
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
            # self.save()   # do not save here, it will add i/o overhead
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
            except (KeyError, ValueError), e:
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
        except (KeyError, ValueError), e:
            e = None
            pass

        # add edge property
        if e:
            self.graph.edge_properties[property_key] = self.graph.new_edge_property(property_type)
            self.graph.edge_properties[property_key][e] = property_value
            # self.save()   # do not save here, it will add i/o overhead
            pass
        else:
            raise EdgeDoesNotExists()
        pass

    def get_edge_property(
            self, property_key, edge=None, source_vertex=None, destination_vertex=None,
            source_vertex_id=None, destination_vertex_id=None):
        # TODO : Implement this
        pass

    def remove_parallel_edges(self):
        gt.remove_parallel_edges(self.graph)
        pass

    def get_vertex(self, vertex_id):
        try:
            v_index = self.redis.get(redis_key_template.format(self.session, "vertex", vertex_id))
            v = self.graph.vertex(v_index)
            v = v if v.is_valid() else None
        except (TypeError, ValueError) as e:
            v = None
            pass
        return v
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

    def update_resource_type_usage(self, resource_type):
        rtu = self.graph.graph_properties["resource_types"]
        if resource_type in rtu:
            rtu[resource_type] += 1
        else:
            rtu[resource_type] = 1
        self.graph.graph_properties["resource_types"] = rtu
        pass

    def update_request_intervals(self):
        last_request = self.graph.graph_properties["last_request_time"]
        this_request = current_time_milliseconds()
        intervals = self.graph.graph_properties["request_intervals"]
        diff = abs(this_request - last_request)

        if 0 <= diff <= 500:
            if '0-500' in intervals:
                intervals['0-500'] += 1
                pass
            else:
                intervals['0-500'] = 1
                pass
            pass

        elif 500 < diff <= 1500:
            if '501-1500' in intervals:
                intervals['501-1500'] += 1
                pass
            else:
                intervals['501-1500'] = 1
                pass
            pass

        elif 1500 < diff <= 4500:
            if '1501-4500' in intervals:
                intervals['1501-4500'] += 1
                pass
            else:
                intervals['1501-4500'] = 1
                pass
            pass

        elif 4500 < diff <= 13500:
            if '4501-13500' in intervals:
                intervals['4501-13500'] += 1
                pass
            else:
                intervals['4501-13500'] = 1
                pass
            pass

        else:
            if '13501<' in intervals:
                intervals['13501<'] += 1
                pass
            else:
                intervals['13501<'] = 1
                pass
            pass

        self.graph.graph_properties["last_request_time"] = this_request
        self.graph.graph_properties["request_intervals"] = intervals
        pass

    def update_consecutive_requests(self, request_uri):
        last_request = self.graph.graph_properties["last_request"]
        if last_request == request_uri:
            self.graph.graph_properties["consecutive_requests"] += 1
            pass
        self.graph.graph_properties["last_request"] = request_uri
        pass

    def update_sequence(self, destination_vertex_index):
        self.graph.graph_properties["request_sequence"].append(destination_vertex_index)
        pass

    def get_session_length(self):
        """
        Get the session length in milliseconds
        :return: session length in milliseconds
        """
        return current_time_milliseconds() - self.session_start
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
            # vertex_text=self.graph.vertex_index,
            vertex_text=self.graph.vertex_properties["url"],
            vertex_font_size=8,
            edge_pen_width=1,
            output_size=(2048, 2048),
            output=os.path.join(self.path, "{0}_c_g.png".format(self.session))
        )
        pass

    pass
