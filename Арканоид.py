import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Основные параметры игры
WIDTH, HEIGHT = 800, 600
FPS = 60
BALL_SPEED = [5, 5]
PLATFORM_SPEED = 7
BALL_RADIUS = 10
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 10
MAX_BALL_SPEED = 5  # Ограничение на скорость мяча

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

# Цвета для блоков
block_colors = [RED, GREEN, YELLOW, PURPLE, CYAN]

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Арканоид")

# Шрифт для текста
font = pygame.font.Font(None, 74)  # Шрифт для больших надписей
font_small = pygame.font.Font(None, 36)  # Шрифт для инструкций

# Переменные состояния игры
game_active = False
ball_in_play = False
auto_play = False  # Переменная для режима автопилота
won = False  # Переменная для победы
show_instructions = False  # Показываем инструкции после выбора сложности
menu_active = True
difficulty = 3  # Количество жизней по умолчанию
lives = 3  # Текущее количество жизней
paused = False  # Состояние паузы
wait_for_space = False  # Флаг, указывающий, что нужно нажать пробел для продолжения после потери жизни

# Платформа
platform = pygame.Rect(WIDTH // 2 - PLATFORM_WIDTH // 2, HEIGHT - 30, PLATFORM_WIDTH, PLATFORM_HEIGHT)

# Мяч
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed = [random.choice([-5, 5]), random.choice([-5, 5])]

# Блоки (прямоугольники, которые нужно разрушить)
block_rows = 5
block_cols = 10
block_padding = 5  # Отступ между блоками
top_margin = 50  # Отступ от потолка

# Расчет ширины и высоты блоков
block_width = (WIDTH - (block_cols + 1) * block_padding) // block_cols
block_height = 20

blocks = []

# Определяем переменные для движения платформы
platform_move_left = False
platform_move_right = False

# Функция для создания блоков
def create_blocks():
    """Функция для создания блоков разных цветов с отступами."""
    blocks.clear()
    for row in range(block_rows):
        for col in range(block_cols):
            x = col * (block_width + block_padding) + block_padding
            y = row * (block_height + block_padding) + top_margin
            block = pygame.Rect(x, y, block_width, block_height)
            blocks.append((block, block_colors[row % len(block_colors)]))

# Основной игровой цикл
clock = pygame.time.Clock()

# Разрешаем только обработку событий, чтобы предотвратить зависания
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_SPACE:
                if menu_active:
                    if difficulty == 1:
                        lives = 1
                    elif difficulty == 3:
                        lives = 3
                    # Скрываем меню и показываем легенду
                    menu_active = False
                    show_instructions = True
                elif show_instructions:
                    # Скрываем легенду и запускаем игру
                    show_instructions = False
                    game_active = True
                    ball_in_play = True
                    ball.topleft = (WIDTH // 2, HEIGHT // 2)
                    ball_speed = [random.choice([-5, 5]), random.choice([-5, 5])]
                    platform = pygame.Rect(WIDTH // 2 - PLATFORM_WIDTH // 2, HEIGHT - 30, PLATFORM_WIDTH, PLATFORM_HEIGHT)
                    create_blocks()
                elif not game_active:
                    if won or lives <= 0:
                        # Переход в меню
                        menu_active = True
                        show_instructions = False
                        game_active = False
                        ball_in_play = False
                        blocks.clear()
                        won = False  # Сбрасываем статус победы
                    else:
                        # Перезапуск уровня
                        game_active = True
                        ball_in_play = True
                        won = False  # Сбрасываем статус победы
                        ball.topleft = (WIDTH // 2, HEIGHT // 2)
                        ball_speed = [random.choice([-5, 5]), random.choice([-5, 5])]
                        create_blocks()
            if event.key == pygame.K_p:
                paused = not paused  # Включение/выключение паузы
            if event.key == pygame.K_a:
                auto_play = not auto_play  # Включение/выключение режима автопилота
            if event.key == pygame.K_UP:
                if menu_active:
                    difficulty = 3 if difficulty == 1 else 1
            if event.key == pygame.K_DOWN:
                if menu_active:
                    difficulty = 1 if difficulty == 3 else 3
            if event.key == pygame.K_LEFT:
                platform_move_left = True
            if event.key == pygame.K_RIGHT:
                platform_move_right = True
            if event.key == pygame.K_SPACE and wait_for_space:
                # Возвращаем платформу в центр и продолжаем игру
                platform = pygame.Rect(WIDTH // 2 - PLATFORM_WIDTH // 2, HEIGHT - 30, PLATFORM_WIDTH, PLATFORM_HEIGHT)
                ball.topleft = (WIDTH // 2, HEIGHT // 2)
                ball_speed = [random.choice([-5, 5]), -random.randint(4, 6)]  # Мяч всегда летит вверх
                ball_in_play = True
                wait_for_space = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                platform_move_left = False
            if event.key == pygame.K_RIGHT:
                platform_move_right = False

    # Игровая логика только если игра активна
    if game_active and not paused:
        # Движение платформы
        if not auto_play:
            if platform_move_left and platform.left > 0:
                platform.move_ip(-PLATFORM_SPEED, 0)
            if platform_move_right and platform.right < WIDTH:
                platform.move_ip(PLATFORM_SPEED, 0)

        # Если режим автопилота включён
        if auto_play:
            if ball.centerx < platform.centerx and platform.left > 0:
                platform.move_ip(-PLATFORM_SPEED, 0)
            elif ball.centerx > platform.centerx and platform.right < WIDTH:
                platform.move_ip(PLATFORM_SPEED, 0)

        if ball_in_play:
            # Движение мяча
            ball.move_ip(ball_speed)

            # Столкновение мяча со стенами
            if ball.left <= 0 or ball.right >= WIDTH:
                ball_speed[0] = -ball_speed[0]
            if ball.top <= 0:
                ball_speed[1] = -ball_speed[1]

            # Столкновение мяча с платформой
            if ball.colliderect(platform) and ball_speed[1] > 0:
                platform_velocity = 0
                if platform_move_left:
                    platform_velocity = -PLATFORM_SPEED
                elif platform_move_right:
                    platform_velocity = PLATFORM_SPEED

                # Уменьшаем влияние инерции на мяч
                ball_speed[0] += platform_velocity // 4  # Уменьшаем влияние скорости платформы на мяч

                # Ограничение на максимальную скорость мяча
                if abs(ball_speed[0]) > MAX_BALL_SPEED:
                    ball_speed[0] = MAX_BALL_SPEED if ball_speed[0] > 0 else -MAX_BALL_SPEED

                ball_speed[1] = -ball_speed[1]  # Отскакивание мяча от платформы


            # Столкновение мяча с блоками
            hit_block = ball.collidelist([block[0] for block in blocks])
            if hit_block != -1:
                block = blocks.pop(hit_block)
                ball_speed[1] = -ball_speed[1]

            # Проверка на победу
            if not blocks:  # Если все блоки уничтожены
                won = True
                game_active = False
                ball_in_play = False

            # Мяч выходит за нижний край экрана
            if ball.bottom >= HEIGHT:
                lives -= 1
                ball_in_play = False
                wait_for_space = True
                if lives <= 0:
                    game_active = False  # Конец игры

    # Рисование экрана
    screen.fill(BLACK)

    
    if menu_active:
        # Отображаем заголовок меню
        text = font.render("Выбери количество жизней", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4))

        # Параметры для меню
        option_1_text = font_small.render("1 Жизнь", True, WHITE)
        option_3_text = font_small.render("3 Жизни", True, WHITE)

        # Определение положения каждого пункта
        option_1_pos = (WIDTH // 2 - option_1_text.get_width() // 2, HEIGHT // 2 - 50)
        option_3_pos = (WIDTH // 2 - option_3_text.get_width() // 2, HEIGHT // 2)

        # Отображение пунктов меню
        screen.blit(option_1_text, option_1_pos)
        screen.blit(option_3_text, option_3_pos)

        # Обводка активного пункта
        if difficulty == 1:
            pygame.draw.rect(screen, WHITE, pygame.Rect(option_1_pos[0] - 10, option_1_pos[1] - 10, option_1_text.get_width() + 20, option_1_text.get_height() + 20), 3)
        elif difficulty == 3:
            pygame.draw.rect(screen, WHITE, pygame.Rect(option_3_pos[0] - 10, option_3_pos[1] - 10, option_3_text.get_width() + 20, option_3_text.get_height() + 20), 3)


    elif show_instructions:
        # Рисуем инструкции
        instructions = [
            "Используй стрелки для управления платформой.",
            "Нажми P для паузы.",
            "Нажми ESC для выхода.",
            "Нажми ПРОБЕЛ для начала игры."
        ]
        for i, instruction in enumerate(instructions):
            text = font_small.render(instruction, True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100 + i * 40))

    elif game_active:
        # Рисуем блоки
        for block, color in blocks:
            pygame.draw.rect(screen, color, block)

        # Рисуем платформу и мяч
        pygame.draw.rect(screen, BLUE, platform)
        pygame.draw.ellipse(screen, WHITE, ball)

        # Рисуем жизни (в виде кругов)
        for i in range(lives):
            pygame.draw.circle(screen, RED, (30 + i * 40, 20), 15)

        if paused:
            text = font.render("ПАУЗА", True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))

    elif won:
        # Отображаем надпись "ПОБЕДА"
        text = font.render("ПОБЕДА!", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))

    else:
        # Если игра окончена
        text = font.render("ИГРА ОКОНЧЕНА", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))

    pygame.display.flip()

    # Ограничиваем частоту кадров
    clock.tick(FPS)
