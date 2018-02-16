import collections
import Poker
import random
import itertools
from bcolors import bcolors
from random import sample

class Player():
	def __init__(self, name:str):
		self.hand = set()
		self.name = name
		self.points = 0

		self.suits = {
		'Hearts' : [],
		'Spades' : [],
		'Diamonds' : [],
		'Clubs' : []
		}

	def __str__(self):
		return self.name

	def setCards(self, cards):
		'''
		Receives cards from the deck
		'''

		if len(cards) != 13:
			raise ValueError('Player {} received {} cards instead of 13 cards! Abort.'.format(self.name, len(cards)))
		else:
			cards.sort(key = lambda x: x.number)

			self.hand = set(cards)

			for card in cards:
				self.suits[card.suit].append(card)


	def printCards(self):
		'''
		Shows the player's hand
		'''
		'''		
		for suit in self.suits:
			for card in self.suits[suit]:
				print('\033[94m' + str(card) + '\033[0m')
			print()
		'''
		for h,s,d,c in itertools.zip_longest(self.suits['Hearts'],self.suits['Spades'],self.suits['Diamonds'],self.suits['Clubs']):
			

			print( bcolors.OKBLUE + "{:25}	{:25}	{:25}	{:25}".format(str(h),str(s),str(d),str(c)) + bcolors.ENDC)

	def addPoints(self, cards):
		'''
		cards are a list of cards of a trick
		'''
		for card in cards:
			self.points += card.points

	def passCards(self):
		#cardsPassed is a list of three cards
		cardsPassed = random.sample((self.hand), 3)

		return cardsPassed


	def playCard(self, suit):

		'''
		suit = ["None", "Hearts","Spades","Diamonds","Clubs"]
		None indicates this player is first to play
		'''

		#uses arbitrary nature of set to pop an random element
		#edit this for playing agent

		if Poker.PokerCard('Clubs',2) in self.hand:
			#Always play the 2 of clubs first
			card_played = Poker.PokerCard('Clubs',2)
			self.hand.discard(card_played)
			self.suits[card_played.suit].remove(card_played)

		elif suit == 'None':
			#if the player is the first to play
			card_played = self.hand.pop()
			self.suits[card_played.suit].remove(card_played)
		else:
			#randomly play a card from the correct suit
			suit_cards = [card for card in self.hand if card.suit == suit]
			#print("{} : {}".format(self.name, list(map(lambda x : str(x) , suit_cards))))

			if len(suit_cards) > 0:
				card_played = random.choice(suit_cards)
				self.hand.remove(card_played)
				self.suits[card_played.suit].remove(card_played)
				
			else:
				#print('No more {} left!'.format(suit))
				card_played = self.hand.pop()
				self.suits[card_played.suit].remove(card_played)			

		#print(str(card_played))
		return card_played

class HumanPlayer(Player):
	def playCard(self,suit, hBroken):

		mySuit = ''
		myNumber = None

		while(mySuit not in ['Hearts','Spades','Clubs','Diamonds'] or myNumber not in range(2,15)):

			mySuit = input("Which card would you like to play? Enter suit. \n")
			myNumber = int (input("Enter number [2 - 14]. \n"))

		#Decide which card to send to the server
		card_played = Poker.PokerCard(mySuit, myNumber)

		#send to server
		print("Card Sent")
		return card_played

class RandomPlayer(Player):


	def playCard(self, suit, hBroken):

		'''
		suit = ["None", "Hearts","Spades","Diamonds","Clubs"]
		hBroken = If Hearts was broken
		None indicates this player is first to play
		'''

		if Poker.PokerCard('Clubs',2) in self.hand:
			#Always play the 2 of clubs first
			return Poker.PokerCard('Clubs',2)

		elif suit == 'None':
			#if the player is the first to play
			card_played = random.sample((self.hand), 1)[0]

			#Loop to make sure we don't get play a heart without it being broken
			if hBroken == False:
				while (card_played.suit == 'Hearts' and len(self.suits["Hearts"]) < len(self.hand)):
					card_played = random.sample((self.hand), 1)[0]


		else:
			#randomly play a card from the correct suit
			suit_cards = [card for card in self.hand if card.suit == suit]

			if len(suit_cards) > 0:
				card_played = random.sample(suit_cards , 1)[0]
				
			else:
				#print('No more {} left!'.format(suit))
				card_played = random.sample((self.hand), 1)[0]			

		#print(str(card_played))
		return card_played
