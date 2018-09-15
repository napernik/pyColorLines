This an implementation of the classic "Color Lines" puzzle game using Python 3.7 and "pygame" library.

Rules:

- There's a 9x9 tile grid with color balls of 6 different colors on it.
- Player moves the balls one ball at a time.
- If after a move 5 or more neighbouring balls of the same color are aligned horizontally, vertically or diagonally, they are removed, and the player is awarded score points.
  5 balls = 5 points,
  6 balls = 7 points,
  7 balls = 9 points
  ...
- If no balls are removed after a move, 3 pending balls are added to the field, and 3 more "pending" balls will be shown.
- A player cannot move a ball into a pending ball position or move to a position that cannot be achieved via moving over adjacent empty tiles.

Objective:

- Score as many points as possible before there are no available moves left.


How to Run (Windows 10):
 
Download a zip archive from the Releases on GitHub


How to run with Python:

1) Install python
2) Install pygame via pip
3) Check out GIT repo
4) py .\game.py 



How to build an executable on Windows:

1) Install Visuall C++ Build Tools
2) Install cx_freeze module from https://www.lfd.uci.edu/~gohlke/pythonlibs/#cx_freeze
3) Create an environment variables TCL_LIBRARY/TK_LIBRARY and point it to: 

set TCL_LIBRARY=C:\Program Files\Python37\tcl\tcl8.6
set TK_LIBRARY=C:\Program Files\Python37\tcl\tk8.6

4) py .\build.py build
4.1) If the game doesn't work, apply a patch for the cx_Freeze,
https://github.com/anthony-tuininga/cx_Freeze/pull/395/commits/76542754e01d2d4b21c6744c563dda8d5c72b3b2/  


Made by: Dmitry Dzygin