import pygame
from random import choice
from buffs import *
from abilities import overhp_before_hp
from abilities import enemy_block_dodge
from abilities import enemy_mental_dodge


consumable_pool, consumable_pool_2, consumable_pool_3 = [], [], []
gear_pool, gear_pool_2, gear_pool_3 = [], [], []

def register(type='gear', act=1):

    def decorate(item):

        if type == 'item' and act == 1:
            consumable_pool.append(item)
        elif type == 'item' and act == 2:
            consumable_pool_2.append(item)
        elif type == 'item' and act == 3:
            consumable_pool_3.append(item)

        elif type == 'gear' and act == 1:
            gear_pool.append(item)
        elif type == 'gear' and act == 2:
            gear_pool_2.append(item)
        elif type == 'gear' and act == 3:
            gear_pool_3.append(item)

        return item
    
    #print(f'consumable_act1: {consumable_pool}')
    #print(f'consumable_act2: {consumable_pool_2}')
    #print(f'gear_act1: {gear_pool}')
    #print(f'gear_act2: {gear_pool_2}')

    return decorate


def random_item(stage):
    match stage:
        case 0 | 1 | 2:
            items = consumable_pool
        case 4 | 5:
            items = consumable_pool_2
        case 7 | 8:
            items = consumable_pool_3
    item = choice(items)
    return item()


def random_gear(stage):
    match stage:
        case 0 | 1 | 2:
            items = gear_pool
        case 4 | 5:
            items = gear_pool_2
        case 7 | 8:
            items = gear_pool_3
    item = choice(items)
    return item()


class Consumable:
    
    def __init__(self, name, power, charges, xp,
                  symbol, image):
        self.name = name
        self.power = power
        self.charges = charges
        self.xp = xp
        self.symbol = symbol
        self.image = image
        
        self.gear = False
        self.active = True
        self.dungeon = False
        self.passive_effekt = False
        self.after_combat_effekt = False

        self.execution_10 = False
        self.execution_15 = False
        self.execution_20 = False

        self.image = pygame.image.load(
            image)
        self.image =pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
    
    def __repr__(self):
        return self.name
    
    def __str__(self):
        return self.name
    
    def _append(self, hero):
        if len(hero.pockets) < hero.pocket_size:
            hero.pockets.append(self)
        else:
            hero.inventory.append(self)

    def _remove(self, hero):
        try:
            hero.pockets.remove(self)
        except ValueError:
            hero.inventory.remove(self)


class Gear:

    def __init__(self, name, power, xp, symbol, image):
        self.name = name
        self.power = power
        self.xp = xp
        self.symbol = symbol
        self.image = image

        self.gear = True
        self.active = False
        self.passive_effekt = False
        self.after_combat_effekt = False
        self.dungeon = False

        self.execution_10 = False
        self.execution_15 = False
        self.execution_20 = False
    
        self.image = pygame.image.load(
            image)
        self.image =pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

    def __repr__(self):
        return self.name
    
    def use_item(self, hero, enemy):
        print("placeholder")


#IMAGES LOADED, EVERY ITEM INSTANCE POITNS TO THESE
simple_health_potion = 'images/items/simple_health_potion.png'
simple_mana_potion = 'images/items/simple_mana_potion.png'
simple_fire_bomb = 'images/items/simple_fire_bomb.png'
moderate_health_potion = 'images/items/moderate_health_potion.png'
berserk_blood = 'images/items/berserk_blood.png'
moderate_fire_bomb = 'images/items/moderate_fire_bomb.png'
good_mana_potion = 'images/items/good_mana_potion.png'
#IMAGES LOADED, EVERY ITEM INSTANCE POITNS TO THESE


@register(type='item')
class Item1(Consumable):#HEILTRANK

    def __init__(self):
        super().__init__("EINFACHER HEILTRANK",
                        60, 1, 55,
                        '', simple_health_potion)
        self.dungeon = True

    def use_item(self, hero, enemy, combat_log):
        hero.life += self.power
        if hero.life >= hero.max_life:
            hero.life = hero.max_life
        self.charges -= 1
        if self.charges == 0:
            self._remove(hero)
        if combat_log != None:#For usage in dungeon
            text = "Du nimmst einen kräftigen Schluck"
            combat_log.add(text)
            text = f"+{self.power} HP"
            combat_log.add(text)


