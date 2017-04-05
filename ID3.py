from node import Node
import math

usedatt = 0
def ID3(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''
  tree = []
  classfc=[]
  A = Node()
  for each in examples:
    classfc.append(each.get('Class'))
#if there is no more items in the list
  if examples == None:
    A.label=default
    A.children=None
    return A
#if all the remaining examples are the same category
  elif all(x==examples[0] for x in examples):
    A.label=examples[0].get('Class')
    A.children=None
    return A
#if we ran out of possible trees
  elif usedatt == 16:
    numD=0
    numR=0
    for each in examples:
      if each.get('Class')=='democrat':
        numD+=1
      elif each.get('Class')=='republican':
        numR+=1
    if numD>numR:
      A.label='democrat'
      A.children=None
      return A
    else:
      A.label='republican'
      A.children=None
      return A
# the general case.
  else:
    return tree
  
def prune(node, examples):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''

def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''


def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
