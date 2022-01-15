# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 20:16:34 2021

@author: Vincent
tutorial from https://www.youtube.com/watch?v=FfWpgLFMI7w
"""
import pygame, sys, random, math
from pygame import mixer

#initialise the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800,600))

#Sur la fenetre, point de coordonnées (0,0) situé en haut a gauche de l'écran

#Title and icon
pygame.display.set_caption("Space invaders")
icon = pygame.image.load("resource/space-ship.png")
pygame.display.set_icon(icon)
meteoriteImg = pygame.image.load("resource/meteorite.png")

#Background
listBackground = []
for i in range (12):
    file = ("resource/background/background-",".png")
    file = str(i).join(file)
    listBackground.append(pygame.image.load(file))

#Player
playerImg = pygame.image.load("resource/octopus.png")
playerX = 370
playerY = 480
playerXChange = 0

#Affichage score
scoreX = 30
scoreY = 16
font = pygame.font.Font("resource/font/Game-Of-Squids.ttf", 32)
def showScore (x, y) :
    score = font.render("Score " + str(scoreValue), True, (255, 255, 255))
    screen.blit(score, (x, y))

#Game over
gameOverX = 210
gameOverY = 250
fontGameOver = pygame.font.Font("resource/font/Game-Of-Squids.ttf", 52)
def showGameOver (x, y) :
    gameOver = fontGameOver.render("Game Over ", True, (255, 255, 255))
    screen.blit(gameOver, (x, y))
    
#Son ambiance
mixer.music.load("resource/music/pic-jul.mp3")
mixer.music.play(-1)

#Enemy
class Enemy:
    """define an enemy"""
    def __init__(self):
        """initialise sa position"""  
        self.Img = pygame.image.load("resource/erotic.png")
        self.X = random.randint(0,768)
        self.Y = random.randint(25,490)
        self.X_dir = random.randint(0,1)*2-1

    def show(self):
        """faire apparaitre l icone de l ennemi"""
        screen.blit(self.Img, (self.X, self.Y) )

#Meteorite
class Meteorite():
    def __init__ (self):
        self.Img = pygame.transform.rotate(meteoriteImg, 225)
        self.X = 0
        self.Y = 0

    def show(self):
        """faire apparaitre l icone de la météorite"""
        screen.blit(self.Img, (self.X, self.Y) )
                
#faire apparaitre l'icone du joueur 
def player (x, y):
    screen.blit(playerImg, (x, y) )
        
      

scoreValue = 0    
ind = 0
rotation = 5
playGame = True
#déclarer un objet enemy
enemyArray = [] #liste des ennemis 

#declarer un objet meteorite
meteoriteArray = []
def enemyLevel(x, enemyArray):
    for i in range(x*20):
        enemyArray.append(Enemy())
    return enemyArray
    
#numéro de la vague d'ennemis 
vague = 1
#meteorite = Meteorite()
#game loop
while True :
    #Screen 
    screen.fill((0,0,0)) #valeur couleur rgb ->0 a 255, affiche l'arrière plan
    ind += 0.007
    if playGame :
        screen.blit(listBackground[int(ind)%12], (0,0)) #indices de [0;11]
    for event in pygame.event.get():
        #Quit button 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
        #if keystroke is pressed check wether it is right or left
        if event.type == pygame.KEYDOWN: #appuyer sur une touche 
            #print("A keystroke is pressed")
            if event.key == pygame.K_LEFT and 0< playerX:
                #print("Left arrow is pressed ")
                playerXChange = -0.5
            if event.key == pygame.K_RIGHT and playerX< 736:
                #print("Right arrow is pressed ")   
                playerXChange = 0.5
            if event.key == pygame.K_SPACE and len(meteoriteArray) <= 2 :
                #print("Space is pressed")
                meteoriteArray.append(Meteorite())
                #print ("nombre de meteorites :", len(meteoriteArray))
                meteoriteArray[-1].X = playerX
                meteoriteArray[-1].Y = playerY
                meteoriteSound = mixer.Sound("resource/music/blast-sound.mp3")
                meteoriteSound.play()

        if event.type == pygame.KEYUP: #appuyer sur une touche 
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXChange = 0
    
    if len(enemyArray) == 0 and playGame :
        enemyArray = enemyLevel(vague, enemyArray)
        vague +=1

    #Player movement 
    playerX += playerXChange
    
    #ennemy movement 
    i = 0
    for enemy in enemyArray :
        enemy.X += enemy.X_dir*0.1
        #Perdre
        if enemy.Y >= 500 :
            playGame = False
        if not playGame :
            enemyArray.pop(i)
        #l'ennemi touche la bordure de l'écran
        elif enemy.X <= 0 or enemy.X >= 760:  
            enemy.X_dir =- enemy.X_dir      #changer la direction de déplacement
            enemy.Y += 5                  #descendre de 5 pixels
        #Collision, test if a collision has occurded
        else :
            j = 0
            for meteorite in meteoriteArray :
                distance=math.sqrt((enemy.X-meteorite.X)**2 + (enemy.Y-meteorite.Y)**2)
                if distance < 27 :
                    collisionSound = mixer.Sound("resource/music/bomb.mp3")
                    collisionSound.play()
                    enemyArray.pop(i)
                    meteoriteArray.pop(j)
                    scoreValue += 1
                    print (scoreValue)
                if meteorite.Y <= 0:
                    meteoriteArray.pop(j)
                j += 1
        i +=1

    #meteorite movement

    for meteorite in meteoriteArray :
        meteorite.Y -= 0.3
        meteorite.show()
    for enemy in enemyArray :
        enemy.show()

    player(playerX, playerY) #affiche le joueur par dessus l arriere plan (respecter l ordre)
    showScore(scoreX, scoreY)
    if not playGame :
        showGameOver(gameOverX, gameOverY)
    pygame.display.update() 