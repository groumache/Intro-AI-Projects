# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions
from math import inf


class PacmanAgent(Agent):

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.
        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.
        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """
        utility = -inf
        move = 'STOP'

        # We choose the successor with the maximum "utility"
        for successor in state.generatePacmanSuccessors():
            maxPlayer = True
            depth = 4   # DEPTH
            score = self.alphabeta(successor[0], -inf, +inf, maxPlayer, depth)
            if utility < score:
                move = successor[1]
                utility = score
        return move

    def alphabeta(self, state, alpha, beta, maxPlayer, depth):
        """
        Take the current state and the current player (True if pacman)
        and return the utility of the state
        """
        # Cutoff-Test : depth = 4 or terminal state
        if depth == 0:
            # Evaluation function :
            return state.getScore() - self.foodDistance(state)
        if state.isWin():
            # Evaluation function (food distance = 0):
            return state.getScore()
        if state.isLose():
            return -inf

        if maxPlayer:   # PACMAN
            utility = -inf
            for successor in state.generatePacmanSuccessors():
                utility = max(utility, self.alphabeta(successor[0], alpha,
                                                      beta, False, depth - 1))
                if utility >= beta:
                    return utility
                alpha = max(alpha, utility)
            return utility
        else:   # GHOST
            utility = inf
            for successor in state.generateGhostSuccessors(1):
                utility = min(utility, self.alphabeta(successor[0], alpha,
                                                      beta, True, depth - 1))
                if utility <= alpha:
                    return utility
                beta = min(beta, utility)
            return utility

    def foodDistance(self, state):
        '''
        Return the distance between Pacman and the closest food dot.
        '''
        position = state.getPacmanPosition()
        food = state.getFood().asList()
        distance = []
        for f in food:
            dist = abs(f[0] - position[0]) + abs(f[1] - position[1])
            distance.append(dist)
        return min(distance)
