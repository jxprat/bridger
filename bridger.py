# *********************************************************************
# System imports ...
# *********************************************************************
import random
import sys
import time
import pygame
from pygame.locals import *

# *********************************************************************
# Constants ...
# *********************************************************************
CARD_WIDTH = 79  # Width of the cards
CARD_HEIGHT = 123  # Height of the cards
BID_CARD_WIDTH = 26  # Width of the bidding cards
BID_CARD_HEIGHT = 36  # Height of the bidding cards

VISUAL_CARD_WIDTH = 15  # Width shown when cards are agrupped

INTERNAL_MARGIN = 15
EXTERNAL_MARGIN = 20

DELTA_SPACE = 120
DELTA_SELECT = 15  # Card lift up this pixels ...

CARD_RULER_WIDTH = VISUAL_CARD_WIDTH * 12 + CARD_WIDTH + INTERNAL_MARGIN * 2
CARD_RULER_HEIGHT = 40

WINDOW_WIDTH = 2 * EXTERNAL_MARGIN + 6 * INTERNAL_MARGIN + 3 * (12 * VISUAL_CARD_WIDTH + CARD_WIDTH)
WINDOW_HEIGHT = 2 * EXTERNAL_MARGIN + 3 * CARD_HEIGHT + 2 * DELTA_SPACE

BG_COLOR = (21, 77, 0)  # Background color of the table
VUL_COLOR = (203, 0, 0)  # Color when vulnerable
NOT_VUL_COLOR = (203, 203, 203)  # Color when not vulnerable
OTHER_BG = (153, 204, 204)

LOGO_ICO = "images/bridger.png"

SUITS = ('C', 'S', 'H', 'D')  # Clubs, Spades, Hearts, Daemonds
RANK = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 14, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'C': 0, 'D': 20, 'H': 40, 'S': 60}
CARDINAL_POINTS = ('N', 'E', 'S', 'W')

# *********************************************************************
# Class Card
# *********************************************************************
class Card:
    def __init__(self, suit, rank):
        if((suit.upper() in SUITS) and (rank.upper() in RANK)):
            self.suit = suit.upper()
            self.rank = rank.upper()
        else:
            self.suit = None
            self.rank = None

    def GetSuit(self):
        return self.suit

    def GetRank(self):
        return self.rank

    def __gt__(self, other):
        if (self.suit == other.suit):
            return VALUES[self.rank] > VALUES[other.rank]
        else:
            return self.suit > other.suit

    def __str__(self):
        return self.suit + self.rank


# *********************************************************************
# Class Deck
# *********************************************************************
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANK:
                self.deck.append(Card(suit, rank))

    def Shuffle(self):
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


# *********************************************************************
# Class Hand
# *********************************************************************
class Hand:
    def __init__(self):
        self.HandCards = []
        self.Spades = []
        self.Hearts = []
        self.Diamonds = []
        self.Clubs = []

    def AddCard(self, card):
        suit = card.GetSuit()
        self.HandCards.append(card)
        if (suit == 'S'):
            self.Spades.append(card)
        elif (suit == 'H'):
            self.Hearts.append(card)
        elif (suit == 'D'):
            self.Diamonds.append(card)
        else:
            self.Clubs.append(card)

    def RemoveCard(self, card):
        suit = card.GetSuit()
        self.HandCards.remove(card)
        if (suit == 'S'):
            self.Spades.remove(card)
        elif (suit == 'H'):
            self.Hearts.remove(card)
        elif (suit == 'D'):
            self.Diamonds.remove(card)
        else:
            self.Clubs.remove(card)

    def Reorder(self, suit1, suit2, suit3, suit4):
        OrderedHand = Hand()
        for i in range(0, len(self.HandCards)):
            if (self.HaveSuit(suit1)):
                card = self.MaxOfSuit(suit1)
            elif (self.HaveSuit(suit2)):
                card = self.MaxOfSuit(suit2)
            elif (self.HaveSuit(suit3)):
                card = self.MaxOfSuit(suit3)
            elif (self.HaveSuit(suit4)):
                card = self.MaxOfSuit(suit4)
            self.RemoveCard(card)
            OrderedHand.AddCard(card)
        self.HandCards = OrderedHand

    def HaveSuit(self, suit):
        if (suit == 'S'):
            return (len(self.Spades) > 0)
        elif (suit == 'H'):
            return (len(self.Hearts) > 0)
        elif (suit == 'D'):
            return (len(self.Diamonds) > 0)
        else:
            return (len(self.Clubs) > 0)

    def MaxOfSuit(self, suit):
        max_card = False
        for card in self.HandCards:
            if (card.GetSuit() == suit):
                if (max_card == False):
                    max_card = card
                else:
                    if (card > max_card):
                        max_card = card
        return max_card

    def MinOfSuit(self, suit):
        min_card = False
        for card in self.HandCards:
            if (card.GetSuit() == suit):
                if (min_card == False):
                    min_card = card
                else:
                    if (card < min_card):
                        min_card = card
        return min_card

    def KillCard(self, card2kill):
        sel_card = False

    def __str__(self):
        hand_str = ""
        for card in self.HandCards:
            hand_str += str(card) + " "
        return hand_str

    def __iter__(self):
        return iter(self.HandCards)

    def __getitem__(self, ndx):
        return self.HandCards[ndx]

    def __len__(self):
        return len(self.HandCards)


