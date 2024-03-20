import pygame
import random
import sys
import time
import asyncio

"""
https://noahbeck01.github.io/NoahBeck01.io/Pygame_WebSnake/
"""

# game variablen
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
pygame.display.set_caption('Snake Game')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
score = 0
high_sore = 0
last_score = 0


def init_game():
    global snake_pos, snake_body, food_pos, food_spawn, direction, change_to, score
    snake_pos = [100, 50]
    snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]
    food_pos = [random.randrange(1, (SCREEN_WIDTH // 10)) * 10, random.randrange(1, (SCREEN_HEIGHT // 10)) * 10]
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

def check_death_or_eat():
    global food_pos, food_spawn, score
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(1, (SCREEN_WIDTH // 10)) * 10, random.randrange(1, (SCREEN_HEIGHT // 10)) * 10]
    food_spawn = True


    for pos in snake_body:
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    pygame.display.update()

    if snake_pos[0] < 0 or snake_pos[0] > SCREEN_WIDTH - 10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > SCREEN_HEIGHT - 10:
        game_over()

    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

def update_snake_position():
    global direction, snake_pos, snake_body
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    snake_body.insert(0, list(snake_pos))

def game_over():
    global high_sore, score
    text_surface = my_font.render('You Died', False, "WHITE")
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(text_surface, text_rect)
    pygame.display.update()
    time.sleep(3)
    if score > high_sore:
        high_sore = score
    init_game()

def score_update():
    global score
    score_surf = my_font.render(f'Score: {score}', True, (255, 255, 255))
    score_rect = score_surf.get_rect()
    if score < 10:
        score_rect.topleft = (680, 0)  # Setzen Sie die Position des Rechtecks
    else:
        score_rect.topleft = (665, 0)
    screen.blit(score_surf, score_rect.topleft)
    pygame.display.update(score_rect)


def high_score_display():
    global high_sore
    high_score_surf = my_font.render(f'Highscore: {high_sore}', True, (255, 255, 255))
    high_score_rect = high_score_surf.get_rect()
    high_score_rect.topleft = (0,0)
    screen.blit(high_score_surf, high_score_rect.topleft)
    pygame.display.update(high_score_rect)

async def main():
    init_game()
    global change_to, score, last_score # Die change_to-Variable muss global sein
    last_score = score

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                if event.key == pygame.K_r:
                    init_game()

        screen.fill('Black')

        update_snake_position()
        check_death_or_eat()
        score_update()
        high_score_display()



        pygame.display.flip() # Verwenden Sie pygame.display.flip() anstelle von pygame.display.update()
        clock.tick(30)
        await asyncio.sleep(0)


asyncio.run(main())
