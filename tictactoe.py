#!/usr/bin/python

# a collection of analysis tools for the game of Tic Tac Toe, developed by Nikki
# this file handles only the main menu itself, and calls everything as needed from here
# TODO: make game.py work better; create stats function; display generation progress

from datagathering import *
from generate import generate_boards


def menu(game):
	"""lets the user examine tic tac toe boards by a variety of methods until they quit"""

	helpText = (
				"\nCommands are noted by the character to enter inside a pair of brackest ex. (S) means the (S)tats command"
				"\nThough they are listed in uppercase, commands can be typed in lowercase too"
				"\nYou can enter multiple commands at once by seperating them with a space"
				"\nIf there are any display issues, try changing the (B)oards Per Line value by entering a number after it ex. \"B5\""
				"\nThe default value is 7 and if that isn't right, you'll have to experiment with it"
				"\n\nEnter a number to see layouts for those turns (0 through 9), or view (A)ll at once"
				"\nYou can enter a turn number followed by a \"-\" and a specific board number to see only that board ex. \"3-24\""
				"\nEnter \":\" and another board number after that to inclusively show all boards inbetween those ex. \"6-8:20\""
				"\n\n(P)aths Display will enable/disable printing out what moves will lead to in the next turn"
				"\n(W)in Check will enable/disable printing out if the current board is a winning or tied move"
				"\n\n(X) or (O) will display their respective their winning moves, and you can also look at (T)ies"
				"\n(E)nds will show all endings, both wins and ties, and entering a number after E will show endings on only those turns"
				"\n\n(S)tats will show you general aggregated stats for tic tac toe"
				"\nA (G)ame of tic tac toe is also available, against another human or AI!"
				"\n\nAt any time you can (Q)uit"
				)
	paths = False
	showWin = False
	quit = False
	boardsPerLine = 7

	while not quit:

		choice = raw_input("\nEnter a command (enter 'C' for a list of commands)\n> ").upper()
		for c in choice.split(' '):

			if len(c) == 0 or quit:
				continue

			if c == 'Q':
				quit = True
			elif c == 'C':
				print helpText
			elif c == 'G':
				play_game(game)
			elif c == 'S':
				print stats(game)

			# prints every layout for a given turn
			elif c.isdigit():
				for t in c:
					print "\n\nShowing all possible states for Turn %s:" % t
					print make_boards(game[int(t)], paths, showWin, boardsPerLine)
			# prints every layouts possible
			elif c == 'A':
				for t in range(0, 10):
					print "\n\nShowing all possible states for Turn %s:" % t
					print make_boards(game[t], paths, showWin, boardsPerLine)
			# prints a single layout, or a selected range of layouts
			elif len(c) >= 3 and c[1] == '-':
				rangeSelected = True
				if ':' not in c:
					rangeSelected = False
					c = c + ':' + c[2:]
				output, success = make_range(game, c, paths, showWin, boardsPerLine)
				if success:
					print("\n\nShowing a %sstate%s from Turn %s:" 
							% ("selection of " * rangeSelected, 's' * rangeSelected, c[0]))
				print output

			# displays selective game endings
			elif c[0] == 'E' and (len(c) == 1 or ( len(c) >= 1 and c[1:].isdigit() )):
				if c[1:].isdigit():
					chosen = []
					for t in c[1:]:
						chosen.append(game[int(t)])
					print show_wins(chosen, boardsPerLine=boardsPerLine)
				# displays all game endings
				else:
					print show_wins(game[5:10], boardsPerLine=boardsPerLine)
			elif c == 'X':
				print show_wins(game[5:10], 'X', False, boardsPerLine)
			elif c == 'O':
				print show_wins(game[5:10], 'O', False, boardsPerLine)
			elif c == 'T':
				print show_wins(game[5:10], '', True, boardsPerLine)

			elif c == 'P':
				paths = not paths
				if paths:
					print "\nGame Paths will now be shown."
				else:
					print "\nGame Paths will no longer be shown."
			elif c == 'W':
				showWin = not showWin
				if showWin:
					print "\nDisplayed boards will now check for a Winning game."
				else:
					print "\nDisplayed boards will no longer check for a Winning game."

			elif c[0] == 'B':
				if c[1:].isdigit() and int(c[1:]) != 0:
					boardsPerLine = int(c[1:])
					print("\nUp to %s Board%s will be printed on a single line at once." 
						% (boardsPerLine, 's' * bool(boardsPerLine-1)))
				elif c[1:].isdigit():
					print "\nYou cannot enter 0 for Boards Per Line."
				else:
					print "\nYou must enter a number to change Boards Per Line, not %s" % c
			else:
				print "\n'%s' is not valid input." % c

# launchs the program after generating the full tic tac toe database
menu(generate_boards())