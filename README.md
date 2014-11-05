Tic-Tac-Toe Analyzer
====================

Run
---
Requires python 2. Run tictactoe.py and wait a short while until it generates all of its data.

Usage
-----
There's four main methods to using this program:
1) (SOON) You will be able to see generalized statistics of interesting conclusions, generated live.
2) Investigate all the possible layouts of the board for each turn in giant pieces, or through careful selections.
3) Play tic tac toe knowing all the secrets of how to get to the best layouts.
4) Branch off the project to add in your own methods of analyzing the results, or use the data it generates to make impossible Tic Tac Toe AI's or anything fun like that.

The first and last two are straightforward enough, but the second method is more complicated, so I'll go in more depth about it here. The program knows all 10 Turns of the game (0 through 9, since it includes a blank board), as well as arbitrary assignments of layout numbers for each board for each turn. Turn 1 has 3 boards, Turn 2 has 12, and so on. These can be viewed by listing the turn number then the layout number wanted, such as "1-2" to call up only the second board of Turn 1, or "7-89" to look at the 89th board of Turn 7.

Also, a range of boards for a given Turn may be selected. To look at only layouts 10 through 20 for Turn 3, you can enter "3-10:20" to specify that. Likewise, "5-25:60" looks up Turn 5 and displays layouts 25 through 60. This lets users sift through selective parts of turns, rather than trying to parse up to hundreds of layouts at once.

Furthermore, a one-way path finder display may be toggled on or off, by entering 'P'. When results are viewed with this on, empty spaces in board now list the layout number of the next Turn that the board will resemble if the next player plays on that space. For instance, the only board for Turn 0 will look a bit like this:

http://cl.ly/image/3c2b3o26372n

This means if the first player plays in a corner, they are going into Layout 1-1 (Turn 1, Layout 1). If they play in a side, they are going to Layout 1-2, and if they play in the middle they are going into Layout 1-3. Keep in mind that the program notes rotated boards and mirrored boards that match up as identical, and only keeps a reference for the first one reached. Layout 1-1 in my program shows an X in the upper left corner, but the board is functionally the same as if X had been played in any corner. The difference is only relative to how it looks on the screen.

Also, it may be of interest to see what the winning boards are. Entering 'W' will toggle checking if a board has won when it's displayed, which is a handy refernce so you don't have to figure it out for yourself constantly. Keep in mind that a winning game is logically impossible before Turn 5. A more direct approach is to enter 'X', 'O', or 'T', each of which will show all winning layouts for X, all winning layouts for O, and all layouts where there is a tie, respectively. The results may surprise you!

History
-------
I first made this project over about a month, in July 2012. Though it is only shortly after my third version of Dragon Fighter RPG, there is a vast difference in quality, which is somewhat due to this being heavily planned by hand, and Dragon Fighter V3 being a slight remake. I have also updated this program much more, splitting it up into four files instead of one big confusing file, and cleaning up code where I've seen fit, mostly in the usability area. But originally it *did* do everything that it did right- the generation code has been untouched, for instance!

My approach to creating it was toying with the idea of wanting to tackle down a game completely. I had recently realized how difficult it would be for a computer to compute every single chess board layout, but I realized a much simpler domain was available: Tic Tac Toe. Before I got tangled up in code that I didn't understand, I started by drawing out legal board layouts. I quickly realized an important distinction: though it may be immediately apparent than the first player in Tic Tac Toe has 9 options, they truly only have 3: a corner, a side, or the middle (see above for an illustration of this).

After doing the first three player turns by hand, I decided I had enough of manual labour (Turn 3 has 38 unique boards, geeze!) and started planning out the current program, developed it over about a month, and recently came back to it to clean it up and present it to the world.