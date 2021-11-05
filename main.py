# Assignment 1
# Written by Tomas Pereira 40128504
# For COMP 472 Section AJ-X – Summer 2021
# --------------------------------------------------------
from queue import PriorityQueue

print("Welcome to the Covid-19 Map Simulation \n")
print("Please enter the grid size for the map to be created")
valRow = input("\tRow length: ")
valColumn = input("\tColumn length: ")

innerGrid = [[0 for x in range(int(valColumn))] for y in range(int(valRow))]

startNum = 0
for x in range(int(valRow)):
    for y in range(int(valColumn)):
        startNum += 1
        innerGrid[x][y] = startNum
print(innerGrid)
numForEntry = 0
# Keeps track of which nodes are goal positions based on the input of the user
# Serves as the goal states for the heuristic function
goalPositions = []

print("\nWhich positions should be Quarantine Places: ")
while numForEntry != -1:
    numForEntry = input("Enter Position (Enter -1 to end): ")
    if int(numForEntry)==-1:
       break
    for i in range(0, int(valRow)):
       for j in range(0, int(valColumn)):
           if innerGrid[i][j]==int(numForEntry):
               innerGrid[i][j] = 'Q'
               goalPositions.append((i, j+1))

print("Done Selecting Quarantine Places")
print(innerGrid)

numForEntry = 0
print("\nWhich positions should be Vaccine Spots: ")
while numForEntry != -1:
    numForEntry = input("Enter Position (Enter -1 to end): ")
    if int(numForEntry) == -1:
        break
    for i in range(0, int(valRow)):
        for j in range(0, int(valColumn)):
            if innerGrid[i][j] == int(numForEntry):
                innerGrid[i][j] = 'V'

print("Done Selecting Vaccine Spots")
print(innerGrid)

numForEntry = 0
print("\nWhich positions should be Playgrounds: ")
while numForEntry != -1:
    numForEntry = input("Enter Position (Enter -1 to end): ")
    if int(numForEntry) == -1:
        break
    for i in range(0, int(valRow)):
        for j in range(0, int(valColumn)):
            if innerGrid[i][j] == int(numForEntry):
                innerGrid[i][j] = 'P'
print("Done Selecting Playgrounds")
print(innerGrid)

numForEntry = 0
print("\nWhich position should be the Start Point: ")
numForEntry = input("Enter Position: ")
for i in range(0, int(valRow)):
        for j in range(0, int(valColumn)):
            if innerGrid[i][j] == int(numForEntry):
                innerGrid[i][j] = 'S'
                startY = i
                startX = j
print("Done Selecting Start Point")
print(innerGrid)

outerGrid = [["@" for x in range(int(valColumn)+1)] for y in range(int(valRow)+1)]
outerGrid[startY][startX+1] = 'S'

print("\nHere is the Finalized ASCII Grid: ")
for i in range(int(valRow)+1):
    print(outerGrid[i])
    if(i<int(valRow)):
        print('   ', end=" ")
        print('    '.join([str(x) for x in innerGrid[i]]))

def getEdgeCost(cellGrid, startNodeY, startNodeX, endNodeY, endNodeX):
    edgeCost = 0
    smallerY = 0
    largerX = 0

    if(startNodeX > endNodeX):
        largerX = startNodeY
    else:
        largerX = endNodeY
    if(startNodeY < endNodeY):
        smallerY = startNodeY
    else:
        smallerY = endNodeY

    # The Case where the player must move on the very top or very bottom on the board
    if ((startNodeY == 0 and endNodeY == 0) or (startNodeY == int(valRow)+1 and endNodeY == int(valRow)+1)):
        if(cellGrid[endNodeY][largerX-1] == 'Q'):
            edgeCost = 0
        elif (cellGrid[endNodeY][largerX - 1] == 'P'):
            edgeCost = 3
        elif (cellGrid[endNodeY][largerX - 1] == 'V'):
            edgeCost = 2
        else:
            edgeCost = 1
    # The Case where the player must move on the very left or very right on the board
    elif ((startNodeX == 0 and endNodeX == 0) or (startNodeX == int(valColumn)+1 and endNodeX == int(valColumn)+1)):
        if (cellGrid[smallerY][endNodeX] == 'Q'):
            edgeCost = 0
        elif (cellGrid[smallerY][endNodeX] == 'P'):
            edgeCost = 3
        elif (cellGrid[smallerY][endNodeX] == 'V'):
            edgeCost = 2
        else:
            edgeCost = 1
    # The Case where the player must make a vertical move in the board
    elif(startNodeX == endNodeX):
        firstTile = cellGrid[smallerY][startNodeX-1]
        secondTile = cellGrid[smallerY][startNodeX]
        if(firstTile == 'Q'):
            firstEdge = 0
        elif(firstTile == 'P'):
            firstEdge = 3
        elif(firstTile == 'V'):
            firstEdge = 2
        else:
            firstEdge = 1

        if (secondTile == 'Q'):
            secondEdge = 0
        elif (secondTile == 'P'):
            secondEdge = 3
        elif (secondTile == 'V'):
            secondEdge = 2
        else:
            secondEdge = 1

        if (firstTile == 'P' and secondTile == 'P'):
            edgeCost = 1000
        else:
            edgeCost = (firstEdge+secondEdge) / 2
    # The Case where the player must make a horizontal move in the board
    elif (startNodeY == endNodeY):
        firstTile = cellGrid[startNodeY-1][endNodeX-1]
        secondTile = cellGrid[startNodeY][endNodeX-1]
        if (firstTile == 'Q'):
            firstEdge = 0
        elif (firstTile == 'P'):
            firstEdge = 3
        elif (firstTile == 'V'):
            firstEdge = 2
        else:
            firstEdge = 1

        if (secondTile == 'Q'):
            secondEdge = 0
        elif (secondTile == 'P'):
            secondEdge = 3
        elif (secondTile == 'V'):
            secondEdge = 2
        else:
            secondEdge = 1

        if (firstTile == 'P' and secondTile == 'P'):
            edgeCost = 1000
        else:
            edgeCost = (firstEdge + secondEdge) / 2

    return edgeCost

