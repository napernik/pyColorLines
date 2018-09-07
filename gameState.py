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

pending_balls = [ 
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

def addRandomBalls(quantity, pendingBallsQuantity):
    freePositions = []
    for col in range(square_count):
        for row in range(square_count):
            if balls[col][row] == 0:
                freePositions.append((col, row))
    # Adding balls            
    for i in range(min(quantity, len(freePositions))):
        posIndex = random.randint(0, len(freePositions) - 1)
        position = freePositions.pop(posIndex)
        balls[position[0]][position[1]] = random.randint(1, ball_color_count)

    # Adding pending balls
    for i in range(min(pendingBallsQuantity, len(freePositions))):
        posIndex = random.randint(0, len(freePositions) - 1)
        position = freePositions.pop(posIndex)
        pending_balls[position[0]][position[1]] = random.randint(1, ball_color_count)

    return len(freePositions)


def onTileClick(col, row, redrawFunc):
    global is_selected
    global selected_ball
    target = balls[col][row]
    if target > 0:
        selected_ball = (col, row)
        is_selected = True
        redrawFunc()
        return
    
    # Cannot move to a pending position
    if pending_balls[col][row]:
        return

    if is_selected:
        # Moving the selected ball to the new position
        balls[col][row] = balls[selected_ball[0]][selected_ball[1]]
        balls[selected_ball[0]][selected_ball[1]] = 0
        is_selected = False

        # Materializing pending balls
        for col in range(square_count):
            for row in range(square_count):
                color = pending_balls[col][row]
                if (color > 0) :
                    balls[col][row] = color
                    pending_balls[col][row] = 0

        #TODO: remove aligned balls and update score


        # Adding new pending balls
        freeTilesLeft = addRandomBalls(0, 3)

        #if there's no spots left -> materialize -> if there're still no left -> declare game over and announce the final score

        redrawFunc()
