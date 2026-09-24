import pygame, random
from time import sleep
from world_rooms import *
from items import *
import abilities, buttons_clog
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
            hero.xp += round(hero.xp / 2)

    screen.fill((20, 255, 20))
    pygame.display.flip(), sleep(2)


def wandering_merchant(hero, stage, screen):
    """hero can buy items and abilities"""
    screen.fill((250, 250, 250))
    font = pygame.font.SysFont(None, 18)
    hero_health_bar(hero, screen)
    hero_mana_bar(hero, screen)
    hero_xp(hero, screen)
    hero_left = False#if true the merchant dissapears

    merchant_offer = []
    while len(merchant_offer) < 6:
    #prepares store items
        if len(merchant_offer) < 3:
            item = random_item(stage)
            if item not in merchant_offer:
                merchant_offer.append(item)

        elif len(merchant_offer) < 5:
            item = random_gear(stage)
            if item not in merchant_offer:
                merchant_offer.append(item)

        elif len(merchant_offer) < 6:
            spells = abilities.random_abilities(hero, stage)
            spell = random.choice(spells)
            merchant_offer.append(spell())

    shop, inventory = buttons_clog.merchant_buttons(hero, screen)
    buttons = inventory + shop

    inventory_index = len(hero.inventory) + len(hero.pockets)
    for i, button in enumerate(buttons):
        if inventory_index <= i < inventory_index + 6:
            buttons[i].text = merchant_offer[i-inventory_index].name
        button.draw(screen, font)
    buttons[-1].text = 'EXIT'

    while not hero_left:
        inventory_index = len(hero.inventory) + len(hero.pockets)
        pygame.display.flip()
        
        choice = buttons_clog.display_answers_clicked(buttons)
        choice = int(choice)
        match choice:

            #SELL-ITEMS *** SELL-ITEMS *** SELL-ITEMS
            case i if 1 <= i <= inventory_index:
                if hero.inventory[i].gear:
                    hero.xp += round(hero.inventory[i].xp * 0.65)
                    hero.inventory[i].unequip(hero)
                else:

                    try:
                        if hero.inventory[i].dungeon:
                            hero.inventory[i].use_item(hero, None, None)
                        else:#just some pennies
                            hero.xp += round(hero.inventory[i] * 0.1)
                            hero.inventory[i]._remove(hero)

                    except ValueError:
                        if hero.pocket[i].dungeon:
                            hero.pocket[i].use_item(hero, None, None)
                        else:#health and mana potions consumed
                            hero.pocktes[i]._remove(hero)
            #SELL-ITEMS *** SELL-ITEMS ***SELL-ITEMS

            #CONSUMABLES *** CONSUMABLES *** CONSUMABLES
            case i if inventory_index < i <= inventory_index + 3:
                inventory_space = len(hero.inventory)<hero.max_inventory
                has_space = inventory_space or len(hero.pockets)<hero.pcoket_size
                if has_space and merchant_offer[i].xp*1.2 <= hero.xp:
                    hero.xp -= round(merchant_offer[i].xp * 1.2)
                    merchant_offer[i]._append(hero)
            #CONSUMABLES *** CONSUMABLES *** CONSUMABLES

            #GEAR *** GEAR *** GEAR
            case i if inventory_index + 3 < i <= inventory_index + 5:
                has_space = len(hero.inventory)<hero.max_inventory
                if has_space and merchant_offer[i].xp*1.5 <= hero.xp:
                    hero.xp -= round(merchant_offer[i].xp * 1.5)
                    merchant_offer[i].equip(hero)
            #GEAR *** GEAR *** GEAR

            #ABILITY *** ABILITY *** ABILITY
            case i if inventory_index + 5 < i <= inventory_index + 6:
                ability = merchant_offer[i]
                abilities.abilities_from_events(hero, ability, screen)

            #ABILITY *** ABILITY *** ABILITY

            #EXIT *** EXIT *** EXIT
            case i if inventory_index + 6 < i <= inventory_index + 7:
                hero_left = True
            #EXIT *** EXIT *** EXIT
    return None


