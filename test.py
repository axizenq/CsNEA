# import pygame
# import sys

# # Initialize Pygame
# pygame.init()

# # Screen dimensions
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 600

# # Colors
# BLUE = (0, 120, 255)
# GREEN = (0, 200, 0)
# WHITE = (255, 255, 255)
# GRAY = (150, 150, 150)

# # Player settings
# PLAYER_WIDTH = 40
# PLAYER_HEIGHT = 60
# PLAYER_SPEED = 5
# JUMP_FORCE = -15
# GRAVITY = 0.8

# # Create screen
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("PyPlatformer")

# clock = pygame.time.Clock()

# class Player(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
#         self.image.fill(BLUE)
#         self.rect = self.image.get_rect(center=(SCREEN_WIDTH//4, SCREEN_HEIGHT//2))
        
#         self.velocity = 0
#         self.on_ground = False

#     def update(self, platforms):
#         keys = pygame.key.get_pressed()
        
#         # Horizontal movement
#         if keys[pygame.K_LEFT]:
#             self.rect.x -= PLAYER_SPEED
#         if keys[pygame.K_RIGHT]:
#             self.rect.x += PLAYER_SPEED
        
#         # Jumping
#         if keys[pygame.K_SPACE] and self.on_ground:
#             self.velocity = JUMP_FORCE
#             self.on_ground = False
        
#         # Apply gravity
#         self.velocity += GRAVITY
#         self.rect.y += self.velocity
        
#         # Platform collision
#         self.on_ground = False
#         for platform in platforms:
#             if self.rect.colliderect(platform.rect):
#                 if self.velocity > 0:  # Falling
#                     self.rect.bottom = platform.rect.top
#                     self.velocity = 0
#                     self.on_ground = True
#                 elif self.velocity < 0:  # Jumping
#                     self.rect.top = platform.rect.bottom
#                     self.velocity = 0

# class Platform(pygame.sprite.Sprite):
#     def __init__(self, x, y, width, height):
#         super().__init__()
#         self.image = pygame.Surface((width, height))
#         self.image.fill(GREEN)
#         self.rect = self.image.get_rect(topleft=(x, y))

# # Create groups
# all_sprites = pygame.sprite.Group()
# platforms = pygame.sprite.Group()

# # Create player
# player = Player()
# all_sprites.add(player)

# # Create sample level
# platform_list = [
#     Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),  # Ground
#     Platform(SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT - 120, 100, 20),
#     Platform(SCREEN_WIDTH//4, SCREEN_HEIGHT - 200, 100, 20),
#     Platform(600, 400, 100, 20),
# ]

# for platform in platform_list:
#     all_sprites.add(platform)
#     platforms.add(platform)

# # Game loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Update
#     all_sprites.update(platforms)

#     # Keep player in screen bounds
#     if player.rect.left < 0:
#         player.rect.left = 0
#     if player.rect.right > SCREEN_WIDTH:
#         player.rect.right = SCREEN_WIDTH

#     # Draw
#     screen.fill(WHITE)
#     all_sprites.draw(screen)

#     pygame.display.flip()
#     clock.tick(60)

# pygame.quit()
# sys.exit()