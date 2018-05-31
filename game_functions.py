import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_events(settings, screen, ship, bullets):
    """Respond to keppresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_keydown_events(event, settings, screen, ship, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, ship, bullets)


def fire_bullet(settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """Respond to keyreleases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_q:
        sys.exit()


def update_screen(settings, screen, ship, aliens, bullets):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(settings.bg_color)
    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(settings, screen, ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(settings, screen, ship, aliens, bullets)


def check_bullet_alien_collisions(settings, screen, ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        # Destroy existing bullets and create new fleet.
        bullets.empty()
        create_fleet(settings, screen, ship, aliens)


def get_number_rows(settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def get_number_aliens_x(settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in row.
    # Spacing between each alien is equal to one alien width.
    alien = Alien(settings, screen)
    number_aliens_x = get_number_aliens_x(settings, alien.rect.width)
    number_rows = get_number_rows(settings, ship.rect.height,
                                  alien.rect.height)

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(settings, screen, aliens, alien_number, row_number)


def update_aliens(settings, stats, screen, ship, aliens, bullets):
    """
    Check if the fleet is at edge,
        and then update the positions of all aliens in the fleet.
    """
    check_fleet_edges(settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, stats, screen, ship, aliens, bullets)


def check_fleet_edges(settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break


def change_fleet_direction(settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1


def ship_hit(settings, stats, screen, ship, aliens, bullets):
    """Respond to ship being his by alien."""
    # Decrement ships_left.
    stats.ships_left -= 1

    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()

    # Create a new fleet and center the ship.
    create_fleet(settings, screen, ship, aliens)
    ship.center_ship()

    # Pause.
    sleep(0.5)