# A function which takes as input, the current (X,Y) of the node and returns
# a list of the possible nodes that can be reached within one edge
def moveList(currentY, currentX):
    nextNodes = []
    # If at the top left node
    if(currentY==0 and currentX == 0):
        nextNodes.append((0, 1))
        nextNodes.append((1,0))
    # If at the bottom right node
    elif(currentY==int(valRow) and currentX==int(valColumn)):
         nextNodes.append((int(valRow)-1, int(valColumn)))
         nextNodes.append((int(valRow), int(valColumn)-1))
    # If at the bottom left node
    elif (currentY==int(valRow) and currentX==0):
        nextNodes.append((int(valRow) - 1, int(valColumn)))
        nextNodes.append((int(valRow), int(valColumn) + 1))
    # If at the top right node
    elif (currentY == 0 and currentX == int(valColumn)):
        nextNodes.append((int(valRow), int(valColumn) -1))
        nextNodes.append((int(valRow)+1, int(valColumn)))
    # If at the top side of grid
    elif (currentY==0):
        nextNodes.append((currentY, currentX-1))
        nextNodes.append((currentY, currentX+1))
        nextNodes.append((currentY+1, currentX))
    # If at the bottom side of grid
    elif (currentY==int(valRow)):
        nextNodes.append((currentY, currentX-1))
        nextNodes.append((currentY, currentX+1))
        nextNodes.append((currentY-1, currentX))
    # If at the left side of grid
    elif (currentX==0):
        nextNodes.append((currentY-1, currentX))
        nextNodes.append((currentY+1, currentX))
        nextNodes.append((currentY, currentX+1))
    # If at the right side of grid
    elif (currentX==int(valColumn)):
        nextNodes.append((currentY-1, currentX))
        nextNodes.append((currentY+1, currentX))
        nextNodes.append((currentY, currentX-1))
    else:
        nextNodes.append((currentY - 1, currentX))
        nextNodes.append((currentY + 1, currentX))
        nextNodes.append((currentY, currentX - 1))
        nextNodes.append((currentY, currentX+1))
    return nextNodes

# Manhattan Distance Heuristic
# Takes the current (x,y) and the list of goal states to estimate the distance to a goal
def manhattanHeuristic(yVal, xVal, goalList):
    heuristicValue = 1000
    for currentGoal in goalList:
        yGoalCurrent = currentGoal[0]
        xGoalCurrent = currentGoal[1]
        heuristicValueCurrent = abs(yVal - yGoalCurrent) + abs(xVal - xGoalCurrent)
        if(heuristicValueCurrent<heuristicValue):
            heuristicValue = heuristicValueCurrent
    return heuristicValue

# A* Algorithm to determine the cheapest path to the goal
# goalList is goalPositions List from above
def a_star_algorithm(startY, startX, goalList):
    closedList = []
    openList = PriorityQueue(0)
    costOfPath = -1
    currentX = startX
    currentY = startY
    openList.put((10, (startY, startX)))
    while not openList.empty():
        currentTuple = openList.get()
        openList = None
        openList = PriorityQueue(0)
        closedList.append(currentTuple[1])
        costOfPath += getEdgeCost(innerGrid, currentY, currentX, currentTuple[1][0], currentTuple[1][1])
        currentY = currentTuple[1][0]
        currentX = currentTuple[1][1]
        nextMoves = moveList(currentY, currentX)
        # The algorithm checks if we have reached one of the goal positions
        for goal in goalList:
            if (goal == (currentY, currentX)):
                print("\nA solution was found: (Coordinates Correspond to Position on Node Grid)")
                print("\tCost of Path: ", end="")
                print(costOfPath)
                for node in closedList:
                    print(node)
                return
        # The list of available moves is created and evaluated
        for move in nextMoves:
            if move in closedList:
                continue
            hn = manhattanHeuristic(move[0], move[1], goalList)
            gn = 1.5 * getEdgeCost(innerGrid, currentY, currentX, move[0], move[1])
            fn = hn + gn
            openList.put((fn, (move[0], move[1])))
    print("No path is found. Please Try Again!")
    return

print("\n----- Starting the A* Algorithm for Role C -----")
a_star_algorithm(startY, startX+1, goalPositions)

print("\n\n")
input("Press enter to exit ;)")




