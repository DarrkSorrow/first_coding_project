import sys
from dataclasses import dataclass, field
from collections import deque
from random import randint
import world, combat, events, buttons_clog
import pygame


@dataclass(slots=True)#Fancy new class definition
class GameState: #just for education purposes
    enemy_counter: int = 0
    last_enemy: object = None
    events_in_row: int = 0
    last_events: deque = field(default_factory=lambda: deque(maxlen=3))
    forgotten_abilities: list = field(default_factory=list)
    last_refused_abilities: deque = field(default_factory=lambda: deque(maxlen=3))


class Hero:

    def __init__(self, name):

        self.game_state = GameState()

        self.name = name
        self.life, self.max_life = 100, 100
        self.reduction, self.dodge = 0, 0 #Percent
        self.mental_reduction = 0 #percent
        self.damage = 15
        self.speed = 50
        self.critical = 0
        self.magic_power = 0
        self.accuracy = 0
        self.mana, self.max_mana = 50, 100
        self.xp = 0

        self.max_inventory, self.max_abilities = 4, 2
        self.inventory, self.abilities = [], []
        self.pocket_size, self.pockets = 0, []
        self.over_hp = 0
        self.buffs = []


    def _items_improve_defend(self):

        armor, shield, mental, mana_gain, evasion, spd = 0, 0, 0, 0, 0, 0
        
        for item in self.inventory:

            try:
                armor += item.extra_armor
            except AttributeError:
                pass
            try:
                shield += item.extra_shield
            except AttributeError:
                pass
            try:
                mental += item.extra_mental
            except AttributeError:
                pass
            try:
                mana_gain += item.extra_mana
            except AttributeError:
                pass
            try:
                evasion += item.extra_dodge
            except AttributeError:
                pass
            try:
                spd += item.extra_spd
            except AttributeError:
                pass

        return armor, shield, mental, mana_gain, evasion, spd


    def defend(self, combat_log):
        stats = self._items_improve_defend()
        armor, shield, mental, mana_gain, evasion, spd = stats
        self.dodge += 15 + evasion
        self.reduction += 20 + armor
        self.mental_reduction += 0 + mental
        self.mana += 10 + mana_gain
        if self.mana >= self.max_mana:
            self.mana = self.max_mana
        self.over_hp += 10 + shield
        text = "ZERTUS geht in Verteidigungsstellung!"
        combat_log.add(text)


    def instant_defend(self):
        stats = self._items_improve_defend()
        armor, shield, mental, mana_gain, evasion, spd = stats
        self.speed += 600 + spd


    def undo_defend(self):
        stats = self._items_improve_defend()
        armor, shield, mental, mana_gain, evasion, spd = stats
        self.speed -= 600 + spd
        self.reduction -= 20 + armor
        self.mental_reduction -= 0 + mental
        self.dodge -= 15 + evasion


    def _items_improve_itemuse(self):
        
        armor, mental, evasion, spd = 0, 0, 0, 0
        
        for item in self.inventory:

            try:
                armor += item.extra_armor
            except AttributeError:
                pass
            try:
                mental += item.extra_mental
            except AttributeError:
                pass
            try:
                evasion += item.extra_dodge
            except AttributeError:
                pass
            try:
                spd += item.extra_spd
            except AttributeError:
                pass

        return armor, mental, evasion, spd


    def instant_item(self, combat_log):
        stats = self._items_improve_itemuse()
        armor, mental, evasion, spd = stats
        active_items = []
        for item in self.inventory:
            if item.active:
                active_items.append(item)
        if active_items == [] and self.pockets == []:
            text = ("Du hast doch garnichts.")
            combat_log.add(text)
            self.speed += 300 + spd
        else:
            self.speed += 300 + spd
            text = (f"{self.name} versucht blitzschnell in seine Tasche zu greifen!")
            combat_log.add(text)


    def item_use(self):
        stats = self._items_improve_itemuse()
        armor, mental, evasion, spd = stats
        self.dodge += 15 + evasion


    def undo_instant_item(self):
        stats = self._items_improve_itemuse()
        armor, mental, evasion, spd = stats
        self.dodge -= 15 + evasion
        self.speed -= 300 + spd


    def decay_over_hp(self):
        if self.over_hp == 1:
            self.over_hp = 0
        else:
            self.over_hp = round(self.over_hp * 0.7)


    def stunned_or_not(self):
        magic_number = randint(0, 100)
        for buff in self.buffs:
            if buff.stun and buff.power >= magic_number:
                return True


class Adventurer(Hero):

    def __init__(self):
        super().__init__("ZERTUS")
        self.max_mana = 200
        self.mental_resistance = 10
        self.mana = int(self.max_mana / 2)
        self.life = 60
        self.max_inventory = 4
        self.xp = 450


def draw_map(position, dungeon, screen):
    
    for i, x in enumerate(dungeon):
        for j, y in enumerate(x):
            
            inside = (i == position[0] and j == position[1])
            
            pygame.draw.rect(
                screen,
                y.get_color(inside),
                (350 + j*70, 160 + i*70, 70, 70))

            if y.image is not None:
                screen.blit(y.image, (350 + j*70, 160 + i*70, 70, 70))


