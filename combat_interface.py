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


def combat_interface(hero, enemy, screen, step):

    hero_health_bar(hero, screen)
    hero_mana_bar(hero, screen)
    buttons_clog.dungeon_inventory(hero, screen)
    buttons_clog.abilities_displayed(hero, screen)
    hero_combat_stats(hero, screen)
    show_buffs(hero, screen)
    
    key = enemy_sprite(hero, enemy, screen, step)
    enemy_health_bar(enemy, screen)
    enemy_combat_stats(enemy, screen)
    show_enemy_buffs(enemy, screen)

    pygame.display.flip()

    action = buttons_clog.combat_buttons(screen)
    
    return action, key


def hero_health_bar(hero, screen):

    font = pygame.font.SysFont(None, 22)
    stat_hp = f"HP: {hero.life} / {hero.max_life}"
    text_image = font.render(stat_hp, True, (0, 0, 0))

    width, height = 300, 25
    pygame.draw.rect(screen, (0, 0, 0),
                      (80, 710, width, height), 2)
    current_width = round(width * hero.life / hero.max_life)
    pygame.draw.rect(screen, (40, 250, 55),
                      (80, 710, current_width, height))

    if hero.over_hp > 0:
        block_width = width * hero.over_hp / hero.max_life
        pygame.draw.rect(screen, (100, 100, 100),
                    (80+current_width, 710, block_width, height))

    screen.blit(text_image, (100, 717))


def hero_mana_bar(hero, screen):

    font = pygame.font.SysFont(None, 22)
    stat_mana = f"Odem: {hero.mana} / {hero.max_mana}"
    text_image = font.render(stat_mana, True, (255, 255, 255))

    width, height = 300, 25
    pygame.draw.rect(screen, (255, 255, 255), (80, 750, width, height), 2)
    current_width = round(width * hero.mana / hero.max_mana)
    pygame.draw.rect(screen, (40, 55, 255), (80, 750, current_width, height))
    screen.blit(text_image, (100, 755))


def hero_combat_stats(hero, screen):

    font = pygame.font.SysFont(None, 20)
    y = 500

    stats = [
        f"DMG: {hero.damage}",
        f"SPEED: {hero.speed}",
        f"DODGE: {hero.dodge}",
        f"ARMOR: {hero.reduction}",
        f"MENTAL: {hero.mental_reduction}",
        f"enemy: {hero.game_state.enemy_counter}",
        f"event: {hero.game_state.events_in_row}",
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
        x += 100


def enemy_sprite(hero, enemy, screen, step):#Images
    """Enemy-Sprites and enemy-intent icon"""
    enemy.blitme(screen)#Enemysprite
    text, key = enemy.enemy_intend(step, hero)#ENemyintent
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
    y = 150

    stats = [
        f"DMG: {enemy.damage}",
        f"SPEED: {enemy.speed}",
        f"DODGE: {enemy.dodge}",
        f"ARMOR: {enemy.reduction}",
        f"MENTAL: {enemy.mental_reduction}",
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
        x += 100
