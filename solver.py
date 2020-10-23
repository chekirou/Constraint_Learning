from string import ascii_lowercase
from random import choice, sample
import numpy as np
import copy
from utils import *
from game import *


## Solver class: defnies basic features + checks for consistence

class Solver:
  def __init__(self, game):
    self.game= game
    self.Xi = [-1] * (self.game.n)
  def checkConstistence(self, proposition):
    if not all_diff(proposition): #check that every two variables are different
       #print("not different")
      return False
    if len(self.game.board) >0:# if there are previous proposed codes
      if not different_history(proposition, self.game.board): # check that the proposition is new
        #print('not different history')
        return False
      for Past_propostion, redPawns, whitePawns in self.game.board: #check the red pawns and white pawns for every past proposition
        if GoodPositions(Past_propostion, proposition) !=  redPawns : # if redPawns are good than we have to leave redPawns untouched
          #print("not goodPositions with " + str(Past_propostion))
          return False
        if misplaced(Past_propostion, proposition) != whitePawns: # if whitePawns must be moved than whitePawns must move the rest is false
          #print("not exact misplaced with " + str(Past_propostion))
          return False
    return True

  def solve(self):
    pass

"""# Engendrer et tester"""

class EngTest(Solver):
  def __init__(self, game):
    super().__init__(game)

  def solve(self):
    i =  0
    while not self.game.isSolved():
      #print("try number : " + str(i))
      self.EngTest([-1]* self.game.n)# we start with new empty line
      self.game.check() # le codeur verifie notre proposition
      #print(self.game.code, self.game.board)
      i+=1
    #print("Solved")
    return i
  def EngTest(self, guess):
    if -1 not in guess:# every variable is instantiated
      if self.checkConstistence(guess):
        #print(" solution", guess)
        self.game.board.append([guess, 0,0])# we add it to the board
        return True
      else:
        return False
    else:
      Xk = choice([ i for i in range(len(guess)) if guess[i] == -1])# random empty variable
      domaine = self.game.getVariable(Xk).getDomaine()
      for v in sample(domaine,len(domaine) ): # for every value
        new = guess.copy()
        new[Xk] = v
        if self.EngTest(new):
          return True
      return False

"""# retour arriere chronologique"""

class RAC(Solver):
  def __init__(self, game):
    super().__init__(game)

  def checkConstistence(self, proposition):
    I = proposition.count(-1)#nombre de variables vides
    l = I < self.game.n # si l'instanciation est locale ou complete
    if not all_diff(proposition, local = l): #check that every two variables are different
        #print("not different adjacent")
        return False
    if len(self.game.board) >0:# if there are previous proposed codes
      for Past_propostion, redPawns, whitePawns in self.game.board: #check the red pawns and white pawns for every past proposition
        gp = GoodPositions(Past_propostion, proposition, local =l)
        if redPawns - gp >  I or gp - redPawns > 0 : # if "redPawns" are good than we have to leave "redPawns" untouched no more no less
          #print("not goodPositions with " + str(Past_propostion))
          return False
        mis = misplaced(Past_propostion, proposition)
        if  mis - whitePawns >0 : # if whitePawns must be moved than whitePawns must move the rest is false
          #print("not exact misplaced with " + str(Past_propostion))
          return False
      if not different_history(proposition, self.game.board, local = l): # check that the proposition is new if it's complete
        #print('not different history')
        return False
    return True


  def solve(self):
    i =  0
    while not self.game.isSolved():
      #print("try number : " + str(i))
      if not self.RAC([-1]* self.game.n):# we start with new empty line

        break
      self.game.check()
      #print(self.game.code, self.game.board)
      i+=1
    #print("Solved")
    return i
  def RAC(self, guess):
    if guess.count(-1) == 0: #if all variables are instantiated
      #print(" solution", guess)
      self.game.board.append([guess, 0,0])
      return True
    else:
      Xk = choice([ i for i in range(len(guess)) if guess[i] == -1])# random empty variable
      for v in self.game.getVariable(Xk).getDomaine():# ordered
        new=  guess.copy()
        new[Xk] = v
        if self.checkConstistence(new):
          #print("test" + str(new))
          if self.RAC(new):
            return True
      return False

"""### Retour arriere chronologique avec forward checking"""

