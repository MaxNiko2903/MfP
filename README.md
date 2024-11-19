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

**Импорт библиотек**
```
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx
from PIL import Image
```
**Задача 1 - Напишите программу, которая создает графическую визуализацию спирали с использованием массивов для хранения координат точек на спирали.**
```
# Количество точек для спиралей
num_points = 1000

# Логарифмическая спираль
theta_log = np.linspace(0, 4 * np.pi, num_points)
r_log = np.exp(0.2 * theta_log)  # Радиус увеличивается экспоненциально
x_log = r_log * np.cos(theta_log)
y_log = r_log * np.sin(theta_log)

# Спираль Архимеда
theta_arch = np.linspace(0, 6 * np.pi, num_points)
r_arch = 0.1 * theta_arch  # Радиус линейно зависит от угла
x_arch = r_arch * np.cos(theta_arch)
y_arch = r_arch * np.sin(theta_arch)

# Спираль Ферма
theta_fermat = np.linspace(0, 6 * np.pi, num_points)
r_fermat = np.sqrt(theta_fermat)  # Радиус увеличивается как квадратный корень
x_fermat = r_fermat * np.cos(theta_fermat)
y_fermat = r_fermat * np.sin(theta_fermat)

# Визуализация
fig, axs = plt.subplots(1, 3, figsize=(18, 6))

# Логарифмическая спираль
axs[0].plot(x_log, y_log, color="blue")
axs[0].set_title("Логарифмическая спираль")
axs[0].set_aspect('equal')

# Спираль Архимеда
axs[1].plot(x_arch, y_arch, color="green")
axs[1].set_title("Спираль Архимеда")
axs[1].set_aspect('equal')

# Спираль Ферма
axs[2].plot(x_fermat, y_fermat, color="red")
axs[2].set_title("Спираль Ферма")
axs[2].set_aspect('equal')

plt.tight_layout()
plt.show()
```
![Спирали](https://github.com/user-attachments/assets/4c454fb0-4603-4070-83a1-57b57ea90b39)
**Задача 2 - Дан массив с количеством проданных товаров по категориям. Необходимо построить круговую диаграмму, визуализирующую процентное соотношение продаж для каждой категории.**
```
categories = ['Категория 1', 'Категория 2', 'Категория 3', 'Категория 4']
sales = np.array([150, 300, 200, 50])

# Построение круговой диаграммы
plt.figure(figsize=(7, 7))
plt.pie(sales, labels=categories, autopct='%1.1f%%', startangle=140)
plt.title("Процентное соотношение продаж по категориям")
plt.show()
```
![Диаграмма](https://github.com/user-attachments/assets/83d718f2-5630-4df5-b810-4412484d973c)
**Задача 3 - Напишите программу, которая создает мозаичное изображение на основе двумерного массива, где каждый элемент массива задает цвет ячейки мозаики.**
```
# Генерация двумерного массива цветов
rows, cols = 10, 10
mosaic = np.random.randint(0, 256, size=(rows, cols, 3))  # Каждый элемент - цвет в RGB

# Визуализация мозаики
plt.figure(figsize=(6, 6))
plt.imshow(mosaic)
plt.title("Мозаичное изображение")
plt.axis('off')
plt.show()

```
![Мозаика](https://github.com/user-attachments/assets/d877cc5a-80dc-4095-b074-b71f9cf37984)
**Задача 4 - Сгенерируйте и визуализируйте фрактал Мандельброта, используя массивы для хранения значений каждого пикселя и отображая его на графике.**
```
# Настройки
x = np.linspace(-2, 1, 1000)
y = np.linspace(-1.5, 1.5, 1000)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y
c = Z.copy()
mandelbrot_set = np.zeros(Z.shape, dtype=int)

# Итерации
for i in range(100):
    mask = np.abs(Z) <= 2
    Z[mask] = Z[mask]**2 + c[mask]
    mandelbrot_set[mask] += 1

# Визуализация
plt.figure(figsize=(10, 8))
plt.imshow(mandelbrot_set, extent=(-2, 1, -1.5, 1.5), cmap='hot', norm=mcolors.PowerNorm(0.5))
plt.colorbar(label='Итерации')
plt.title("Фрактал Мандельброта")
plt.show()

```
![Мандельброт](https://github.com/user-attachments/assets/5682ba01-ce6a-4024-8e8c-eaacf3e7ce18)
**Задача 5 - Дан массив координат частиц, которые изначально находятся в центре. Визуализируйте процесс их расхождения от центра с разными скоростями.**
```
particles = np.zeros((100, 2))  # 100 частиц в центре
velocities = np.random.uniform(-1, 1, (100, 2))  # Случайные скорости

# Визуализация
plt.figure(figsize=(6, 6))
for step in range(10):  # 10 шагов
    particles += velocities  # Обновление координат
    plt.scatter(particles[:, 0], particles[:, 1], alpha=0.6, label=f"Шаг {step + 1}")

plt.title("Расхождение частиц")
plt.legend()
plt.axis("equal")
plt.show()

```
![Частицы](https://github.com/user-attachments/assets/42edfa3c-008b-439b-9959-e8f04a2edd45)
**Задача 6 - Создайте симуляцию движения планет вокруг звезды на основе массивов координат и скоростей планет. Постройте анимацию, показывающую движение планет по их орбитам.**
```
# Параметры планетарной системы
num_planets = 5  # Количество планет
radii = np.linspace(50, 200, num_planets)  # Радиусы орбит планет
speeds = 1 / np.sqrt(radii)  # Скорости обратно пропорциональны корню радиуса
colors = ['red', 'blue', 'green', 'orange', 'purple']  # Цвета планет

# Настройка графика
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-250, 250)
ax.set_ylim(-250, 250)
ax.set_aspect('equal')
ax.set_facecolor('black')
ax.axis('off')

# Солнечная система: звезда и планеты
star = plt.Circle((0, 0), 10, color='yellow', zorder=10)
ax.add_artist(star)

# Создание массивов для позиций планет
planet_positions = [plt.Circle((0, 0), 5, color=colors[i], zorder=5) for i in range(num_planets)]
for planet in planet_positions:
    ax.add_artist(planet)

# Функция обновления кадров
def update(frame):
    for i, planet in enumerate(planet_positions):
        x = radii[i] * np.cos(speeds[i] * frame * 0.5)  # Умножаем на 0.5 для более заметной скорости
        y = radii[i] * np.sin(speeds[i] * frame * 0.5)
        planet.center = (x, y)
    return planet_positions

# Анимация
ani = animation.FuncAnimation(fig, update, frames=200, interval=50, blit=True)

# Сохранение анимации в GIF
ani.save("planet_simulation_kepler.gif", writer="pillow")

# Отображение в Google Colab
from IPython.display import Image
Image("planet_simulation_kepler.gif")

```
![planet_simulation_kepler](https://github.com/user-attachments/assets/e9242c20-9c04-4953-b45b-de836233a505)
**Задача 7 - Напишите программу, которая генерирует массивы данных для трехмерной функции (например, z = f(x, y)) и строит ее график в виде поверхности.**
```
# Генерация данных
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)

# Настройка графика
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

def update(frame):
    ax.clear()
    Z = np.sin(np.sqrt(X**2 + Y**2) - 0.1 * frame)  # Имитация капли
    ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.set_zlim(-1, 1)
    ax.set_title(f"Волна. Шаг: {frame}")

ani = animation.FuncAnimation(fig, update, frames=62, interval=100)

# Сохранение анимации в GIF
ani.save("wave_simulation.gif", writer="pillow")

# Отображение в Google Colab
from IPython.display import Image
Image("wave_simulation.gif")

```
![wave_simulation](https://github.com/user-attachments/assets/e58b976c-c2ec-40f0-bb09-d3e4b16bdcd2)
**Задача 8 - Дан двумерный массив с данными о температуре в разных точках региона. Визуализируйте данные в виде тепловой карты, где цвета будут соответствовать разным температурным значениям.**
```
# Создание двумерного массива температур
temperatures = np.random.uniform(-10, 40, (20, 20))  # Температуры в °C

# Визуализация тепловой карты
plt.figure(figsize=(7, 6))
plt.imshow(temperatures, cmap='coolwarm', interpolation='nearest')
plt.colorbar(label='Температура (°C)')
plt.title("Тепловая карта региона")
plt.show()
```
![Температура](https://github.com/user-attachments/assets/943a8bc4-3774-40c8-aafe-8352ff67a7c5)
**Задача 9 - Дан массив, представляющий сеть узлов и соединений между ними (например, социальная сеть или компьютерная сеть). Постройте граф, визуализирующий эту сеть.**
```
# Настройки
network = nx.DiGraph()
devices = ['Firewall', 'Server', 'PC1', 'PC2', 'Printer', 'Router', 'WiFi']
edges = [('Firewall', 'Server'), ('Server', 'Router'), ('Router', 'PC1'), ('Router', 'PC2'), ('Router', 'Printer'), ('Router', 'WiFi')]

# Построение графа
network.add_nodes_from(devices)
network.add_edges_from(edges)

# Визуализация графа
plt.figure(figsize=(10, 7))
nx.draw_networkx(network, with_labels=True, node_color='skyblue', font_weight='bold')
plt.title("Локальная сеть предприятия")
plt.show()
```
![Сеть](https://github.com/user-attachments/assets/1aef2bc4-a3d8-4f11-99c9-77c605eae1a5)
**Задание 10 - Дан массив значений, представляющих амплитуды волны в различных точках пространства. Создайте анимацию, которая покажет распространение волны с течением времени.**
```
# Настройки пространства
size = 500  # Размер экрана
slit_distance = 50  # Расстояние между щелями
wavelength = 20  # Длина волны
screen_distance = 200  # Расстояние до экрана

# Создание двумерного массива экрана
x = np.linspace(-size // 2, size // 2, size)
y = np.linspace(0, size, size)
X, Y = np.meshgrid(x, y)

# Расчет амплитуд для каждого опыта
def calculate_interference(num_slits=2):
    intensity = np.zeros_like(X)
    for i in range(num_slits):
        slit_y = 0
        slit_x = i * slit_distance - (num_slits - 1) * slit_distance / 2
        r = np.sqrt((X - slit_x)**2 + (Y - slit_y + screen_distance)**2)
        intensity += np.sin(2 * np.pi * r / wavelength)
    return intensity**2

# Настройка анимации
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
axes[0].set_title("Интерференция света (много полос)")
axes[1].set_title("Двухщелевой опыт (две полоски)")
im1 = axes[0].imshow(calculate_interference(10), extent=(-size // 2, size // 2, 0, size), cmap="viridis", origin="lower")
im2 = axes[1].imshow(calculate_interference(2), extent=(-size // 2, size // 2, 0, size), cmap="viridis", origin="lower")

def update(frame):
    phase_shift = frame * 2 * np.pi / 50
    intensity1 = calculate_interference(10) * np.sin(phase_shift)
    intensity2 = calculate_interference(2) * np.sin(phase_shift)
    im1.set_array(intensity1)
    im2.set_array(intensity2)
    return im1, im2

ani = animation.FuncAnimation(fig, update, frames=100, interval=50)

# Сохранение анимации в GIF
ani.save("young_double_slit.gif", writer="pillow")

# Отображение в Google Colab
from IPython.display import Image
Image("young_double_slit.gif")
```
![young_double_slit](https://github.com/user-attachments/assets/111301a2-a02a-45ee-a5d6-a92ff1313ab5)

## Контакты

Если у вас есть вопросы или предложения, пожалуйста, свяжитесь со мной:

- **[Email](mailto:nikolaev.m.d2@edu.mirea.ru)** <img src="https://www.svgrepo.com/show/452213/gmail.svg" alt="Email Icon" width="20"/>
- **[GitHub](https://github.com/MaxNiko2903)** <img src="https://www.svgrepo.com/show/475654/github-color.svg" alt="GitHub Icon" width="20"/>
- **[VK](https://vk.com/maxniko2903)** <img src="https://www.svgrepo.com/show/349554/vk.svg" alt="VK Icon" width="20"/>
- **[Telegram](https://t.me/maxniko2903)** <img src="https://www.svgrepo.com/show/354443/telegram.svg" alt="Telegram Icon" width="20"/>

---

**Николаев Максим Дмитриевич**  
**Москва, Институт РТУ МИРЭА** 

