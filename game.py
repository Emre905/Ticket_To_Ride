# Create turn based Ticket to Ride game for 2 players 
import sys 
import networkx as nx 
import numpy as np 
import random
from collections import deque
import time
from functions import VERTICES, EDGES, TICKETS, EDGES_DICT, POINT_EDGE_DICT, G, CITY_LOCATIONS
import functions as func
from Ui_windows.Ui_mainwindow import Ui_MainWindow 
from Ui_windows.Ui_widget_game_board import Ui_Form_Game_Board
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget


''' 
Too add: 
- Define a player's turn. its possible to select a ticket after selecting one card etc
- longest road point to functions.calculate_point()
- stations to functions

Issues:
1- set_ok_cancel_buttons() doesn't connect buttons to functions

rules were taken from https://www.ultraboardgames.com/ticket-to-ride/game-rules.php
number of cards were taken from https://boardgamegeek.com/wiki/page/Ticket_to_Ride_series
- 240 Colored Train Cars (48 each in Blue, Red, Green, Yellow & Black)
- 96 Train Cards (12 each in Red, Orange, Yellow, Green, Blue, Purple, Black & White)
- 14 Locomotive Wild Cards (Multicolored)
But I decided to make it all 14
'''

# set first game state
class Train_Cards:
    def __init__(self):
        self.cards : deque = deque(i for i in list('blue red green yellow black orange purple white rainbow'.split())*14)
        random.shuffle(self.cards)

class Destination_Tickets:
    def __init__(self):
        self.tickets : deque = deque(TICKETS)
        random.shuffle(self.tickets)

