import collections
import Poker
import random
import itertools
import time
from bcolors import bcolors
from Player import Player, HumanPlayer, RandomPlayer

#random.seed(120)

#where to save the games
FILEPATH = './games/' + str(time.time()) + '.txt'


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

		#Leaderboard
		'''self.Leaderboard = {
								playerNames[0]: 0,
								playerNames[1]: 0,
								playerNames[2]: 0,
								playerNames[3]: 0,
								}'''

		#output file
		self.OUTPUT_FILE = open(FILEPATH,'w')

		#Variable to determine if hearts have been broken
		self.HeartsBroken = False



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
		a
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

	def showState(self, player):
		#Show the game state to the player
		print('\nYour Hand:')
		player.printCards()
		print()


	def getPassedCards(self, player):
		#This function checks if a player passed the right cards at the beginning of the game

		Legal = False
		attemptedPass = None

		while (Legal == False):
			Legal = True

			#list containing cards that player wants to pass
			attemptedPass = player.passCards()

			#Player needs to pass 3 cards
			if (len(attemptedPass) != 3):
				Legal = False

			#all three cards need to be in the player's hand
			for card in attemptedPass:
				if card not in player.hand:
					Legal = False

		#We've asserted that the pass is legal, we will update the cards

		#First remove from the player's hand
		for card in attemptedPass:
			player.hand.remove(card)
			player.suits[card.suit].remove(card)

		return attemptedPass


	#Sends current board state to player
	def getPlay(self, player, suit = 'None'):
		#Obtains the play returned by player

		if isinstance(player, HumanPlayer):
			print("Your turn, Human")
			self.showState(player)

		Legal = False
		attemptedPlay = None

		#Check if the play is a valid play
		while(Legal == False):

			Legal = True

			attemptedPlay = player.playCard(suit = suit, hBroken = self.HeartsBroken)

			#Check if Hearts broken
			if self.HeartsBroken == False:
				if suit == 'None':
					if attemptedPlay.suit == 'Hearts':
						#This checks the case where the player ONLY has hearts in hand
						if len(player.suits["Hearts"]) < len(player.hand):
							print("Cancelled hearts")
							Legal = False

			#Check if player did not start with 2 of clubs
			if Poker.PokerCard('Clubs',2) in player.hand:
				if attemptedPlay != Poker.PokerCard('Clubs',2):
					Legal = False

			#Check if player has the card
			if (attemptedPlay not in player.hand):
				Legal = False

			#If card is not in starting suit, check if player has any cards from starting suit
			if attemptedPlay.suit != suit and suit != 'None':
					if len(player.suits[suit]) != 0:
						Legal = False

			if not Legal:
				print("Play is Illegal, Please choose another play")

		#At this point, the play is legal, and the game is updated.

		#Remove card from player's hand
		player.hand.discard(attemptedPlay)
		player.suits[attemptedPlay.suit].remove(attemptedPlay)

		#Hearts have been broken if someone plays a heart card
		if attemptedPlay.suit == 'Hearts':
			self.HeartsBroken = True

		#returns the card played for point accumulation
		return attemptedPlay


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

			#The first card sets the suit for the trick
			if self.players.index(player) == 0:			
				played_card = self.getPlay(player, suit = 'None')
				trick_suit = played_card.suit
				print("Current Trick suit: {}".format(trick_suit))
			else:
				played_card = self.getPlay(player, suit = trick_suit)				

			trick_points += played_card.points
			trick_data.append((player, played_card))

			print("Player {} played : ".format(player) + bcolors.FAIL + "{}".format(played_card) + bcolors.ENDC)
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

		print("Player {} won the trick".format(trick_winner[0]))
		self.OUTPUT_FILE.write("Player {} won the trick".format(trick_winner[0]))

		#print("\nScores : \n\tA: {}\n\tB: {}\n\tC: {}\n\tD: {}".format(self.playerNames[0].points, self.playerNames[1].points, self.playerNames[2].points, self.playerNames[3].points))

		return trick_winner[0]

	def playMatch(self, matchNumber):
		'''
		Shuffle the deck before each match
		Deal the cards to players
		Show players' cards
		'''
		self.Deck.shuffle()
		self.dealDeck()
		self.printPlayerCards()
		self.HeartsBroken = False

		#Passing Phase
		t = matchNumber % 4

		'''
		if t == 0:
			#Pass left
		elif t == 1:
			#pass right
		elif t == 2:
			#pass across
		else:
			#no pass
		'''


		#First Trick is played by the 2 of clubs
		#print(self.Deck.cards.index(Poker.PokerCard('Clubs',2)))
		starting_player = self.players[int(self.Deck.cards.index(Poker.PokerCard('Clubs',2)) / 13)]
		
		winner = starting_player

		for trick in range(1,14):

			print( bcolors.HEADER + '\nTrick number {}'.format(trick) + bcolors.ENDC)
			self.OUTPUT_FILE.write('Trick number {}'.format(trick))

			winner = self.playTrick(winner)

		print("\nScores : \n\tA: {}\n\tB: {}\n\tC: {}\n\tD: {}".format(self.playerNames[0].points, self.playerNames[1].points, self.playerNames[2].points, self.playerNames[3].points))

	def playGame(self):

		gameOver = False

		matchNumber = 0

		while (not gameOver):
			self.playMatch(matchNumber)

			for player in self.playerNames:
				if player.points >= 100:
					gameOver = True

			matchNumber += 1

		finalScores = sorted([(p.name, p.points) for p in self.playerNames] , key = lambda x: x[1])

		#Show the Final Scores
		print("\nFinal Scores : \n\t1st Place: {} - {}\n\t2nd Place: {} - {}\n\t3rd Place: {} - {}\n\t4th Place: {} - {}".format(
			finalScores[0][0],finalScores[0][1],
			finalScores[1][0],finalScores[1][1],
			finalScores[2][0],finalScores[2][1],
			finalScores[3][0],finalScores[3][1],
			))




def main():
	myPlayers = [RandomPlayer('A'),RandomPlayer('B'),RandomPlayer('C'),RandomPlayer('D')]
	myGame = HeartsGame(myPlayers)

	myGame.playGame()

if __name__ == '__main__':
	main()