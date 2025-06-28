import pygame

pygame.init()

# Створення вікна
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Pygame Hvostia")

# Завантаження іконки
icon = pygame.image.load('image/icon.png')  # ← виправлено 'igame' на 'image'
pygame.display.set_icon(icon)

# Створення синього прямокутника
square = pygame.Surface((50, 170))
square.fill('blue')

# Основний цикл
running = True  # ← виправлено 'runing' і 'white' на 'running' і 'while'
while running:

    screen.fill((0, 0, 0))  # ← очищення екрану (чорний фон)
    screen.blit(square, (0, 0))

    pygame.draw.circle(screen,'red',(250,150), 30)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()  # ← винесено з циклу
