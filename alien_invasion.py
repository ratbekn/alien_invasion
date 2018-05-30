import pygame
import game_functions as gf
from settings import Settings
from ship import Ship
from alien import Alien
from pygame.sprite import Group


def run_game():
    # Initialize game and create a screen object
    pygame.init()
    display = pygame.display
    settings = Settings()
    screen = display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make a ship.
    ship = Ship(settings, screen)

    # Make a group to store bullets in.
    bullets = Group()

    # Make an alien.
    alien = Alien(settings, screen)

    # Start the main loop for the game.
    while True:
        gf.check_events(settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(bullets)
        gf.update_screen(settings, screen, ship, alien, bullets)


run_game()