# *********************************************************************
# Class BridgePlayer
# *********************************************************************
class BridgePlayer:
    def __init__(self, Pos):
        self.PlayerPosition = Pos  # N, E, S or W

    def set_Position(self, Pos):
        self.PlayerPosition = Pos

    def get_Position(self):
        return self.PlayerPosition

    def set_Vulnerability(self, v):
        self.PlayerVulnerability = v

    def isVulnerable(self):
        return self.PlayerVulnerability

    def set_Hand(self, newHand):
        self.PlayerHand = newHand

    def get_Hand(self):
        return self.PlayerHand

    def set_Dealer(self, d):
        self.isPlayerDealer = d

    def isDealer(self):
        return self.isPlayerDealer


# *********************************************************************
# Class Bridge
# *********************************************************************
class Bridge:
    def __init__(self):
        self.bridgeDeck = Deck()
        self.bridgeDeck.Shuffle()
        self.Dealer = None  # N, E, S, W
        self.Vulnerability = []  # N, E, S, W Also could be an empty list, meaning no vulnerability
        self.Turn = None  # N -> E -> S -> W -> N -> ...
        self.northP = BridgePlayer('N')
        self.eastP = BridgePlayer('E')
        self.SouthP = BridgePlayer('S')
        self.westP = BridgePlayer('W')

    def NewGame(self, deal, vul):
        if (len(self.bridgeDeck != 52)):
            self.bridgeDeck = Deck()
            self.bridgeDeck.Shuffle()

# -----------------------------------------------------
# SetDealer
# IN        None
# OUT       None
# -----------------------------------------------------
    def SetDealer(self, deal):
        if (deal in CARDINAL_POINTS):
            self.Dealer = deal
        else:
            self.Dealer = None

# -----------------------------------------------------
# NextPlayer
# IN        None
# OUT       char (N, E, S, W, None) Next Player Turn
# -----------------------------------------------------
    def NextPlayer(self):
        if (self.Turn == 'N'):
            self.Turn = 'E'
        elif (self.Turn == 'E'):
            self.Turn = 'S'
        elif (self.Turn == 'S'):
            self.Turn == 'W'
        elif (self.Turn == 'W'):
            self.Turn = 'N'
        else:
            self.Turn = None
        return self.Turn

# -----------------------------------------------------
# GetTurn
#   IN      None
#   OUT     char (N, E, S, W, None) Next Player Turn
# -----------------------------------------------------
    def GetTurn(self):
        return self.Turn

# -----------------------------------------------------
# DealCards
#   IN      None
#   OUT     None
# -----------------------------------------------------
    def DealCards(self):
        if (self.Dealer != None):
            self.northP
            for i in range(0, 13):
                pass


# *********************************************************************
# Functions ...
# *********************************************************************
def load_image(filename, transparent=False):
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        raise SystemExit, message
    image = image.convert()
    if transparent:
        color = image.get_at((0, 0))
        image.set_colorkey(color, RLEACCEL)
    return image

def card2filename(card):
    filename = 'images/cards/'
    rank = card.GetRank().lower()
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
    suit = card.GetSuit().lower()
    return filename + rank + suit + '.gif'

