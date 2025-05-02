import pygame
import random

class Particle(pygame.sprite.Sprite):
    def __init__(self, x = None, y = None, vx = None, vy = None):
        super().__init__()
        x = x if x else random.randint(0, screen_width - particle_size)
        y = y if y else random.randint(0, screen_height - particle_size)
        self.image = pygame.Surface((particle_size, particle_size))
        r,g,b = (random.randint(100, 255) for _ in range(3))
        self.image.fill((r, g, b))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.vx = vx if vx else random.uniform(-1,1) * default_random_speed_cap
        self.vy = vy if vy else random.uniform(-1,1) * default_random_speed_cap

    def move(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.vx *= -1

        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.vy *= -1

    def detect_collision(self, other):
        if self.rect.colliderect(other.rect):
            side = check_side(self.rect, other.rect)
            if side == "top" or side == "bottom":
                other.vy, self.vy = self.vy, other.vy
            elif side == "corner":
                other.vy, self.vy = self.vy, other.vy
                other.vx, self.vx = self.vx, other.vx
            else:
                other.vx, self.vx = self.vx, other.vx

    def update(self):
        self.move()

def check_side(rect1, rect2):
    xdiff = rect2.centerx - rect1.centerx
    ydiff = rect2.centery - rect1.centery

    if abs(ydiff) > abs(xdiff):
        if ydiff >= 0:
            return "bottom"
        else:
            return "top"
    elif abs(ydiff) == abs(xdiff):
        return "corner"
    else:
        if xdiff >= 0:
            return "right"
        else:
            return "left"


    """
    if xdiff >= ydiff:
        if ydiff >= -xdiff:
            return "top"
        else:
            return "right"
    else:
        if ydiff >= -xdiff:
            return "left"
        else:
            return "bottom"
    """

def collisions():
    for i,this in enumerate(particles):
        for j,other in enumerate(particles):
            if i >= j: continue
            this.detect_collision(other)


screen_width = 1000
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

particle_size = 10
default_random_speed_cap = 3

particles = pygame.sprite.Group()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            print('a')
            mouse_x, mouse_y = pygame.mouse.get_pos()
            particles.add(Particle(mouse_x, mouse_y))

    collisions()

    screen.fill((0, 0, 0))

    particles.draw(screen)
    particles.update()

    pygame.display.update()

    if pygame.mouse.get_pressed()[0]:
        pass

    clock.tick(60)