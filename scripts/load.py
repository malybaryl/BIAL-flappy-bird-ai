import pygame
import os

BASE_IMG_PATH = "assets/images/"

def loadImage(path):
    return pygame.image.load(BASE_IMG_PATH + path).convert_alpha()

def loadImages(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(loadImage(path + "/" + img_name))
    return images