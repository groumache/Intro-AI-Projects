# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions, GhostRules
import numpy as np
from pacman_module import util


class BeliefStateAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        """
            Variables to use in 'updateAndFetBeliefStates' method.
            Initialization occurs in 'get_action' method.
        """
        # Current list of belief states over ghost positions
        self.beliefGhostStates = None
        # Grid of walls (assigned with 'state.getWalls()' method)
        self.walls = None
        # Uniform distribution size parameter 'w'
        # for sensor noise (see instructions)
        self.w = self.args.w
        # Probability for 'leftturn' ghost to take 'EAST' action
        # when 'EAST' is legal (see instructions)
        self.p = self.args.p

    def updateAndGetBeliefStates(self, evidences):
        """
        Given a list of (noised) distances from pacman to ghosts,
        returns a list of belief states about ghosts positions

        Arguments:
        ----------
        - `evidences`: list of (noised) ghost positions at state x_{t}
          where 't' is the current time step

        Return:
        -------
        - A list of Z belief states at state x_{t} about ghost positions
          as N*M numpy matrices of probabilities
          where N and M are respectively width and height
          of the maze layout and Z is the number of ghosts.

        N.B. : [0,0] is the bottom left corner of the maze
        """

        beliefStates = self.beliefGhostStates
        # XXX: Your code here
        f = beliefStates[-1]

        Tt = np.zeros((N, M, N, M))
        O = np.zeros((N, M, N, M))
        walls = self.walls
        p = self.args.p
        w = self.args.w

        for i in N:
            for j in M:
                if i-w <= evidences[-1][0] <= i + w and j-w <= evidences[-1][1] <= j+w:
                     
        for k in range(0,N*M):
            x_t_1 = int(k/M)
            y_t_1 = k%M
            if y_t_1 < M-1:
                north = not(walls[x_t_1][y_t_1 + 1])
            else:
                north = False
            if y_t_1 > 0:
                south = not(walls[x_t_1][y_t_1 - 1])
            else:
                south = False
            if x_t_1 < N-1:
                east = not(walls[x_t_1 + 1][y_t_1])
            else:
                east = False
            if x_t_1 > 0:
                west = not(walls[x_t_1 - 1][y_t_1])
            else:
                west = False
            possibleMove = north + south + west + east
            if east:
                Tt[k+N][k] = p + (1-p)/possibleMove
                if south:
                    Tt[k-1][k] = (1-p)/possibleMove
                if north:
                    Tt[k+1][k] = (1-p)/possibleMove
                if west:
                    Tt[k-N][k] = (1-p)/possibleMove
            else:
                if south:
                    Tt[k-1][k] = 1/possibleMove
                if north:
                    Tt[k+1][k] = 1/possibleMove
                if west:
                    Tt[k-N][k] = 1/possibleMove

            if x_t_1 - w <= evidences[-1][0] <= x_t_1 + w and y_t_1 - w <= evidences[-1][1] <= x_t_1 - w:
                O[k][k] = 1/(4*w*(1+w)+1)

        bS = self.normalize(O @ Tt @ f)
        beliefStates = [bS.reshape(N,M)]

        # XXX: End of your code
        self.beliefGhostStates = beliefStates
        return beliefStates

    def _computeNoisyPositions(self, state):
        """
            Compute a noisy position from true ghosts positions.
            XXX: DO NOT MODIFY THAT FUNCTION !!!
            Doing so will result in a 0 grade.
        """
        positions = state.getGhostPositions()
        w = self.args.w
        w2 = 2*w+1
        div = float(w2 * w2)
        new_positions = []
        for p in positions:
            (x, y) = p
            dist = util.Counter()
            for i in range(x - w, x + w + 1):
                for j in range(y - w, y + w + 1):
                    dist[(i, j)] = 1.0 / div
            dist.normalize()
            new_positions.append(util.chooseFromDistribution(dist))
        return new_positions

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

        """
           XXX: DO NOT MODIFY THAT FUNCTION !!!
                Doing so will result in a 0 grade.
        """

        # XXX : You shouldn't care on what is going on below.
        # Variables are specified in constructor.
        if self.beliefGhostStates is None:
            self.beliefGhostStates = state.getGhostBeliefStates()
        if self.walls is None:
            self.walls = state.getWalls()
        return self.updateAndGetBeliefStates(
            self._computeNoisyPositions(state))
