import pygame, random
from time import sleep
from world_rooms import *
import items, buttons_clog
from combat_interface import hero_health_bar, hero_mana_bar


def generate_world(stage):
    dungeon = dungeon_by_stage(stage)
    return dungeon
        
        
def movement(hero, dungeon, position, event):

    match event.key:
        
        case pygame.K_UP:
            if dungeon[position[0]-1][position[1]].enter==True:
                if position[0] > 0:
                    position[0] -= 1

        case pygame.K_DOWN:
            if position[0] < len(dungeon) - 1:
                if dungeon[position[0]+1][position[1]].enter==True:
                    position[0] += 1

        case pygame.K_LEFT:
            if dungeon[position[0]][position[1]-1].enter==True:
                if position[1] > 0:
                    position[1] -= 1

        case pygame.K_RIGHT:
            if position[1] < len(dungeon[0]) - 1:
                if dungeon[position[0]][position[1]+1].enter==True:
                    position[1] += 1

        case pygame.K_i:
            pass
            
    return position


def bond_fire(hero, stage, screen):
    """Hero can rest or gain xp"""
    screen.fill((20, 255, 20))
    font = pygame.font.SysFont(None, 24)
    hero_health_bar(hero, screen)
    hero_mana_bar(hero, screen)
    hero_xp(hero, screen), pygame.display.flip()

    buttons = buttons_clog.bond_fire_buttons(hero)

    for button in buttons:
        button.draw(screen, font)

    pygame.display.flip()

    action = buttons_clog.display_answers_clicked(buttons)
    match action:
        
        case "1":
            healing = round(hero.max_life / 2)
            hero.life += healing
            if hero.life > hero.max_life:
                hero.life = hero.max_life
        
        case "2":
            hero.mana = hero.max_mana
        
        case "3":
            hero.xp += round(hero.xp * 0.7)

    screen.fill((20, 255, 20))
    pygame.display.flip(), sleep(3)


def reward(hero, enemy, stage, screen):
    
    screen.fill((50, 50, 50)), pygame.display.flip()

    if stage == 0:
        points = 35
        points += random.randint(0, 35)
        reward_system(hero, points, screen)

    elif enemy == 1:
        points = 100
        points += random.randint(0, 50)
        reward_system(hero, points, screen)

    elif enemy == 2:
        points = 150
        points += random.randint(0, 100)
        reward_system(hero, points, screen)    

    elif enemy == 3:
        boss_reward(hero,screen)
        

def boss_reward(hero, screen):

    font = pygame.font.SysFont(None, 20)
    screen.fill((150, 50, 50)), pygame.display.flip()
    buttons = buttons_clog.boss_reward_and_buttons(hero, screen)

    for button in buttons:
        button.draw(screen, font)

    pygame.display.flip()

    choice = buttons_clog.display_answers_clicked(buttons)
    match choice:
        case '1':
            hero.max_life += 100
            hero.reduction += 10
        case '2':
            hero.max_mana += 100
            hero.mental_reduction += 10
        case '3':
            hero.max_inventory += 1
            #some item has to be given
        case '4':
            hero.max_abilities += 1
            hero.xp += 150 # sollte dynamisch sein 
            
    hero.life += round(hero.max_life / 2)
    if hero.life >= hero.max_life:
        hero.life = hero.max_life

    hero.mana += round(hero.max_mana / 3)
    if hero.mana >= hero.max_mana:
        hero.mana = hero.max_mana

        
def reward_system(hero, points, screen):

    font = pygame.font.SysFont(None, 28)
    y = 100

    item = items.random_gear()
    if item.xp <= points:
        y = get_item(hero, item, screen, font, y)
        points -= item.xp
    
    item = items.random_item()
    if item.xp <= points:
        y = get_item(hero, item, screen, font, y)
        points -= item.xp
    
    if points != 0:
        hero.xp += points
        text = f"+{points}XP"
        y = buttons_clog.display_text(text, y, screen, font)
        sleep(1.5)


def get_item(hero, item, screen, font, y):

    if len(hero.inventory) < hero.max_inventory:            
        item.equip(hero), sleep(1)
        text = f"{item} erhalten"
        y = buttons_clog.display_text(text, y, screen, font)

    else:
        y = max_inventory(hero, item, screen, font, y)
    
    return y


def max_inventory(hero, item, screen, font, y):

    text = f'Du hast keinen Platz für {item.name}'
    y = buttons_clog.display_text(text, y, screen, font)

    text = 'MÖCHTEST DU EIN ITEM AUFLÖSEN?'
    y = buttons_clog.display_text(text, y, screen, font)

    buttons = buttons_clog.yes_no_button(screen, font)

    answer = buttons_clog.display_answers_clicked(buttons)
    pygame.draw.rect(                               #drawn to cover up
        screen, (50, 50, 50), (300, 500, 400, 300)) #old buttons
    pygame.display.flip()

    match answer:
        case '1':
            y = release_item(hero, item, screen, font, y)
        case '2':
            hero.xp += round(item.xp * 0.7)
            text = f'+{round(item.xp * 0.7)}XP'
            y = buttons_clog.display_text(text, y, screen, font)
            del item
    return y


def release_item(hero, item, screen, font, y):
    
    reward = item #stores reward before item-variable changes
    
    buttons = buttons_clog.item_buttons(hero ,screen)

    text = "Welchen Gegenstand auflösen?"
    y = buttons_clog.display_text(text, y, screen, font)

    choice = buttons_clog.display_answers_clicked(buttons)
    choice = int(choice)
    item = hero.inventory[choice]
    hero.xp += round(item.xp * 0.3)
    text = f'+{round(item.xp * 0.3)}XP'
    y = buttons_clog.display_text(text, y, screen, font)

    text = f'{item.name} aus dem Inventar entfernt.'
    y = buttons_clog.display_text(text, y, screen, font)
    item.unequip(hero)

    text = f'{reward.name} dem Inventar hinzugefügt.'
    y = buttons_clog.display_text(text, y, screen, font)
    reward.equip(hero)
    return y


def hero_xp(hero, screen):

    font = pygame.font.SysFont(None, 32)
    text = f"{hero.name}: {hero.xp}XP"
    textrend = font.render(text, True, (255, 255, 255))
    screen.blit(textrend, (20, 50))

