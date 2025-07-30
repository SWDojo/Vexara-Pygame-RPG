##pygame 2.6.1 (SDL 2.28.4, Python 3.12.4)
from operator import truediv
from pickle import TRUE
import os, sys, pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from config import *
from debug import *
from sprites import *

class Game:
    def __init__(self):
        #Program Initilization
        pygame.init()
        #Screen
        pygame.display.set_caption('Kingdoms of Ash: Oathbreaker')
        #icon
        win_icon = pygame.image.load("KOAOIcon.png")
        pygame.display.set_icon(win_icon)
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        #Clock(FPS)
        self.clock = pygame.time.Clock()
        #Run
        self.running = True

    def load_map(self):
        for row_index, row in enumerate(tilemap):
            for col_index, tile in enumerate(row):
                if tile == 'B':
                    Block(self, col_index, row_index)
                if tile == 'P':
                    Player(self, col_index, row_index)

    def new_game(self):
        #New Game
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.npc = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.load_map()

        #Calculate World Size In Pixels
        map_width = len(tilemap[0]) * TILESIZE
        map_height = len(tilemap) * TILESIZE
        
        self.camera = Camera(map_width, map_height)

    def events(self):
        #Game Loop Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        #Game Loop Updates
        self.all_sprites.update()
        #Find Player
        for sprite in self.all_sprites:
            if isinstance(sprite, Player):
                self.camera.update(sprite)

    def draw(self):
        #Game Loop Draw
        self.screen.fill(BLACK)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.clock.tick(FPS)
       ###debug()
        pygame.display.update()

    def main(self):
        #Game Loop
          while self.playing:
            self.events()
            self.update()
            self.draw()
            self.game_over()
            self.intro_screen()
          self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        pass

g = Game()
g.intro_screen()
g.new_game()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()