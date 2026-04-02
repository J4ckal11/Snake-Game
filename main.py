import pygame
import math

bulletsArray = []

class Bullets():
    def __init__(self):
        self.x = cannonX
        self.y = cannonY
        self.speed = 10

    def update(self):
        self.y -= self.speed
        pygame.draw.circle(window, 'red', (self.x, self.y), 5)

pygame.init()
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
running = True

cannon_surface = pygame.Surface((25, 50), pygame.SRCALPHA)
cannon = pygame.draw.rect(cannon_surface, 'white', cannon_surface.get_rect())

cannonAngle = 0
cannonX = window_width//2
cannonY = window_height//2 + 40
cannonPos = (cannonX, cannonY)

cx, cy = window_width//2, window_height//2
radius =  25
orbitAngle = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                Bullets()
                print("MOUSEDOWN")

    window.fill('skyblue')
    Bullets().update()

    pygame.draw.circle(window, 'white', (window_width//2, window_height//2), 25)
    
    mouseX, mouseY = pygame.mouse.get_pos()
    dx = mouseX - cannonX
    dy = mouseY - cannonY
    cannonAngle = math.atan2(dy, dx) + 90 * (math.pi / 180)

    fx = mouseX - cx
    fy = mouseY - cy
    targetOrbit = math.atan2(fy, fx)
    orbitAngle += targetOrbit - orbitAngle

    cannonX = cx + math.cos(orbitAngle) * radius
    cannonY = cy + math.sin(orbitAngle) * radius
    cannonPos = (cannonX, cannonY)

    rotated_cannon = pygame.transform.rotate(cannon_surface, -math.degrees(cannonAngle))
    rotated_surface = rotated_cannon.get_rect(center=cannonPos)

    window.blit(rotated_cannon, rotated_surface)

    pygame.display.flip()
    clock.tick(60)
