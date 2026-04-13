import time
import pygame
import math
import random

class Button:
    def __init__(self, value, x, y, width, height, color, text_color, font=None):
        global smallFont
        self.value = value
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = tuple(int(c * 0.8) for c in color)
        self.text_color = text_color
        self.isHover = False
        if font is None:
            self.font = smallFont
        else:
            self.font = font
        self.text_surface = self.font.render(self.value, True, self.text_color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = (self.x + self.width//2, self.y + self.height//2)
        self.wasPressed = False
        self.isPressed = False
        self.setHover = False

    def update(self):
        self.text_surface = self.font.render(self.value, True, self.text_color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = (self.x + self.width // 2, self.y + self.height // 2)
        if self.x < mousePos.x < (self.x + self.width) and self.y < mousePos.y < (self.y + self.height):
            if mouse_pressed[0] and not self.wasPressed and not self.setHover:
                self.isHover = False
                self.wasPressed = True
                self.isPressed = True
            elif not mouse_pressed[0]:
                self.isHover = True
                self.wasPressed = False
                self.isPressed = False
            else:
                self.isPressed = False
        elif not self.setHover:
            self.isHover = False

        if self.isHover:
            pygame.draw.rect(window, self.hover_color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

        window.blit(self.text_surface, self.text_rect)

bulletsArray = []
class Bullets:
    def __init__(self):
        global playerHealthPoints
        self.pos = cannonPos
        self.speed = 100
        bulletsArray.append(self)
        self.direction = (mousePos - self.pos).normalize()
        self.hitbox = 5
        self.healthPoints = 1

    def update(self):
        if self.healthPoints > 0:
            if playerHealthPoints > 0 and not pauseMenu:
                self.pos += self.direction * self.speed * deltaTime
            pygame.draw.circle(window, 'darkgray', (self.pos.x, self.pos.y), 5)
            pygame.draw.circle(window, 'black', (self.pos.x, self.pos.y), 5, 2)
        else:
            bulletsArray.pop(bulletsArray.index(self))


snakeSpawnRate = 5
snakeArray = []
class Snake:
    def __init__(self):
        snakeArray.append(self)
        self.pos = pygame.math.Vector2(rand_edge())
        self.animFrame = 0
        self.animSpeed = 30
        self.counter = 1
        self.snakeFrame = None
        self.speed = 1
        self.direction = None
        self.healthPoints = 10
        self.value = 1
        self.hitboxPoints = [
            pygame.Vector2(self.pos.x, self.pos.y),
            pygame.Vector2(self.pos.x + 16, self.pos.y),
            pygame.Vector2(self.pos.x, self.pos.y + 32),
            pygame.Vector2(self.pos.x + 16, self.pos.y + 32)
        ]
        self.rotatedHitboxPoints = [p.rotate(math.atan2(window_height//2 - self.pos.y, window_width//2 - self.pos.x)) for p in self.hitboxPoints]
        self.rotatedSnakeSurf = pygame.transform.rotate(snakeFrames[self.animFrame], -math.degrees(math.atan2((window_height // 2) - self.pos.y, (window_width // 2) - self.pos.x)) - 90)
        self.snakeRect = self.rotatedSnakeSurf.get_rect(center=self.pos)

    def update(self):
        global playerHealthPoints
        if window_width//2 - 20 < self.pos.x < window_width//2 + 20 and window_height//2 - 20 < self.pos.y < window_height//2 + 20:
            self.healthPoints = 0
            playerHealthPoints -= 1

        if self.healthPoints > 0:
            if playerHealthPoints > 0 and not pauseMenu:
                self.direction = pygame.Vector2(window_width//2, window_height//2) - self.pos
                if self.direction.length() != 0:
                    self.direction = self.direction.normalize()
                self.pos += self.direction * self.speed
                if self.counter >= self.animSpeed:
                    self.counter = 0
                    if self.animFrame < len(snakeFrames) - 1:
                        self.animFrame += 1
                    else:
                        self.animFrame = 0
                else:
                    self.counter += 1

            self.rotatedSnakeSurf = pygame.transform.rotate(snakeFrames[self.animFrame], -math.degrees(math.atan2((window_height//2) - self.pos.y, (window_width//2) - self.pos.x)) - 90)
            self.snakeRect = self.rotatedSnakeSurf.get_rect(center=self.pos)
            window.blit(self.rotatedSnakeSurf, self.snakeRect)

            self.hitboxPoints = [
                pygame.Vector2(-16, 32),
                pygame.Vector2(-16, -32),
                pygame.Vector2(16, -32),
                pygame.Vector2(16, 32)
            ]

            self.rotatedHitboxPoints = [p.rotate(math.degrees(math.atan2(window_height // 2 - self.pos.y, window_width // 2 - self.pos.x)) + 90) + self.pos for p in self.hitboxPoints]

            #pygame.draw.line(window, 'red', self.rotatedHitboxPoints[0], self.rotatedHitboxPoints[1])
            #pygame.draw.line(window, 'red', self.rotatedHitboxPoints[1], self.rotatedHitboxPoints[2])
            #pygame.draw.line(window, 'red', self.rotatedHitboxPoints[2], self.rotatedHitboxPoints[3])
            #pygame.draw.line(window, 'red', self.rotatedHitboxPoints[3], self.rotatedHitboxPoints[0])
            #pygame.draw.circle(window, 'red', self.pos, 1)
        else:
            print("Snake popped", time.perf_counter() )
            snakeArray.pop(snakeArray.index(self))


def sprite_sheet(sheet_surf, x, y_val, width, height):
    surf = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    surf.blit(sheet_surf, (0, 0), (x, y_val, width, height))
    return surf

def transform(points, pos, angle):
    return [p.rotate(angle) + pos for p in points]

# SOURCE: ChatGPT
def closest_point_on_segment(a, b, p):
    ab = b - a
    t = (p - a).dot(ab) / ab.dot(ab)
    t = max(0, min(1, t))
    return a + ab * t

def circle_polygon_collision(circle_pos, radius, polygon):
    # 1. Edge tests
    for p in range(len(polygon)):
        a = polygon[p]
        b = polygon[(p + 1) % len(polygon)]

        closest = closest_point_on_segment(a, b, circle_pos)
        if (circle_pos - closest).length_squared() <= radius * radius:
            return True
    return False

def rand_edge():
    rand_num = random.randint(0, 3)
    if rand_num == 0:
        return random.randint(0, window_width), 0
    elif rand_num == 1:
        return 0, random.randint(0, window_height)
    elif rand_num == 2:
        return random.randint(0, window_width), window_height
    elif rand_num == 3:
        return window_width, random.randint(0, window_height)
    else:
        return False


pygame.init()
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
mousePos = pygame.math.Vector2(pygame.mouse.get_pos())
running = True
pauseMenu = False
cannonAngle = 0
playerHealthPoints = 100
playerCurrency = 0

backgroundColor = 'limegreen'

menuHeight = window.get_height()//6
window_height -= menuHeight

youLoseSurf = pygame.image.load('sprites/youLose.png').convert_alpha()
youLoseRect = youLoseSurf.get_rect()
youLoseSurf = pygame.transform.scale(youLoseSurf, (youLoseSurf.get_width() * 6, youLoseSurf.get_height() * 6))
youLoseRect.topleft = ((window_width//2) - youLoseSurf.get_width()//2, ((window_height//3) - youLoseSurf.get_height()//2))

overlay = pygame.Surface(window.get_size(), pygame.SRCALPHA)
print(overlay.get_height())
overlay.fill((0, 0, 0, 120))  # black with alpha (0–255)

smallFont = pygame.font.Font('fonts/PixelifySans.ttf', 15)
largeFont = pygame.font.Font('fonts/PixelifySans.ttf', 30)

circleSurf = pygame.image.load('sprites/circle2.png').convert_alpha()
circleSurf = pygame.transform.scale(circleSurf, (circleSurf.get_width() * 1.5, circleSurf.get_height() * 1.5))
circleRect = circleSurf.get_rect()
circleRect.center = window_width//2, window_height//2

cannon_surface = pygame.Surface((50, 25), pygame.SRCALPHA)
cannon = pygame.draw.rect(cannon_surface, 'white', cannon_surface.get_rect())
cannonBorder = pygame.draw.rect(cannon_surface, 'black', cannon_surface.get_rect(), 4)
cannonPos = pygame.math.Vector2((window_height//2), (window_width//2 + 40))

addedRotation = 0
wallRadius = 75
wallWidth = 25
wallHeight = 50
wallSurf = pygame.Surface((wallWidth, wallHeight), pygame.SRCALPHA)
wallRect = pygame.draw.rect(wallSurf, 'white', wallSurf.get_rect())
wallLevel = 0
wallHitbox = [
    pygame.Vector2(-wallWidth / 2, wallHeight / 2),
    pygame.Vector2(wallWidth / 2, wallHeight / 2),
    pygame.Vector2(-wallWidth / 2, -wallHeight / 2),
    pygame.Vector2(wallWidth / 2, -wallHeight / 2)
]
wallHealthArray = []

snakeSheet = pygame.image.load('sprites/snake.png').convert_alpha()
snakeFrames = [
    sprite_sheet(snakeSheet, 0, 0, 16, 16),  # Frame 0
    sprite_sheet(snakeSheet, 0, 16, 16, 16)  # Frame 1
]
for i in snakeFrames:
    snakeFrames[snakeFrames.index(i)] = pygame.transform.scale(sprite_sheet(i, 0, 0, 16, 16), (64, 64))

quitBtn = Button("Quit", 0, 0, 50, 25, (255, 0, 0), (255, 255, 255))
retryBtn = Button("Retry", window_width//2 - 50, window_height//2, 100, 50, (255, 255, 255), (0, 0, 0), largeFont)

wallUpgradeBtnCost = 10
wallUpgradeBtn = Button(f'Unlock: {wallUpgradeBtnCost}', window.get_width()//2 - 50, (window.get_height() - menuHeight) + menuHeight//2 - 20, 100, 40, (255, 255, 255), (0, 0, 0), smallFont)

snakeSpawned = False
while running:
    deltaTime = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mousePos.y < window_height:
            Bullets()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not pauseMenu:
                    pauseMenu = True
                else:
                    pauseMenu = False
            if event.key == pygame.K_SPACE:
                Snake()

    mouse_pressed = pygame.mouse.get_pressed()
    mousePos = pygame.math.Vector2(pygame.mouse.get_pos())

    # Draw/Update Elements
    pygame.draw.rect(window, backgroundColor, (0, 0, window.get_width(), window.get_height() - menuHeight))

    if quitBtn.isPressed:
        running = False

    if retryBtn.isPressed:
        retryBtn.isPressed = False
        playerHealthPoints = 100
        snakeArray.clear()
        bulletsArray.clear()
        playerCurrency = 0
        wallLevel = 0
        wallUpgradeBtnCost = 10
        wallUpgradeBtn.value = f'Upgrade: {wallUpgradeBtnCost}'
        snakeSpawnRate = 5
        addedRotation = 0
        snakeSpawned = False

    for s in snakeArray:
        s.update()

    for i in bulletsArray:
        i.update()

    if playerHealthPoints > 0 and not pauseMenu:
        cannonAngle = math.atan2(mousePos.y - window_height//2, mousePos.x - window_width//2)
        cannonPos = pygame.math.Vector2((window_width//2), (window_height//2)) + pygame.math.Vector2(math.cos(cannonAngle), math.sin(cannonAngle)) * 25 #=radius

        if round(time.perf_counter()) % snakeSpawnRate == 0:
            if not snakeSpawned:
                Snake()
                snakeSpawned = round(time.perf_counter())
                snakeSpawnRate = snakeSpawnRate - 1 if snakeSpawnRate > 1 else snakeSpawnRate
            elif snakeSpawned != round(time.perf_counter()):
                snakeSpawned = False
        else:
            if snakeSpawned:
                snakeSpawned = False

        addedRotation += 0.01

    # Draw surfaces
    rotated_cannon = pygame.transform.rotate(cannon_surface, -math.degrees(cannonAngle))
    window.blit(rotated_cannon, rotated_cannon.get_rect(center=cannonPos))

    window.blit(circleSurf, circleRect)

    for i in range(wallLevel):
        wallAngle = (addedRotation + ((2 * math.pi) / wallLevel) * i)
        wallOrigin = (window_width / 2 + wallRadius * math.cos(wallAngle), window_height / 2 + wallRadius * math.sin(wallAngle))

        if wallHealthArray[i] == True:
            wallSurf.set_alpha(255)

            wallHitboxRotated = []
            for (x, y) in wallHitbox:
                rx = x * math.cos(wallAngle) - y * math.sin(wallAngle)
                ry = x * math.sin(wallAngle) + y * math.cos(wallAngle)

                wallHitboxRotated.append((wallOrigin[0] + rx, wallOrigin[1] + ry))

            # pygame.draw.line(window, 'red', wallHitboxRotated[0], wallHitboxRotated[1])
            # pygame.draw.line(window, 'red', wallHitboxRotated[1], wallHitboxRotated[3])
            # pygame.draw.line(window, 'red', wallHitboxRotated[3], wallHitboxRotated[2])
            # pygame.draw.line(window, 'red', wallHitboxRotated[2], wallHitboxRotated[0])

            for s in snakeArray:
                collision = True
                axes_to_check = []
                for p in range(len(wallHitboxRotated)):
                    p1 = wallHitboxRotated[p]
                    p2 = wallHitboxRotated[(p + 1) % len(wallHitboxRotated)]
                    edge = (p2[0] - p1[0], p2[1] - p1[1])
                    axes_to_check.append((-edge[1], edge[0]))

                for h in range(len(s.rotatedHitboxPoints)):
                    p1 = s.rotatedHitboxPoints[h]
                    p2 = s.rotatedHitboxPoints[(h + 1) % len(s.rotatedHitboxPoints)]
                    edge = (p2[0] - p1[0], p2[1] - p1[1])
                    axes_to_check.append((-edge[1], edge[0]))

                for axis in axes_to_check:
                    dotsA = [d[0] * axis[0] + d[1] * axis[1] for d in wallHitboxRotated]
                    dotsB = [d[0] * axis[0] + d[1] * axis[1] for d in s.rotatedHitboxPoints]

                    if max(dotsA) < min(dotsB) or max(dotsB) < min(dotsA):
                        collision = False  # Separating axis found
                        break

                if collision:
                    s.healthPoints = 0
                    wallHealthArray[i] = time.perf_counter()
                    print("wall collision!")

        else:
            timeSince = time.perf_counter() - wallHealthArray[i]
            if timeSince >= 8:
                wallHealthArray[i] = True
            alpha = int((timeSince / 5) * 255)
            wallSurf.set_alpha(alpha)

        rotatedWallSurf = pygame.transform.rotate(wallSurf, -math.degrees(wallAngle))
        rotatedWallRect = rotatedWallSurf.get_rect(center=wallOrigin)
        window.blit(rotatedWallSurf, rotatedWallRect)

    text_surface = smallFont.render(str(playerHealthPoints), True, 'white')
    text_rect = text_surface.get_rect()
    text_rect.center = int((window_width * (playerHealthPoints/100))/2), 10

    if playerHealthPoints > 0:
        pygame.draw.rect(window, 'red', (0, 0, window_width * (playerHealthPoints / 100), 20))
        window.blit(text_surface, text_rect)
    else:
        window.blit(overlay, (0, 0))
        window.blit(youLoseSurf, youLoseRect)
        retryBtn.update()

    if pauseMenu:
        window.blit(overlay, (0, 0))
        quitBtn.update()

    for bullet in bulletsArray:
        for snake in snakeArray:
            if circle_polygon_collision(bullet.pos, bullet.hitbox, snake.rotatedHitboxPoints):
                snake.healthPoints = 0
                bullet.healthPoints -= 1
                playerCurrency += snake.value

    pygame.draw.rect(window, "darkgray", (0, window.get_height() - menuHeight, window.get_width(), window.get_height()))

    wallUpgradeBtn.update()
    if wallUpgradeBtn.isPressed and playerCurrency >= wallUpgradeBtnCost and wallLevel < 6:
        wallLevel += 1
        wallUpgradeBtnCost += 10
        wallUpgradeBtn.value = f'Upgrade: {wallUpgradeBtnCost}'
        wallHealthArray.append(True)
    elif playerCurrency < wallUpgradeBtnCost:
        wallUpgradeBtn.is_hover = True
    elif wallLevel >= 6:
        wallUpgradeBtn.value = 'MAXED'
        wallUpgradeBtn.setHover = True

    currencySurface = largeFont.render(str(playerCurrency), True, 'black')
    currencyRect = currencySurface.get_rect()
    currencyRect.center = (window_width - 40, 40)
    window.blit(currencySurface, currencyRect)

    pygame.display.flip()
