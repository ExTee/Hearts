import collections
import Poker
import random
import itertools
import time

random.seed(120)

class Player():
	def __init__(self, name:str):
		self.hand = set()
		self.name = name

	def __str__(self):
		return self.name

	def setCards(self, cards):
		'''
		Receives cards from the deck
		'''

		if len(cards) != 13:
			raise ValueError('Player {} received {} cards instead of 13 cards! Abort.'.format(self.name, len(cards)))
		else:
			self.hand = set(cards)

	def printCards(self):
		'''
		Shows the player's hand
		'''
		for card in self.hand:
			print(card)

	def playCard(self):

		#uses arbitrary nature of set to pop an random element
		#edit this for playing agent

		card_played = self.hand.pop()

		#print(str(card_played))
		return card_played


class HeartsGame():
	'''
	A Hearts Game consists of multiple MATCHES.
	Each match consists of thirteen TRICKS.
	At the End of each match, points are tallied and added.
	The Game ends when a player reaches 100 points.
	'''

	


	def __init__(self, players:list):

		self.Deck = Poker.Deck()
		self.players = collections.deque(players,4)

		#output file
		self.OUTPUT_FILE = open(str(time.time()) + '.txt','w')

		#shuffle the deck before play
		self.Deck.shuffle()
		print("Hearts game starts with {} players".format(len(self.players)))

		for player in self.players:
			print("Player {} : {}".format(players.index(player) +1, player.name))

	def dealDeck(self):
		'''
		Player 1: cards 0 to 12
		Player 2: cards 13 to 25
		Player 3: cards 26 to 38
		Player 4: cards 39 to 51

		This has essentially the same effect as distributing cards one by one, it speeds up computation
		'''
		a = 0
		b = 13
		for aPlayer in self.players:
			aPlayer.setCards(self.Deck.cards[a:b])

			#record which player has which cards
			temp_cards = ",".join(map(lambda x : str(x), self.Deck.cards[a:b]))
			self.OUTPUT_FILE.write(str(aPlayer) + ": " + temp_cards + '\n')

			#go to next player
			a += 13
			b += 13

	def printPlayerCards(self):
		'''
		Prints each player's hand
		'''
		for aPlayer in self.players:
			print('Player {} has :'.format(aPlayer.name))
			aPlayer.printCards()
			print()

	def showState(self,player):
		#Show the game state to the player
		player.printCards()

	def getPlay(self,player):
		#Obtains the play returned by player
		return player.playCard()

	def playTrick(self, winningPlayer):
		'''
		Each round is played by 4 cards, one from each player
		1. Start from previous winner
		2. go clockwise
		'''
		#rotate the deque so that the winning_player plays first
		#Example: [1,2,3,4] - winning player is 3.
		#index of 3 is 2
		#rotate 3 -> [3,4,1,2]

		print("Index: " + str(self.players.index(winningPlayer)))
		self.players.rotate(-self.players.index(winningPlayer))

		for player in self.players:
			#self.showState(player)
			played_card = self.getPlay(player)
			print("Player {} played : {}".format(player, played_card))

	def playMatch(self):
		#First Trick is played by the 2 of clubs
		print(self.Deck.cards.index(Poker.PokerCard('Clubs',2)))
		starting_player = self.players[int(self.Deck.cards.index(Poker.PokerCard('Clubs',2)) / 13)]
		print(str(starting_player))



def main():
	myPlayers = [Player('A'),Player('B'),Player('C'),Player('D')]
	myGame = HeartsGame(myPlayers)

	myGame.dealDeck()
	myGame.printPlayerCards()
	#myGame.playTrick(myPlayers[3])
	myGame.playMatch()

if __name__ == '__main__':
	main()