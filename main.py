import pygame

pygame.init()

screen = pygame.display.set_mode((680, 510))
pygame.display.set_caption("Pygame Hvostia")

icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

myfont = pygame.font.Font('fonts/RobotoSlab-Bold.ttf', 40)
text_surface = myfont.render('My Game', False, (255, 220, 0))

bg = pygame.image.load('images/background.png').convert()

walk_right = [
    pygame.image.load('images/player/right/frame_00.png').convert_alpha(),
    pygame.image.load('images/player/right/frame_01.png').convert_alpha(),
    pygame.image.load('images/player/right/frame_02.png').convert_alpha(),
    pygame.image.load('images/player/right/frame_03.png').convert_alpha(),
]
walk_left = [
    pygame.image.load('images/player/left/frame_04.png').convert_alpha(),
    pygame.image.load('images/player/left/frame_05.png').convert_alpha(),
    pygame.image.load('images/player/left/frame_06.png').convert_alpha(),
    pygame.image.load('images/player/left/frame_07.png').convert_alpha()
]

enemy1_img = pygame.image.load('images/bat.png').convert_alpha()
enemy2_img = pygame.image.load('images/enemy2.png').convert_alpha()
bullet_img = pygame.image.load('images/bullet.png').convert_alpha()

# Таймери ворогів
ENEMY1_TIMER_EVENT = pygame.USEREVENT + 1
ENEMY2_TIMER_EVENT = pygame.USEREVENT + 2

pygame.time.set_timer(ENEMY1_TIMER_EVENT, 1000)

enemy_list = []
bullets = []  # Список куль

bg_sound = pygame.mixer.Sound('sound/bg_sound.wav')
bg_sound.play(loops=-1)

GROUND_LEVEL = 350
ENEMY_Y = 375  # вороги нижче за гравця

BULLET_SPEED = 15

def reset_game():
    pygame.time.set_timer(ENEMY2_TIMER_EVENT, 0)
    pygame.time.set_timer(ENEMY1_TIMER_EVENT, 1000)
    bullets.clear()
    return {
        'player_anim_count': 0,
        'bg_x': 0,
        'player_speed': 5,
        'player_x': 150,
        'player_y': GROUND_LEVEL,
        'player_direction': 'right',
        'is_jump': False,
        'jump_count': 10,
        'game_over': False
    }

state = reset_game()
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(30)  # FPS

    screen.blit(bg, (state['bg_x'], 0))
    screen.blit(bg, (state['bg_x'] + bg.get_width(), 0))

    player_image = walk_right[state['player_anim_count']] if state['player_direction'] == 'right' else walk_left[state['player_anim_count']]
    player_rect = player_image.get_rect(topleft=(state['player_x'], state['player_y']))

    # Малюємо ворогів і рухаємо їх
    for enemy in enemy_list[:]:
        enemy_img = enemy1_img if enemy['type'] == 1 else enemy2_img
        enemy_rect = enemy_img.get_rect(topleft=enemy['pos'])
        screen.blit(enemy_img, enemy['pos'])

        if not state['game_over']:
            enemy['pos'][0] -= 10

        if enemy['pos'][0] < -enemy_img.get_width():
            if enemy['type'] == 1 and not state['game_over']:
                pygame.time.set_timer(ENEMY2_TIMER_EVENT, 3000)
            enemy_list.remove(enemy)

        # Колізія з гравцем (тільки якщо гравець на землі)
        if not state['game_over'] and player_rect.colliderect(enemy_rect):
            if state['player_y'] >= GROUND_LEVEL - 10:
                state['game_over'] = True
                pygame.time.set_timer(ENEMY1_TIMER_EVENT, 0)
                pygame.time.set_timer(ENEMY2_TIMER_EVENT, 0)

    # Рух фону
    if not state['game_over']:
        state['bg_x'] -= 2
        if state['bg_x'] <= -bg.get_width():
            state['bg_x'] = 0

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False

        if event.type == ENEMY1_TIMER_EVENT and not state['game_over']:
            if not any(e['type'] == 1 for e in enemy_list):
                enemy_list.append({'pos': [700, ENEMY_Y], 'type': 1})

        if event.type == ENEMY2_TIMER_EVENT and not state['game_over']:
            enemy_list.append({'pos': [700, ENEMY_Y], 'type': 2})
            pygame.time.set_timer(ENEMY2_TIMER_EVENT, 0)

        if state['game_over'] and keys[pygame.K_r]:
            state = reset_game()
            enemy_list.clear()

    if not state['game_over']:
        # Рух гравця
        if keys[pygame.K_LEFT] and state['player_x'] > 50:
            state['player_x'] -= state['player_speed']
            state['player_direction'] = 'left'
        elif keys[pygame.K_RIGHT] and state['player_x'] < 600:
            state['player_x'] += state['player_speed']
            state['player_direction'] = 'right'

        # Стрибок
        if not state['is_jump']:
            if keys[pygame.K_UP]:
                state['is_jump'] = True
        else:
            if state['jump_count'] >= -10:
                neg = 1
                if state['jump_count'] < 0:
                    neg = -1
                state['player_y'] -= (state['jump_count'] ** 2) * 0.3 * neg
                state['jump_count'] -= 1
            else:
                state['is_jump'] = False
                state['jump_count'] = 10

        # Стрільба по пробілу — додаємо кулю
        if keys[pygame.K_SPACE]:
            if len(bullets) == 0 or (bullets and bullets[-1]['x'] > state['player_x'] + 50):
                direction = 1 if state['player_direction'] == 'right' else -1
                bullet_x = state['player_x'] + 40 if direction == 1 else state['player_x']
                bullet_y = state['player_y'] + 30
                bullets.append({'x': bullet_x, 'y': bullet_y, 'dir': direction})

        # Анімація гравця
        state['player_anim_count'] = (state['player_anim_count'] + 1) % len(walk_right)

    # Малюємо гравця
    screen.blit(player_image, (state['player_x'], state['player_y']))

    # Малюємо кулі і оновлюємо їхню позицію
    for bullet in bullets[:]:
        bullet_rect = bullet_img.get_rect(topleft=(bullet['x'], bullet['y']))
        screen.blit(bullet_img, (bullet['x'], bullet['y']))
        bullet['x'] += BULLET_SPEED * bullet['dir']

        # Перевірка колізії кулі з ворогами
        for enemy in enemy_list[:]:
            enemy_img = enemy1_img if enemy['type'] == 1 else enemy2_img
            enemy_rect = enemy_img.get_rect(topleft=enemy['pos'])
            if bullet_rect.colliderect(enemy_rect):
                enemy_list.remove(enemy)
                if bullet in bullets:
                    bullets.remove(bullet)
                break

        # Видалення кулі, якщо вона вийшла за межі екрану
        if bullet['x'] < -bullet_img.get_width() or bullet['x'] > 680:
            if bullet in bullets:
                bullets.remove(bullet)

    # Текст
    screen.blit(text_surface, (250, 10))

    if state['game_over']:
        lose_text = myfont.render('You lose! Press R to restart', True, (255, 0, 0))
        screen.blit(lose_text, (100, 200))

    pygame.display.update()

pygame.quit()