@register(type='item')
class Item2(Consumable):#ODEM-ESSENZ

    def __init__(self):
        super().__init__("EINFACHE ODEM-ESSENZ",
                        60, 1, 50,
                        '', simple_mana_potion)
        self.dungeon = True

    def use_item(self, hero, enemy, combat_log):
        hero.mana += self.power
        if hero.mana >= hero.max_mana:
            hero.mana = hero.max_mana
        self.charges -= 1
        if self.charges == 0:
            self._remove(hero)
        if combat_log != None:#for usage in dungeon
            text = "Die ODEM-ESSENZ erhöht deine Macht."
            combat_log.add(text)
            text = f"+{self.power} ODEM"
            combat_log.add(text)


@register(type='item')
class Item3(Consumable):#BRANDBOMBE

    def __init__(self):
        super().__init__("KLEINE BRANDBOMBE",
                          20, 1, 65, '', simple_fire_bomb)
        
    def use_item(self, hero, enemy, combat_log):
        block = (1 - enemy.reduction / 100)
        if block > 1:
            block = 1
        damage_taken1 = round(self.power*block)
        if damage_taken1 < 0:
            damage_taken1 = 0
        block = (1 - enemy.mental_reduction / 100)
        if block > 1:
            block = 1
        damage_taken2 = round(self.power*block)
        if damage_taken2 < 0:
            damage_taken2 = 0
        damage_taken = damage_taken1 + damage_taken2
        damage_taken = overhp_before_hp(enemy, damage_taken)
        enemy.life -= damage_taken
        if damage_taken >= 0:
            FireH2E(3, 2).buff(enemy)
        text = f"{enemy.name} erleidet {damage_taken} Schaden!"
        combat_log.add(text)
        self.charges -= 1
        if self.charges == 0:
            self._remove(hero)


@register(type='item', act=2)
@register(type='item')
class Item4(Consumable):#prakt. HEILTRANK

    def __init__(self):
        super().__init__("PRAKTISCHER HEILTRANK",
                          60, 2, 110, "", moderate_health_potion)
        self.dungeon = True
        self.update_symbol()

    def update_symbol(self):
        self.symbol = f"{self.charges}"

    def use_item(self, hero, enemy, combat_log):
        hero.life += self.power
        if hero.life >= hero.max_life:
            hero.life = hero.max_life
        self.charges -= 1
        self.update_symbol()
        if self.charges == 0:
            self._remove(hero)
        if combat_log != None:#For usage in dungeon
            text = "Du nimmst einen kräftigen Schluck"
            combat_log.add(text)
            text = f"+{self.power} HP"
            combat_log.add(text)
            text = f"{self.charges} Ladungen noch übrig."
            combat_log.add(text)


@register(type='item')
class Item5(Consumable):#BERSERKER BLUT
    item_name = "BERSERKER-BLUT" #needed for an event

    def __init__(self):
        super().__init__("BERSERKER-BLUT",
                        0, 1, 75, "", berserk_blood)
        
    def use_item(self, hero, enemy, combat_log):
        BerserkH2H(3, 10).buff(hero)
        text = f"Die Macht der Ahnen übermannt {hero.name}."
        combat_log.add(text)
        self.charges -= 1
        if self.charges == 0:
            self._remove(hero)


