import pygame
import random
import time

pygame.init()

grid_rows, grid_cols = 15, 20
cell_size = 30
width, height = grid_cols * cell_size, grid_rows * cell_size

screen = pygame.display.set_mode((width, height + 50))
pygame.display.set_caption("Falling Rain Pattern")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def generate_random_color():
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

def lerp_color(start_color, end_color, t):
    return (int(start_color[0] + (end_color[0] - start_color[0]) * t),
            int(start_color[1] + (end_color[1] - start_color[1]) * t),
            int(start_color[2] + (end_color[2] - start_color[2]) * t))

start_color = generate_random_color()
target_color = generate_random_color()
color_transition_duration = 3  
start_time = time.time()

raindrops = [{'position': random.randint(-grid_rows, 0), 'trail': []} for _ in range(grid_cols)]

def draw_rain(current_color):
    for col in range(grid_cols):
        for row in range(grid_rows):
            if row == raindrops[col]['position']:
                color = current_color
            elif row > raindrops[col]['position']:
                color = BLACK
            else:
                trail_index = raindrops[col]['position'] - row
                if trail_index < len(raindrops[col]['trail']):
                    brightness = max(0, 255 - trail_index * 25)
                    color = (max(0, current_color[0] - trail_index * 25), 
                             max(0, current_color[1] - trail_index * 25), 
                             max(0, current_color[2] - trail_index * 25))
                else:
                    color = BLACK
            pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, BLACK, (col * cell_size, row * cell_size, cell_size, cell_size), 1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    elapsed_time = time.time() - start_time
    t = min(elapsed_time / color_transition_duration, 1.0)
    current_color = lerp_color(start_color, target_color, t)

    if t >= 1.0:
        start_color = target_color
        target_color = generate_random_color()
        start_time = time.time()

    for i in range(grid_cols):
        raindrops[i]['position'] += 1
        if raindrops[i]['position'] > grid_rows:
            raindrops[i]['position'] = random.randint(-grid_rows, 0)
            raindrops[i]['trail'] = []
        else:
            raindrops[i]['trail'].append(raindrops[i]['position'])

    screen.fill(BLACK)

    draw_rain(current_color)

    font = pygame.font.SysFont(None, 36)
    text = font.render("Rain Pattern", True, WHITE)
    screen.blit(text, (width // 2 - text.get_width() // 2, height + 10))

    pygame.display.flip()

    pygame.time.delay(100)
pygame.quit()
