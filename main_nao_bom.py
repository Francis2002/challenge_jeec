import numpy as np
import re

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
        print("entrou")
        print(open_set)
        n = None
        #node with lowest f() is found
        """
        for v in open_set:
            if n == None or g[v] + heuristic(v, stop_node) < g[n] + heuristic(n, stop_node):
                n = v
        """

        for v in open_set:
            if n == None:
                n = v
            else:
                if (g[v] + heuristic(v, stop_node) < g[n] + heuristic(n, stop_node)):
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
    a_coor = re.findall(r'\d+', a)
    a_x = a_coor[0]
    a_y = a_coor[1]
    b_coor = re.findall(r'\d+', b)
    b_x = b_coor[0]
    b_y = b_coor[1]
    return floor(math.sqrt(abs(a_x - b_x)*abs(a_x - b_x) + abs(a_y - b_y)*abs(a_y - b_y)))

#Describe your graph here
Graph_nodes = {}

for i in range(11):
    for j in range(11):
        Graph_nodes[str(i) + "-" + str(j)] = []

moves_played = 0

target_arr = []

got_to_middle = False

target_dist = {}
target_path = {}
closest_apple = 0
closest_dist = 1000

graph_created = False

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

    my_pos_id = str(my_position[0]) + "-" + str(my_position[1])

    print(my_pos_id)

    if(graph_created == False):
        k = 0
        b = 0

        for i in range(11):
            for j in range(11):
                if(map[i][j] == "1" or map[i][j] == "2" or map[i][j] == "-"):
                    target_arr.append(str(i) + "-" + str(j))
                    k = k + 1
                if(map[i][j] == "0"):
                    buracos_arr.append(str(i) + "-" + str(j))
                    b = b + 1
                else:
                    if(i == worm_position[0] and j == worm_position[1]): 
                        continue
                    if(i > 0): 
                        Graph_nodes[str(i) + "-" + str(j)].append((str(i - 1) + "-" + str(j), 1))
                    if(i < 11): 
                        Graph_nodes[str(i) + "-" + str(j)].append((str(i + 1) + "-" + str(j), 1))
                    if(j > 0): 
                        Graph_nodes[str(i) + "-" + str(j)].append((str(i) + "-" + str(j - 1), 1))
                    if(j < 11): 
                        Graph_nodes[str(i) + "-" + str(j)].append((str(i) + "-" + str(j + 1), 1))

        for i in target_arr:
            target_dist[i], target_path[i] = aStarAlgo(my_pos_id, i)
            if(closest_dist > target_dist[i]):
                closest_dist = target_dist[i]
                closest_apple = i

    if(got_to_middle == False):
        target = middle_square = str((width-1)/2) + "-" + str((width-1)/2)
    else:
        target = closest_apple(map, my_position)

    aStarAlgo(my_pos_id, middle_square)

    moves_played = moves_played + 1

    print(target_path[closest_apple][0])

#aStarAlgo('A', 'J')



def test_move(move):
        if move == 'n':
            new_position = [my_position[0], my_position[1]-1]
        elif move == 's':
            new_position = [my_position[0], my_position[1]+1]
        elif move == 'e':
            new_position = [my_position[0]+1, my_position[1]]
        elif move == 'w':
            new_position = [my_position[0]-1, my_position[1]]
        else:
            new_position = my_position
        
        # check borders
        if new_position[0]<0 or new_position[1]<0 or new_position[0]>width or new_position[1]>height:
            return False
        
        map_symbol = map[new_position[1]][new_position[0]]
        # check holes
        if map_symbol == 'O':
            return False
        # check worm position
        if new_position==worm_position:
            return False
        
        return True