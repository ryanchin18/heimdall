import operator
from modeller.factors import BaseFactor


class FactorUserAgentCyclingRatio(BaseFactor):
    """
    Modern DDOS Botnets are tend to change user agent repeatedly during an attack.
    This strategy can be quite effective against even the most generalised regex rules. If
    the IP never repeats its user agent then rules put in place to block requesters using
    obscure user agents will still be subverted. In the context of a real human user, or even
    a spider bot, user agent rotation is highly aberrant. Therefore this factor can be used
    to identify user agent rotating behaviour of different attack types. This factor represent
    the computed average change rate of User-Agents per Session. This will be calculated
    by taking the ratio between sum of minority usage of unique User-Agents and Total
    number of requests. If the value of User-Agent Cycling Ratio is greater than 0, that
    implies there's been a User-Agents cycling within that session.
    """
    def __init__(self, session, session_graph, traffic_record):
        BaseFactor.__init__(self, session, session_graph, traffic_record)
        self._FACTOR_INDEX = 10
        self._FACTOR_KEY = "FactorUserAgentCyclingRatio"
        pass

    def compute(self):
        """
        Compute User-Agent Cycling Ratio.
        
        Variables Required:
            * Total Requests Count (TR),
            * Unique User-Agents per session and their usages as a Dictionary
              sorted by Usage in descending order (SUU)

        Calculation:
        Assume sorted User-Agents usage dictionary as this
        {
             "User-Agent-A" : 7,
             "User-Agent-B" : 2,
             "User-Agent-C" : 1,
             "User-Agent-D" : 1,
        }
        
        According to that;
             Total requests = Sigma (User-Agent Usage)
             Total requests = 11
             Minority User-Agent Usage = Total requests - Majority User-Agent Usage
             Minority User-Agent Usage = 11 -  7
             User-Agent Cycling Ratio = Minority User-Agent Usage / Total requests
             User-Agent Cycling Ratio = (11 -  7) / 11 = 0.364
             
        If the value of User-Agent Cycling Ratio is greater than 0, that implies
        there's been a User-Agents cycling within that session
        """
        tr = self._session_graph.graph.num_edges()
        tr = tr if tr > 0 else 1
        suu = sorted(
            self._session_graph.get_graph_property('user_agents').iteritems(),
            key=operator.itemgetter(1),
            reverse=True
        )
        ua_cycle_ratio = float(tr - suu[0][1]) / float(tr)
        self.append_graph_factor('float', ua_cycle_ratio)
        print "User-Agent Cycling Ratio : ", ua_cycle_ratio
        pass
    pass