class Forward_checking(Solver):
  def __init__(self, game):
    super().__init__(game)

  def checkConstistence(self, proposition):
    I = proposition.count(-1)#nombre de variables vides
    l = I < self.game.n
    if not all_diff(proposition, local = l): #check that every two variables are different
        #print("not different adjacent")
        return False
    if len(self.game.board) >0:# if there are previous proposed codes
      for Past_propostion, redPawns, whitePawns in self.game.board: #check the red pawns and white pawns for every past proposition
        gp = GoodPositions(Past_propostion, proposition, local =l)
        if redPawns - gp >  I or gp - redPawns > 0 : # if "redPawns" are good than we have to leave "redPawns" untouched
          #print("not goodPositions with " + str(Past_propostion))
          return False
        mis = misplaced(Past_propostion, proposition)
        if  mis - whitePawns >0 :
          #print("not exact misplaced with " + str(Past_propostion))
          return False
      if not different_history(proposition, self.game.board, local = l): # check that the proposition is new if it's complete
        #print('not different history')
        return False
    return True

  def check_forward(self, x, v, variables):# supression de la valeur ajoutée
    consistant = True
    for i in range(len(variables)):
      if i != x:
        variables[i].remove_value(v)# on reduit le domaine
        if len(variables[i].getDomaine()) == 0:
          return False
    return True

  def solve(self):
    i =  0
    while not self.game.isSolved():
      #print("try number : " + str(i))
      if not self.forward_checking([-1]* self.game.n, self.game.variables):# we start with new empty line
        #print("false")
        break
      self.game.check()
      #print(self.game.code, self.game.board)
      i+=1
    #print("Solved")
    return i
  def forward_checking(self,guess, variables):
    if guess.count(-1) == 0: #list of empty variables
      self.game.board.append([guess, 0,0])
      #print(" solution", guess)
      return True
    else:
      Xk = choice([ i for i in range(len(guess)) if guess[i] == -1])# random empty variable
      for v in variables[Xk].getDomaine():
        new = copy.deepcopy(variables)
        new_guess = guess.copy()
        new_guess[Xk] = v
        #print("check", new_guess)
        if self.checkConstistence(new_guess):
          #print("consistant")
          if self.check_forward(Xk, v, new ):
            #print("essaie :" , new_guess, [i.getDomaine() for i in new] )
            if self.forward_checking(new_guess,new):
              return True
          else:
            print("false")
      return False

class Forward_checking_2(Solver):# A4
  def __init__(self, game):
    super().__init__(game)

  def checkConstistence(self, proposition):
    I = proposition.count(-1)#nombre de variables vides
    l = I < self.game.n
    #if not all_diff_2(proposition, local = l): #check that the proposition respects the rule
    #    #print("not different adjacent")
    #    return False
    if len(self.game.board) >0:# if there are previous proposed codes
      for Past_propostion, redPawns, whitePawns in self.game.board: #check the red pawns and white pawns for every past proposition
        gp = GoodPositions(Past_propostion, proposition, local =l)
        if redPawns - gp >  I or gp - redPawns > 0 : # if "redPawns" are good than we have to leave "redPawns" untouched
          #print("not goodPositions with " + str(Past_propostion))
          return False
        mis = misplaced(Past_propostion, proposition)
        if  mis - whitePawns >0 : # if whitePawns must be moved than whitePawns must move the rest is false
          #print("not exact misplaced with " + str(Past_propostion))
          return False
      if not different_history(proposition, self.game.board, local = l): # check that the proposition is new if it's complete
        #print('not different history')
        return False
    return True

  def check_forward(self, x, v, variables, guess):
    if guess.count(v) == 2:#if the max occurences has been attained
      indices = [i for i in enumerate(guess)]
      for i in range(len(variables)):
        if i not in indices:
          variables[i].remove_value(v)
          if len(variables[i].getDomaine()) == 0:
            return False
    return True

  def solve(self):
    i =  0
    while not self.game.isSolved():
      #print("try number : " + str(i))
      if not self.forward_checking([-1]* self.game.n, self.game.variables):# we start with new empty line
        print("false")
        break
      self.game.check()
      #print(self.game.code, self.game.board)
      i+=1
    #print("Solved")
    return i
  def forward_checking(self,guess, variables):
    if guess.count(-1) == 0: #list of empty variables
      self.game.board.append([guess, 0,0])
      #print(" solution", guess)
      return True
    else:
      Xk = choice([ i for i in range(len(guess)) if guess[i] == -1])# first empty variable
      for v in variables[Xk].getDomaine():
        new = copy.deepcopy(variables)
        new_guess = guess.copy()
        new_guess[Xk] = v
        #print("check", new_guess)
        if self.checkConstistence(new_guess):
          #print("consistant")
          if self.check_forward(Xk, v, new, new_guess ):
            #print("essaie :" , new_guess, [i.getDomaine() for i in new] )
            if self.forward_checking(new_guess,new):
              return True
      return False

