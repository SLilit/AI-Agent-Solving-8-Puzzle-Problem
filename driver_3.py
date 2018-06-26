import sys
import math
import time
import os
import psutil
import queue as Q

goal = (0,1,2,3,4,5,6,7,8)

# the class that reprezents the Puzzle
class PuzzleState(object):
    
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        
        if n != 3:
            raise Exception("the length of config is not correct!")

        self.n = n
        self.cost = cost
        if parent == None:
            self.parent = self
        else:
            self.parent = parent
        self.action = action
        self.dimension = n
        self.config = config
        self.children = []
        for i, item in enumerate(self.config):
            if item == 0:
                self.blank_row = int(i / self.n)
                self.blank_col = i % self.n
                break

    def display(self):
        
        for i in range(self.n):
            line = []
            offset = i*self.n
            for j in range(self.n):
                line.append(self.config[offset + j])
            print (line)


    def move_up(self):

        if self.blank_row == 0:
            return None

        else:
            blank_index = self.blank_row*self.n + self.blank_col
            target = blank_index - self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost+1)

    def move_down(self):

        if self.blank_row == self.n - 1:
            return None

        else:
            blank_index = self.blank_row*self.n + self.blank_col
            target = blank_index + self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost+1)

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
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost+1)

    def expand(self):

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
def writeOutput(path_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, running_time, max_ram_usage):
    with open("output.txt", "w") as output:
        output.write("path_to_goal: {}\n".format(path_to_goal))
        output.write("cost_of_path: {}\n".format(cost_of_path))
        output.write("nodes_expanded: {}\n".format(nodes_expanded))
        output.write("search_depth: {}\n".format(search_depth))
        output.write("max_search_depth: {}\n".format(max_search_depth))
        output.write("running_time: {}\n".format(running_time))
        output.write("max_ram_usage: {}\n".format(max_ram_usage))

        
        print ("path_to_goal: {}\n".format(path_to_goal))
        print ("cost_of_path: {}\n".format(cost_of_path))
        print ("nodes_expanded: {}\n".format(nodes_expanded))
        print ("search_depth: {}\n".format(search_depth))
        print ("max_search_depth: {}\n".format(max_search_depth))
        print ("running_time: {}\n".format(running_time))
        print ("max_ram_usage: {}\n".format(max_ram_usage))
 
def bfs_search(state):
    
    start = calculate_total_cost()
    frontier = Q.Queue()
    max_depth = 0
    nodes = 0
    front = [str(state.config)]
       
    while not test_goal(state.config):
        states = state.expand()
        nodes += 1
        if states[0].cost > max_depth:
            max_depth = states[0].cost
        
        for i in range(len(states)):
            if str(states[i].config) not in front:
                frontier.put(states[i])
                front.append(str(states[i].config))
        state = frontier.get()
        
    cost = state.cost
    depth = state.cost
    path = [state.action]
    state = state.parent
    
    while state.action != 'Initial':
        path.append(state.action)
        state = state.parent
        
    end = calculate_total_cost()
    writeOutput(path[::-1], cost, nodes, depth, max_depth, end[0]- start[0], end[1] - start[1])            
 

def dfs_search(state):

    start = calculate_total_cost()
    frontier = []
    max_depth = 0
    nodes = 0
    front = [str(state.config)]
       
    while not test_goal(state.config):
        
        states = state.expand()[::-1]
        nodes += 1
        
        for i in range(len(states)):
            if str(states[i].config) not in front:
                frontier.append(states[i])
                front.append(str(states[i].config))
                
        state = frontier.pop()
        
        if state.cost > max_depth:
            max_depth = state.cost
        
    cost = state.cost
    depth = state.cost
    path = [state.action]
    state = state.parent
    
    while state.action != 'Initial':
        path.append(state.action)
        state = state.parent

    end = calculate_total_cost()   
    writeOutput(path[::-1], cost, nodes, depth, max_depth, end[0]- start[0], end[1] - start[1])            
 

def A_star_search(state):

    start = calculate_total_cost()
    frontier = {}
    front = []
    mf = []
    nodes = 0
    
       
    while not test_goal(state.config):
        nodes += 1
        states = state.expand()[::-1]
        
        for i in range(len(states)):
            if str(states[i].config) not in front:
                f = 0
                front.append(str(states[i].config))

                for j in range(8):
                    f = f + abs(int(states[i].config[j]/3) - int(j/3)) + abs(states[i].config[j]%3 - j%3)
                    #if state_config[j] != goal[j]:
                     #   f += 1

                f = f + states[i].cost
                if f not in frontier:
                    frontier[f] = Q.Queue()
                    frontier[f].put(states[i])
                    #frontier[f] = [states[i]]
                else:
                    frontier[f].append(states[i])
                
                    
                               
        min_f = min(frontier)
        state = frontier[min_f].get()
        if frontier[min_f].empty():
            frontier.pop(min_f)

        
        #if len(frontier[min_f]) == 1:
         #   state = frontier.pop(min_f)[0]
        #else:
         #   state = frontier[min_f].pop()
        
        if state.cost > 8000:
            print("too long")
            break
        
    cost = state.cost
    depth = state.cost
    max_depth = state.cost
    path = [state.action]
    state = state.parent
    
    while state.action != 'Initial':
        path.append(state.action)
        state = state.parent
        
    end = calculate_total_cost()
    writeOutput(path[::-1], cost, nodes, depth, max_depth, end[0]- start[0], end[1] - start[1])            
 


                        

def calculate_total_cost():
    import time
    time = time.time()
    process = psutil.Process(os.getpid())
    return [time,process.memory_info().rss]

def test_goal(puzzle_state):

    if puzzle_state == goal:
        return True
    else:
        return False

#Main Function that reads in Input and Runs corresponding algorithm
def main():
    
    sm = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = tuple(map(int, begin_state))
    size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, size)

    if sm == "bfs":
        bfs_search(hard_state)

    elif sm == "dfs":
        dfs_search(hard_state)

    elif sm == "ast":
        A_star_search(hard_state)

    else:
        print('Enter valid command argument!')


if __name__ == '__main__':

    main()


    
    





            




            
