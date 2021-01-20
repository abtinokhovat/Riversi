import turtle

# Initializing Board
# Dorost Kardane Board
def initialiseBoard(n):
    board = []
    board = [[0 for i in range(n)] for j in range(n)]
    half = int(n / 2)
    board[half - 1][half - 1] = 1
    board[half - 1][half] = -1
    board[half][half - 1] = -1
    board[half][half] = 1
    return board

# Making GUI Playing Board And User Interface With Turtle
# Dorost Kardane Mohit Bazi Va neveshtar haye marboot be mohit karbari
def drawBoard(boardSize, t):
    t.hideturtle()
    t.speed(0)
    t.penup()
    t.right(90)
    t.forward(350)
    t.left(90)
    t.forward(350)
    t.left(90)
    t.pendown()
    t.forward(700)
    t.left(90)
    for coln in range(boardSize):
        t.forward(700 / boardSize)
        t.left(90)
        t.forward(700)
        t.backward(700)
        t.right(90)

    t.left(90)

    for row in range(boardSize):
        t.forward(700 / boardSize)
        t.left(90)
        t.forward(700)
        t.backward(700)
        t.right(90)

    t.penup()

    for row in range(boardSize):
        t.pencolor("black")
        t.goto(-370, (350 - (row) * 700 / boardSize - 700 / boardSize / 3 * 2))
        t.write(str(row + 1), False, align='center', font=("Arial", 12, "normal"))

    for coln in range(boardSize):
        t.pencolor("red")
        t.goto((-350 + coln * 700 / boardSize + 700 / boardSize / 2), 360)
        t.write(chr(coln + 65), False, align='center', font=("Arial", 12, "normal"))


# Adding taws to the playing board
# Ezafe Kardane Mohre ha
def updateScreen(b):
    boardSize = len(b)
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    t.shapesize(700 / boardSize / 25)
    t.pencolor("black")
    t.shape("circle")
    t.penup()
    for row in range(boardSize):
        for coln in range(boardSize):
            if (b[row][coln] > 0):
                t.goto(700 / boardSize * coln - 350 + 700 / boardSize / 2,
                       700 / boardSize * row - 350 + 700 / boardSize / 2)
                t.fillcolor("black")
                t.stamp()
            if (b[row][coln] < 0):
                t.goto(700 / boardSize * coln - 350 + 700 / boardSize / 2,
                       700 / boardSize * row - 350 + 700 / boardSize / 2)
                t.fillcolor("red")
                t.stamp()
    return


def move(b, m, p):
    r = m[0]
    c = m[1]
    if (len(m[2]) == 0):
        return
    else:
        for move in m[2]:
            newR = r + move[0]
            newC = c + move[1]
            while (b[newR][newC] != abs(b[newR][newC]) * p):
                b[newR][newC] = (abs(b[newR][newC]) + 1) * p
                newR = newR + move[0]
                newC = newC + move[1]
        b[r][c] = p
        # placePiece(b, r, c, p)
        updateScreen(b)


def legalDirection(r, c, b, p, u, v):
    foundOpponent = False
    while (r >= 0 and r <= len(b) and c >= 0 and c <= len(b)):
        r = r + u
        c = c + v
        if (r < 0 or r >= len(b) or c < 0 or c >= len(b)):
            return False
        if (b[r][c] == 0):
            return False
        if (b[r][c] == abs(b[r][c]) * p):
            if foundOpponent:
                return True
            else:
                return False
        if (b[r][c] != abs(b[r][c]) * p):
            foundOpponent = True
    return False


def legalMove(r, c, b, p):
    legalDirections = []
    if (b[r][c] != 0):
        return legalDirections
    if (legalDirection(r, c, b, p, -1, -1)):
        legalDirections.append((-1, -1))
    if (legalDirection(r, c, b, p, -1, 0)):
        legalDirections.append((-1, 0))
    if (legalDirection(r, c, b, p, -1, 1)):
        legalDirections.append((-1, 1))
    if (legalDirection(r, c, b, p, 0, -1)):
        legalDirections.append((0, -1))
    if (legalDirection(r, c, b, p, 0, 0)):
        legalDirections.append((0, 0))
    if (legalDirection(r, c, b, p, 0, 1)):
        legalDirections.append((0, 1))
    if (legalDirection(r, c, b, p, 1, -1)):
        legalDirections.append((1, -1))
    if (legalDirection(r, c, b, p, 1, 0)):
        legalDirections.append((1, 0))
    if (legalDirection(r, c, b, p, 1, 1)):
        legalDirections.append((1, 1))
    return legalDirections