class Game:
    def __init__(self) -> None:
        self.train_cards : deque = Train_Cards().cards # train cards deck. new cards will be selected from here
        random.shuffle(self.train_cards)
        self.destination_tickets : deque = Destination_Tickets().tickets # destination tickets deck
        self.train_cards_player1 : list = [] # train cards player 1 has
        self.train_cards_player2 : list = [] # train cards player 2 has
        self.ticket_cards_player1 : list = [] # ticket cards player 1 has
        self.ticket_cards_player2 : list = [] # ticket cards player 2 has
        self.displayed_cards : list = [] # 5 cards that player selects train cards
        self.discarded_cards : deque = deque() # used cards goes to discarded pile
        self.taken_routes_player1 : list = [] # selected destination tickets by player1
        self.taken_routes_player2 : list = [] # selected destination tickets by player2
        self.trains_player1 : int = 45
        self.trains_player2 : int = 45
        self.player1_train_draw_count : int = 0 # will be 0, 1 or 2. number of cards player drew
        self.select_ticket_bool : bool = True # if player can select ticket now
        self.player = 'player1' # current player who has right to play
        self.round_count = 0 # which round it is
        self.GRAPH = G # get networkx graph
        self.selected_nodes : list = [] # will be the nodes player selects when he tries to claim a road
        self.select_color_bool = False
        self.run()
    
    # deal cards in the beginning of the game
    def deal_train_cards(self) -> None:
        for i in range(4):
            self.train_cards_player1.append(self.train_cards.popleft()) # deal top card to player 1
            self.train_cards_player2.append(self.train_cards.popleft()) # deal (new) top card to player 2

    # select cards to be displayed
    def display_train_cards(self) -> None:
        try: 
            if not self.displayed_cards: # if there are no displayed cards, reveal 5 cards
                while True:
                    for i in range(5):
                        top_card = self.train_cards.popleft() 
                        self.displayed_cards.append(top_card) # remove 5 top cards and append to displayed cards
                    
                    rainbow_count = self.displayed_cards.count('rainbow')
                    if rainbow_count >= 3: # if there are 3 rainbow cards reset displayed cards and repeat the process
                        self.discarded_cards.extend(self.displayed_cards) # discard displayed cards
                        self.displayed_cards : list = []
                    else:
                        break

            # this part will be used each time a player drew a card from displayerd cards. reveal top card and check for 3 rainbows
            else:
                top_card = self.train_cards.popleft() 
                self.displayed_cards.append(top_card) # remove top card and append to displayed cards
                
                rainbow_count = self.displayed_cards.count('rainbow')
                if rainbow_count >= 3:
                    self.discarded_cards.extend(self.displayed_cards) # add discarded cards to list
                    self.displayed_cards : list = []
                    self.display_train_cards()

        except IndexError: # when the train_cards is empty, pop will raise IndexError.
            self.discarded_cards.extend(self.displayed_cards) # add discarded cards to list
            self.displayed_cards : list = []
            self.reset_train_cards() # reset draw deck
            self.display_train_cards()

    # deal destination tickets to both players in the beginning of the game
    def deal_ticket_cards(self) -> list:
        self.ticket_options_player1 : list = []
        self.ticket_options_player2 : list = []
        for i in range(3):
            self.ticket_options_player1.append(self.destination_tickets.popleft()) # deal top card to player 1
            self.ticket_options_player2.append(self.destination_tickets.popleft()) # deal top card to player 2

    # draw a card from displayed cards
    def draw_train_card(self, player, card_index):
        if player == 'player1': # add corresponding card to player's deck
            self.train_cards_player1.append(self.displayed_cards[card_index])
        else:
            self.train_cards_player2.append(self.displayed_cards[card_index])

        self.displayed_cards.remove(self.displayed_cards[card_index]) # remove selected cards from display

        try:
            top_card = self.train_cards.popleft() # get the top card
            self.displayed_cards.insert(card_index, top_card) # remove top card and append to displayed cards

        except IndexError: # when the train_cards is empty, pop will raise IndexError.
            self.reset_train_cards() # reset draw deck
            top_card = self.train_cards.popleft()
            self.displayed_cards.insert(card_index, top_card)

    # draw a card from pile    
    def draw_train_card_random(self, player):
        try:
            if player == 'player1':
                self.train_cards_player1.append(self.train_cards.popleft()) # get top card
            else:
                self.train_cards_player2.append(self.train_cards.popleft())

        except IndexError: # when the train_cards is empty, pop will raise IndexError. reset the deck and repeat
            self.reset_train_cards() # reset draw deck
            if player == 'player1':
                self.train_cards_player1.append(self.train_cards.popleft())
            else:
                self.train_cards_player2.append(self.train_cards.popleft())

    # take discarded cards, shuffle and make it train cards 
    def reset_train_cards(self):
        self.train_cards : deque = self.discarded_cards.copy() # take all discarded cards and put on train cards
        random.shuffle(self.train_cards) # shuffle train cards
        self.discarded_cards : deque = deque([]) # reset discarded cards (they're back in the game)

    def get_next_player(self, player):
        # self.player = "player2" if player == "player1" else "player1"
        self.player = "player1" # test mode
        if player == "player1": # if it's 2nd player, increase round count
            self.round_count += 1 

    def deal_first_round(self) -> None:
        self.deal_train_cards() # deal 4 train cards to players in the beginning
        self.display_train_cards() # display top 5 cards to start the game
        self.deal_ticket_cards()

    def run(self):
        self.deal_first_round()

