import sys, math, pygame
import graphics, gameState
from gameconfig import *

pygame.init()
graphics.init()

pygame.display.set_caption(WINDOW_CAPTION)

gameState.add_random_balls(STARTING_AMOUNT_OF_BALLS, NEW_PENDING_BALLS_PER_TURN)

def redraw():
    graphics.draw_scene(gameState)
    pygame.display.flip()

def on_tile_click(col, row):
    gameState.on_tile_click(col, row, redraw)
    
redraw()

timeCounter = 0

# Event loop
running = True
while running:
    for event in pygame.event.get():  
        if event.type == pygame.QUIT: 
            running = False
        elif event.type == pygame.VIDEORESIZE:
            newSize = event.dict['size']
            adjustedSize = graphics.recalculateProportions(*newSize)
            graphics.init()
            redraw()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                graphics.check_board_click(*event.pos, on_tile_click) 

    timeCounter += 1
    if gameState.is_selected:
        graphics.animateSelectedBall(gameState.balls, gameState.selected_position, timeCounter)
        

    pygame.time.wait(100)

sys.exit()