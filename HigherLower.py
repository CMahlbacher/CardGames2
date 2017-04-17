'''
Created on Apr 16, 2017

@author: cmahl_000
'''

from Deque import Deque
from random import randint
from Stack import Stack
from Linked_List import Linked_List


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
        self.totalCardValue = 8 * 52
        self.helperList = Linked_List()
           
        for i in range(2, 15):
            self.deck.push_front(Card(i, 'Club'))
            self.deck.push_front(Card(i, 'Spade'))
            self.deck.push_front(Card(i, 'Diamond'))
            self.deck.push_front(Card(i, 'Heart'))
            for k in range(4):
                self.helperList.append_element(i)
                
        
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
        
        card = self.deck.pop_front()
        self.totalCardValue = self.totalCardValue - card.getValue()
        self.helperList.remove_element(card.getValue())
        return card
    
    
    def randomShuffle(self):
        deckLength = len(self.deck)
        tempArray = [None] * deckLength
        
        while len(self.deck) > 0:
            x = randint(0, deckLength - 1)
            
            if tempArray[x] is None:
                tempArray[x] = self.deck.pop_back()
                
        
        for k in range(0, deckLength):
            self.deck.push_front(tempArray[k])
            
    def averageCardLeft(self):
        return self.totalCardValue / len(self)
            
    def medianCardLeft(self):
        return self.helperList

class ComputerPlayer:
    
    def decide(self, card, deck):
        if card.getValue() < deck.averageCardLeft():
            return "h"
        if card.getValue() > deck.averageCardLeft():
            return "l"
        if card.getValue() == deck.averageCardLeft():
            return "tie"
        
    def decide2(self, card, deck):
        length = len(deck)
        index = randint(0, length - 1)
        #print("The random index was " + str(index))
        number = deck.medianCardLeft().get_element_at(index)
        #print("The randomly chosen number was " + str(number))
        #print("The list looks like " + str(deck.medianCardLeft()))
        if card.getValue() < number:
            return "h"
        if card.getValue() > number:
            return "l"
        if card.getValue() == number:
            return "tie"
        
        
        


class UserInteraction:
    
    def run(self):
        #stillPlaying = True
        runs = 0
        #while stillPlaying:
        wins = 0
        lowestCardsLeft = 50
        while runs < 1000:
            game = Game()
            #print(str(lowestCardsLeft))
            #lowestCardsLeft, won = game.run(wins, lowestCardsLeft)
            game.run(wins, lowestCardsLeft)
            #if won:
                #wins += 1
            #runs +=1
            #answer = input("Play again? (y/n)")
            #if answer == "n":
             #   stillPlaying = False
        #print("Won " + str(wins) + " times")
        #print("Fewest cards left was " + str(lowestCardsLeft))
            
class Game:
    
    def __init__(self):
        self.deck = Deck()
        self.computerPlayer = ComputerPlayer()
        self.deck.randomShuffle()
        self.stack1 = Stack()
        self.stack2 = Stack()
        self.stack3 = Stack()
        self.stack4 = Stack()
        self.stack5 = Stack()
        self.stacks = [self.stack1, self.stack2, self.stack3, self.stack4, self.stack5]
        self.stacksAlive = [True, True, True, True, True]
        for i in self.stacks:
            i.push(self.deck.dealCard())
            
        
        
    def alive(self):
        for i in self.stacksAlive:
            if i:
                return i
        return False
    
    def run(self, wins, lowestCardsLeft):
        counter = 0
        while len(self.deck) > 0 and self.alive():
            if self.stacksAlive[counter % 5] == False:
                counter += 1
            else: 
                compareCard = self.stacks[counter % 5].peek()
                answer = input("Higher or lower than(or same as) " + str(compareCard) + "?")
                #print("Higher or lower than(or same as) " + str(compareCard) + "?")
                #answer = self.computerPlayer.decide(compareCard, self.deck)
                #print(answer)
                newCard = self.deck.dealCard()
                print(str(newCard))
                self.stacks[counter % 5].push(newCard)
                if answer == "h":
                    if newCard > compareCard:
                        pass
                        print("Correct!")
                    else:
                        print("Wrong!")
                        self.stacksAlive[counter % 5] = False
                if answer == "l":
                    if newCard < compareCard:
                        print("Correct!")
                        pass
                    else:
                        print("Wrong!")
                        self.stacksAlive[counter % 5] = False
                if answer == "tie":
                    if newCard == compareCard:
                        print("Correct!")
                        pass
                    else:
                        print("Wrong!")
                        self.stacksAlive[counter % 5] = False
                counter+= 1
                print()
        #x = False
        if self.alive():
            print("You win!")
            #x = True
        print("You lose!")
        print("There were still " + str(len(self.deck)) + " cards left.")
        #print(str(lowestCardsLeft))
        #if len(self.deck) < lowestCardsLeft:
            #return len(self.deck), x
        #return lowestCardsLeft, x
            
            

if __name__ == "__main__":
    x = UserInteraction()
    x.run()
    
    
    
    
    
    