@register(type='item', act=2)
@register(type='item')
class Item6(Consumable):#verb. BRANDBOMBE

    def __init__(self):
        super().__init__("VERBESSERTE BRANDBOMBE",
                          21, 2, 110, '', moderate_fire_bomb)
        self.update_symbol()

    def update_symbol(self):
        self.symbol = f"{self.charges}"

    def use_item(self, hero, enemy, combat_log):
        block = (1 - enemy.reduction / 100)
        if block > 1:
            block = 1
        damage_taken1 = round(self.power * block)
        if damage_taken1 < 0:
            damage_taken1 = 0
        block = (1 - enemy.mental_reduction / 100)
        if block > 1:
            block = 1
        damage_taken2 = round(self.power * block)
        if damage_taken2 < 0:
            damage_taken2 = 0
        damage_taken = damage_taken1 + damage_taken2
        damage_taken = overhp_before_hp(enemy, damage_taken)
        enemy.life -= damage_taken
        if damage_taken >= 0:
            FireH2E(4, 3).buff(enemy)
        text = f"{enemy.name} erleidet {damage_taken} Schaden!"
        combat_log.add(text)
        self.charges -= 1
        self.update_symbol()
        if self.charges == 0:
            self._remove(hero)


@register(type='item', act=2)
@register(type='item')
class Item7(Consumable):#GUTE ODEM-ESSENZ

    def __init__(self):
        super().__init__("GUTE ODEM-ESSENZ",
                        45, 1, 110,
                        '', good_mana_potion)
        self.dungeon = True

    def use_item(self, hero, enemy, combat_log):
        hero.mana += self.power
        if combat_log == None:
            hero.mana += self.power
        if hero.mana > hero.max_mana:
            hero.mana = hero.max_mana
        if combat_log != None:
            text = "Die gute ODEM-ESSENZ sorgt für Klarheit."
            combat_log.add(text)
            text = f"+{self.power} ODEM"
            combat_log.add(text)
            ClarityH2H(16, 3).buff(hero)
        self.charges -= 1
        if self.charges == 0:
            self._remove(hero)


#IMAGES LOADED, EVERY ITEM INSTANCE POITNS TO THESE
short_sword = 'images/items/gear/short_sword.png'
long_sword = 'images/items/gear/long_sword.png'
shattered_runes = 'images/items/gear/shattered_runes.png'
simple_armor = 'images/items/gear/simple_armor.png'
boots = 'images/items/gear/boots.png'
simple_warmogs = 'images/items/gear/simple_warmogs.png'
mana_mantle = 'images/items/gear/mana_mantle.png'
#IMAGES LOADED, EVERY ITEM INSTANCE POITNS TO THESE
life_stone = 'images/items/gear/life_Stone.png'
khans_hat = 'images/items/gear/khans_hat.png'
elven_boots = 'images/items/gear/elven_boots.png'
ritual_dagger = 'images/items/gear/ritual_dagger.png'
soul_stealer = 'images/items/gear/soul_stealer.png'
old_pistole = 'images/items/gear/old_pistole.png'
moon_stone = 'images/items/gear/moon_stone.png'
#IMAGES LOADED, EVERY ITEM INSTANCE POITNS TO THESE


@register()
class ShortSword(Gear):

    def __init__(self):
        super().__init__("KURZSCHWERT",
                          15, 140, '', short_sword)
        
    def equip(self, hero):
        hero.inventory.append(self)
        hero.damage += self.power / 3
        hero.speed += self.power

    def unequip(self, hero):
        hero.speed -= self.power
        hero.damage -= self.power / 3
        hero.inventory.remove(self)


@register()
class LongSword(Gear):

    def __init__(self):
        super().__init__("LANGSCHWERT",
                          8, 140, '', long_sword)
        
    def equip(self, hero):
        hero.inventory.append(self)
        hero.damage += self.power

    def unequip(self, hero):
        hero.damage -= self.power
        hero.inventory.remove(self)


@register()
class ShatteredRunes(Gear):

    def __init__(self):
        super().__init__("VERWITTERTE RUNE",
                          10, 140, '', shattered_runes)
        
    def equip(self, hero):
        hero.inventory.append(self)
        hero.max_mana += self.power
        hero.mana += self.power
        hero.damage += round(self.power / 2)

    def unequip(self, hero):
        hero.damage -= round(self.power / 2)
        hero.max_mana -= self.power
        if hero.mana > hero.max_mana:
            hero.mana = hero.max_mana
        hero.inventory.remove(self)


@register()
class SimpleArmor(Gear):

    def __init__(self):
        super().__init__("LEDERHARNISCH",
                         7, 135, '', simple_armor)
        
    def equip(self, hero):
        hero.inventory.append(self)
        hero.reduction += self.power

    def unequip(self, hero):
        hero.reduction -= self.power
        hero.inventory.remove(self)


