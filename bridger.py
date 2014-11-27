# System imports ...
# ---------------------------------------------------------------------
import random
import sys
import time
import pygame
from pygame.locals import *
# ---------------------------------------------------------------------

# Constants ...
# ---------------------------------------------------------------------
CARD_WIDTH = 79             # Width of the card
CARD_HEIGHT = 123           # Height of th e card

VISUAL_CARD_WIDTH = 15      # Width shown when cards are agrupped
VISUAL_CARD_HEIGHT = 82     # Height shown when cards are in hand

INTERNAL_MARGIN = 10
EXTERNAL_MARGIN = 20

DELTA_SPACE = 15

WINDOW_WIDTH = 800 #2 * EXTERNAL_MARGIN + 2 * VISUAL_CARD_HEIGHT + 2 * DELTA_SPACE + 12 * VISUAL_CARD_WIDTH + CARD_WIDTH
WINDOW_HEIGHT = 600 #2 * EXTERNAL_MARGIN + 2 * CARD_HEIGHT + 2 * INTERNAL_MARGIN + 12 * VISUAL_CARD_WIDTH + CARD_WIDTH

BG_COLOR = (21, 77, 0)			# Background color of the table
CARD_BAR = (203, 203, 203)		# Background color of the rectangle card bar
VUL_COLOR = (203, 0, 0)			# Color when vulnerable
NOT_VUL_COLOR = (0, 0, 0)		# Color when not vulnerable
OTHER_BG = (153, 204, 204)

LOGO_ICO = "images/bridger.png"

SUITS = ('C', 'S', 'H', 'D')  # Clubs, Spades, Hearts, Daemonds
RANK = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 14, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'C': 0, 'D': 20, 'H': 40, 'S': 60}

# Class Card
# ---------------------------------------------------------------------
class Card:
    def __init__(self, suit, rank):
        self.suit = suit.upper()
        self.rank = rank.upper()

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def __gt__(self,other):
        if (self.suit == other.suit):
            return VALUES [self.rank] > VALUES[other.rank]
        else:
            return self.suit > other.suit

    def __str__(self):
        return self.suit + self.rank
# ---------------------------------------------------------------------

# Class Deck
# ---------------------------------------------------------------------
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANK:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop(-1)

    def __str__(self):
        deck_str = ""
        for card in self.deck:
            deck_str += str(card) + " "
        return deck_str

    def __iter__(self):
        return iter(self.deck)
# ---------------------------------------------------------------------

# Class Hand
# ---------------------------------------------------------------------
class Hand:
    def __init__(self):
        self.hand_cards = []

    def add_card(self, card):
        self.hand_cards.append(card)

    def remove_card(self, card):
        if (card in self.hand_cards):
            self.hand_cards.remove(card)
        else:
            # Error ...
            pass

    def max(self):
        if (len(self.hand_cards) > 0):
            max_card = self.hand_cards[0]
            for card in self.hand_cards:
                if (card > max_card):
                    max_card = card
            return max_card
        else:
            return False

    def reorder(self):
        ordered_hand = Hand()
        for i in range(0,13):
            card = self.max()
            self.remove_card(card)
            ordered_hand.add_card(card)
        self.hand_cards = ordered_hand.hand_cards

    def __str__(self):
        hand_str = ""
        for card in self.hand_cards:
            hand_str += str(card) + " "
        return hand_str

    def __iter__(self):
        return iter(self.hand_cards)

    def __getitem__(self, ndx):
        return self.hand_cards[ndx]
# ---------------------------------------------------------------------

# Class BridgePlayer
# ---------------------------------------------------------------------
class BridgePlayer:
	def __init__(self, Pos, isVul, Hand, isDealer):
		self.Position = Pos
		self.MyHand = Hand()
		self.Vulnerability = isVul
		self.Dealer = isDealer

	def set_Position(self, Pos):
		self.Position = Pos

	def get_Position(self):
		return self.Position

	def set_Vulnerability(self, v):
		self.Vulnerability = v

	def isVulnerable(self):
		return self.Vulnerability

	def set_Hand(self, newHand):
		self.MyHand = newHand

	def set_Dealer(self, d):
		self.Dealer = d

	def isDealer(self):
		return self.isDealer
# ---------------------------------------------------------------------

# Functions ...
# ---------------------------------------------------------------------
def load_image(filename, transparent=False):
    try: image = pygame.image.load(filename)
    except pygame.error, message:
        raise SystemExit, message
    image = image.convert()
    if transparent:
         color = image.get_at((0,0))
         image.set_colorkey(color, RLEACCEL)
    return image

def card2filename(card):
	filename = 'images/cards/'
	rank = card.get_rank().lower()
	if (rank == 'a'):
		rank = '01'
	elif (rank == 't'):
		rank = '10'
	elif (rank == 'j'):
		rank = '11'
	elif (rank == 'q'):
		rank = '12'
	elif (rank == 'k'):
		rank = '13'
	else:
		rank = '0' + rank
	suit = card.get_suit().lower()
	return filename + rank + suit + '.gif'

