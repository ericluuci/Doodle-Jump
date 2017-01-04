# Eric Lu

import pygame
from pygame import *
import sys
from random import randint
import start_menu

max_height = -30000

def random1():
    
    # Generates platform1 positions
    text_file = open('random1.txt','w')
    text_file.write('750 210\n')
    for x in range (650, max_height, -100):
        text_file.write(str(x)+' '+str(randint(0, 500 - 70))+'\n')
    text_file.close()

def random2():
    
    # Generates platform2 positions
    text_file = open('random2.txt','w')
    for x in range (randint(100,600), max_height, randint(-1000, -500)):
        text_file.write(str(x)+' '+str(randint(0, 500 - 70))+'\n')
    text_file.close()

def random3():
    
    # Generates platform3 positions
    text_file = open('random3.txt','w')
    for x in range (randint(-800, 200), max_height, randint(-3500, -2000)):
        text_file.write(str(x)+' '+str(randint(0, 500 - 70))+'\n')
    text_file.close()

def random():
    
    # Generates all platform positions
    random1()
    random2()
    random3()

def main():

    direction = 1 # Left <- 0 | 1 -> Right
    left = False
    right = False
    points = 0
    gameOver = False
    platform1List = [] # List of platform1
    platform2List = [] # List of platform2
    platform3List = [] # List of platform3

    # Create a sprite group
    entities = pygame.sprite.Group()

    # Create/adds player to the group
    player = Player(240, 580, 30, 1) # (x-position, y-position, Side, Direction)
    entities.add(player)


    # Create/add platform1 to the group
    platform1_text = open('random1.txt','r')
    for line in platform1_text:
        platform = Platform1(int(line.split()[0]), int(line.split()[1]))
        entities.add(platform)
        platform1List.append(platform)

    # Create/add platform2 to the group
    platform2_text = open('random2.txt','r')
    for line in platform2_text:
        platform = Platform2(int(line.split()[0]), int(line.split()[1]))
        entities.add(platform)
        platform2List.append(platform)

    # Create/add platform3 to the group
    platform3_text = open('random3.txt','r')
    for line in platform3_text:
        platform = Platform3(int(line.split()[0]), int(line.split()[1]))
        entities.add(platform)
        platform3List.append(platform)


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

            if (e.type == QUIT):
                pygame.quit()
                sys.exit()

            if (e.type == KEYDOWN and (e.key == K_LEFT or e.key == K_a)):
                left =  True
                direction = 0

            if (e.type == KEYDOWN and (e.key == K_RIGHT or e.key == K_d)):
                right = True
                direction = 1
                
            if (e.type == KEYUP and (e.key == K_LEFT or e.key == K_a)):
                left = False

            if (e.type == KEYUP and (e.key == K_RIGHT or e.key == K_d)):
                right = False
            
            if (e.type == KEYDOWN and e.key == K_r):
                
                direction = 1
                left = False
                right = False
                points = 0
                gameOver = False
                
                platform1List = []
                platform2List = []
                platform3List = []

                random()
                
                entities = pygame.sprite.Group()
                player = Player(240, 580, 30, 1)
                entities.add(player)
                
                platform1_text = open('random1.txt','r')
                for line in platform1_text:
                    platform = Platform1(int(line.split()[0]), int(line.split()[1]))
                    entities.add(platform)
                    platform1List.append(platform)
                    
                platform2_text = open('random2.txt','r')
                for line in platform2_text:
                    platform = Platform2(int(line.split()[0]), int(line.split()[1]))
                    entities.add(platform)
                    platform2List.append(platform)

                platform3_text = open('random3.txt','r')
                for line in platform3_text:
                    platform = Platform3(int(line.split()[0]), int(line.split()[1]))
                    entities.add(platform)
                    platform3List.append(platform)

        if (player.rect.y + 30 >= 798):
            # Game over state
            gameOver = True

        if (not gameOver):
            
            # Draw background    
            screen.blit(bg, (0, 0))

            # Update player
            player.update(left, right, direction, platform1List, platform2List, platform3List)


            # Update platform1
            for platform in platform1List:
                if (not player.same):
                    platform.update(player.y_vel)

            # Update platform2
            for platform in platform2List:
                if (not player.same):
                    platform.update(player.y_vel)

            # Update platform3
            for platform in platform3List:
                if (not player.same):
                    platform.update(player.y_vel)


            # Mimic camera movement
            if (player.rect.y <= 400):
                for platform in platform1List:
                    platform.update_camera(player.rect.y)
                for platform in platform2List:
                    platform.update_camera(player.rect.y)
                for platform in platform3List:
                    platform.update_camera(player.rect.y)
                player.rect.y = (400+1)


            # Draw sprites
            entities.draw(screen)

            # Update/draw points
            if (player.y_vel < 0 and not player.same):
                points += int(abs(player.y_vel))
            font = pygame.font.SysFont('Times New Roman', 16)
            points_text = font.render('Points : ' + str(points), 1, (0, 0, 0))
            screen.blit(points_text, (400, 10))

        elif (gameOver):

            # Draw background    
            screen.blit(bg, (0, 0))

            # Draw sprites
            entities.draw(screen)

            # Write 'Game Over!'
            font1 = pygame.font.SysFont('Times New Roman', 48)
            end_text = font1.render('Game Over!', 1, (0, 0, 0))
            screen.blit(end_text, (130, 100))

            # Write 'Press 'R' to try again!'
            font2 = pygame.font.SysFont('Times New Roman', 36)
            retry_text = font2.render("Press 'R' to try again!", 1, (0, 0, 0))
            screen.blit(retry_text, (100, 400))

            # Draw points
            font = pygame.font.SysFont('Times New Roman', 16)
            points_text = font.render('Points : ' + str(points), 1, (0, 0, 0))
            screen.blit(points_text, (400, 10))

        # Update screen
        pygame.display.update()

