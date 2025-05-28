import pygame
import os

BASE_IMG_PATH = "assets/images/"

def loadImage(path):
    """
    Loads a single image from the assets/images directory.

    Args:
        path (str): The path to the image file, relative to the assets/images directory.

    Returns:
        pygame.Surface: The loaded image.
    """
    return pygame.image.load(BASE_IMG_PATH + path).convert_alpha()

def loadImages(path):
    """
    Loads a sequence of images from the assets/images directory.

    Args:
        path (str): The path to the image sequence, relative to the assets/images directory.

    Returns:
        list of pygame.Surface: The loaded images, in the order they were found in the directory.
    """
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(loadImage(path + "/" + img_name))
    return images