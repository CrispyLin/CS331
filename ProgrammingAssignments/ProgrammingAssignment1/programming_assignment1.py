# CS 331 Programming Assignment #1:
# Uninformed and Informed Search
# Name: Xinwei Lin
# School: Oregon State University
import sys
import os
from queue import PriorityQueue
import copy

class Node:
    def __init__(self):
        self.leftC = 0
        self.leftW = 0
        self.leftB = 0
        
        self.rightC = 0
        self.rightW = 0
        self.rightB = 0
        
        self.depth = 1


    # assignment operator overload
    def __eq__(self, other):
        if self.rightB==other.rightB and self.rightW==other.rightW and self.rightC==other.rightC and self.leftB==other.leftB and self.leftW==other.leftW and self.leftC==other.leftC:
            return True
        else:
            return False
    

    def __gt__(self, other):
        if self.heuristic_eval() > other.heuristic_eval():
            return True
        else:
            return False

    
    def __lt__(self, other):
        if self.heuristic_eval() < other.heuristic_eval():
            return True
        else:
            return False

    def printNode(self):
        print('['+ str(self.leftC) + ', ' + str(self.leftW) + ', ' + str(self.leftB) + '], ', end = "")
        print('['+ str(self.rightC) + ', ' + str(self.rightW) + ', ' + str(self.rightB) + ']')

    
    def get_String(self):
        s = ('['+ str(self.leftC) + ', ' + str(self.leftW) + ', ' + str(self.leftB) + '], ')
        s += ('['+ str(self.rightC) + ', ' + str(self.rightW) + ', ' + str(self.rightB) + ']')
        return s


    def heuristic_eval(self):
        heur = 0
        heur += self.leftC
        heur += self.leftW
        heur += self.leftB
        heur -= self.rightC
        heur -= self.rightW
        heur -= self.rightB
        return heur


def mov_chicken(toWhichSide, howMany,tempNode):
    if toWhichSide == 'right':
        tempNode.leftC -= howMany
        tempNode.rightC += howMany
    else: #else means moving chicken from right to left
        tempNode.rightC -= howMany
        tempNode.leftC += howMany
    

def mov_boat(toWhichSide,tempNode):
    if toWhichSide == 'right':
        tempNode.leftB -= 1
        tempNode.rightB += 1
    else:# mov boat to the left
        tempNode.rightB -= 1
        tempNode.leftB += 1
        

def mov_wolf(toWhichSide, howMany,tempNode):
    if toWhichSide == 'right':
        tempNode.leftW -= howMany
        tempNode.rightW += howMany
    else: #else means moving wolf from right to left
        tempNode.rightW -= howMany
        tempNode.leftW += howMany


# Put one chicken in the boat
def generator1(tempNode):
    if tempNode.leftB == 1:
        mov_chicken('right', 1, tempNode)
        mov_boat('right', tempNode)

    else: # else boat is on the right side where (node.rightB == 1)
        mov_chicken('left', 1, tempNode)
        mov_boat('left', tempNode)


# Put two chickens in the boat
def generator2(tempNode):
    if tempNode.leftB == 1:
        mov_chicken('right', 2, tempNode)
        mov_boat('right', tempNode)
    else:
        mov_chicken('left', 2, tempNode)
        mov_boat('left', tempNode)


# Put one wolf in the boat
def generator3(tempNode):
    if tempNode.leftB == 1:
        mov_wolf('right', 1, tempNode)
        mov_boat('right', tempNode)
    else:
        mov_wolf('left', 1, tempNode)
        mov_boat('left', tempNode)


# Put one wolf and one chicken in the boat
def generator4(tempNode):
    if tempNode.leftB == 1:
        mov_chicken('right', 1, tempNode)
        mov_wolf('right', 1, tempNode)
        mov_boat('right', tempNode)
    else:
        mov_chicken('left', 1, tempNode)
        mov_wolf('left', 1, tempNode)
        mov_boat('left', tempNode)

# Put two wolves in the boat
def generator5(tempNode):
    if tempNode.leftB == 1:
        mov_wolf('right', 2, tempNode)
        mov_boat('right', tempNode)
    else:
        mov_wolf('left', 2, tempNode)
        mov_boat('left', tempNode)


#checking if commandline arguments are enough
def commandlineCheck():
    if len(sys.argv) != 5:
        print('Please provide enough commandline arguments orderly!')
        exit()


def checkFiles():
    if not os.path.exists(sys.argv[1]):
        print("Please provide correct initial state file!")
        exit()
    if not os.path.exists(sys.argv[2]):
        print("Please provide correct goal state file!")
        exit()


def getMod():
    mod = sys.argv[3]
    mod = mod.lower()
    if mod == 'bfs':
        return 0
    elif mod == 'dfs':
        return 1
    elif mod == 'iddfs':
        return 2
    elif mod == 'astar':
        return 3
    else:
        print('Please provide correct mod option! (bfs/dfs/iddfs/astar)')
        exit()


