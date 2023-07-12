import pygame
from tkinter import messagebox

MAX_VAL = 10e9
MIN_VAL = -10e9
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0 , 0)

EMPTY = '.'

lastMovePlayed = (-1, -1)
numberOfMovesOnBoard = 0


def check_beside(i, j):
    # check if the square is empty and if it is a valid square
    if (j == 0 or j == 7 or(j-1 >= 0 and board[i][j-1] !=EMPTY) or (j+1 <=7 and board[i][j+1] != EMPTY)):
        return True
    return False



# here we will make an 8x8 grid of squares (like a chess board)
# each square will be 100x100 pixels
# we will use a 2D array to store the board of the board

board = [[EMPTY for i in range(8)] for j in range(8)]

# build the ui for the board
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Magnetic Cave')

# the empty squares are just white squares
# the squares with a piece on them are also white squares, but with a circle drawn on them (black or red)

# the board is 800x800 pixels
# each square is 100x100 pixels
# the top left square is (0, 0)


def draw_board():
    # draw the board
    for i in range(8):
        for j in range(8):
            # draw the square
            pygame.draw.rect(screen, WHITE, (i * 100, j * 100, 100, 100), 0)

            # draw the piece (if there is one)
            if board[i][j] != EMPTY:
                pygame.draw.circle(screen, BLACK, (i * 100 + 50, j * 100 + 50), 40, 0)

    # draw the grid
    for i in range(9):
        pygame.draw.line(screen, BLACK, (i * 100, 0), (i * 100, 800), 3)
        pygame.draw.line(screen, BLACK, (0, i * 100), (800, i * 100), 3)


def show_game_over_dialog(message):
    # Show a message box with the game over message and an exit button
    messagebox.showinfo(message=message, title='Game Over')
    pygame.quit()
    quit()

# will use n to check if there are n consecutive pieces of the same color in a row column or diagonal, n = 5 for win condition and n = 4 for heuristic function to evaluate the goodness of a board
def check_win(turn):

    global lastMovePlayed
    # not quite working because it is not checking the whole line (row, column or diagonal) but only the part that is on the right/left of the last move played
    # Fix: go to the tail of the line and check if there are 5 pieces of the same color in a row, column or diagonal (quite easy to implement)

    # try to extend lastMovePlayed in all directions and check if there are 5 pieces of the same color in a row, column or diagonal
    # if there are, return True, otherwise return False

    i, j = lastMovePlayed

    count = 1

    # try to extend to left in the same row
    while count < 5 and j - 1 >= 0 and board[i][j - 1] == turn:
        count += 1
        j -= 1
    
    if count == 5:
        return True

    # try to extend to right in the same row
    j = lastMovePlayed[1]
    while count < 5 and j + 1 <= 7 and board[i][j + 1] == turn:
        count += 1
        j += 1
    
    if count == 5:
        return True
    
    count = 1

    # try to extend to top in the same column
    j = lastMovePlayed[1]
    while count < 5 and i - 1 >= 0 and board[i - 1][j] == turn:
        count += 1
        i -= 1
    
    if count == 5:
        return True

    # try to extend to bottom in the same column
    i = lastMovePlayed[0]
    while count < 5 and i + 1 <= 7 and board[i + 1][j] == turn:
        count += 1
        i += 1
    
    if count == 5:
        return True
    
    count = 1

    # try to extend to top left in the same diagonal
    i = lastMovePlayed[0]
    j = lastMovePlayed[1]
    while count < 5 and  i - 1 >= 0 and j - 1 >= 0 and board[i - 1][j - 1] == turn:
        count += 1
        i -= 1
        j -= 1
    
    if count == 5:
        return True
    
    # try to extend to bottom right in the same diagonal
    i = lastMovePlayed[0]
    j = lastMovePlayed[1]
    while count < 5 and  i + 1 <= 7 and j + 1 <= 7 and board[i + 1][j + 1] == turn:
        count += 1
        i += 1
        j += 1
    
    if count == 5:
        return True

    count = 1

    # try to extend to top right in the same diagonal
    i = lastMovePlayed[0]
    j = lastMovePlayed[1]
    while count < 5 and  i - 1 >= 0 and j + 1 <= 7 and board[i - 1][j + 1] == turn:
        count += 1
        i -= 1
        j += 1
    
    if count == 5:
        return True
    
    # try to extend to bottom left in the same diagonal
    i = lastMovePlayed[0]
    j = lastMovePlayed[1]

    while count < 5 and  i + 1 <= 7 and j - 1 >= 0 and board[i + 1][j - 1] == turn:
        count += 1
        i += 1
        j -= 1
    
    if count == 5:
        return True
    
    return False
    

