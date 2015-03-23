import graph_tool.all as gt


class BFSearchVisitor(gt.BFSVisitor):
    def __init__(self):
        self.sequence = []
        pass

    def discover_vertex(self, u):
        self.sequence.append(int(u))
        pass
    pass


class DFSearchVisitor(gt.DFSVisitor):
    def __init__(self):
        self.sequence = []
        pass

    def discover_vertex(self, u):
        self.sequence.append(int(u))
        pass
    pass