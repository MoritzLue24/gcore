import os
import pygame


assets_path = os.path.dirname(os.path.abspath(__file__)) + "/../../assets/"

pygame.font.init()
fonts = {
    "dialogue": pygame.font.Font(assets_path  + "/Pixeboy-z8XGD.ttf", 40),
    "text": pygame.font.Font(assets_path  + "/Pixeboy-z8XGD.ttf", 30)
}

