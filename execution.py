"""
	auteur; H Chekirou
	fichier de demonstration
"""

from game import *
from utils import *
from solver import *

print("=======================================================================")
print("                        Engendrer et tester")
print("=======================================================================")
jeu = Game(6, 12)# declaration d'un jeu n = 6 et p = 12
Algo = EngTest(jeu)# on declare l'algorithme
Algo.solve()# on lance la resoltion
print("===== code secret =====")
print(jeu.code)
print("===== L'execution du jeu (propositon, Pions rouges, Pions Blancs) =====")
print(jeu.board) # on affiche la partie

print("=======================================================================")
print("                  Retour arriere chronologique")
print("=======================================================================")
jeu = Game(6, 12)
Algo = RAC(jeu)
Algo.solve()
print("===== code secret =====")
print(jeu.code)
print("===== L'execution du jeu (propositon, Pions rouges, Pions Blancs) =====")
print(jeu.board)

print("=======================================================================")
print("                       Forward checking")
print("=======================================================================")
jeu = Game(6, 12)
Algo = Forward_checking(jeu)
Algo.solve()
print("===== code secret =====")
print(jeu.code)
print("===== L'execution du jeu (propositon, Pions rouges, Pions Blancs) =====")
print(jeu.board)
print("=======================================================================")
print("         Forward_checking version avec occurrences")
print("=======================================================================")
jeu = Game_2(6, 12) # jeu avec occurences
Algo = Forward_checking_2(jeu)
Algo.solve()
print("===== code secret =====")
print(jeu.code)
print("===== L'execution du jeu (propositon, Pions rouges, Pions Blancs) =====")
print(jeu.board)
print("=======================================================================")
print("                              A5")
print("=======================================================================")
jeu = Game(6, 12)
Algo = Forward_checking_3(jeu)
Algo.solve()
print("===== code secret =====")
print(jeu.code)
print("===== L'execution du jeu (propositon, Pions rouges, Pions Blancs) =====")
print(jeu.board)
print("=======================================================================")
print("                            Genetique")
print("=======================================================================")
jeu = Game(6, 12)
Algo = Genetic(jeu, maxsize=3, maxgen=10, timeout=300, populationSize=15, similarity= "random" , probability = 1/4)
Algo.solve()
print("===== code secret =====")
print(jeu.code)
print("===== L'execution du jeu (propositon, Pions rouges, Pions Blancs) =====")
print(jeu.board)