def sort_inventory(hero):

    active = []
    inactive = []

    for item in hero.inventory:
        if item.active:
            active.append(item)
        else:
            inactive.append(item)

    hero.inventory = active + inactive
    return hero.inventory


pygame.init()

screen = pygame.display.set_mode((1200,800))
pygame.display.set_caption("Dungeon")
clock = pygame.time.Clock()

stage = 4
dungeon = world.generate_world(stage)
hero = Adventurer()
world.arm_hero(hero)
combat.train_hero(hero)
position = [0, 0]

while hero.life > 0:

    screen.fill((40, 20, 20))
    draw_map(position, dungeon, screen)
    combat.hero_interface(hero, screen)
    buttons = buttons_clog.dungeon_inventory(hero, screen)
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            position = world.movement(dungeon, position, event)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            buttons_clog.dungeon_buttons_clicked(hero, buttons, screen, event)
        
    hero.inventory = sort_inventory(hero)

    #*** HIDDEN-RANDOM ***
    if dungeon[position[0]][position[1]].random == True:
        magic_number =randint(0, 100)
        match magic_number:
            case magic_number if magic_number in (0, 40):
                dungeon[position[0]][position[1]] = world.EmptyRoom()
            case magic_number if magic_number in (41, 60):
                dungeon[position[0]][position[1]].fight = True
            case magic_number if magic_number in (61, 80):
                dungeon[position[0]][position[1]].event = True
            case magic_number if magic_number in (81, 100):
                dungeon[position[0]][position[1]] = world.EmptyRoom()
                pass#will contain traps in act=3
    #*** HIDDEN-RANDOM ***

    #*** EVENTS ***
    if dungeon[position[0]][position[1]].event == True:
        ambush = events.start_event(hero, stage, screen)
        if not ambush and hero.life > 0:
            dungeon[position[0]][position[1]] = world.EmptyRoom()
        elif ambush == True:#== True does make a difference
            dungeon[position[0]][position[1]].fight = True
        elif ambush == 'merchant':
            dungeon[position[0]][position[1]].merchant = True
    #*** EVENTS ***        

    #*** BONDFIRE ***
    elif dungeon[position[0]][position[1]].rest == True:
        world.bond_fire(hero, stage, screen)
        dungeon[position[0]][position[1]] = world.EmptyRoom()
    #*** BONDFIRE ***

    #*** TELEPORT ***
    elif dungeon[position[0]][position[1]].warp == True:
        stage += 1
        position = [0, 0]
        dungeon = world.generate_world(stage)
    #*** TELEPORT ***

    #*** MERCHANT ***
    if dungeon[position[0]][position[1]].merchant == True:
        world.wandering_merchant(hero, stage, screen)
        dungeon[position[0]][position[1]] = world.EmptyRoom()
    #*** MERCHANT ***

    #*** NORMAL FIGHT ***
    if dungeon[position[0]][position[1]].fight == True:
        
            #*** SURPRISE ELITE ***
        magic_number = randint(hero.game_state.enemy_counter, 10)
        magic_number += hero.game_state.enemy_counter
        if magic_number >= 12:
            enemy_defeated = combat.start_elite(hero, stage, screen)
            if hero.life > 0 and enemy_defeated:
                enemy = 2 # elite enemies
                world.reward(hero, enemy, stage, screen)
            dungeon[position[0]][position[1]] = world.EmptyRoom()
            #*** SURPRISE ELITE ***

        elif dungeon[position[0]][position[1]].fight == True:
            if hero.life > 0:
                enemy_defeated = combat.start_fight(hero, stage, screen)
            if hero.life > 0 and enemy_defeated:
                enemy = 1 # normal enemies
                world.reward(hero, enemy, stage, screen)
            dungeon[position[0]][position[1]] = world.EmptyRoom()
    #*** NORMAL FIGHT ***

    #*** ELITE FIGHT ***
    elif dungeon[position[0]][position[1]].elite == True:
        enemy_defeated = combat.start_elite(hero, stage, screen)
        if hero.life > 0 and enemy_defeated:
            enemy = 2 # elite Gegner
            world.reward(hero, enemy, stage, screen)
        dungeon[position[0]][position[1]] = world.EmptyRoom()
    #*** ELITE FIGHT ***

    #*** BOSS FIGHT ***
    elif dungeon[position[0]][position[1]].boss == True:
        combat.start_boss(hero, stage, screen)
        if hero.life > 0:
            enemy = 3 # Boss Gegner
            world.reward(hero, enemy, stage, screen)
            stage += 1 #WARP
            position = [0, 0]
            dungeon = world.generate_world(stage)
    #*** BOSS FIGHT ***

    clock.tick(30)
    #HI_d89cf752-cf12-43e1-9eeb-a5ea7abc3b0a
    pygame.display.flip()