import pygame
import sys


def run():
    # Initialize game and create a screen object.
    pygame.init()
    screen = pygame.display.set_mode((1366, 658))
    pygame.display.set_caption("Keys")

    font = pygame.font.SysFont('Comic Sans MS', 100)

    centercoordinates = (screen.get_rect().centerx, screen.get_rect().centery)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                screen.fill((255, 255, 255))
                textsurf = font.render(str(event.key), False, (0, 0, 0))
                screen.blit(textsurf, centercoordinates)

        pygame.display.flip()


run()
