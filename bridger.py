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
CARDINAL_POINTS = ('N', 'E', 'S', 'W')

VALUES = {'A': 14, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'C': 0, 'D': 20, 'H': 40, 'S': 60}

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

    def IsHonor(self):
        return (self.rank == 'A' or self.rank == 'K' or self.rank == 'Q' or self.rank == 'J')

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

    def DealCard(self):
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
#        self.Spades = 0
#        self.Hearts = 0
#        self.Diamonds = 0
#        self.Clubs = 0

    def AddCard(self, card):
        self.HandCards.append(card)

    def RemoveCard(self, card):
        self.HandCards.remove(card)

# -----------------------------------------------------
# Order
# IN        
# OUT       Ordered Hand using Spades, Hearts, Diamonds and Clubs suit order
# -----------------------------------------------------
    def Order(self):
        for i in range(len(self.HandCards)):
            for j in range(len(self.HandCards) - 1 - i):
                if(self.HandCards[j] < self.HandCards[j + 1]):
                    self.HandCards[j], self.HandCards[j + 1] = self.HandCards[j + 1], self.HandCards[j]

    def ReOrder(self, s1, s2, s3, s4):
        new_hand = Hand()
        new_hand = self.CardsOfSuit(s1)
        new_hand.HandCards += self.CardsOfSuit(s2)
        new_hand.HandCards += self.CardsOfSuit(s3)
        new_hand.HandCards += self.CardsOfSuit(s4)
        self.HandCards = new_hand.HandCards

# -----------------------------------------------------
# HaveSuit
# IN        char (S, H, D, C) selected suit
# OUT       Integer representing the number of cards of the suit
# -----------------------------------------------------
    def HowMany(self, suit):
        retval = 0
        for card in self.HandCards:
            if (card.GetSuit() == suit):
                retval += 1
        return retval

# -----------------------------------------------------
# MaxOfSuit
# IN        char (S, H, D, C) selected suit
# OUT       Card/Boolean (the greater card of the suit)
# -----------------------------------------------------
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

# -----------------------------------------------------
# MinOfSuit
# IN        char (S, H, D, C) selected suit
# OUT       Card/Boolean (the smaller card of the suit)
# -----------------------------------------------------
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

    def KillCard(self, card_to_kill):
        ret_card = False
        suit = card_to_kill.GetSuit()
        for card in self.HandCards:
            if(card.GetSuit() == suit):
                if(card > card_to_kill):
                    ret_card = card
        return ret_card

    def CardsOfSuit(self, suit):
        retval = Hand()
        for card in self.HandCards:
            if(card.GetSuit() == suit):
                retval.AddCard(card)
        return retval

    def HonorPoints(self):
        hp = 0
        for card in self.HandCards:
            rank = card.GetRank()
            if(rank == 'A'):
                hp += 4
            elif(rank == 'K'):
                hp += 3
            elif(rank == 'Q'):
                hp += 2
            elif(rank == 'J'):
                hp += 1
        return hp

### Retocar porque hay que tener mas cosas en consideracion (que no sea triunfo, honores secos, ...)
    def DistributionPoints(self):
        dp = 0
        for s in SUITS:
            if(self.HowMany(s) == 0):
                dp += 3
            elif(self.HowMany(s) == 1):
                dp += 2
            elif(self.HowMany(s) == 2):
                dp += 1
        return dp

    def IsBalanced(self):
        retval = False
        aux = 0
        spades = self.HowMany('S')
        hearts = self.HowMany('H')
        diamonds = self.HowMany('D')
        clubs = self.HowMany('C')
        if(spades > 1 and hearts > 1 and diamonds > 1 and clubs > 1): # No hay fallos ni semifallos
            if(spades > 2 and hearts > 2 and diamonds > 2 and clubs > 2): # No hay doubletones ...
                retval = True
            else:
                aux += (spades == 2)
                aux += (hearts == 2)
                aux += (diamonds == 2)
                aux += (clubs == 2)
                if(aux == 1):
                    retval = True
        return retval

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
        self.Vulnerability = False
        self.PlayerHand = None
        self.isPlayerDealer = False

    def set_Position(self, Pos):
        self.PlayerPosition = Pos

    def GetPosition(self):
        return self.PlayerPosition

    def SetVulnerability(self, v):
        self.Vulnerability = v

    def IsVulnerable(self):
        return self.Vulnerability

    def set_Hand(self, newHand):
        self.PlayerHand = newHand

    def get_Hand(self):
        return self.PlayerHand

    def set_Dealer(self, d):
        self.isPlayerDealer = d

    def IsDealer(self):
        return self.isPlayerDealer


