from random import randint
from Deque import Deque
from Stack import Stack
from Linked_List import Linked_List

class Durak:
    
    
    
    def __init__(self):
        self.run()
    
    def run(self):
        self.player1 = Player(False, "Brad")
        self.player2 = Player(False, "Rachel")
        self.masterDeck = Deck()
        self.masterDeck.randomShuffle()
        self.deal()
        self.trumpSuit = self.masterDeck.trumpCard().getSuit()
        self.setInitialAttacker()
        self.play()
        
    def play(self):
        
        gameOver = self.gameOver()
        while not gameOver:
            attackSuccess = self.startAttack()
            print("Player 1: " + str(self.player1))
            print("Player 2: " + str(self.player2))
            self.draw(attackSuccess)
            print("////////////////////")
            print("Player 1: " + str(self.player1))
            print("Player 2: " + str(self.player2))
            gameOver = self.gameOver()
        
    def draw(self, attackSuccess):
        if len(self.masterDeck) == 0:
            return
        if attackSuccess:
            while len(self.masterDeck) > 0 and len(self.attacker) < 6:
                self.attacker.append_element(self.masterDeck.dealCard())
        else:
            while len(self.masterDeck) > 0 and len(self.defender) < 6:
                self.defender.append_element(self.masterDeck.dealCard())
            while len(self.masterDeck) > 0 and len(self.attacker) < 6:
                self.attacker.append_element(self.masterDeck.dealCard())
            
        
            
    def startAttack(self):
        attackStack = Stack()
        playedCards = Linked_List()
        return self.attack(attackStack, playedCards)
        
    def attack(self, attackStack, playedCards):
        maxCards = self.setMaximumCardsTaken()
        isResolved = False
        self.attackCard(playedCards, attackStack)
        while not isResolved:
            defenseCard = self.defendCard(attackStack, playedCards)
            if defenseCard is not None:
                attackStack.push(defenseCard)
                isResolved = self.attackAgain(attackStack, playedCards, isResolved, maxCards)
            else:
                self.failedDefense(playedCards, attackStack, maxCards)
                print("Failed defense")
                return True
        return False

    def setMaximumCardsTaken(self):
        if len(self.defender) > 6:
            numOfCards = 6
        else:
            numOfCards = len(self.defender)
        return numOfCards
            
                
    def failedDefense(self, playedCards, attackStack, numOfCards):
        
        self.gibMoreCards(playedCards, attackStack, numOfCards)
        
        for i in range(0, len(playedCards)):
            self.defender.append_element(playedCards.remove_element_at(0))
        for i in range(0, len(attackStack)):
            self.defender.append_element(attackStack.pop())
            
            
    def gibMoreCards(self, playedCards, attackStack, numOfCards):
        cardsTaken = (len(playedCards) / 2) - 1 
        
        
        while cardsTaken < numOfCards:
            givenCard = self.canPlayAgain(playedCards)
            if self.chooseGibCard() and givenCard is not None:
                print("Also Take " + str(givenCard))
                self.defender.append_element(givenCard)
            else: 
                return 
            
    def chooseGibCard(self):
        return True
    
    def attackAgain(self, attackStack, playedCards, isResolved, numOfCards):
        print(attackStack)
        for i in range(0, len(attackStack)):
            playedCards.append_element(attackStack.pop())
        attackCard = self.canPlayAgain(playedCards)
        if attackCard is not None and (len(playedCards) / 2) < numOfCards:
            if self.choosePlayAgain():
                print("Attack with " + str(attackCard))
                attackStack.push(attackCard)
                return False
            else:
                self.attacker.append_element(attackCard)
        else:
            print("Successful defense")
            self.switchPlayers()
            return True

    def choosePlayAgain(self):
        return True
            
    def canPlayAgain(self, playedCards):
        for i in range(0, len(playedCards)):
            for k in range(0, len(self.attacker)):
                if self.attacker.get_element_at(k).card == playedCards.get_element_at(i).card:
                    return self.attacker.remove_element_at(k)
        return None
        
    
    def attackCard(self, playedCards, attackStack):
        if len(playedCards) == 0:    
            print("Attack with " + str(self.attacker.get_element_at(0)))
            attackStack.push(self.attacker.remove_element_at(0))
            
        else:
            return self.canPlayAgain(playedCards)
        
        
    
    def defendCard(self, attackStack, playedCards):
        
        for i in range(0, len(self.defender)):
            candidateCard = self.defender.get_element_at(i)
            if candidateCard.beats(attackStack.peek(), self):
                
                print("Defend with " + str(candidateCard))
                self.defender.remove_element_at(i)
                return candidateCard
        return None
            
        
        
    
    def gameOver(self):
        
        if len(self.masterDeck) == 0 and len(self.defender) == 0:
            if self.defender == self.player1:
                print("Player 1 wins!")
            else:
                print("Player 2 wins!")
            return True
        if len(self.masterDeck) == 0 and len(self.attacker) == 0:
            if self.attacker == self.player1:
                print("Player 1 wins!")
            else:
                print("Player 2 wins!")
            return True
        return False
    
    def setInitialAttacker(self):
        lowTrump1 = 16
        lowTrump2 = 16
        
        for i in range(0, 6):
            current = self.player1.get_element_at(i)
            if (current.getSuit() == self.masterDeck.trumpCard().getSuit()):
                if lowTrump1 > current.getValue():
                    lowTrump1 = current.getValue()
            
            current2 = self.player2.get_element_at(i)
            if (current2.getSuit() == self.masterDeck.trumpCard().getSuit()):
                if lowTrump2 > current2.getValue():
                    lowTrump2 = current2.getValue()
            
        
        if lowTrump1 < lowTrump2:
            self.attacker = self.player1
            self.defender = self.player2
            print("Attacker is Player 1")
        else:
            self.attacker = self.player2
            self.defender = self.player1
            print("Attacker is Player 2")
            
    
    def setAttacker(self, player):
        self.attacker = player
        
    def setDefender(self, player):
        self.defender = player
        
    def switchPlayers(self):
        temp = self.attacker
        self.attacker = self.defender
        self.defender = temp
        
        
    def deal(self):
        for k in range(0, 2):
            for i in range (0, 3):
                self.player1.append_element(self.masterDeck.dealCard())
            for i in range (0, 3):
                self.player2.append_element(self.masterDeck.dealCard())
        
        print(str(self.masterDeck.trumpCard()) + " is the bottom card.")
        
        print("Player 1:" + str(self.player1))
        print("Player 2:" + str(self.player2))
        
