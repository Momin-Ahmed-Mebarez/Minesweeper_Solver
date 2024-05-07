#Mistakes the region parameter should be changed to a variable containg the region size

import pyautogui as gui
import time
board = []
hints = []
mines = []
boardDimList = []
height = 0
width = 0

#This function is used once to return the width and height between each square
def boardDimCalc(board):
    global height
    global width
    global boardDimList

    #Calculating the width between squares (The width is fixed for every square getting it once is enough) 
    width = abs(board[0][0] - board[1][0])

    #Calculating the height between squares (The height is fixed for every square getting it once is enough)
    for i in range(len(board)):
        #Since we don't know the coordinates of the last square we are checking with every square (blocks in the same row will have zero height between them)
        if board[i][1] - board[i + 1][1] != 0:
            height = abs(board[i][1] - board[i + 1][1])
            boardDimList = [height, width]
            return boardDimList



#A function to find squares (Not solved and not a hint) then return the coordinates of every square as (x,y)
#We use this fucntion at the start to get the every square and then use it to keep the bord updated from the script perspective
def countBoard():
    board = []
    #If the program is not working at all the region parameter should be changed a very big number will gurantee that it works but will make it slower
    for square in gui.locateAllOnScreen("Square.png",region =(431,106,319,403)):
        board.append([gui.center(square).x , gui.center(square).y])
    return board

#A function to get the coordinates of every hint then return one big array that contain an array of every hint based on it's number 
def countHints():
    oneHint = []
    twoHints = []
    threeHints = []
    hints = []
    
    for hint in gui.locateAllOnScreen("1.png",region =(431,106,319,403)):
        oneHint.append([gui.center(hint).x, gui.center(hint).y])
    hints.append(oneHint)
    
    for hint in gui.locateAllOnScreen("2.png",region =(431,106,319,403)):
        twoHints.append([gui.center(hint).x, gui.center(hint).y])
    hints.append(twoHints)
    
    for hint in gui.locateAllOnScreen("3.png",region =(431,106,319,403)):
        threeHints.append([gui.center(hint).x, gui.center(hint).y])
    hints.append(threeHints)
    
    return hints

#Adding the coodrinations of every thing near the hint
def neighbourFinder(hint):
    neighbours = []
    
    rtCorner = [hint[0] + width, abs(hint[1] - height)]
    neighbours.append(rtCorner)

    ltCorner = [abs(hint[0] - width), abs(hint[1] - height)]
    neighbours.append(ltCorner)

    top = [hint[0], abs(hint[1] - height)]
    neighbours.append(top)
    
    right = [hint[0] + width, hint[1]]
    neighbours.append(right)
    
    left = [hint[0] - width, hint[1]]
    neighbours.append(left)
    
    bottom = [hint[0], hint[1] + height]
    neighbours.append(bottom)
    
    rbCorner = [hint[0] + width, hint[1] + height]
    neighbours.append(rbCorner)
    
    lbCorner = [abs(hint[0] - width), hint[1] + height]
    neighbours.append(lbCorner)
    return neighbours

#The main logic of deciding the move
def moveMaker(board, hint, hints, neighbours):
    global mines
    
    connectedMines = 0
    connectedSquares = 0
    connectedSquaresList = []
    connectedHints = 0
    toDo = ""
    for neighbour in neighbours:
        if neighbour in mines:
            connectedMines += 1
            continue
        
        if neighbour in board:
            connectedSquares += 1
            connectedSquaresList.append(neighbour)
            continue
        
        if neighbour in hints[0]:
            connectedHints += 1
            continue
        
    #One hint
    if hint in hints[0]:
        toDo = rules(1, connectedSquares, connectedMines)

    #Two hints
    if hint in hints[1]:
        toDo = rules(2, connectedSquares, connectedMines)

    #Three hints
    if hint in hints[2]:
        toDo = rules(3, connectedSquares, connectedMines)
        
    if toDo == "safe":
        for square in connectedSquaresList:
            gui.click(square)
        return toDo
    
    elif toDo == "mine":
        for square in connectedSquaresList:
            mines.append(connectedSquaresList[0])
        return toDo


def rules(hintType, connectedSquares, connectedMines):

    if connectedSquares != 0:
        if connectedMines == hintType: return "safe"
        if connectedSquares + connectedMines == hintType: return "mine"
    
def main():
    input("Hit enter to start")
    
    board = countBoard()
    boardDim = boardDimCalc(board)
    #This can be any random x and y on the board to start it
    gui.click(625,316)
    #Our program main loop
    while True:
        board = countBoard()
        hints = countHints()

        #Remove squares that are certian to be mines
        #First iteration will always keep the same board
        for square in board:
            if square in mines:
                board.remove(square)

        #Break the loop when no more squares can be found
        if board == []: break

        #Iretate through the every hint coordinate
        for hintList in hints:
            for hint in hintList:
                
                neighbours = neighbourFinder(hint)
                move = moveMaker(board, hint, hints, neighbours)
                
                if move == "mine":
                    break
            if move == "mine":
                break
    print("You win")


if __name__ == "__main__":
    main()
