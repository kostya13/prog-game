#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import os
import pyganim

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#000000"
ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами

ANIMATION_BLOCKTELEPORT = [
            ('%s/blocks/portal2.png' % ICON_DIR),
            ('%s/blocks/portal1.png' % ICON_DIR)]
            
 
class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("blocks/platform.png")
        self.image.set_colorkey(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        
class Stop(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("blocks/stop.png")
        self.image.set_colorkey(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        
class BlockTeleport(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        boltAnim = []
        for anim in ANIMATION_BLOCKTELEPORT:
            boltAnim.append((anim, 0.3))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()
        
    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

        
class Skill(Platform):
    def __init__(self, x, y, image_path):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load(image_path)
        self.image.set_colorkey(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

       