class Forward_checking_3(Solver):
  def __init__(self, game):
    super().__init__(game)

  def checkConstistence(self, proposition):
    I = proposition.count(-1)#nombre de variables vides
    l = I < self.game.n
    if not all_diff(proposition, local = l): #check that the proposition respects the rule
        #print("not different adjacent")
        return False
    if len(self.game.board) >0:# if there are previous proposed codes
      for Past_propostion, redPawns, whitePawns in self.game.board: #check the red pawns and white pawns for every past proposition
        _,gp = GoodPositions_2(Past_propostion, proposition, local =l)
        if redPawns - gp >  I or gp - redPawns > 0 : # if "redPawns" are good than we have to leave "redPawns" untouched
          #print("not goodPositions with " + str(Past_propostion))
          return False
        _,mis = misplaced_2(Past_propostion, proposition)
        if  mis - whitePawns >0 : # if whitePawns must be moved than whitePawns must move the rest is false
          #print("not exact misplaced with " + str(Past_propostion))
          return False
      if not different_history(proposition, self.game.board, local = l): # check that the proposition is new if it's complete
        #print('not different history')
        return False
    return True

  def check_forward(self, x, v, variables, proposition):
    I = proposition.count(-1)#nombre de variables vides
    l = I < self.game.n
    if len(self.game.board) >0:
      for Past_propostion, redPawns, whitePawns in self.game.board: #check the red pawns and white pawns for every past proposition
        indexes_gp, gp = GoodPositions_2(Past_propostion, proposition, local =l)
        if redPawns == gp: # if the redpawns are atteined, no other position can replicate
          remove_values(variables, indexes_gp, [proposition[i] for i in indexes_gp], False)# on enleve les valeurs concernés
        indexes_mis ,mis = misplaced_2(Past_propostion, proposition)
        if  mis == whitePawns :
          #print("not exact misplaced with " + str(Past_propostion))
          remove_values(variables, indexes_mis, proposition, True)# on enleve les valeurs concerné
      for i in range(len(variables)):
        if i!=x and v in variables[i].getDomaine():
          variables[i].remove_value(v)
          if len(variables[i].getDomaine()) == 0:
            return False
    return True

  def solve(self):
    i =  0
    while not self.game.isSolved():
      #print("try number : " + str(i))
      if not self.forward_checking([-1]* self.game.n, self.game.variables):# we start with new empty line
        print("false")
        break
      self.game.check()
      #print(self.game.code, self.game.board)
      i+=1
    #print("Solved")
    return i
  def forward_checking(self,guess, variables):
    if guess.count(-1) == 0: #if no empty variable
      self.game.board.append([guess, 0,0])
      #print(" solution", guess)
      return True
    else:
      Xk = choice([ i for i in range(len(guess)) if guess[i] == -1])# first empty variable
      for v in variables[Xk].getDomaine():
        new = copy.deepcopy(variables)
        new_guess = guess.copy()
        new_guess[Xk] = v
        #print("check", new_guess)
        if self.checkConstistence(new_guess):
          #print("consistant")
          if self.check_forward(Xk, v, new, new_guess ):
            #print("essaie :" , new_guess, [i.getDomaine() for i in new] )
            if self.forward_checking(new_guess,new):
              return True
    return False

"""# Partie 2
## algorithme genetique
"""

