from turtle import width
import pygame
from config import *
import os
import math
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):    
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(YELLOW)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()

        #Vertical Movement
        self.rect.x += self.x_change
        self.collide_blocks('x')

        #Horizontal Movement
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0 

#Collision On Blocks
    def collide_blocks(self, direction):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if hits:
            if direction == 'x':
                if self.x_change > 0:  # moving right
                    self.rect.right = hits[0].rect.left
                if self.x_change < 0:  # moving left
                    self.rect.left = hits[0].rect.right
            if direction == 'y':
                if self.y_change > 0:  # moving down
                    self.rect.bottom = hits[0].rect.top
                if self.y_change < 0:  # moving up
                    self.rect.top = hits[0].rect.bottom

    def movement(self):
        key_press = pygame.key.get_pressed()

        #WASD
        if key_press[pygame.K_a]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if key_press[pygame.K_d]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if key_press[pygame.K_w]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if key_press[pygame.K_s]:
            self.y_change += PLAYER_SPEED

        #Arrow Keys
        if key_press[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if key_press[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if key_press[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if key_press[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update (self, target):
        x = -target.rect.centerx + WIN_WIDTH // 2
        y = -target.rect.centery + WIN_HEIGHT // 2

        #Limit Scrolling To Map Size
        x = min(0, x) #Left
        y = min(0, y) #Top
        x = max(-(self.width - WIN_WIDTH), x) #Right
        y = max (-(self.height - WIN_HEIGHT), y) #Left

        self.camera = pygame.Rect(x, y, self.width, self.height)

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y