# *********************************************************************
# Class Bridge
# *********************************************************************
class Bridge:
    def __init__(self):
        self.bridgeDeck = Deck()
        self.Dealer = None  # N, E, S, W
        self.Turn = None  # N -> E -> S -> W -> N -> ...
        self.northP = BridgePlayer('N')
        self.eastP = BridgePlayer('E')
        self.southP = BridgePlayer('S')
        self.westP = BridgePlayer('W')
        # Bridge Game should have a final contract, who win it, ...
        self.Bazas = None # 1, 2, 3, ... 7
        self.Triump = None # C, D, H, S, NT 

    def NewGame(self, dealer, vul):
        self.bridgeDeck = Deck()
        self.bridgeDeck.Shuffle()
        self.Dealer = dealer
        self.Turn = dealer
        self.deal_cards()
        self.northP.PlayerHand.Order()
        self.eastP.PlayerHand.Order()
        self.southP.PlayerHand.Order()
        self.southP.PlayerHand.ReOrder('S', 'H', 'C', 'D')
        self.westP.PlayerHand.Order()
        self.northP.SetVulnerability(vul[0])
        self.eastP.SetVulnerability(vul[1])
        self.southP.SetVulnerability(vul[2])
        self.westP.SetVulnerability(vul[3])
        if(dealer == 'N'):
            self.northP.set_Dealer(True)
        elif(dealer == 'E'):
            self.eastP.set_Dealer(True)
        elif(dealer == 'S'):
            self.southP.set_Dealer(True)
        elif(dealer == 'W'):
            self.westP.set_Dealer(True)
        self.Contract = None
        self.Triump = None

# -----------------------------------------------------
# SetDealer
# IN        char (N, E, S, W, None) Player Position
# OUT       Boolean
# -----------------------------------------------------
    def SetDealer(self, deal):
        retval = False
        if (deal in CARDINAL_POINTS):
            retval = True
            self.Dealer = deal
            if(deal == 'N'):
            	self.northP.set_Dealer(True)
            elif(deal == 'E'):
            	self.eastP.set_Dealer(True)
            elif(deal == 'S'):
            	self.southP.set_Dealer(True)
            else:
            	self.westP.set_Dealer(True)
        else:
            self.Dealer = None
        return retval

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
# SetContract
#   IN      Integer (1, 2, 3. ... 7) Representing the number of "bazas" to win
#   OUT     
# -----------------------------------------------------
def SetContract(self, bazas):
    self.Bazas = bazas

def GetContract(self):
    return self.Bazas

# -----------------------------------------------------
# SetTriump
#   IN      char (S, H, D, C, NT)
#   OUT     
# -----------------------------------------------------
def SetTriump(self, tr):
    self.Triump = tr

def GetTriump(self):
    return self.Triump

# -----------------------------------------------------
# DealCards
#   IN      None
#   OUT     None
# -----------------------------------------------------
    def deal_cards(self):
        retval = False
        if (self.Dealer != None):
            H1 = Hand()
            H2 = Hand()
            H3 = Hand()
            H4 = Hand()
            for i in range(0, 13):
                H1.AddCard(self.bridgeDeck.DealCard())
                H2.AddCard(self.bridgeDeck.DealCard())
                H3.AddCard(self.bridgeDeck.DealCard())
                H4.AddCard(self.bridgeDeck.DealCard())
            if(self.Dealer == 'N'):
                self.eastP.set_Hand(H1)
                self.southP.set_Hand(H2)
                self.westP.set_Hand(H3)
                self.northP.set_Hand(H4)
            elif(self.Dealer == 'E'):
                self.southP.set_Hand(H1)
                self.westP.set_Hand(H2)
                self.northP.set_Hand(H3)
                self.eastP.set_Hand(H4)
            elif(self.Dealer == 'S'):
                self.westP.set_Hand(H1)
                self.northP.set_Hand(H2)
                self.eastP.set_Hand(H3)
                self.southP.set_Hand(H4)
            else:
                self.northP.set_Hand(H1)
                self.eastP.set_Hand(H2)
                self.southP.set_Hand(H3)
                self.westP.set_Hand(H4)
            retval = True
        return retval

    def GetPlayer(self, player_pos):
        retval = False
        if(player_pos == 'N'):
            retval = self.northP
        elif(player_pos == 'E'):
            retval = self.eastP
        elif(player_pos == 'S'):
            retval = self.southP
        elif(player_pos == 'W'):
            retval = self.westP
        return retval

