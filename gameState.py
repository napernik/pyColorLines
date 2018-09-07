import math, random

square_count = 9
ball_color_count = 6

def getEmptySquareMatrix(size):
     return [[0 for i in range(size)] for i in range(size)]

balls = getEmptySquareMatrix(square_count)
pending_balls =  getEmptySquareMatrix(square_count)

is_selected = False
selected_ball = (-1, -1)

score=0

# 0 points for less than 5 balls, 5 for 5, 7 for 6, 10 for 7, 14 for 8
def getRewardScore(sequenceLength): 
    if sequenceLength < 5:
        return 0
    
    rewardableBalls = sequenceLength - 4
    return 4 + (1 + rewardableBalls) * rewardableBalls // 2; 


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

def consume_consequent_balls(startPosition, getNextPosition, balls_to_remove):
    global score    
    sequenceColor = 0
    sequence = []
    position = startPosition
    isLastStep = False

    while not isLastStep:
        currentColor=balls[position[0]][position[1]]
        if currentColor == sequenceColor and sequenceColor != 0:
            sequence.append(position)

        nextPosition = getNextPosition(position)
        isLastStep = nextPosition[0] >= square_count or nextPosition[1] >= square_count or nextPosition[0] < 0 or nextPosition[1] < 0
        if currentColor != sequenceColor or isLastStep:
            reward = getRewardScore(len(sequence))
            if reward > 0:
                score += reward
                for pos in sequence:
                    balls_to_remove[pos[0]][pos[1]] = 1

        if currentColor != sequenceColor:
            sequenceColor = currentColor
            sequence.clear()
            sequence.append(position)
        
        position = nextPosition

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

        # Remove aligned 5+ balls and update score
        balls_to_remove = getEmptySquareMatrix(square_count)

        # Vertical rows
        for col in range(square_count):
            consume_consequent_balls((col, 0), lambda position : (position[0], position[1] + 1), balls_to_remove)

        # Horizontal rows
        for row in range(square_count):
            consume_consequent_balls((0, row), lambda position : (position[0] + 1, position[1]), balls_to_remove)

        # Down-Right diagonal
        getNextPosition = lambda position : (position[0] + 1, position[1] + 1)
        for col in range(square_count):
            consume_consequent_balls((col, 0), getNextPosition, balls_to_remove)
        for row in range(square_count - 1):
            consume_consequent_balls((0, row + 1), getNextPosition, balls_to_remove)

        # Down-Left diagonal
        getNextPosition = lambda position : (position[0] - 1, position[1] + 1)
        for col in range(square_count):
            consume_consequent_balls((col, 0), getNextPosition, balls_to_remove)
        for row in range(square_count - 1):
            consume_consequent_balls((square_count - 1, row + 1), getNextPosition, balls_to_remove)            

        for col in range(square_count):
            for row in range(square_count):
                if balls_to_remove[col][row] == 1:
                    balls[col][row] = 0

        # Adding new pending balls
        freeTilesLeft = addRandomBalls(0, 3)

        #if there's no spots left -> materialize -> if there're still no left -> declare game over and announce the final score

        redrawFunc()
