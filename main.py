import pygame

pygame.init()

# Створення вікна
screen = pygame.display.set_mode((680, 510))
pygame.display.set_caption("Pygame Hvostia")

# Завантаження іконки
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

# Завантаження шрифту та тексту
myfont = pygame.font.Font('fonts/RobotoSlab-Bold.ttf', 40)
text_surface = myfont.render('My Game', False, (255, 0, 0))

# Завантаження зображення фону
bg = pygame.image.load('images/background.jpg')

walk_right = [
    pygame.image.load('images/player/right/player_walk_r1.png'),
    pygame.image.load('images/player/right/player_walk_r2.png'),
    pygame.image.load('images/player/right/player_walk_r3.png'),
    pygame.image.load('images/player/right/player_walk_r4.png')
]

walk_left = [
    pygame.image.load('images/player/left/player_walk_l1.png'),
    pygame.image.load('images/player/left/player_walk_l2.png'),
    pygame.image.load('images/player/left/player_walk_l3.png'),
    pygame.image.load('images/player/left/player_walk_l4.png')
]

player_anim_count = 0
bg_x = 0

bg_sound = pygame.mixer.Sound('sound/teleport.wav')
bg_sound.play(loops=-1)  # запускаємо звук циклічно

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(10)  # FPS

    # Малюємо рухомий фон
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + bg.get_width(), 0))

    bg_x -= 2
    if bg_x <= -bg.get_width():
        bg_x = 0

    # Малюємо анімацію гравця вправо
    screen.blit(walk_right[player_anim_count], (200, 200))
    player_anim_count = (player_anim_count + 1) % len(walk_right)

    # Малюємо текст
    screen.blit(text_surface, (10, 10))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
