# converts data to format
# [
#    (['path','to','prompt'], ['answer','paragraphs'])
# ]

import re

# takes string, string
# returns ([string, ... ], [string, ...])
# splits prompts about ': '
# splits answers about '<br><br>'
def escapedCardToPath(prompt, answer):
    answers = re.split(r'<br ?\/?>', answer)
    answers = [t for t in answers if t != ''] # remove blank answers
    return (prompt.split(': '), answers)


# this will consolidate the paths into a tree structure
def createTree(paths):
    root = Node('')
    for path in paths:
        tree = pathToTree(path)
        root.add(tree)
    root = consolidate(root)
    return root


# takes tree
# return tree
# collapses duplicate nodes in prompt to single node
# eg
# a ->
#   b ->
#     c
# a ->
#   b ->
#     d
# becomes
# a ->
#   b ->
#     c
#     d
def consolidate(node):
    uniqueChildren = []
    for child in node.children:
        # we are allowed to duplicate terminal leaves
        if len(child.children) == 0:
            uniqueChildren.append(child)
            continue
        else:
            # recursive
            updatedChild = consolidate(child)
        # either unique node or has duplicates
        existingChild = findNode(uniqueChildren, updatedChild)
        if existingChild == None:
            # this child is unique, just add it to the pile
            uniqueChildren.append(updatedChild)
        else:
            # if this is a duplicate, just add its children to the
            # existing child
            existingChild.addChildren(updatedChild.children)
    node.children = uniqueChildren
    return node


def findNode(nodeList, testNode):
    for node in nodeList:
        if testNode.text == node.text:
            return node
    return None


# takes path [[string],[string]]
# returns tree 
# eg [['a','b',c'],['ans1','ans2']]
# becomes:
# a ->
#  b ->
#   c ->
#     ans1
#     ans2
# will fail if path arg is malformed
def pathToTree(path):
    root = Node('')
    prevNode = root
    currNode = root
    # walk down the prompts
    for text in path[0]:
        currNode = Node(text)
        prevNode.add(currNode)
        prevNode = currNode
    answers = []
    # now add the answers to the last prompt
    for text in path[1]:
        answers.append(Node(text))
    currNode.addChildren(answers)
    if len(root.children) > 0:
        return root.children[0] # don't return the dummy root node
    else:
        return root # fail silently



def pathsToBullets(paths):
    root = createTree(paths)
    bullets = [] # no bullet for the root
    for child in root.children:
        childBullets = getBullets(0, child)
        bullets.extend(childBullets)
    return bullets

# tree traversal
# returns [(ilvl, text)]
def getBullets(ilvl, node):
    currBullet = (ilvl, node.text)
    bullets = [currBullet]
    for child in node.children:
        childBullets = getBullets(ilvl+1, child)
        bullets.extend(childBullets)
    return bullets

# legacy method
# given list of paths [([string],[string])] 
# returns bullets with indent levels [(ilvl, text)]
# def pathsToBullets(paths):
#     bullets = []
#     for path in paths:
#         ilvl = 0
#         promptPath = path[0]
#         for text in promptPath:
#             bullet = (ilvl, text)
#             bullets.append(bullet)
#             ilvl += 1
#         answers = path[1]
#         for elem in answers:
#             bullet = (ilvl, elem)
#             bullets.append(bullet)        
#     return bullets


# simple tree structure
class Node:
    def __init__(self, text):
        self.text = text
        self.children = []

    def add(self, child):
        self.children.append(child)
    
    def addChildren(self, children):
        self.children.extend(children)