def check_board(turn):
    
    if numberOfMovesOnBoard == 64:
        print('Draw!')
        # show a message box saying that the game is a draw and exit button to exit the game
        show_game_over_dialog('Draw!')
        exit()
    # check if any row, column or diagonal has 5 pieces of the same color 
    # in a row
    if check_win(turn):
        print('Player ' + str(turn + 1) + ' wins!')
        # show a message box saying that the game is a draw and exit button to exit the game
        show_game_over_dialog('Player ' + str(turn + 1) + ' wins!')
        exit()
    


# draw the initial board
# the game has 3 modes, two player, player vs ai, and ai vs player
draw_board()

mode = input('Enter the mode of the game (0 for two player, 1 for player vs ai, 2 for ai vs player): ')
mode = int(mode)
turn = 0 # 0 is black, 1 is red

if mode == 1 or mode == 2:
    depth = input('Enter the depth of the ai: ')
    depth = int(depth)


def get_all_5_length_columns(board):
    columns = []

    for col in range(8):
        for row in range(4):
            column = [board[row + i][col] for i in range(5)]
            columns.append(column)

    return columns



def get_all_5_length_neg_diagonals(board):

    diagonals = []

    # positive diagonals
    for i in range(4):
        for j in range(4):
            diagonal = [board[i + k][j + k] for k in range(5)]
            diagonals.append(diagonal)

    return diagonals

def get_all_5_length_pos_diagonals(board):
    
        diagonals = []
    
        # positive diagonals
        for i in range(4):
            for j in range(4):
                diagonal = [board[i + k][7 - j - k] for k in range(5)]
                diagonals.append(diagonal)
    
        return diagonals


# give center moves and first and last column a small bias
extra_points = [[1, 0, 0, 0, 0, 0, 0, 1], 
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 0, 0, 0, 0, 0, 0, 1], 
                [1, 0, 0, 0, 0, 0, 0, 1]]


def eval_func(turn):


    # give a small bias towards the center


    # like 1 point for center moves 

    score = 0

    # add of the pieces location to the score

    for i in range(8):
        for j in range(8):
            if board[i][j] == turn:
                score += extra_points[i][j]/3


    for i in range(8):
        for j in range(4):
            row = board[i][j:j+5]

            if row.count(turn) == 5:
                score += 150
            elif row.count(turn) == 4 and row.count(EMPTY) == 1:
                score += 8
            elif row.count(turn) == 3 and row.count(EMPTY) == 2:
                score += 3
            
            elif row.count(1 - turn) == 4 and row.count(EMPTY) == 1:
                score -= 130
            elif row.count(1 - turn) == 3 and row.count(EMPTY) == 2:
                score -= 2
            

    for column in get_all_5_length_columns(board):
        if column.count(turn) == 5:
            score += 150
        elif column.count(turn) == 4 and column.count(EMPTY) == 1:
            score += 8
        elif column.count(turn) == 3 and column.count(EMPTY) == 2:
            score += 3
        
        elif column.count(1 - turn) == 4 and column.count(EMPTY) == 1:
            score -= 130
        elif column.count(1 - turn) == 3 and column.count(EMPTY) == 2:
            score -= 2

    for diagonal in get_all_5_length_neg_diagonals(board):
        if diagonal.count(turn) == 5:
            score += 150
        elif diagonal.count(turn) == 4 and diagonal.count(EMPTY) == 1:
            score += 8
        elif diagonal.count(turn) == 3 and diagonal.count(EMPTY) == 2:
            score += 3
        
        elif diagonal.count(1 - turn) == 4 and diagonal.count(EMPTY) == 1:
            score -= 130
        elif diagonal.count(1 - turn) == 3 and diagonal.count(EMPTY) == 2:
            score -= 2
    
    for diagonal in get_all_5_length_pos_diagonals(board):
        if diagonal.count(turn) == 5:
            score += 150
        elif diagonal.count(turn) == 4 and diagonal.count(EMPTY) == 1:
            score += 8
        elif diagonal.count(turn) == 3 and diagonal.count(EMPTY) == 2:
            score += 3
        
        elif diagonal.count(1 - turn) == 4 and diagonal.count(EMPTY) == 1:
            score -= 130
        elif diagonal.count(1 - turn) == 3 and diagonal.count(EMPTY) == 2:
            score -= 2
    

    return score