# GetHand
# IN        char (N, E, S, W, None) Player Position
# OUT       Hand
# -----------------------------------------------------
    def GetHand(self, player_pos):
        if(player_pos == 'N'):
            return self.northP.get_Hand()
        elif(player_pos == 'E'):
            return self.eastP.get_Hand()
        elif(player_pos == 'S'):
            return self.southP.get_Hand()
        else:
            return self.westP.get_Hand()

    def set_hand(self,player_pos, hand):
        if(player_pos == 'N'):
            self.northP.set_Hand(hand)
        elif(player_pos == 'E'):
            self.eastP.set_Hand(hand)
        elif(player_pos == 'S'):
            self.southP.set_Hand(hand)
        else:
            self.westP.set_Hand(hand)

    def GetDeck(self):
        return self.bridgeDeck

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

def DrawHand(scr, posX, posY, player, visible):
    delta = 0
    for card in player.get_Hand():
        if (visible):  # Show card
            img = load_image(card2filename(card))
        else:  # Show back
            img = load_image("images/cards/back.gif")
        scr.blit(img, (posX + delta, posY))
        delta += VISUAL_CARD_WIDTH
    if(player.GetPosition() == 'N'):
        player_pos = 'North'
        if(player.IsDealer()):
            player_pos += ' (D)'
    elif(player.GetPosition() == 'E'):
        player_pos = 'East'
        if(player.IsDealer()):
            player_pos += ' (D)'
    elif(player.GetPosition() == 'S'):
        player_pos = 'South'
        if(player.IsDealer()):
            player_pos += ' (D)'
    elif(player.GetPosition() == 'W'):
        player_pos = 'West'
        if(player.IsDealer()):
            player_pos += ' (D)'
    if(player.IsVulnerable()):
        color = VUL_COLOR
    else:
        color = NOT_VUL_COLOR
    pygame.draw.rect(scr, color, [posX - INTERNAL_MARGIN, posY + CARD_HEIGHT - CARD_RULER_HEIGHT, CARD_RULER_WIDTH, CARD_RULER_HEIGHT], 0)
    mytext = FontGame.render(player_pos, True, (0, 0, 0))
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

def CardUp(scr, ndx, player):
    posX = EXTERNAL_MARGIN + CARD_RULER_WIDTH + INTERNAL_MARGIN
    posY = WINDOW_HEIGHT - EXTERNAL_MARGIN - CARD_HEIGHT
    scr.fill(BG_COLOR, (posX - INTERNAL_MARGIN, posY - DELTA_SELECT, CARD_RULER_WIDTH, CARD_HEIGHT))
    delta = 0
    for card in player.get_Hand():
        img = load_image(card2filename(card))
        if (delta == ndx and ndx != -1):
            scr.blit(img, (posX + delta * VISUAL_CARD_WIDTH, posY - DELTA_SELECT))
        else:
            scr.blit(img, (posX + delta * VISUAL_CARD_WIDTH, posY))
        delta += 1
    if(player.IsVulnerable()):
        color = VUL_COLOR
    else:
        color = NOT_VUL_COLOR
    pygame.draw.rect(scr, color, [posX - INTERNAL_MARGIN, posY + CARD_HEIGHT - CARD_RULER_HEIGHT, CARD_RULER_WIDTH, CARD_RULER_HEIGHT], 0)
    mytext = FontGame.render("South", True, (0, 0, 0))
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
# print 'Hello Bridger!'
# print 'Window is ', WINDOW_WIDTH, WINDOW_HEIGHT
# deck = Deck()
# deck.Shuffle()
# print deck

# NorthPlayerHand = Hand()
# EastPlayerHand = Hand()
# SouthPlayerHand = Hand()
# WestPlayerHand = Hand()

# for i in range(1, 14):
#     NorthPlayerHand.AddCard(deck.DealCard())
#     EastPlayerHand.AddCard(deck.DealCard())
#     SouthPlayerHand.AddCard(deck.DealCard())
#     WestPlayerHand.AddCard(deck.DealCard())

# print "North Hand: ", NorthPlayerHand
# print "East Hand: ", EastPlayerHand
# print "South Hand: ", SouthPlayerHand
# print "West Hand: ", WestPlayerHand

