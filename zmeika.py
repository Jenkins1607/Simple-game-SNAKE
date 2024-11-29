import pygame
import time
import random

# Инициализация Pygame
pygame.init()

# Определение цветов
white = (255, 255, 255)
red = (213, 50, 80)
snake_color = (57, 230, 57)

# Размеры окна
width = 1280
height = 720
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption('Змейка')

# Настройки змейки
snake_block = 30
initial_speed = 15

# Шрифт для отображения счета
font_style = pygame.font.SysFont("bahnschrift", 25)

# Загрузка фонового изображения и изображения яблока
background_image = pygame.image.load('Fonchik.png')
apple_image = pygame.image.load('yablocko.png')
apple_image = pygame.transform.scale(apple_image, (snake_block, snake_block))

# Загрузка звуковых файлов
pygame.mixer.music.load('fon.mp3')
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)

try:
    game_over_sound = pygame.mixer.Sound('game_over.mp3')
    restart_sound = pygame.mixer.Sound('restart.mp3')
    eat_sound = pygame.mixer.Sound('apple.mp3')
except pygame.error as e:
    print(f"Ошибка загрузки звуков: {e}")


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, snake_color, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [width / 6, height / 3])


def draw_score(score):
    score_text = font_style.render(f"Счет: {score}", True, white)
    dis.blit(score_text, [10, 10])


def gameLoop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
    apple_count = 0

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    collision_occurred = False  # Переменная состояния для отслеживания столкновения

    while not game_over:
        while game_close:
            dis.fill((0, 0, 0))
            message("Нажми R для рестарта или Q для выхода", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                        pygame.mixer.music.stop()
                    if event.key == pygame.K_r:
                        restart_sound.play()
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= width:
            x1 = 0
        elif x1 < 0:
            x1 = width - snake_block
        if y1 >= height:
            y1 = 0
        elif y1 < 0:
            y1 = height - snake_block

        x1 += x1_change
        y1 += y1_change

        dis.blit(background_image, (0, 0))
        dis.blit(apple_image, (foodx, foody))

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
        # Проверка на столкновение с самой собой (конец игры)
        for x in snake_List[:-1]:
            if x == snake_Head:
                collision_occurred = True

        our_snake(snake_block, snake_List)

        if collision_occurred and not game_close:
            game_close = True
            game_over_sound.play()  # Воспроизведение звука проигрыша только при столкновении
            time.sleep(2)  # Задержка для проигрыша звука

        if (foodx - 10 <= x1 <= foodx + snake_block + 10) and (foody - 10 <= y1 <= foody + snake_block + 10):
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            apple_count += 1

            eat_sound.play()

        draw_score(apple_count)

        # Обновление экрана
        pygame.display.update()

        # Управление скоростью змейки (фиксированная скорость)
        clock.tick(initial_speed + (Length_of_snake // 5))

        # Остановка фоновой музыки перед выходом или перезапуском игры.
    pygame.mixer.stop()


clock = pygame.time.Clock()
gameLoop()
pygame.quit()
