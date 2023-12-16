#Please do not add any imports
#This particularly includes numpy!
import math

############################## PROBLEM 1 ######################################

#This function should take a matrix with your payoffs for the game and your
#opponent's current strategy and compute your expected utility for each action.
#This will be useful in implementing the learning dynamics
def expectedValues(game,opponentStrategy):
    myResponse = []
    for i in game:
        ll = 0
        for j in range(len(i)):
            ll += (i[j]*opponentStrategy[j])

        myResponse.append(ll)
    return myResponse


############################## PROBLEM 2 ######################################

#This function should implement one iteration of best response dynamics for
#a player.  It takes that players's payoff matrix and the opponent's strategy
#and returns a best response
def argmax(a):
    return max(range(len(a)), key=lambda x : a[x])
def bestResponseDynamics(game,opponentStrategy):
    exp_vals = expectedValues(game,opponentStrategy)
    best_res = argmax(exp_vals)
    resp = [0.0 for i in range(len(exp_vals))]
    resp[best_res] = 1.0
    return resp

############################## PROBLEM 3 ######################################

#This class should implement fictitious play for one player.
class FictitiousPlay:
    #You shouldn't need to change __init__
    def __init__(self,game):
        self.history = [0.0 for i in range(len(game[0]))]
        self.game = game
        self.myres = []
        self.round = 0
    #This should perform one iteration of fictitious play
    #The argument is your opponent's more recent strategy
    #You have access to self.game (your payoffs)
    #and self.history (a list to track your opponent's history)
    #You should return the updated strategy
    def updateStrategy(self, opponentStrategy):
        for i in range(len(self.history)):
            self.history[i] += opponentStrategy[i]
        x = sum(self.history)
        temp = []
        for i in range(len(self.history)):
            temp.append(self.history[i] / x)
        res = bestResponseDynamics(self.game,temp)
        #print('--------', self.history, res)
                
        self.round += 1
        return res

############################## PROBLEM 4 ######################################

#This class should implement smoothed fictitious play for one player.
class SmoothedFictitiousPlay:
    #You shouldn't need to change __init__
    def __init__(self,game,gamma):
        self.history = [0.0 for i in range(len(game[0]))]
        self.game = game
        self.gamma = gamma

    #This should perform one iteration of smoothed fictitious play
    #The argument is your opponent's more recent strategy
    #You have access to self.game (your payoffs)
    #self.history (a list to track your opponent's history)
    #and self.gamma (see slides for what this does)
    #You should return the updated strategy
    def updateStrategy(self, opponentStrategy):
        for i in range(len(self.history)):
            self.history[i] += opponentStrategy[i]
        x = sum(self.history)
        dorito = []
        for i in range(len(self.history)):
            dorito.append(self.history[i] / x)
        res = expectedValues(self.game,dorito)
        x = 0
        for i in res:
            x += math.exp(i/self.gamma)
        ans = []
        for i in res:
            ans.append(math.exp(i/self.gamma)/x)
        return ans

############################## PROBLEM 5 ######################################

#This class should implement regret matching for one player.
class RegretMatching:
    #You shouldn't need to change __init__
    def __init__(self,game):
        self.regretSums = [0.0 for i in range(len(game[0]))]
        self.game = game
        self.strategy = [1.0/len(game) for i in range(len(game))]

    #You may optionally want to implement this helper function
    #It should convert your current regret sums to a strategy
    #My implementation of updateStrategy calls it twice
    def regretSumsToStrategy(self):
        "Your Code (Optionally) Here!"

        return [0.0]

    #This should perform one iteration of regret matching
    #The argument is your opponent's more recent strategy
    #You have access to self.game (your payoffs)
    #and self.regretSums (a list to track your regret sums)
    #You should return the updated strategy
    def updateStrategy(self, opponentStrategy):
        actions_payoff = expectedValues(self.game,opponentStrategy)
        instead = 0
        for i, j in zip(actions_payoff, self.strategy):
            instead += i*j
        for i in range(len(self.regretSums)):
            self.regretSums[i] += (actions_payoff[i] - instead)

        sumsss = 0
        for i in self.regretSums:
            sumsss += max(i, 0)
        if not sumsss:
            self.strategy = [1.0/len(self.game) for i in range(len(self.game))]
        else:
            for i in range(len(self.strategy)):
                self.strategy[i] = max(self.regretSums[i],0) / sumsss
        # print('--------', self.strategy)
        return self.strategy

