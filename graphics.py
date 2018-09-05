import sys, math, pygame

square_side = 38
ball_radius = 13
square_count = 9

grid_left = 100
grid_top = 50

grid_right = grid_left + square_side * square_count
grid_bottom = grid_top + square_side * square_count

grid_right_margin = 100
grid_bottom_margin = 50

screen_size = screen_width, screen_height = grid_right + grid_right_margin, grid_bottom + grid_bottom_margin

background_color = 200, 200, 200

emptySquare = pygame.image.load("square.png")

def square_coordinates(col, row):
    return grid_left + square_side * col, grid_top + square_side * row

def generate_ball_image(red, green, blue):
    image = pygame.Surface((square_side, square_side))
    transColor = image.get_at((0,0))
    image.set_colorkey(transColor)
    ball_top = ball_left = square_side // 2 - ball_radius - 2

    for x in range(2 * ball_radius):
        for y in range(2 * ball_radius):
            dx = (x - ball_radius) ** 2
            dy = (y - ball_radius) ** 2
            #dx + dy <= (ball_radius + 0.5) ** 2
            if dx + dy <= ball_radius * ball_radius: 
                brightness = 1 - math.sqrt ((x * x + y * y) / 8) / ball_radius
                image.set_at((ball_left + x, ball_top + y), (brightness * red, brightness * green, brightness * blue))
    return image

def generate_shadow_image():
    image = pygame.Surface((square_side, square_side))
    transColor = image.get_at((0,0))
    image.set_colorkey(transColor)
    ball_top = ball_left = 1 + square_side // 2 - ball_radius

    for x in range(2 * ball_radius):
        for y in range(2 * ball_radius):
            dx = (x - ball_radius) ** 2
            dy = (y - ball_radius) ** 2
            distanceFromCenter = math.sqrt(dx + dy) / ball_radius
            if distanceFromCenter <= 1: 
                shadow_color = 0 + 75 * distanceFromCenter
                image.set_at((ball_left + x, ball_top + y), (shadow_color, shadow_color, shadow_color))
    return image 

def draw_scene(screen, fieldState):
    screen.fill(background_color)
    for col in range(square_count):
        for row in range(square_count):
            screen.blit(emptySquare, square_coordinates(col, row))
            ball_color = fieldState[col][row]
            if ball_color > 0:
                coord = square_coordinates(col, row)
                screen.blit(ball_shadow_image, (coord[0] + 2, coord[1] + 2))
                screen.blit(ball_images[ball_color - 1], coord)

def check_board_click(x, y, onCellClick):
    if x >= grid_left and x < grid_right and y >= grid_top and y < grid_bottom:
        col = (x - grid_left) // square_side
        row = (y - grid_top) // square_side
        onCellClick(col, row)

ball_images = (
    generate_ball_image(255, 0, 0), 
    generate_ball_image(0, 255, 0),
    generate_ball_image(0, 0, 255),
    generate_ball_image(255, 255, 0),
    generate_ball_image(0, 255, 255),
    generate_ball_image(255, 0, 255)
)    

ball_shadow_image = generate_shadow_image()