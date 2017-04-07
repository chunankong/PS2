from node import Node
import math

usedatt = []
def ID3(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''
  tree = []
  classfc=[]
  yexamples = []
  nexamples = []
  A = Node()
  modeA = Node()
  tree = Node()
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
  elif len(usedatt) == 16:
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
      modeA = A
      return A
    else:
      A.label='republican'
      A.children=None
      modeA = A
      return A
# the general case.
# the first children is the node of next category with selection 'n'
# the second children is the node of next category with the selection 'y'
  else:
    bestL= getBestL(examples,default)
    usedatt.append(bestL)
    for each in examples:
      if each.get(bestL) == 'y':
        yexamples.append(each)
      else:
        nexamples.append(each)
    ysubtree = ID3(yexamples, modeA.label)
    nsubtree = ID3(nexamples, modeA.label)
    tree.label = bestL
    children[0] = nsubtree
    children[1] = ysubtree
    return tree

def getBestL(examples, default):
  '''
  helper function that returns the best label for the root node
  '''
  myatts = examples.keys()
  myatts.remove('Class')
  total = len(examples)
  mystats = []
  mylabel = default
## the following gets a list of dictionaries with key=label and value = list of difference
## in votings number of d-number of r in the order of n, y
  for each in myatts:
    sig = 0
    eachyr = 0
    eachyd = 0
    eachnr = 0
    eachnd = 0
    if each not in usedatt:
      for example in examples:
      if example.get(each) == 'y' and example.get('Class') == 'democrat':
        eachyd += 1
      elif example.get(each) == 'y' and example.get('Class') == 'republican':
        eachyr += 1
      elif example.get(each) == 'n' and example.get('Class') == 'democrat':
        eachnd += 1
      elif example.get(each) == 'n' and example.get('Class') =='republican':
        eachnr += 1
    ysig = math.pow(((eachnd-eachnr)/(eachnd+eachnr)),2)
    nsig = math.pow(((eachyd-eachyr)/(eachyd+eachyr)),2)
    sig = ysig+nsig
    mystats.append({each, sig})
##
  mycandvs = mystats.values()
  mymax = 0
  for each in mycandvs:
    if each > mymax:
      mymax = each
  d2 = dict((v,k) for k,v in mystats.iteritems())
  mylabel = d2.get(mymax)
  return mylabel



  


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
  accr = 1
  total = len(examples)
  for each in examples:
    myresult = evaluate(node, each)
    if myresult == each.get('Class'):
      accr += 1
  return accr/total 


def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
