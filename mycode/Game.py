import pygame
from mycode.Menu import Menu
from mycode.Level import Level
from mycode.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTIONS


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        print("Setup Start")
        print("Setup End")

    def run(self):
        while True:
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return == MENU_OPTIONS[0]:
                level1 = Level(self.window, 'Level1', "./assets/Background/Castle/castle.png", "./assets/Sounds/castle_sound.wav", 1)
                level1_result = level1.run()

                if level1_result == 'completed':
                    level2 = Level(self.window, 'Level2', "./assets/Background/Forest/dead forest.png",
                                  "./assets/Sounds/forrest_sound.wav", 2)
                    level2_result = level2.run()
                    if level2_result == 'completed':
                        level3 = Level(self.window, 'Level3', "./assets/Background/Terrace/terrace.png",
                                       "./assets/Sounds/terrace_sound.wav",3)
                        level3_result = level3.run()
                        if level3_result == 'completed':
                            level4 = Level(self.window, 'Level4', "./assets/Background/Throne/throne_room.png",
                                           "./assets/Sounds/throne_sound.wav",5)
                            level4_result = level4.run()

            elif menu_return == MENU_OPTIONS[1]:
                pygame.quit()
                quit()