# print "Reordering al hands ... "
# NorthPlayerHand.Reorder("S", "H", "C", "D")
# EastPlayerHand.Reorder("S", "H", "C", "D")
# SouthPlayerHand.Reorder("S", "H", "C", "D")
# WestPlayerHand.Reorder("S", "H", "C", "D")

# print "New North Hand: ", NorthPlayerHand
# print "New East Hand: ", EastPlayerHand
# print "New South Hand: ", SouthPlayerHand
# print "New West Hand: ", WestPlayerHand

# print "Max/Min of Suits ..."
# print "Max of Spades: ", SouthPlayerHand.MaxOfSuit("S")
# print "Max of Hearts: ", SouthPlayerHand.MaxOfSuit("H")
# print "Min of Diamonds: ", SouthPlayerHand.MinOfSuit("D")
# print "Min of Clubs: ", SouthPlayerHand.MinOfSuit("C")

# *********************************************************************
# Testing new core classes ...
# *********************************************************************

# print "*********************************************************************"
# Game = Bridge()
# Game.NewGame('N')
# print "Deck: ", Game.GetDeck()
# print "Turn: ", Game.GetTurn()
# print "North Hand: ", Game.GetHand('N')
# print "East Hand: ", Game.GetHand('E')
# print "South Hand: ", Game.GetHand('S')
# print "West Hand: ", Game.GetHand('W')
# print

# my_hand = Game.GetHand('S')
# print "My Hand: \t\t", my_hand
# my_hand.ReOrder('S', 'H', 'C', 'D')
# print "Reordered Hand: \t", my_hand
# print "Is Balanced? ", my_hand.IsBalanced()
# print "Honor Points: ", my_hand.HonorPoints()
# for suit in SUITS:
#     print "Num cards: ", my_hand.HowMany(suit)
#     print "Cads of suit: ", my_hand.CardsOfSuit(suit)
#     print "Max of : ", my_hand.MaxOfSuit(suit)
#     print "Min of : ", my_hand.MinOfSuit(suit)

# print
# card_to_beat = Card('S', '8')
# print "Kill Card ", card_to_beat, my_hand.KillCard(card_to_beat)

# print
# print "*********************************************************************"


# *********************************************************************
# Main Bridge Init ...
# *********************************************************************
Game = Bridge()
Game.NewGame('N', [False, False, False, False])
# *********************************************************************
# Graphic part ...
# *********************************************************************
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # , pygame.RESIZABLE)
pygame.display.set_caption("Bridger!")
pygame.display.set_icon(pygame.image.load(LOGO_ICO))
pygame.font.init()

screen.fill(BG_COLOR)
FontGame = pygame.font.SysFont("None", 36, True)  # Default sysfont, size=12 and bold

DrawHand(screen, EXTERNAL_MARGIN + 3 * INTERNAL_MARGIN + 12 * VISUAL_CARD_WIDTH + CARD_WIDTH, EXTERNAL_MARGIN, Game.GetPlayer('N'), False)
DrawHand(screen, WINDOW_WIDTH - EXTERNAL_MARGIN - INTERNAL_MARGIN - CARD_WIDTH - 12 * VISUAL_CARD_WIDTH, EXTERNAL_MARGIN + CARD_HEIGHT + DELTA_SPACE, Game.GetPlayer('E'), False)
DrawHand(screen, EXTERNAL_MARGIN + 3 * INTERNAL_MARGIN + 12 * VISUAL_CARD_WIDTH + CARD_WIDTH, WINDOW_HEIGHT - EXTERNAL_MARGIN - CARD_HEIGHT, Game.GetPlayer('S'), True)
DrawHand(screen, EXTERNAL_MARGIN + INTERNAL_MARGIN, EXTERNAL_MARGIN + CARD_HEIGHT + DELTA_SPACE, Game.GetPlayer('W'), False)

