
class Course:
    '''
    Represents a vertex in the DAG
    Course name: either "Math 180A" (simple vertex) or ["Math 180A" or "Math 183"]
    '''
    def __init__(self, name, prereq):
        self.name = name
        self.prereq = prereq
        self.out = []

        self.utility = 0
        pass

    def __str__(self):
        return "Course " + self.name

def readInput(graph):

    def addVertex(graph, course):
        graph[course.name] = course

    # simulate: data input from WebScraper.py
    Z = Course('Z', [])
    A = Course('A', [])
    B = Course('B', prereq=['A'])
    C = Course('C', prereq=['A'])
    D = Course('D', prereq=['A', 'B', 'C'])
    E = Course('E', prereq=['D','A', 'C'])

    addVertex(graph, Z)
    graph['A'] = A
    graph['C'] = C
    graph['B'] = B
    graph['D'] = D
    addVertex(graph, E)


def setOutEdges(graph):
    '''
    Knowing each vertex's ingoing edges (prereq), set their outgoing edges.
    :param graph:
    '''
    # track visit status for each vertex
    visited = {name : False for name in graph.keys()}

    # run graph search
    for vertex, hasVisited in visited.items():
        if not hasVisited:
            dfsReverse(graph, visited, vertex)

def dfsReverse(graph, visited, s):
    '''
    Traverse the graph using depth-first-search to set the outgoing edges
    :param graph:
    :param visited:
    :param s: starting vertex
    '''
    visited[s] = True

    stack = [s]
    while stack:
        curr = stack.pop()
        for pre in graph[curr].prereq:     # for all the [pre]requisite courses of curr
            if not visited[pre]:
                visited[pre] = True
                stack += pre
            # let all curr's prerequisites recognize 'curr' as a member of their 'out' edges
            graph[pre].out += curr



def topologicalSort(graph):
    '''
    Run topological sort based on Kahn's algorithm
    :param graph:
    :return: a sequence of courses
    '''
    avail = [name for name, course in graph.items() if len(course.prereq) == 0]      ## TODO DS: priority queue?
    print("Available vertices: ", avail)

    plan = []
    numCourseThisQuarter = len(avail)
    plan.append([x for x in avail])  # snap shot of avail

    while avail:
        if len(avail) < numCourseThisQuarter:
            a = avail.pop()


        for outNeighbor in graph[a].out:
            graph[outNeighbor].prereq.remove(a)     # remove the edge a --> outNeighbor
            # determine if the outNeighbor is available
            if len( graph[outNeighbor].prereq ) == 0:
                avail += outNeighbor      # not this. we don't know when a quarter stops

        print(plan)



def displayGraph(graph):
    print("------------------Start Graph--------------------")
    for course in graph.values():
        print(course.name)
        print("\t Prereqs: ", end="")
        print(course.prereq)
        print("\t Outs: ", end="")
        print(course.out)
        print()

    print("------------------End Graph--------------------\n")


if __name__ == '__main__':
    graph = {}
    readInput(graph)
    setOutEdges(graph)
    displayGraph(graph)

    print("-----------------------------Begin topological sort------------------------------")
    topologicalSort(graph)

    # displayGraph(graph)

