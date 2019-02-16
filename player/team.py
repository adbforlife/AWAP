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
from sets import *

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

        self.comp_visited = Set([]) #set of companies visited


        print(team_size)
        print (company_info)
        print (initial_board)
        print (len(initial_board))
        print (len(initial_board[0]))


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
                if Tile.is_end_of_line(visible_board[s.x][s.y]) && Tile.get_booth(visible_board[s.x][s.y]) not in self.comp_visited:
                    res.append(Direction.ENTER)
                    self.comp_visited.add(Tile.get_booth(visible_board[s.x][s.y]))
                else:
                    res.append(possible_dirs[randint(0,3)])
        return res


