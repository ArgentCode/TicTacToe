"""
Code largely based off of https://github.com/Cledersonbc/tic-tac-toe-minimax
"""

import pygame
import random
from pygame.constants import MOUSEBUTTONDOWN
from math import inf as infinity
import sys
import time
WIDTH = HEIGHT = 512
DIMENSION = 3 #dimension is 3x3
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 5
IMAGES = {}
randomOpponent = False
minMaxOpponent = True
HUMAN = -1
COMP = +1


# Single load of images is essential
def loadImages():
    pieces = [-1, 1]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + str(piece) + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = GameState()
    gameOver = False
    loadImages()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if randomOpponent and not gs.XToMove:
                rand = random.randint(0, len(gs.validMoves)-1)
                row, col = gs.validMoves[rand][0], gs.validMoves[rand][1]
                gameOver = gs.makeMove(row, col)
            if minMaxOpponent and not gs.XToMove:
                row, col = ai_turn(gs)
                gameOver = gs.makeMove(row, col)
            if e.type == MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                gameOver = gs.makeMove(row, col)
        drawGameState(screen, gs.board)
        clock.tick(MAX_FPS)
        pygame.display.flip()
        if gameOver:
            time.sleep(3)
            sys.exit()


def getValidMoves(board):
    validMoves = []
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            if board[r][c] == 0:
                validMoves.append((r,c))
    return validMoves


# Responsible for all graphics within current gamestate
def drawGameState(screen, board):
    drawBoard(screen) #draw squares on a board
    drawPieces(screen, board) #draw peices on top of those squares
    

def drawBoard(screen):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != 0: #if not empty square
                screen.blit(IMAGES[piece], pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


class GameState():
    def __init__(self):
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.XToMove = True
        self.validMoves = getValidMoves(self.board)


    def makeMove(self, row, col):
        if self.board[row][col] == 0:
            temp = (row, col)
            self.validMoves.remove(temp)
            self.board[row][col] = -1 if self.XToMove else 1
            self.XToMove = not self.XToMove
            gameOver = self.checkWin()
            return gameOver


    def checkWin(self):
        winner = "O" if self.XToMove else "X"
        win = False
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] != 0:
                win =True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] != 0:
                win =True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[1][1] != 0:
                win =True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[1][1] != 0:
                win =True
        if len(self.validMoves) == 0:
            print("Stalemate!")
            return True
        if win:
            print("winner is: " + winner)
            return True
        return False


# Min Max Algorithm Attempt

def minimax(board, depth, player):
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]
    gameCondition = gameOver(board)
    if depth == 0 or gameCondition[1]:
        score = gameCondition[0]
        return [-1, -1, score]

    for cell in getValidMoves(board):
        x, y = cell[0], cell[1]
        board[x][y] = player
        score = minimax(board, depth - 1, -player)
        board[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


def ai_turn(gs):
    depth = len(getValidMoves(gs.board))
    if depth == 0 or gameOver(gs.board)[1]:
        return

    move = minimax(gs.board, depth, COMP)
    x, y = move[0], move[1]

    return x, y


def gameOver(board):
    output = [0, False] #0 is no winner, -1 is human, +1 is computer, True if game is over
    winner = -5
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != 0:
            winner = board[i][0]
            output[1] =True
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != 0:
            winner = board[0][i]
            output[1] =True
    if board[0][0] == board[1][1] == board[2][2] and board[1][1] != 0:
            winner = board[1][1]
            output[1] =True
    if board[0][2] == board[1][1] == board[2][0] and board[1][1] != 0:
            winner = board[1][1]
            output[1] =True
    if len(getValidMoves(board)) == 0:
        return (0, True) # no winner, game is over
    if winner == -1:
        output[0] = -1
    if winner == 1:
        output[0] = +1
    return output


if __name__ == "__main__":
    main()
