import pyCardDeck
import collections
from typing import List
import time
from pyCardDeck.cards import PokerCard




class Player:
	#initialize a player with a hand and a name
	def __init__(self, name: str):
		self.hand = []
		self.name = name

	def __str__(self):
		return self.name

	def sort_hand(self):



class HeartsGame:

	def __init__(self, players: List[Player]):
		self.deck = pyCardDeck.Deck()
		self.deck.load_standard_deck()
		self.players = collections.deque(players, 4)		#only 4 players are allowed
		self.scores = {}

		print("Hearts game starts with {} players".format(len(self.players)))
		
		for player in self.players:
			print("Player {} : {}".format(players.index(player) +1, player.name))


	def Hearts(self):
		print("Game is Starting...")
		time.sleep(5)

		print("Shuffling deck ...")
		self.deck.shuffle()

		print("Dealing the cards.")
		self.deal()

		for player in self.players:
			#each player gets a turn
			self.play(player)
		else:
			print("The round is over, counting points")
			self.count_points()		

	def deal(self):
		'''
		Deals 13 cards to each player
		'''

		for _ in range(13):
			for p in self.players:
				newcard = self.deck.draw()
				p.hand.append(newcard)
				print("Dealt {} the {}.".format(p.name, str(newcard)))


	def play_round(self, winning_player):
		'''
		Each round is played by 4 cards, one from each player
		1. Start from previous winner
		2. go clockwise
		'''
		#rotate the deque so that the winning_player plays first
		#Example: [1,2,3,4] - winning player is 3.
		#index of 3 is 2
		#rotate 3 -> [3,4,1,2]
		for player in players.rotate(d.index(winning_player)+1):
			self.play(player)


	def play(self, player):
		'''
		A player's turn

		0. Show player the state of the game
		1. Check what is the suit.
		2. Let player select which card to play
		3. If card is legal, play it, otherwise prompt again
		'''
		print("\nYou are player: {}".format(player.name))
		
		spades, diamonds, hearts, clubs = [],[],[],[]
		for card in player.hand:
			if(card.suit == "Spades"):
				spades.append(card)
			elif(card.suit == "Diamonds"):
				diamonds.append(card)
			elif(card.suit == "Hearts"):
				hearts.append(card)
			else:
				clubs.append(card)





		#todo: number of cards in others' hands



	def count_points(self):
		print("hi")


def main():
	print("We're Running the program")

	players = [Player("A"), Player("B"), Player("C"), Player("D")]
	game = HeartsGame(players)
	game.Hearts()



if __name__ == "__main__":
	main()