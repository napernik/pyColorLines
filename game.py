import sys, math, pygame
import graphics, gameState

pygame.init()

screen = pygame.display.set_mode(graphics.screen_size)

gameState.addRandomBalls(10)

def redraw():
    graphics.draw_scene(screen, gameState.balls)
    pygame.display.flip()

def onCellClick(col, row):
    gameState.balls[col][row] = 2
    redraw()
    
redraw()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:  #Better to seperate to a new if statement aswell, since there's more buttons that can be clicked and makes for cleaner code.
            if event.button == 1:
                graphics.check_board_click(event.pos[0], event.pos[1], onCellClick) 

    pygame.time.wait(50)
    # ballrect = ballrect.move(speed)
    # if ballrect.left < 0 or ballrect.right > width:
    #     speed[0] = -speed[0]
    # if ballrect.top < 0 or ballrect.bottom > height:
    #     speed[1] = -speed[1]
 
    # screen.fill(red)
    # screen.blit(ball, ballrect)
    # #pygame.display.flip()
    # pygame.display.update(ballrect)