import math, random
from gameconfig import *

def get_empty_square_matrix(size):
     return [[0 for i in range(size)] for i in range(size)]

balls = get_empty_square_matrix(TILES_COUNT)
pending_balls =  get_empty_square_matrix(TILES_COUNT)

is_selected = False
selected_position = (-1, -1)

score=0

is_game_over = False

def get_reward_score(sequenceLength): 
    "0 points for less than 5 balls, 5 for 5, 7 for 6, 10 for 7, 14 for 8"
    if sequenceLength < 5:
        return 0
    
    rewardableBalls = sequenceLength - 4
    return 4 + (1 + rewardableBalls) * rewardableBalls // 2; 


def add_random_balls(quantity, pendingBallsQuantity):
    freePositions = []
    for col in range(TILES_COUNT):
        for row in range(TILES_COUNT):
            if balls[col][row] == 0:
                freePositions.append((col, row))
    # Adding balls            
    for i in range(min(quantity, len(freePositions))):
        posIndex = random.randint(0, len(freePositions) - 1)
        position = freePositions.pop(posIndex)
        balls[position[0]][position[1]] = random.randint(1, BALL_COLOR_COUNT)

    # Adding pending balls
    for i in range(min(pendingBallsQuantity, len(freePositions))):
        posIndex = random.randint(0, len(freePositions) - 1)
        position = freePositions.pop(posIndex)
        pending_balls[position[0]][position[1]] = random.randint(1, BALL_COLOR_COUNT)

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
        isLastStep = nextPosition[0] >= TILES_COUNT or nextPosition[1] >= TILES_COUNT or nextPosition[0] < 0 or nextPosition[1] < 0
        if currentColor != sequenceColor or isLastStep:
            reward = get_reward_score(len(sequence))
            if reward > 0:
                score += reward
                for col, row in sequence:
                    balls_to_remove[col][row] = 1

        if currentColor != sequenceColor:
            sequenceColor = currentColor
            sequence.clear()
            sequence.append(position)
        
        position = nextPosition

def remove_aligned_balls():
    "Removes aligned 5+ balls and updates the score."
    balls_to_remove = get_empty_square_matrix(TILES_COUNT)


    # Vertical rows
    for col in range(TILES_COUNT):
        consume_consequent_balls((col, 0), lambda position : (position[0], position[1] + 1), balls_to_remove)

    # Horizontal rows
    for row in range(TILES_COUNT):
        consume_consequent_balls((0, row), lambda position : (position[0] + 1, position[1]), balls_to_remove)

    # Down-Right diagonal
    getNextPosition = lambda position : (position[0] + 1, position[1] + 1)
    for col in range(TILES_COUNT):
        consume_consequent_balls((col, 0), getNextPosition, balls_to_remove)
    for row in range(1, TILES_COUNT):
        consume_consequent_balls((0, row), getNextPosition, balls_to_remove)

    # Down-Left diagonal
    getNextPosition = lambda position : (position[0] - 1, position[1] + 1)
    for col in range(TILES_COUNT):
        consume_consequent_balls((col, 0), getNextPosition, balls_to_remove)
    for row in range(1, TILES_COUNT):
        consume_consequent_balls((TILES_COUNT - 1, row), getNextPosition, balls_to_remove)            

    totalConsumed = 0
    for col in range(TILES_COUNT):
        for row in range(TILES_COUNT):
            if balls_to_remove[col][row] == 1:
                balls[col][row] = 0
                totalConsumed += 1

    return totalConsumed

def materialize_pending_balls():
    for col in range(TILES_COUNT):
        for row in range(TILES_COUNT):
            color = pending_balls[col][row]
            if (color > 0) :
                balls[col][row] = color
                pending_balls[col][row] = 0

def get_reachable_tile_map(position):
    reachableTiles = get_empty_square_matrix(TILES_COUNT)
    expanded = True
    reachableTiles[position[0]][position[1]] = 1
    while expanded:
        expanded = False
        for col in range(TILES_COUNT):
            for row in range(TILES_COUNT):
                if reachableTiles[col][row] == 0 and balls[col][row] == 0 and \
                   ((col > 0 and reachableTiles[col - 1][row] == 1) or
                    (col < TILES_COUNT - 1 and reachableTiles[col + 1][row] == 1) or
                    (row > 0 and reachableTiles[col][row - 1] == 1) or
                    (row < TILES_COUNT - 1 and reachableTiles[col][row + 1] == 1)
                    ):
                    reachableTiles[col][row] = 1
                    expanded = True
    return reachableTiles

def on_tile_click(col, row, redrawFunc):
    global is_selected
    global selected_position
    global is_game_over
    target = balls[col][row]
    if target > 0:
        selected_position = (col, row)
        is_selected = True
        redrawFunc()
        return
    
    if is_selected:
        # Cannot move to a pending position
        if pending_balls[col][row]:
            return

        # Cannot move to a position that's not reachable
        reachable = get_reachable_tile_map(selected_position)
        if reachable[col][row] == 0:
            return

        # Moving the selected ball to the new position
        balls[col][row] = balls[selected_position[0]][selected_position[1]]
        balls[selected_position[0]][selected_position[1]] = 0
        is_selected = False

        ballsRemoved = remove_aligned_balls()

        if ballsRemoved == 0:
            materialize_pending_balls()
            ballsRemoved = remove_aligned_balls()

            if ballsRemoved == 0:
                # If nothing is removed - adding new pending balls
                freeTilesLeft = add_random_balls(0, NEW_PENDING_BALLS_PER_TURN)
                if freeTilesLeft == 0:
                    materialize_pending_balls()
                    ballsRemoved = remove_aligned_balls()

                    if ballsRemoved == 0:
                        # When there're no available moves -> Game Over!
                        is_game_over = True

        redrawFunc()
