from PyQt5 import QtCore, QtGui, QtWidgets 
from functions import EDGES, CITY_LOCATIONS 
import networkx as nx 
from matplotlib.image import imread 
import numpy as np 
from PyQt5.QtWidgets import QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib.figure import Figure 
import sys 
from matplotlib.patches import FancyArrowPatch 

class Ui_Form_Game_Board(object):
    def setupUi(self, 
                Form, 
                player, 
                train_cards, 
                ticket_cards, 
                button_colors, 
                ticket_options_player1, 
                select_ticket, 
                draw_ticket_number,  
                player_routes,
                train_counts):

        self.player1_routes = player_routes[0]
        self.player2_routes = player_routes[1]


        Form.setObjectName("Form")
        Form.resize(1330, 875)
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(130, 660, 1011, 100))
        self.layoutWidget.setObjectName("layoutWidget")

        # display whose turn it is
        self.player = player
        font = QtGui.QFont()
        font.setPointSize(16)
        self.current_player = QtWidgets.QLabel(Form)
        self.current_player.setFont(font)
        self.current_player.setGeometry(QtCore.QRect(20, 30, 141, 31)) # adjust player's turn location

        # add a warning label
        font.setPointSize(30)
        self.label_warn_user = QtWidgets.QLabel(Form)
        self.label_warn_user.setFont(font)
        self.label_warn_user.setGeometry(250, 300, 330, 50)  # set position and size of the label
        self.label_warn_user.hide()  # hide the label initially

        # display player's train cards at bottom

        self.train_count = {i:train_cards[0].count(i) \
                       for i in list('blue red green yellow black orange purple white rainbow'.split())}
        self.train_count2 = {i:train_cards[1].count(i) \
                       for i in list('blue red green yellow black orange purple white rainbow'.split())}
        rainbow_gradient = "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 0, 0, 255), \
            stop:0.166 rgba(255, 255, 0, 255), stop:0.333 rgba(0, 255, 0, 255), stop:0.5 rgba(0, 255, 255, 255), \
            stop:0.666 rgba(0, 0, 255, 255), stop:0.833 rgba(255, 0, 255, 255), stop:1 rgba(255, 0, 0, 255)); color:black"
        
        # set all train card buttons
        self.layoutWidget_mycards = QtWidgets.QWidget(Form)
        self.layoutWidget_mycards.setGeometry(QtCore.QRect(-30, 100, 1011, 150))
        self.layoutWidget_mycards.setObjectName("layoutWidget")
        self.horizontalLayout_mycards = QtWidgets.QHBoxLayout(self.layoutWidget_mycards)
        self.horizontalLayout_mycards.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_mycards.setSpacing(0)
        self.horizontalLayout_mycards.setObjectName("horizontalLayout")
        spacerItem_mycards = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_mycards.addItem(spacerItem_mycards)
        self.label_mycards = QtWidgets.QLabel(self.layoutWidget_mycards)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_mycards.setFont(font)
        self.label_mycards.setObjectName("label_mycards")
        self.horizontalLayout_mycards.addWidget(self.label_mycards)

        # Creating train card buttons
        self.button_train_red = self.create_button("button_train_red", "red", "white")
        self.button_train_green = self.create_button("button_train_green", "green", "white")
        self.button_train_blue = self.create_button("button_train_blue", "blue", "white")
        self.button_train_orange = self.create_button("button_train_orange", "orange", "black")
        self.button_train_yellow = self.create_button("button_train_yellow", "yellow", "black")
        self.button_train_black = self.create_button("button_train_black", "black", "white")
        self.button_train_white = self.create_button("button_train_white", "white", "black")
        self.button_train_purple = self.create_button("button_train_purple", "purple", "white")
        self.button_train_rainbow = self.create_button("button_train_rainbow", rainbow_gradient, "black")       


        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_mycards.addItem(spacerItem1)
        self.label_mytrains = QtWidgets.QLabel(self.layoutWidget_mycards)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_mytrains.setFont(font)
        self.label_mytrains.setObjectName("label_mytrains")
        self.horizontalLayout_mycards.addWidget(self.label_mytrains)
        self.label_mytrains.setText(f"  My Trains: {train_counts[0]}") # number of train cards
        spacerItem2_mycards = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_mycards.addItem(spacerItem2_mycards)
        self.layoutWidget_mycards.setGeometry(QtCore.QRect(300, 640, 800, 60)) # adjust my cards location


        # right widget (draw destination and display cards)
        button_colors_rename = [i if i != 'rainbow' else "qlineargradient(spread:pad, x1:0, \
                               y1:0, x2:1, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.166 rgba(255, 255, 0, 255), \
                               stop:0.333 rgba(0, 255, 0, 255), stop:0.5 rgba(0, 255, 255, 255), stop:0.666 \
                               rgba(0, 0, 255, 255), stop:0.833 rgba(255, 0, 255, 255), stop:1 rgba(255, 0, 0, 255))" \
                               for i in button_colors]
        self.draw_ticket_number = draw_ticket_number # get total number of train cards on the draw pile
        
        self.layoutWidget1 = QtWidgets.QWidget(Form)
        self.layoutWidget1.setGeometry(QtCore.QRect(1201, 52, 102, 592))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.button_draw_train = QtWidgets.QPushButton(self.layoutWidget1)
        self.button_draw_train.setMinimumSize(QtCore.QSize(100, 60))
        self.button_draw_train.setMaximumSize(QtCore.QSize(100, 60))
        self.button_draw_train.setStyleSheet("QPushButton{\n"
"background-color: rgb(11, 182, 255); \n"
"border-style: outset; \n"
"border-width: 2px;\n"
"border-radius: 12px; \n"
"border-color: black;\n"
"padding: 6px}\n"
"QPushButton:hover{\n"
"border: 2px solid red}background-color: red;")
        self.button_draw_train.setObjectName("button_draw_train")
        self.verticalLayout.addWidget(self.button_draw_train)

        # first draw card
        self.button_draw1 = QtWidgets.QPushButton(self.layoutWidget1)
        self.button_draw1.setMinimumSize(QtCore.QSize(0, 100))
        self.button_draw1.setMaximumSize(QtCore.QSize(60, 100))
        self.button_draw1.setStyleSheet("QPushButton{\n"
f"background-color: {button_colors_rename[0]}; \n"
"border-style: outset; \n"
"border-width: 2px;\n"
"border-radius: 12px; \n"
"border-color: black;\n"
"padding: 6px}\n"
"QPushButton:hover{\n"
"border: 2px solid red}background-color: red;")
        self.button_draw1.setText("")
        self.button_draw1.setAutoRepeatDelay(300)
        self.button_draw1.setObjectName("button_draw1")
        self.verticalLayout.addWidget(self.button_draw1)
        self.button_draw2 = QtWidgets.QPushButton(self.layoutWidget1)
        self.button_draw2.setMinimumSize(QtCore.QSize(0, 100))
        self.button_draw2.setMaximumSize(QtCore.QSize(60, 100))
        self.button_draw2.setStyleSheet("QPushButton{\n"
f"background-color: {button_colors_rename[1]}; \n"
"border-style: outset; \n"
"border-width: 2px;\n"
"border-radius: 12px; \n"
"border-color: black;\n"
"padding: 6px}\n"
"QPushButton:hover{\n"
"border: 2px solid red}")
        self.button_draw2.setText("")
        self.button_draw2.setObjectName("button_draw2")
        self.verticalLayout.addWidget(self.button_draw2)
        self.button_draw3 = QtWidgets.QPushButton(self.layoutWidget1)
        self.button_draw3.setMinimumSize(QtCore.QSize(0, 100))
        self.button_draw3.setMaximumSize(QtCore.QSize(60, 100))
        self.button_draw3.setStyleSheet("QPushButton{\n"
f"background-color: {button_colors_rename[2]}; \n"
"border-style: outset; \n"
"border-width: 2px;\n"
"border-radius: 12px; \n"
"border-color: black;\n"
"padding: 6px}\n"
"QPushButton:hover{\n"
"border: 2px solid red}")
        self.button_draw3.setText("")
        self.button_draw3.setObjectName("button_draw3")
        self.verticalLayout.addWidget(self.button_draw3)
        self.button_draw4 = QtWidgets.QPushButton(self.layoutWidget1)
        self.button_draw4.setMinimumSize(QtCore.QSize(0, 100))
        self.button_draw4.setMaximumSize(QtCore.QSize(60, 100))
        self.button_draw4.setStyleSheet("QPushButton{\n"
f"background-color: {button_colors_rename[3]}; \n"
"border-style: outset; \n"
"border-width: 2px;\n"
"border-radius: 12px; \n"
"border-color: black;\n"
"padding: 6px}\n"
"QPushButton:hover{\n"
"border: 2px solid red}")
        self.button_draw4.setText("")
        self.button_draw4.setObjectName("button_draw4")
        self.verticalLayout.addWidget(self.button_draw4)
        self.button_draw5 = QtWidgets.QPushButton(self.layoutWidget1)
        self.button_draw5.setMinimumSize(QtCore.QSize(0, 100))
        self.button_draw5.setMaximumSize(QtCore.QSize(60, 100))
        self.button_draw5.setStyleSheet("QPushButton{\n"
f"background-color: {button_colors_rename[4]}; \n"
"border-style: outset; \n"
"border-width: 2px;\n"
"border-radius: 12px; \n"
"border-color: black;\n"
"padding: 6px}\n"
"QPushButton:hover{\n"
"border: 2px solid red}\n"
"")
        self.button_draw5.setText("")
        self.button_draw5.setObjectName("button_draw5")
        self.verticalLayout.addWidget(self.button_draw5)
        self.verticalLayout

        # use game board picture
        self.label_board = QtWidgets.QLabel(Form)
        self.label_board.setGeometry(QtCore.QRect(-7, -80, 1231, 621)) # adjust  borders of map
        self.label_board.setText("")
        self.label_board.setPixmap(QtGui.QPixmap("USA_map.jpg"))
        # self.label_board.setScaledContents(True)
        self.label_board.setObjectName("label_board")
        self.label_board.resize(1350,820) # adjust size of map
        self.label_board.lower()


        self.layoutWidget2 = QtWidgets.QWidget(Form)
        self.layoutWidget2.setGeometry(QtCore.QRect(20, 60, 91, 450)) # adjust black rectangle
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_players = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_players.setFont(font)
        self.label_players.setObjectName("label_players")
        self.verticalLayout_2.addWidget(self.label_players)
        self.label_tickets = QtWidgets.QLabel(self.layoutWidget2)

        # list player's selected tickets
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_tickets.setFont(font)
        self.label_tickets.setObjectName("label_tickets")
        self.verticalLayout_2.addWidget(self.label_tickets)
        self.list_tickets = QtWidgets.QListWidget(self.layoutWidget2)
        self.list_tickets.setObjectName("list_tickets")
        self.verticalLayout_2.addWidget(self.list_tickets)
        self.label_status = QtWidgets.QLabel(Form)
        self.label_status.setGeometry(QtCore.QRect(1170, 10, 151, 20))
        self.label_status.setObjectName("label_status")
        self.button_draw_destination = QtWidgets.QPushButton(Form)
        self.button_draw_destination.setGeometry(QtCore.QRect(1201, 12, 128, 33))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.button_draw_destination.setFont(font)
        self.button_draw_destination.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.button_draw_destination.setObjectName("button_draw_destination")
        self.pushButton_mytickets = QtWidgets.QPushButton(Form)
        self.pushButton_mytickets.setGeometry(QtCore.QRect(30, 60, 141, 31))
        self.pushButton_mytickets.setCheckable(True)
        self.pushButton_mytickets.setChecked(False)
        self.pushButton_mytickets.setAutoRepeat(False)
        self.pushButton_mytickets.setAutoDefault(False)
        self.pushButton_mytickets.setFlat(False)
        self.pushButton_mytickets.setObjectName("pushButton_mytickets")

        
        # opponent ticket info
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 580, 140, 100)) # adjust location
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_opponent_info = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_opponent_info.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_opponent_info.setObjectName("verticalLayout_opponent_info")
        self.label_opponent_info = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_opponent_info.setFont(font)
        self.label_opponent_info.setObjectName("label_opponent_info")
        self.verticalLayout_opponent_info.addWidget(self.label_opponent_info)
        self.text_opponent_tickets = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.text_opponent_tickets.setFont(font)
        self.text_opponent_tickets.setObjectName("text_opponent_tickets")
        self.verticalLayout_opponent_info.addWidget(self.text_opponent_tickets)
        self.text_opponent_cards = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.text_opponent_cards.setFont(font)
        self.text_opponent_cards.setObjectName("text_opponent_cards")
        self.verticalLayout_opponent_info.addWidget(self.text_opponent_cards)
        self.text_opponent_trains = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.text_opponent_trains.setFont(font)
        self.text_opponent_trains.setObjectName("text_opponent_trains")
        self.verticalLayout_opponent_info.addWidget(self.text_opponent_trains)

        # opponent info
        self.label_opponent_info.setText("Opponent info:")
        self.text_opponent_tickets.setText(f"{len(ticket_cards[1])} TICKETS")
        self.text_opponent_cards.setText(f"{len(train_cards[1])} CARDS")
        self.text_opponent_trains.setText(f"{train_counts[1]} TRAINS")


        # player (my) tickets
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 95, 150, 450)) 
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutWidget.setStyleSheet("background-color: white;")  # Debugging (try to remove unnecessary rectangle on left)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 10, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # add destination tickets names
        ticket_cards_format = [f"<li>{i[0]} - {i[1]} {i[2]}</li>" for i in ticket_cards[0]] 
        self.ticket_cards_text = f"<ul>{''.join(ticket_cards_format)}</ul>" # get player1 tickets as bullet list text
        self.label_ticket1 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_ticket1.setWordWrap(True)
        self.label_ticket1.setObjectName("label_ticket1")
        self.verticalLayout_2.addWidget(self.label_ticket1)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)


        # select destination ticket
        self.stackedwidget_select_ticket = QtWidgets.QStackedWidget(Form)
        self.stackedwidget_select_ticket.setGeometry(QtCore.QRect(440, 10, 581, 121))
        self.stackedwidget_select_ticket.setObjectName("stackedWidget_board")

        self.state_game = QtWidgets.QWidget()
        self.state_game.setObjectName("state_game")
        self.stackedwidget_select_ticket.addWidget(self.state_game)


        # set and display ticket options to player1
        self.ticket_options_player1_text = [f"{i[0]}-{i[1]} {i[2]}" for i in ticket_options_player1]

        # set widget and text
        self.state_select_ticket = QtWidgets.QWidget()
        self.state_select_ticket.setObjectName("state_select_ticket")
        self.label_state_select_ticket = QtWidgets.QLabel(self.state_select_ticket)
        self.label_state_select_ticket.setGeometry(QtCore.QRect(130, 0, 291, 41))
        self.label_state_select_ticket.setObjectName("label_state_select_ticket")
        self.label_state_select_ticket.setStyleSheet('background: white; font: 20px')
        self.label_state_select_ticket.setAlignment(QtCore.Qt.AlignCenter)

        # set ticket option buttons
        button1_x, button1_y, button1_w, button1_h = 50, 40, 141, 41
        self.button_ticket_option1 = QtWidgets.QPushButton(self.state_select_ticket)
        self.button_ticket_option1.setGeometry(QtCore.QRect(button1_x, button1_y, button1_w, button1_h))
        self.button_ticket_option1.setCheckable(True)
        self.button_ticket_option1.setObjectName("pushButton_ticket_option1")
        self.label_ticket_option1 = QtWidgets.QLabel(self.state_select_ticket)
        self.label_ticket_option1.setText("This is a long text.")
        self.label_ticket_option1.setGeometry(QtCore.QRect(button1_x+5, button1_y, button1_w-5, button1_h))
        self.label_ticket_option1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ticket_option1.setWordWrap(True)
        self.label_ticket_option1.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents) # button isn't clickable without this

        button2_x, button2_y, button2_w, button2_h = 210, 40, 141, 41
        self.button_ticket_option2 = QtWidgets.QPushButton(self.state_select_ticket)
        self.button_ticket_option2.setGeometry(QtCore.QRect(button2_x, button2_y, button2_w, button2_h))
        self.button_ticket_option2.setCheckable(True)
        self.button_ticket_option2.setObjectName("pushButton_ticket_option2")
        self.label_ticket_option2 = QtWidgets.QLabel(self.state_select_ticket)
        self.label_ticket_option2.setText("This is a long text.")
        self.label_ticket_option2.setGeometry(QtCore.QRect(button2_x+5, button2_y, button2_w-5, button2_h))
        self.label_ticket_option2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ticket_option2.setWordWrap(True)
        self.label_ticket_option2.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents) # button isn't clickable without this

        button3_x, button3_y, button3_w, button3_h = 370, 40, 141, 41
        self.button_ticket_option3 = QtWidgets.QPushButton(self.state_select_ticket)
        self.button_ticket_option3.setGeometry(QtCore.QRect(button3_x, button3_y, button3_w, button3_h))
        self.button_ticket_option3.setCheckable(True)
        self.button_ticket_option3.setObjectName("pushButton_ticket_option3")
        self.label_ticket_option3 = QtWidgets.QLabel(self.state_select_ticket)
        self.label_ticket_option3.setText("This is a long text")
        self.label_ticket_option3.setGeometry(QtCore.QRect(button3_x+5, button3_y, button3_w-5, button3_h))
        self.label_ticket_option3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ticket_option3.setWordWrap(True) 
        self.label_ticket_option3.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents) # button isn't clickable without this


        self.button_ticket_option_okay = QtWidgets.QPushButton(self.state_select_ticket)
        self.button_ticket_option_okay.setGeometry(QtCore.QRect(240, 90, 75, 23))
        self.button_ticket_option_okay.setObjectName("pushButton_ticket_option_okay")
        self.stackedwidget_select_ticket.addWidget(self.state_select_ticket)


        # set claim road stackedwidget. will run when player wants to claim a road
        self.stackedWidget_claim_road = QtWidgets.QStackedWidget(Form)
        self.stackedWidget_claim_road.setGeometry(QtCore.QRect(400, -20, 641, 110))
        self.stackedWidget_claim_road.setObjectName("stackedWidget_claim_road")
        self.state_claim_road_empty = QtWidgets.QWidget()
        self.state_claim_road_empty.setObjectName("state_claim_road_empty")
        self.label_claim_road_empty = QtWidgets.QLabel(self.state_claim_road_empty)
        self.label_claim_road_empty.setGeometry(QtCore.QRect(300, 40, 47, 13))
        self.label_claim_road_empty.setText("")
        self.label_claim_road_empty.setObjectName("label_claim_road_empty")
        self.stackedWidget_claim_road.addWidget(self.state_claim_road_empty)

        self.state_claim_road_select_path = QtWidgets.QWidget()
        self.state_claim_road_select_path.setObjectName("state_claim_road_select_path")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.state_claim_road_select_path)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(150, 10, 381, 101))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_2_claim_road_select_color = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_2_claim_road_select_color.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2_claim_road_select_color.setObjectName("verticalLayout_2_claim_road_select_color")
        self.label_claim_road_select_color = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_claim_road_select_color.setFont(font)
        self.label_claim_road_select_color.setAlignment(QtCore.Qt.AlignCenter)
        self.label_claim_road_select_color.setObjectName("label_claim_road_select_color")
        self.verticalLayout_2_claim_road_select_color.addWidget(self.label_claim_road_select_color)
        self.horizontalLayout_claim_road_select_color = QtWidgets.QHBoxLayout()
        self.horizontalLayout_claim_road_select_color.setObjectName("horizontalLayout_claim_road_select_color")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_claim_road_select_color.addItem(spacerItem)
        

        self.stackedWidget_claim_road.addWidget(self.state_claim_road_select_path)
        self.state_claim_road_question = QtWidgets.QWidget()
        self.state_claim_road_question.setObjectName("state_claim_road_question")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.state_claim_road_question)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 641, 111))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_claim_road_question = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_claim_road_question.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_claim_road_question.setObjectName("verticalLayout_claim_road_question")
        self.textEdit_claim_road_question_select_cities = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.textEdit_claim_road_question_select_cities.setFont(font)
        self.textEdit_claim_road_question_select_cities.setAlignment(QtCore.Qt.AlignCenter)
        self.textEdit_claim_road_question_select_cities.setObjectName("textEdit_claim_road_question_select_cities")
        self.verticalLayout_claim_road_question.addWidget(self.textEdit_claim_road_question_select_cities)
        self.label_claim_road_question_cost = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_claim_road_question_cost.setFont(font)
        self.label_claim_road_question_cost.setAlignment(QtCore.Qt.AlignCenter)
        self.label_claim_road_question_cost.setObjectName("label_claim_road_question_cost")
        self.verticalLayout_claim_road_question.addWidget(self.label_claim_road_question_cost)
        self.verticalLayout_claim_road_question.setContentsMargins(0, 25, 0, 0)
        self.horizontalLayout_claim_road_question = QtWidgets.QHBoxLayout()
        self.horizontalLayout_claim_road_question.setObjectName("horizontalLayout_claim_road_question")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_claim_road_question.addItem(spacerItem2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_claim_road_question.addItem(spacerItem3)
        self.verticalLayout_claim_road_question.addLayout(self.horizontalLayout_claim_road_question)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_claim_road_question.addItem(spacerItem4)
        self.textEdit_claim_road_background = QtWidgets.QPlainTextEdit(self.state_claim_road_question)
        self.textEdit_claim_road_background.setGeometry(QtCore.QRect(0, 0, 871, 141))
        self.textEdit_claim_road_background.setObjectName("textEdit_claim_road_background")
        self.textEdit_claim_road_background.raise_()
        self.verticalLayoutWidget_2.raise_()
        self.stackedWidget_claim_road.addWidget(self.state_claim_road_question)

        # state claim road confirm
        self.state_claim_road_confirm = QtWidgets.QWidget()
        self.state_claim_road_confirm.setObjectName("state_claim_road_confirm")
        self.verticalLayoutWidget_claim_road_confirm = QtWidgets.QWidget(self.state_claim_road_confirm) # claim road widget
        self.verticalLayoutWidget_claim_road_confirm.setGeometry(QtCore.QRect(30, 10, 601, 91))
        self.verticalLayoutWidget_claim_road_confirm.setObjectName("verticalLayoutWidget_claim_road_confirm")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_claim_road_confirm)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_claim_road_cost = QtWidgets.QLabel(self.verticalLayoutWidget_claim_road_confirm)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_claim_road_cost.setFont(font)
        self.label_claim_road_cost.setAlignment(QtCore.Qt.AlignCenter)
        self.label_claim_road_cost.setContentsMargins(0, 10, 0, 0)
        self.label_claim_road_cost.setObjectName("label_claim_road_cost")
        self.verticalLayout.addWidget(self.label_claim_road_cost)
        self.textEdit_claim_road_background_3 = QtWidgets.QPlainTextEdit(self.state_claim_road_confirm)
        self.textEdit_claim_road_background_3.setGeometry(QtCore.QRect(-120, -40, 871, 191))
        self.textEdit_claim_road_background_3.setObjectName("textEdit_claim_road_background_3")
        self.textEdit_claim_road_background_3.raise_()
        self.verticalLayoutWidget_claim_road_confirm.raise_()
        self.stackedWidget_claim_road.addWidget(self.state_claim_road_confirm)

        # state claim road reject
        self.state_claim_road_reject = QtWidgets.QWidget()
        self.state_claim_road_reject.setObjectName("state_claim_road_reject")
        self.verticalLayoutWidget_claim_road_reject = QtWidgets.QWidget(self.state_claim_road_reject) # claim road widget
        self.verticalLayoutWidget_claim_road_reject.setGeometry(QtCore.QRect(30, 10, 601, 91))
        self.verticalLayoutWidget_claim_road_reject.setObjectName("verticalLayoutWidget_claim_road_reject")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_claim_road_reject)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_claim_road_cost_reject = QtWidgets.QLabel(self.verticalLayoutWidget_claim_road_reject)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_claim_road_cost_reject.setFont(font)
        self.label_claim_road_cost_reject.setAlignment(QtCore.Qt.AlignCenter)
        self.label_claim_road_cost_reject.setContentsMargins(0, 10, 0, 0)
        self.label_claim_road_cost_reject.setObjectName("label_claim_road_cost_reject")
        self.verticalLayout.addWidget(self.label_claim_road_cost_reject)
        self.textEdit_claim_road_background_3 = QtWidgets.QPlainTextEdit(self.state_claim_road_reject)
        self.textEdit_claim_road_background_3.setGeometry(QtCore.QRect(-120, -40, 871, 191))
        self.textEdit_claim_road_background_3.setObjectName("textEdit_claim_road_background_3")
        self.textEdit_claim_road_background_3.raise_()
        self.verticalLayoutWidget_claim_road_reject.raise_()
        self.stackedWidget_claim_road.addWidget(self.state_claim_road_reject)

        self.layoutWidget.raise_()
        self.button_draw_destination.raise_()
        self.pushButton_mytickets.raise_()
        self.label_opponent_info.raise_()
        self.text_opponent_tickets.raise_()
        self.text_opponent_cards.raise_()
        self.verticalLayoutWidget_claim_road_confirm.raise_()
        # self.verticalLayoutWidget_claim_road_reject.raise_()
        self.stackedwidget_select_ticket.raise_()
        self.verticalLayoutWidget_2.raise_()
        self.layoutWidget_mycards.raise_()


        self.retranslateUi(Form)
        self.stackedwidget_select_ticket.setCurrentIndex(1)
        self.pushButton_mytickets.toggled['bool'].connect(self.label_ticket1.setHidden) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Form)

        # display select_ticket state or game state depending on the player move
        if select_ticket is True:
            self.stackedwidget_select_ticket.setCurrentWidget(self.state_select_ticket)
        else:
            self.stackedwidget_select_ticket.setCurrentWidget(self.state_game)

        # display empty claim road stackedwidget
        self.stackedWidget_claim_road.setCurrentWidget(self.state_claim_road_empty)
        
        
        # Add the MplCanvas widget to the layout
        self.fig = Figure(figsize=(12, 6))
        self.ax = self.fig.add_subplot(111)
        self.canvas = MplCanvas(self)
        self.label_board.setLayout(QVBoxLayout())
        self.label_board.layout().addWidget(self.canvas)
        self.img = imread("data/USA_map.jpg") # load board
        self.get_plot()
    
        # Create buttons for each node
        self.button_map = {}
        for node, (x, y) in CITY_LOCATIONS.items():
            button = QtWidgets.QPushButton(Form)
            button.setGeometry(QtCore.QRect(int(x * self.img.shape[1]) + 165, int((1-0.9*y) * self.img.shape[0]) - 50, 20, 20))
            button.setCheckable(True)
            button.setStyleSheet("QPushButton" # default button style
                                 "{"
                                 "background-color: rgba(64, 235, 127, 1);"
                                 "border-radius: 10px;\n"
                                 "border: 2px solid #555"
                                 "}"
                                 "QPushButton:checked" # button style when pressed
                                 "{" 
                                 "background-color: #73cbdf;"
                                 "}"
                                 "QPushButton:hover" # button style when hovered over
                                 "{"
                                 "background-color: #73cbdf;"
                                 "}"
            )
            self.button_map[node] = button
            

    # create buttons with styles 
    def create_button(self, name, color, text_color="white"):
        button = QtWidgets.QPushButton(self.layoutWidget_mycards)
        button.setMinimumSize(QtCore.QSize(60, 60))
        button.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        button.setFont(font)
        button.setStyleSheet(f"background-color: {color}; color: {text_color}")
        button.setObjectName(name)
        # button.setFocusPolicy(Qt.NoFocus) #test
        self.horizontalLayout_mycards.addWidget(button)
        return button

    def get_plot(self):
        player_1_edges = self.player1_routes
        # player_2_edges = {(EDGES[i][0],EDGES[i][1]):(EDGES[i][2],EDGES[i][3]) for i in range(0,10)} #test
        player_2_edges = self.player2_routes

        # Build graph to plot the current game situation
        taken_vertices = {edge[j] for edge in player_1_edges for j in range(2)}
        taken_vertices.update({edge[j] for edge in player_2_edges for j in range(2)})

        # Build bidirectional weighted graph from both players' taken VERTICES and EDGES
        G1 = nx.MultiGraph()  # for player 1 and other plots
        G1.add_nodes_from(taken_vertices)  # add vertices

        G2 = nx.MultiGraph()  # just for player 2 edges
        G2.add_nodes_from(taken_vertices)  # add vertices

        for (node1, node2), (weight, color) in player_1_edges.items():
            G1.add_edge(node1, node2, weight=int(weight), color=color)  # add edges

        for (node1, node2), (weight, color) in player_2_edges.items():
            G2.add_edge(node1, node2, weight=int(weight), color=color)  # add edges
        
        self.plot(G1, 'player_1')
        self.plot(G2, 'player_2')

    def plot(self, G, player):
        # Load and plot the background image
        self.canvas.ax.imshow(self.img, extent=[0, self.img.shape[1], 0, self.img.shape[0]], aspect='auto') # show image
        self.canvas.ax.axis('off')  # Hide x and y axis

        player_color = 'blue' if player == 'player_1' else 'red'

        pos = CITY_LOCATIONS
        y, x, z = np.shape(self.img) # get image size

        POS_REFLECTED = {k: (v[0] * x, v[1] * y) for k, v in pos.items()}
        # nx.draw_networkx_nodes(G, POS_REFLECTED, ax=self.canvas.ax, node_color=PINK, node_size=50)
        # nx.draw_networkx_edges(G, POS_REFLECTED, width=6, ax=self.canvas.ax, edge_color=player_color, alpha=0.8)

        # edge_labels = nx.get_edge_attributes(G, "color")
        # nx.draw_networkx_edge_labels(G, POS_REFLECTED, edge_labels, ax=self.canvas.ax, rotate=False, bbox=dict(alpha=0), horizontalalignment='right')
        
        # optional for fancy arrows (alternative plot is all 4 lines above, unmark them)
        with open('data/road_curvature.txt') as f:
                next(f) # skipping header
                # get data as (node1, node2): curvature
                curvature = {(nodes[0], nodes[1]): float(nodes[2]) for line in f if (nodes := line.strip().split(','))}

        for u, v in G.edges():
                # Check if (u, v) exists in curvature dictionary
                if (u, v) in curvature:
                        # Get the curvature value for (u, v)
                        curv = curvature[(u, v)]
                        # if u,v is same order as in G.edges, get its order
                        node1 = POS_REFLECTED[u]
                        node2 = POS_REFLECTED[v]
                elif (v, u) in curvature:  # Check if (v, u) exists for reversed direction
                        # Get the curvature value for (v, u)
                        curv = curvature[(v, u)]
                        # if u,v is opposite order as in G.edges, flip its order
                        node1 = POS_REFLECTED[v]
                        node2 = POS_REFLECTED[u]

                # optional plot for 2 curvy paths with concavity changing
                if ((u,v) == ("Chicago","Toronto") or (v,u) == ("Chicago","Toronto")):
                        node1 = POS_REFLECTED["Chicago"]
                        node2 = POS_REFLECTED["Toronto"]
                        mid_point = ((node1[0]+node2[0]) / 2, (node1[1]+node2[1]) / 2 + 8)
                        arrow1 = FancyArrowPatch(node1, mid_point,
                                                connectionstyle="arc3,rad=-0.4", 
                                                linewidth=4,
                                                color=player_color)
                        arrow2 = FancyArrowPatch(mid_point, node2,
                                connectionstyle="arc3,rad=0.2", 
                                linewidth=4,
                                color=player_color)
                        self.canvas.ax.add_patch(arrow1)
                        self.canvas.ax.add_patch(arrow2)
                        
                elif (u,v) == ("Nashville","Pittsburgh") or (v,u) == ("Nashville","Pittsburgh"):
                        node1 = POS_REFLECTED["Nashville"]
                        node2 = POS_REFLECTED["Pittsburgh"]
                        mid_point = ((node1[0]+node2[0]) / 2, (node1[1]+node2[1]) / 2 + 5)
                        arrow1 = FancyArrowPatch(node1, mid_point,
                                                connectionstyle="arc3,rad=-0.4", 
                                                linewidth=4,
                                                color=player_color)
                        arrow2 = FancyArrowPatch(mid_point, node2,
                                connectionstyle="arc3,rad=0.2", 
                                linewidth=4,
                                color=player_color)
                        self.canvas.ax.add_patch(arrow1)
                        self.canvas.ax.add_patch(arrow2)

                else:
                        arrow = FancyArrowPatch(node1, node2,
                                                connectionstyle=f"arc3,rad={curv}", 
                                                linewidth=4,
                                                color=player_color)
                        self.canvas.ax.add_patch(arrow)

        # Refresh canvas
        self.canvas.draw()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

        # current player info
        self.current_player.setText(_translate("Form", f"{self.player}'s turn"))


        #labels of train cards
        self.label_mycards.setText(_translate("Form", "My Cards:   \nOpponent's:")) # test. remove 2nd parts from this line and below lines
        self.button_train_red.setText(_translate("Form", str(self.train_count['red'])+f"\n{self.train_count2['red']}"))
        self.button_train_green.setText(_translate("Form", str(self.train_count['green'])+f"\n{self.train_count2['green']}"))
        self.button_train_blue.setText(_translate("Form", str(self.train_count['blue'])+f"\n{self.train_count2['blue']}"))
        self.button_train_orange.setText(_translate("Form", str(self.train_count['orange'])+f"\n{self.train_count2['orange']}"))
        self.button_train_yellow.setText(_translate("Form", str(self.train_count['yellow'])+f"\n{self.train_count2['yellow']}"))
        self.button_train_black.setText(_translate("Form", str(self.train_count['black'])+f"\n{self.train_count2['black']}"))
        self.button_train_white.setText(_translate("Form", str(self.train_count['white'])+f"\n{self.train_count2['white']}"))
        self.button_train_purple.setText(_translate("Form", str(self.train_count['purple'])+f"\n{self.train_count2['purple']}"))
        self.button_train_rainbow.setText(_translate("Form", str(self.train_count['rainbow'])+f"\n{self.train_count2['rainbow']}"))

        # draw button
        self.button_draw_train.setText(_translate("Form", f"Draw Card ({self.draw_ticket_number})"))
        self.button_draw_destination.setText(_translate("Form", "Draw Tickets"))
        self.pushButton_mytickets.setText(_translate("Form", "My Tickets (show/hide)"))
        

        # player1 tickets
        self.label_ticket1.setText(_translate("Form", self.ticket_cards_text))

        # write names of ticket options
        self.label_state_select_ticket.setText("SELECT AT LEAST 2 TICKETS")
        self.label_ticket_option1.setText(_translate("Form", self.ticket_options_player1_text[0]))
        self.label_ticket_option2.setText(_translate("Form", self.ticket_options_player1_text[1])) 
        self.label_ticket_option3.setText(_translate("Form", self.ticket_options_player1_text[2]))
        self.button_ticket_option_okay.setText(_translate("Form", "OK"))

        # write names of claim road labels/buttons
        self.label_claim_road_select_color.setText(_translate("Form", " SELECT COLOR OF THE PATH YOU WANT"))
        self.textEdit_claim_road_question_select_cities.setText(_translate("Form", "SELECTING DENVER-CALGARY"))
        self.label_claim_road_question_cost.setText(_translate("Form", "IT WILL COST YOU AN ARM AND LEG"))
        self.label_claim_road_cost.setText(_translate("Form", "IT\'LL COST YOU 3 CARDS (2 Green + 1 Rainbow)"))

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=12, height=6, dpi=100):
        self.fig = Figure(figsize=(width, height))
        self.ax = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)

class Game_Board_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize the UI form
        self.ui = Ui_Form_Game_Board()
        self.ui.setupUi(self)  # Setup the UI inside the main window

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = Game_Board_Window()
    main_window.show()
    sys.exit(app.exec_())
