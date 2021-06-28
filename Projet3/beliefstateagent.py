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

        # Data of the problem
        walls = self.walls
        p = self.args.p
        w = self.args.w
        
        # Load previous distribution
        f = beliefStates[-1]
        M = len(f[0,:])
        N = len(f[:,1])

        # We reshape the distribution in order to use a matrix formalism
        f = f.reshape(N*M, 1)

        # We compute our transition matrix
        # NB : We could have computed it only once...(ie, not at each computation of a new distribution)
        Tt = np.zeros((N*M, N*M))
        O = np.zeros((N*M,N*M))
        for k in range(0, N*M):
        # We compute our transition matrix
        # NB : We could have computed it only once...(ie, not at each computation of a new distribution)
            x_t_1 = int(k/M)
            y_t_1 = k%M
            # We define that P(x_t+1|x_t = wall) = 0
            if walls[x_t_1][y_t_1]:
                pass
            
            else:
                if y_t_1 < M-2:
                    north = not(walls[x_t_1][y_t_1 + 1])
                else:
                    north = False
                if y_t_1 > 1:
                    south = not(walls[x_t_1][y_t_1 - 1])
                else:
                    south = False
                if x_t_1 < N-2:
                    east = not(walls[x_t_1 + 1][y_t_1])
                else:
                    east = False
                if x_t_1 > 1:
                    west = not(walls[x_t_1 - 1][y_t_1])
                else:
                    west = False
                possibleMove = north + south + west + east
                if east:
                    Tt[k+M][k] = p + (1-p)/possibleMove
                    if south:
                        Tt[k-1][k] = (1-p)/possibleMove
                    if north:
                        Tt[k+1][k] = (1-p)/possibleMove
                    if west:
                        Tt[k-M][k] = (1-p)/possibleMove
                else:
                    if south:
                        Tt[k-1][k] = 1/possibleMove
                    if north:
                        Tt[k+1][k] = 1/possibleMove
                    if west:
                        Tt[k-M][k] = 1/possibleMove

        # Computation of the evidence matrix
            x_t = int(k/M)
            y_t = k%M
            if x_t - w <= evidences[-1][0] <= x_t + w and y_t - w <= evidences[-1][1] <= y_t + w:
                O[k][k] = 1/(2*w+1)**2

        # Computation of the next distribution
        bS = np.zeros((N*M, 1))
        bS = O @ Tt @ f
        bS = bS / sum(bS)
        beliefStates = [bS.reshape(N,M)]

        # XXX: End of your code
        self.beliefGhostStates = beliefStates
        print(beliefStates)
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
