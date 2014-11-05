#!/usr/bin/python

# generates and stores information on every possible, legal, and unique board layout for a game of tic tac toe

from board import Board

def generate_boards():
    """
    generates layouts for every turn reachable in tic tac toe and stores unique ones
    as well as noting the branching paths between them
    """

    print "Generating data, please hold on..."
    # a list for turns, each which is a list of boards, which are unique layouts
    # a completely blank layout is always the start of the game, counting for turn 0
    game = [[Board(' ' * 9, 1)]]

    # there are at most 9 turns in a game of tic tac toe
    for turnNum in range(1, 10):
        # list of layouts for the current turn
        turn = []
        upperLayouts = game[-1]

        if turnNum % 2 == 1: player = 'X'
        else: player = 'O'

        # every turns' unique layouts are numbered to seperate them more easily
        pattern = 1
        # goes through every layout from the previous turn
        for ul in upperLayouts:
            # game does not continue after a winning move, and using a won board is only possible after turn 5
            if turnNum <= 5 or not ul.check_win()[0]:
                # 9 positions on every board
                for pos in range(9):
                    if ul[pos] == ' ':
                        newLayout = Board(ul[0:pos] + player + ul[pos+1:])
                        # if it is a unique layout
                        unique = True
                        # goes through every existing layout for this turn
                        for item in turn:
                            if newLayout.matches(item): 
                                unique = False
                                # the upper layout leads to an existing layout
                                ul.paths.append(item.pattern)
                                break
                        if unique:
                            turn.append(Board(newLayout, pattern))
                            # the current upper layout leads to the new layout
                            ul.paths.append(pattern)
                            pattern += 1
                    else:
                        # adds a zero for paths because a played character is taking up that space
                        ul.paths.append(0)
        game.append(turn)
    return game