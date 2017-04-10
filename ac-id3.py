from node import Node
import math

CLASS_ATTR = 'Class'

def ID3(examples, default):
    '''
    Takes in an array of examples, and returns a tree (an instance of Node)
    trained on the examples.  Each example is a dictionary of attribute:value
    pairs, and the target class variable is a special attribute with the name
    "Class". Any missing attributes are denoted with a value of "?"
    '''
    # return default value if the example set is empty
    if not examples:
        return Node(default)

    class_vals = [example[CLASS_ATTR] for example in examples]
    # return the classification if all examples have the same class value
    if class_vals.count(class_vals[0]) == len(class_vals):
        return Node(class_vals[0])
    else:
        attrs = [attr for attr in examples[0].keys() if attr != CLASS_ATTR]
        # return the most common class value if attribute set is empty
        if not attrs:
            return Node(find_majority(examples))

        # create a new node with the best attribute as label
        best_attr = choose_attr(examples, attrs)
        node = Node(best_attr)
        node.majority = find_majority(examples)

        for val in get_values(examples, best_attr):
            # filter a subset
            subset = []
            for example in examples:
                if example[best_attr] == val:
                    new_example = {}
                    for example_attr, example_val in example.items():
                        if example_attr != best_attr:
                            new_example[example_attr] = example_val
                    subset.append(new_example)

            subtree = ID3(subset, default)
            node.children[val] = subtree

        return node

def prune(node, examples):
    '''
    Takes in a trained tree and a validation set of examples. Prunes nodes in
    order to improve accuracy on the validation data; the precise pruning
    strategy is up to you. Reduced Error Pruning used.
    '''
    acc_table = {}
    nodes = [node]

    while nodes:
        curr_node = nodes.pop()
        # skip leaf nodes
        if not curr_node.children:
            continue

        nodes.extend([child for child in curr_node.children.values()])
        children_save = curr_node.children
        label_save = curr_node.label

        # change current node to leaf node and test accuracy
        curr_node.children = {}
        curr_node.label = curr_node.majority
        acc_table[curr_node] = test(node, examples)

        curr_node.children = children_save
        curr_node.label = label_save

    curr_acc = test(node, examples)
    best_acc = curr_acc
    prune_node = None
    for key, val in acc_table.items():
        if val > best_acc:
            best_acc = val
            prune_node = key

    # prune the node with better accuracy
    if best_acc != curr_acc:
        prune_node.label = prune_node.majority
        prune_node.children = {}
        prune(node, examples)

def test(node, examples):
    '''
    Takes in a trained tree and a test set of examples.  Returns the accuracy
    (fraction of examples the tree classifies correctly).
    '''
    success = 0.0
    for example in examples:
        if evaluate(node, example) == example[CLASS_ATTR]:
            success += 1.0
    return success / len(examples)

def evaluate(node, example):
    '''
    Takes in a tree and one example.  Returns the Class value that the tree
    assigns to the example.
    '''
    if not node.children:
        return node.label

    # handle unknown attribute values
    if example[node.label] not in node.children.keys():
        keys = node.children.keys()
        return evaluate(node.children[keys[0]], example)
    else:
        return evaluate(node.children[example[node.label]], example)

############################## HELPER FUNCTIONS ###############################

def calc_entropy(examples, attr):
    '''
    Return entropy of the given attribute.
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

def calc_infogain(examples, attr):
    '''
    Return informaiton gain of the given attribute.
    '''
    val_freq = {}
    missing_attr = 0.0
    for example in examples:
        if example[attr] == '?':
            missing_attr += 1.0
        elif example[attr] in val_freq:
            val_freq[example[attr]] += 1.0
        else:
            val_freq[example[attr]] = 1.0

    # handle missing attributes
    if missing_attr != 0.0:
        # find the majority value
        majority_val = None
        majority_freq = 0.0
        for val, freq in val_freq.items():
            if freq > majority_freq:
                majority_val = val
                majority_freq = freq

        # swap missing attributes with the majority value
        for example in examples:
            if example[attr] == '?':
                example[attr] = majority_val

        # update frequency table
        val_freq[majority_val] += missing_attr

    subset_entropy = 0.0
    for val in val_freq.values():
        val_prob = val / sum(val_freq.values())
        subset = [example for example in examples if example[attr] == val]
        subset_entropy += val_prob * calc_entropy(subset, CLASS_ATTR)

    return calc_entropy(examples, CLASS_ATTR) - subset_entropy

def choose_attr(examples, attrs):
    '''
    Return the best attribute to split on based on information gain.
    '''
    best_attr = None
    best_infogain = 0.0
    for attr in attrs:
        infogain = calc_infogain(examples, attr)
        if infogain > best_infogain:
            best_infogain = infogain
            best_attr = attr
    return best_attr

def get_values(examples, attr):
    '''
    Return all possible values of the given attribute.
    '''
    vals = []
    for example in examples:
        if example[attr] not in vals:
            vals.append(example[attr])
    return vals

def find_majority(examples):
    '''
    Return the majority calss value.
    '''
    val_freq = {}
    majority_freq = 0.0
    majority_val = None
    for example in examples:
        if example[CLASS_ATTR] in val_freq:
            val_freq[example[CLASS_ATTR]] += 1.0
        else:
            val_freq[example[CLASS_ATTR]] = 1.0

    for val, freq in val_freq.items():
        if freq > majority_freq:
            majority_freq = freq
            majority_val = val

    return majority_val
