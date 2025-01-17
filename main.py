import time
import pygame, sys
from pygame.locals import *
import random, time
import json

with open("character_config.json", "r") as config_file:
    CHARACTER_CONFIG = json.load(config_file)

#Initialzing 
pygame.init()
vec = pygame.math.Vector2 

#Setting up FPS 
FPS = 30
FramePerSec = pygame.time.Clock()

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Other Variables for use in the program
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
ACC = 0.5
FRIC = -0.12
GRAVITY = 0.5

#Create a white screen 
BUFFER = pygame.display.set_mode((600,400))
BUFFER.fill(WHITE)
pygame.display.set_caption("Game")


class Character(pygame.sprite.Sprite):
    def __init__(self, characterType, position=(0, 0)):
        self.position = position  # (x, y) coordinates of the players
        self.speed = CHARACTER_CONFIG.get(characterType, {}).get("speed", 5) # movement speed
        self.velocity_y = 0
        self.characterType = characterType

        self.image = pygame.Surface((30, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.jumping = False
        self.on_ground = False

    def move(self, direction):
        x, y = self.position
        if direction == "none":
            pass
        elif direction == 'up':
            self.jump()
        elif direction == 'down':
            y -= self.speed
        elif direction == 'left':
            x -= self.speed
        elif direction == 'right':
            x += self.speed

        self.position = (x, y)

    def jump(self):
        print("jumping -> self.jumping ", self.jumping, " self.on_ground -> ", self.on_ground)
        if (self.jumping == False ) and (self.on_ground == True):
            self.jumping == True
            self.velocity_y = -10
            self.on_ground = False
            print("self.velocity_y - >", self.velocity_y)

    def apply_gravity(self):
        x, y = self.position
        if not self.on_ground:
            self.velocity_y += GRAVITY
        y += self.velocity_y
        self.position = (x, y)

    def check_collisions(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top  
                    self.velocity_y = 0  
                    self.on_ground = True  

    def update_rect(self):
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

ASTR_KEYS = {
    "left": K_a,  
    "right": K_d,  
    "up": K_w  
}

ALIEN_KEYS = {
    "left": K_LEFT,  
    "right": K_RIGHT,  
    "up": K_UP  
}

class Player(Character):
    def __init__(self, speed, position=(0, 0)):
        super().__init__("player", position) # calls the character's constructor 
        self.width = 30
        self.height = 40
        self.left = False
        self.right = True

    def takeDamage(self):
        pass

    def interactWithObject(self, obj):
        pass

    def updatePlayerState(self):
        pass

class Enemy(Character):
    def __init__(self, position=(0, 0)):
        super().__init__("enemy", position)

        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  

class Alien(Player):
    def __init__(self, position=(0, 0), speed=5, phaseAbilityDuration=10, shapeShiftState="default"):
        super().__init__(speed, position)  # calls the player's constructor
        self.phaseAbilityDuration = phaseAbilityDuration 
        self.shapeShiftState = shapeShiftState
        self.image = pygame.image.load("assets/alien_still.png")  
        self.image = pygame.transform.scale(self.image, (30, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def phaseThroughWalls(self):
        pass

    def shapeShift(self):
        pass

    def update(self, platforms):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[ALIEN_KEYS["left"]]:
            dir = "left"
        elif pressed_keys[ALIEN_KEYS["right"]]:
            dir = "right"
        elif pressed_keys[ALIEN_KEYS["up"]]:
            dir = "up"
        else:
            dir = "none"
        self.move(dir)

        self.apply_gravity()
        self.check_collisions(platforms)
        self.update_rect()

AlienChar = Alien(position=(300, 100))

class Astronaut(Player):
    def __init__(self, position=(0, 0), speed=5, oxygenLevel=100, toolbox=None, currentEnvironment="space_station"):
        super().__init__(speed, position)  # calls the player's constructor
        self.baseSpeed = speed             # base speed (used on the space station, matches the alien's)
        self.oxygenLevel = oxygenLevel     
        self.toolbox = toolbox if toolbox is not None else []  # toolbox is an empty list, updates as the player gets items
        self.currentEnvironment = currentEnvironment  # this is the environment of the level (Space station or Planet), this affects speed
        self.rfid_use = False  # boolean flag for RFID scanner usage
        self.rfid_detectable = []  # list to store detected items or enemies
        self.lastDepletionTime = time.time() #tracks the time oxygen was last depleted

        self.image = pygame.image.load("assets/astronaut_still.png")
        self.image = pygame.transform.scale(self.image, (30, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def oxygenDeplete(self, oxygenLevel):
        currentTime = time.time()
        if currentTime - self.lastDepletionTime >= 2: #compares the last time oxygen was depleted to the current time
            if self.oxygenLevel > 0: #oxygen cannot deplete if it is at 0
                oxygenLevel -= 1
        return oxygenLevel
        #oxygen is depleted by 1% every 2 seconds, will stop depleting after it reaches 0

    def repairObject(self): #use tools to repair or interact with objects
        pass

    def replenishOxygen(self): #called whenever the astronaut interacts with an oxygen refill station
        if self.interactWithObject(oxygenStation) == True:
            oxygenLevel = 100
        return oxygenLevel

    def scanWithRFID(self, items_on_screen):
        self.rfid_detectable = items_on_screen

        overlay = "\n".join(f"Detected: {item}" for item in self.rfid_detectable)
        print("RFID Scan Results:\n" + overlay)
        pygame.time.wait(1000) #duration of the scan
        self.rfid_use = False #finishes the scan

    def update(self, platforms):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[ASTR_KEYS["left"]]:
            dir = "left"
        elif pressed_keys[ASTR_KEYS["right"]]:
            dir = "right"
        elif pressed_keys[ASTR_KEYS["up"]]:
            dir = "up"
        else:
            dir = "none"
        self.move(dir)

        self.apply_gravity()
        self.check_collisions(platforms)
        self.update_rect()

class Environment:
    def __init__(self, gravity, background, ambientSound):
        self.gravity = gravity
        
    def applyGravity(self, gravity):
        pass

    def loadLevel(self):
        pass

    def renderEnvironment(self):
        pass
 
#Setting up Sprites        
AstrChar = Astronaut(position=(200, 100))

background = pygame.image.load("assets/bg.png") 

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))


    def draw(self, buffer):
        buffer.blit(self.image, self.rect) 

def is_on_platform(character, platform): #checks if character is on platform 
    return (character.rect.bottom == platform.rect.top and character.rect.right > platform.rect.left and character.rect.left < platform.rect.right)   

platforms = pygame.sprite.Group()
platforms.add(Platform(100, 300, 150, 20))
platforms.add(Platform(400, 100, 150, 40))
platforms.add(Platform(400, 100, 40, 150))


#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

 
#Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    BUFFER.fill(WHITE)
    BUFFER.blit(background, (0, 0))

    for platform in platforms:
        platform.draw(BUFFER)

    AstrChar.update(platforms)
    AlienChar.update(platforms)

    # Draw both characters
    BUFFER.blit(AstrChar.image, AstrChar.rect)
    BUFFER.blit(AlienChar.image, AlienChar.rect)

    pygame.display.update()
    FramePerSec.tick(FPS)

    BUFFER.fill(WHITE)

    BUFFER.blit(background, (0,0))