def moves(b, p):
    availableMoves = []
    for r in range(len(b)):
        for c in range(len(b)):
            legal = legalMove(r, c, b, p)
            if legal != []:
                availableMoves.append((r, c, legal))
    return availableMoves


def scoreBoard(b):
    blackScore = 0
    redScore = 0
    for r in range(len(b)):
        for c in range(len(b)):
            if (b[r][c] > 0):
                if b[r][c] > 0:
                    blackScore = blackScore + b[r][c]
            if (b[r][c] < 0):
                if b[r][c] < 0:
                    redScore = redScore - b[r][c]
    return (blackScore, redScore)


def checkMoveScore(b, m, p):  # Goes through all possible moves and finds the one with the highest score. The computer will choose this one.
    moveScore = 1
    r = m[0]
    c = m[1]
    if (len(m[2]) == 0):
        return 0
    else:
        for move in m[2]:
            newR = r + move[0]
            newC = c + move[1]
            while (b[newR][newC] != abs(b[newR][newC]) * p):
                moveScore = moveScore + abs(b[newR][newC])
                newR = newR + move[0]
                newC = newC + move[1]
    return moveScore


def selectMove(b, availableMoves, p):
    bestMoveScore = 0
    bestMoveIndex = -1
    currentMoveIndex = 0
    for availableMove in availableMoves:
        currentMoveScore = checkMoveScore(b, availableMove, p)
        if (bestMoveScore < currentMoveScore):
            bestMoveIndex = currentMoveIndex
            bestMoveScore = currentMoveScore
        currentMoveIndex = currentMoveIndex + 1
    return availableMoves[bestMoveIndex]


def main():
    playing = True
    while playing:
        board = []
        while (board == []):
            try:
                screen = turtle.Screen()
                screen.clear()
                board = initialiseBoard(8)
            except:
                print("Enter a valid number.")
                pass

        t = turtle.Turtle()
        t.hideturtle()
        turtleText = turtle.Turtle()
        turtleText.hideturtle()
        turtleText.penup()
        turtleText.speed(0)
        turtle.title("Othello")
        turtle.setup(800, 800)
        screen.bgcolor("white")
        drawBoard(8, t)
        updateScreen(board)
        playerTurn = 1
        gameOver = False
        blackCanMove = True
        redCanMove = True
        while (not gameOver):
            if playerTurn == -1:
                print("Player Red's turn.")
            else:
                print("Player black's turn.")
            scores = scoreBoard(board)
            turtleText.clear()
            turtleText.pencolor("black")
            turtleText.goto(-300, -380)
            turtleText.write("Black: " + str(scores[0]), False, align='center', font=("Arial", 12, "bold"))
            turtleText.pencolor("Red")
            turtleText.goto(300, -380)
            turtleText.write("Red: " + str(scores[1]), False, align='center', font=("Arial", 12, "bold"))
            validMove = False

            if (not blackCanMove and not redCanMove):
                print("GAME OVER!")
                if scores[0] > scores[1]:
                    print("Black wins!")
                else:
                    print("Red wins!")
                gameOver = True

            while (not validMove):
                inRange = False
                while (not inRange):
                    r = -1
                    try:
                        r = 8 - int(input("Row of new piece: "))
                    except:
                        print("Enter a valid number in range.")
                        pass
                    if (r >= 0 and r < 8):
                        inRange = True
                    else:
                        print("Enter a valid number in range.")
                inRange = False
                while (not inRange):
                    c = input("Column of new piece: ")
                    c = c.upper()
                    try:
                        c = ord(c) - ord('A')
                        if (c >= 0 and c < 8):
                            inRange = True
                        else:
                            print("Enter a valid letter in range.")
                    except:
                        print("Enter a valid letter in range.")
                        pass
                availableMoves = [r, c, legalMove(r, c, board, playerTurn)]
                if (availableMoves[2] != []):
                    validMove = True
                    move(board, availableMoves, playerTurn)
                else:
                    print("Invalid move.")
            if playerTurn == -1:
                playerTurn = 1
            else:
                playerTurn = -1
        playAgain = -1
        while (playAgain < 1 or playAgain > 2):
            try:
                print("Play again?")
                print("1. yes")
                print("2. no")
                playAgain = int(input(""))
                if playAgain == 2:
                    playing = False
            except:
                pass
    return


main()
