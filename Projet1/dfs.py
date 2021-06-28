#  Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions


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

        # node = [Sequence_of_action,state]
        node = [[], initState]
        # FIFO queue
        fringe = []
        fringe.append(node)
        visited = []

        # Search a winning state
        # ----------------------

        while not(fringe is None):
            # We choose a node
            node = fringe.pop()
            # If it is a winning node
            if node[1].isWin():
                return node[0]
            # We add the node to the explored set
            position = node[1].getPacmanPosition()
            food = node[1].getFood()
            if (position, food) not in visited:
                visited.append((position, food))
                # Expansion
                for successors in node[1].generatePacmanSuccessors():
                    newNode = [node[0]+[successors[1]], successors[0]]
                    fringe.append(newNode)
        return False
