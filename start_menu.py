# Eric Lu

import doodle_jump
import pygame
from pygame import *

def show():

    left = False
    right = False
    platform1List = [] # List of platform1

    # Prepares the txt files
    doodle_jump.random()

    # Create a sprite group
    entities = pygame.sprite.Group()

    # Create/adds player to the group
    player = Player(120, 270, 300, 1)
    entities.add(player)

    # Create/adds platform to the group
    platform = Platform1(750, 110)
    entities.add(platform)
    platform1List.append(platform)

    # Creates window and title
    pygame.init()
    screen = pygame.display.set_mode((500, 800))
    pygame.display.set_caption('Doodle Jump - Eric Lu')

    # Loads background image
    bg = pygame.image.load('background.png')
    bg = pygame.transform.scale(bg, (500, 800))

    # Creates clock
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        for e in pygame.event.get():

            if (e.type == KEYDOWN and (e.key == K_RIGHT or e.key == K_LEFT or e.key == K_d or e.key == K_a)):
                return

        # Draw background    
        screen.blit(bg, (0, 0))

        # Write Title
        font1 = pygame.font.SysFont('Times New Roman', 54)
        title_text = font1.render('Doodle Jump', 1, (0, 0, 0))
        screen.blit(title_text, (100, 35))

        # Write 'Eric Lu'
        font2 = pygame.font.SysFont('Times New Roman', 36)
        eric_text = font2.render('Eric Lu', 1, (0, 0, 0))
        screen.blit(eric_text, (190, 120))

        # Write 'Play using Arrow Keys'
        font3 = pygame.font.SysFont('Times New Roman', 28)
        press_text = font3.render('Play using Arrow Keys', 1, (0, 0, 0))
        screen.blit(press_text, (125, 200))

        # Update player
        player.update(platform1List)

        # Draw sprites
        entities.draw(screen)

        # Update screen
        pygame.display.update()


class Entity(pygame.sprite.Sprite):
    
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)

class Player(Entity):

    def __init__(self, x, y, side, direction):

        Entity.__init__(self)

        # Load/scales image
        self.image = pygame.image.load('character.png')
        self.image = pygame.transform.scale(self.image, (side, side))
        self.image = pygame.transform.flip(self.image, True, False)
        
        self.rect = Rect(x, y, side, side)

        self.rect.x = x
        self.rect.y = y
        self.y_vel = 0
        self.side = side

    def update(self, platform1List):

        # Simulates y-axis gravity
        self.y_vel += 0.4

        # Adds the position according to velocity
        self.rect.y += self.y_vel

        # Changes the rect of the Player
        self.rect = Rect(self.rect.x, self.rect.y, self.side, self.side-1)

        # Checks collision
        self.collide1(platform1List)

    def collide1(self, platformList):

        for platform in platformList:
            if pygame.sprite.collide_rect(self, platform):
                self.y_vel = -12

class Platform1(Entity):

    def __init__(self, y, x):

        Entity.__init__(self)
        self.image = pygame.image.load('platform1.png')
        self.image = pygame.transform.scale(self.image, (250, 35))
        self.rect = Rect(x, y, 250, 35)
