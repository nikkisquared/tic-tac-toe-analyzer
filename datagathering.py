#!/usr/bin/python

# many functions to usefully organize given data for printing

import random
from board import Board
from game import play_game


def mult_boards(layouts, paths=False, showWin=False):
    """puts multiple boards on a single row, and returns them as a single string"""

    lines = []
    # there are 8 seperate lines of data for each board, but the last one is optional
    # each line will hold text for every layout given, by clumping them together
    for i in range(7 + 1 * showWin):
        lines.append("")

    # a completely formatted board has 8 lines
    for l in layouts:

        # if paths are to be displayed, this keeps track of them
        for row in range(3):
            line = row * 2
            for col in range(3):

                # offsets by 3 for every new row, and offsets by one more for each column
                toAdd = l[row * 3 + col]
                # if a layout finishes the game, there are no more paths leading from it
                if paths and toAdd == ' ' and not l.check_win()[0]:
                    toAdd = str(l.paths[row * 3 + col])

                # paths may be 1 to 3 digits, so this makes sure they displace empty spots properly
                if len(toAdd) == 1: lines[line] += " %s " % toAdd
                elif len(toAdd) == 2: lines[line] += " %s" % toAdd
                else: lines[line] += toAdd
                if col != 2: lines[line] += "|"
                if col == 2: lines[line] += "\t"

        lines[1] += "-----------\t"
        lines[3] += "-----------\t"
        lines[5] += "\t"
        lines[6] += "Layout %s-%s\t" % (l.what_turn(), l.pattern)

        if showWin:
            win, winner = l.check_win()
            if win:
                lines[7] += ("%s Wins\t\t" % winner)
            elif ' ' not in l:
                lines[7] += ("Tie game\t")
            else:
                lines[7] += ("No Win\t\t")

    # puts together the previously made lines and spaces them apart
    toPrint = "\n"
    for l in lines:
        toPrint += '\n' + l

    return toPrint


def make_boards(game, paths=False, showWin=False, boardsPerLine=7):
    """
    runs through many layouts and groups multiple boards together
    can print out branching paths, as well as limit the number of boards per line
    """
    toPrint = ""
    toAdd = []
    for layout in game:
        toAdd.append(layout)
        if len(toAdd) == boardsPerLine:
            # if toPrint is empty still, the first newline is cut off since it is unwanted
            toPrint += mult_boards(toAdd, paths, showWin)[1 * (not toPrint):] + "\n"
            toAdd = []
    # adds any boards left over
    if len(toAdd) > 0:
        toPrint += mult_boards(toAdd, paths, showWin)[1 * (not toPrint):]
    return toPrint


def make_range(game, selection, paths=False, showWin=False, boardsPerLine=7):
    """
    attempts to write out either a full set of boards based on the syntax X-Y:Z
    where X is the turn number, Y is the first board to show, and Z is the last board to show
    returns either the boards and True for success, or an error message and False
    """

    # will become false if bad input was given
    validInput = True
    turn = selection[0]
    layoutRange = selection.split('-')[1].split(':')
    firstLayout = layoutRange[0]
    lastLayout = layoutRange[1]

    if turn.isdigit() and firstLayout.isdigit() and lastLayout.isdigit():
        turn = int(turn)
        firstLayout = int(firstLayout)
        lastLayout = int(lastLayout)
        layoutMax = len(game[turn])

        if firstLayout == 0 or lastLayout == 0:
            validInput = False
            error = "\nYou cannot enter 0 for a layout number."
        elif firstLayout > lastLayout:
            validInput = False
            error = ("\nLayouts can only go from lower to higher, not from %s to %s."
                        % (firstLayout, lastLayout))
        elif firstLayout > layoutMax or lastLayout > layoutMax:
            validInput = False
            if firstLayout == lastLayout:
                error = ("\nThe highest layout for turn %s is %s, and you entered %s."
                            % (turn, len(game[turn]), firstLayout))
            else:
                error = ("\nThe highest layout for turn %s is %s, and you entered %s through %s."
                            % (turn, layoutMax, firstLayout, lastLayout))
    else:
        validInput = False
        error = "\nYou must to enter numbers to display boards, not %s." % selection

    if not validInput:
        output = error
    else:
        # firstLayout get -1 because layouts start at 1, but lastLayout is exclusive automatically
        # turn starts at 0 so it already matches the 0-indexing of arrays
        output = make_boards(game[turn][firstLayout-1:lastLayout], paths, showWin, boardsPerLine)

    return output, validInput


def show_wins(game, limit='XO', ties=True, boardsPerLine=7):
    """selects only winning and/or tied matches to display from any turns"""

    XWins = OWins = numTies = 0
    toShow = []
    toPrint = ""

    for turn in game:

        toPrint += "\n\nShowing endings for turn %s:\n" % turn[0].what_turn()
        for layout in turn:

            win, winner = layout.check_win()
            if win:
                if 'X' in limit and winner == 'X':
                    XWins += 1
                    toShow.append(layout)
                elif 'O' in limit and winner == 'O':
                    OWins += 1
                    toShow.append(layout)

            # ties can only happen on the 9th turn
            elif ties and layout.what_turn() == 9:
                numTies += 1
                toShow.append(layout)

        toPrint += make_boards(toShow, showWin=True, boardsPerLine=boardsPerLine)
        if toPrint and turn[0].what_turn() != 9:
            toPrint += "\n"
        toShow = []

    toPrint += "\n\n"

    if limit == 'XO' and ties:
        toPrint += "X Wins %s times, O Wins %s times, and there are %s Ties." % (XWins, OWins, numTies)
    elif 'X' in limit:
        toPrint += "X Wins %s times.\t" % XWins
    elif 'O' in limit:
        toPrint += "O Wins %s times.\t" % OWins
    elif ties:
        toPrint += "There are %s Ties." % numTies
    return toPrint


def stats(game):
    """creates and prints out varying stats about the game of tic tac toe"""
    pass