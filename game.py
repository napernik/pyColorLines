import sys, math, pygame
import graphics, gameState

pygame.init()

graphics.init()

gameState.addRandomBalls(5, 3)

def redraw():
    graphics.draw_scene(gameState)
    pygame.display.flip()

def onTileClick(col, row):
    gameState.onTileClick(col, row, redraw)
    
redraw()

timeCounter = 0

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:  #Better to seperate to a new if statement aswell, since there's more buttons that can be clicked and makes for cleaner code.
            if event.button == 1:
                graphics.check_board_click(event.pos[0], event.pos[1], onTileClick) 

    timeCounter += 1
    if gameState.is_selected:
        graphics.animateSelectedBall(gameState.balls, gameState.selected_ball, timeCounter)
        

    pygame.time.wait(50)
