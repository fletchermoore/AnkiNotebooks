

# expects list of paths (list of strings)
# returns list of cards: ('front', 'back')
def genCards(pathList):
    cards = []
    for path in pathList:
        length = len(path)
        if length > 1:
            front = ': '.join(path[:length-1])
            back = path[-1]
            cards.append((front, back)) 
    cards = consolidateCards(cards)
    return cards


# expects a list of tuples
# returns a list of tuples
# cards with same front are joined into a single card
def consolidateCards(cards):
    shorterList = []
    for card in cards:
        index = findIndex(shorterList, card)
        if index > -1:
            #print("found dupplicate: ", str(card))
            preexistingCard = shorterList[index]
            shorterList[index] = (preexistingCard[0], preexistingCard[1] + '<br/><br/>' + card[1])
        else:
            shorterList.append(card)
    return shorterList


def findIndex(list, targetCard):
    for key, card in enumerate(list):
        if card[0] == targetCard[0]:
            return key
    return -1

