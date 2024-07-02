from PyQt5 import QtCore, QtGui, QtWidgets
from functions import EDGES, CITY_LOCATIONS
import networkx as nx
from matplotlib.image import imread
import numpy as np
from PyQt5.QtWidgets import QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys

class Ui_Form_Game_Board(object):
    def setupUi(self, Form, train_cards, ticket_cards, button_colors, ticket_options_player1, select_ticket, draw_ticket_number):
        Form.setObjectName("Form")
        Form.resize(1330, 875)
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(130, 660, 1011, 100))
        self.layoutWidget.setObjectName("layoutWidget")

        # display player's train cards at bottom
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(180, 0, 170, 80) # adjust card locations
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_mycards = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_mycards.setFont(font)
        self.label_mycards.setObjectName("label_mycards")
        self.horizontalLayout.addWidget(self.label_mycards)
        self.button_train_red = QtWidgets.QPushButton(self.layoutWidget)
        self.button_train_red.setMinimumSize(QtCore.QSize(60, 60))
        self.button_train_red.setMaximumSize(QtCore.QSize(60, 60))

        self.train_count = {i:train_cards.count(i) \
                       for i in list('blue red green yellow black orange purple white rainbow'.split())}
        rainbow_gradient = "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 0, 0, 255), \
            stop:0.166 rgba(255, 255, 0, 255), stop:0.333 rgba(0, 255, 0, 255), stop:0.5 rgba(0, 255, 255, 255), \
            stop:0.666 rgba(0, 0, 255, 255), stop:0.833 rgba(255, 0, 255, 255), stop:1 rgba(255, 0, 0, 255)); color:black"
        font = QtGui.QFont()
        font.setPointSize(20)
        self.button_train_red.setFont(font)
        self.button_train_red.setStyleSheet("background-color: red;")
        self.button_train_red.setAutoRepeatDelay(300)
        self.button_train_red.setObjectName("button_train_red")
        self.horizontalLayout.addWidget(self.button_train_red)
        self.button_train_green = QtWidgets.QPushButton(self.layoutWidget)
        self.button_train_green.setMinimumSize(QtCore.QSize(0, 60))
        self.button_train_green.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.button_train_green.setFont(font)
        self.button_train_green.setStyleSheet("background-color: green; color: white")
        self.button_train_green.setObjectName("button_train_green")
        self.horizontalLayout.addWidget(self.button_train_green)
        self.button_train_blue = QtWidgets.QPushButton(self.layoutWidget)
        self.button_train_blue.setMinimumSize(QtCore.QSize(0, 60))
        self.button_train_blue.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.button_train_blue.setFont(font)
        self.button_train_blue.setStyleSheet("background-color: blue; color: white")
        self.button_train_blue.setObjectName("button_train_blue")
        self.horizontalLayout.addWidget(self.button_train_blue)
        self.button_train_orange = QtWidgets.QPushButton(self.layoutWidget)
        self.button_train_orange.setMinimumSize(QtCore.QSize(0, 60))
        self.button_train_orange.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.button_train_orange.setFont(font)
        self.button_train_orange.setStyleSheet("background-color: orange")
        self.button_train_orange.setObjectName("button_train_orange")
        self.horizontalLayout.addWidget(self.button_train_orange)
        self.button_train_yellow = QtWidgets.QPushButton(self.layoutWidget)
        self.button_train_yellow.setMinimumSize(QtCore.QSize(0, 60))
        self.button_train_yellow.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.button_train_yellow.setFont(font)
        self.button_train_yellow.setStyleSheet("background-color: yellow;")
        self.button_train_yellow.setObjectName("button_train_yellow")
        self.horizontalLayout.addWidget(self.button_train_yellow)
        self.button_train_black = QtWidgets.QPushButton(self.layoutWidget)
        self.button_train_black.setMinimumSize(QtCore.QSize(0, 60))
        self.button_train_black.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setUnderline(False)
        self.button_train_black.setFont(font)
        self.button_train_black.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.button_train_black.setStyleSheet("background-color: black; color: white")
        self.button_train_black.setObjectName("button_train_black")
        self.horizontalLayout.addWidget(self.button_train_black)
        self.button_train_white = QtWidgets.QPushButton(self.layoutWidget)
        self.button_train_white.setMinimumSize(QtCore.QSize(0, 60))
        self.button_train_white.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.button_train_white.setFont(font)
        self.button_train_white.setStyleSheet("background-color: white")
        self.button_train_white.setObjectName("button_train_white")
        self.horizontalLayout.addWidget(self.button_train_white)
        self.button_train_purple = QtWidgets.QPushButton(self.layoutWidget)
        self.button_train_purple.setMinimumSize(QtCore.QSize(0, 60))
        self.button_train_purple.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.button_train_purple.setFont(font)
        self.button_train_purple.setStyleSheet("background-color: purple; color: white")
        self.button_train_purple.setObjectName("button_train_purple")
        self.horizontalLayout.addWidget(self.button_train_purple)
        self.button_train_rainbow = QtWidgets.QPushButton(self.layoutWidget)
        self.button_train_rainbow.setMinimumSize(QtCore.QSize(0, 60))
        self.button_train_rainbow.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.button_train_rainbow.setFont(font)
        self.button_train_rainbow.setStyleSheet(f"background-color: {rainbow_gradient}")
        self.button_train_rainbow.setObjectName("button_train_rainbow")
        self.horizontalLayout.addWidget(self.button_train_rainbow)
        self.layoutWidget1 = QtWidgets.QWidget(Form)
        self.layoutWidget1.setGeometry(QtCore.QRect(1201, 52, 102, 592))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")


        # right widget (draw destination and display cards)
        button_colors_rename = [i if i != 'rainbow' else "qlineargradient(spread:pad, x1:0, \
                               y1:0, x2:1, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.166 rgba(255, 255, 0, 255), \
                               stop:0.333 rgba(0, 255, 0, 255), stop:0.5 rgba(0, 255, 255, 255), stop:0.666 \
                               rgba(0, 0, 255, 255), stop:0.833 rgba(255, 0, 255, 255), stop:1 rgba(255, 0, 0, 255))" \
                               for i in button_colors]
        self.draw_ticket_number = draw_ticket_number # get total number of train cards on the draw pile
        
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
        self.layoutWidget2.setGeometry(QtCore.QRect(20, 50, 91, 600))
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
        self.label_opponent_info = QtWidgets.QLabel(Form)
        self.label_opponent_info.setGeometry(QtCore.QRect(40, 520, 131, 31))
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(50, 560, 101, 100))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_opponent_info = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_opponent_info.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_opponent_info.setObjectName("verticalLayout_opponent_info")
        self.label_opponent_info = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_opponent_info.setFont(font)
        self.label_opponent_info.setObjectName("label_opponent_info")
        self.verticalLayout_opponent_info.addWidget(self.label_opponent_info)
        self.text_opponent_tickets = QtWidgets.QTextEdit(self.verticalLayoutWidget_2)
        self.text_opponent_tickets.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.text_opponent_tickets.setObjectName("text_opponent_tickets")
        self.verticalLayout_opponent_info.addWidget(self.text_opponent_tickets)
        self.text_opponent_cards = QtWidgets.QTextEdit(self.verticalLayoutWidget_2)
        self.text_opponent_cards.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.text_opponent_cards.setObjectName("text_opponent_cards")
        self.verticalLayout_opponent_info.addWidget(self.text_opponent_cards)


        # player (my) tickets
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 95, 150, 450)) 
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutWidget.setStyleSheet("background-color: white;")  # Debugging (try to remove unnecessary rectangle on left)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 10, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # add destination tickets names
        ticket_cards_format = [f"<li>{i[0]} - {i[1]} {i[2]}</li>" for i in ticket_cards] 
        self.ticket_cards_text = f"<ul>{''.join(ticket_cards_format)}</ul>" # get player1 tickets as bullet list text
        self.label_ticket1 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_ticket1.setWordWrap(True)
        self.label_ticket1.setObjectName("label_ticket1")
        self.verticalLayout_2.addWidget(self.label_ticket1)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)


        # select destination ticket
        self.stackedWidget = QtWidgets.QStackedWidget(Form)
        self.stackedWidget.setGeometry(QtCore.QRect(440, 10, 581, 121))
        self.stackedWidget.setObjectName("stackedWidget_board")

        self.state_game = QtWidgets.QWidget()
        self.state_game.setObjectName("state_game")
        self.stackedWidget.addWidget(self.state_game)


        # set and display ticket options to player1
        self.ticket_options_player1_text = [f"{i[0]}-{i[1]} {i[2]}" for i in ticket_options_player1]

        self.state_select_ticket = QtWidgets.QWidget()
        self.state_select_ticket.setObjectName("state_select_ticket")
        self.button_ticket_option1 = QtWidgets.QPushButton(self.state_select_ticket)
        self.button_ticket_option1.setGeometry(QtCore.QRect(50, 40, 141, 41))
        self.button_ticket_option1.setCheckable(True)
        self.button_ticket_option1.setObjectName("pushButton_ticket_option1")
        self.textEdit_state_select_ticket = QtWidgets.QTextEdit(self.state_select_ticket)
        self.textEdit_state_select_ticket.setGeometry(QtCore.QRect(130, 0, 291, 41))
        self.textEdit_state_select_ticket.setObjectName("textEdit_state_select_ticket")
        self.button_ticket_option2 = QtWidgets.QPushButton(self.state_select_ticket)
        self.button_ticket_option2.setGeometry(QtCore.QRect(210, 40, 141, 41))
        self.button_ticket_option2.setCheckable(True)
        self.button_ticket_option2.setObjectName("pushButton_ticket_option2")
        self.button_ticket_option3 = QtWidgets.QPushButton(self.state_select_ticket)
        self.button_ticket_option3.setGeometry(QtCore.QRect(370, 40, 141, 41))
        self.button_ticket_option3.setCheckable(True)
        self.button_ticket_option3.setObjectName("pushButton_ticket_option3")
        self.button_ticket_option_okay = QtWidgets.QPushButton(self.state_select_ticket)
        self.button_ticket_option_okay.setGeometry(QtCore.QRect(240, 90, 75, 23))
        self.button_ticket_option_okay.setObjectName("pushButton_ticket_option_okay")
        self.stackedWidget.addWidget(self.state_select_ticket)



        self.layoutWidget.raise_()
        self.button_draw_destination.raise_()
        self.pushButton_mytickets.raise_()
        self.label_opponent_info.raise_()
        self.text_opponent_tickets.raise_()
        self.text_opponent_cards.raise_()
        self.verticalLayoutWidget.raise_()
        self.stackedWidget.raise_()
     

        self.retranslateUi(Form)
        self.stackedWidget.setCurrentIndex(1)
        self.pushButton_mytickets.toggled['bool'].connect(self.label_ticket1.setHidden) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Form)

        # display select_ticket state or game state depending on the player move
        if select_ticket is True:
            self.stackedWidget.setCurrentWidget(self.state_select_ticket)
        else:
            self.stackedWidget.setCurrentWidget(self.state_game)

        # Add the MplCanvas widget to the layout
        self.fig = Figure(figsize=(12, 6))
        self.ax = self.fig.add_subplot(111)
        self.canvas = MplCanvas(self)
        self.label_board.setLayout(QVBoxLayout())
        self.label_board.layout().addWidget(self.canvas)
        self.get_plot()

    def get_plot(self):
        player_1_edges = [EDGES[i] for i in range(10)]
        player_2_edges = [EDGES[i] for i in range(20, 32)]

        # Build graph to plot the current game situation
        taken_vertices = {edge[j] for edge in player_1_edges for j in range(2)}
        taken_vertices.update({edge[j] for edge in player_2_edges for j in range(2)})

        # Build bidirectional weighted graph from both players' taken VERTICES and EDGES
        G1 = nx.MultiGraph()  # for player 1 and other plots
        G1.add_nodes_from(taken_vertices)  # add vertices

        G2 = nx.MultiGraph()  # just for player 2 edges
        G2.add_nodes_from(taken_vertices)  # add vertices

        for edge in player_1_edges:
            G1.add_edge(edge[0], edge[1], weight=int(edge[2]), color=edge[3])  # add edges

        for edge in player_2_edges:
            G2.add_edge(edge[0], edge[1], weight=int(edge[2]), color=edge[3])  # add edges
        
        self.plot(G1, 'player_1')
        self.plot(G2, 'player_2')

    def plot(self, G, player):
        # Load and plot the background image
        img = imread("data/USA_map.jpg")
        self.canvas.ax.imshow(img, extent=[0, img.shape[1], 0, img.shape[0]], aspect='auto')
        PINK = '#fd6cee'
        player_color = 'blue' if player == 'player_1' else 'red'

        pos = CITY_LOCATIONS
        y, x, z = np.shape(img)

        POS_REFLECTED = {k: (v[0] * x, v[1] * y) for k, v in pos.items()}
        nx.draw_networkx_nodes(G, POS_REFLECTED, ax=self.canvas.ax, node_color=PINK, node_size=100)
        nx.draw_networkx_edges(G, POS_REFLECTED, width=8, ax=self.canvas.ax, edge_color=player_color, alpha=0.8)
        edge_labels = nx.get_edge_attributes(G, "color")
        nx.draw_networkx_edge_labels(G, POS_REFLECTED, edge_labels, ax=self.canvas.ax, rotate=False, bbox=dict(alpha=0), horizontalalignment='right')

        # Refresh canvas
        self.canvas.draw()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

        #labels of train cards
        self.label_mycards.setText(_translate("Form", "My Cards:"))
        self.button_train_red.setText(_translate("Form", str(self.train_count['red'])))
        self.button_train_green.setText(_translate("Form", str(self.train_count['green'])))
        self.button_train_blue.setText(_translate("Form", str(self.train_count['blue'])))
        self.button_train_orange.setText(_translate("Form", str(self.train_count['orange'])))
        self.button_train_yellow.setText(_translate("Form", str(self.train_count['yellow'])))
        self.button_train_black.setText(_translate("Form", str(self.train_count['black'])))
        self.button_train_white.setText(_translate("Form", str(self.train_count['white'])))
        self.button_train_purple.setText(_translate("Form", str(self.train_count['purple'])))
        self.button_train_rainbow.setText(_translate("Form", str(self.train_count['rainbow'])))


        self.button_draw_train.setText(_translate("Form", f"Draw Card ({self.draw_ticket_number})"))
        self.button_draw_destination.setText(_translate("Form", "Draw Tickets"))
        self.pushButton_mytickets.setText(_translate("Form", "My Tickets (show/hide)"))
        self.label_opponent_info.setText(_translate("Form", "Opponent info"))
        self.text_opponent_tickets.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">5 Tickets</span></p></body></html>"))
        self.text_opponent_cards.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">4 Cards</span></p></body></html>"))
        # self.label_ticket1.setText(_translate("Form", self.ticket_cards_text))
        self.label_ticket1.setText(_translate("Form", self.ticket_cards_text))

        # write names of ticket options
        self.button_ticket_option1.setText(_translate("Form", self.ticket_options_player1_text[0]))
        self.textEdit_state_select_ticket.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">SELECT AT LEAST 2 TICKETS</span></p></body></html>"))
        self.button_ticket_option2.setText(_translate("Form", self.ticket_options_player1_text[1]))
        self.button_ticket_option3.setText(_translate("Form", self.ticket_options_player1_text[2]))
        self.button_ticket_option_okay.setText(_translate("Form", "OK"))

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
