#!/usr/bin/python

# plays a game of tic tac toe, given data from ttt.py

import random
from board import Board


def get_input(msg, wanted):
    """keeps the user in a loop until they enter wanted input"""
    while True:
        entry = raw_input("%s\n" % msg).upper()
        if entry not in wanted:
            print "Incorrect entry. You must enter one of: %s\n" % wanted
        else: 
            return entry


def set_players():
    """sets the players for a game of tic tac toe as human and/or AI"""
    players = ['first', 'second']
    for x in range(len(players)):
        players[x] = get_input("Is the %s player a (H)uman, or a (C)omputer?" % players[x], ['H', 'C'])
    return players


def human_turn(player, layout):
    """manages a turn from a human player, and returns the position they are playing on"""

    goodInput = False
    # loops until valid input is given
    while not goodInput:
        move = raw_input("\nChoose a spot to play on, player %s. Enter a number from 1 to 9.\n" % player)
        if not move.isdigit():
            print "You must enter a valid number."
        else:
            # move needs to fit into an array
            move = int(move) - 1
            if move < 0 or move > 8:
                print "You have to enter a number from 1 to 9."
            elif layout[move] != ' ':
                print "That spot is taken."
            else:
                goodInput = True
    return move


def ai_turn(layout):
    """simulates a turn by the computer by making an absolutely random move"""

    available = []
    for pos in range(9):
        if layout[pos] == ' ':
            available.append(pos)
    move = available[random.randint(0, len(available) - 1)]
    return move


def play_game(game):
    """plays a game of tic tac toe with humans and/or AI"""

    # first game or a restart
    setPlayers = True
    # whether or not to list paths that can be reached
    paths = False

    donePlaying = False
    # loops through games until the user is done playing
    while not donePlaying:

        if setPlayers:
            setPlayers = False
            players = set_players()
            # whether paths will be shown or not
            if get_input("Do you want to show game path solutions? (Y)es or (N)o", ['Y', 'N']) == 'Y':
                paths = True

        # the game currently in play
        gameState = Board('         ', 1)
        gameState.paths = game[0][0].paths
        turnNum = 0

        # loops until the game is won
        while not gameState.check_win()[0] and gameState.what_turn() != 9:

            print gameState.make_board(paths)

            # gets the character for the current player
            if turnNum % 2 == 0:
                player = 'X'
            else:
                player = 'O'
            # human move
            if players[turnNum % 2] == 'H':
                move = human_turn(player, gameState)
            # AI controlled move
            else:
                move = ai_turn(gameState)
                raw_input("\nComputer player %s has made their move. Press enter to see it.\n" % player)

            # re-makes the board with new information
            gameState = Board(gameState[0:move] + player + gameState[move + 1:9])

            for layout in game[gameState.what_turn()]:
                if layout.matches(gameState):
                    gameState.pattern = layout.pattern

                    # won't continue if there are no paths to show
                    if len(layout.paths) == 9:

                        l = Board(layout, layout.pattern, layout.paths)

                        # goes through every possible rotation of the board to correctly set the paths
                        for rots in range(8):
                            if l.make_board(False) == gameState.make_board(False):
                                gameState.paths = l.paths
                                break

                            p = l.paths
                            # rotates the board and the paths
                            l = Board(l.rotate(), l.pattern, 
                                      [p[6], p[3], p[0], p[7], p[4], p[1], p[8], p[5], p[2]])
                            if rots == 3:
                                p = l.paths
                                # mirrors the board and the paths
                                l = Board(l.mirror(), l.pattern, 
                                          [p[2], p[1], p[0], p[5], p[4], p[3], p[8], p[7], p[6]])

            turnNum += 1

        # prints the winning or tied board
        print gameState.make_board(showWin = True)

        again = get_input("\n(R)ematch, (C)hange players / toggle paths display, or go (B)ack?", 'R C B'.split())
        if again == 'B':
            donePlaying = True
        elif again == 'C':
            setPlayers = True