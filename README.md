<p align="center">
  <img src="https://www.mirea.ru/upload/medialibrary/c1a/MIREA_Gerb_Colour.jpg" alt="MIREA" width="80"/>
  <img src="https://www.mirea.ru/upload/medialibrary/26c/FTI_colour.jpg" alt="IPTIP" width="137"/> 
</p>

# MfP
## Математика для программирования (часть 1/2) [I.24-25]
---

**Студент:**  
**Николаев Максим Дмитриевич**  

**Место обучения:**  
**Москва, Институт РТУ МИРЭА**  
**Факультет ИПТИП**  
**Кафедра Индустриального програмирования**  

**Направление:**  
**Фулстек разработка**  

**Группа:**  
**ЭФБО-07-22**  

**Шифр:**  
**22Т0111**  

**Преподаватель:**  
**Клёсов Дмитрий Николаевич**  

**Семестр:**  
**5 семестр, 2024-2025 гг.**

---

## Описание проекта

Этот репозиторий посвящён дисциплине "Математика для программирования". В данном проекте рассматриваются различные аспекты разработки приложений и игр с использованием математике.

## Практические задания
# Лабиринт
**Случайноая генерация лабиринта и пояления врагов, показывание кратчайшего пути и вывод рузультатов**
```
import pygame
import random
import heapq
import time

# Константы
WIDTH, HEIGHT = 21, 21  # Размеры лабиринта
CELL_SIZE = 30  # Размер клетки в пикселях
WINDOW_WIDTH = WIDTH * CELL_SIZE
WINDOW_HEIGHT = HEIGHT * CELL_SIZE

# Цвета
COLOR_WALL = (0, 0, 0)
COLOR_PATH = (200, 200, 200)
COLOR_PLAYER = (0, 0, 255)
COLOR_EXIT = (0, 255, 0)
COLOR_ENEMY = (255, 0, 0)
COLOR_HINT = (255, 255, 0)

# Символы
WALL = 0
PATH = 1

# Генерация пустого лабиринта
def create_empty_maze(width, height):
    return [[WALL for _ in range(width)] for _ in range(height)]

# Генерация лабиринта (DFS)
def generate_maze(maze, start_x, start_y):
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    random.shuffle(directions)
    maze[start_y][start_x] = PATH

    for dx, dy in directions:
        nx, ny = start_x + dx, start_y + dy
        if 0 < nx < WIDTH - 1 and 0 < ny < HEIGHT - 1 and maze[ny][nx] == WALL:
            maze[start_y + dy // 2][start_x + dx // 2] = PATH
            generate_maze(maze, nx, ny)

# A* поиск пути
def a_star(maze, start, goal):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < WIDTH and 0 <= neighbor[1] < HEIGHT and maze[neighbor[1]][neighbor[0]] == PATH:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []

def move_player(player_pos, direction, maze):
    px, py = player_pos
    if direction == 'up' and py > 0 and maze[py - 1][px] == PATH:
        return (px, py - 1)
    elif direction == 'down' and py < HEIGHT - 1 and maze[py + 1][px] == PATH:
        return (px, py + 1)
    elif direction == 'left' and px > 0 and maze[py][px - 1] == PATH:
        return (px - 1, py)
    elif direction == 'right' and px < WIDTH - 1 and maze[py][px + 1] == PATH:
        return (px + 1, py)
    return player_pos  # Если движение невозможно, остаёмся на месте


# Проверка, не блокируют ли враги путь
def validate_enemy_positions(enemies, maze, player_pos, exit_pos):
    path = a_star(maze, player_pos, exit_pos)
    if not path:
        return enemies  # Если пути нет, оставить как есть
    valid_positions = set(path)  # Клетки, на которых враги не должны находиться
    new_enemies = []
    for ex, ey in enemies:
        if (ex, ey) in valid_positions:
            # Найдём свободное место
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = ex + dx, ey + dy
                if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and maze[ny][nx] == PATH and (nx, ny) not in valid_positions:
                    new_enemies.append((nx, ny))
                    break
        else:
            new_enemies.append((ex, ey))
    return new_enemies

# Движение врагов
def move_enemies(enemies, maze, player_pos, exit_pos):
    enemies = validate_enemy_positions(enemies, maze, player_pos, exit_pos)
    new_enemies = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for ex, ey in enemies:
        dx, dy = random.choice(directions)
        nx, ny = ex + dx, ey + dy
        if 0 < nx < WIDTH - 1 and 0 < ny < HEIGHT - 1 and maze[ny][nx] == PATH and (nx, ny) != exit_pos:
            new_enemies.append((nx, ny))
        else:
            new_enemies.append((ex, ey))
    return new_enemies

def draw_maze(screen, maze, player_pos, exit_pos, enemies, path_to_exit=None):
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            color = COLOR_WALL if maze[y][x] == WALL else COLOR_PATH
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Отрисовка кратчайшего пути (если включён)
    if path_to_exit:
        for px, py in path_to_exit:
            pygame.draw.rect(screen, COLOR_HINT, (px * CELL_SIZE, py * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Отрисовка выхода
    ex, ey = exit_pos
    pygame.draw.rect(screen, COLOR_EXIT, (ex * CELL_SIZE, ey * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Отрисовка игрока
    px, py = player_pos
    pygame.draw.rect(screen, COLOR_PLAYER, (px * CELL_SIZE, py * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Отрисовка врагов
    for ex, ey in enemies:
        pygame.draw.rect(screen, COLOR_ENEMY, (ex * CELL_SIZE, ey * CELL_SIZE, CELL_SIZE, CELL_SIZE))


# Инициализация
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Лабиринт с врагами и анализом")
clock = pygame.time.Clock()

maze = create_empty_maze(WIDTH, HEIGHT)
generate_maze(maze, 1, 1)
player_pos = (1, 1)
exit_pos = (WIDTH - 2, HEIGHT - 2)
enemies = [(3, 3), (WIDTH - 4, HEIGHT - 4)]  # Враги на старте
steps = 0
start_time = time.time()
path_to_exit = []

# Основной игровой цикл
running = True
show_path = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_pos = move_player(player_pos, 'up', maze)
        steps += 1
    if keys[pygame.K_DOWN]:
        player_pos = move_player(player_pos, 'down', maze)
        steps += 1
    if keys[pygame.K_LEFT]:
        player_pos = move_player(player_pos, 'left', maze)
        steps += 1
    if keys[pygame.K_RIGHT]:
        player_pos = move_player(player_pos, 'right', maze)
        steps += 1
    if keys[pygame.K_m]:
        path_to_exit = a_star(maze, player_pos, exit_pos)
        show_path = True

    # Движение врагов
    enemies = move_enemies(enemies, maze, player_pos, exit_pos)

    # Проверка на столкновение с врагами
    if player_pos in enemies:
        print("Вы проиграли! Столкновение с врагом.")
        running = False

    # Проверка на выход
    if player_pos == exit_pos:
        end_time = time.time()
        print("Вы нашли выход!")
        optimal_path = a_star(maze, (1, 1), exit_pos)
        print(f"Эффективность:")
        print(f"- Оптимальный путь: {len(optimal_path)} шагов.")
        print(f"- Ваш путь: {steps} шагов.")
        print(f"- Время прохождения: {end_time - start_time:.2f} секунд.")
        running = False

    # Отрисовка
    screen.fill(COLOR_WALL)
    draw_maze(screen, maze, player_pos, exit_pos, enemies, path_to_exit if show_path else None)
    pygame.display.flip()
    clock.tick(10)

pygame.quit()

```

