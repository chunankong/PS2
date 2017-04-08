from node import Node
import math
import random

def ID3(examples, default):
    '''
    Takes in an array of examples, and returns a tree (an instance of Node)
    trained on the examples.  Each example is a dictionary of attribute:value
    pairs, and the target class variable is a special attribute with the name
    "Class". Any missing attributes are denoted with a value of "?"
    '''
    if not examples:
        return Node(default)

    target_vals = [example['Class'] for example in examples]
    if target_vals.count(target_vals[0]) == len(target_vals):
        print 'enter len check'
        return Node(target_vals[0])
    else:
        attrs = [key for key in examples[0].keys() if key != 'Class']
        best_attr = choose_attr(examples, 'Class', attrs)
        node = Node(best_attr)

        for val in get_values(examples, best_attr):
            subset = []
            for example in examples:
                if best_attr in example and example[best_attr] == val:
                    subset.append(example)

            for entry in subset:
                del entry[best_attr]

            subtree = ID3(subset, default)
            node.children[val] = subtree

        return node

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
    if not node.children:
        return node.label

############################## HELPER FUNCTIONS ###############################

def calc_entropy(examples, attr):
    '''
    Calculates entropy of the given attribute.
    '''
    val_freq = {}
    for example in examples:
        if example[attr] in val_freq:
            val_freq[example[attr]] += 1.0
        else:
            val_freq[example[attr]] = 1.0

    entropy = 0.0
    for val in val_freq.values():
        val_prob = val / sum(val_freq.values())
        entropy += (-val_prob) * math.log(val_prob, 2)

    return entropy

def calc_infogain(examples, target_attr, attr):
    '''
    Calculates informaiton gain of the given attribute.
    '''
    val_freq = {}
    for example in examples:
        if example[attr] == '?':
            example[attr] = random.choice('yn')

        if example[attr] in val_freq:
            val_freq[example[attr]] += 1.0
        else:
            val_freq[example[attr]] = 1.0

    subset_entropy = 0.0
    for val in val_freq.values():
        val_prob = val / sum(val_freq.values())
        subset = [example for example in examples if example[attr] == val]
        subset_entropy += val_prob * calc_entropy(subset, target_attr)


    return calc_entropy(examples, target_attr) - subset_entropy

def choose_attr(examples, target_attr, attrs):
    '''
    Choose the best attribute to split on based on information gain.
    '''
    best_attr = None
    best_infogain = 0.0

    for attr in attrs:
        infogain = calc_infogain(examples, target_attr, attr)
        if infogain >= best_infogain:
            best_infogain = infogain
            best_attr = attr

    return best_attr

def get_values(examples, attr):
    vals = []
    for example in examples:
        if not vals or example[attr] not in vals:
            vals.append(example[attr])
    return vals
