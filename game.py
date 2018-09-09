import sys, math, pygame
import graphics, gameState

pygame.init()
graphics.init()

pygame.display.set_caption('Color Lines')

gameState.add_random_balls(5, 3)

def redraw():
    graphics.draw_scene(gameState)
    pygame.display.flip()

def on_tile_click(col, row):
    gameState.on_tile_click(col, row, redraw)
    
redraw()

timeCounter = 0

# Event loop
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                graphics.check_board_click(event.pos[0], event.pos[1], on_tile_click) 

    timeCounter += 1
    if gameState.is_selected:
        graphics.animateSelectedBall(gameState.balls, gameState.selected_position, timeCounter)
        

    pygame.time.wait(100)
