#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import pygame
from pygame import *
from player import *
from blocks import *
from monsters import *

#Объявляем переменные
WIN_WIDTH = 800 #Ширина создаваемого окна
WIN_HEIGHT = 640 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#000000"

FILE_DIR = os.path.dirname(__file__)

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)
        
def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-WIN_WIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-WIN_HEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h) 


def loadLevel():
    global playerX, playerY # объявляем глобальные переменные, это координаты героя

            playerX= 0
            playerY = 0
                tp = BlockTeleport(int(commands[1]),int(commands[2]),int(commands[3]),int(commands[4]))
                entities.add(tp)
                platforms.append(tp)
                animatedEntities.add(tp)
    x=y=0 # координаты
    total_level_width  = len(level[0])*PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = len(level)*PLATFORM_HEIGHT   # высоту
    for row in level: # вся строка
        for col in row: # каждый символ
            if col == "-":
                pf = Platform(x,y)
                entities.add(pf)
                platforms.append(pf)
            if col == "*":
                bd = Platform(x,y)
                entities.add(bd)
                platforms.append(bd)
            if col == "P":
                pr = Princess(x,y)
                entities.add(pr)
                platforms.append(pr)
                animatedEntities.add(pr)
   
            x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT    #то же самое и с высотой
        x = 0                   #на каждой новой строчке начинаем с нуля

def main():
    loadLevel()
    pygame.init() # Инициация PyGame, обязательная строчка 
    screen = pygame.display.set_mode(DISPLAY) # Создаем окошко
    pygame.display.set_caption("Super Mario Boy") # Пишем в шапку
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) # Создание видимой поверхности
                                         # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))     # Заливаем поверхность сплошным цветом
        
    left = right = False # по умолчанию - стоим
    up = False
    running = False
     
    hero = Player(playerX,playerY) # создаем героя по (x,y) координатам
    entities.add(hero)
           
    timer = pygame.time.Clock()
    
    
    camera = Camera(camera_configure, total_level_width, total_level_height) 
    
    while not hero.winner: # Основной цикл программы
        timer.tick(60)
        for e in pygame.event.get(): # Обрабатываем события
            if e.type == QUIT:
                raise SystemExit, "QUIT"
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_LSHIFT:
                running = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_LSHIFT:
                running = False

        screen.blit(bg, (0,0))      # Каждую итерацию необходимо всё перерисовывать 

        animatedEntities.update() # показываеaм анимацию 
        monsters.update(platforms) # передвигаем всех монстров
        camera.update(hero) # центризируем камеру относительно персонажа
        hero.update(left, right, up, running, platforms) # передвижение
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()     # обновление и вывод всех изменений на экран
        
level = []
entities = pygame.sprite.Group() # Все объекты
animatedEntities = pygame.sprite.Group() # все анимированные объекты, за исключением героя
platforms = [] # то, во что мы будем врезаться или опираться
if __name__ == "__main__":
    main()