![image](https://github.com/user-attachments/assets/b1bf7a78-2382-4499-b244-190b6685a876)
![image](https://github.com/user-attachments/assets/514f3f64-e6e1-46c1-8304-4c33b7701284)
![image](https://github.com/user-attachments/assets/a91d8a09-4b86-4cf7-a810-bc56a47aeb2d)
![image](https://github.com/user-attachments/assets/f8b3ed05-94c5-4ec6-9405-a40250a1dca6)
![image](https://github.com/user-attachments/assets/71080fe2-645f-4240-a912-ffdb164e0cd9)

**Редактор**
```
import pygame
import random
import heapq
import time

# Константы
WIDTH, HEIGHT = 21, 21  # Размеры лабиринта
CELL_SIZE = 30  # Размер клетки в пикселях
WINDOW_WIDTH = WIDTH * CELL_SIZE
WINDOW_HEIGHT = HEIGHT * CELL_SIZE

# Цвета
COLOR_WALL = (0, 0, 0)
COLOR_PATH = (200, 200, 200)
COLOR_PLAYER = (0, 0, 255)
COLOR_EXIT = (0, 255, 0)
COLOR_ENEMY = (255, 0, 0)
COLOR_HINT = (255, 255, 0)

# Символы
WALL = 0
PATH = 1
PLAYER = 2
EXIT = 3
ENEMY = 4

# Генерация пустого лабиринта
def create_empty_maze(width, height):
    return [[WALL for _ in range(width)] for _ in range(height)]

# Генерация лабиринта (DFS)
def generate_maze(maze, start_x, start_y):
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    random.shuffle(directions)
    maze[start_y][start_x] = PATH

    for dx, dy in directions:
        nx, ny = start_x + dx, start_y + dy
        if 0 < nx < WIDTH - 1 and 0 < ny < HEIGHT - 1 and maze[ny][nx] == WALL:
            maze[start_y + dy // 2][start_x + dx // 2] = PATH
            generate_maze(maze, nx, ny)

# A* поиск пути
def a_star(maze, start, goal):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < WIDTH and 0 <= neighbor[1] < HEIGHT and maze[neighbor[1]][neighbor[0]] == PATH:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []

def move_player(player_pos, direction, maze):
    px, py = player_pos
    if direction == 'up' and py > 0 and maze[py - 1][px] == PATH:
        return (px, py - 1)
    elif direction == 'down' and py < HEIGHT - 1 and maze[py + 1][px] == PATH:
        return (px, py + 1)
    elif direction == 'left' and px > 0 and maze[py][px - 1] == PATH:
        return (px - 1, py)
    elif direction == 'right' and px < WIDTH - 1 and maze[py][px + 1] == PATH:
        return (px + 1, py)
    return player_pos

# Проверка на столкновение с врагами и обновление их позиций остается без изменений...

def draw_maze(screen, maze, player_pos, exit_pos, enemies):
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            color = COLOR_WALL if maze[y][x] == WALL else COLOR_PATH
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Отрисовка выхода
    ex, ey = exit_pos
    pygame.draw.rect(screen, COLOR_EXIT, (ex * CELL_SIZE, ey * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Отрисовка игрока
    px, py = player_pos
    pygame.draw.rect(screen, COLOR_PLAYER, (px * CELL_SIZE, py * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Отрисовка врагов
    for ex, ey in enemies:
        pygame.draw.rect(screen, COLOR_ENEMY, (ex * CELL_SIZE, ey * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Функция для отображения карты в текстовом виде для редактирования
def display_map(maze):
    map_representation = ""
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if (x,y) == player_pos:
                map_representation += f"{PLAYER} "
            elif (x,y) == exit_pos:
                map_representation += f"{EXIT} "
            elif (x,y) in enemies:
                map_representation += f"{ENEMY} "
            else:
                map_representation += f"{maze[y][x]} "
        map_representation += "\n"
    print(map_representation)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Лабиринт с врагами и анализом")
clock = pygame.time.Clock()

maze = create_empty_maze(WIDTH, HEIGHT)
generate_maze(maze, 1, 1)
player_pos = (1, 1)
exit_pos = (WIDTH - 2 , HEIGHT -2 )
enemies = [(3 ,3) ,(WIDTH -4 , HEIGHT -4)]  
steps=0 
start_time= time.time()
path_to_exit=[] 
editing_mode= False

# Основной игровой цикл
running=True 
show_path=False 
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False 

    # Управление игроком и редактирование карты
    keys=pygame.key.get_pressed()
    
    if editing_mode: 
        if keys[pygame.K_UP]:
            player_pos=(player_pos[0], max(player_pos[1]-1 ,0))
        elif keys[pygame.K_DOWN]:
            player_pos=(player_pos[0], min(player_pos[1]+1 ,HEIGHT-1))
        elif keys[pygame.K_LEFT]:
            player_pos=(max(player_pos[0]-1 ,0), player_pos[1])
        elif keys[pygame.K_RIGHT]:
            player_pos=(min(player_pos[0]+1 ,WIDTH-1), player_pos[1])
        
        # Изменение ячейки по нажатию клавиш от '0' до '4'
        for i in range(5):
            if keys[getattr(pygame ,f"K_{i}")]: 
                x_cell ,y_cell=player_pos 
                maze[y_cell][x_cell]=i 

        # Выход из режима редактирования при повторном нажатии 'r'
        if keys[pygame.K_r]:
            editing_mode=False 
            
    else: 
        if keys[pygame.K_UP]:
            player_pos=move_player(player_pos ,'up' ,maze) 
            steps+=1 
        if keys[pygame.K_DOWN]:
            player_pos=move_player(player_pos ,'down' ,maze) 
            steps+=1 
        if keys[pygame.K_LEFT]:
            player_pos=move_player(player_pos ,'left' ,maze) 
            steps+=1 
        if keys[pygame.K_RIGHT]:
            player_pos=move_player(player_pos ,'right' ,maze) 
            steps+=1 

        # Вход в режим редактирования карты при нажатии 'r'
        if keys[pygame.K_r]: 
            editing_mode=True 
            display_map(maze) 

    
    # Проверка на столкновение с врагами и выход остаются без изменений...

    
    # Отрисовка карты и объектов на ней
    screen.fill(COLOR_WALL) 
    draw_maze(screen ,maze ,player_pos ,exit_pos ,enemies) 
    pygame.display.flip() 
    clock.tick(10)

pygame.quit()
```

![image](https://github.com/user-attachments/assets/0095b2c6-9bf7-4b66-b3be-750ae445bad2)
![image](https://github.com/user-attachments/assets/51c0bc15-8ed5-4041-b046-5fe92b2780d3)
![image](https://github.com/user-attachments/assets/0906f6dd-85af-4a61-8b22-d0a1d830b261)
![image](https://github.com/user-attachments/assets/d62477a6-96e5-43a6-9d08-15277cb46d77)



## Контакты

Если у вас есть вопросы или предложения, пожалуйста, свяжитесь со мной:

- **[Email](mailto:nikolaev.m.d2@edu.mirea.ru)** <img src="https://www.svgrepo.com/show/452213/gmail.svg" alt="Email Icon" width="20"/>
- **[GitHub](https://github.com/MaxNiko2903)** <img src="https://www.svgrepo.com/show/475654/github-color.svg" alt="GitHub Icon" width="20"/>
- **[VK](https://vk.com/maxniko2903)** <img src="https://www.svgrepo.com/show/349554/vk.svg" alt="VK Icon" width="20"/>
- **[Telegram](https://t.me/maxniko2903)** <img src="https://www.svgrepo.com/show/354443/telegram.svg" alt="Telegram Icon" width="20"/>

---

**Николаев Максим Дмитриевич**  
**Москва, Институт РТУ МИРЭА** 

