from matching import SemanticMatcher
import heapq as hq 
import pandas as pd

class makeGraph:
    def __init__(self):
        #nodes: companies and organizations
        #edges: weights/edge cost = factors - resources available, quantity, time frame, distance
        self.nodes = set()
        self.edges = {}
    
    def makeNode(self, node):
        self.nodes.add(node)
        if node not in self.edges:
            self.edges[node] = []

    def makeEdge(self, startNode, pointNode, weight):
        if startNode not in self.edges:
            self.makeNode(startNode)
        if pointNode not in self.edges:
            self.makeNode(pointNode)
        self.edges[startNode].append((pointNode, weight))
        self.edges[pointNode].append((startNode, weight))

#insert calculate cost function here (calc compatibilty btwn a company and org)
#input is resource availability, quantity, time, distance
#output is list of edge tuples

class highestCompatibility: #creates compatibilites for ALL companies and orgs
    #need to inherit variables from companies, organizations classes
    def __init__(self):
        self.graph = makeGraph()

    def addNodes(self, companies, organizations):
        for company in companies:
            self.graph.makeNode(company)
        for organization in organizations:
            self.graph.makeNode(organization)

    def addWeights(self, edges): #edges is 3 element tuple w/company, organization, weight btwn 2
        for startNode, pointNode, weight in edges:
            self.graph.makeEdge(startNode, pointNode, weight)

def dijkstra(graph, source):
    distances = {node: float('inf') for node in graph.edges} #initialize distances btwn nodes - default to infinity
    distances[source] = 0
    pq = [(0, source)]
    #hq.push(pq(dist, source))

    while pq:
        currWeight, currNode = hq.heappop(pq) #get smallest distance
        if currWeight>distances[currNode]: #check not unreachable and skip if not optimal
            continue
        for neighbor, weight in graph.edges[currNode]: # loop through neighbors of current node
            newWeight = currWeight + weight # if new better update queue
            if newWeight < distances[neighbor]:
                distances[neighbor] = newWeight
                hq.heappush(pq, (newWeight, neighbor)) # push neighbor update cost
    worstWeight = max([d for d in distances.values() if d < float('inf')], default=1) # largest diff in distance, exclude infinity - unreachable 
    compatibilities = {node: 100-(dist/worstWeight)*100 if dist != float('inf') else 0 for node, dist in distances.items()} # tentative score calculator (inverse proportion)
    return compatibilities 