# reading file and save data in an array
def readingFile(filename):
    fp = open(filename, "r")
    temp = []
    node = Node()
    allLines = fp.readlines()
    for line in allLines:
        aLineOfData = []
        for char in line.split(','):
            aLineOfData.append(int(char))
        temp.append(aLineOfData)
    fp.close()
    node.leftC = temp[0][0]
    node.leftW = temp[0][1]
    node.leftB = temp[0][2]
    node.rightC = temp[1][0]
    node.rightW = temp[1][1]
    node.rightB = temp[1][2]
    """
    print(data[0].leftC)
    print(data[0].leftW)
    print(data[0].leftB)
    """
    return node


# check to see if chicken is more than or euqal wolfs on both side, return true or false
def is_chicken_more_than_wolf(tempNode):
    if (tempNode.leftC >= tempNode.leftW or tempNode.leftC == 0) and (tempNode.rightC >= tempNode.rightW or tempNode.rightC == 0):
        return True
    else:
        return False


# check to see if all value stored in tempNode is not negative, return true for no negative values,
# return false for 1 or more negative values
def have_no_nagative_value(tempNode):
    if tempNode.leftC >= 0 and tempNode.leftW >= 0 and tempNode.rightC >= 0 and tempNode.rightW >=0:
        return True
    else:
        return False


# check to see if the node have been visited previously,
# more specificlly, not appear in the visited_nodes
def have_never_visited(tempNode, visited_nodes):
    for node in visited_nodes:
        if node == tempNode:
            return False
    return True


def bfs(startS,goalS, outputFile):
    # file descriptor for output
    fp_w = open(outputFile,'a')
    fp_w.write('bfs:\n')

    # set a counter for the node I have expanded
    num_expanded = 0
    # array to hold already visisted nodes
    visited_nodes = []
    # queue to hold nodes to check next
    queue = []

    visited_nodes.append(startS)
    queue.append(startS)

    while queue:
        # get the node from the front of the queue
        currentNode = queue.pop(0)
        currentNode.printNode()
        fp_w.write(currentNode.get_String() + '\n')
        # check if the current state is our goal state
        if currentNode == goalS:
            # output result on screen and output file
            print('Goal state found\n')
            print('Number of expanded nodes: ' + str(num_expanded))
            fp_w.write('Goal state found\n')
            fp_w.write('Number of expanded nodes: ' + str(num_expanded) + '\n\n')
            fp_w.close()
            return # exit the method
        num_expanded += 1

        # below code will be executed if the current Node is not the goal node
        # check 5 actions and add vaild and not the same states to the queue
        for i in range(0, 5):
            tempNode = copy.deepcopy(currentNode)
            if i==0:
                generator1(tempNode)
            elif i==1:
                generator2(tempNode)
            elif i==2:
                generator3(tempNode)
            elif i==3:
                generator4(tempNode)
            else:
                generator5(tempNode)
            if is_chicken_more_than_wolf(tempNode) and have_no_nagative_value(tempNode) and have_never_visited(tempNode, visited_nodes):
                visited_nodes.append(tempNode)
                queue.append(tempNode)
    
    # when queue is empty and the method is still running means the goal state is not found, print the message
    print("No solution for this case\n\n")


def dfs(startS,goalS, outputFile):
    # file descriptor for output
    fp_w = open(outputFile,'a')
    fp_w.write('dfs:\n')

    # set a counter for the node I have expanded
    num_expanded = 0
    # array to hold already visisted nodes
    visited_nodes = []
    # queue to hold nodes to check next
    queue = []

    visited_nodes.append(startS)
    queue.append(startS)

    while queue:
        # get the node from the front of the queue
        currentNode = queue.pop(0)
        currentNode.printNode()
        fp_w.write(currentNode.get_String() + '\n')
        # check if the current state is our goal state
        if currentNode == goalS:
            # output result on screen and output file
            print('Goal state found\n')
            print('Number of expanded nodes: ' + str(num_expanded))
            fp_w.write('Goal state found\n')
            fp_w.write('Number of expanded nodes: ' + str(num_expanded) + '\n\n')
            fp_w.close()
            return # exit the method
        num_expanded += 1

        # below code will be executed if the current Node is not the goal node
        # check 5 actions and add vaild and not the same states to the queue
        for i in range(0, 5):
            tempNode = copy.deepcopy(currentNode)
            if i==0:
                generator1(tempNode)
            elif i==1:
                generator2(tempNode)
            elif i==2:
                generator3(tempNode)
            elif i==3:
                generator4(tempNode)
            else:
                generator5(tempNode)
            if is_chicken_more_than_wolf(tempNode) and have_no_nagative_value(tempNode) and have_never_visited(tempNode, visited_nodes):
                visited_nodes.append(tempNode)
                queue.insert(0, tempNode)
    
    # when queue is empty and the method is still running means the goal state is not found, print the message
    print("No solution for this case\n\n")
    return