while True:
    pass
    for event in pygame.event.get():
        if (event.type == QUIT):
            sys.exit(0)
        elif (event.type == KEYDOWN):  # Key pressed ...
            keys = pygame.key.get_pressed()  # Witch key?
            if keys[K_n]:  # Test key in keys[]
                Game.NewGame('N', [False, True, False, True])

                DrawHand(screen, EXTERNAL_MARGIN + 3 * INTERNAL_MARGIN + 12 * VISUAL_CARD_WIDTH + CARD_WIDTH, EXTERNAL_MARGIN, Game.GetPlayer('N'), False)
                DrawHand(screen, WINDOW_WIDTH - EXTERNAL_MARGIN - INTERNAL_MARGIN - CARD_WIDTH - 12 * VISUAL_CARD_WIDTH, EXTERNAL_MARGIN + CARD_HEIGHT + DELTA_SPACE, Game.GetPlayer('E'), False)
                DrawHand(screen, EXTERNAL_MARGIN + 3 * INTERNAL_MARGIN + 12 * VISUAL_CARD_WIDTH + CARD_WIDTH, WINDOW_HEIGHT - EXTERNAL_MARGIN - CARD_HEIGHT, Game.GetPlayer('S'), True)
                DrawHand(screen, EXTERNAL_MARGIN + INTERNAL_MARGIN, EXTERNAL_MARGIN + CARD_HEIGHT + DELTA_SPACE, Game.GetPlayer('W'), False)

            elif keys[K_h]:
                DrawHand(screen, EXTERNAL_MARGIN + 3 * INTERNAL_MARGIN + 12 * VISUAL_CARD_WIDTH + CARD_WIDTH, EXTERNAL_MARGIN, Game.GetPlayer('N'), False)
                DrawHand(screen, WINDOW_WIDTH - EXTERNAL_MARGIN - INTERNAL_MARGIN - CARD_WIDTH - 12 * VISUAL_CARD_WIDTH, EXTERNAL_MARGIN + CARD_HEIGHT + DELTA_SPACE, Game.GetPlayer('E'), False)
                DrawHand(screen, EXTERNAL_MARGIN + INTERNAL_MARGIN, EXTERNAL_MARGIN + CARD_HEIGHT + DELTA_SPACE, Game.GetPlayer('W'), False)
            elif keys[K_s]:
                DrawHand(screen, EXTERNAL_MARGIN + 3 * INTERNAL_MARGIN + 12 * VISUAL_CARD_WIDTH + CARD_WIDTH, EXTERNAL_MARGIN, Game.GetPlayer('N'), True)
                DrawHand(screen, WINDOW_WIDTH - EXTERNAL_MARGIN - INTERNAL_MARGIN - CARD_WIDTH - 12 * VISUAL_CARD_WIDTH, EXTERNAL_MARGIN + CARD_HEIGHT + DELTA_SPACE, Game.GetPlayer('E'), True)
                DrawHand(screen, EXTERNAL_MARGIN + INTERNAL_MARGIN, EXTERNAL_MARGIN + CARD_HEIGHT + DELTA_SPACE, Game.GetPlayer('W'), True)

        elif (event.type == KEYUP):  # Key released ...
            if event.key == pygame.K_q:
                sys.exit(0)
#         elif (event.type == MOUSEBUTTONDOWN):
#             print "Mouse button pressed ..."
#             print pygame.mouse.get_pressed()
#             print pygame.mouse.get_pos()
#         elif (event.type == MOUSEBUTTONUP):
#             print "Mouse button released ..."
#             print pygame.mouse.get_pressed()
#             print pygame.mouse.get_pos()
        else:  # Other events ...
            pass

    # Contol where the mouse is to lift card up/down
    mouse_pos = pygame.mouse.get_pos()
    initY = WINDOW_HEIGHT - EXTERNAL_MARGIN - CARD_HEIGHT
    finalY = WINDOW_HEIGHT - EXTERNAL_MARGIN - CARD_RULER_HEIGHT
    initX = EXTERNAL_MARGIN + CARD_RULER_WIDTH + INTERNAL_MARGIN
    finalX = initX + (len(Game.GetHand('S')) - 1) * VISUAL_CARD_WIDTH + CARD_WIDTH
    if ((mouse_pos[1] > initY) and (mouse_pos[1] < finalY) and (mouse_pos[0] > initX) and (mouse_pos[0] < finalX)):
        ndx = GetIndexCardFromMouse(mouse_pos[0], Game.GetHand('S'))
        CardUp(screen, ndx, Game.GetPlayer('S'))
    else:
        CardUp(screen, -1, Game.GetPlayer('S'))

    # Draw the Bidding Control Window ...
    ##DrawBiddingWindow(screen, WINDOW_WIDTH - EXTERNAL_MARGIN - CARD_RULER_WIDTH + INTERNAL_MARGIN, WINDOW_HEIGHT - EXTERNAL_MARGIN - CARD_HEIGHT)

    # Draw the General Info Window ...
    ##DrawGeneralInfoWindow(screen)
