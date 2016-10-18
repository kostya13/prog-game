#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import pygame
from pygame import *
from player import *
from blocks import *

#Объявляем переменные
WIN_WIDTH = 800 #Ширина создаваемого окна
WIN_HEIGHT = 350 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR1 = "#000000"
BACKGROUND_COLOR2 = "#003F00"

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

    level='--W-B--T--C---W------------B------------W-----M--------------WM----------C----------------------F'
    playerX= 0
    playerY = 0
    x = 0 # координаты
    y = 10 * PLATFORM_HEIGHT
    total_level_width  = len(level)*PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = 10*PLATFORM_HEIGHT   # высоту
    for col in level: # каждый символ
        pf = Platform(x,y)
        entities.add(pf)
        platforms.append(pf)
        if col == "B":
            bd = Book(x,y - PLATFORM_HEIGHT)
            entities.add(bd)
            platforms.append(bd)
        if col == "M":
            bd = Money(x,y - PLATFORM_HEIGHT)
            entities.add(bd)
            platforms.append(bd)
        if col == "C":
            bd = Conference(x,y - PLATFORM_HEIGHT)
            entities.add(bd)
            platforms.append(bd)
        if col == "W":
            bd = Computer(x,y - PLATFORM_HEIGHT)
            entities.add(bd)
            platforms.append(bd)
        if col == "F":
            bd = Briefcase(x,y - PLATFORM_HEIGHT)
            entities.add(bd)
            platforms.append(bd)
        if col == "T":
            tp = BlockTeleport(x, y - PLATFORM_HEIGHT)
            entities.add(tp)
            platforms.append(tp)
            animatedEntities.add(tp)
        x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
    return total_level_width, total_level_height

def main():
    total_level_width, total_level_height = loadLevel()
    pygame.init() # Инициация PyGame, обязательная строчка 
    screen = pygame.display.set_mode(DISPLAY) # Создаем окошко
    pygame.display.set_caption("Programmers emulator") # Пишем в шапку
    bg1 = Surface((WIN_WIDTH,WIN_HEIGHT)) # Создание видимой поверхности
                                         # будем использовать как фон
    bg1.fill(Color(BACKGROUND_COLOR1))     # Заливаем поверхность сплошным цветом
        
    bg2 = Surface((WIN_WIDTH,WIN_HEIGHT)) # Создание видимой поверхности
                                         # будем использовать как фон
    bg2.fill(Color(BACKGROUND_COLOR2))     # Заливаем поверхность сплошным цветом
        
    left = right = False # по умолчанию - стоим
    up = False
    running = False
     
    hero = Player(playerX,playerY, total_level_width) # создаем героя по (x,y) координатам
    entities.add(hero)
           
    timer = pygame.time.Clock()
    
    
    camera = Camera(camera_configure, total_level_width, total_level_height) 
    myfont = pygame.font.SysFont("arial.ttf", 35)
    winfont = pygame.font.SysFont("arial.ttf", 55)
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

        if hero.home:
            screen.blit(bg1, (0,0))      # Каждую итерацию необходимо всё перерисовывать 
        else:
            screen.blit(bg2, (0,0))      # Каждую итерацию необходимо всё перерисовывать 
        exp_label = myfont.render("Опыт: {}".format(hero.experience).decode('utf8'), 1, (255,255,0))
        level_label = myfont.render("Уровень: {}".format(hero.current_level).decode('utf8'), 1, (255,255,0))
        money_label = myfont.render("Деньги: {}".format(hero.money).decode('utf8'), 1, (255,255,0))
        city_label = myfont.render("Город: {}".format(hero.city()).decode('utf8'), 1, (255,255,0))
        if hero.current_level > 1:
            win_label = winfont.render("Вы достигли уровня 4!".decode('utf8'), 1, (255,255,255))
            screen.blit(win_label, (150, 150))
        screen.blit(exp_label, (0, 0))
        screen.blit(level_label, (0, 30))
        screen.blit(money_label, (0, 60))
        screen.blit(city_label, (0, 90))

        animatedEntities.update() # показываеaм анимацию 
        camera.update(hero) # центризируем камеру относительно персонажа
        hero.update(left, right, up, running, platforms, entities) # передвижение
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()     # обновление и вывод всех изменений на экран
        
entities = pygame.sprite.Group() # Все объекты
animatedEntities = pygame.sprite.Group() # все анимированные объекты, за исключением героя
platforms = [] # то, во что мы будем врезаться или опираться
if __name__ == "__main__":
        
    main()
