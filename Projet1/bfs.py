#  Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions
from collections import deque


class PacmanAgent(Agent):

    globSeq = []

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

    def graphSearch(self, initState):
        # Initialisation
        # --------------

        # node = [state, action]
        node = [initState, None]
        # LIFO queue
        fringe = deque()
        fringe.append(node)
        visited = []
        # To construct the path
        previousNode = dict()
        previousNode[initState] = (None, None)

        # Search a winnning state
        # -----------------------

        while not(fringe is None):
            # We choose a node
            node = fringe.popleft()
            # If it is a winning node
            if node[0].isWin():
                return self.constructPath(node[0], previousNode)
            # We verify that this node hasn't been explored yet
            curPos = node[0].getPacmanPosition()
            curFood = node[0].getFood()
            if (curPos, curFood) not in visited:
                # If not, we add them to the explored set
                visited.append((curPos, curFood))
                # We add successors that are relevant to the fringe
                for successors in node[0].generatePacmanSuccessors():
                    newNode = successors
                    fringe.append(newNode)
                    previousNode[successors[0]] = (node[0], successors[1])
        return False

    def constructPath(self, state, previousNode):
        actionList = list()

        while previousNode[state][0] is not None:
            prevState, action = previousNode[state]
            actionList.append(action)
            state = prevState

        actionList.reverse()
        return actionList