@register()
class Boots(Gear):
    def __init__(self):
        super().__init__("WANDERSTIEFEL",
                        34, 130, '', boots)
        
    def equip(self, hero):
        hero.inventory.append(self)
        hero.speed += self.power

    def unequip(self, hero):
        hero.speed -= self.power
        hero.inventory.remove(self)


@register()
class SimpleWarmogs(Gear):

    def __init__(self):
        super().__init__("Rüstung der Lebenskraft",
                          20, 138, '', simple_warmogs)
        
    def equip(self, hero):
        hero.inventory.append(self)
        hero.max_life += self.power
        hero.life += self.power

    def unequip(self, hero):
        hero.max_life -= self.power
        if hero.life > hero.max_life:
            hero.life = hero.max_life
        hero.inventory.remove(self)


@register()
class ManaMantle(Gear):

    def __init__(self):
        super().__init__("Mantel der Intelligenz",
                        25, 132, '', mana_mantle)
        
    def equip(self, hero):
        hero.inventory.append(self)
        hero.max_mana += self.power
        hero.mana += self.power

    def unequip(self, hero):
        hero.max_mana -= self.power
        if hero.mana > hero.max_mana:
            hero.mana = hero.max_mana
        hero.inventory.remove(self)


#^^^ UNDER 150 XP | obtainable from normal enemies ^^^


@register()
class LifeStone(Gear):

    def __init__(self):
        super().__init__("Stein des Lebens",
                         2, 200, '', life_stone)
        self.passive_effekt = True

    def equip(self, hero):
        hero.inventory.append(self)

    def unequip(self, hero):
        hero.inventory.remove(self)

    def trigger_passive(self, hero):
        hero.life += self.power
        if hero.life > hero.max_life:
            hero.life = hero.max_life


@register()
class KhansHat(Gear):

    def __init__(self):
        super().__init__("Helm des Eroberers", 
                        6, 190, '', khans_hat)
        
    def equip(self, hero):
        hero.inventory.append(self)
        hero.damage += self.power
        hero.critical += self.power

    def unequip(self, hero):
        hero.critical -= self.power
        hero.damage -= self.power
        hero.inventory.remove(self)


@register()
class ElvenBoots(Gear):

    def __init__(self):
        super().__init__("Elfen-Schuhe", 
                        10, 185, '', elven_boots)
        
    def equip(self, hero):
        hero.inventory.append(self)
        hero.dodge += self.power
        hero.speed += 3 * self.power

    def unequip(self, hero):
        hero.speed -= 3 * self.power
        hero.dodge -= self.power
        hero.inventory.append(self)


@register()
class RitualDagger(Gear):

    def __init__(self):
        super().__init__("Ritual-Dolch",
                         3, 185, '', ritual_dagger)
        self.execution_10 = True

    def equip(self, hero):
        hero.inventory.append(self)
        hero.damage += self.power

    def unequip(self, hero):
        hero.damage -= self.power
        hero.inventory.remove(self)


@register()
class SoulStealer(Gear):

    def __init__(self):
        super().__init__("Seelen-Dieb",
                        30, 165, '', soul_stealer)
        self.after_combat_effekt = True

    def equip(self, hero):
        hero.inventory.append(self)

    def unequip(self, hero):
        hero.inventory.remove(self)

    def after_combat(self, hero):
        if hero.life < self.power:
            hero.life = self.power
        if hero.mana < self.power:
            hero.mana = self.power


@register()
class OldPistole(Gear):

    def __init__(self):
        super().__init__("Alte Pistole",
                         14, 200, '', old_pistole)
        
    def equip(self, hero):
        hero.inventory.append(self)
        hero.damage += self.power
        hero.speed -= self.power * 2

    def unequip(self, hero):
        hero.speed += self.power * 2
        hero.damage -= self.power
        hero.inventory.remove(self)


