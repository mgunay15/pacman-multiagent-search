# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        newFood = successorGameState.getFood()
        oldCapsule = currentGameState.getCapsules()
        newCapsule = successorGameState.getCapsules()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        currentPos = currentGameState.getPacmanPosition()
        currentNumAgents = currentGameState.getNumAgents()

        newScore = 0
        totalDistToFood1 = 0
        totalDistToFood2 = 0
        foodPoint = 0
        for foodLocations in oldFood.asList():
            dist1 = manhattanDistance(currentPos, foodLocations)
            dist2 = manhattanDistance(newPos, foodLocations)
            totalDistToFood1 += dist1
            totalDistToFood2 += dist2
            if foodLocations == newPos:
                foodPoint = 12
        if totalDistToFood1 > totalDistToFood2:
            foodPoint += 5

        totalDistToGhost1 = 0
        totalDistToGhost2 = 0
        ghostPoint = 0
        ghostList = [0]
        x = 0
        while x < currentNumAgents - 1:
            ghostList[x] = currentGameState.getGhostState(x + 1).getPosition()
            x += 1
        for ghost in ghostList:
            dist1 = manhattanDistance(currentPos, ghost)
            dist2 = manhattanDistance(newPos, ghost)
            totalDistToGhost1 += dist1
            totalDistToGhost2 += dist2
            if newPos == ghost:
                ghostPoint -= 100000
            if totalDistToGhost2 > totalDistToGhost1:
                ghostPoint += 5

        totalDistToCapsule1 = 0
        totalDistToCapsule2 = 0
        capsulePoint = 0
        for capsuleLocations in oldCapsule:
            dist1 = manhattanDistance(currentPos, capsuleLocations)
            dist2 = manhattanDistance(newPos, capsuleLocations)
            totalDistToCapsule1 += dist1
            totalDistToCapsule2 += dist2
            if dist1 == 0:
                capsulePoint = 20
        if totalDistToCapsule2 < totalDistToCapsule1:
            capsulePoint += 10

        newScore = ghostPoint + foodPoint + capsulePoint

        return newScore