def reward(hero, enemy, stage, screen):
    
    screen.fill((50, 50, 50))
    buttons_clog.abilities_displayed(hero, screen)
    buttons_clog.dungeon_inventory(hero, screen)
    pygame.display.flip()

    match stage:
        
        #Akt 0 *** Akt 0 *** Akt 0
        case 0:
            points = 35
            points += random.randint(0, 35)
            reward_system(hero, stage, points, screen)

        #Akt 1 *** Akt 1 *** Akt 1
        case 1 | 2 | 3:
            match enemy:
                case 1:
                    points = 100
                    points += random.randint(0, 50)
                    reward_system(hero, stage, points, screen)
                case 2:
                    points = 150
                    points += random.randint(0, 100)
                    reward_system(hero, stage, points, screen)    
                case 3:
                    boss_reward(hero, screen)

        #Akt 2 *** Akt 2 *** Akt 2
        case 4 | 5 | 6:
            match enemy:
                case 1:
                    points = 300
                    points += random.randint(0, 150)
                    reward_system(hero, stage, points, screen)
                case 2:
                    points = 450
                    points += random.randint(0, 300)
                    reward_system(hero, stage, points, screen)
                case 3:
                    boss_reward(hero, screen)

        #Akt 3 *** Akt 3 *** Akt 3
        case 7 | 8 | 9:
            match enemy:
                case 1:
                    points = 900
                    points += random.randint(0, 450)
                    reward_system(hero, stage, points, screen)
                case 2:
                    points = 1350
                    points += random.randint(0, 900)
                    reward_system(hero, stage, points, screen)
                case 3:
                    pass#hero won
        

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
            
        case '4':
            hero.max_abilities += 1
            
    hero.life += round(hero.max_life / 2)
    if hero.life >= hero.max_life:
        hero.life = hero.max_life

    hero.mana += round(hero.max_mana / 3)
    if hero.mana >= hero.max_mana:
        hero.mana = hero.max_mana

        
def reward_system(hero, stage, points, screen):

    font = pygame.font.SysFont(None, 28)
    y = 100

    item = random_gear(stage)
    if item.xp <= points:
        y = get_item(hero, item, screen, font, y)
        points -= item.xp
    
    item = random_item(stage)
    if item.xp <= points:
        y = get_item(hero, item, screen, font, y)
        points -= item.xp
    
    if points != 0:
        hero.xp += points
        text = f"+{points}XP"
        y = buttons_clog.display_text(text, y, screen, font)
        sleep(1)


def get_item(hero, item, screen, font, y):

    if item.gear and len(hero.inventory) < hero.max_inventory:            
        item.equip(hero), sleep(1)
        text = f"{item} erhalten"
        y = buttons_clog.display_text(text, y, screen, font)

    elif not item.gear and len(hero.inventory+hero.pockets)<hero.max_inventory+hero.pocket_size:
        item._append(hero), sleep(1)
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
            if item.gear:
                cashback = item.xp * 0.85
            else:
                cashback = item.xp * 0.4

            hero.xp += round(cashback)
            text = f'+{round(cashback)}XP'
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

    try:
        item = hero.inventory[choice]
    except ValueError:
        item = hero.pockets[choice - hero.max_inventory]

    if item.gear:
        cashback = item.xp * 0.65
    else:
        cashback = 0

    hero.xp += round(cashback)
    text = f'+{round(cashback)}XP'
    y = buttons_clog.display_text(text, y, screen, font)

    text = f'{item.name} aus dem Inventar entfernt.'
    y = buttons_clog.display_text(text, y, screen, font)

    if item.gear:
        item.unequip(hero)
    else:
        item._remove(hero)

    text = f'{reward.name} dem Inventar hinzugefügt.'
    y = buttons_clog.display_text(text, y, screen, font)

    if reward.gear:
        reward.equip(hero)
    else:
        reward._append(hero)
    
    return y


def hero_xp(hero, screen):

    font = pygame.font.SysFont(None, 32)
    text = f"{hero.name}: {hero.xp}XP"
    textrend = font.render(text, True, (255, 255, 255))
    screen.blit(textrend, (20, 50))


def arm_hero(hero):#only called during the beginning

    #items = (ShortSword(), RitualDagger(), ElvenBoots())
    items = ()

    try:
        for item in items:
            if item.gear:
                item.equip(hero)
            else:
                item._append(hero)
    except TypeError:
        if items.gear:
            items.equip(hero)
        else:
            items._append(hero)