import random, turtle
from collections import defaultdict
#defaultdict acts like dict but yields default value when key not found

class Maze:
    def __init__(self, x, y):
        #Window size
        turtle.Screen().setup(x + 10, y + 10)
        #Canvas size
        turtle.Screen().screensize(x, y)
        turtle.title("Maze Generator")
        turtle.bgcolor("black")

    def main(self, sides):
        #self.setSeed(20)
        self.baseMap(sides)
        results = self.DFS(0, sides)
        for path in results:
            self.draw(path, sides, path[0])

    def setSeed(self,seed):
        random.seed(seed)
        
    #Generates a map with all of a cells neighbors (no diagonal) 
    def baseMap(self, sides):
        self.graph = defaultdict(list)
        for i in range(0, sides * sides):
            #Left neighbors
            if i >= 1 and (i % sides) != 0 :
                self.graph[i].append(i - 1)
            #Right neigbhors
            if (i + 1) % sides != 0:
                self.graph[i].append(i + 1)
            #Bot neighbors
            if i < sides * (sides - 1):
                self.graph[i].append(i + sides)
            #Top neighbors
            if i > sides - 1:
                self.graph[i].append(i - sides)

    #Creates paths, then connects them to top right corner, node 0
    def DFS(self, v, sides):
        results = self.DFSVisit(v)
        connected = [False] * len(results)
        connected[0] = True
        for indx, path in enumerate(results):
            for neighborNode in self.graph[path[0]]:
                if self.connectedNode(results, neighborNode, connected):
                    connected[indx] = True
                    path.insert(0, neighborNode)
                    break
                
        return results

    #Checks if a node is on a connected path
    def connectedNode(self, results, node, connected):
        for indx, path in enumerate(results):
            if node in path and connected[indx]:
                return True

    #Creates a list of paths between nodes
    def DFSVisit(self, v):
        results = []
        temp = []
        visited = [False] * (max(self.graph) + 1)
        
        while False in visited:
            visited[v] = True
            temp.append(v)
            i = self.pickNode(v, visited)
            if visited[i] == False and i != len(visited) - 1:
                v = i
            else:
                results.append(temp)
                temp = []
                if False in visited:
                    v = visited.index(False)
        return results

    #Checks if a cell's neighbors have been visited
    def checkNeighbors(self, v, visited):
        nodeList = []
        for i in self.graph[v]:
            nodeList.append(visited[i])
        return False in nodeList

    #Randomly returns the unexplored neighbor of an explored node
    def pickNode(self, v, visited):
        if not self.checkNeighbors(v, visited):
            return v
        
        unexplored = random.choice(self.graph[v])
        while visited[unexplored] == True:
            unexplored = random.choice(self.graph[v])
        return unexplored

    #Given a list of nodes, draws map accordingly
    def draw(self, array, sides, startPoint):
        t = turtle.Turtle()
        s = turtle.getscreen()

        coordStart = self.convert(startPoint, sides)
        
        t.up()
        t.goto(coordStart)
        t.down()
        t.ht()
        t.pen(pencolor="white", fillcolor="orange", pensize=15, speed=100)

        for i in array:
            coords = self.convert(i, sides)
            t.goto(coords[0], coords[1])

    #Converts a numerical value to a coordinate value, cell 15px wall 5px
    def convert(self, num, sides):
         x = num % sides
         y = int(num / sides)
         return ((x * 20) - 300, 300 - (y * 20))        
         

if __name__ == "__main__":
    maze = Maze(700, 700)
    #Issue with seeds 12,13,17,20
    maze.main(20)
    #maze.main(30)
    
