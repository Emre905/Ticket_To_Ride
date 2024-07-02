# Create turn based Ticket to Ride game for 2 players 
import sys 
import networkx as nx 
import numpy as np 
import random
from collections import deque
from functions import VERTICES, EDGES, TICKETS, EDGES_DICT, POINT_EDGE_DICT, G, CITY_LOCATIONS
import functions as func
from Ui_windows.Ui_mainwindow import Ui_MainWindow 
from Ui_windows.Ui_widget_game_board import Ui_Form_Game_Board
from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 

''' Too add: 
1- longest road point to functions.calculate_point()
2- add function to reset discard pile and train cards each time len(self.train_cards) == 0
3- stations to functions

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
        self.cards : deque = deque(i for i in list('blue red green yellow black orange purple white rainbow'.split())*4)
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
        self.train_cards_player2 : list = [] 
        self.ticket_cards_player1 : list = [] # ticket cards player 1 has
        self.ticket_cards_player2 : list = [] # check!! can also be set()
        self.displayed_cards : list = [] # 5 cards that player selects train cards
        self.discarded_cards : deque = deque()
        self.taken_routes_player1 : list = []
        self.taken_routes_player2 : list = []
        self.select_ticket_bool : bool = True
        self.player = 'player1'
        self.round_count = 0
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
            self.train_cards : deque = self.discarded_cards.copy() # take all discarded cards and put on train cards
            random.shuffle(self.train_cards) # shuffle train cards
            self.discarded_cards : deque = deque([]) # reset discarded cards (they're back in the game)
            self.display_train_cards()

    # deal destination tickets to both players in the beginning of the game
    def deal_ticket_cards(self) -> list:
        self.ticket_options_player1 : list = []
        self.ticket_options_player2 : list = []
        for i in range(3):
            self.ticket_options_player1.append(self.destination_tickets.popleft()) # deal top card to player 1
            self.ticket_options_player2.append(self.destination_tickets.popleft()) # deal top card to player 2
        
        # player_1_input = input(f'Player 1 tickets: {player_1_ticket_options} \n'
        #                        '(select at least 2 tickets and give input like 1 3 or 13 for 1st and 3rd card): ')
        # while True:
        #     try: # get player 1 ticket choice
        #         player_1_idx = [int(i)-1 for i in list(player_1_input) if i!=' '] #remove spaces and get all integers
        #         if not len(player_1_idx) in [2,3]: # user selected 1 or 0 ticket
        #             player_1_input = input(f'Player 1 tickets: {player_1_ticket_options} \n'
        #                         '(select at least 2 tickets and give input like 1 3 or 13 for 1st and 3rd card): ')
        #         else:
        #             break
        #     except ValueError:
        #         player_1_input = input(f'Player 1 tickets: {player_1_ticket_options} \n'
        #                         '(try again! give input like 1 3 or 13 for 1st and 3rd card): ')
                
        # player_2_input = input(f'Player 2 tickets: {player_2_ticket_options} \n'
        #                        '(try again! select at least 2 tickets and give input like 1 3 for 1st and 3rd card): ')
        
        # return player_2(bot) later 

        # # This part will later be changed to bot_select_destination_tickets()
        # while True:
        #     try: # get player 2 ticket choice
        #         player_2_idx = [int(i)-1 for i in list(player_2_input) if i!=' ']
        #         if not len(player_2_idx) in [2,3]: # user selected 0, 1 or >4 ticket
        #             player_2_input = input(f'Player 2 tickets: {player_2_ticket_options} \n'
        #                         '(select at least 2 tickets and give input like 1 3 or 13 for 1st and 3rd card): ')
        #         else:
        #             break
        #     except ValueError:
        #         player_2_input = input(f'Player 2 tickets: {player_2_ticket_options} \n'
        #                         '(try again! give input like 1 3 or 13 for 1st and 3rd card): ')
        
        # player_1_tickets = [player_1_ticket_options[i] for i in player_1_idx] # use indexes to get corresponding tickets
        # player_2_tickets = [player_2_ticket_options[i] for i in player_2_idx] # use indexes to get corresponding tickets

        # self.ticket_cards_player1.extend(player_1_tickets) # append selected tickets to player's list
        # self.ticket_cards_player2.extend(player_2_tickets) # append selected tickets to player's list

    # get which player's turn it is
    def get_player_turn(self):
        pass

    # draw a card from pile    
    def draw_train_card_random(self, player):
        try:
            if player == 'player1':
                self.train_cards_player1.append(self.train_cards.popleft())
            else:
                self.train_cards_player2.append(self.train_cards.popleft())

        except IndexError: # when the train_cards is empty, pop will raise IndexError.
            self.train_cards : deque = self.discarded_cards.copy() # take all discarded cards and put on train cards
            random.shuffle(self.train_cards) # shuffle train cards
            self.discarded_cards : deque = deque([]) # reset discarded cards (they're back in the game)

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
            self.train_cards : deque = self.discarded_cards.copy() # take all discarded cards and put on train cards
            random.shuffle(self.train_cards) # shuffle train cards
            self.discarded_cards : deque = deque([]) # reset discarded cards (they're back in the game)  

            top_card = self.train_cards.popleft()
            self.displayed_cards.insert(card_index, top_card)

    def draw_ticket_cards(self, player):
        pass

    def claim_route(self, player):
        pass

    def deal_first_round(self) -> None:
        self.deal_train_cards() # deal 4 train cards to players in the beginning
        self.display_train_cards() # display top 5 cards to start the game
        self.deal_ticket_cards()
        # func.plot_graph([],[])
        # self.deal_ticket_cards() # deal 3 train cards to players in the beginning (player must select at least 2)
        # print(self.ticket_cards_player1, self.ticket_cards_player2)

    def run(self):
        self.deal_first_round()
        # print(self.ticket_options_player1)
        # print(self.train_cards_player1) #test
        # print(self.discarded_cards, len(self.train_cards), self.displayed_cards) #test

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
                                 game.train_cards_player1, 
                                 game.ticket_cards_player1,
                                 game.displayed_cards,
                                 game.ticket_options_player1,
                                 game.select_ticket_bool,
                                 len(game.train_cards))
        
        # Add the game board container to the stacked widget
        self.ui.stackedWidget.addWidget(self.boardWidgetContainer)
        
        # Switch to the game board UI
        self.ui.stackedWidget.setCurrentWidget(self.boardWidgetContainer)
    
        # check which buttons are pressed when ok button is hit
        self.boardWidget.button_ticket_option_okay.clicked.connect(self.button_ticket_draw_listener)

        self.boardWidget.button_draw1.clicked.connect(lambda: self.draw_train_card(game.player, 0))
        self.boardWidget.button_draw2.clicked.connect(lambda: self.draw_train_card(game.player, 1))
        self.boardWidget.button_draw3.clicked.connect(lambda: self.draw_train_card(game.player, 2))
        self.boardWidget.button_draw4.clicked.connect(lambda: self.draw_train_card(game.player, 3))
        self.boardWidget.button_draw5.clicked.connect(lambda: self.draw_train_card(game.player, 4))
        self.boardWidget.button_draw_train.clicked.connect(lambda: self.draw_train_card_random(game.player))

    def draw_train_card(self, player, card_index):
        game.draw_train_card(player, card_index)
        self.initUI()

    def draw_train_card_random(self, player):
        game.draw_train_card_random(player) # select a card inside function
        self.initUI() #display new board

    def button_ticket_draw_listener(self):
        button_1 = self.boardWidget.button_ticket_option1 # get name of each button (displaying ticket)
        button_2 = self.boardWidget.button_ticket_option2
        button_3 = self.boardWidget.button_ticket_option3

        button_list : list = [button_1, button_2, button_3]
        button_bool_list : list = [i.isChecked() for i in button_list] # get state of each button as bool
        button_count = button_bool_list.count(True) # number of pressed buttons

        if (
            (self.game.round_count == 0 and button_count >= 2) or 
            (self.game.round_count > 0 and button_count >= 1)
        ): # at first round player must select at least 2 tickets

            selected_tickets = [game.ticket_options_player1[idx] for idx, bool in enumerate(button_bool_list) if bool is True]
            game.ticket_cards_player1.extend(selected_tickets)
            game.select_ticket_bool = False
            self.initUI()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Game()
    main_win = MainWindow(game)
    main_win.show()
    sys.exit(app.exec())
