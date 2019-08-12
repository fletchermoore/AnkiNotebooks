

# expects list of paths (list of strings)
# returns list of cards: ('front', 'back')
def genCards(pathList):
    cards = []
    for path in pathList:
        length = len(path)
        if length > 1:
            front = ': '.join(path[:length-1])
            back = path[-1]
            cards.append((front.strip(), back.strip()))
    cards = reverseMarkedCards(cards)
    cards = consolidateCards(cards)
    return cards


# expects list of tuples ('front', 'back')
# swaps back and front if the back-string starts with '<<'
# returns same format
def reverseMarkedCards(cards):
    updatedCards =[]
    for card in cards:
        front = card[0]
        back = card[1]
        if back.find('<<') == 0: # if back starts with <<
            newFront = back[2:].lstrip()
            newBack = front
            updatedCards.append((newFront, newBack))
        else:
            updatedCards.append(card)
    return updatedCards


# expects a list of tuples
# returns a list of tuples
# ADJACENT cards with same front are joined into a single card
def consolidateCards(cards):
    shorterList = []
    prevCard = ('', '')
    for card in cards:
        if card[0] == prevCard[0]:
            #print("found dupplicate: ", str(card))
            prevCard = shorterList[-1]
            shorterList[-1] = (prevCard[0], prevCard[1] + '<br/><br/>' + card[1])
        else:
            shorterList.append(card)
            prevCard = card
    return shorterList
