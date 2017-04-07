from node import Node
import math

def ID3(examples, default):
    '''
    Takes in an array of examples, and returns a tree (an instance of Node)
    trained on the examples.  Each example is a dictionary of attribute:value
    pairs, and the target class variable is a special attribute with the name
    "Class". Any missing attributes are denoted with a value of "?"
    '''
    if not examples:
        return default
    elif: # return classification if all examples have the same classification
    else:


def calc_entropy(examples, attr):
    """
    Calculates entropy of the given attribute.
    """
    val_freq = {}
    for example in examples:
        if example[attr] in val_freq:
            val_freq[example[attr]] += 1.0
        else:
            freq[example[attr]] = 1.0

    entropy = 0.0
    for val in val_freq.values():
        val_prob = val / sum(val_freq.values())
        entropy += val_prob * math.log(val / val_prob), 2)

    return entropy * (-1.0)

def calc_infogain(examples, prior_attr, attr):
    """
    Calculates informaiton gain of the given attribute.
    """
    val_freq = {}
    for example in examples:
        if example[attr] in val_freq:
            val_freq[example[attr]] += 1.0
        else:
            freq[example[attr]] = 1.0

    subset_entropy = 0.0
    for val in val_freq.values():
        val_prob = val / sum(val_freq.values())
        subset = [example for example in examples if example[attr] = val]
        subset_entropy += val_prob * calc_entropy(subset, prior_attr)

    return calc_entropy(examples, prior_attr) - subset_entropy

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
