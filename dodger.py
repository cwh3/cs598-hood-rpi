#!/usr/bin/python

import sys
import random
import pygame
import time
import sys



WIDTH = 800
HEIGHT = 600
score = 0
high_score = 0

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
gray = (211,211,211)
tomato = (255,9,71)


class Enemy():

    MIN_SIZE = 15
    MAX_SIZE = 40

    

    def __init__(self):

        self.size = random.randint(self.MIN_SIZE, self.MAX_SIZE)
        self.rect = pygame.Rect(random.randint(0, WIDTH), 0-self.size,
                                self.size, self.size)
        self.surface = pygame.Surface((self.rect.width, self.rect.height))
        self.speed = random.randint(1,5)
        self.color = (random.randint(130, 255), random.randint(130, 255), random.randint(130, 255))
        self.surface.fill(self.color)

    

    def move(self, increase):
        self.rect.bottom += self.speed + increase

    

    def draw(self, surface):
        surface.blit(self.surface, self.rect)



class EnemyManager():

    def __init__(self):

        self.counter = 0
        self.rate = 100

    

    def generate(self):

        self.counter += self.rate
        self.rate += 0.5
        if self.counter > 1000:
            self.counter %= 1000
            return True
        return False



class Player():

    def __init__(self, x):

        self.rect = pygame.Rect(x, HEIGHT-50, 25, 25)
        self.surface = pygame.Surface((25, 25))
        self.color = (255, 255, 255)
        self.surface.fill(self.color)

    

    def draw(self, surface):

        surface.blit(self.surface, self.rect)

    

    def move(self, dest):

        self.rect.centerx = dest
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(WIDTH, self.rect.right)



	
class Game():


    def __init__(self, surface):

        pygame.init()
        self.surface = surface
        self.intro()


    
    def _check_collisions(self, enemies, player):

        for enemy in enemies:
            if enemy.rect.colliderect(player.rect):
                return True
        return False

    def text_objects(text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()
    
    def button(msg, x, y, w, h, i, a, action = None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(screen, a,(x,y,w,h))
            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(screen, i,(x,y,w,h))

        smallText = pygame.font.Font("freesansbold.ttf", 20)
        textSurf, textRect = Game.text_objects(msg, smallText)
        textRect.center = (x+(w/2), y+(h/2))
        screen.blit(textSurf, textRect)

    def quitgame(self):
        pygame.quit()
        quit()
        

    def intro(self):

        global score
        global high_score
        now = time.time()
        seconds = int(now % 60)
        if score > high_score:
            high_score = score
        while True:
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            background_image = "background.png"
            background = pygame.transform.scale(pygame.image.load(background_image), (WIDTH, HEIGHT)).convert()
            screen.blit(background,(0,0))
            title = pygame.font.Font(None, 60).render('ASTRODODGE', True, tomato)
            instructions = pygame.font.Font(None, 30).render(("HIGH SCORE: " + str(high_score)), True, tomato)
            self.surface.blit(title, ((WIDTH-title.get_rect().width)/2, 40))
            self.surface.blit(instructions, ((WIDTH-instructions.get_rect().width)/2, 90))
            
            Game.button("PLAY", 150,450,100,50, white, blue, self.play)
            Game.button("QUIT", 550,450,100,50, white, red, self.quitgame)
            
            #print(mouse)
            pygame.display.update()
                          

    

    def play(self):

        # initialize variables
        clock = pygame.time.Clock()
        enemies = []
        enemymanager = EnemyManager()
        player = Player(pygame.mouse.get_pos()[0])
        increase = 0
        lives = 3
        global score
        score = 0
        background_image = "background.png"
        background = pygame.transform.scale(pygame.image.load(background_image), (WIDTH, HEIGHT)).convert()

        while lives > 0:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit(0)
                if e.type == pygame.MOUSEMOTION:
                    player.move(e.pos[0])
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    nitro = 1
                if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                    nitro = 0
      
            # draw surface
            screen.blit(background,(0,0)) 
       

            # draw enemies
            for enemy in enemies:
                enemy.move(increase)
                enemy.draw(self.surface)
                if enemy.rect.top > HEIGHT:
                    enemies.remove(enemy)
            if enemymanager.generate() and len(enemies) < 41:
                enemies.append(Enemy())
            if score < 0 and score < 10000:
                increase = 0
            if score > 10000 and score < 40000:
                increase = 1
            if score > 40000 and score < 80000:
                increase = 2
            if score > 80000 and score < 100000:
                increase = 4
            message = ('Score: ' + str(score))
            font = pygame.font.Font(None, 40)
            text = font.render(message, 1, white)
            screen.blit(text, (600,50))
            
            # draw player
            player.draw(self.surface)
           
            # increment score
            score += len(enemies)
            
            # check for collisions - if so, remove all enemies and subtract a life
            if self._check_collisions(enemies, player):
                enemies = []
                lives -= 1
                if lives > 0:
                    time.sleep(1)
                if lives == 0:
                    gameover()
                    self.intro()
            #print(score)
            pygame.display.update()
            clock.tick(60)
        sys.exit(0)

def gameover():
        message_display("GAME OVER!")
		
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 100)
    TextSurf, TextRect = text_objects(text,largeText)
    TextRect.center = ((WIDTH/2), (HEIGHT/2))
    screen.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(2)

def text_objects(text, font):
    textSurface = font.render(text, True, red)
    return textSurface, textSurface.get_rect()           



if __name__ == '__main__':
    pygame.init()
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('AstroDodge')
    screen = pygame.display.get_surface()
    g = Game(surface)
