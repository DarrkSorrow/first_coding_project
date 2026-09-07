import sys, pygame
from collections import deque
from random import randint
import world, combat, events, buttons_clog


class GameState:

    def __init__(self):
        self.enemy_counter = 0
        self.last_enemy = None
        self.events_in_row = 0
        self.last_events = deque(maxlen=3)
        self.forgotten_abilities = []
        self.last_refused_abilities = deque(maxlen=3)


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
        self.accuracy = 0
        self.mana, self.max_mana = 0, 100
        self.xp = 0

        self.max_inventory, self.max_abilities = 4, 2
        self.inventory, self.abilities = [], []
        self.pocket_size, self.pockets = 0, []
        self.over_hp = 0
        self.buffs = []
    

    def defend(self, combat_log):
        self.dodge += 15
        self.reduction += 30
        self.mana += 15
        if self.mana >= self.max_mana:
            self.mana = self.max_mana
        self.over_hp += 10
        text = "ZERTUS geht in Verteidigungsstellung!"
        combat_log.add(text)


    def instant_defend(self):
        self.speed += 600


    def undo_defend(self):
        self.speed -= 600
        self.reduction -= 30
        self.dodge -= 15


    def instant_item(self, combat_log):
        active_items = []
        for item in self.inventory:
            if item.active:
                active_items.append(item)
        if active_items == []:
            text = ("Du hast doch garnichts.")
            combat_log.add(text)
            self.dodge += 15
            self.speed += 300
        else:
            self.dodge += 15
            self.speed += 300
            text = (f"{self.name} versucht blitzschnell in seine Tasche zu greifen!")
            combat_log.add(text)


    def undo_instant_item(self):
        self.dodge -= 15
        self.speed -= 300


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
        self.mana = int(self.max_life / 2)


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

stage = 0
dungeon = world.generate_world(stage)
hero = Adventurer()
world.arm_hero(hero)
combat.train_hero(hero)
position = [0, 0]

while hero.life > 0:

    screen.fill((40, 20, 20))
    draw_map(position, dungeon, screen)
    combat.hero_health_bar(hero, screen)
    combat.hero_mana_bar(hero, screen)
    combat.hero_combat_stats(hero, screen)
    world.hero_xp(hero, screen)
    buttons = buttons_clog.dungeon_inventory(hero, screen)
    buttons_clog.abilities_displayed(hero, screen)
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            position = world.movement(hero, dungeon, position, event)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            buttons_clog.dungeon_buttons_clicked(hero, buttons, screen, event)
        
    hero.inventory = sort_inventory(hero)


    #*** EVENTS ***
    if dungeon[position[0]][position[1]].event == True:
        ambush = events.start_event(hero, stage, screen)
        if not ambush and hero.life > 0:
            dungeon[position[0]][position[1]] = world.EmptyRoom()
        elif ambush:
            dungeon[position[0]][position[1]].fight = True
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


    #*** NORMAL FIGHT ***
    if dungeon[position[0]][position[1]].fight == True:
# this random if is needed
        
        #*** SURPRISE ELITE ***
        if hero.game_state.enemy_counter <= 1:
            pass

        elif hero.game_state.enemy_counter == 2:
            magic_number = randint(0, 10)
            if magic_number <= 1: # Small chance
                combat.start_elite(hero, stage, screen)
                if hero.life > 0:
                    enemy = 2 # elite Gegner
                    world.reward(hero, enemy, stage, screen)
                    dungeon[position[0]][position[1]] = world.EmptyRoom()

        elif hero.game_state.enemy_counter >= 3:
            magic_number = randint(0, 10)
            if magic_number <= 5: # Big chance
                combat.start_elite(hero, stage, screen)
                if hero.life > 0:
                    enemy = 2 # elite Gegner
                    world.reward(hero, enemy, stage, screen)
                    dungeon[position[0]][position[1]] = world.EmptyRoom()
        #*** SURPRISE ELITE ***

        if dungeon[position[0]][position[1]].fight == True:
            combat.start_fight(hero, stage, screen)
            if hero.life > 0:
                enemy = 1 # normaler Gegner
                world.reward(hero, enemy, stage, screen)
                dungeon[position[0]][position[1]] = world.EmptyRoom()
    #*** NORMAL FIGHT ***


    #*** ELITE FIGHT ***
    elif dungeon[position[0]][position[1]].elite == True:
        combat.start_elite(hero, stage, screen)
        if hero.life > 0:
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
    pygame.display.flip()