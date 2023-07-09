#########################################
# 89078  - Luis Filipe Correia do Couto #
# 103248 - Jose Miguel Guardado Silva   #
#########################################

import math
import heapq
import time

class SearchProblem:

    '''
    Checks if current state is the solution
        - if target car touches the right side of the map, the solution is found
    '''
    def goal_test(dimensions, state): 
        if (state[0].index("A")%dimensions + state[0].count("A") - 1) == dimensions-1:
            return True
        else:
            return False   


    '''
    Calculates heuristic of current state, defined as the sum of:
        - the number of unique cars blocking the way
        - the minimum number of unique cars blocking the cars that are blocking the way 
    '''
    def calculate_heuristic(dimensions, state):
        targetCar = [i for i, letter in enumerate(state) if letter == "A"]
        targetPath = state[targetCar[-1]+1:targetCar[-1]+(dimensions - (targetCar[-1]%dimensions))]
        blockingCars = set([i for i in targetPath if i !="A" and i !="o" and i !="x"])

        blockingCarsPos = {}
        for car in blockingCars:
            carPos = [i for i, letter in enumerate(state) if letter == car]
            backward = carPos[0]
            forward = (dimensions**2) - carPos[-1]

            for i in range(1, backward+1):
                if i == 1 and state[backward-i] == state[backward]:
                    blockingCarsPos[car] = ("H", carPos)

                elif i == dimensions and state[backward-i] == state[backward]:
                    blockingCarsPos[car] = ("V", carPos)

                else:
                    continue

            for i in range(1, forward+1):
                if i == 1 and state[forward+i] == state[forward]:
                    blockingCarsPos[car] = ("H", carPos)

                elif i == dimensions and state[forward+i] == state[forward]:
                    blockingCarsPos[car] = ("V", carPos)
                
                else:
                    continue
        
        blockingTheBlockers = {}
        for car, pos in blockingCarsPos.items():
            backward = pos[1][0]
            forward = (dimensions**2) - pos[1][-1]
            
            if pos[0] == "H":
                leftCars = []
                rightCars = []
                for i in range(1, backward+1):
                    validLeft = pos[1][0]-i >= 0

                    if validLeft and i == 1 and pos[1][0]%dimensions != 0 and state[pos[1][0]] != state[pos[1][0]-i] and state[pos[1][0]-i] != 'o' and state[pos[1][0]-i] != 'x':
                        leftCars.append(state[pos[1][0]-i])
                    
                    else:
                        continue

                for i in range(1, forward+1):
                    validRight = pos[1][-1]+i < dimensions**2
                    
                    if validRight and i == 1 and math.floor(pos[1][-1]/dimensions) != dimensions-1 and state[pos[1][-1]] != state[pos[1][-1]+i] and state[pos[1][-1]+i] != 'o' and state[pos[1][-1]+i] != 'x':
                        rightCars.append(state[pos[1][0]+i])
                    
                    else:
                        continue

                blockingTheBlockers[car] = min(len(set(leftCars)), len(set(rightCars)))      

            elif pos[0] == "V":
                topCars = []
                botCars = []

                for i in range(1, backward+1):
                    validTop = pos[1][0]-i >= 0

                    if validTop and i == dimensions and pos[1][0]%dimensions != 0 and state[pos[1][0]] != state[pos[1][0]-i] and state[pos[1][0]-i] != 'o' and state[pos[1][0]-i] != 'x':
                        topCars.append(state[pos[1][0]-i])

                    else:
                        continue        
                    

                for i in range(1, forward+1):
                    validBot = pos[1][-1]+i < dimensions**2

                    if validBot and i == dimensions and math.floor(pos[1][-1]/dimensions) != dimensions-1  and state[pos[1][-1]] != state[pos[1][-1]+i] and state[pos[1][-1]+i] != 'o' and state[pos[1][-1]+i] != 'x':
                        botCars.append(state[pos[1][-1]+i])

                    else:
                        continue    
        
                blockingTheBlockers[car] = min(len(set(topCars)), len(set(botCars)))  

            else:
                continue
        
        return len(blockingCars) + sum(blockingTheBlockers.values())

    '''
    Checks if current cursor position is an empty position, blocked position or car 
        - returns ("o", current index) if position is empty
        - returns ("x", current index) if position is blocked
        - returns (orientation (vertical "V" or horizontal "H"), current index, index of each occurence) if position is car
    '''
    def calculate_coordinates(dimensions, state, cursor): 
        currIndex = (dimensions*cursor[1])+cursor[0]

        if state[0][currIndex] == 'o':
            return ("o", currIndex)
        
        if state[0][currIndex] == "x":
            return ("x", currIndex)

        if currIndex == 0:
            if state[0][currIndex+1] == state[0][currIndex]:
                return ("H", currIndex, [i for i, letter in enumerate(state[0]) if letter == state[0][currIndex]])
            
            elif state[0][currIndex+dimensions] == state[0][currIndex]:
                return ("V", currIndex, [i for i, letter in enumerate(state[0]) if letter == state[0][currIndex]])
            
            else:
                raise Exception("Invalid Vehicle!")

        elif currIndex == (dimensions**2)-1:
            if state[0][currIndex-1] == state[0][currIndex]:
                return ("H", currIndex, [i for i, letter in enumerate(state[0]) if letter == state[0][currIndex]])
            
            elif state[0][currIndex-dimensions] == state[0][currIndex]:
                return ("V", currIndex, [i for i, letter in enumerate(state[0]) if letter == state[0][currIndex]])

            else:
                raise Exception("Invalid Vehicle!")

        else:
            backward = currIndex
            forward = (dimensions**2) - currIndex 

            for i in range(1, backward+1):
                if i == 1 and state[0][currIndex-i] == state[0][currIndex]:
                    return ("H", currIndex, [i for i, letter in enumerate(state[0]) if letter == state[0][currIndex]])

                elif i == dimensions and state[0][currIndex-i] == state[0][currIndex]:
                    return ("V", currIndex, [i for i, letter in enumerate(state[0]) if letter == state[0][currIndex]])

                else:
                    continue

            for i in range(1, forward+1):
                if i == 1 and state[0][currIndex+i] == state[0][currIndex]:
                    return ("H", currIndex, [i for i, letter in enumerate(state[0]) if letter == state[0][currIndex]])

                elif i == dimensions and state[0][currIndex+i] == state[0][currIndex]:
                    return ("V", currIndex, [i for i, letter in enumerate(state[0]) if letter == state[0][currIndex]])

                else:
                    continue        
                    
            raise Exception("Invalid State")      
            

    '''
    Get possible moves according to current cursor position and/or selected position
        - accepts wasd only if the corresponding next cursor position is free 
        and/or car can be moved there
        - accepts " " only if current cursor position is selected and/or contains a car
    '''
    def possible_moves(dimensions, state):
        posMoves = []

        if state[2] and state[2] is not None:
            selectedDir = (SearchProblem.calculate_coordinates(dimensions, state,  state[1]))
            
            if selectedDir[0] != "o" and selectedDir[0] != "x":
                posMoves.append(" ")

            if(selectedDir[0] == "H"):
                if selectedDir[2][0]%dimensions > 0 and state[0][selectedDir[2][0]-1] == "o":
                    posMoves.append("a")

                if (selectedDir[2][-1]%dimensions)+1 < dimensions and state[0][selectedDir[2][-1]+1] == "o":
                    posMoves.append("d")

            elif(selectedDir[0] == "V"):
                if math.floor(selectedDir[2][0]/dimensions) > 0 and state[0][selectedDir[2][0]-dimensions] == "o":
                    posMoves.append("w")

                if math.floor(selectedDir[2][-1]/dimensions)+1 < dimensions and state[0][selectedDir[2][-1]+dimensions] == "o":
                    posMoves.append("s")

        else:
            if state[1][0] > 0: 
                posMoves.append("a")  

            if state[1][0] < dimensions - 1:
                posMoves.append("d")  
            
            if state[1][1] > 0:
                posMoves.append("w")  

            if state[1][1] < dimensions - 1:
                posMoves.append("s")

            selectedDir = SearchProblem.calculate_coordinates(dimensions, state, state[1])
            if selectedDir[0] != "o" and selectedDir[0] != "x":
                posMoves.append(" ")
    
        return posMoves


    '''
    Performs action on current state
        - returns new state defined as (updated map, updated cursor, updated selected)
    '''
    def perform_action(dimensions, state, action):
        if not state[2] or state[2] is None:
            if action == "w":
                return (state[0], [state[1][0],state[1][1]-1], state[2])

            elif action == "s":
                return (state[0], [state[1][0],state[1][1]+1], state[2])

            elif action == "a":
                return (state[0], [state[1][0]-1,state[1][1]], state[2])

            elif action == "d":
                return (state[0], [state[1][0]+1,state[1][1]], state[2])

            else:
                selectedDir = SearchProblem.calculate_coordinates(dimensions, state, state[1])
                if selectedDir[0] != "o" and selectedDir[0] != "x":
                    return (state[0], state[1], state[1])
    
        else:
            selectedDir = (SearchProblem.calculate_coordinates(dimensions, state, state[1]))
            mapList = list(state[0])

            if selectedDir[0] == "V":
                if action == "w":
                    mapList[selectedDir[2][0]-dimensions] = state[0][selectedDir[1]]
                    mapList[selectedDir[2][-1]] = "o"
                    mapList = "".join(i for i in mapList)
                    return (mapList, [state[1][0],state[1][1]-1], [state[1][0],state[1][1]-1])

                elif action == "s":
                    mapList[selectedDir[2][0]] = "o"
                    mapList[selectedDir[2][-1]+dimensions] = state[0][selectedDir[1]]
                    mapList = "".join(i for i in mapList)
                    return (mapList, [state[1][0],state[1][1]+1], [state[1][0],state[1][1]+1])

                else:
                    return (state[0], state[1], "")

            elif selectedDir[0] == "H":
                if action == "a":
                    mapList[selectedDir[2][-1]] = "o"
                    mapList[selectedDir[2][0]-1] = state[0][selectedDir[1]]
                    mapList = "".join(i for i in mapList)
                    return (mapList, [state[1][0]-1,state[1][1]], [state[1][0]-1,state[1][1]])

                elif action == "d":
                    mapList[selectedDir[2][0]] = "o"
                    mapList[selectedDir[2][-1]+1] = state[0][selectedDir[1]]
                    mapList = "".join(i for i in mapList)
                    return (mapList, [state[1][0]+1,state[1][1]], [state[1][0]+1,state[1][1]])

                else: 
                    return (state[0], state[1], "")

            else:
                return state