def draw_hand(scr, posX, posY, hand, visible, color):
    delta = 0
    for card in hand:
        if (visible):  # Show card
            img = load_image(card2filename(card))
        else:  # Show back
            img = load_image("images/cards/back.gif")
        scr.blit(img, (posX + delta, posY))
        delta += VISUAL_CARD_WIDTH
    pygame.draw.rect(scr, color, [posX - INTERNAL_MARGIN, posY + CARD_HEIGHT - CARD_RULER_HEIGHT, CARD_RULER_WIDTH, CARD_RULER_HEIGHT], 0)
    mytext = FontGame.render("North", True, (0, 0, 0))
    scr.blit(mytext, (posX, posY + CARD_HEIGHT - CARD_RULER_HEIGHT + 5))
    pygame.display.flip()

def GetIndexCardFromMouse(posX, player_hand):
    if (len(player_hand) == 1):
        ndx = 0
    else:
        ndx = (posX - EXTERNAL_MARGIN - CARD_RULER_WIDTH - INTERNAL_MARGIN) / VISUAL_CARD_WIDTH
        if (ndx > 12):
            ndx = 12
    return ndx

def CardUp(scr, ndx, player_hand):
    posX = EXTERNAL_MARGIN + CARD_RULER_WIDTH + INTERNAL_MARGIN
    posY = WINDOW_HEIGHT - EXTERNAL_MARGIN - CARD_HEIGHT
    scr.fill(BG_COLOR, (posX - INTERNAL_MARGIN, posY - DELTA_SELECT, CARD_RULER_WIDTH, CARD_HEIGHT))
    delta = 0
    for card in player_hand:
        img = load_image(card2filename(card))
        if (delta == ndx and ndx != -1):
            scr.blit(img, (posX + delta * VISUAL_CARD_WIDTH, posY - DELTA_SELECT))
        else:
            scr.blit(img, (posX + delta * VISUAL_CARD_WIDTH, posY))
        delta += 1
    pygame.draw.rect(scr, VUL_COLOR, [posX - INTERNAL_MARGIN, posY + CARD_HEIGHT - CARD_RULER_HEIGHT, CARD_RULER_WIDTH, CARD_RULER_HEIGHT], 0)
    mytext = FontGame.render("North", True, (0, 0, 0))
    scr.blit(mytext, (posX, posY + CARD_HEIGHT - CARD_RULER_HEIGHT + 5))
    pygame.display.flip()

def DrawBiddingWindow(scr, posX, posY):
    deltaY = 0
    for i in range(1, 8):
        deltaX = 0
        for j in ("c", "d", "h", "s", "nt"):
            # filename = "0" + str(i) + j + ".gif"
            filename = "02c.png"
            img = load_image("images/bidding/" + filename, False)
            scr.blit(img, (posX + deltaX * BID_CARD_WIDTH, posY + deltaY * BID_CARD_HEIGHT))
            deltaX += 1
        deltaY += 1
    pygame.display.flip()

def DrawGeneralInfoWindow(scr):
    pygame.draw.rect(scr, (180, 180, 180), [EXTERNAL_MARGIN, EXTERNAL_MARGIN, CARD_RULER_WIDTH, CARD_HEIGHT], 1)

# *********************************************************************
# Main program ...
# *********************************************************************
print 'Hello Bridger!'
print 'Window is ', WINDOW_WIDTH, WINDOW_HEIGHT
deck = Deck()
deck.Shuffle()
print deck

Game = Bridge()

NorthPlayerHand = Hand()
EastPlayerHand = Hand()
SouthPlayerHand = Hand()
WestPlayerHand = Hand()

for i in range(1, 14):
    NorthPlayerHand.AddCard(deck.deal_card())
    EastPlayerHand.AddCard(deck.deal_card())
    SouthPlayerHand.AddCard(deck.deal_card())
    WestPlayerHand.AddCard(deck.deal_card())

print "North Hand: ", NorthPlayerHand
print "East Hand: ", EastPlayerHand
print "South Hand: ", SouthPlayerHand
print "West Hand: ", WestPlayerHand

print "Reordering al hands ... "
NorthPlayerHand.Reorder("S", "H", "C", "D")
EastPlayerHand.Reorder("S", "H", "C", "D")
SouthPlayerHand.Reorder("S", "H", "C", "D")
WestPlayerHand.Reorder("S", "H", "C", "D")

print "New North Hand: ", NorthPlayerHand
print "New East Hand: ", EastPlayerHand
print "New South Hand: ", SouthPlayerHand
print "New West Hand: ", WestPlayerHand

