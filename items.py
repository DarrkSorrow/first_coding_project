import pygame
from random import choice
from buffs import *


def random_item():
    items = (Item1, Item2, Item3, Item4, Item5,
             Item6, Item7)
    item = choice(items)
    return item()


def random_gear():
    items = (ShortSword, LongSword, ShatteredRunes,
            SimpleArmor, Boots, SimpleWarmogs, ManaMantle,
            LifeStone, KhansHat, ElvenBoots, ShukoClaws,
            RitualDagger, SoulStealer)
    item = choice(items)
    return item()


#IMAGES LOADED, EVERY ITEM INSTANCE POITNS TO THESE
simple_health_potion = 'images/items/simple_health_potion.png'
simple_mana_potion = 'images/items/simple_mana_potion.png'
simple_fire_bomb = 'images/items/simple_fire_bomb.png'
moderate_health_potion = 'images/items/moderate_health_potion.png'
berserk_blood = 'images/items/berserk_blood.png'
moderate_fire_bomb = 'images/items/moderate_fire_bomb.png'
good_mana_potion = 'images/items/good_mana_potion.png'
#IMAGES LOADED, EVERY ITEM INSTANCE POITNS TO THESE


class Item:
    
    def __init__(self, name, power, charges, xp,
                  symbol, image):
        self.name = name
        self.power = power
        self.charges = charges
        self.xp = xp
        self.symbol = symbol
        self.image = image
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
    
    def equip(self, hero):
        hero.inventory.append(self)

    def unequip(self, hero):
        hero.inventory.remove(self)


class Item1(Item):#HEILTRANK
    def __init__(self):
        super().__init__("EINFACHER HEILTRANK",
                        60, 1, 50,
                        '', simple_health_potion)
        self.dungeon = True
    def use_item(self, hero, enemy, combat_log):
        hero.life += self.power
        if hero.life >= hero.max_life:
            hero.life = hero.max_life
        self.charges -= 1
        if self.charges == 0:
            hero.inventory.remove(self)
        if combat_log != None:#For usage in dungeon
            text = "Du nimmst einen kräftigen Schluck"
            combat_log.add(text)
            text = f"+{self.power} HP"
            combat_log.add(text)


class Item2(Item):#ODEM-ESSENZ
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
            hero.inventory.remove(self)
        if combat_log != None:#for usage in dungeon
            text = "Die ODEM-ESSENZ erhöht deine Macht."
            combat_log.add(text)
            text = f"+{self.power} ODEM"
            combat_log.add(text)


class Item3(Item):#BRANDBOMBE
    def __init__(self):
        super().__init__("KLEINE BRANDBOMBE",
                          20, 1, 55, '', simple_fire_bomb)
    def use_item(self, hero, enemy, combat_log):
        block = (1 - enemy.reduction / 100)
        damage_taken1 = round(self.power*block)
        if damage_taken1 < 0:
            damage_taken1 = 0
        enemy.life -= damage_taken1
        block = (1 - enemy.mental_reduction / 100)
        damage_taken2 = round(self.power*block)
        if damage_taken2 < 0:
            damage_taken2 = 0
        enemy.life -= damage_taken2
        damage_taken = damage_taken1 + damage_taken2
        if damage_taken >= 0:
            ItemBuff2(3, 2).buff(enemy)
        text = f"{enemy.name} erleidet {damage_taken} Schaden!"
        combat_log.add(text)
        self.charges -= 1
        if self.charges == 0:
            hero.inventory.remove(self)


class Item4(Item):#prakt. HEILTRANK
    def __init__(self):
        super().__init__("PRAKTISCHER HEILTRANK",
                          50, 2, 85, "", moderate_health_potion)
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
            hero.inventory.remove(self)
        if combat_log != None:#For usage in dungeon
            text = "Du nimmst einen kräftigen Schluck"
            combat_log.add(text)
            text = f"+{self.power} HP"
            combat_log.add(text)
            text = f"{self.charges} Ladungen noch übrig."
            combat_log.add(text)


class Item5(Item):#BERSERKER BLUT
    item_name = "BERSERKER-BLUT" #needed for an event
    def __init__(self):
        super().__init__("BERSERKER-BLUT",
                        0, 1, 100, "", berserk_blood)
    def use_item(self, hero, enemy, combat_log):
        ItemBuff1(2, 10).buff(hero)
        text = f"Die Macht der Ahnen übermannt {hero.name}."
        combat_log.add(text)
        self.charges -= 1
        if self.charges == 0:
            hero.inventory.remove(self)


class Item6(Item):#verb. BRANDBOMBE
    def __init__(self):
        super().__init__("VERBESSERTE BRANDBOMBE",
                          20, 2, 100, '', moderate_fire_bomb)
        self.update_symbol()
    def update_symbol(self):
        self.symbol = f"{self.charges}"
    def use_item(self, hero, enemy, combat_log):
        block = (1 - enemy.reduction / 100)
        damage_taken1 = round(self.power * block)
        if damage_taken1 < 0:
            damage_taken1 = 0
        enemy.life -= damage_taken1
        block = (1 - enemy.mental_reduction / 100)
        damage_taken2 = round(self.power * block)
        if damage_taken2 < 0:
            damage_taken2 = 0
        enemy.life -= damage_taken2
        damage_taken = damage_taken1 + damage_taken2
        if damage_taken >= 0:
            ItemBuff2(4, 3).buff(enemy)
        text = f"{enemy.name} erleidet {damage_taken} Schaden!"
        combat_log.add(text)
        self.charges -= 1
        self.update_symbol()
        if self.charges == 0:
            hero.inventory.remove(self)


