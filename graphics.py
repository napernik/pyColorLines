import sys, math, pygame
from gameconfig import *

screen = None

emptySquare = pygame.image.load("square.png")
default_tile_width = emptySquare.get_width()

BACKGROUND_COLOR = 200, 200, 200

# Score text
pygame.font.init()
scoreFont = pygame.font.SysFont('Comic Sans MS', 30)
scoreColor = (43, 91, 132)
scoreCoords = (30, 5)

# Grid and screen sizes
grid_left = 30
grid_top = 50

grid_right_margin = 30
grid_bottom_margin = 30

class Proportions:
    def __init__(self, tile_size):
        self.ball_radius = tile_size // 3
        self.tile_size = tile_size

        self.ball_diagonal_offset = - tile_size // 15
        self.shadow_animation_movement_range = tile_size // 7

        self.pending_ball_image_size = tile_size // 2
        self.pending_ball_image_offset = (tile_size - self.pending_ball_image_size) // 2 - self.ball_diagonal_offset

        self.grid_right = grid_left + tile_size * TILES_COUNT
        self.grid_bottom = grid_top + tile_size * TILES_COUNT

        self.screen_size = self.grid_right + grid_right_margin, self.grid_bottom + grid_bottom_margin

    def tile_coordinates(self, col, row):
        "calculates the the coordinates of the top left corner of a grid tile"

        return grid_left + self.tile_size * col, grid_top + self.tile_size * row

proportions = Proportions(default_tile_width)




def init():
    global screen
    screen = pygame.display.set_mode(proportions.screen_size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)


def add_diagonal_offset(coords, value):
    return (coords[0] + value, coords[1] + value)



def generate_ball_image(proportions, red, green, blue):
    tile_size, ball_radius = proportions.tile_size, proportions.ball_radius

    image = pygame.Surface((tile_size, tile_size))
    transColor = image.get_at((0,0))
    image.set_colorkey(transColor)
    ball_top = ball_left = tile_size // 2 - ball_radius + proportions.ball_diagonal_offset

    for x in range(2 * ball_radius):
        for y in range(2 * ball_radius):
            dx = (x - ball_radius) ** 2
            dy = (y - ball_radius) ** 2
            if dx + dy < ball_radius * ball_radius: 
                brightness = 1 - math.sqrt ((x * x + y * y) / 8) / ball_radius
                image.set_at((ball_left + x, ball_top + y), (brightness * red, brightness * green, brightness * blue))
    return image

def generate_shadow_image(proportions):
    tile_size, ball_radius = proportions.tile_size, proportions.ball_radius

    image = pygame.Surface((tile_size, tile_size))
    transColor = image.get_at((0,0))
    image.set_colorkey(transColor)
    ball_top = ball_left = 1 + tile_size // 2 - ball_radius

    for x in range(2 * ball_radius):
        for y in range(2 * ball_radius):
            dx = (x - ball_radius) ** 2
            dy = (y - ball_radius) ** 2
            distanceFromCenter = math.sqrt(dx + dy) / ball_radius
            if distanceFromCenter <= 1: 
                shadow_color = 0 + 75 * distanceFromCenter
                image.set_at((ball_left + x, ball_top + y), (shadow_color, shadow_color, shadow_color))
    return image 

def draw_tile(col, row, ball_color, shadowOffset, isPendingBall = False):
    coord = proportions.tile_coordinates(col, row)
    screen.blit(emptySquare, coord)
    if ball_color > 0:
        if not isPendingBall:
            screen.blit(ball_shadow_image, add_diagonal_offset(coord, shadowOffset))
            screen.blit(ball_images[ball_color - 1], coord)
        else:
            screen.blit(pending_ball_images[ball_color - 1], add_diagonal_offset(coord, proportions.pending_ball_image_offset))

    return (coord[0], coord[1], proportions.tile_size, proportions.tile_size)


def draw_scene(gameState):
    screen.fill(BACKGROUND_COLOR)
    for col in range(TILES_COUNT):
        for row in range(TILES_COUNT):
            ball_color = gameState.balls[col][row]
            pending_ball_color = gameState.pending_balls[col][row]
            if pending_ball_color > 0:
                draw_tile(col, row, pending_ball_color, 2, True)
            else:
                draw_tile(col, row, ball_color, 2, False)

    scoreText = 'Score: ' + str(gameState.score)
    textSurface = scoreFont.render(scoreText, False, scoreColor)
    screen.blit(textSurface, scoreCoords)

def animateSelectedBall(balls, coords, timeCounter):
    color = balls[coords[0]][coords[1]]
    shadowOffset = proportions.ball_diagonal_offset + proportions.shadow_animation_movement_range * (1 + math.sin(timeCounter / 2.5)) / 2
    updateArea = draw_tile(coords[0], coords[1], color, shadowOffset)
    pygame.display.update(updateArea)
    


def check_board_click(x, y, onCellClick):
    if x >= grid_left and x < proportions.grid_right and y >= grid_top and y < proportions.grid_bottom:
        col = (x - grid_left) // proportions.tile_size
        row = (y - grid_top) // proportions.tile_size
        onCellClick(col, row)

ball_images = [generate_ball_image(proportions, *color) for color in BALL_COLORS]

pending_ball_images = []



for imageIndex in range(len(ball_images)):
    newSize = (proportions.pending_ball_image_size, proportions.pending_ball_image_size)
    #pending_ball_images.append(pygame.transform.smoothscale(ball_images[imageIndex], newSize))
    pending_ball_images.append(pygame.transform.scale(ball_images[imageIndex], newSize))

ball_shadow_image = generate_shadow_image(proportions)