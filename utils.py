from game import *

def misplaced(instantiation,proposition): # nombre de piece qui change de place
    a ,b ,misplaced= instantiation.copy(), proposition.copy(), 0
    for index ,variable in enumerate(b):
      if variable == a[index] or variable == -1:
        a[index] = -1
        b[index] = -1
    for index ,variable in enumerate(b):
      i=0
      if variable != -1:
        while i < len(a) and a[i] != variable:
          i+=1
        if i < len(a):
          a[i]=-1
          misplaced +=1
    return misplaced
def GoodPositions(instantiation, proposition, local = False): # nombre de pice qui reste au meme endroit
  if not local:
    return sum([1 if proposition[i] == v else 0 for i,v in enumerate(instantiation)])
  else:
    return sum([1 if proposition[i] != -1 and proposition[i] == v else 0 for i,v in enumerate(instantiation)])

def all_diff(proposition, local=False): # test si tout les caracteres sont distincts
  if not local:
    if len(proposition) > len(set(proposition)):
      return False
    return True
  else:
    x =list(filter((-1).__ne__, proposition))
    if len(x) > len(set(x)):
      return False
    return True

def different_history(proposition, instantiations, local = False): # test si la proposition est nouvelle
  if not local:
    for i in instantiations:
      if proposition == i[0]:
        return False
    return True
  else:
    return True
def checkConstistence(proposition, history): # verifier la consistance d'une proposition
    if not all_diff(proposition): #check that every two variables are different
       #print("not different")
      return False
    if len(history) >0:# if there are previous proposed codes
      if not different_history(proposition, history): # check that the proposition is new
        #print('not different history')
        return False
      for Past_propostion, redPawns, whitePawns in history: #check the red pawns and white pawns for every past proposition
        if GoodPositions(Past_propostion, proposition) !=  redPawns : # if redPawns are good than we have to leave redPawns untouched
          #print("not goodPositions with " + str(Past_propostion))
          return False
        if misplaced(Past_propostion, proposition) != whitePawns: # if whitePawns must be moved than whitePawns must move the rest is false
          #print("not exact misplaced with " + str(Past_propostion))
          return False
    return True

def all_diff_2(proposition, local=False): # version de all diff pour cette version
  if not local:
    for v in set(proposition):
      if proposition.count(v) >2:
        return False
    return True
  else:
    x =list(filter((-1).__ne__, proposition))
    for v in set(x):
      if x.count(v) >2:
        return False
    return True

"""## A5"""
# nous utilisans une autre version des fonctions googpositions et misplaced
# pour renvoyer en plus les indices des variables concernés
def GoodPositions_2(instantiation, proposition, local = False):
  if not local:
    a = [i for i,v in enumerate(instantiation) if proposition[i] == v]
    return a, len(a)
  else:
    a =  [i for i,v in enumerate(instantiation) if proposition[i] == v]
    return a, len(a)


def misplaced_2(instantiation,proposition):
    a ,b ,misplaced= instantiation.copy(), proposition.copy(), 0
    indexes = []
    for index ,variable in enumerate(b):
      if variable == a[index] or variable == -1:
        a[index] = -1
        b[index] = -1
    for index ,variable in enumerate(b):
      i=0
      if variable != -1:
        while i < len(a) and a[i] != variable:
          i+=1
        if i < len(a):
          a[i]=-1
          indexes.append(index)
          misplaced +=1
    return indexes, misplaced
def remove_values(variables, exception, values, Misplaced): # supression de values sauf pour les exceptions
  if Misplaced: # dans le cas des caracteres mal placés
    for i, v in enumerate(variables):
      if i not in exception:
        for j, v_ in enumerate(values):
          if j != i and v_ in v.getDomaine():
            v.remove_value(v_)
  else: # dans le cas des caracteres au meme endroit
    for v in variables:
      for v_ in values:
        if v_ in v.getDomaine():
          v.remove_value(v_)
