# game class

from string import ascii_lowercase
from random import choice, sample
import numpy as np
import copy
from utils import *
class variable: # definition d'une variable
  def __init__(self, domaine):
    self.domaine = domaine.copy()
  def setDomaine(self, domaine):
    self.domaine = domaine
  def getDomaine(self):
    return self.domaine
  def remove_value(self, value):
    self.domaine.remove(value)


class Game: #definition du jeu
  def __init__(self, n, p):
    self.n = n
    self.p = p
    self.domaine = ([str(a) for a in range(10)] + list(ascii_lowercase))[:self.p]
    self.variables = [variable(self.domaine) for _ in range(n)]
    self.generate_code()
    self.board = []
  def getVariable(self, index):
    return self.variables[index]
  def generate_code(self): # generer un code avec caractere distincts
    self.code = [choice(self.domaine) ]
    for i in range(self.n -1):
        letter = choice(self.domaine)
        while letter in self.code:
          letter = choice(self.domaine)
        self.code.append(letter)
  def isSolved(self): # verifie si le jeu est resolu
    return True if len(self.board) > 0 and self.board[-1][0] == self.code  else False
  def check(self): # renvoie le nombre de pions rouges et blancs pour une proposition
    redPawns = GoodPositions(self.code, self.board[-1][0])
    whitePawns= misplaced(self.code, self.board[-1][0])
    self.board[-1][1], self.board[-1][2] = redPawns, whitePawns

class Game_2:# definition d'une classe du jeu qui accepte deux occurences du meme caractere
  def __init__(self, n, p):
    self.n = n
    self.p = p
    self.domaine = ([str(a) for a in range(10)] + list(ascii_lowercase))[:self.p]
    self.variables = [variable(self.domaine) for _ in range(n)]
    self.generate_code()
    self.board = []
  def getVariable(self, index):
    return self.variables[index]
  def generate_code(self):
    self.code = [choice(self.domaine) ]
    for i in range(self.n -1):
        letter = choice(self.domaine)
        while self.code.count(letter) >= 2:
          letter = choice(self.domaine)
        self.code.append(letter)
  def isSolved(self):
    return True if len(self.board) > 0 and self.board[-1][0] == self.code  else False
  def check(self):
    redPawns = GoodPositions(self.code, self.board[-1][0])
    whitePawns= misplaced(self.code, self.board[-1][0])
    self.board[-1][1], self.board[-1][2] = redPawns, whitePawns
