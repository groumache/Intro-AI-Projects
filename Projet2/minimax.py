# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions
from math import inf


class PacmanAgent(Agent):

    visited = {}

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
        self.visited = {}
        utility = -inf
        move = 'STOP'

        # We choose the successor with the maximum utility
        for successor in state.generatePacmanSuccessors():
            maxPlayer = True
            score = self.minimax(successor[0], maxPlayer)
            if utility < score:
                move = successor[1]
                utility = score

        # If there's no winning state, we try to to move farther from the ghost
        if utility == -inf:
            dist = -inf
            for successor in state.generatePacmanSuccessors():
                newDist = self.distanceFromGhost(successor[0])
                if not successor[0].isLose() and newDist > dist:
                    move = successor[1]
                    dist = newDist
        return move

    def minimax(self, state, maxPlayer):
        """
        Take the current state and the current player (True if pacman)
        and return the utility of the state
        """
        # Are we in terminal state ?
        if state.isWin():
            # Utility function
            utility = state.getScore()
            return utility
        if state.isLose():
            utility = -inf
            return utility

        if maxPlayer:   # PACMAN
            visited = self.visited
            utility = -inf
            for successor in state.generatePacmanSuccessors():
                nextPosition = successor[0].getPacmanPosition()
                nextScore = successor[0].getScore()
                # We only consider relevant nodes
                if (nextPosition not in visited or
                        nextScore >= visited[nextPosition]):
                    visited[nextPosition] = nextScore
                    utility = max(utility, self.minimax(successor[0], False))
            return utility
        else:   # GHOST
            utility = inf
            for successor in state.generateGhostSuccessors(1):
                utility = min(utility, self.minimax(successor[0], True))
            return utility

    def distanceFromGhost(self, state):
        """
        Take a state as args and
        return the distance between pacman and the ghost
        """
        pacPos = state.getPacmanPosition()
        ghoPos = state.getGhostPositions()
        d = abs(pacPos[1]-ghoPos[0][1]) + abs(pacPos[0]-ghoPos[0][0])
        return d
