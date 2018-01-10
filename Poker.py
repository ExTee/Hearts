import random

random.seed(100)

class PokerCard:

	def __init__(self, suit:str, number:int):
		'''
		suit: 	"Hearts","Spades","Diamonds","Clubs"
		number:	2 to 14
		'''
		self.suit = suit
		self.number = number

	def __str__(self):

		mydict = {
		2:	'Two',
		3:	'Three',
		4:	'Four',
		5:	'Five',
		6:	'Six',
		7:	'Seven',
		8:	'Eight',
		9:	'Nine',
		10:	'Ten',
		11: 'Jack',
		12: 'Queen',
		13: 'King',
		14: 'Ace'
		}

		return( mydict[self.number] + " Of " + self.suit)

	def __hash__(self):
		#hash using the name of the card
		return hash(str(self))

	def __eq__(self,other):
		#equality (two cards that are the same are the same card)
		return (
			self.suit == other.suit and
			self.number == other.number
			)

class Deck:
	'''
	Poker Deck consisting of 52 cards
	'''

	def __init__(self):
		self.cards = []

		for s in ["Hearts","Spades","Diamonds","Clubs"]:
			for n in range(2, 15):
				self.cards.append(PokerCard(s,n))

		#self.shuffle()

	def shuffle(self):
		random.shuffle(self.cards)

	def __str__(self):
		for card in self.cards:
			print(str(card))

		return ''

