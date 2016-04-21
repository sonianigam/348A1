# File: Player.py
# Sonia Nigam snk088, Amar Shah ats545, Armaan Shah asf408
# Date:
# Group work statement: <All group members were present and contributing during all work on this project.>
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.

from random import *
from decimal import *
from copy import *
from MancalaBoard import *

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4
    
    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)
    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            print "move: {} score : {}".format(m, s)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score
    
    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        #print "Alpha Beta Move not yet implemented"
        #returns the score adn the associated moved
        move = -1
        alpha = -INFINITY
        beta  = INFINITY
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board) #don't want to actually make move
            #make a new board
            nb.makeMove(self, m) #test each move
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minAb(nb, ply-1, turn, alpha, beta)
            print "move: {} score : {}".format(m, s)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
            alpha = max(score, alpha)
        #return the best score and move so far
        return score, move

    def minAb(self, state, ply, turn, alpha, beta):
        #state of game
        #alpha, the value of the best alternative for MAX along the path of state
        # beta  ^ MIN

        if state.gameOver():
            return turn.score(state)
        score = INFINITY
        opponent = Player(self.opp, self.type, self.ply)
        for m in state.legalMoves(self):
            if ply == 0:
                return turn.score(state)
            nextBoard = deepcopy(state)
            nextBoard.makeMove(self, m)    
            score = min(score, opponent.maxAb(nextBoard, ply-1, turn, alpha, beta))
            if score <= alpha:
                # print "pruning"
                return score
            else:
                beta = min(beta, score)
        return score

    def maxAb(self, state, ply, turn, alpha, beta):
        #state of game
        #alpha, the value of the best alternative for MAX along the path of state
        # beta  ^ MIN

        if state.gameOver():
            return turn.score(state)
        score = -INFINITY
        opponent = Player(self.opp, self.type, self.ply)
        for m in state.legalMoves(self):
            if ply == 0:
                return turn.score(state)
            nextBoard = deepcopy(state)
            nextBoard.makeMove(self, m)   
            score = max(score, opponent.minAb(nextBoard, ply-1, turn, alpha, beta))
            if score >= beta:
                # print "pruning"
                return score
            else:
                alpha = max(alpha, score)
        return score

    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print board.scoreCups
            print "score is"
            print self.score(board)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.minimaxMove(board, self.ply)
            print "minimax would choose move", move, "with value", val
            val, move = self.alphaBetaMove(board, self.ply)
            print "ab pruning chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            # TODO: Implement a custom player
            # You should fill this in with a call to your best move choosing
            # function.  You may use whatever search algorithm and scoring
            # algorithm you like.  Remember that your player must make
            # each move in about 10 seconds or less.
            
            val, move = self.alphaBetaMove(board, 7)
            print "ab pruning chose move", move, " with value", val
            return move
        
        
        else:
            print "Unknown player type"
            return -1




# Note, you should change the name of this player to be your netid
class snk088(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def score(self, board):
        """ Evaluate the Mancala board for this player. the way we are doing our heuristic is by breaking
        everything down into three categories. The first category is how many marbles you have on your side
        as a percentage of how many marbles your opponent has. 
        The next category is how marbles you have in your mancala compared to how many your opponent has
        the lastly is how many cups of yours are empty and the opposing player has marbles in them. Then we place
        weights on all three to calculate a new heuristic.
        Furthermore, we also have base cases to ensure that we dont obtain a divide by 0 error but if that does happen
        we still use two out of the other three categories to calculate our heuristic. """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board
        
        player1marbles = sum(board.P1Cups)
        player2marbles = sum(board.P2Cups)
        total_marbles = player1marbles + player2marbles
        empty = 0


        if (board.scoreCups[0]+ board.scoreCups[1]) == 0:
            return 0
        elif self.num == 1:
            
            for x in range(0,6):
                if board.P1Cups[x] == 0 and board.P2Cups[5-x] != 0:
                    empty += 1
        
            empty_portion = (float(empty)/5.0) * 100

            if board.scoreCups[0]+ board.scoreCups[1] != 0:
                endcups_portion = (float(board.scoreCups[0])/float(board.scoreCups[0]+ board.scoreCups[1]))*100
            else:
                endcups_portion = 0
            
            if total_marbles != 0:
                boardcups_portion = (float(player1marbles)/float(total_marbles))*100
            else:
                boardcups_portion = 0
            total_score = endcups_portion * .5 + boardcups_portion * .25 + empty_portion * .25
            return total_score
        
        elif self.num == 2:

            for x in range(0,6):
                if board.P2Cups[x] == 0 and board.P1Cups[5-x] != 0:
                    empty += 1

            empty_portion = ((float(empty))/5.0) * 100

            if board.scoreCups[0]+ board.scoreCups[1] != 0:
                endcups_portion = (float(board.scoreCups[1])/float(board.scoreCups[0]+ board.scoreCups[1]))*100
            else:
                endcups_portion = 0

            if total_marbles != 0:
                boardcups_portion = (float(player2marbles)/float(total_marbles))*100  
            else:
                boardcups_portion = 0          
            total_score = endcups_portion * .5 + boardcups_portion * .25 + empty_portion * .25
            #print board
            #print empty_portion, endcups_portion, boardcups_portion
            return total_score
        #return Player.score(self, board)
