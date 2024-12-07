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
# Гонки

```
import arcade
import math
import random

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Гонка по кругу"
NUM_CARS = 5  # Количество машин
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2
RADIUS = 200  # Радиус круга
TOTAL_LAPS = 3  # Общее количество кругов для завершения гонки

class Car(arcade.Sprite):
    def __init__(self, filename, scale):
        super().__init__(filename, scale)
        self.angle = 0
        self.speed = random.uniform(1, 3)
        self.laps = 0
        self.center_x = CENTER_X + RADIUS * math.cos(math.radians(self.angle))
        self.center_y = CENTER_Y + RADIUS * math.sin(math.radians(self.angle))

    def update(self):
        self.angle += self.speed
        self.center_x = CENTER_X + RADIUS * math.cos(math.radians(self.angle))
        self.center_y = CENTER_Y + RADIUS * math.sin(math.radians(self.angle))
        if self.angle >= 360:
            self.angle -= 360
            self.laps += 1

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AMAZON)

        # Создаем машины
        self.cars = [Car(":resources:images/topdown_tanks/tankBody_blue_outline.png", 0.5) for _ in range(NUM_CARS)]
        self.leader = None

    def on_draw(self):
        """ Отрисовка экрана. """
        arcade.start_render()

        # Рисуем трассу
        arcade.draw_circle_outline(CENTER_X, CENTER_Y, RADIUS, arcade.color.GRAY, 5)

        # Рисуем машины
        for car in self.cars:
            car.draw()

        # Отображаем текущего лидера
        if self.leader:
            arcade.draw_text(f"Лидер: Персонаж {self.cars.index(self.leader) + 1}", 10, 10, arcade.color.WHITE, 14)

    def update(self, delta_time):
        """ Обновление игровой логики. """
        for car in self.cars:
            car.update()
            # Случайное изменение скорости и направления
            if random.random() < 0.1:
                car.speed = random.uniform(1, 3)

        # Определяем текущего лидера
        self.leader = max(self.cars, key=lambda c: c.laps)

        # Проверяем завершение гонки
        if all(car.laps >= TOTAL_LAPS for car in self.cars):
            self.end_game()

    def end_game(self):
        """ Завершение гонки и отображение результатов. """
        arcade.draw_text("Гонка завершена!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, arcade.color.WHITE, 24, anchor_x="center")
        for i, car in enumerate(sorted(self.cars, key=lambda c: c.laps, reverse=True)):
            arcade.draw_text(f"Место {i + 1}: Персонаж {self.cars.index(car) + 1}, Круги: {car.laps}", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30 * (i + 1), arcade.color.WHITE, 14, anchor_x="center")
        arcade.finish_render()
        arcade.pause(5)
        arcade.close_window()

def main():
    game = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()

```
![image](https://github.com/user-attachments/assets/5fd49833-9d97-4928-8be1-8fac50306c41)
![image](https://github.com/user-attachments/assets/ab0228a4-3e0e-402f-9935-d00fa60897bf)

## Контакты

Если у вас есть вопросы или предложения, пожалуйста, свяжитесь со мной:

- **[Email](mailto:nikolaev.m.d2@edu.mirea.ru)** <img src="https://www.svgrepo.com/show/452213/gmail.svg" alt="Email Icon" width="20"/>
- **[GitHub](https://github.com/MaxNiko2903)** <img src="https://www.svgrepo.com/show/475654/github-color.svg" alt="GitHub Icon" width="20"/>
- **[VK](https://vk.com/maxniko2903)** <img src="https://www.svgrepo.com/show/349554/vk.svg" alt="VK Icon" width="20"/>
- **[Telegram](https://t.me/maxniko2903)** <img src="https://www.svgrepo.com/show/354443/telegram.svg" alt="Telegram Icon" width="20"/>

---

**Николаев Максим Дмитриевич**  
**Москва, Институт РТУ МИРЭА** 

