import constants, pygame
from controller import GameController



def main():
    controller = GameController(constants.SCREEN)
    while True:
        for event in pygame.event.get():
            controller.handle(event)



main()