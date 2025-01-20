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

camera_offset = pygame.math.Vector2(0, 0)

def update_camera(player, camera_offset):
    """Update the camera's offset based on the player's position."""
    global SCREEN_WIDTH, SCREEN_HEIGHT

    # Center the camera on the player
    camera_offset.x = player.rect.centerx - SCREEN_WIDTH // 2
    camera_offset.y = player.rect.centery - SCREEN_HEIGHT // 2

    # Optional: Clamp camera to the bounds of the level
    camera_offset.x = max(0, min(camera_offset.x, LEVEL_WIDTH - SCREEN_WIDTH))
    camera_offset.y = max(0, min(camera_offset.y, LEVEL_HEIGHT - SCREEN_HEIGHT))

    return camera_offset

LEVEL_WIDTH = 1000  # Example: Make your level larger than the screen
LEVEL_HEIGHT = 800

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
        self.rect_checker = None
        self.standing_on = None

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
        self.update_rect()


    def jump(self):
        print("jumping -> self.jumping ", self.jumping, " self.on_ground -> ", self.on_ground)
        if (self.jumping == False ) and (self.on_ground == True):
            self.jumping == True
            self.velocity_y = -10
            self.on_ground = False
            self.standing_on = None

    def apply_gravity(self):
        x, y = self.position
        if not self.on_ground:
            self.velocity_y += GRAVITY
        y += self.velocity_y
        self.position = (x, y)

    def check_collisions(self, platforms, camera_offset):
        pygame.draw.rect(BUFFER, (255, 0, 0), self.rect, 2)  # Player collision box
        

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                print("collided at -> ", platform.name)
                
                if self.velocity_y > 0 and self.rect.bottom <= platform.rect.top + 10:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.standing_on = platform
                    print("now standing on => ", self.standing_on.name)

                elif self.rect.right >= platform.rect.left and self.rect.left <= platform.rect.right:
                    if self.position[0] < platform.rect.centerx:  
                        self.rect.right = platform.rect.left
                    elif self.position[0] > platform.rect.centerx:  
                        self.rect.left = platform.rect.right
           
                self.position = self.rect.topleft
        
        if self.on_ground and self.velocity_y == 0:
            if self.check_falling_off() == True:
                self.on_ground = False
                self.standing_on = None
                     
                    
    def check_falling_off(self):
        if not self.standing_on:
            return True
        self.check_rect = self.rect.copy()
        self.check_rect.y += 1  
        # self.standing_on.up
        if self.check_rect.colliderect(self.standing_on.rect):
            return False
        
        return True  

    def update_rect(self):
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.rect.topleft = self.position




class Player(Character):
    def __init__(self, speed, position=(0, 0), keys=ASTR_KEYS):
        super().__init__("player", position) # calls the character's constructor 
        self.width = 30
        self.height = 40
        self.left = False
        self.right = True
        self.KEYS = keys

    def takeDamage(self):
        pass

    def interactWithObject(self, obj):
        pass

    def updatePlayerState(self):
        pass


    def update(self, platforms, camera_offset):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[self.KEYS["left"]]:
            dir = "left"
        elif pressed_keys[self.KEYS["right"]]:
            dir = "right"
        elif pressed_keys[self.KEYS["up"]]:
            dir = "up"
        else:
            dir = "none"
        self.move(dir)

        self.apply_gravity()
        self.check_collisions(platforms, camera_offset)
        self.update_rect()

class Enemy(Character):
    def __init__(self, position=(0, 0)):
        super().__init__("enemy", position)

        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  

class Alien(Player):
    def __init__(self, position=(0, 0), keys=ASTR_KEYS, speed=5, phaseAbilityDuration=10, shapeShiftState="default"):
        super().__init__(speed, position, keys)  # calls the player's constructor
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

class Astronaut(Player):
    def __init__(self, position=(0, 0), keys=ASTR_KEYS, speed=5, oxygenLevel=100, toolbox=None, currentEnvironment="space_station"):
        super().__init__(speed, position, keys)  # calls the player's constructor
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
AstrChar = Astronaut(position=(200, 100), keys=ASTR_KEYS)
AlienChar = Alien(position = (220, 100), keys=ALIEN_KEYS)

background = pygame.image.load("assets/bg.png") 

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name="none"):
        super().__init__()
        self.name = name
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.original_position = pygame.math.Vector2(x, y)
        self.rect = self.image.get_rect(topleft=(x, y))


    # def draw(self, buffer):
    #     buffer.blit(self.image, self.rect) 

    def draw(self, buffer, camera_offset):
        self.updateRect(camera_offset)
        buffer.blit(self.image, self.rect) 

    def updateRect(self, camera_offset):
        # self.rect.topleft = self.original_position - camera_offset
        pass

def is_on_platform(character, platform): #checks if character is on platform 
    return (character.rect.bottom == platform.rect.top and character.rect.right > platform.rect.left and character.rect.left < platform.rect.right)   

platforms = pygame.sprite.Group()
platforms.add(Platform(100, 300, 200, 20, name="starter"))
platforms.add(Platform(100, 150, 20, 150, name="left bound"))
platforms.add(Platform(200, 220, 200, 20, name="starter"))

platforms.add(Platform(400, 150, 150, 40, name="upper right flat"))
platforms.add(Platform(400, 100, 40, 150, name="upper right vert"))


#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

 
#Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # BUFFER.fill(WHITE)
    # BUFFER.blit(background, (0, 0))

    camera_offset = update_camera(AstrChar, camera_offset)

    BUFFER.fill(WHITE)
    BUFFER.blit(background, (-camera_offset.x, -camera_offset.y))

    for platform in platforms:
        platform.draw(BUFFER, camera_offset)
    
    for platform in platforms:
        pygame.draw.rect(BUFFER, (255, 0, 0), platform.rect, 2)  # Platform collision boxes

    AstrChar.update(platforms, camera_offset)
    # AlienChar.update(platforms)

    # Draw both characters
    BUFFER.blit(AstrChar.image, AstrChar.rect)
    # BUFFER.blit(AlienChar.image, AlienChar.rect)

    pygame.display.update()
    FramePerSec.tick(FPS)

    BUFFER.fill(WHITE)

    # BUFFER.blit(background, (0,0))