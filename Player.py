# File: Player.py
# Sonia Nigam snk088, Amar Shah, Armaan Shah asf408
# Date:
# Group work statement: <please type the group work statement
#      given in the pdf here>
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
            print "move: {}score : {}".format(m, s)
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
            s = opp.minAb(nb, ply-1, self.score(nb))
            print "move: {}score : {}".format(m, s)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def minAb(self, state, ply, leftmost):
        #state of game
        #alpha, the value of the best alternative for MAX along the path of state
        # beta  ^ MIN
        if leftmost > self.score(state):
            ply -= 1
            self.maxAb(state, ply, leftmost)
        # else:
        #     if state.gameOver():
        #         return self.score(state)
        #     if cutoff(state, ply):
        #         return self.score(state)
        #     score = INFINITY
        #     for a,s in state.legalMoves():
        #         utility = maxAb()
        #         if score > utility:
        #             score = utility
        if state.gameOver():
            return turn.score(state)
        score = leftmost
        for m in state.legalMoves(self):
            if ply == 0:
                #print "turn.score(state) in min Value is: " + str(turn.score(state))
                return turn.score(state)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the state so that we don't ruin it
            nextBoard = deepcopy(state)
            nextBoard.makeMove(self, m)
            #using this as a cutoff
            if self.score(nextBoard) <= score:
                score = self.score(nextBoard)
                opp = Player(self.opp, self.type, self.ply)
                s = opponent.maxAb(nextBoard, ply-1, score)    
            else:
                continue # we prune
                print m
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s

        return score


    def cutoff():
        if ply == 0:
            return self.score(state)
        if len(state.legalMoves(self)) ==0:
            return self.score(state)



    def maxAb(self, state, ply, leftmost):
                #state of game
        #alpha, the value of the best alternative for MAX along the path of state
        # beta  ^ MIN
        if leftmost < self.score(state):
            ply -= 1
            self.minAb(state, ply, leftmost)
        if state.gameOver():
            return turn.score(state)
        score = leftmost
        for m in state.legalMoves(self):
            if ply == 0:
                #print "turn.score(state) in min Value is: " + str(turn.score(state))
                return turn.score(state)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the state so that we don't ruin it
            nextBoard = deepcopy(state)
            nextBoard.makeMove(self, m)

            if self.score(nextBoard) > score:
                score = self.score(nextBoard)
                opp = Player(self.opp, self.type, self.ply)
                s = opponent.maxAb(nextBoard, ply-1, score)    
            else:
                continue # we prune
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s

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
            val, move = self.alphaBetaMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            # TODO: Implement a custom player
            # You should fill this in with a call to your best move choosing
            # function.  You may use whatever search algorithm and scoring
            # algorithm you like.  Remember that your player must make
            # each move in about 10 seconds or less.
            print "Custom player not yet implemented"
            return -1
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be your netid
class MancalaPlayer(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board
        if (board.scoreCups[0]+ board.scoreCups[1]) == 0:
            return 0
        #print "Calling score in MancalaPlayer"
        elif self.num == 1:
            #print board.scoreCups
            return (float(board.scoreCups[1])/float(board.scoreCups[0]+ board.scoreCups[1]))*100
        elif self.num == 2:
            #print board.scoreCups
            return (float(board.scoreCups[1])/float(board.scoreCups[0]+ board.scoreCups[1]))*100


        #return Player.score(self, board)