class Item7(Item):#GUTE ODEM-ESSENZ
    def __init__(self):
        super().__init__("GUTE ODEM-ESSENZ",
                        45, 1, 85,
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
            ItemBuff3(16, 3).buff(hero)
        self.charges -= 1
        if self.charges == 0:
            hero.inventory.remove(self)
    

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
shuko_claws = 'images/items/gear/shuko_claws.png'
ritual_dagger = 'images/items/gear/ritual_dagger.png'
soul_stealer = 'images/items/gear/soul_stealer.png'
#IMAGES LOADED, EVERY ITEM INSTANCE POITNS TO THESE


class Gear:
    def __init__(self, name, power, xp, symbol, image):
        self.name = name
        self.power = power
        self.xp = xp
        self.symbol = symbol
        self.image = image

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


class ShortSword(Gear):
    def __init__(self):
        super().__init__("KURZSCHWERT",
                          15, 144, '', short_sword)
    def equip(self, hero):
        hero.inventory.append(self)
        hero.damage += self.power / 3
        hero.speed += self.power
    def unequip(self, hero):
        hero.speed -= self.power
        hero.damage -= self.power / 3
        hero.inventory.remove(self)


class LongSword(Gear):
    def __init__(self):
        super().__init__("LANGSCHWERT",
                          8, 144, '', long_sword)
    def equip(self, hero):
        hero.inventory.append(self)
        hero.damage += self.power
    def unequip(self, hero):
        hero.damage -= self.power
        hero.inventory.remove(self)


class ShatteredRunes(Gear):
    def __init__(self):
        super().__init__("VERWITTERTE RUNE",
                          10, 144, '', shattered_runes)
    def equip(self, hero):
        hero.inventory.append(self)
        hero.max_mana += self.power
        hero.damage += round(self.power / 2)
    def unequip(self, hero):
        hero.damage -= round(self.power / 2)
        hero.max_mana -= self.power
        if hero.mana > hero.max_mana:
            hero.mana = hero.max_mana
        hero.inventory.remove(self)


class SimpleArmor(Gear):
    def __init__(self):
        super().__init__("LEDERHARNISCH",
                         7, 138, '', simple_armor)
    def equip(self, hero):
        hero.inventory.append(self)
        hero.reduction += self.power
    def unequip(self, hero):
        hero.reduction -= self.power
        hero.inventory.remove(self)


class Boots(Gear):
    def __init__(self):
        super().__init__("WANDERSTIEFEL",
                        34, 138, '', boots)
    def equip(self, hero):
        hero.inventory.append(self)
        hero.speed += self.power
    def unequip(self, hero):
        hero.speed -= self.power
        hero.inventory.remove(self)


class SimpleWarmogs(Gear):
    def __init__(self):
        super().__init__("Rüstung der Lebenskraft",
                          20, 138, '', simple_warmogs)
    def equip(self, hero):
        hero.inventory.append(self)
        hero.max_life += self.power
    def unequip(self, hero):
        hero.max_life -= self.power
        if hero.life > hero.max_life:
            hero.life = hero.max_life
        hero.inventory.remove(self)


class ManaMantle(Gear):
    def __init__(self):
        super().__init__("Mantel der Intelligenz",
                        25, 138, '', mana_mantle)
    def equip(self, hero):
        hero.inventory.append(self)
        hero.max_mana += self.power
    def unequip(self, hero):
        hero.max_mana -= self.power
        if hero.mana > hero.max_mana:
            hero.mana = hero.max_mana
        hero.inventory.remove(self)


#^^^ UNDER 150 XP | obtainable from normal enemies ^^^


class LifeStone(Gear):
    def __init__(self):
        super().__init__("Stein des Lebens",
                         2, 210, '', life_stone)
        self.passive_effekt = True
    def equip(self, hero):
        hero.inventory.append(self)
    def unequip(self, hero):
        hero.inventory.remove(self)
    def trigger_passive(self, hero):
        hero.life += self.power
        if hero.life > hero.max_life:
            hero.life = hero.max_life


class KhansHat(Gear):
    def __init__(self):
        super().__init__("Mönchs-Stirnband", 
                        4, 195, '', khans_hat)
    def equip(self, hero):
        hero.inventory.append(self)
        hero.damage += self.power
        hero.critical += self.power
    def unequip(self, hero):
        hero.critical -= self.power
        hero.damage -= self.power
        hero.inventory.remove(self)


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


class ShukoClaws(Gear):
    def __init__(self):
        super().__init__("Shuko-Krallen", 
                        0, 180, '', shuko_claws)
    def equip(self, hero):
        self.power = round(hero.speed / 10)#Set power for Item
        hero.inventory.append(self)#only once by equiping
        hero.damage += self.power
    def unequip(self, hero):
        hero.damage -= self.power
        hero.inventory.remove(self)


class RitualDagger(Gear):
    def __init__(self):
        super().__init__("Ritual-Dolch",
                         2, 188, '', ritual_dagger)
        self.execution_10 = True
    def equip(self, hero):
        hero.inventory.append(self)
        hero.damage += self.power
    def unequip(self, hero):
        hero.damage -= self.power
        hero.inventory.remove(self)


class SoulStealer(Gear):
    def __init__(self):
        super().__init__("Seelen-Dieb",
                        30, 200, '', soul_stealer)
        self.after_combat_effekt = True
    def equip(self, hero):
        hero.inventory.append(self)
    def unequip(self, hero):
        hero.inventory.remove(self)
    def after_combat(self, hero):
        if hero.mana < self.power:
            hero.mana = self.power