class MainWindow(QMainWindow):
    def __init__(self, game):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.boardWidget = Ui_Form_Game_Board()
        self.game = game

        self.setWindowState(QtCore.Qt.WindowMaximized) # get screen fullsize
        # self.resize(1366,768) #use if upper line doesn't work

        self.ui.stackedWidget.setCurrentWidget(self.ui.home)

        self.ui.button_instructions.clicked.connect(self.show_instructions)
        self.ui.button_play.clicked.connect(self.initUI)


    def show_instructions(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.instruction)

    def initUI(self):
        # remove first window
        self.ui.button_instructions.setParent(None)
        self.ui.button_play.setParent(None)

        self.boardWidgetContainer = QWidget()
        
        # Initialize the game board UI within this container
        self.boardWidget.setupUi(self.boardWidgetContainer, 
                                game.player, 
                                game.train_cards_player1, 
                                game.ticket_cards_player1,
                                game.displayed_cards,
                                game.ticket_options_player1,
                                game.select_ticket_bool,
                                len(game.train_cards),
                                game.GRAPH,
                                game.taken_routes_player1)
                                
        
        # Add the game board container to the stacked widget
        self.ui.stackedWidget.addWidget(self.boardWidgetContainer)
        
        # Switch to the game board UI
        self.ui.stackedWidget.setCurrentWidget(self.boardWidgetContainer)

        if game.round_count == 0: #display ticket selection at first round
            self.boardWidget.stackedWidget.setCurrentWidget(self.boardWidget.state_select_ticket)
        else:
            self.boardWidget.stackedWidget.setCurrentWidget(self.boardWidget.state_game)

        # at ticket select state check which buttons are pressed when ok button is hit
        self.boardWidget.button_ticket_option_okay.clicked.connect(self.button_ticket_draw_listener)

        # set actions taken from draw buttons clicked
        self.boardWidget.button_draw1.clicked.connect(lambda: self.draw_train_card(game.player, 0))
        self.boardWidget.button_draw2.clicked.connect(lambda: self.draw_train_card(game.player, 1))
        self.boardWidget.button_draw3.clicked.connect(lambda: self.draw_train_card(game.player, 2))
        self.boardWidget.button_draw4.clicked.connect(lambda: self.draw_train_card(game.player, 3))
        self.boardWidget.button_draw5.clicked.connect(lambda: self.draw_train_card(game.player, 4))
        self.boardWidget.button_draw_train.clicked.connect(lambda: self.draw_train_card_random(game.player))

        for node in self.boardWidget.button_map:
            self.boardWidget.button_map[node].toggled.connect(lambda checked, node=node: self.city_button_clicked(checked, node))

        # set actions to pressing draw (destination) tickets button
        self.boardWidget.button_draw_destination.clicked.connect(lambda: self.deal_ticket_cards_to_player(game.player))

        

    def deal_ticket_cards_to_player(self, player):
        if player == 'player1':
            game.ticket_options_player1 = []
            # deal top 3 cards to player
            for i in range(3):
                game.ticket_options_player1.append(game.destination_tickets.popleft()) # deal top card to player 1
        
        else: # if player2
            game.ticket_options_player2 = []
            # deal top 3 cards to player
            for i in range(3):
                game.ticket_options_player2.append(game.destination_tickets.popleft()) # deal top card to player 2

        self.initUI() #update board        
        self.boardWidget.stackedWidget.setCurrentWidget(self.boardWidget.state_select_ticket) # set ticket select state
        self.button_ticket_draw_listener() # set actions to buttons

    def city_button_clicked(self, checked, node):
        if checked: # button is selected
            game.selected_nodes.append(node) # add node

        else: # button is deselected
            game.selected_nodes.remove(node) # remove node

        # if 2 nodes are selected, check for the road
        if len(game.selected_nodes) == 2: # 2 nodes are selected
            # get if last 2 selected nodes are neighbors
            self.node1, self.node2 = game.selected_nodes[0], game.selected_nodes[1]
            adjaceny_list = [(u, v, k, d) for u, v, k, d in game.GRAPH.edges(self.node1, keys=True, data=True) if v == self.node2]
            road_count = len(adjaceny_list) # number of edges(roads) between selected 2 nodes(cities)  

            if road_count >= 1: # if selected 2 nodes are neighbors
                self.boardWidget.stackedWidget_claim_road.setCurrentWidget(self.boardWidget.state_claim_road_question) # get question state
                # set question text 
                self.boardWidget.textEdit_claim_road_question_select_cities.setText(
                    f"SELECTING {game.selected_nodes[-2].upper()}-{game.selected_nodes[-1].upper()}")

                if road_count == 2: # if there are 2 parallel roads, give 2 options (1 for each color)
                    colors = [i[3]['color'] for i in adjaceny_list]
                    weight = adjaceny_list[0][3]['weight'] # weight is always same at parallel roads

                    if colors[0] == colors[1]: # if 2 colors are same (they're both none)
                        # set cost text
                        self.boardWidget.label_claim_road_question_cost.setText(
                            f"IT WILL COST YOU {weight} CARDS OF ANY COLOR (SELECT FROM MY CARDS BELOW)")
                        self.set_train_card_buttons(weight) #set actions for color buttons
            
                    else:
                        # set cost text
                        self.boardWidget.label_claim_road_question_cost.setText(
                            f"IT WILL COST YOU {weight} CARDS OF {colors[0]} OR {colors[1]} (SELECT FROM MY CARDS BELOW)")
                        self.set_train_card_buttons(weight, [colors[0], colors[1]]) #set actions for color buttons


                else: # if there's a single road 
                    color = adjaceny_list[0][3]['color'].lower() # get color
                    weight = adjaceny_list[0][3]['weight'] # get weight

                    if color == 'none': # if color is none, display slightly different text
                        # set cost text
                        self.boardWidget.label_claim_road_question_cost.setText(
                            f"IT WILL COST YOU {weight} CARDS OF ANY COLOR (SELECT FROM MY CARDS BELOW)")
                        self.set_train_card_buttons(weight) #set actions for color buttons
                    else:
                        self.select_color(color, weight)

    def select_color(self, color, weight):
        # check if player has enough cards
        card_count = game.train_cards_player1.count(color.lower())
        rainbow_count = game.train_cards_player1.count("rainbow")

        if weight <= card_count:
            select_color_text = f"COST: {weight} {color} CARDS \nYOU CAN SELECT ANOTHER COLOR IF YOU'D LIKE TO"
            select_color_bool = True
            cost = [card_count, 0] # cost of colored card + rainbow card
        
        # check if player can compensate with rainbow cards
        elif weight <= card_count + rainbow_count:
            select_color_text = (f"COST: {weight} CARDS ({card_count} {color} + {weight - card_count} RAINBOW)\n"
                                    "YOU CAN SELECT ANOTHER COLOR IF YOU'D LIKE TO")
            select_color_bool = True
            cost = [card_count, weight - card_count] # cost of colored card + rainbow card

        # player can't select with that color
        else:
            select_color_text = "YOU DON'T HAVE ENOUGH CARDS \nSELECT ANOTHER COLOR!"
            select_color_bool = False

        # if player selected a valid color
        if select_color_bool:
            # get color and display cost
            self.boardWidget.label_claim_road_cost.setText(select_color_text)
            self.boardWidget.stackedWidget_claim_road.setCurrentWidget(self.boardWidget.state_claim_road_confirm)

            # self.set_ok_cancel_buttons(color, cost) # doesnt work !! so I had to skip this part for now

            self.take_road("player1", color, cost, self.node1, self.node2) # take selected road
            self.initUI()
        else:
            self.boardWidget.label_claim_road_cost.setText(select_color_text)
            self.boardWidget.stackedWidget_claim_road.setCurrentWidget(self.boardWidget.state_claim_road_confirm)

    def take_road(self, player, color, cost, node1, node2):
        if player == 'player1':
            for i in range(cost[0]):
                game.discarded_cards.append(color.lower()) # discard selected color cards
                game.train_cards_player1.remove(color.lower()) # remove from user cards
            for i in range(cost[1]):
                game.discarded_cards.append('RAINBOW'.lower()) # discard rainbow cards
                game.train_cards_player1.remove('RAINBOW'.lower()) # remove from user cards
            game.trains_player1 -= cost[0] + cost[1] # spend trains
        else:
            for i in range(cost[0]):
                game.discarded_cards.append(color.lower()) # discard selected color cards
                game.train_cards_player2.remove(color.lower()) # remove from user cards
            for i in range(cost[1]):
                game.discarded_cards.append('RAINBOW'.lower()) # discard rainbow cards
                game.train_cards_player2.remove('RAINBOW'.lower()) # remove from user cards
            game.trains_player2 -= cost[0] + cost[1] # spend trains

        game.taken_routes_player1.append((node1, node2, str(cost[0]+cost[1]), color)) # take selected road
        game.selected_nodes = [] #reset selected nodes

        self.display_warning('player2\'s turn')
        game.get_next_player(player)

    def draw_train_card(self, player, card_index):
        if player == 'player1':
            if game.player1_train_draw_count < 2: 
                if game.displayed_cards[card_index] == 'rainbow' and game.player1_train_draw_count == 0:
                    game.draw_train_card(player, card_index) # draw card
                    game.get_next_player(player) # skip player's turn
                    game.player1_train_draw_count = 0 # reset count for player1
                    self.initUI() # update board
                    self.display_warning('player2\'s turn') 

                elif game.displayed_cards[card_index] != 'rainbow':
                    game.draw_train_card(player, card_index) # draw card 
                    game.player1_train_draw_count += 1 # increase count
                    self.initUI() # update board
                    if game.player1_train_draw_count == 2: # if it was 2nd draw skip players turn
                        game.player1_train_draw_count = 0 # reset count for player1
                        game.get_next_player(player) # skip player's turn
                        self.display_warning('player2\'s turn')
                else:
                    self.display_warning("DON'T CHEAT, BRO") # display dont cheat warning

        else:
            self.display_warning("IT'S NOT YOUR TURN") # display dont cheat warning
            # self.boardWidget.button_ticket_option1.setEnabled(False)

        # add method for bot
        if player == 'player2':
            pass

    def draw_train_card_random(self, player):
        if player == 'player1':
            if game.player1_train_draw_count < 2:
                game.draw_train_card_random(player) # draw a random card
                game.player1_train_draw_count += 1 # increase count
                
                if game.player1_train_draw_count == 2: # if it was 2nd draw skip players turn
                    game.player1_train_draw_count = 0 # reset count for player1
                    game.get_next_player(player) # skip player's turn
                    self.display_warning('player2\'s turn')
            else:
                self.display_warning("DON'T CHEAT, BRO") # display dont cheat warning
        
            self.initUI() #display new board
        
        else:
            self.display_warning("IT'S NOT YOUR TURN", 0.2) # display dont cheat warning

        # add method for bot
        if player == 'player2':
            pass


    def button_ticket_draw_listener(self):
        button_1 = self.boardWidget.button_ticket_option1 # get name of each button (displays tickets)
        button_2 = self.boardWidget.button_ticket_option2
        button_3 = self.boardWidget.button_ticket_option3

        button_list : list = [button_1, button_2, button_3]
        button_bool_list : list = [i.isChecked() for i in button_list] # get state of each button as bool
        button_count = button_bool_list.count(True) # number of pressed buttons

        if (
            (self.game.round_count == 0 and button_count >= 2) or # at first round player must select at least 2 tickets
            (self.game.round_count > 0 and button_count >= 1) # at other rounds player must select at least 1 ticket
        ):

            selected_tickets = [game.ticket_options_player1[idx] for idx, bool in enumerate(button_bool_list) if bool is True]
            other_tickets = set(game.ticket_cards_player1) - set(selected_tickets) # get unselected tickets
            game.destination_tickets.extend(other_tickets) # place unselected cards to bottom of the deck
            game.ticket_cards_player1.extend(selected_tickets)
            game.select_ticket_bool = False


            if game.round_count > 0: # skip player's turn if it wasn't first round
                game.get_next_player(game.player)

            game.round_count += 1 

            self.initUI()
            self.boardWidget.stackedWidget.setCurrentWidget(self.boardWidget.state_game)
        
        # add method for bot


    def set_train_card_buttons(self, weight, selected_colors = list('blue red green yellow black orange purple white'.upper().split())):
        # set actions of train buttons
        color_button_map = {
            "BLACK": self.boardWidget.button_train_black,
            "BLUE": self.boardWidget.button_train_blue,
            "GREEN": self.boardWidget.button_train_green,
            "ORANGE": self.boardWidget.button_train_orange,
            "PURPLE": self.boardWidget.button_train_purple,
            "RED": self.boardWidget.button_train_red,
            "WHITE": self.boardWidget.button_train_white,
            "YELLOW": self.boardWidget.button_train_yellow,
        }
        
        # Connect signals for selected colors
        for color in selected_colors:
            color_button_map[color].clicked.connect(lambda checked, color=color: self.select_color(color, weight))

    # doesnt work yet
    def set_ok_cancel_buttons(self, color, cost):
        self.boardWidget.buttonBox_claim_road.accepted.connect(self.handle_accept)
        self.boardWidget.buttonBox_claim_road.rejected.connect(lambda : self.take_road("player1", color, cost, self.node1, self.node2))


    def display_warning(self, text, duration = 0.5):
        self.boardWidget.dont_cheat_label.setText(text) # set text and background
        self.boardWidget.dont_cheat_label.setStyleSheet("QLabel {background-color: white; color: black;}")
        
        self.boardWidget.dont_cheat_label.adjustSize() # adjust label size to match text size
        
        self.boardWidget.dont_cheat_label.setAlignment(QtCore.Qt.AlignCenter) # Center the label
    
        self.boardWidget.dont_cheat_label.raise_() # raise label to the top

        # Show the label
        self.boardWidget.dont_cheat_label.show() # display warning
        self.boardWidget.dont_cheat_label.repaint() # update board
        time.sleep(duration) # wait for specified amount of seconds
        self.boardWidget.dont_cheat_label.hide() # hide warning

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Game()
    main_win = MainWindow(game)
    main_win.show()
    sys.exit(app.exec())
