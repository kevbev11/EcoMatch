class Graph:
    def __init__(self):
        #nodes: companies and organizations
        #edges: weights/edge cost = factors - resources available, quantity, time frame, distance
        self.nodes = set()
        self.edges = {}
    
    def makeNode(self, node):
        self.nodes.add(node)
        if node not in self.edges:
            self.edges[node] = []

    def addEdge(self, startNode, pointNode, weight):
        if startNode not in self.edges:
            self.edges.makeNode(startNode)
        if pointNode not in self.edges:
            self.edges.makeNode(pointNode)
        self.edges[startNode].append((pointNode, weight))
        self.edges[pointNode].append((startNode, weight))

#add def of cost function (calc compatibilty)

def dijkstra(graph, source):
