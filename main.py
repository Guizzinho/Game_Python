import pygame

pygame.init()
print("Setup Start")
window = pygame.display.set_mode(size=(900, 600))
print("Setup End")

print("Loop Start")
while True:
    #Check for all the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()#Close Window
            quit()#End Pygame