import pymunk
import pygame

def create_ball(space):
    mass = 1
    radius = 15
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    body.position = (300, 200)
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.9
    space.add(body, shape)
    return shape

def create_static_box(space, pos):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Poly.create_box(body, (100, 20))
    shape.elasticity = 0.4
    space.add(body, shape)
    return shape

# Inicjalizacja Pygame i Pymunk
pygame.init()
screen = pygame.display.set_mode((600, 400))
space = pymunk.Space()

# Utworzenie piłki i platformy
ball = create_ball(space)
static_box = create_static_box(space, (300, 350))

# Główna pętla gry
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Aktualizacja symulacji fizyki
    space.step(1/60.0)

    # Rysowanie na ekranie
    screen.fill((255, 255, 255))

    # Rysowanie piłki
    ball_pos = ball.body.position
    ball_radius = ball.radius
    pygame.draw.circle(screen, (0, 0, 255), (int(ball_pos.x), int(ball_pos.y)), int(ball_radius))

    # Rysowanie platformy
    box_pos = static_box.body.position
    box_width = static_box.width
    box_height = static_box.height
    pygame.draw.rect(screen, (0, 0, 0), (box_pos.x - box_width / 2, box_pos.y - box_height / 2, box_width, box_height))

    pygame.display.flip()
    clock.tick(60)
