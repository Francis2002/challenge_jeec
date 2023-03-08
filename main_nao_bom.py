#import numpy as np
import re
import math

def vertex(x, y):
    return chr(x*11 + y)

def inverse_vertex(num):
    n = ord(num)
    y = n%11
    x = math.floor(n/11)
    return x, y

def aStarAlgo(start_node, stop_node):
    open_set = set(start_node)
    closed_set = set()
    g = {}               #store distance from starting node
    parents = {}         # parents contains an adjacency map of all nodes
    #distance of starting node from itself is zero
    g[start_node] = 0
    #start_node is root node i.e it has no parent nodes
    #so start_node is set to its own parent node
    parents[start_node] = start_node
    while len(open_set) > 0:
        n = None
        #node with lowest f() is found
        for v in open_set:
            if n == None or g[v] + heuristic(v, stop_node) < g[n] + heuristic(n, stop_node):
                n = v

        if n == stop_node or Graph_nodes[n] == None:
            pass
        else:
            for (m, weight) in get_neighbors(n):
                #nodes 'm' not in first and last set are added to first
                #n is set its parent
                if m not in open_set and m not in closed_set:
                    open_set.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight
                #for each node m,compare its distance from start i.e g(m) to the
                #from start through n node
                else:
                    if g[m] > g[n] + weight:
                        #update g(m)
                        g[m] = g[n] + weight
                        #change parent of m to n
                        parents[m] = n
                        #if m in closed set,remove and add to open
                        if m in closed_set:
                            closed_set.remove(m)
                            open_set.add(m)
        if n == None:
            print('Path does not exist!')
            return None
        
        # if the current node is the stop_node
        # then we begin reconstructin the path from it to the start_node
        if n == stop_node:
            path = []
            while parents[n] != n:
                path.append(n)
                n = parents[n]
            path.append(start_node)
            path.reverse()
            print('Path found: {}'.format(path))
            return path
        # remove n from the open_list, and add it to closed_list
        # because all of his neighbors were inspected
        open_set.remove(n)
        closed_set.add(n)
    print('Path does not exist!')
    return None

#define fuction to return neighbor and its distance
#from the passed node
def get_neighbors(v):
    if v in Graph_nodes:
        return Graph_nodes[v]
    else:
        return None
    
#for simplicity we ll consider heuristic distances given
#and this function returns heuristic distance for all nodes
def heuristic(a, b):
    a_x, a_y = inverse_vertex(a)
    b_x, b_y = inverse_vertex(b)
    return math.floor(math.sqrt(abs(a_x - b_x)*abs(a_x - b_x) + abs(a_y - b_y)*abs(a_y - b_y)))

def near_worm(i, j, worm_x, worm_y):
        if(not (worm_x == i and worm_y == j) and not (worm_x - 1 == i and worm_y == j) and not (worm_x == i and worm_y == j - 1) and not (worm_x + 1 == i and worm_y == j) and not (worm_x == i and worm_y + 1 == j)):
            return False
        else:
            return True

#Describe your graph here
Graph_nodes = {}

for i in range(11):
    for j in range(11):
        Graph_nodes[vertex(i,j)] = []

moves_played = 0

target_arr = []

got_to_middle = False
middle_square = vertex(int((11-1)/2),int((11-1)/2))

target_dist = {}
target_path = {}
target_completed = {}
closest_apple = 0
closest_dist = 1000

graph_created = False

move = "stay"

next_x = 0
next_y = 0

while(True):
    width, height = int(input()), int(input())
    map = [ [0]*width for i in range(height)]
    x = str()
    for h in range(int(height)):
        l = input()
        for w in range(width):
            map[h][w] = l[w]

    worm_position = [int(i) for i in input().split(' ')]
    priority, number_players = int(input()), int(input())
    my_position = [int (i) for i in input().split(' ')]
    other_players_positions = list()
    for j in range(int(number_players) - 1):
        s = input().split(' ')
        other_players_positions.append((s[0], [int (i) for i in s[1:]]))

    my_pos_id = vertex(my_position[0], my_position[1])

    if(graph_created == False):
        for i in range(11):
            for j in range(11):
                if(map[i][j] == "1" or map[i][j] == "2" or map[i][j] == "3"):
                    target_arr.append(vertex(i,j))
                    target_completed[vertex(i,j)] = False
        graph_created = True

    for i in range(11):
        for j in range(11):
            if(map[i][j] != "0" and (not near_worm(i, j, worm_position[0], worm_position[1]) or map[i-1][j] == "1" or map[i-1][j] == "2" or map[i-1][j] == "3" or (map[i-1][j] == "#" and not got_to_middle))):
                if(i > 0): 
                    if(map[i-1][j] != "0" and (not near_worm(i-1, j, worm_position[0], worm_position[1]) or map[i-1][j] == "1" or map[i-1][j] == "2" or map[i-1][j] == "3" or (map[i-1][j] == "#" and not got_to_middle))):
                        Graph_nodes[vertex(i,j)].append((vertex(i - 1,j), 1))
                if(i < 10): 
                    if(map[i+1][j] != "0" and (not near_worm(i+1, j, worm_position[0], worm_position[1]) or map[i-1][j] == "1" or map[i-1][j] == "2" or map[i-1][j] == "3" or (map[i-1][j] == "#" and not got_to_middle))):
                        Graph_nodes[vertex(i,j)].append((vertex(i + 1,j), 1))
                if(j > 0): 
                    if(map[i][j-1] != "0" and (not near_worm(i, j-1, worm_position[0], worm_position[1]) or map[i-1][j] == "1" or map[i-1][j] == "2" or map[i-1][j] == "3" or (map[i-1][j] == "#" and not got_to_middle))):
                        Graph_nodes[vertex(i,j)].append((vertex(i,j - 1), 1))
                if(j < 10): 
                    if(map[i][j+1] != "0" and (not near_worm(i, j+1, worm_position[0], worm_position[1]) or map[i-1][j] == "1" or map[i-1][j] == "2" or map[i-1][j] == "3" or (map[i-1][j] == "#" and not got_to_middle))):
                        Graph_nodes[vertex(i,j)].append((vertex(i,j + 1), 1))

    if(got_to_middle):
        if(map[my_position[0]][my_position[1]] == "1" or map[my_position[0]][my_position[1]] == "2"  or map[my_position[0]][my_position[1]] == "3"):
            target_completed[vertex(my_position[0], my_position[1])] = True
    
    if(got_to_middle == False):
        if(my_position[0] == 5 and my_position[1] == 5):
            got_to_middle = True

    for i in target_arr:
        if(target_completed[i] == False):
            target_path[i] = aStarAlgo(my_pos_id, i)
            target_dist[i] = len(target_path[i])
            if(closest_dist > target_dist[i]):
                closest_dist = target_dist[i]
                closest_apple = i

    if(got_to_middle == False):
        target = middle_square 
        
    else:
        target = closest_apple

    aStarAlgo(my_pos_id, target)

    next_x, next_y = inverse_vertex(target_path[closest_apple][1])

    print(str(ord(target_path[closest_apple][1])))

    if(next_x == my_position[0]):
        if(next_y == (my_position[1] + 1)):
            move = "e"
        else:
            if(next_y == (my_position[1] - 1)):
                move = "w"
    else:
        if(next_y == my_position[1]):
            if(next_x == (my_position[0] + 1)):
                move = "s"
            else:
                if(next_x == (my_position[0] - 1)):
                    move = "n"
                else:
                    move = "stay"

    moves_played = moves_played + 1

    print(move)