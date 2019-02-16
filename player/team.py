"""
The team.py file is where you should write all your code!

Write the __init__ and the step functions. Further explanations
about these functions are detailed in the wiki.

List your Andrew ID's up here!
amahanka
sixiangg
hengz2
"""
from awap2019 import Tile, Direction, State
from random import *

class Graph():
    def __init__(self, graph):
        """
        :type graph: list(list(vertices))
        """
        self.num_v = len(graph)
        self.graph = graph

    def printSolution(self, dist): 
        print("Vertex \tDistance from Source")
        for node in range(self.num_v): 
            print(node,"\t",dist[node]) 

    def minDist(self, dist, visited):
        minimum = float('inf')
        minimum_index = -1
        for i in range(self.num_v):
            if (not visited[i]) and dist[i] < minimum:
                minimum = dist[i]
                minimum_index = i
        return minimum_index

    def dijkstra(self, src):
        dist = [float('inf') for _ in range(self.num_v)]
        dist[src] = 0
        visited = [False for _ in range(self.num_v)]

        for _ in range(self.num_v):
            u = self.minDist(dist, visited)
            if u == -1:
                print("-1")
                break
            visited[u] = True

            for v in range(self.num_v):
                if visited[v]:
                    neighbors = self.graph[v]
                    for e in neighbors:
                        if not visited[e[0][0]]:
                            dist[e[0][0]] = dist[v] + e[1]

        self.printSolution(dist)


class Team(object):
    def __init__(self, initial_board, team_size, company_info):
        """
        The initializer is for you to precompute anything from the
        initial board and the company information! Feel free to create any
        new instance variables to help you out.

        Specific information about initial_board and company_info are
        on the wiki. team_size, although passed to you as a parameter, will
        always be 4.
        """

        self.board = initial_board
        self.team_size = team_size
        self.company_info = company_info

        self.team_name = "Null Graphs' Lives Matter"

        self.comp_visited = set([]) #set of companies visited


        print(team_size)
        print(company_info)
        print(initial_board)
        print(len(initial_board))
        print(len(initial_board[0]))


        # Information about company booth locations and line locations
        booth_loc = {}
        line_loc = {}
        endLine_loc = {}

        for x in (company_info):
            booth_loc[x] = []
            line_loc[x] = []
            endLine_loc[x] = []
        
        print (booth_loc)
        print (line_loc)

        for i in range (len(initial_board)):
            for j in range (len(initial_board[0])):
                booth_info = initial_board[i][j].get_booth()
                if(booth_info != None):
                    booth_loc[booth_info].append([i,j])
                line_info = initial_board[i][j].get_line()
                if(line_info != None):
                    line_loc[line_info].append([i, j])
        for x in (company_info):
            if (len(line_loc[x]) == 1):
                endLine_loc[x] = line_loc[x]
            else:
                pos1 = line_loc[x][0]
                pos2 = line_loc[x][-1]
                if ((self.nextBooth(pos1, booth_loc[x])) and 
                not(self.nextBooth(pos2, booth_loc[x]))):
                    endLine_loc[x] = [pos2]
                elif ((self.nextBooth(pos2, booth_loc[x])) and
                not(self.nextBooth(pos1, booth_loc[x]))):
                    endLine_loc[x] = [pos1]
                else:
                    endLine_loc[x] = [pos1, pos2]
        


        print (booth_loc)
        print (line_loc)
        print (endLine_loc)

        vertices = []
        # Create a list of vertices
        # ((x, y), if start line, if line)
        counter = 0
        for i in range (len(initial_board)):
            for j in range (len(initial_board[0])):
                booth_info = initial_board[i][j].get_booth()
                line_info = initial_board[i][j].get_line()
                if (booth_info == None):
                    isLine = (line_info != None)
                    isEnd = False
                    if (line_info != None):
                        isEnd = ((i == (endLine_loc[line_info][0][0]))
                        and (j == (endLine_loc[line_info][0][1])))
                    vertex = (counter, (i, j), isLine, isEnd)
                    vertices.append(vertex)
                    counter += 1
        print (vertices)


        # Create graph
        graph = []
        for i in range (len(vertices)):
            toAdd = []
            a = vertices[i]
            a1 = a[1][0]
            a2 = a[1][1]
            for j in range (len(vertices)):
                b = vertices[j]
                b1 = b[1][0]
                b2 = b[1][1]
                if self.nextTo([a1, a2], [b1, b2]):
                    toAdd.append((b, 1))
            graph.append(toAdd)

        print (graph)
        print (len(graph))

        self.graph = Graph(graph)
        self.graph.dijkstra(1)


    # Tests if two points are adjacent 
    def nextTo(self, loc1, loc2):
        if (loc1[0] == loc2[0]):
            return (abs(loc1[1]-loc2[1]) == 1)
        if (loc1[1] == loc2[1]):
            return (abs(loc1[0]-loc2[0]) == 1)
        return False
        
    # Tests if a point is next to booth
    def nextBooth(self, loc, boothList):
        for i in range (len(boothList)):
            if self.nextTo(loc, boothList[i]):
                return True
        return False

    #Returns a new graph where the vertices are all the cells of
    #the board. Edge weights are based on threshold for the visible
    #5x5 board. 
    def makeGraph(self, visible_board):
        #New graph of vertices and their weights

        #Similar to the graph previously created
        #But weights are different, based on threshold
        G = self.graph
        newGraph = []

        for edgelist in G.graph:
            newEdgeList = []
            for vertexWeight in edgelist:
                v = vertexWeight[0]
                v1 = v[0]
                v2 = v[1]
                currentTile = visible_board[v1][v2]
                newWeight = -1
                if (Tile.is_visible(currentTile)) newWeight = Tile.get_threshold(currentTile)
                else newWeight = 1
                newEdgeList.append((v, newWeight))
            newGraph.append(newEdgeList)

        self.graph = newGraph

    def step(self, visible_board, states, score):
        """
        The step function should return a list of four Directions.

        For more information on what visible_board, states, and score
        are, please look on the wiki.
        """
        possible_dirs = [Direction.LEFT, Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.NONE, Direction.ENTER, Direction.REPLACE]
        res = []
        for s in states:
            if s.line_pos != -1:
                res.append(Direction.NONE)
            else:
                if Tile.is_end_of_line(visible_board[s.x][s.y]) and Tile.get_booth(visible_board[s.x][s.y]) not in self.comp_visited:
                    res.append(Direction.ENTER)
                    self.comp_visited.add(Tile.get_booth(visible_board[s.x][s.y]))
                else:
                    res.append(possible_dirs[randint(0,3)])
        return res