class Entity(pygame.sprite.Sprite):
    
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)

class Player(Entity):

    def __init__(self, x, y, side, direction):

        Entity.__init__(self)
        self.image_base = pygame.image.load('character.png')
        self.image_base = pygame.transform.scale(self.image_base, (side, side))
        self.rect = Rect(x, y, side, side)

        self.rect.x = x
        self.rect.y = y
        self.x_vel = 0
        self.y_vel = 0
        self.side = side
        self.direction = direction
        self.same = False

    def update(self, left, right, direction, platform1List, platform2List, platform3List):

        # X Boundary
        if (self.rect.x < 0):
            self.rect.x = 0
            self.x_vel = 0
        elif (self.rect.x + self.side >= 500):
            self.rect.x = 500 - self.side
            self.x_vel = 0

        # Increases the character's velocity
        if (left):
            self.x_vel -= 0.35
        if (right):
            self.x_vel += 0.35

        # Simulates x-axis friction
        if (self.x_vel >= -0.05 and self.x_vel <= 0.05):
            self.x_vel = 0
        elif (self.x_vel > 0):
            self.x_vel -= 0.1
        elif (self.x_vel < 0):
            self.x_vel += 0.1

        # Simulates y-axis gravity
        self.y_vel += 0.2

        # Adds the position according to velocity
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        # Changes the rect of the Player
        self.rect = Rect(self.rect.x, self.rect.y, self.side, self.side-1)

        # Flips the character image
        if (direction != self.direction):
            self.image = self.image_base
        else:
            self.direction = direction
            self.image = pygame.transform.flip(self.image_base, True, False)

        self.collide1(platform1List)
        self.collide2(platform2List)
        self.collide3(platform3List)

    def collide1(self, platformList):

        for platform in platformList:
            if pygame.sprite.collide_rect(self, platform):
                
                if (self.y_vel >= 0):

                    if (not platform.touch):
                        self.same = False
                    elif (platform.touch):
                        self.same = True
                    
                    self.y_vel = -7
                    if (self.same):
                        self.y_vel -= 1

                    for test in range(0, platformList.index(platform)+1):
                        platformList[test].touch = True

    def collide2(self, platformList):

        for platform in platformList:
            if pygame.sprite.collide_rect(self, platform):
                
                if (self.y_vel >= 0):

                    if (not platform.touch):
                        self.same = False
                    elif (platform.touch):
                        self.same = True
                    
                    self.y_vel = -5
                    if (self.same):
                        self.y_vel -= 1

                    for test in range(0, platformList.index(platform)+1):
                        platformList[test].touch = True

    def collide3(self, platformList):

        for platform in platformList:
            if pygame.sprite.collide_rect(self, platform):
                
                if (self.y_vel >= 0):

                    if (not platform.touch):
                        self.same = False
                    elif (platform.touch):
                        self.same = True
                    
                    self.y_vel = -15
                    for test in range(0, platformList.index(platform)+1):
                        platformList[test].touch = True

class Platform1(Entity):

    def __init__(self, y, x):

        Entity.__init__(self)
        self.image = pygame.image.load('platform1.png')
        self.image = pygame.transform.scale(self.image, (70, 15))
        self.rect = Rect(x, y, 70, 15)
        self.rect.x = x
        self.rect.y = y
        self.touch = False

    def update(self, y_vel):

        if (y_vel <= 0):
            self.rect.y -= y_vel

        self.rect = Rect(self.rect.x, self.rect.y, 70, 15)

    def update_camera(self, y):
        
        self.rect.y += (400 - y)

        self.rect = Rect(self.rect.x, self.rect.y, 70, 15)

class Platform2(Entity):

    def __init__(self, y, x):

        Entity.__init__(self)
        self.image = pygame.image.load('platform2.png')
        self.image = pygame.transform.scale(self.image, (70, 15))
        self.rect = Rect(x, y, 70, 15)
        self.rect.x = x
        self.rect.y = y
        self.touch = False

    def update(self, y_vel):

        if (y_vel <= 0):
            self.rect.y -= y_vel

        if (not self.touch):
            self.rect = Rect(self.rect.x, self.rect.y, 70, 15)
        elif (self.touch):
            self.rect = Rect(self.rect.x, self.rect.y, 0, 0)
            self.image = pygame.image.load('platform2_break.png')
            self.image = pygame.transform.scale(self.image, (70, 26))

    def update_camera(self, y):
        
        self.rect.y += (400 - y)
        self.rect = Rect(self.rect.x, self.rect.y, 70, 15)
        
        if (self.touch):
            self.rect = Rect(self.rect.x, self.rect.y, 0, 0)

class Platform3(Entity):

    def __init__(self, y, x):

        Entity.__init__(self)
        self.image = pygame.image.load('platform3.png')
        self.image = pygame.transform.scale(self.image, (70, 25))
        self.rect = Rect(x, y, 70, 25)
        self.rect.x = x
        self.rect.y = y
        self.touch = False

    def update(self, y_vel):

        if (y_vel <= 0):
            self.rect.y -= y_vel
        
        self.rect = Rect(self.rect.x, self.rect.y, 70, 25)

    def update_camera(self, y):
        
        self.rect.y += (400 - y)

        self.rect = Rect(self.rect.x, self.rect.y, 70, 25)

if __name__ == '__main__':
    start_menu.show()
    main()
