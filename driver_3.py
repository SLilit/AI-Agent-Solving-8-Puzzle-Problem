import sys
import math
import time
import resource
import queue as Q

# the class that reprezents the Puzzle

class PuzzleState(object):
    
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        
        if n*n != len(config) or n < 2:
            raise Exception("the length of config is not correct!")

        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.dimension = n
        self.config = config
        self.children = []
        for i, item in enumerate(self.config):
            if item == 0:
                self.blank_row = i / self.n
                self.blank_col = i % self.n
                break

    def display(self):
        
        for i in range(self.n):
            line = []
            offset = i*self.n
            for j in range(self.n):
                line.append(self.config[offset + j])
            print line


    def move_up(self):

        if self.blank_row == 0:
            return None

        else:
            blank_index = self.blank_row*self.n + self.blank_col
            target = blank_index - self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost+1)

    def move_Down(self):

        if self.blank_row == self.n - 1:
            return None

        else:
            blank_index = self.blank_row*self.n + self.blank_col
            target = blank_index + self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost+1)

    def move_left(self):
        
        if self.blank_col == 0:
            return None

        else:
            blank_index = self.blank_row*self.n + self.blank_col
            target = blank_index - 1
            new_config = list(self.config)
            new_config[blank_index],new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost+1)

    def move_right(self):

        if self.blank_col == self.n -1:
            return None

        else:
            blank_index = self.blank_row*self.n + self.blank_col
            target = blank_index + 1
            new_config = lest(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost+1)

    def expend(self):

        if len(self.children) == 0:
            
            up_child = self.move_up()
            if up_child is not None:
                self.children.append(up_child)

            down_child = self.move_down()
            if down_child is not None:
                self.children.append(down_child)

            left_child = self.move_left()
            if left_child is not None:
                self.children.append(left_child)

            right_child = self.move_right()
            if right_child is not None:
                self.children.append(right_child)
        
        return self.children        

# Function that writes to output.txt

                
def writeOutput():
    pass

def bfs_search(initial_state):
    pass

def dfs_search(initial_state):
    pass

def A_star_search(initial_state):
    pass

def calculate_total_cost(state):
    pass

def test_goal(puzzle_state):
    pass

#Main Function that reads in Input and Runs corresponding algorithm

def main():

    sm = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = tuple(map(int, begin_state))
    size = int(math.sqrt(len(begin_state)))

    if sm == "bfs":
        bfs_search(hard_state)

    elif sm = "dfs":
        dfs_search(hard_state)

    elif sm = "ast":
        A_star_search(hard_state)

    else:
        print('Enter valid command argument!')


if __name__ == '__main__':

    main()


    
    





            




            
