from time import sleep
from random import randint
from functools import partial
from combat_interface import *
import enemies, abilities, buttons_clog


def start_fight(hero, stage, screen):
    enemy = enemies.random_enemy(hero, stage)
    combat_start_screen(enemy, screen), sleep(1.5)
    main_fight(hero, enemy, screen)


def start_elite(hero, stage, screen):
    enemy = enemies.random_elite(hero, stage)
    combat_start_screen(enemy, screen), sleep(2)
    main_fight(hero, enemy, screen)


def start_boss(hero, stage, screen):
    enemy = enemies.random_boss(hero, stage)
    combat_start_screen(enemy, screen), sleep(2)
    main_fight(hero, enemy, screen)


def main_fight(hero, enemy, screen):
    
    font = pygame.font.SysFont(None, 20)
    combat_log = buttons_clog.CombatLog(screen, font)
    step = 0
    while enemy.life > 0 and hero.life > 0:

        cooldown_and_passive_trigger(hero, screen, combat_log)

        action, key = combat_interface(hero, enemy, screen, step)
        action = pre_hero_turn(
            hero, action, combat_log, screen, font)
        attack_order = []
        attack_order = who_first(hero, enemy, attack_order,
                                  key, action, combat_log, screen)
        #attack_order[] gets initialzied by () due to partial
        action_1 = attack_order[0]()#First move
        if action_1 != None:
            action = action_1
        pygame.display.flip()
        
        if hero.life > 0 and enemy.life > 0:# second move
            action_2 = attack_order[1]()
            if action_2 != None:
                action = action_2
            pygame.display.flip()
        
        debuff_hero_enemy(hero, enemy, combat_log, screen, font)
        undo(hero, enemy, action, combat_log, screen, font)
        step += 1

    hero_alive = after_combat(hero, enemy, combat_log)
    if not hero_alive:
        return None
    sleep(1), abilities.learn_ability(hero, screen), sleep(1)


def cooldown_and_passive_trigger(hero, screen, combat_log):

    screen.fill((150,100,0)), combat_log.draw()

    for spell in hero.abilities:#cooldown -1
        spell.reduce_cool_down()
        
    for item in hero.inventory:# triggers items if
        if item.passive_effekt:# passive_effekt 
            item.trigger_passive(hero)


def pre_hero_turn(hero, action, combat_log, screen, font):
    
    match action:
        case "0":  #Angriff
            None
        case "1":  #Abwehr
            hero.instant_defend()
        case "2":  #Fähigkeiten
            if hero.abilities == []:
                text = ("Du kannst doch garnichts.")
                combat_log.add(text)
            else:
                pygame.draw.rect(                               #drawn to cover up
                    screen, (150,100,0), (650, 500, 1100, 730)) #old buttons
                pygame.display.flip()
                action = buttons_clog.choose_ability(hero, action, screen)
        case "3":  #Gegenstände
            active_items = []
            for item in hero.inventory:
                if item.active:
                    active_items.append(item)
            if active_items == []:
                text = ("Du hast doch garnichts.")
                combat_log.add(text)
                hero.dodge += 15
                hero.speed += 300
            else:
                hero.dodge += 15
                hero.speed += 300
                text = (f"{hero.name} versucht blitzschnell in seine Tasche zu greifen!")
                combat_log.add(text)
        case _:
            text = ("!!Du hast das Gleichgewicht für einen Moment verloren!!")
            combat_log.add(text)
    sleep(1)
    return action


def who_first(hero, enemy, attack_order, key, action, combat_log, screen):
    
    total_speed = hero.speed + enemy.speed
    if total_speed < 1:
        magic_number = 1
    else:
        magic_number = randint(0, int(total_speed))
    
    if magic_number in range(round(hero.speed) + 1):
        attack_order.append(partial(hero_turn, hero, enemy, action, combat_log, screen))
        attack_order.append(partial(enemy_turn, hero, enemy, key, combat_log))
        text = f"{hero.name} ist schneller!"
        combat_log.add(text), sleep(0.5)
    
    else:
        attack_order.append(partial(enemy_turn, hero, enemy, key, combat_log))
        attack_order.append(partial(hero_turn, hero, enemy, action, combat_log, screen))
        text = f"{enemy.name} ist schneller!"
        combat_log.add(text, True), sleep(0.5)
    
    return attack_order


def enemy_turn(hero, enemy, key, combat_log):
    if enemy.life > 0:
       enemy.enemy_ai(hero, key, combat_log)
    return None


def hero_turn(hero, enemy, action, combat_log, screen):
    
    match action:

        case "0":
            abilities.enemy_block_dodge(hero, enemy, combat_log)
        case "1":
            hero.defend(combat_log)
            if hero.mana >= hero.max_mana:
                hero.mana = hero.max_mana
        case "a":
            casted = hero.abilities[0].use_ability(hero, enemy, combat_log)
            if casted:
                action = "z"
        case "b":
            casted = hero.abilities[1].use_ability(hero, enemy, combat_log)
            if casted:
                action = "y"
        case "c":
            casted = hero.abilities[2].use_ability(hero, enemy, combat_log)
            if casted:
                action = "x"
        case "d":
            casted = hero.abilities[3].use_ability(hero, enemy, combat_log)
            if casted:
                action = "w"
        case "3":
            active_items = []
            for item in hero.inventory:
                if item.active:
                    active_items.append(item)
            if active_items != []:
                pygame.draw.rect(                               #drawn to cover up
                    screen, (150,100,0), (650, 500, 1100, 730)) #old buttons
                pygame.display.flip()
                choice = buttons_clog.item_in_combat(hero, enemy, screen)
                hero.inventory[choice].use_item(hero, enemy, combat_log)
    
    return action


def undo(hero, enemy, action, combat_log, screen, font):
    
    match action:
        case "0":
            return None
        case "1":
            hero.undo_defend()
        case "z":
            hero.abilities[0].undo_ability(hero, enemy)
        case "y":
            hero.abilities[1].undo_ability(hero, enemy)
        case "x":
            hero.abilities[2].undo_ability(hero, enemy)
        case "w":
            hero.abilities[3].undo_ability(hero, enemy)
        case "3":
            hero.dodge -= 15
            hero.speed -= 300


def debuff_hero_enemy(hero, enemy, combat_log, screen, font):

    if hero.over_hp > 0:
        hero.decay_over_hp()

    if enemy.over_hp > 0:
        enemy.decay_over_hp()

    for buff in hero.buffs:
        if buff.active:
            buff.effekt(hero)
        buff.count_down()
        if buff.clear == True:
            buff.debuff(hero)

    for buff in enemy.buffs:
        if buff.active:
            buff.effekt(enemy)
        buff.count_down()
        if buff.clear == True:
            buff.debuff(enemy)


def after_combat(hero, enemy, combat_log):

    if hero.life <= 0:
        text = f"{hero.name} wurde von {enemy.name} erschlagen."
        combat_log.add(text)
        sleep(2)
        return False
    
    text = f"***Du hast {enemy.name} niedergestreckt***"
    combat_log.add(text)
    
    for spell in hero.abilities:#strip cooldowns after fight
        while spell.cool_down > 0:
            spell.reduce_cool_down()

    while hero.buffs != []: #strip buffs without pain
        for buff in hero.buffs:
            buff.count_down()
            if buff.clear == True:
                buff.debuff(hero)
    
    hero.over_hp = 0 # strip remaining block after fight

    for item in hero.inventory:# triggers items if
        if item.after_combat_effekt:# after_combat_effekt
            item.after_combat(hero)

    return True


def train_hero(hero):#only called during the beginning
    hero.abilities.append(abilities.Ability0())