def minimax(depth, alpha, beta, maximizingPlayer, turn, whoIsMaximizing):

    global numberOfMovesOnBoard
    global lastMovePlayed

    # check if the game is over
    

    #base cases
    if depth == 0:

        if check_win(whoIsMaximizing):
            return (None, MAX_VAL)

        if numberOfMovesOnBoard == 64:
            return (None, 0)

        return (None, eval_func(whoIsMaximizing))



    

    valid_moves = []
    for i in range(8):
        for j in range(8):
            if board[i][j] == EMPTY and (j == 0 or j == 7 or(j-1 >= 0 and board[i][j-1] != EMPTY) or (j+1 <=7 and board[i][j+1] != EMPTY)):
                valid_moves.append((i, j))


    if maximizingPlayer:
        maxEval = MIN_VAL
        # random move from the valid moves for bestMove
        bestMove = valid_moves[0]

        for move in valid_moves:
            i, j = move
            board[i][j] = turn
            numberOfMovesOnBoard += 1
            temp = lastMovePlayed
            lastMovePlayed = (i, j)
            eval = minimax(depth - 1, alpha, beta, False,1-turn, whoIsMaximizing)[1]
            board[i][j] = EMPTY
            numberOfMovesOnBoard -= 1
            lastMovePlayed = temp
            if eval > maxEval:
                maxEval = eval
                bestMove = move

            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        return bestMove, maxEval

    else:
        minEval = MAX_VAL
        bestMove = valid_moves[0]

        for move in valid_moves:
            i, j = move
            board[i][j] = turn
            numberOfMovesOnBoard += 1
            temp = lastMovePlayed
            lastMovePlayed = (i, j)
            eval = minimax(depth - 1, alpha, beta, True, 1-turn, whoIsMaximizing)[1]
            board[i][j] = EMPTY
            numberOfMovesOnBoard -= 1
            lastMovePlayed = temp
            if eval < minEval:
                minEval = eval
                bestMove = move
            
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return bestMove, minEval        


# if the mode is 2, the ai will make the first move but we have to let him play the move before we enter the game loop so that the user can play his move
# and the ai can play his move after that and so on

if mode == 2:

    board[3][0] = 0
    numberOfMovesOnBoard += 1
    lastMovePlayed = (3, 0)
    pygame.draw.circle(screen, BLACK, (0 * 100 + 50, 3 * 100 + 50), 40, 0)
    pygame.display.update()
    turn =  1 - turn

AI = 1 if mode == 1 else 0


# keep the window open until the user closes it
running = True
while running:
    # check if the user has closed the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        else: # check if user clicked on a valid square
            if (mode == 0 or (mode == 1 and turn == 0) or (mode == 2 and turn == 1)) and event.type == pygame.MOUSEBUTTONDOWN:
                # here we will check if the user clicked on a valid square
                # a valid square is an empty square that is either first or last column, or next to a piece of any color

                # get the position of the mouse click
                pos = pygame.mouse.get_pos()

                # check if the click was on a valid square
                j = pos[0] // 100
                i = pos[1] // 100

                print(i, j)

                # check if the square is empty and if it is a valid square
                if board[i][j] == EMPTY and check_beside(i, j):
                    # check turn (0 is black, 1 is red)
                    if turn == 0:
                        board[i][j] = turn
                        lastMovePlayed = (i, j)
                        numberOfMovesOnBoard += 1
                        # update the display to show the new board
                        # draw the cirlce on the square
                        pygame.draw.circle(screen, BLACK, (j * 100 + 50, i * 100 + 50), 40, 0)
                        pygame.display.update()

                        if numberOfMovesOnBoard > 8:
                            check_board(turn)

                        turn = 1 - turn
                        

                        if mode == 1:
                            
                            bestMove = minimax(depth, MIN_VAL, MAX_VAL, True, turn, AI)[0]

                            board[bestMove[0]][bestMove[1]] = turn
                            lastMovePlayed = (bestMove[0], bestMove[1])
                            numberOfMovesOnBoard += 1
                            pygame.draw.circle(screen, RED, (bestMove[1] * 100 + 50, bestMove[0] * 100 + 50), 40, 0)
                            pygame.display.update()


                            if numberOfMovesOnBoard > 8:
                                check_board(turn)
                            turn =  1 - turn



                    else:

                        board[i][j] = turn
                        lastMovePlayed = (i, j)
                        numberOfMovesOnBoard += 1
                        # update the display to show the new board
                        # draw the cirlce on the square
                        pygame.draw.circle(screen, RED, (j * 100 + 50, i * 100 + 50), 40, 0)
                        pygame.display.update()


                        if numberOfMovesOnBoard > 8:
                            check_board(turn)
                        turn = 1 - turn


                        if mode == 2:

                            bestMove = minimax(depth, MIN_VAL, MAX_VAL, True, turn , AI)[0]
                
                            board[bestMove[0]][bestMove[1]] = 0
                            lastMovePlayed = (bestMove[0], bestMove[1])
                            numberOfMovesOnBoard += 1
                            pygame.draw.circle(screen, BLACK, (bestMove[1] * 100 + 50, bestMove[0] * 100 + 50), 40, 0)
                            pygame.display.update()

                            if numberOfMovesOnBoard > 8:
                                check_board(turn)
                            turn = 1 - turn
    
    # update the display
    pygame.display.update()