############################## PROBLEM 6 ######################################

#Give priors so that Matching Pennies does not reach
#steady state with fictitious play but the empirical distribution converges    
#
#MatchingPenniesP1 = [[1,-1],[-1,1]] (defined in autograder)
#MatchingPenniesP2 = [[-1,1],[1,-1]] (defined in autograder)
MPPrior1 = [0.99, 0.01]
MPPrior2 = [0.01, 0.99]

############################## PROBLEM 7 ######################################

#Give priors so that the Shapley game's empircal distribution
#does not converge with fictitious play
#
#ShapleyGame = [[0,0,1],[1,0,0],[0,1,0]] (defined in autograder)
ShapleyPrior1 = [1.0, 0.0, 0.0]
ShapleyPrior2 = [0.0, 1.0, 0.0]

############################## PROBLEM 8 ######################################

#Give a game and priors so that best response self-play does not converge to
#the pure Nash equilibrium (0,0) but fictitious play
#reaches it as a steady state
#
P8Game1 = [[1, 0], [0, 1]]
P8Game2 = [[1, -1], [-1, 1]]
P8Prior1 = [0, 1]
P8Prior2 = [1, 0]

############################## PROBLEM 9 ######################################

#Give a game and priors so that best response self-play converges to
#the pure Nash equilibrium (0,0) but fictitious play
#does not reach it as a steady state
#
P9Game1 = [[1, 0], [0, 1]]
P9Game2 = [[1, 0], [0, 1]]
P9Prior1 = [1, 0]
P9Prior2 = [0.5, 0.5]


############################## PROBLEM 10 ######################################

#Give a 2x2 game and priors so that smoothed fictitious play converges to a
#mixed Nash equilirbium in its current strategy but regret matching does not
#(both with converge in their empirical distribution)
#
P10Game1 = [[1, -1], [-1, 1]]
P10Game2 = [[-1, 1], [1, -1]]
P10Prior1 = [0, 1]
P10Prior2 = [0, 1]

############################## PROBLEM 11 ######################################

#This class should implement optimistic regret matching for one player.
class OptimisticRegretMatching:
    #You shouldn't need to change __init__
    def __init__(self,game):
        self.regretSums = [0.0 for i in range(len(game[0]))]
        self.game = game
        self.strategy = [1.0/len(game) for i in range(len(game))]
        self.lastRegret = [0.0 for i in range(len(game[0]))]

    #You may optionally want to implement this helper function
    #It should convert your current regret sums to a strategy
    #My implementation of updateStrategy calls it twoce
    def regretSumsToStrategy(self):
        sumsss = 0
        for i in self.regretSums:
            sumsss += max(i, 0)
        if not sumsss:
            self.strategy = [1.0/len(self.game) for i in range(len(self.game))]
        else:
            for i in range(len(self.strategy)):
                self.strategy[i] = max(self.regretSums[i],0) / sumsss
        return self.strategy

    #This should perform one iteration of regret matching
    #The argument is your opponent's more recent strategy
    #You have access to self.game (your payoffs)
    #self.regretSums (a list to track your regret sums)
    #and self.lastRegret (save your regrets here before you return!) 
    #You should return the updated strategy
    def updateStrategy(self, opponentStrategy):
        # actions_payoff = expectedValues(self.game,opponentStrategy)
        # instead = 0
        # for i, j in zip(actions_payoff, self.strategy):
        #     instead += i*j
        
        # for i in range(len(self.regretSums)):
        #     self.regretSums[i] = self.regretSums[i] + 2 * (actions_payoff[i] - instead) - self.lastRegret[i]
        
        actions_payoff = expectedValues(self.game,opponentStrategy)
        instead = 0
        for i, j in zip(actions_payoff, self.strategy):
            instead += i*j
        for i in range(len(self.regretSums)):
            self.regretSums[i] += (2 * (actions_payoff[i] - instead) - self.lastRegret[i])
        return self.regretSumsToStrategy()
