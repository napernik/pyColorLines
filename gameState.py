import math, random

square_count = 9
ball_color_count = 6

balls = [ 
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

balls_to_materialize = [ 
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

is_selected = False
selected_ball = (-1, -1)

score=0

def addRandomBalls(quantity):
    freePositions = []
    for col in range(square_count):
        for row in range(square_count):
            if balls[col][row] == 0:
                freePositions.append((col, row))
    for i in range(min(quantity, len(freePositions))):
        posIndex = random.randint(0, len(freePositions) - 1)
        position = freePositions.pop(posIndex)
        balls[position[0]][position[1]] = random.randint(1, ball_color_count)

def onCellClick(col, row, redrawFunc):
    global is_selected
    global selected_ball
    target = balls[col][row]
    if target > 0:
        selected_ball = (col, row)
        is_selected = True
        redrawFunc()
        return
    
    if is_selected:
        # Moving the selected ball to the new position
        balls[col][row] = balls[selected_ball[0]][selected_ball[1]]
        balls[selected_ball[0]][selected_ball[1]] = 0
        is_selected = False
        #TODO: materialize pending balls
        #TODO: remove aligned balls and update score
        #TODO: todo add new balls to materialize or end the game
        redrawFunc()
