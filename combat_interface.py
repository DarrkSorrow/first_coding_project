import pygame
import buttons_clog


def combat_start_screen(enemy, screen):

    font = pygame.font.SysFont(None, 48)
    screen_rect = screen.get_rect()
    screen.fill((150,0,0))
    prompt = "ist dabei dich anzugreifen!"
    text = f"Ein {enemy.name} {prompt}"
    text_image = font.render(text, True, (50, 50, 50), (0, 0, 0))
    text_rect = text_image.get_rect()
    text_rect.center = screen_rect.center
    screen.blit(text_image, text_rect)
    pygame.display.flip()


def combat_inputs(hero, enemy, screen, step):

    key = enemy_visuals(hero, enemy, screen, step)
    action = buttons_clog.combat_buttons(screen)
    
    return action, key


def combat_interface(hero, enemy, screen):

    hero_health_bar(hero, screen)
    hero_mana_bar(hero, screen)
    buttons_clog.dungeon_inventory(hero, screen)
    buttons_clog.abilities_displayed(hero, screen)
    hero_combat_stats(hero, screen)
    show_buffs(hero, screen)
    
    enemy_health_bar(enemy, screen)
    enemy_combat_stats(enemy, screen)
    show_enemy_buffs(enemy, screen)

    pygame.display.flip()


def hero_health_bar(hero, screen):

    font = pygame.font.SysFont(None, 22)
    stat_hp = f"HP: {hero.life} / {hero.max_life}"
    text_image = font.render(stat_hp, True, (0, 0, 0))

    width, height = 300, 25
    pygame.draw.rect(screen, (0, 0, 0),
                      (30, 715, width, height), 2)
    current_width = round(width * hero.life / hero.max_life)
    pygame.draw.rect(screen, (40, 250, 55),
                    (30, 715, current_width, height))

    if hero.over_hp > 0:
        block_width = width * hero.over_hp / hero.max_life
        pygame.draw.rect(screen, (100, 100, 100),
                    (30+current_width, 715, block_width, height))

    screen.blit(text_image, (50, 722))


def hero_mana_bar(hero, screen):

    font = pygame.font.SysFont(None, 22)
    stat_mana = f"Odem: {hero.mana} / {hero.max_mana}"
    text_image = font.render(stat_mana, True, (255, 255, 255))

    width, height = 300, 25
    pygame.draw.rect(screen, (255, 255, 255),
                    (30, 755, width, height), 2)
    current_width = round(width * hero.mana / hero.max_mana)
    pygame.draw.rect(screen, (40, 55, 255),
                    (30, 755, current_width, height))
    screen.blit(text_image, (50, 760))


def hero_combat_stats(hero, screen):

    font = pygame.font.SysFont(None, 20)
    y = 500

    stats = [
        f"DMG: {int(max(hero.damage, 0))}",
        f"SPEED: {int(max(hero.speed, 0))}",
        f"DODGE: {int(max(hero.dodge, 0))}",
        f"ARMOR: {int(max(hero.reduction, 0))}",
        f"MENTAL: {int(max(hero.mental_reduction, 0))}",
        f'CRIT: {int(max(hero.critical, 0))}',
        f'ACC: {int(max(hero.accuracy, 0))}',
        f"enemies in row: {hero.game_state.enemy_counter}",
        f"event in row: {hero.game_state.events_in_row}",
    ]

    for stat in stats:

        text = font.render(stat, True, (255, 255, 255))

        screen.blit(text, (20, y))
        y += 20


def show_buffs(hero, screen):
    
    font = pygame.font.SysFont(None, 20)   
    x = 80
    
    for buff in hero.buffs:

        buff_text = f"{buff}({buff.duration})"
        text = font.render(
            buff_text, True, (0, 0, 0))
        screen.blit(text, (x, 690))
        x += 80


def enemy_visuals(hero, enemy, screen, step):
    """Enemy-Sprites and enemy-intent icon"""
    enemy.blitme(screen)
    text, key = enemy.enemy_intend(step, hero)
    screen.blit(text, (710, 150))
    return key


def enemy_health_bar(enemy, screen):

    font = pygame.font.SysFont(None, 22)
    stat_hp = f"{enemy.name}"
    text_image = font.render(stat_hp, True, (0, 0, 0))

    width, height = 300, 25
    pygame.draw.rect(screen, (0, 0, 0),
                      (500, 50, width, height), 2)
    current_width = round(width * enemy.life / enemy.max_life)
    pygame.draw.rect(screen, (200, 50, 55),
                      (500, 50, current_width, height))
    
    if enemy.over_hp > 0:
        block_width = width * enemy.over_hp / enemy.max_life
        pygame.draw.rect(screen, (100, 100, 100),
                    (500+current_width, 50, block_width, height))

    screen.blit(text_image, (520, 56))


def enemy_combat_stats(enemy, screen):

    font = pygame.font.SysFont(None, 20)
    y = 120

    stats = [
        f"DMG: {int(max(enemy.damage, 0))}",
        f"SPEED: {int(max(enemy.speed, 0))}",
        f"DODGE: {int(max(enemy.dodge, 0))}",
        f"ARMOR: {int(max(enemy.reduction, 0))}",
        f"MENTAL: {int(max(enemy.mental_reduction, 0))}",
        f'CRIT: {int(max(enemy.critical, 0))}',
        f'ACC: {int(max(enemy.accuracy, 0))}'
    ]

    for stat in stats:

        text = font.render(
            stat, True, (255, 255, 255))
        screen.blit(text, (1100, y))
        y += 20


def show_enemy_buffs(enemy, screen):

    font = pygame.font.SysFont(None, 22)
    x = 500

    for buff in enemy.buffs:
        
        buff_text = f"{buff}({buff.duration})"
        text = font.render(
            buff_text, True, (0, 0, 0))
        screen.blit(text, (x, 100))
        x += 80
