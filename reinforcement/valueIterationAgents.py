# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

MIN = -2147483648

class ValueIterationAgent(ValueEstimationAgent):
    """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
    """
    
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
         
        "*** YOUR CODE HERE ***"
        states = mdp.getStates()

        #Iterate through user-defined number of iterations
        for num in range(iterations):
            temp = util.Counter()

            #Compute Ut+1 for all states
            for state in states:
                
                if mdp.isTerminal(state):
                    self.values[state] = 0
                    continue
                
                actions = mdp.getPossibleActions(state)
                maxVal = MIN

                #iterate through trans of each action of the state and sum up values 
                for action in actions:
                    transitions = mdp.getTransitionStatesAndProbs(state, action)
                    totalSum = 0
                    
                    for transition in transitions:
                        #transition[0] = nextState, transition[1] = probability
                        reward = mdp.getReward(state, action, transition[0])
                        #value of the nextState
                        UtValue = self.values[transition[0]]
                        #using formula of value iteration from wikipedia
                        totalSum += transition[1]*(reward + discount * UtValue)
                    maxVal = max(maxVal, totalSum)
                    
                    #for some reason, self.values[state] = maxVal doesn't work.
                    temp[state] = maxVal
            
            for state in states:
                self.values[state] = temp[state]
                
                    
    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        transitions = self.mdp.getTransitionStatesAndProbs(state, action)
        sum = 0
        for transition in transitions:
            reward = self.mdp.getReward(state, action, transition[0])
            UtValue = self.values[transition[0]]
            sum += transition[1]*(reward + self.discount * UtValue)

        return sum
        
    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        maxval = MIN
        finalAction = None

        actions = self.mdp.getPossibleActions(state)

        for action in actions:
            qValue = self.getQValue(state, action)
            if maxval <= qValue:
                maxval = qValue
                finalAction = action

        return finalAction
        
    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

