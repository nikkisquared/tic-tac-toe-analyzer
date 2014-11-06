#!/usr/bin/python

# analysis tools for the game of tic tac toe, developed by Nikki
# TODO: create stats function; display generation progress; why is there an extra line spacing all the time?!?

import random
from board import Board
from game import play_game
from generate import generate_boards


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
	# the most unique layouts is 228
	for num in range(1, 299):
		for layout in game:

			# enters layouts in numerical order
			if layout.pattern == num:
				toAdd.append(layout)
			if len(toAdd) == boardsPerLine:
				toPrint += mult_boards(toAdd, paths, showWin)
				toAdd = []

	# adds on any boards left over
	if len(toAdd) > 0:
		toPrint += mult_boards(toAdd, paths, showWin)

	return toPrint


def show_wins(game, limit='XO', ties=True, boardsPerLine=7):
	"""selects only winning and/or tied matches to display from any turns"""

	XWins = OWins = numTies = 0
	toShow = []
	toPrint = ""

	for turn in game:
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


def stats(game):
	"""creates and prints out varying stats about the game of tic tac toe"""
	pass


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
					print "\nShowing all possible states for Turn %s." % t
					print make_boards(game[int(t)], paths, showWin, boardsPerLine)
			# prints every layouts possible
			elif c == 'A':
				for t in range(0, 10):
					print "\nShowing all possible states for Turn %s." % t
					print make_boards(game[t], paths, showWin, boardsPerLine)
			# prints a single layout, or a selected range of layouts
			elif len(c) >= 3 and c[1] == '-':
				rangeSelected = True
				if ':' not in c:
					rangeSelected = False
					c = c + ':' + c[2:]
				output, success = make_range(game, c, paths, showWin, boardsPerLine)
				if success:
					print("\nShowing a %sstate%s from Turn %s." 
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