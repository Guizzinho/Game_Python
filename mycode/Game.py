import pygame
from mycode.Menu import Menu
from mycode.Const import WIN_WIDTH, WIN_HEIGHT

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        print("Setup Start")
        print("Setup End")


    def run(self):


        while True:
            menu = Menu(self.window)
            menu.run()
            print("Loop Start")
            pass








