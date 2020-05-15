from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex):
        self.vertices[vertex] = set()

    def opposite_direction(self, direction):
        exits = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
        return exits[direction]

    def bfs(self, start):
        queue = Queue()
        queue.enqueue([start])
        visited = set() 
        
        while queue.size() > 0:
            path = queue.dequeue()
            vertex = path[-1]
            if vertex not in visited:
                visited.add(vertex)

                for neighbor in self.vertices[vertex]:
                    if self.vertices[vertex][neighbor] == '?':
                        return path

                for direction in self.vertices[vertex]:
                    neighbor_room = self.vertices[vertex][direction]
                    new_path = path.copy()
                    new_path.append(neighbor_room)
                    queue.enqueue(new_path)
        return None


traversal_path = []
visited = set()
graph = Graph()

while len(graph.vertices) < len(room_graph):
    current_room = player.current_room.id
    if current_room not in graph.vertices:
        graph.add_vertex(current_room)
        graph.vertices[current_room] = {i: '?' for i in player.current_room.get_exits()}
    room_exit = None
    for direction in graph.vertices[current_room]:
        if graph.vertices[current_room][direction] == '?':
            room_exit = direction
            if room_exit is not None:
                traversal_path.append(room_exit)
                player.travel(room_exit)
                if player.current_room.id not in graph.vertices:
                    graph.add_vertex(player.current_room.id)
                    graph.vertices[player.current_room.id] = { i: '?' for i in player.current_room.get_exits()}
            graph.vertices[current_room][room_exit] = player.current_room.id
            graph.vertices[player.current_room.id][graph.opposite_direction(room_exit)] = current_room
            current_room = player.current_room.id   
            break
    rooms = graph.bfs(player.current_room.id)
    if rooms is not None:
        for room in rooms:
            for direction in graph.vertices[current_room]:
                if graph.vertices[current_room][direction] == room:
                    traversal_path.append(direction)
                    player.travel(direction)

            current_room = player.current_room.id


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
