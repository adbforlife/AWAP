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

        print(initial_board)
        print(team_size)
        print(company_info)

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
                if Tile.is_end_of_line(visible_board[s.x][s.y]):
                    res.append(Direction.ENTER)
                else:
                    res.append(possible_dirs[randint(0,3)])
        return res

        