def draw_hand(scr, posX, posY, hand, visible):
	deltaX = 0
	for card in hand:
		if (visible):
			img = load_image(card2filename(card))
		else:
			img = load_image("images/cards/back.gif")
		scr.blit(img,(posX + deltaX, posY))
		deltaX += VISUAL_CARD_WIDTH
	pygame.display.flip()
# ---------------------------------------------------------------------

# Main program ...
# ---------------------------------------------------------------------
print 'Hello Bridger!'
print 'Window is ', WINDOW_WIDTH, WINDOW_HEIGHT
deck = Deck()
deck.shuffle()
print deck

NorthPlayerHand = Hand()
EastPlayerHand = Hand()
SouthPlayerHand = Hand()
WestPlayerHand = Hand()

for i in range(1,14):
    NorthPlayerHand.add_card(deck.deal_card())
    EastPlayerHand.add_card(deck.deal_card())
    SouthPlayerHand.add_card(deck.deal_card())
    WestPlayerHand.add_card(deck.deal_card())

print "North Hand: ", NorthPlayerHand
print "East Hand: ", EastPlayerHand
print "South Hand: ", SouthPlayerHand
print "West Hand: ", WestPlayerHand

print "Reordering al hands ... "
NorthPlayerHand.reorder()
EastPlayerHand.reorder()
SouthPlayerHand.reorder()
WestPlayerHand.reorder()

print "New North Hand: ", NorthPlayerHand
print "New East Hand: ", EastPlayerHand
print "New South Hand: ", SouthPlayerHand
print "New West Hand: ", WestPlayerHand
# ---------------------------------------------------------------------

# Graphic part ...
# ---------------------------------------------------------------------
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Bridger!")
pygame.display.set_icon(pygame.image.load(LOGO_ICO))

screen.fill(BG_COLOR)
## logo_image = pygame.transform.scale(load_image("images/Bridger Logo.png"), (100, 75))
## screen.blit(logo_image, (WINDOW_WIDTH / 2 - 50 , WINDOW_HEIGHT / 2 - 37))

draw_hand(screen, 300, 50, NorthPlayerHand, True)
pygame.draw.rect(screen, CARD_BAR, [300 - INTERNAL_MARGIN , 133, VISUAL_CARD_WIDTH*12+CARD_WIDTH+INTERNAL_MARGIN*2, 41], 0)
draw_hand(screen, 400, 250, EastPlayerHand, False)
draw_hand(screen, 300, 450, SouthPlayerHand, True)
draw_hand(screen, 50, 250, WestPlayerHand, False)

while True:
	for event in pygame.event.get():
		if (event.type == QUIT):
			sys.exit(0)
		elif (event.type == KEYDOWN):			# Key pressed ...
			keys = pygame.key.get_pressed()		# Wich key?
			if keys[K_n]:						# Test key in keys[]
				deck = Deck()
				deck.shuffle()
				NorthPlayerHand = Hand()
				EastPlayerHand = Hand()
				SouthPlayerHand = Hand()
				WestPlayerHand = Hand()

				for i in range(0,13):
				    NorthPlayerHand.add_card(deck.deal_card())
				    EastPlayerHand.add_card(deck.deal_card())
				    SouthPlayerHand.add_card(deck.deal_card())
				    WestPlayerHand.add_card(deck.deal_card())

				NorthPlayerHand.reorder()
				EastPlayerHand.reorder()
				SouthPlayerHand.reorder()
				WestPlayerHand.reorder()

				draw_hand(screen, 300, 50, NorthPlayerHand, False)
				pygame.draw.rect(screen, CARD_BAR, [300 - INTERNAL_MARGIN , 133, VISUAL_CARD_WIDTH*12+CARD_WIDTH+INTERNAL_MARGIN*2, 41], 0)
				draw_hand(screen, 400, 250, EastPlayerHand, False)
				draw_hand(screen, 300, 450, SouthPlayerHand, True)
				draw_hand(screen, 50, 250, WestPlayerHand, False)
			elif keys[K_h]:
				draw_hand(screen, 300, 50, NorthPlayerHand, False)
			elif keys[K_s]:
				draw_hand(screen, 300, 50, NorthPlayerHand, True)
		elif (event.type == KEYUP):
			pass 	# Key released ...
		elif (event.type == MOUSEBUTTONDOWN):
			print "Mouse button pressed ..."
			print pygame.mouse.get_pressed()
			print pygame.mouse.get_pos()
		elif (event.type == MOUSEBUTTONUP):
			print "Mouse button released ..."
			print pygame.mouse.get_pressed()
			print pygame.mouse.get_pos()
		else:
			pass
    	#pygame.display.update()     # Podem passar una porcio de la pantalla per actualitzar aquest recuadre,
    	#pygame.display.flip()        # sino funciona igual que aquesta altra funcio

