#  Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions
import heapq


class PacmanAgent(Agent):

    globSeq = []
    globState = None

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
        if self.globSeq == []:
            self.globSeq = self.graphSearch(state)
            if not(self.globSeq):
                return Directions.STOP
        return self.globSeq.pop(0)

    def graphSearch(self, state):

        # Initialisation
        # --------------

        # node(cost,[sequence_of_actions,state,cost_without_heuristic])
        node = (0, [[], state, 0])
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
            # We add the node to the explored set
            position = node[1][1].getPacmanPosition()
            food = node[1][1].getFood()
            if (position, food) not in visited:
                visited.append((position, food))
                # If not, we generate successors
                for successors in node[1][1].generatePacmanSuccessors():
                    seq = node[1][0] + [successors[1]]
                    g = self.cost(successors[0], node)
                    h = self.heuristic(successors[0], food.asList())
                    newNode = (g+h, [seq, successors[0], g])
                    heapq.heappush(fringe, newNode)
        return False

    def cost(self, suc, curNode):
        # cost : +1 if our score decrease
        if suc.getScore() < curNode[1][1].getScore():
            g = curNode[1][2]+1
        else:
            g = curNode[1][2]
        return g

    def heuristic(self, suc, foodList):
        # heuristic max_i{dist(Pacman,food_i)}
        h = 0
        if len(foodList) is not 0:
            position = suc.getPacmanPosition()
            x = position[0]-foodList[0][0]
            y = position[1]-foodList[0][1]
            h = abs(x)+abs(y)
            for i in range(1, len(foodList)):
                    x = position[0]-foodList[i][0]
                    y = position[1]-foodList[i][1]
                    dist = abs(x)+abs(y)
                    if h < dist:
                        h = dist
        return h
