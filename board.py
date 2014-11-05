#!/usr/bin/python

# represents data for a tic tac toe board with functions to modify it, compare boards, and display it

class Board(str):
    # inherits string because this is what the board is represented by:
    # a 9 character string, where each character is a ' ', 'X', or 'O'
    # ' ' for any empty board spaces, 'X' for spaces X played on, and 'O' for spaces O played on
    
    def __new__(cls, layout='         ', p=0, paths=[]):
        obj = str.__new__(cls, layout)
        # the unique number of layout for this turn
        obj.pattern = p
        # boards for the next turn this one can lead to
        obj.paths = paths[:]
        return obj

    def matches(self, other):
        """
        compares a given layout against all 8 possible rotations of it
        and returns true if any two of them are identical
        """
        mirrored = other.mirror()
        return (self == other or self == other.rotate() or
                self == other.rotate(2) or self == other.rotate(3)
                or self == mirrored or self == mirrored.rotate() or 
                self == mirrored.rotate(2) or self == mirrored.rotate(3))

    def rotate(self, rots=1):
        """recursively rotates a layout 90 degrees clockwise by a specified number of times, and returns it"""
        if rots > 1:
            self = self.rotate(rots - 1)
        return Board(self[6] + self[3] + self[0] + self[7] + self[4] + self[1] + self[8] + self[5] + self[2])

    def mirror(self):
        """mirrors a move layout down the middle and returns it"""
        return Board(self[2] + self[1] + self[0] + self[5] + self[4] + self[3] + self[8] + self[7] + self[6])

    def make_board(self, paths=False, showWin=False):
        """makes and returns a full display of a layout"""

        board = "\n"
        for row in range(3):
            for col in range(3):
                # characters for a single row are stored 3 characters apart
                # and columns offset this by 0 to 2 spaces
                toAdd = self[row * 3 + col]

                # ii wanted, adds the path instead of a blank
                if paths and toAdd == ' ' and not self.check_win()[0]:
                    toAdd = str(self.paths[row * 3 + col])

                # paths may be 1 to 3 digits, so this makes sure they fit into empty spots perfectly
                if len(toAdd) == 1: board += " %s " % toAdd
                elif len(toAdd) == 2: board += " %s" % toAdd
                else: board += "%s" % toAdd
                # puts dividers between game spaces
                if col != 2: board += "|"
                # end of the row reached
                else: board += "\n"

            if row != 2: board += "-----------\n"
            
        # adds the pattern, and turn number, for a layout if there is a pattern
        if len(str(self.pattern)) > 0 and self.pattern > 0:
            board += "\nLayout %s-%s" % (self.what_turn(), self.pattern)

        if showWin:
            board += "\n"
            win, winner = self.check_win()
            if win: board += "%s Wins" % winner
            elif ' ' not in self: board += "Tie game"
            else: board += 'No Win'

        return board

    def what_turn(self):
        """checks what turn a layout is from and returns that"""
        turn = 9
        for i in self:
            # 9 spaces = start of game, 8 spaces = turn 1, etc
            if i == ' ':
                turn -= 1
        return turn

    def check_win(self):
        """
        returns true if there is a winning move, and the winning player
        returns false otherwise, and an empty string for the winner
        """

        win = False
        winner = ''

        # winning is only possible from turn 5 and on
        if self.what_turn() >= 5:
            
            # goes through both possible winning players
            for p in ('X', 'O'):
                 # checks for a diagonal win
                if self[4] == p and (self[0] == self[8] == p or self[2] == self[6] == p):
                    win = True
                else:
                    for i in range(3):
                        # checks for vertical and horizontal wins
                        if (self[i] == self[i+3] == self[i+6] == p or 
                            self[i*3] == self[i*3+1] == self[i*3+2] == p):
                            win = True
                if win:
                    winner = p
                    break

        return (win, winner)