@register()
class MoonStone(Gear):

    def __init__(self):
        super().__init__('Mondfragment',
                         15, 170, '', moon_stone)
        self.active = True
        self.after_combat_effekt = True

    def equip(self, hero):
        hero.inventory.append(self)
        hero.mental_reduction += self.power

    def unequip(self, hero):
        hero.mental_reduction -= self.power
        hero.inventory.remove(self)

    def use_item(self, hero, enemy, combat_log):
        text = f'{hero.name} ergreift den Stein und drückt ihn fest!'
        combat_log.add(text)
        self.active = False
        hero.mental_reduction -= self.power
        hero.mana += self.power * 3
        if hero.mana > hero.max_mana:
            hero.mana = hero.max_mana
        text = 'Der Stein hat seinen Schimmer temporär verloren.'
        combat_log.add(text)

    def after_combat(self, hero):
        if not self.active:
            hero.mental_reduction += self.power
            self.active = True


class MagicWand(Gear):
    pass#noch einzufügen


#IMAGES LOADED, EVERY ITEM INSTANCE POITNS TO THESE
smoke_bomb = 'images/items/smoke_bomb.png'
healing_salve = 'images/items/healing_salve.png'
#IMAGES LOADED, EVERY ITEM INSTANCE POITNS TO THESE


@register(type='item', act=1)
@register(type='item', act=2)
class SmokeBomb(Consumable):

    def __init__(self):
        super().__init__("Rauchbombe",
                        0, 1, 20,
                        '', smoke_bomb)
        
    def use_item(self, hero, enemy, combat_log):
        text = 'In einem Augenblick zündet und wirft'
        combat_log.add(text)
        text = f'{hero.name} eine Rauchbombe'
        combat_log.add(text)
        text = f'{hero.name} konnte erfolgreich entkommen'
        combat_log.add(text)
        self.charges -= 1
        if self.charges == 0:
            self._remove(hero)
        return 'escape'


@register(type='item', act=2)
class HealingSalve(Consumable):

    def __init__(self):
        super().__init__("Heilsalbe",
                        33, 2, 200,
                        '', healing_salve)
        self.update_symbol()

    def update_symbol(self):
        self.symbol = f"{self.charges}"

    def use_item(self, hero, enemy, combat_log):
        hero.life += self.power
        if combat_log == None:
            hero.life += self.power
        if hero.life >= hero.max_life:
            hero.life = hero.max_life
        if combat_log != None:
            RegenerationH2H(11, 10).buff(hero)
            text = "Du Salbe legt sich über die Haut"
            combat_log.add(text)
            text = "wie Honig über einen Apfel"
            combat_log.add(text)
        self.charges -= 1
        self.update_symbol()
        if self.charges == 0:
            self._remove(hero)


@register(type='item', act=2)
class HandyManaPotion(Consumable):#reused and altered for act 2
    
    def __init__(self):
        super().__init__("PRAKTISCHE ODEM-ESSENZ",
                        45, 2, 200,
                        '', good_mana_potion)#icon png from act 1
        self.dungeon = True
        self.update_symbol()

    def update_symbol(self):
        self.symbol = f"{self.charges}"

    def use_item(self, hero, enemy, combat_log):
        hero.mana += self.power
        if combat_log == None:
            hero.mana += self.power
        if hero.mana > hero.max_mana:
            hero.mana = hero.max_mana
        if combat_log != None:
            text = "Die gute ODEM-ESSENZ sorgt für Klarheit."
            combat_log.add(text)
            text = f"+{self.power} ODEM"
            combat_log.add(text)
            ClarityH2H(16, 3).buff(hero)
        self.charges -= 1
        self.update_symbol()
        if self.charges == 0:
            self._remove(hero)


#IMAGES LOADED, EVERY ITEM INSTANCE POITNS TO THESE
shuko_claws = 'images/items/gear/shuko_claws.png'
sobi_mask = 'images/items/gear/sobi_mask.png'
item_belt = 'images/items/gear/item_belt.png'
magi_robe = 'images/items/gear/magi_robe.png'
#IMAGES LOADED, EVERY ITEM INSTANCE POITNS TO THESE
back_pack = 'images/items/gear/back_pack.png'
war_bow = 'images/items/gear/war_bow.png'
shield = 'images/items/gear/shield.png'
#IMAGES LOADED, EVERY ITEM INSTANCE POITNS TO THESE


