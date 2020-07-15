# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph
from functools import reduce

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    path = [start] ; queue = [path]
    goal_reached = start == goal
    while len(queue) > 0 and not goal_reached:
        first_path = queue.pop(0)
        last_node = first_path[-1]
        extended_paths = [first_path + [x] for x in graph.get_connected_nodes(last_node) if x not in first_path]
        queue = queue + extended_paths
        goal_reached = len(queue) > 0 and queue[0][-1] == goal
    return queue[0] if len(queue) > 0 else []
        
# Once you have completed the breadth-first search,
# this part should be very simple to complete.
def dfs(graph, start, goal):
    path = [start] ; queue = [path]
    goal_reached = start == goal
    while len(queue) > 0 and not goal_reached:
        first_path = queue.pop(0)
        last_node = first_path[-1]
        extended_paths = [first_path + [x] for x in graph.get_connected_nodes(last_node) if x not in first_path]
        queue = extended_paths + queue
        goal_reached = len(queue) > 0 and queue[0][-1] == goal
    return queue[0] if len(queue) > 0 else []
        
## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    path = [start] ; queue = [path] ; goal_reached = start == goal
    while len(queue) > 0 and not goal_reached:
        first_path = queue.pop(0)
        last_node = first_path[-1]
        extended_paths = [first_path + [x] for x in graph.get_connected_nodes(last_node) if x not in first_path]
        extended_paths.sort(key = lambda x: graph.get_heuristic(x[-1] , goal) , reverse = False )
        queue = extended_paths + queue
        goal_reached = len(queue) > 0 and queue[0][-1] == goal
    return queue[0] if len(queue) > 0 else []

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    path = [start] ; queue = [path] ; goal_reached = start == goal
    while len(queue) > 0  and not goal_reached:
        first_path = queue.pop(0)
        last_node = first_path[-1]
        extended_paths = [first_path + [x] for x in graph.get_connected_nodes(last_node) if x not in first_path]
        if len(extended_paths) > 0:
            temp_ext = list(filter(lambda x: len(x) == len(extended_paths[0]), queue))
            queue = list(filter(lambda x: x not in temp_ext, queue))
            extended_paths = temp_ext + extended_paths
            extended_paths.sort(key = lambda x: graph.get_heuristic(x[-1] , goal) , reverse = False )
            extended_paths = extended_paths[0:beam_width]
            queue = queue + extended_paths
        goal_reached = len(queue) > 0 and queue[0][-1] == goal
    return queue[0] if len(queue) > 0 else []

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    length = 0
    for index in range(1,len(node_names)) :
        length += graph.get_edge(node_names[index-1], node_names[index]).length
    return length

def branch_and_bound(graph, start, goal):
    path = [start] ; queue = [path] ; goal_reached = start == goal
    while len(queue) > 0 and not goal_reached:
        first_path = queue.pop(0)
        last_node = first_path[-1]
        extended_paths = [first_path + [x] for x in graph.get_connected_nodes(last_node) if x not in first_path]
        queue = extended_paths + queue
        queue.sort(key = lambda x: path_length(graph, x) , reverse = False )
        goal_reached = len(queue) > 0 and queue[0][-1] == goal
    return queue[0] if len(queue) > 0 else []

def a_star(graph, start, goal):
    path = [start] ; queue = [path] ; goal_reached = start == goal
    extended = set()
    while len(queue) > 0 and not goal_reached:
        first_path = queue.pop(0)
        last_node = first_path[-1]
        extended_paths = [first_path + [x] for x in graph.get_connected_nodes(last_node) if x not in first_path and x not in extended]
        queue = extended_paths + queue
        extended.add(first_path[-1])
        queue.sort(key = lambda x: path_length(graph, x) + graph.get_heuristic(x[-1], goal), reverse = False )
        goal_reached = len(queue) > 0 and queue[0][-1] == goal
    return queue[0] if len(queue) > 0 else []

def is_admissible(graph, goal):
    for node in graph.nodes:
        length = path_length(graph, branch_and_bound(graph, node, goal))
        if graph.get_heuristic(node, goal) > length:
            return False
    return True

def is_consistent(graph, goal):
    for edge in graph.edges:
        heuristic = abs(graph.get_heuristic(edge.node1, goal) - graph.get_heuristic(edge.node2, goal))
        if heuristic > edge.length:
            return False
    return True

HOW_MANY_HOURS_THIS_PSET_TOOK = '1 Day'
WHAT_I_FOUND_INTERESTING = 'All the algorithms'
WHAT_I_FOUND_BORING = 'Nothing about this lab but I discovered that integer division changed with python 3 and \
that is the version I am using, on the other hand this course is 10 years old! So I had to change exp_graph(depth) func in \
tests.py. But it took couple hours to realize it.'