import numpy as np
from random import random
import time
class Genetic(Solver):
    def __init__(self, game, maxsize, maxgen, timeout, populationSize, similarity , probability = 1/4):
      super().__init__(game)
      self.maxsize = maxsize
      self.maxgen = maxgen
      self.timeout = timeout
      self.populationSize = populationSize
      self.probability = probability
      self.similarity = similarity
    def population(self):
      return np.random.choice(self.game.domaine, (self.populationSize, self.game.n))
    def solve(self):
      i =  0
      while not self.game.isSolved():
        #print("try number : " + str(i))
        if not self.generate():
          print("======== failure of the algorithm ==========")
          break
        self.game.check()
        #print(self.game.code, self.game.board)
        i+=1
      #print("Solved")
      return i
    def fitness1(self, proposition): # fitness
      fitness = 0
      fitness += int( not all_diff(proposition)) * 100 # si non all diff, score penalisé
      if len(self.game.board) >0:
        fitness += int(not different_history(proposition, self.game.board))*100 # si non different, score penalisé
        for Past_propostion, redPawns, whitePawns in self.game.board:
          fitness += np.abs(GoodPositions(Past_propostion, proposition) - redPawns)# on ajoute le nombre d'incompatibilité
          fitness += np.abs(misplaced(Past_propostion, proposition) - whitePawns)
      return fitness

    def fitnessCalculation(self, fitness,population):
      fitnesses = []
      for code in population:
        fitnesses.append(fitness(list(code)))
      return np.array(fitnesses)



    def selectParents(self, fitnesses, population, K):
      parents = []
      for i in range(self.populationSize):# tournois
        tournoi = sample(list(range(self.populationSize)),K)
        parents.append(population[ sorted(tournoi, key=lambda x:fitnesses[x])[0] ])# on prend le plus petit des 10
      return np.array(parents)



    def mutation_permutation(self, code, pMute):
      nouvelIndividu = []
      for e in code:
        if random() < pMute:
          nouvelIndividu.append ( np.random.choice(self.game.domaine) )
        else:
          nouvelIndividu.append( e )
      return nouvelIndividu




    def mutate(self, parents, mutation, pMute):
      mutated = []
      for i in parents:
        mutated.append(mutation(i, pMute))
      return np.array(mutated)



    def add(self, population, E):
      for code in population:
        if self.checkConstistence(list(code)) and list(code) not in E:
          E.append(list(code))


    def select_similar(self, E):# selection du plus similaire
      similarities = np.zeros((len(E,)))
      for i, a in enumerate(E):
        for j, b in enumerate(E):
          if i!=j:
            similarities[i] += (np.array(a) == np.array(b)).sum()
      return E[similarities.argmax()]


    def select_least_similar(self, E):# selection du moins similaire
      similarities = np.zeros((len(E,)))
      for i, a in enumerate(E):
        for j, b in enumerate(E):
          if i!=j:
            similarities[i] += (np.array(a) == np.array(b)).sum()
      return E[similarities.argmin()]

    def select_estimation(self, E):# selection par estimation
      reduced = np.zeros((len(E)))
      for i, c in enumerate(E):
        for j, c1 in enumerate(E):
          if i!=j:
            history = self.game.board.copy()
            history.append([c1, GoodPositions(c1, c), misplaced(c1, c)])
            for k,c2 in enumerate(E):
              if k!=i and k!= j:
                reduced[i] += int(checkConstistence(c2, history))
      return E[reduced.argmin()]
    def select(self, E):
      if self.similarity == "most": # pick the most similar code
        return self.select_similar(E)
      elif self.similarity == "least": # picj the least similar
        return self.select_least_similar(E)
      elif self.similarity == "estimation": # pick the one that reduces the most
        return self.select_estimation(E)
      else:#random pick
        return E[np.random.choice(list(range(len(E))))]

    def generate(self):
      E = []
      population = self.population()
      start_time = time.time()
      generation = 0
      while( (len(E) < self.maxsize and generation < self.maxgen ) or ( len(E) == 0 and time.time() - start_time < self.timeout) ):
        fitnesses = self.fitnessCalculation(self.fitness1,population)
        parents = self.selectParents(fitnesses, population, 10)
        population =  self.mutate(parents, self.mutation_permutation, self.probability)
        self.add(population, E)
        generation +=1
      if len(E) > 0:
        essai = self.select(E)
        #print("essai : ", essai)
        self.game.board.append([essai, 0,0])
        return True
      return False
