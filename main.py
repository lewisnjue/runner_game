import sys
import pygame
import os
from random import randint

# Initialize pygame
pygame.init()
current_time = 0

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def collisions(player, obstacles):
    global game_active
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                game_active = False

def player_animation():
    global PLAYER_WALK_INDEX, PLAYER_WALK_LIST, PLAYER_SURF, PLAYER_RECT, PLAYER_JUMP
    if PLAYER_RECT.bottom < 300:
        PLAYER_SURF = PLAYER_JUMP
    else:
        PLAYER_WALK_INDEX += 0.1
        if PLAYER_WALK_INDEX >= len(PLAYER_WALK_LIST):
            PLAYER_WALK_INDEX = 0
        PLAYER_SURF = PLAYER_WALK_LIST[int(PLAYER_WALK_INDEX)]

def snail_animation():
    global SNAIL_WALK_INDEX, SNAIL_WALK_LIST, SNAIL_SURF
    SNAIL_WALK_INDEX += 0.1
    if SNAIL_WALK_INDEX > len(SNAIL_WALK_LIST):
        SNAIL_WALK_INDEX = 0
    SNAIL_SURF = SNAIL_WALK_LIST[int(SNAIL_WALK_INDEX)]

def fly_animation():
    global fly_surf_index, fly_surf_list, fly_surf
    fly_surf_index += 0.1
    if fly_surf_index > len(fly_surf_list):
        fly_surf_index = 0
    fly_surf = fly_surf_list[int(fly_surf_index)]

def display_score():
    global current_time
    current_time = pygame.time.get_ticks() // 1000 - start_time // 1000
    score_surf = FONT.render(f'SCORE: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    SCREEN.blit(score_surf, score_rect)

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:
                SCREEN.blit(SNAIL_SURF, obstacle_rect)
            else:
                SCREEN.blit(fly_surf, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

FONT = pygame.font.Font(resource_path('font/Pixeltype.ttf'), 50)
SCREEN = pygame.display.set_mode((800, 400))
game_active = False
start_time = 0
SKY_SURF = pygame.image.load(resource_path('graphics/Sky.png')).convert()
GROUND_SURF = pygame.image.load(resource_path('graphics/ground.png')).convert()

SNAIL_WALK_1 = pygame.image.load(resource_path('graphics/snail/snail1.png')).convert_alpha()
SNAIL_WALK_2 = pygame.image.load(resource_path('graphics/snail/snail2.png')).convert_alpha()
SNAIL_WALK_LIST = [SNAIL_WALK_1, SNAIL_WALK_2]
SNAIL_WALK_INDEX = 0
JUMP_SOUND = pygame.mixer.Sound(resource_path('audio/jump.mp3'))
JUMP_SOUND.set_volume(0.5)
PLAY_SOUND = pygame.mixer.Sound(resource_path('audio/music.wav'))
SNAIL_SURF = SNAIL_WALK_LIST[SNAIL_WALK_INDEX]

PLAYER_WALK_1 = pygame.image.load(resource_path('graphics/Player/player_walk_1.png')).convert_alpha()
PLAYER_WALK_2 = pygame.image.load(resource_path('graphics/Player/player_walk_2.png')).convert_alpha()
PLAYER_JUMP = pygame.image.load(resource_path('graphics/Player/jump.png'))
PLAYER_WALK_LIST = [PLAYER_WALK_1, PLAYER_WALK_2]
PLAYER_WALK_INDEX = 0
PLAYER_SURF = PLAYER_WALK_LIST[PLAYER_WALK_INDEX]
PLAYER_RECT = PLAYER_SURF.get_rect(midbottom=(80, 300))
SNAIL_RECT = SNAIL_SURF.get_rect(bottomright=(600, 300))

fly_surf_1 = pygame.image.load(resource_path('graphics/Fly/Fly1.png'))
fly_surf_2 = pygame.image.load(resource_path('graphics/Fly/Fly2.png'))
fly_surf_list = [fly_surf_1, fly_surf_2]
fly_surf_index = 0
fly_surf = fly_surf_list[fly_surf_index]

obstacle_rect_list = []
PLAYER_STAND_IMPORT = pygame.image.load(resource_path('graphics/Player/player_stand.png')).convert_alpha()
PLAYER_STAND = pygame.transform.rotozoom(PLAYER_STAND_IMPORT, 0, 2)
PLAYER_STAND_RECT = PLAYER_STAND.get_rect(center=(400, 200))

pygame.display.set_caption('RUNNER')
clock = pygame.time.Clock()
SNAIL_X_POS = 600
PLAYER_GRAVITY = 0
obstancle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstancle_timer, 1500)
PLAY_SOUND.play(loops=-5)

while True:
    if game_active:
        clock.tick(60)
        SCREEN.blit(SKY_SURF, (0, 0))
        SCREEN.blit(GROUND_SURF, (0, 300))
        SCREEN.blit(SNAIL_SURF, SNAIL_RECT)

        PLAYER_GRAVITY += 1
        PLAYER_RECT.y += PLAYER_GRAVITY
        if PLAYER_RECT.bottom >= 300:
            PLAYER_RECT.bottom = 300

        SCREEN.blit(PLAYER_SURF, PLAYER_RECT)
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        display_score()
        player_animation()
        snail_animation()
        fly_animation()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and PLAYER_RECT.bottom >= 300:
                    PLAYER_GRAVITY = -20
                    JUMP_SOUND.play()
            if event.type == pygame.MOUSEBUTTONDOWN and PLAYER_RECT.bottom >= 300:
                if PLAYER_RECT.collidepoint((pygame.mouse.get_pos())):
                    PLAYER_GRAVITY = -20
                    JUMP_SOUND.play()
            if event.type == obstancle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(SNAIL_SURF.get_rect(bottomright=(randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1100), 210)))

        collisions(PLAYER_RECT, obstacle_rect_list)
    else:
        start_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    obstacle_rect_list = []
                    SNAIL_RECT.left = 800

        SCREEN.fill((94, 129, 162))
        SCREEN.blit(PLAYER_STAND, PLAYER_STAND_RECT)
        game_name = FONT.render('pixel runner', False, (111, 196, 169))
        game_name_rect = game_name.get_rect(center=(400, 70))
        SCREEN.blit(game_name, game_name_rect)
        game_messange = FONT.render('press space to run', False, (111, 196, 169))
        game_messange_rect = game_messange.get_rect(center=(400, 350))
        if current_time > 0:
            score_surf = FONT.render(f'YOUR SCORE: {current_time}', False, (64, 64, 64))
            score_rect = score_surf.get_rect(center=(400, 350))
            SCREEN.blit(score_surf, score_rect)
        else:
            SCREEN.blit(game_messange, game_messange_rect)

    pygame.display.update()