def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():

        """

        def value(state, depth, agentIndex):

            if depth >= self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            if agentIndex >=state.getNumAgents()-1:
                depth += 1
                agentIndex = 0
            else :
                agentIndex += 1

            if depth >= self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            if agentIndex == 0:
                return maxValue(state, depth, agentIndex)
            else:
                return minValue(state,depth,agentIndex)

        def maxValue (state, depth, agentIndex):
            v = -9999
            possibleActList = state.getLegalActions(0)
            for action in possibleActList:
                currentValue = value(state.generateSuccessor(0, action), depth, 0)
                if currentValue > v:
                    v = currentValue
            return v

        def minValue(state, depth, agentIndex):
            v = 9999
            possibleActList = state.getLegalActions(agentIndex)

            for action in possibleActList:
                currentValue = value(state.generateSuccessor(agentIndex, action), depth, agentIndex)
                if currentValue < v:
                    v = currentValue
            return v

        nextAction = 0
        v = -9999
        possibleActList = gameState.getLegalActions(0)
        for actions in possibleActList:
            actV = value(gameState.generateSuccessor(0, actions), 0, 0)
            if actV > v:
                v = actV
                nextAction = actions
        return nextAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        def value(state, depth, agentIndex, a, b):

            if depth >= self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            if agentIndex >=state.getNumAgents()-1:
                depth += 1
                agentIndex = 0
            else :
                agentIndex += 1

            if depth >= self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            if agentIndex == 0:
                return maxValue(state, depth, agentIndex, a, b)
            else:
                return minValue(state,depth,agentIndex, a, b)

        def maxValue (state, depth, agentIndex, a, b):
            v = -99999
            possibleActList = state.getLegalActions(0)
            for action in possibleActList:
                currentValue = value(state.generateSuccessor(0, action), depth, 0, a, b)
                v = max(v, currentValue)
                if b < v:
                    return v
                if v > a :
                    a = v
            return v

        def minValue(state, depth, agentIndex, a, b):
            v = 99999
            possibleActList = state.getLegalActions(agentIndex)
            for action in possibleActList:
                currentValue = value(state.generateSuccessor(agentIndex, action), depth, agentIndex, a, b)
                v = min(v, currentValue)
                if a > v:
                    return v
                if v < b :
                    b = v
            return v

        nextAction = 0
        v = -99999
        a = -99999
        b = 99999
        possibleActList = gameState.getLegalActions(0)
        for actions in possibleActList:
            actV = value(gameState.generateSuccessor(0, actions), 0, 0, a, b)
            if actV > v:
                v = actV
                nextAction = actions
            if v > a:
                a = v
        return nextAction


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        def value(state, depth, agentIndex):

            if depth >= self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            if agentIndex >=state.getNumAgents()-1:
                depth += 1
                agentIndex = 0
            else :
                agentIndex += 1

            if depth >= self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            if agentIndex == 0:
                return maxValue(state, depth, agentIndex)
            else:
                return expectValue(state,depth,agentIndex)

        def maxValue (state, depth, agentIndex):
            v = -9999
            possibleActList = state.getLegalActions(0)
            for action in possibleActList:
                currentValue = value(state.generateSuccessor(0, action), depth, 0)
                if currentValue > v:
                    v = currentValue
            return v

        def expectValue(state, depth, agentIndex):
            possibleActList = state.getLegalActions(agentIndex)
            numOfActs = len(possibleActList)
            total=0
            for action in possibleActList:
                currentValue = value(state.generateSuccessor(agentIndex, action), depth, agentIndex)
                total+=currentValue
            v = (total*1.0)/numOfActs
            return v

        nextAction = 0
        v = -9999
        possibleActList = gameState.getLegalActions(0)
        for actions in possibleActList:
            actV = value(gameState.generateSuccessor(0, actions), 0, 0)
            if actV > v:
                v = actV
                nextAction = actions
        return nextAction


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: Other than the first question, in this question I wrote a new evaluation function which takes
      the current state and evaluate it. Since this function will be used to compare successor states, I gave different
      points for specified criteria such as distance to a ghost or total distance to the foods etc.
    """
    oldFood = currentGameState.getFood()
    oldCapsule = currentGameState.getCapsules()
    currentGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in currentGhostStates]
    currentPos = currentGameState.getPacmanPosition()
    currentNumAgents = currentGameState.getNumAgents()
    ghostList = [currentGhostStates[x].getPosition() for x in range(len(currentGhostStates))]

    newScore = 0
    totalDistToFood1 = 0
    foodPoint = 0
    for foodLocations in oldFood.asList():
        dist1 = manhattanDistance(currentPos, foodLocations)
        totalDistToFood1 += dist1
        if dist1 == 0 :
            foodPoint = 12
    if totalDistToFood1 < 500:
        foodPoint += 6


    totalDistToGhost1 = 0
    ghostPoint = 0

    if currentGameState.isLose():
        return -100000
    if currentGameState.isWin():
        return 10000


    for ghost in ghostList:
        dist1 = manhattanDistance(currentPos, ghost)
        totalDistToGhost1 += dist1
        if dist1 <= 2 :
            ghostPoint = -100000
    if totalDistToGhost1 < 10:
        ghostPoint -=5

    totalDistToCapsule1 = 0
    capsulePoint = 0
    for capsuleLocations in oldCapsule:
        dist1 = manhattanDistance(currentPos, capsuleLocations)
        totalDistToCapsule1 += dist1
        if dist1 == 0 or totalDistToCapsule1==0:
            capsulePoint = 20
    if totalDistToCapsule1 < 20:
        capsulePoint += 13


    newScore = foodPoint + capsulePoint + 0.8*ghostPoint + currentGameState.getScore()

    return newScore

# Abbreviation
better = betterEvaluationFunction

