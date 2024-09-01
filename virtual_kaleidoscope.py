import pygame
import random
import math

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Realistic Virtual Kaleidoscope")

# Center point and number of sections
centerX, centerY = WIDTH // 2, HEIGHT // 2
numSections = 22
angleIncrement = (2 * math.pi) / numSections
rotationSpeed = 0.005
currentAngle = 0

# Color constants
BLACK = (0, 0, 0)

def get_random_int(min_val, max_val):
    return random.randint(min_val, max_val)

def get_random_color():
    return (get_random_int(0, 255), get_random_int(0, 255), get_random_int(0, 255))

shapes = []

def generate_shapes():
    global shapes
    shapes = []
    for _ in range(50):  # Adjust number of shapes as needed
        x = get_random_int(-centerX, centerX)
        y = get_random_int(-centerY, centerY)
        size = get_random_int(10, 50)
        color = get_random_color()
        shape_type = get_random_int(0, 2)
        shapes.append((x, y, size, color, shape_type))

def draw_shape(surface, x, y, size, color, shape_type):
    if shape_type == 0:  # Circle
        pygame.draw.circle(surface, color, (x, y), size // 2)
    elif shape_type == 1:  # Square
        pygame.draw.rect(surface, color, (x - size // 2, y - size // 2, size, size))
    elif shape_type == 2:  # Triangle
        points = [(x, y - size // 2), (x + size // 2, y + size // 2), (x - size // 2, y + size // 2)]
        pygame.draw.polygon(surface, color, points)

def draw_kaleidoscope():
    global currentAngle

    screen.fill((240, 240, 240))

    for i in range(numSections):
        angle = currentAngle + i * angleIncrement
        for shape in shapes:
            x, y, size, color, shape_type = shape

            rotated_x = int(centerX + x * math.cos(angle) - y * math.sin(angle))
            rotated_y = int(centerY + x * math.sin(angle) + y * math.cos(angle))
            draw_shape(screen, rotated_x, rotated_y, size, color, shape_type)

            rotated_x_mirrored = int(centerX - x * math.cos(angle) + y * math.sin(angle))
            rotated_y_mirrored = int(centerY + x * math.sin(angle) + y * math.cos(angle))
            draw_shape(screen, rotated_x_mirrored, rotated_y_mirrored, size, color, shape_type)

    for i in range(numSections):
        angle = currentAngle + i * angleIncrement
        end_x = int(centerX + centerX * math.cos(angle))
        end_y = int(centerY + centerY * math.sin(angle))
        pygame.draw.line(screen, BLACK, (centerX, centerY), (end_x, end_y), 2)

    if not paused:
        currentAngle += rotationSpeed

generate_shapes()

running = True
paused = False  # Pause flag
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            generate_shapes()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused  # Toggle paused state

    draw_kaleidoscope()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