print "Max/Min of Suits ..."
print "Max of Spades: ", SouthPlayerHand.MaxOfSuit("S")
print "Max of Hearts: ", SouthPlayerHand.MaxOfSuit("H")
print "Min of Diamonds: ", SouthPlayerHand.MinOfSuit("D")
print "Min of Clubs: ", SouthPlayerHand.MinOfSuit("C")

# *********************************************************************
# Graphic part ...
# *********************************************************************
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # , pygame.RESIZABLE)
pygame.display.set_caption("Bridger!")
pygame.display.set_icon(pygame.image.load(LOGO_ICO))
pygame.font.init()

screen.fill(BG_COLOR)
FontGame = pygame.font.SysFont("None", 36, True)  # Default sysfont, size=12 and bold
## logo_image = pygame.transform.scale(load_image("images/Bridger Logo.png"), (100, 75))
## screen.blit(logo_image, (WINDOW_WIDTH / 2 - 50 , WINDOW_HEIGHT / 2 - 37))

draw_hand(screen, EXTERNAL_MARGIN + 3 * INTERNAL_MARGIN + 12 * VISUAL_CARD_WIDTH + CARD_WIDTH, EXTERNAL_MARGIN, NorthPlayerHand, False, VUL_COLOR)
draw_hand(screen, WINDOW_WIDTH - EXTERNAL_MARGIN - INTERNAL_MARGIN - CARD_WIDTH - 12 * VISUAL_CARD_WIDTH, EXTERNAL_MARGIN + CARD_HEIGHT + DELTA_SPACE, EastPlayerHand, False, NOT_VUL_COLOR)
draw_hand(screen, EXTERNAL_MARGIN + 3 * INTERNAL_MARGIN + 12 * VISUAL_CARD_WIDTH + CARD_WIDTH, WINDOW_HEIGHT - EXTERNAL_MARGIN - CARD_HEIGHT, SouthPlayerHand, True, VUL_COLOR)
draw_hand(screen, EXTERNAL_MARGIN + INTERNAL_MARGIN, EXTERNAL_MARGIN + CARD_HEIGHT + DELTA_SPACE, WestPlayerHand, False, NOT_VUL_COLOR)

