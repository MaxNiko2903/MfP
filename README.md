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
# Унитчтожение комических тел

```
import arcade
import random
import json

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Space Game"

class SpaceGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.spaceship = None
        self.comets = []
        self.rockets = []
        self.explosions = []
        self.bonuses = []
        self.score = 0
        self.energy = 5
        self.energy_recharge_time = 0
        self.lives = 3
        self.explosion_sound = arcade.load_sound(":resources:sounds/explosion1.wav")
        self.rocket_sound = arcade.load_sound(":resources:sounds/laser1.wav")
        self.bonus_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.high_scores = self.load_high_scores()

    def setup(self):
        self.spaceship = arcade.Sprite(":resources:images/space_shooter/playerShip1_orange.png", 0.5)
        self.spaceship.center_x = SCREEN_WIDTH // 2
        self.spaceship.center_y = 50
        self.comets = []
        self.rockets = []
        self.explosions = []
        self.bonuses = []
        self.score = 0
        self.energy = 5
        self.lives = 3

    def on_draw(self):
        arcade.start_render()
        self.spaceship.draw()
        for comet in self.comets:
            comet.draw()
        for rocket in self.rockets:
            rocket.draw()
        for explosion in self.explosions:
            explosion.draw()
        for bonus in self.bonuses:
            bonus.draw()
        arcade.draw_text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 14)
        arcade.draw_text(f"Energy: {self.energy}", 10, SCREEN_HEIGHT - 50, arcade.color.WHITE, 14)
        arcade.draw_text(f"Lives: {self.lives}", 10, SCREEN_HEIGHT - 70, arcade.color.WHITE, 14)
        self.draw_high_scores()

    def update(self, delta_time):
        self.spaceship.update()
        for comet in self.comets:
            comet.update()
        for rocket in self.rockets:
            rocket.update()
        for explosion in self.explosions:
            explosion.update()
        for bonus in self.bonuses:
            bonus.update()
        self.check_collisions()
        self.keep_on_screen()
        self.recharge_energy(delta_time)

    def check_collisions(self):
        for comet in self.comets:
            if arcade.check_for_collision(self.spaceship, comet):
                self.comets.remove(comet)
                self.create_explosion(comet.center_x, comet.center_y)
                arcade.play_sound(self.explosion_sound)
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over()
            for rocket in self.rockets:
                if arcade.check_for_collision(rocket, comet):
                    self.comets.remove(comet)
                    self.rockets.remove(rocket)
                    self.create_explosion(comet.center_x, comet.center_y)
                    arcade.play_sound(self.explosion_sound)
                    self.score += 1
        for bonus in self.bonuses:
            if arcade.check_for_collision(self.spaceship, bonus):
                self.bonuses.remove(bonus)
                arcade.play_sound(self.bonus_sound)
                self.energy = min(10, self.energy + 3)

    def create_explosion(self, x, y):
        explosion = arcade.Sprite(":resources:images/space_shooter/playerLife1_orange.png", 0.5)
        explosion.center_x = x
        explosion.center_y = y
        self.explosions.append(explosion)
        arcade.schedule(self.remove_explosion, 0.5)

    def remove_explosion(self, delta_time):
        if self.explosions:
            self.explosions.pop(0)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.spaceship.change_x = -5
        elif key == arcade.key.RIGHT:
            self.spaceship.change_x = 5
        elif key == arcade.key.UP:
            self.spaceship.change_y = 5
        elif key == arcade.key.DOWN:
            self.spaceship.change_y = -5
        elif key == arcade.key.SPACE and self.energy > 0:
            self.fire_rocket()
        elif key == arcade.key.R:
            self.recharge_energy_full()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.spaceship.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.spaceship.change_y = 0

    def fire_rocket(self):
        if self.energy > 0:
            rocket = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", 0.5)
            rocket.center_x = self.spaceship.center_x
            rocket.center_y = self.spaceship.center_y
            rocket.change_y = 10
            rocket.angle = 90  # Поворот на 90 градусов
            self.rockets.append(rocket)
            self.energy -= 1
            arcade.play_sound(self.rocket_sound)

    def add_comet(self, delta_time):
        comet_type = random.choice(["normal", "fast", "bonus"])
        if comet_type == "normal":
            comet = arcade.Sprite(":resources:images/space_shooter/meteorGrey_big1.png", 0.5)
            comet.change_y = -2
        elif comet_type == "fast":
            comet = arcade.Sprite(":resources:images/space_shooter/meteorGrey_med1.png", 0.5)
            comet.change_y = -3
        elif comet_type == "bonus":
            comet = arcade.Sprite(":resources:images/items/star.png", 0.5)
            comet.change_y = -2
            self.bonuses.append(comet)
        comet.center_x = random.randint(0, SCREEN_WIDTH)
        comet.center_y = SCREEN_HEIGHT
        self.comets.append(comet)

    def load_high_scores(self):
        try:
            with open("high_scores.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_high_scores(self):
        with open("high_scores.json", "w") as file:
            json.dump(self.high_scores, file)

    def draw_high_scores(self):
        y = SCREEN_HEIGHT - 100
        arcade.draw_text("High Scores:", 10, y, arcade.color.WHITE, 14)
        for score in self.high_scores:
            y -= 20
            arcade.draw_text(f"{score}", 10, y, arcade.color.WHITE, 14)

    def on_close(self):
        self.high_scores.append(self.score)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[:5]
        self.save_high_scores()
        super().on_close()

    def keep_on_screen(self):
        if self.spaceship.center_x < 0:
            self.spaceship.center_x = 0
        elif self.spaceship.center_x > SCREEN_WIDTH:
            self.spaceship.center_x = SCREEN_WIDTH
        if self.spaceship.center_y < 0:
            self.spaceship.center_y = 0
        elif self.spaceship.center_y > SCREEN_HEIGHT:
            self.spaceship.center_y = SCREEN_HEIGHT

    def recharge_energy(self, delta_time):
        self.energy_recharge_time += delta_time
        if self.energy_recharge_time >= 1.0:
            self.energy = min(5, self.energy + 1)
            self.energy_recharge_time = 0

    def recharge_energy_full(self):
        self.energy = 5

    def game_over(self):
        arcade.close_window()

def main():
    game = SpaceGame()
    game.setup()
    arcade.schedule(game.add_comet, 2.0)
    arcade.run()

if __name__ == "__main__":
    main()

```
![image](https://github.com/user-attachments/assets/495f663b-ca6d-4dba-976e-31ed6c51f51f)
![image](https://github.com/user-attachments/assets/9f278f5f-43e1-40d9-90aa-6a61c25f1642)
![image](https://github.com/user-attachments/assets/69c22acd-0e02-43ae-b333-6fe58eea03e8)

У нас есть система сохранений рекордов, система подсчёта очков, бонусы, разные типы космических тел и озвучка этого всего.

## Контакты

Если у вас есть вопросы или предложения, пожалуйста, свяжитесь со мной:

- **[Email](mailto:nikolaev.m.d2@edu.mirea.ru)** <img src="https://www.svgrepo.com/show/452213/gmail.svg" alt="Email Icon" width="20"/>
- **[GitHub](https://github.com/MaxNiko2903)** <img src="https://www.svgrepo.com/show/475654/github-color.svg" alt="GitHub Icon" width="20"/>
- **[VK](https://vk.com/maxniko2903)** <img src="https://www.svgrepo.com/show/349554/vk.svg" alt="VK Icon" width="20"/>
- **[Telegram](https://t.me/maxniko2903)** <img src="https://www.svgrepo.com/show/354443/telegram.svg" alt="Telegram Icon" width="20"/>

---

**Николаев Максим Дмитриевич**  
**Москва, Институт РТУ МИРЭА** 