class Node:
    def __init__(self, state, parent, heuristic, depth, cost):
        self.state = state
        self.parent = parent
        self.heuristic = heuristic
        self.depth = depth
        self.cost = cost
        self.eval = self.cost + self.heuristic if self.cost < self.heuristic else (self.cost + (2*1.5-1)*self.heuristic) / 1.5
    
    def __lt__(self, other):
        return self.eval < other.eval

    def __str__(self):
        return str(self.state) + ", " + str(self.parent) + ", " + str(self.depth) + ", " + str(self.eval)

    def __repr__(self):
        return str(self)


class SearchTree:
    alreadyVisited = {}

    def __init__(self, start, dimensions, cursorPos, selectPos): 
        self.root = Node((start, cursorPos, selectPos), None, SearchProblem.calculate_heuristic(dimensions, start), 0, 0)
        self.dimensions = dimensions
        self.cursorPos = cursorPos
        self.selectPos = selectPos
        self.open_nodes = []
        heapq.heappush(self.open_nodes, (self.root.eval, self.root))

    def get_path(self, node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return path

    def aStar(self, level):
        maxNodesAllowed = level * 10000
        maxTimeAllowed = 3
        timeStart = time.process_time()
        numNodes = 0
        closed = self.alreadyVisited
        closestNode = self.root

        while self.open_nodes != []:
            node = heapq.heappop(self.open_nodes)

            # If time taken has exceeded limit or max nodes reached, return path using best node found so far
            if time.process_time()-timeStart > maxTimeAllowed or numNodes > maxNodesAllowed:
                self.alreadyVisited = closed
                return self.get_path(closestNode)

            # If solution is found, return path using solution node
            if SearchProblem.goal_test(self.dimensions, node[1].state):
                self.alreadyVisited.clear()
                self.solution = node[1]
                return self.get_path(node[1])

            numNodes +=1

            # Check possible movements and manage nodes accordingly
            for action in SearchProblem.possible_moves(self.dimensions, node[1].state):
                newstate = SearchProblem.perform_action(self.dimensions, node[1].state, action)

                visited = repr(newstate) in closed

                if not visited or (visited and node[1].cost+1 < closed[repr(newstate)].cost):
                    newnode = Node(newstate, node[1], SearchProblem.calculate_heuristic(self.dimensions, newstate[0]), node[1].depth+1, node[1].cost+1)

                    closed[repr(newstate)] = newnode
                    
                    if newnode.heuristic <= closestNode.heuristic:
                        closestNode = newnode
                    
                    if (newnode.eval, newnode) not in self.open_nodes:
                        heapq.heappush(self.open_nodes, (newnode.eval, newnode))

        return self.get_path(closestNode)

    def solve(self, level):
        solution = self.aStar(level)
        movesToMake = []
        
        for i in range(0, len(solution)-1):
            if (not solution[i][2] and solution[i+1][2]) or (solution[i][2] and not solution[i+1][2]):
                movesToMake.append(" ")

            if solution[i][1][0] > solution[i+1][1][0]:
                movesToMake.append("a") 

            if solution[i][1][0] < solution[i+1][1][0]:
                movesToMake.append("d")

            if solution[i][1][1] < solution[i+1][1][1]:
                movesToMake.append("s") 

            if solution[i][1][1] > solution[i+1][1][1]:
                movesToMake.append("w") 

        return movesToMake
       