@register(act=2)
class ShukoClaws(Gear):

    def __init__(self):
        super().__init__("Shuko-Krallen", 
                        0, 400, '', shuko_claws)
        
    def equip(self, hero):
        self.power = round(hero.speed / 9)#Set power for Item
        hero.inventory.append(self)#only once by equiping
        hero.damage += self.power

    def unequip(self, hero):
        hero.damage -= self.power
        hero.inventory.remove(self)


@register(act=2)
class SobiMask(Gear):

    def __init__(self):
        super().__init__("Sobi-Maske",
                        8, 390, '', sobi_mask)
        
    def equip(self, hero):
        hero.inventory.append(self)
        hero.mental_reduction += self.power
        hero.dodge += self.power
        hero.max_life += self.power

    def unequip(self, hero):
        hero.max_life -= self.power
        if hero.life > hero.max_life:
            hero.life = hero.max_life
        hero.dodge -= self.power
        hero.mental_reduction -= self.power
        hero.inventory.remove(self)


@register(act=2)
class ItemBelt(Gear):

    def __init__(self):
        super().__init__('praktischer Gürtel',
                         5, 400, '', item_belt)
        self.extra_dodge = self.power
        self.extra_spd = self.power * 20

    def equip(self, hero):
        hero.inventory.append(self)
        hero.pocket_size += 1

    def unequip(self, hero):
        hero.pocket_size -= 1
        while not len(hero.pockets) <= hero.pocket_size:
            del hero.pockets[-1]
        hero.inventory.remove(self)


@register(act=2)
class MagiRobe(Gear):

    def __init__(self):
        super().__init__('Magier-Robe',
                         10, 420, '', magi_robe)
        
    def equip(self, hero):
        hero.inventory.append(self)
        hero.magic_power += self.power
        hero.mana += self.power * 4

    def unequip(self, hero):
        hero.mana -= self.power * 4
        hero.magic_power -= self.power
        hero.inventory.remove(self)


#^^^ UNDER 450 XP | obtainable from normal enemies ^^^
        

@register(act=2)
class BackPack(Gear):

    def __init__(self):
        super().__init__('RUCKSACK',
                        1, 580, '', back_pack)
        
    def equip(self, hero):
        hero.inventory.append(self)
        hero.pocket_size += 2

    def unequip(self, hero):
        hero.pocket_size -= 2
        while not len(hero.pockets) <= hero.pocket_size:
            del hero.pockets[-1]
        hero.inventory.remove(self)


@register(act=2)
class WarBow(Gear):

    def __init__(self):
        super().__init__('KRIEGSBOGEN',
                         4, 580, '', war_bow)
        self.spell_cost = 10
        self.active = True
        self.after_combat_effekt = True

        
    def equip(self, hero):
        hero.inventory.append(self)
        hero.damage += self.power * 2
        hero.critical += self.power

    def unequip(self, hero):
        hero.critical -= self.power
        hero.damage -= self.power * 2
        hero.inventory.remove(self)

    def use_item(self, hero, enemy, combat_log):
        if hero.mana >= self.spell_cost and self.active:
            text = f'{hero.name} spannt den den Bogen so weit er kann'
            combat_log.add(text)
            self.active = False
            text = f'Der Pfeil zischt mit Gewalt richtung {enemy.name}'
            combat_log.add(text)
            hero.damage *= 2
            enemy_block_dodge(hero, enemy, combat_log)
            hero.damage /= 2
            hero.mana - self.spell_cost * 4
            if hero.mana < 0:
                hero.mana = 0

    def after_combat(self, hero):
        if not self.active:
            self.active = True


@register(act=2)
class Shield(Gear):

    def __init__(self):
        super().__init__('WÄCHTERSCHILD',
                        10, 580, '', shield)
        self.extra_armor = self.power
        self.extra_shield = self.power
        
    def equip(self, hero):
        hero.inventory.append(self)

    def unequip(self, hero):
        hero.inventory.remove(self)