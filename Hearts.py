import collections
import Poker
import random
import itertools
import time

random.seed(120)

#where to save the games
FILEPATH = './games/' + str(time.time()) + '.txt'

class Player():
	def __init__(self, name:str):
		self.hand = set()
		self.name = name
		self.points = 0

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

	def addPoints(self, cards):
		'''
		cards are a list of cards of a trick
		'''
		for card in cards:
			self.points += card.points


	def playCard(self, suit):

		'''
		suit = ["None", "Hearts","Spades","Diamonds","Clubs"]
		None indicates this player is first to play
		'''

		#uses arbitrary nature of set to pop an random element
		#edit this for playing agent

		if Poker.PokerCard('Clubs',2) in self.hand:
			#Always play the 2 of clubs first
			self.hand.discard(Poker.PokerCard('Clubs',2))
			return Poker.PokerCard('Clubs',2)
		elif suit == 'None':
			#if the player is the first to play
			card_played = self.hand.pop()
		else:
			#randomly play a card from the correct suit
			suit_cards = [card for card in self.hand if card.suit == suit]
			#print("{} : {}".format(self.name, list(map(lambda x : str(x) , suit_cards))))

			if len(suit_cards) > 0:
				card_played = random.choice(suit_cards)
				self.hand.remove(card_played)
				
			else:
				#print('No more {} left!'.format(suit))
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

		#List of all players (This is needed because deque will be modified)
		self.playerNames = players

		self.Deck = Poker.Deck()
		self.players = collections.deque(players,4)

		#output file
		self.OUTPUT_FILE = open(FILEPATH,'w')



		#shuffle the deck before play
		#self.Deck.shuffle()
		print("Hearts game starts with {} players".format(len(self.players)))

		#Show who's playing
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
		for aPlayer in self.playerNames:
			print('Player {} has :'.format(aPlayer.name))
			aPlayer.printCards()
			print()

	def showState(self,player):
		#Show the game state to the player
		player.printCards()

	def getPlay(self,player, suit = 'None'):
		#Obtains the play returned by player
		#Check if the play is a valid play

		return player.playCard(suit = suit)

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

		#print("Index: " + str(self.players.index(winningPlayer)))
		self.players.rotate(-self.players.index(winningPlayer))

		#holds the cards and suit played this trick
		trick_suit = None
		trick_data = []
		trick_points = 0

		for player in self.players:
			

			#self.showState(player)

			#The first card sets the suit for the trick
			if self.players.index(player) == 0:			
				played_card = self.getPlay(player, suit = 'None')
				trick_suit = played_card.suit
				print("Current Trick suit: {}".format(trick_suit))
			else:
				played_card = self.getPlay(player, suit = trick_suit)				

			trick_points += played_card.points
			trick_data.append((player, played_card))

			print("Player {} played : {}".format(player, played_card))
			self.OUTPUT_FILE.write("Player {} played : {}".format(player, played_card))


 
			#update which card was the highest
			if self.players.index(player) == 0:
				trick_winner = (player, played_card)
			else:
				if not (trick_winner[1].bigger_than(played_card)):
					#	the new card is bigger than the winner so far
					trick_winner = (player, played_card)

		#Player who won the tricks adds up the points
		#print("Player {} took : {}".format(trick_winner[0], list(map(lambda x : str(x), [a[1] for a in trick_data]))))
		#trick_winner[0].addPoints([a[1] for a in trick_data])
		trick_winner[0].points += trick_points

		#print("Player {} won the trick".format(trick_winner[0]))
		self.OUTPUT_FILE.write("Player {} won the trick".format(trick_winner[0]))

		#print("\nScores : \n\tA: {}\n\tB: {}\n\tC: {}\n\tD: {}".format(self.playerNames[0].points, self.playerNames[1].points, self.playerNames[2].points, self.playerNames[3].points))

		return trick_winner[0]

	def playMatch(self):


		'''
		Shuffle the deck before each match
		Deal the cards to players
		Show players' cards
		'''
		self.Deck.shuffle()
		self.dealDeck()
		self.printPlayerCards()

		#First Trick is played by the 2 of clubs
		#print(self.Deck.cards.index(Poker.PokerCard('Clubs',2)))
		starting_player = self.players[int(self.Deck.cards.index(Poker.PokerCard('Clubs',2)) / 13)]
		
		winner = starting_player

		for trick in range(1,14):

			print('\nTrick number {}'.format(trick))
			self.OUTPUT_FILE.write('Trick number {}'.format(trick))

			winner = self.playTrick(winner)

		print("\nScores : \n\tA: {}\n\tB: {}\n\tC: {}\n\tD: {}".format(self.playerNames[0].points, self.playerNames[1].points, self.playerNames[2].points, self.playerNames[3].points))

	def playGame(self):

		gameOver = False

		while (not gameOver):
			self.playMatch()

			for player in self.playerNames:
				if player.points >= 100:
					gameOver = True

		finalScores = sorted([(p.name, p.points) for p in self.playerNames] , key = lambda x: x[1])

		print("\nFinal Scores : \n\t1st Place: {} - {}\n\t2nd Place: {} - {}\n\t3rd Place: {} - {}\n\t4th Place: {} - {}".format(
			finalScores[0][0],finalScores[0][1],
			finalScores[1][0],finalScores[1][1],
			finalScores[2][0],finalScores[2][1],
			finalScores[3][0],finalScores[3][1],
			))




def main():
	myPlayers = [Player('A'),Player('B'),Player('C'),Player('D')]
	myGame = HeartsGame(myPlayers)

	myGame.playGame()

if __name__ == '__main__':
	main()