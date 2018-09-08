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



Run (with Python installed)

1) Install python
2) Install pygame module via pip
3) Check out GIT repo
4) Run
  py .\game.py 


Run (without Python, Windows):
 
Executables coming soon...  
  


Made by: Dmitry Dzygin