def iddfs(startS,goalS, outputFile):
    # file descriptor for output
    fp_w = open(outputFile,'a')
    print('iddfs:')
    fp_w.write('iddfs:\n')
    num_expanded = 0

    for maxDepth in range(0, 9999):
        # set a counter for the node I have expanded
        sol_num_expanded = 0
        # array to hold already visisted nodes
        visited_nodes = []
        # queue to hold nodes to check next
        queue = []

        visited_nodes.append(startS)
        queue.append(startS)
        print("maxDepth: ", maxDepth)
        fp_w.write("maxDepth: " + str(maxDepth) + '\n')
        while queue and maxDepth > 0:
            # get the node from the front of the queue
            currentNode = queue.pop(0)
            currentNode.printNode()
            fp_w.write(currentNode.get_String() + '\n')

            # check if the current state is our goal state
            if currentNode == goalS:
                # output result on screen and output file
                print('Goal state found\n')
                print('Number of expanded nodes for solution path: ' + str(sol_num_expanded))
                print('Total number of expanded nodes in all iterations: ' + str(num_expanded))
                fp_w.write('Goal state found\n')
                fp_w.write('Number of expanded nodes for solution path: ' + str(sol_num_expanded) + '\n')
                fp_w.write('Total number of expanded nodes in all iterations: ' + str(num_expanded) + '\n\n')
                fp_w.close()
                return # exit the method
            num_expanded += 1
            sol_num_expanded += 1
            # if depthLimit is reached, dont expand this node further
            if currentNode.depth == maxDepth:
                continue
            # below code will be executed if the current Node is not the goal node
            # check 5 actions and add vaild and not the same states to the queue
            for i in range(0, 5):
                tempNode = copy.deepcopy(currentNode)
                tempNode.depth += 1
                if i==0:
                    generator1(tempNode)
                elif i==1:
                    generator2(tempNode)
                elif i==2:
                    generator3(tempNode)
                elif i==3:
                    generator4(tempNode)
                else:
                    generator5(tempNode)
                if is_chicken_more_than_wolf(tempNode) and have_no_nagative_value(tempNode) and have_never_visited(tempNode, visited_nodes):
                    visited_nodes.append(tempNode)
                    queue.insert(0, tempNode)
        
        # when queue is empty and the method is still running means the goal state is not found, print the message
        print("No solution for this maxDepth\n\n")
        fp_w.write("No solution for this maxDepth\n\n")
    print('no solution')
    fp_w.write("no solution\n\n")
    return


def astar(startS,goalS, outputFile):
    # file descriptor for output
    fp_w = open(outputFile,'a')
    fp_w.write('astar:\n')

    # set a counter for the node I have expanded
    num_expanded = 0
    # array to hold already visisted nodes
    visited_nodes = []
    # initialize variable pq
    pq = []
    # qp to hold nodes to check next
    pq = PriorityQueue()
    # put start state into pq with heuristic evaluation and visisted_nodes 
    pq.put((startS.heuristic_eval(), startS))
    visited_nodes.append(startS)

    while pq:
        currentObj = pq.get()
        currentNode = currentObj[1]
        currentNode.printNode()
        fp_w.write(currentNode.get_String() + '\n')

        # check if the current state is our goal state
        if currentNode == goalS:
            # output result on screen and output file
            print('Goal state found\n')
            print('Number of expanded nodes: ' + str(num_expanded))
            fp_w.write('Goal state found\n')
            fp_w.write('Number of expanded nodes: ' + str(num_expanded) + '\n\n')
            fp_w.close()
            return # exit the method
        num_expanded += 1

        # below code will be executed if the current Node is not the goal node
        # check 5 actions and add vaild and not the same states to the queue
        for i in range(0, 5):
            tempNode = copy.deepcopy(currentNode)
            if i==0:
                generator1(tempNode)
            elif i==1:
                generator2(tempNode)
            elif i==2:
                generator3(tempNode)
            elif i==3:
                generator4(tempNode)
            else:
                generator5(tempNode)
            if is_chicken_more_than_wolf(tempNode) and have_no_nagative_value(tempNode) and have_never_visited(tempNode, visited_nodes):
                visited_nodes.append(tempNode)
                pq.put((tempNode.heuristic_eval(), tempNode))
    # when queue is empty and the method is still running means the goal state is not found, print the message
    print("No solution for this case\n\n")
    return


    return


def main():
    # check if user provide enough commandline arguments
    commandlineCheck()
    # check if initial state file and goal state file exists
    checkFiles()
    #after checking the files, 3 files become avaliable to use
    outputFile = sys.argv[4]
    # check if user provide correct mod option, and get that mod option
    mode = getMod()
    #reading files into array form
    startState = readingFile(sys.argv[1])
    goalState = readingFile(sys.argv[2])


    if mode == 0:
        bfs(startState,goalState, outputFile)
    elif mode == 1:
        dfs(startState,goalState, outputFile)
    elif mode == 2:
        iddfs(startState,goalState, outputFile)
    else:
        astar(startState,goalState, outputFile)


    # end of the main function, close the program
    exit()


#running main method
main()