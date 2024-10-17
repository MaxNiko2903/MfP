import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
CELL_SIZE = 40
GRID_SIZE = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREY = (192, 192, 192)  # Цвет для промаха
GREEN = (0, 255, 0)     # Цвет для попадания
GAP_BETWEEN_GRIDS = 50  # Расстояние между двумя полями

# Экран
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Морской бой")

# Типы кораблей
ships_config = [
    ("battleship", 4),  
    ("cruiser", 3),     
    ("cruiser", 3),
    ("destroyer", 2),   
    ("destroyer", 2),
    ("destroyer", 2),
    ("boat", 1),        
    ("boat", 1),
    ("boat", 1),
    ("boat", 1)
]

# Ориентация корабля
HORIZONTAL = 0
VERTICAL = 1

# Класс для корабля
class Ship:
    def __init__(self, length):
        self.length = length
        self.orientation = HORIZONTAL
        self.placed = False
        self.cells = []
        self.hits = 0

    def rotate(self):
        """Вращаем корабль."""
        self.orientation = VERTICAL if self.orientation == HORIZONTAL else HORIZONTAL

    def is_sunk(self):
        """Проверяем, потоплен ли корабль."""
        return self.hits == self.length

# Класс для игрока
class Player:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.ships = []
        self.attacks = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.ship_cells = set()

    def place_ship(self, x, y, ship):
        """Пытаемся установить корабль на поле с проверкой границ."""
        if self.can_place_ship(x, y, ship):
            for i in range(ship.length):
                if ship.orientation == HORIZONTAL:
                    self.grid[y][x + i] = 1
                    ship.cells.append((x + i, y))
                    self.ship_cells.add((x + i, y))
                else:
                    self.grid[y + i][x] = 1
                    ship.cells.append((x, y + i))
                    self.ship_cells.add((x, y + i))
            ship.placed = True
            return True
        return False

    def can_place_ship(self, x, y, ship):
        """Проверка возможности установки корабля с учетом границ и расстояния между кораблями."""
        for i in range(ship.length):
            try:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if ship.orientation == HORIZONTAL:
                            nx, ny = x + i + dx, y + dy
                        else:
                            nx, ny = x + dx, y + i + dy

                        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                            if self.grid[ny][nx] != 0:  
                                return False

                if ship.orientation == HORIZONTAL:
                    if x + i >= GRID_SIZE or self.grid[y][x + i] != 0:
                        return False
                else:
                    if y + i >= GRID_SIZE or self.grid[y + i][x] != 0:
                        return False
            except IndexError:
                return False
        return True

    def receive_attack(self, x, y):
        """Обрабатываем атаку на поле игрока."""
        if (x, y) in self.ship_cells:  
            self.attacks[y][x] = 2  
            for ship in self.ships:
                if (x, y) in ship.cells:
                    ship.hits += 1
                    if ship.is_sunk():
                        print("Корабль потоплен!")
            return True
        else:
            self.attacks[y][x] = 1  
            return False

def draw_grid(offset_x):
    """Рисуем поле игрока."""
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(offset_x + x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)

