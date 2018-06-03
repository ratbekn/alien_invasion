import pygame
import game_functions as gf
from settings import Settings
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStats
from button import Button


def run_game():
    # Initialize game and create a screen object
    pygame.init()
    display = pygame.display
    settings = Settings()
    screen = display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make the Play button.
    play_button = Button(settings, screen, "Play")

    # Create an instance to store game statistics.
    stats = GameStats(settings)

    # Make a ship, a group of bullets, and a group of aliens.
    ship = Ship(settings, screen)
    bullets = Group()
    aliens = Group()

    # Create the fleet of aliens.
    gf.create_fleet(settings, screen, ship, aliens)

    # Start the main loop for the game.
    while True:
        gf.check_events(settings, screen, stats, play_button, ship, aliens,
                        bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(settings, screen, ship, aliens, bullets)
            gf.update_aliens(settings, stats, screen, ship, aliens, bullets)

        gf.update_screen(settings, screen, stats, ship, aliens, bullets,
                         play_button)


run_game()