while True:
    for event in pygame.event.get():
        if (event.type == QUIT):
            sys.exit(0)
        elif (event.type == KEYDOWN):  # Key pressed ...
            keys = pygame.key.get_pressed()  # Witch key?
            if keys[K_n]:  # Test key in keys[]
                deck = Deck()
                deck.Shuffle()
                NorthPlayerHand = Hand()
                EastPlayerHand = Hand()
                SouthPlayerHand = Hand()
                WestPlayerHand = Hand()

                for i in range(0, 13):
                    NorthPlayerHand.AddCard(deck.deal_card())
                    EastPlayerHand.AddCard(deck.deal_card())
                    SouthPlayerHand.AddCard(deck.deal_card())
                    WestPlayerHand.AddCard(deck.deal_card())

                NorthPlayerHand.Reorder("S", "H", "C", "D")
                EastPlayerHand.Reorder("S", "H", "C", "D")
                SouthPlayerHand.Reorder("S", "H", "C", "D")
                WestPlayerHand.Reorder("S", "H", "C", "D")

                draw_hand(screen, EXTERNAL_MARGIN + 3 * INTERNAL_MARGIN + 12 * VISUAL_CARD_WIDTH + CARD_WIDTH, EXTERNAL_MARGIN, NorthPlayerHand, False, VUL_COLOR)
                draw_hand(screen, WINDOW_WIDTH - EXTERNAL_MARGIN - INTERNAL_MARGIN - CARD_WIDTH - 12 * VISUAL_CARD_WIDTH, EXTERNAL_MARGIN + CARD_HEIGHT + DELTA_SPACE, EastPlayerHand, False, NOT_VUL_COLOR)
                draw_hand(screen, EXTERNAL_MARGIN + 3 * INTERNAL_MARGIN + 12 * VISUAL_CARD_WIDTH + CARD_WIDTH, WINDOW_HEIGHT - EXTERNAL_MARGIN - CARD_HEIGHT, SouthPlayerHand, True, VUL_COLOR)
                draw_hand(screen, EXTERNAL_MARGIN + INTERNAL_MARGIN, EXTERNAL_MARGIN + CARD_HEIGHT + DELTA_SPACE, WestPlayerHand, False, NOT_VUL_COLOR)

                print "New North Hand: ", NorthPlayerHand
                print "New East Hand: ", EastPlayerHand
                print "New South Hand: ", SouthPlayerHand
                print "New West Hand: ", WestPlayerHand

                print "Max/Min of Suits ..."
                print "Max of Spades: ", SouthPlayerHand.MaxOfSuit("S")
                print "Max of Hearts: ", SouthPlayerHand.MaxOfSuit("H")
                print "Min of Diamonds: ", SouthPlayerHand.MinOfSuit("D")
                print "Min of Clubs: ", SouthPlayerHand.MinOfSuit("C")
                
                print "Have Spades? ", SouthPlayerHand.HaveSuit("S")
                print "Have Hearts? ", SouthPlayerHand.HaveSuit("H")
                print "Have Diamonds? ", SouthPlayerHand.HaveSuit("D")
                print "Have Clubs? ", SouthPlayerHand.HaveSuit("C")

            elif keys[K_h]:
                draw_hand(screen, EXTERNAL_MARGIN + 3 * INTERNAL_MARGIN + 12 * VISUAL_CARD_WIDTH + CARD_WIDTH, EXTERNAL_MARGIN, NorthPlayerHand, False, VUL_COLOR)
                draw_hand(screen, WINDOW_WIDTH - EXTERNAL_MARGIN - INTERNAL_MARGIN - CARD_WIDTH - 12 * VISUAL_CARD_WIDTH, EXTERNAL_MARGIN + CARD_HEIGHT + DELTA_SPACE, EastPlayerHand, False, NOT_VUL_COLOR)
                draw_hand(screen, EXTERNAL_MARGIN + INTERNAL_MARGIN, EXTERNAL_MARGIN + CARD_HEIGHT + DELTA_SPACE, WestPlayerHand, False, NOT_VUL_COLOR)
            elif keys[K_s]:
                draw_hand(screen, EXTERNAL_MARGIN + 3 * INTERNAL_MARGIN + 12 * VISUAL_CARD_WIDTH + CARD_WIDTH, EXTERNAL_MARGIN, NorthPlayerHand, True, VUL_COLOR)
                draw_hand(screen, WINDOW_WIDTH - EXTERNAL_MARGIN - INTERNAL_MARGIN - CARD_WIDTH - 12 * VISUAL_CARD_WIDTH, EXTERNAL_MARGIN + CARD_HEIGHT + DELTA_SPACE, EastPlayerHand, True, NOT_VUL_COLOR)
                draw_hand(screen, EXTERNAL_MARGIN + INTERNAL_MARGIN, EXTERNAL_MARGIN + CARD_HEIGHT + DELTA_SPACE, WestPlayerHand, True, NOT_VUL_COLOR)
        elif (event.type == KEYUP):  # Key released ...
            if event.key == pygame.K_q:
                pass  # sys.exit(0)
        elif (event.type == MOUSEBUTTONDOWN):
            print "Mouse button pressed ..."
            print pygame.mouse.get_pressed()
            print pygame.mouse.get_pos()
        elif (event.type == MOUSEBUTTONUP):
            print "Mouse button released ..."
            print pygame.mouse.get_pressed()
            print pygame.mouse.get_pos()
        else:  # Other events ...
            pass

    # Contol where the mouse is to lift card up/down
    mouse_pos = pygame.mouse.get_pos()
    initY = WINDOW_HEIGHT - EXTERNAL_MARGIN - CARD_HEIGHT
    finalY = WINDOW_HEIGHT - EXTERNAL_MARGIN - CARD_RULER_HEIGHT
    initX = EXTERNAL_MARGIN + CARD_RULER_WIDTH + INTERNAL_MARGIN
    finalX = initX + (len(SouthPlayerHand) - 1) * VISUAL_CARD_WIDTH + CARD_WIDTH
    if ((mouse_pos[1] > initY) and (mouse_pos[1] < finalY) and (mouse_pos[0] > initX) and (mouse_pos[0] < finalX)):
        ndx = GetIndexCardFromMouse(mouse_pos[0], SouthPlayerHand)
        CardUp(screen, ndx, SouthPlayerHand)
    else:
        CardUp(screen, -1, SouthPlayerHand)

    # Draw the Bidding Control Window ...
    DrawBiddingWindow(screen, WINDOW_WIDTH - EXTERNAL_MARGIN - CARD_RULER_WIDTH + INTERNAL_MARGIN, WINDOW_HEIGHT - EXTERNAL_MARGIN - CARD_HEIGHT)

    # Draw the General Info Window ...
    DrawGeneralInfoWindow(screen)