def draw_labels():
    """Рисуем буквы и цифры для сетки."""
    font = pygame.font.SysFont(None, 24)

    # Рисуем буквы A-J
    for i in range(GRID_SIZE):
        letter = chr(65 + i)  # A = 65 в ASCII
        text_surface = font.render(letter, True, BLACK)
        screen.blit(text_surface, (CELL_SIZE + i * CELL_SIZE + (CELL_SIZE // 2) - 10, 0))  # Центрируем по X

    # Рисуем цифры 1-10
    for i in range(GRID_SIZE):
        number = str(i + 1)
        text_surface = font.render(number, True, BLACK)
        screen.blit(text_surface, (0, CELL_SIZE + i * CELL_SIZE + (CELL_SIZE // 2) - 10))  # Центрируем по Y


def draw_ships(player, offset_x, highlight_ship=None):
    """Рисуем все корабли игрока, с выделением каждой повреждённой клетки."""
    for ship in player.ships:
        if ship.placed:  # Рисуем только установленные корабли
            for cell in ship.cells:
                rect = pygame.Rect(offset_x + cell[0] * CELL_SIZE,
                                   cell[1] * CELL_SIZE,
                                   CELL_SIZE,
                                   CELL_SIZE)
                
                # Проверяем, попали ли в эту клетку корабля
                if player.attacks[cell[1]][cell[0]] == 2:  # Если клетка атакована
                    pygame.draw.rect(screen, RED, rect)  # Выделяем клетку красным цветом
                else:
                    pygame.draw.rect(screen, BLUE, rect)  # Неатакованная клетка остается синей

    # Визуализация текущего корабля при установке (если он еще не установлен)
    if highlight_ship and not highlight_ship.placed:  
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x = mouse_x // CELL_SIZE
        grid_y = mouse_y // CELL_SIZE
        
        # Ограничиваем возможность установки в поле противника
        if offset_x == 0:  # Поле первого игрока
            for i in range(highlight_ship.length):
                if highlight_ship.orientation == HORIZONTAL:
                    if 0 <= grid_x + i < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                        rect = pygame.Rect(offset_x + (grid_x + i) * CELL_SIZE,
                                           grid_y * CELL_SIZE,
                                           CELL_SIZE,
                                           CELL_SIZE)
                    else:
                        continue
                else:
                    if 0 <= grid_x < GRID_SIZE and 0 <= grid_y + i < GRID_SIZE:
                        rect = pygame.Rect(offset_x + grid_x * CELL_SIZE,
                                           (grid_y + i) * CELL_SIZE,
                                           CELL_SIZE,
                                           CELL_SIZE)
                    else:
                        continue
                
                pygame.draw.rect(screen, RED, rect)


def draw_attacks(player, offset_x):
    """Рисуем результаты атак."""
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if player.attacks[y][x] == 1:  
                rect = pygame.Rect(offset_x + x * CELL_SIZE,
                                   y * CELL_SIZE,
                                   CELL_SIZE,
                                   CELL_SIZE)
                pygame.draw.rect(screen, GREY, rect)
            elif player.attacks[y][x] == 2:  
                rect = pygame.Rect(offset_x + x * CELL_SIZE,
                                   y * CELL_SIZE,
                                   CELL_SIZE,
                                   CELL_SIZE)
                pygame.draw.rect(screen, GREEN, rect)

# Основная функция игры
def main():
    clock = pygame.time.Clock()

    # Игроки
    player1 = Player()
    player2 = Player()

    # Добавляем корабли игрокам
    for ship_type, length in ships_config:
        player1.ships.append(Ship(length))
        player2.ships.append(Ship(length))

    current_player = player1
    opponent = player2
    current_ship_index = 0  
    placing = True

    # Этап расстановки кораблей для первого игрока
    while current_player == player1:
        screen.fill(WHITE)

        # Обрабатываем события
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Нажатие клавиши для вращения корабля
            if event.type == pygame.KEYDOWN and current_ship_index < len(current_player.ships):
                if event.key == pygame.K_r:  
                    current_player.ships[current_ship_index].rotate()

            # Нажатие мыши для установки корабля
            if event.type == pygame.MOUSEBUTTONDOWN and current_ship_index < len(current_player.ships):
                if event.button == 1:  
                    mouse_x, mouse_y = event.pos
                    grid_x = mouse_x // CELL_SIZE
                    grid_y = mouse_y // CELL_SIZE

                    if (0 <= grid_x < GRID_SIZE) and (0 <= grid_y < GRID_SIZE):
                        ship = current_player.ships[current_ship_index]
                        if current_player.place_ship(grid_x, grid_y, ship):
                            current_ship_index += 1 
                            # Если все корабли расставлены у первого игрока 
                            if current_ship_index >= len(current_player.ships): 
                                current_player = player2
                                current_ship_index = 0  

        # Рисуем поле первого игрока
        draw_grid(0)
        draw_ships(player1, 0, current_player.ships[current_ship_index] if current_ship_index < len(player1.ships) else None)

        # Рисуем пустое поле для второго игрока
        draw_grid(GRID_SIZE * CELL_SIZE + GAP_BETWEEN_GRIDS) 

        pygame.display.flip()
        clock.tick(60)

    # Этап расстановки кораблей для второго игрока
    current_player = player2
    current_ship_index = 0  

    while current_player == player2:
        screen.fill(WHITE)

        # Обрабатываем события
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Нажатие клавиши для вращения корабля
            if event.type == pygame.KEYDOWN and current_ship_index < len(current_player.ships):
                if event.key == pygame.K_r:  
                    current_player.ships[current_ship_index].rotate()

            # Нажатие мыши для установки корабля
            if event.type == pygame.MOUSEBUTTONDOWN and current_ship_index < len(current_player.ships):
                if event.button == 1:  
                    mouse_x, mouse_y = event.pos
                    grid_x = mouse_x // CELL_SIZE
                    grid_y = mouse_y // CELL_SIZE

                    if (0 <= grid_x < GRID_SIZE) and (0 <= grid_y < GRID_SIZE):
                        ship = current_player.ships[current_ship_index]
                        if current_player.place_ship(grid_x, grid_y, ship):
                            current_ship_index += 1  
                            # Если все корабли расставлены у второго игрока
                            if current_ship_index >= len(current_player.ships): 
                                current_player = player1
                                current_ship_index = 0  

        # Рисуем поле второго игрока, но корабли не отображаются
        draw_grid(0)  # Поле игрока (всегда показываем)
        draw_ships(player2, 0, current_player.ships[current_ship_index] if current_ship_index < len(player2.ships) else None)

        # Рисуем пустое поле для первого игрока
        draw_grid(GRID_SIZE * CELL_SIZE + GAP_BETWEEN_GRIDS) 

        pygame.display.flip()
        clock.tick(60)

    # Этап атаки
    current_player = player1
    opponent = player2
    hit_streak = False  # Флаг, показывающий, что текущий игрок делает несколько ходов подряд

    while True:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    mouse_x, mouse_y = event.pos
                    grid_x = (mouse_x - (GRID_SIZE * CELL_SIZE + GAP_BETWEEN_GRIDS)) // CELL_SIZE
                    grid_y = mouse_y // CELL_SIZE

                    if (0 <= grid_x < GRID_SIZE) and (0 <= grid_y < GRID_SIZE):
                        hit = opponent.receive_attack(grid_x, grid_y)
                        
                        if hit:
                            print("Попадание!")
                            add_chat_message("Попадание!")
                            hit_streak = True

                            # Проверяем, потоплены ли все корабли противника
                            if all_ships_sunk(opponent):
                                add_chat_message("Все корабли противника потоплены! Победа игрока!")
                                pygame.quit()
                                sys.exit()

                        else:
                            print("Промах!")
                            add_chat_message("Промах!")
                            hit_streak = False

                        # Меняем текущего игрока только если промах
                        if not hit_streak:
                            current_player, opponent = opponent, current_player

        # Рисуем поле игрока и противника
        draw_grid(0)
        draw_grid(GRID_SIZE * CELL_SIZE + GAP_BETWEEN_GRIDS)
        draw_ships(current_player, 0)
        draw_attacks(opponent, GRID_SIZE * CELL_SIZE + GAP_BETWEEN_GRIDS)

        # Отображаем чат с сообщениями
        #draw_chat()

        pygame.display.flip()
        clock.tick(60)

# Добавляем список для хранения сообщений чата
chat_messages = []

def add_chat_message(message):
    """Добавляет сообщение в чат."""
    chat_messages.append(message)
    if len(chat_messages) > 10:  # Ограничиваем количество сообщений на экране
        chat_messages.pop(0)

def draw_chat():
    """Отображаем чат на экране."""
    font = pygame.font.SysFont(None, 24)
    chat_x = GRID_SIZE * CELL_SIZE + GAP_BETWEEN_GRIDS + 20  # Позиция для чата справа от полей
    chat_y = 20

    for message in chat_messages:
        text_surface = font.render(message, True, BLACK)
        screen.blit(text_surface, (chat_x, chat_y))
        chat_y += 30  # Отступ между строками чата

# Модифицируем receive_attack для отображения сообщения о попадании и потоплении
def receive_attack(self, x, y):
    """Обрабатываем атаку на поле игрока."""
    if (x, y) in self.ship_cells:  
        self.attacks[y][x] = 2  
        for ship in self.ships:
            if (x, y) in ship.cells:
                ship.hits += 1
                if ship.is_sunk():
                    add_chat_message("Корабль потоплен!")
                else:
                    add_chat_message("Корабль подбит!")
        return True
    else:
        self.attacks[y][x] = 1  
        return False

    # Функция для проверки, потоплены ли все корабли игрока
def all_ships_sunk(player):
    """Проверяем, потоплены ли все корабли игрока."""
    return all(ship.is_sunk() for ship in player.ships)

if __name__ == "__main__":
    main()
