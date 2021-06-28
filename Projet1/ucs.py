#  Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions
import heapq


class PacmanAgent(Agent):

    globSeq = []

    def __init__(self, args):
        """²
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
        if self.globSeq == []:
            self.globSeq = self.graphSearch(state)
            if not(self.globSeq):
                return Directions.STOP
        return self.globSeq.pop(0)

    # Function that return a sequence of action to execute
    def graphSearch(self, state):
        # Initialisation
        # --------------

        # node(cost,[sequence_of_actions,state])
        node = (0, [[], state])
        # creation of a priority queu to store node in the frontier
        fringe = []
        heapq.heappush(fringe, node)
        visited = []

        # Search a winning state
        # ----------------------

        while not(fringe is None):
            # We choose a node
            node = heapq.heappop(fringe)
            # Is it a wining node ?
            if node[1][1].isWin():
                return node[1][0]
            # Updating of the explored set if we haven't explored this node yet
            curPos = node[1][1].getPacmanPosition()
            curFood = node[1][1].getFood()
            if (curPos, curFood) not in visited:
                visited.append((curPos, curFood))
                # If not, we generate successors
                # We add successors that are relevant to the fringe
                for successors in node[1][1].generatePacmanSuccessors():
                    seq = node[1][0] + [successors[1]]
                    newNode = (self.cost(successors[0], node),
                               [seq, successors[0]])
                    heapq.heappush(fringe, newNode)
        return False

    def cost(self, suc, curNode):
        # cost : +1 if our score decrease
        if suc.getScore() < curNode[1][1].getScore():
            return curNode[0]+1
        else:
            return curNode[0]