class Player:
    
    def __init__(self, human, name):
        self.name = name
        self.human = human
        self.cards = Linked_List()
        
        if self.human == False:
            self.chooseComputerLevel()
            
    def remove_element_at(self, index):
        
        return self.cards.remove_element_at(index)
    
    def __str__(self):
        
        return str(self.cards)
            
    def __len__(self):
        
        return len(self.cards)
            
            
    def chooseComputerLevel(self):
        self.level = 1
        
    def chooseGibCard(self):
        if self.human:
            return userChoice()
        if self.level == 1:
            return True
        
    def choosePlayAgain(self):
        if self.human:
            return userChoice()
        if self.level == 1:
            return True
        
    def append_element(self, card):
        
        self.cards.append_element(card)
        
    def get_element_at(self, index):
        
        return self.cards.get_element_at(index)
    
    def attackAgainCard(self, playedCards):
        if self.human:
            return userChoice()
        for i in range(0, len(playedCards)):
            for k in range(0, len(self.attacker)):
                if self.attacker.get_element_at(k).card == playedCards.get_element_at(i).card:
                    if self.level == 1:
                        return self.attacker.remove_element_at(k)
        return None

class Card:
            
    def __init__(self, card, suit):
        self.card = card
        self.suit = suit
        self.cardValues = {2 : 'Two', 3 : 'Three', 4 : 'Four', 5 : 'Five', 6 : 'Six', 7 : 'Seven', 8 : 'Eight', 9 : 'Nine', 10 : 'Ten', 11 : 'Jack', 12 : 'Queen', 13 : 'King', 14 : 'Ace'}        
    
    def __lt__(self, other):
        
        return self.card < other.card
    
    def __gt__(self, other):
        return self.card > other.card
    
    def __eq__(self, other):
        return self.card == other.card
    
    def __str__(self):
        return self.cardValues[self.card] + " of " + self.suit + "s"
    
    def getSuit(self):
        return self.suit
    
    def getValue(self):
        return self.card
    
    def beats(self, otherCard, currentGame):
        
        if self.suit == otherCard.suit:
            return self.card > otherCard.card
        else:
            return self.suit == currentGame.trumpSuit
    
    
        
class Deck:
        
        
    def __init__(self):
        self.deck = Deque()
           
        for i in range(6, 15):
            self.deck.push_front(Card(i, 'Club'))
            self.deck.push_front(Card(i, 'Spade'))
            self.deck.push_front(Card(i, 'Diamond'))
            self.deck.push_front(Card(i, 'Heart'))
        
    def __str__(self):
        
        toReturn = ''
            
        for i in range(0, len(self.deck)):
            guv = self.deck.pop_front()
            toReturn = toReturn + str(guv) + '\n'
            self.deck.push_back(guv)
            
        return toReturn
    
    def __len__(self):
        
        return len(self.deck)
    
    def dealCard(self):
        
        return self.deck.pop_front()
    
    def trumpCard(self):
        
        return self.deck.peek_back()
    
    def randomShuffle(self):
        deckLength = len(self.deck)
        tempArray = [None] * deckLength
        
        while len(self.deck) > 0:
            x = randint(0, deckLength - 1)
            
            if tempArray[x] is None:
                tempArray[x] = self.deck.pop_back()
                
        
        for k in range(0, deckLength):
            self.deck.push_front(tempArray[k])
            
    def shuffle_deck(self):
        
        deckA = Deque()
        deckB = Deque()
        
        for k in range(0, 30):
            for i in range(0, 36):
                if i < 18:
                    deckA.push_front(self.deck.pop_back())
                else:
                    deckB.push_front(self.deck.pop_back())
                    
            while len(deckA) > 0 or  len(deckB) > 0:
                x = randint(0, 3)
                for i in range(0, x):
                    if len(deckA) > 0:
                        self.deck.push_front(deckA.pop_back())
                x = randint(0, 3)
                for i in range(0, x):
                    if len(deckB) > 0:
                        self.deck.push_front(deckB.pop_back())
                        
        print("Shuffled")



    
if __name__ == '__main__':
    bob = Durak()
