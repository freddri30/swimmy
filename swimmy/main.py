import pygame
import random

# Set up the Enemy's brain
class Enemy():
    # Enemy constructor function
    def __init__(self, x, y, speed, size):
        # Make the Enemy's variables 
        self.x = x
        self.y = y
        self.pic = pygame.image.load("./assets/Fish03_A.png")
        self.speed = speed
        self.size = size
        self.hitbox = pygame.Rect(self.x, self.y, int(self.size*1.2), self.size)

        # shrink the enemy pic
        self.pic = pygame.transform.scale(self.pic, (int(self.size*1.25), self.size))

        # Flip the pic if the enemy is moving left
        if self.speed < 0:
            self.pic = pygame.transform.flip(self.pic, True, False)
        
    # Enemy update function (stuff to happen over and over again)
    def update(self, screen):
        self.x += self.speed
        self.hitbox.x += self.speed
        #pygame.draw.rect(screen, (255, 0 ,255), self.hitbox)
        screen.blit(self.pic, (self.x, self.y))
       
    
# End of enemy class

# Start the game
pygame.init()
game_width = 1000
game_height = 650
screen = pygame.display.set_mode((game_width, game_height))
clock = pygame.time.Clock()
running = True
# Load all the pictures for our game

background_pic = pygame.image.load("./assets/Scene_A.png")
player_pic = pygame.image.load("./assets/Fish03_open.png")

# make some variables for our player
player_x = 15
player_y = 30
player_speed = 10
player_size = 30
player_facing_left = False
player_hitbox = pygame.Rect(player_x, player_y, int(player_size*1.25), player_size)
player_alive = True

# Make some variables for the HUD (head-up display)
score = 0
score_font = pygame.font.SysFont("helveticaneuedeskinterface", 30)
score_text = score_font.render("score: "+str(score), 1, (255,255,255))
play_button_pic = pygame.image.load("./assets/BtnPlayIcon.png")

# Make the enemies spawing timer variable
enemy_timer_max = 25
enemy_timer = enemy_timer_max 

# Make the enemies array
enemies = []




# ***************** Loop Land Below *****************
# Everything under 'while running' will be repeated over and over again
while running:
    # Makes the game stop if the player clicks the X or presses esc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
    # Check what keys the player is pressing               
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_facing_left = False
        player_x += player_speed
    if keys[pygame.K_LEFT]:
        player_facing_left = True
        player_x -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed
    if keys[pygame.K_UP]:
         player_y-= player_speed
    if keys[pygame.K_SPACE]:
        player_size += 2
    

    screen.blit(background_pic, (0, 0))

    # spawn a naw enemy whenever enemy_timer hits 0
    enemy_timer -= 1
    if enemy_timer <= 0:
        new_enemy_y = random.randint(0, game_height)
        new_enemy_speed = random.randint(2, 5)
        new_enemy_size = random.randint(player_size/2, player_size*2)
        if random.randint(0, 1) == 0:
            enemies.append(Enemy(-new_enemy_size*2, new_enemy_y, new_enemy_speed, new_enemy_size ))
        else:
            enemies.append(Enemy(game_width, new_enemy_y, -new_enemy_speed, new_enemy_size))
        enemy_timer = enemy_timer_max

    # Update all of the enemies

    for enemy in enemies:
        enemy.update(screen)

    if player_alive:
        # update the player hitbox
        player_hitbox.x = player_x
        player_hitbox.y = player_y
        player_hitbox.width = int(player_size * 1.25)
        player_hitbox.height = player_size
        #pygame.draw.rect(screen, (255, 255, 255), player_hitbox)
        
        # Check to see when the player hits an Enemy
        for enemy in enemies:
            if player_hitbox.colliderect(enemy.hitbox):
                if player_size >= enemy.size:
                    score += enemy.size
                    player_size += 2
                    enemies.remove(enemy)
                else:
                    player_alive = False
        
        # Draw the player pic
        player_pic_small = pygame.transform.scale(player_pic, (int(player_size*1.25), player_size))
        if player_facing_left:
            player_pic_small = pygame.transform.flip(player_pic_small, True, False)
        screen.blit(player_pic_small, (player_x, player_y))

    if player_alive:
        score_text = score_font.render("score: "+str(score), 1, (255,255,255))
    else:
        score_text = score_font.render("final score: "+str(score), 1, (255,255,255))
    screen.blit(score_text, (30, 30))

    # Tell pygame to update the screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("MY GAME fps: " + str(clock.get_fps()))
