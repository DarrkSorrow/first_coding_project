import pygame
import random
from time import sleep
from buffs import *
import buttons_clog 


spells = []

def register(ability):
    spells.append(ability)
    return ability


def random_abilities(hero):

    canditates = []
    
    for spell in spells: 
        already_known = False
        recently_refused = False #deque(maxlen=3)
        already_forgotten = False

        for ability in hero.abilities:
            if isinstance(ability, spell):
                already_known = True
                break

        for ability in hero.game_state.last_refused_abilities:
            if ability is spell: 
                recently_refused = True
                break

        for ability in hero.game_state.forgotten_abilities:
            if isinstance(ability, spell):
                already_forgotten = True
                break

        if not already_known and not recently_refused and not already_forgotten:
            canditates.append(spell)
            
    return canditates


def learn_ability(hero, screen):
    
    font = pygame.font.SysFont(None, 28)
    screen.fill((50, 50, 50)), pygame.display.flip()

    canditates = random_abilities(hero)
    
    if len(canditates) != 0:
        spell = random.choice(canditates)
        instance = spell()

    if instance.xp <= hero.xp:
        y = 100

        if len(hero.abilities) < hero.max_abilities:#same
            pass
        else:
            text = f"Willst du {instance.name} lernen?"
            y = buttons_clog.display_text(text, y, screen, font)
            buttons = buttons_clog.yes_no_button(screen, font)
            answer = buttons_clog.display_answers_clicked(buttons)

            if answer == "1":
                if len(hero.abilities) == hero.max_abilities:
                    forget_ability(hero, screen)

            elif answer == "2":
                text = f"{hero.name} verwirft {instance.name}"
                y = buttons_clog.display_text(text, y, screen, font)
                hero.game_state.last_refused_abilities.append(spell) #hero.game_state

        if len(hero.abilities) < hero.max_abilities:#same
            hero.abilities.append(instance)
            hero.xp -= instance.xp
            text = f"{hero.name} hat {instance.name} gelernt!"
            y = buttons_clog.display_text(text, y, screen, font)


def forget_ability(hero, screen):

    font = pygame.font.SysFont(None, 28)
    screen.fill((50, 50, 50))
    y = 100
    pygame.display.flip(), sleep(1)
    text = f"{hero.name} kann derzeit nur "
    text += f"{hero.max_abilities} Fähigkeiten lernen."
    y = buttons_clog.display_text(text, y, screen, font)
    text = "Eine Fähigkeit vergessen?"
    y = buttons_clog.display_text(text, y, screen, font)
    buttons = buttons_clog.yes_no_button(screen, font)
    pygame.display.flip()
    choice = buttons_clog.display_answers_clicked(buttons)
    screen.fill((50, 50, 50)), pygame.display.flip()
   
    match choice:

        case '1':
            choice = buttons_clog.choose_ability(hero, " ", screen)   
            match choice:
                
                case "a":
                    hero.game_state.forgotten_abilities.append(hero.abilities[0])
                    del hero.abilities[0]

                case "b":
                    hero.game_state.forgotten_abilities.append(hero.abilities[1])
                    del hero.abilities[1]

                case "c":
                    hero.game_state.forgotten_abilities.append(hero.abilities[2])
                    del hero.abilities[2]

                case "d":
                    hero.game_state.forgotten_abilities.append(hero.abilities[3])
                    del hero.abilities[3]                  
        case '2':
            return None
    

def abilities_from_events(hero, ability, screen):

    font = pygame.font.SysFont(None, 28)
    screen.fill((50, 50, 50)), pygame.display.flip()
    y = 100

    if len(hero.abilities) < hero.max_abilities:
        hero.abilities.append(ability)

    elif len(hero.abilities) == hero.max_abilities:
        text = f"{hero.name} kann {ability.name} nicht lernen."
        y = buttons_clog.display_text(text, y, screen, font)
        forget_ability(hero, screen)
        hero.abilities.append(ability)

    text = f"{hero.name} hat {ability.name} gelernt!"
    y = buttons_clog.display_text(text, y, screen, font)


def enemy_block_dodge(hero, enemy, combat_log):
#Verteidigungsmöglichkeit der Gegner + crit
    magic_number = random.randint(0, 100)
    magic_number += hero.accuracy
    if magic_number < enemy.dodge:
        text = f"{enemy.name} konnte ausweichen!!!"
        combat_log.add(text, True)
        damage_taken = 0
        return damage_taken
    else:
        block = (1 - enemy.reduction / 100)
        if block > 1:
            block = 1
        crit_factor = hero_critical_hit(hero, combat_log)
        damage_taken = round(hero.damage * crit_factor * block)
        if damage_taken < 0:
            damage_taken = 0
        damage_taken = overhp_before_hp(enemy, damage_taken)
        enemy.life -= damage_taken
        execution_x(hero, enemy, combat_log)#Checks instakill
        text = f"{enemy.name} erleidet {damage_taken} Schaden!"
        combat_log.add(text)
        return damage_taken


def overhp_before_hp(enemy, damage_taken):
    """Depleet enemy shield_hp before real HP"""
    damage_taken -= enemy.over_hp
    if damage_taken >= 0:
        enemy.over_hp = 0
    else: #when damage_taken negative -> then over_hp > 0
        enemy.over_hp = abs(damage_taken)
        damage_taken = 0
    return damage_taken


def execution_x(hero, enemy, combat_log):
    """Checks if item grants execution and if it applies"""   
    execution_10 = False
    execution_15 = False
    execution_20 = False

    for item in hero.inventory:
        if item.execution_20 == True:
            execution_20 = True
            break #if 20 = True, nothing else matters
        elif item.execution_15 == True:
            execution_15 = True
        elif item.execution_10 == True:
            execution_10 = True
        
    if execution_20:
        if enemy.life < enemy.max_life * 0.2:
            enemy.life = 0
    elif execution_15:
        if enemy.life < enemy.max_life * 0.15:
            enemy.life = 0
    elif execution_10:
        if enemy.life < enemy.max_life * 0.1:
            enemy.life = 0
    else:
        return None

    if enemy.life == 0:
        text = f"{enemy.name} wurde exekutiert!!"
        combat_log.add(text)


def hero_critical_hit(hero, combat_log):
    """Determines if attack was critical"""
    magic_number = random.randint(0, 100)
    if magic_number < hero.critical:
        text = "KRITISCHER TREFFER!!"
        combat_log.add(text)
        crit_factor = 1.5
    else:
        crit_factor = 1
    return crit_factor


def enemy_mental_dodge(ability, enemy, combat_log):
#Verteidigungsmöglichkeit der Gegner
    magic_number = random.randint(0, 150)
    if magic_number < enemy.dodge:
        text = f"{enemy.name} konnte dem ZAUBER ausweichen!!!"
        combat_log.add(text, True)
        damage_taken = 0
        return damage_taken
    else:
        block = (1 - enemy.mental_reduction / 100)
        if block > 1:
            block = 1
        damage_taken = round(ability * block)
        if damage_taken < 0:
            damage_taken = 0
        damage_taken = overhp_before_hp(enemy, damage_taken)
        enemy.life -= damage_taken
        text = f"{enemy.name} erleidet {damage_taken} Zauberschaden!"
        combat_log.add(text)
        return damage_taken


class Ability:

    def __init__(self, name, power, cost, xp, image, cool_down = 0):
        self.name = name
        self.power = power
        self.cost = cost
        self.xp = xp
        self.cool_down = cool_down
        self.image = image

        self.image = pygame.image.load(image)
        self.image =pygame.transform.scale(self.image, (65, 65))
        self.rect = self.image.get_rect()
    
    def __repr__(self):
        return self.name

    def _cost_and_cooldown(self, hero, mana_cost, cooldown=0, life_cost=0):
        hero.life -= life_cost
        hero.mana -= mana_cost
        self.cool_down += cooldown

    def draw(self, screen, x, y):
        if self.image is not None:
            screen.blit(self.image, (x, y))
    
    def reduce_cool_down(self):
        if self.cool_down > 0:
            self.cool_down -= 1

    def undo_ability(self, hero, enemy):
        pass
        
#IMAGES LOADED, EVERY ABILITY INSTANCE POITNS TO THESE
starting_ability = 'images/abilities/starting_ability.png'
heavy_strike = 'images/abilities/heavy_strike.png'
crippling_strike = 'images/abilities/crippling_strike.png'
precise_hit = 'images/abilities/precise_hit.png'
fire_ball = 'images/abilities/fire_ball.png'
magical_strike = 'images/abilities/magical_strike.png'
mord_hau = 'images/abilities/mord_hau.png'
poison_dart = 'images/abilities/poison_dart.png'
harden = 'images/abilities/harden.png'
simple_heal = 'images/abilities/simple_heal.png'
frost_arrow = 'images/abilities/frost_arrow.png'
#IMAGES LOADED, EVERY ABILITY INSTANCE POITNS TO THESE


class Ability0(Ability):#STARTFÄHIGKEIT

    def __init__(self):
        super().__init__("WAPPNEN", 5, 25, 0, 
                        starting_ability)
        
    def use_ability(self, hero, enemy, combat_log):
        if hero.mana >= self.cost:
            text = f"{hero.name} wappnet sich."
            combat_log.add(text)

            hero.reduction += self.power * 2 #UNDO
            EmpoweredH2H(10, 4).buff(hero)
            enemy_mental_dodge(self.power, enemy, combat_log)

            self._cost_and_cooldown(hero, self.cost)
            return True
        else:
            text = "Dir fehlt die Stergge die es braucht."
            combat_log.add(text)
            return False
        
    def undo_ability(self, hero, enemy):
        hero.reduction -= self.power * 2


@register
class Ability1(Ability):#SCHWERER HIEB

    def __init__(self):
        super().__init__("SCHWERER HIEB", 19, 19, 250,
                        heavy_strike)
        
    def use_ability(self, hero, enemy, combat_log):
        if hero.mana >= self.cost:
            text = f"{hero.name} schlägt mit aller Kraft zu!"
            combat_log.add(text)

            hero.damage += self.power
            enemy_block_dodge(hero, enemy, combat_log)
            hero.damage -= self.power

            self._cost_and_cooldown(hero, self.cost)
            return True
        else:
            text = "Deine Beine verkrampfen."
            combat_log.add(text)
            return False


@register
class Ability2(Ability):# VERKRÜPPELNDER HIEB

    def __init__(self):
        super().__init__("VERKRÜPPELNDER HIEB", 9, 23, 250,
                        crippling_strike)
        
    def use_ability(self, hero, enemy, combat_log):
        if self.cool_down == 0:
            if hero.mana >= self.cost:
                text = f"{hero.name} haut in die Schwachstelle!"
                combat_log.add(text)

                hero.damage += self.power#### normal dmg
                damage_taken = enemy_block_dodge(hero, enemy, combat_log)
                hero.damage -= self.power####
                if damage_taken > 0:
                    text = f"{enemy.name}'s Schaden ist reduziert."
                    combat_log.add(text)
                    CrippleH2E(5, 3).buff(enemy)

                self._cost_and_cooldown(hero, self.cost, cooldown=2)
                return True
            else:
                text = f"Du hast dich verschätzt. {enemy.name} verfehlt!"
                combat_log.add(text)
                return False
        else:
            text = f"{self.name} ist auf Cooldown."
            combat_log.add(text)
            return False


@register
class Ability3(Ability):# PRÄZISER STICH
        
        def __init__(self):
            super().__init__("PRÄZISER STICH", 9, 17, 250,
                            precise_hit)
            
        def use_ability(self, hero, enemy, combat_log):
            if self.cool_down == 0:
                if hero.mana >= self.cost:
                    text = f"{hero.name} setzt zum Stoß an!"
                    combat_log.add(text)

                    hero.damage += self.power####
                    damage_taken = enemy_block_dodge(hero, enemy, combat_log)
                    hero.damage -= self.power####
                    if damage_taken > 0:
                        enemy.life -= self.power #Truedmg
                        text = f"+{self.power} Schaden."
                        combat_log.add(text)

                    self._cost_and_cooldown(hero, self.cost, cooldown=2)
                    return True
                else:
                    text = f"{enemy.name} steht weiter weg als gedacht."
                    combat_log.add(text)
                    return False
            else:
                text = f"{self.name} ist auf Cooldown."
                combat_log.add(text)
                return False


@register
class Ability4(Ability):# FEUERBALL

    def __init__(self):
        super().__init__("FEUERBALL", 60, 65, 315, 
                        fire_ball)
        
    def use_ability(self, hero, enemy, combat_log):
        if self.cool_down == 0:
            if hero.mana >= self.cost:
                text = f"{hero.name} beschwört einen Feuerball!"
                combat_log.add(text)

                enemy_mental_dodge(self.power, enemy, combat_log)

                self._cost_and_cooldown(hero, self.cost, cooldown=3)
                return True
            else:
                text = "Es fliegen einige Funken und sonst passiert nichts."
                combat_log.add(text)
                return False
        else:
            text = "Das Feuer zehrt noch an deiner Seele."
            combat_log.add(text)
            return False


@register
class Ability5(Ability): #MAGISCHER HIEB

    def __init__(self):
        super().__init__("MAGISCHER HIEB", 17, 31, 345,
                        magical_strike)
        
    def use_ability(self, hero, enemy, combat_log):
        if hero.mana >= self.cost:
            text = "MAGISCHER HIEB!"
            combat_log.add(text)

            hero.damage += self.power#normal dmg
            enemy_block_dodge(hero, enemy, combat_log)
            hero.damage -= self.power####

            text = "Die Magie brennt nach."
            combat_log.add(text)
            enemy_mental_dodge(self.power, enemy, combat_log)

            self._cost_and_cooldown(hero, self.cost)
            return True
        else:
            text = f"{hero.name}'s Kräfte versagen."
            combat_log.add(text)
            return False


@register
class Ability6(Ability): #MORDHAU

    def __init__(self):
        super().__init__("MORDHAU", 22, 5, 265,
                        mord_hau)
        
    def use_ability(self, hero, enemy, combat_log):
        if self.cool_down == 0:
            if hero.mana > self.cost:
                text = f"{hero.name} haut mit unmenschlicher Brutalität!"
                combat_log.add(text)

                hero.damage += self.power####
                enemy_block_dodge(hero, enemy, combat_log)
                hero.damage -= self.power####

                self._cost_and_cooldown(hero, self.cost, cooldown=2, life_cost=self.cost)
                return True
            else:
                text = f"Diese Technik würde {hero.name} dahinraffen."
                combat_log.add(text)
                return False
        else:
            text = f"{hero.name} rutscht beim Ausfallschritt weg!"
            combat_log.add(text)
            return False


@register
class Ability7(Ability): #KLEINER GIFTPFEIL

    def __init__(self):
        super().__init__("KLEINER GIFTPFEIL", 5, 25, 400,
                        poison_dart)
        
    def use_ability(self, hero, enemy, combat_log):
        if self.cool_down == 0:
            if hero.mana >= self.cost:
                text = f"{hero.name} wirft einen kleinen Pfeil."
                combat_log.add(text)

                self._cost_and_cooldown(hero, self.cost, cooldown=2)

                hero.damage -= self.power # decrease atk
                damage_taken = enemy_block_dodge(hero, enemy, combat_log)
                hero.damage += self.power
                if damage_taken > 0:
                    PoisonH2E(10, 4).buff(enemy)
                    text = f"{enemy.name} wurde vergiftet."
                    combat_log.add(text)
                    return True
                else:
                    text = "Der Pfeil konnte keinen Kratzer verursachen."
                    combat_log.add(text)
                    return False
            else:
                text = f"{hero.name} konnte nicht rechtzeitig ziehen."
                combat_log.add(text)
                return False
        else:
            text = f"{hero.name} konnte noch kein Gift auftragen."
            combat_log.add(text)
            return False


@register
class Ability8(Ability): #SCHILD-HALTUNG

    def __init__(self):
        super().__init__('SCHILD-HALTUNG', 10, 30, 300,
                         harden)
        
    def use_ability(self, hero, enemy, combat_log):
        if self.cool_down == 0:
            if hero.mana >= self.cost:
                text = f"{hero.name}'s Konstitution wächst."
                combat_log.add(text)

                hero.reduction += self.power #UNDO
                hero.over_hp += self.power * 2
                HardenH2H(8, 6).buff(hero)

                self._cost_and_cooldown(hero, self.cost, cooldown=7)
                return True
            else:
                text = f'{hero.name} fehlt die Ausdauer für diese Technik.'
                combat_log.add(text)
                return False
        else:
            text = f'{hero.name} hält bereits die SCHILD-HALTUNG.'
            combat_log.add(text)
            return False
        
    def undo_ability(self, hero, enemy):
        hero.reduction -= self.power


@register
class Ability9(Ability): #HEILUNG

    def __init__(self):
            super().__init__("HEILUNG", 56, 40, 355,
                            simple_heal)#power must be mod 8
            
    def use_ability(self, hero, enemy, combat_log):
            if self.cool_down == 0:
                if hero.mana >= self.cost:
                    text = f"{hero.name} heilt sich mit Magie."
                    combat_log.add(text)

                    hero.dodge += self.power / 8 #UNDO
                    hero.life += self.power
                    if hero.life > hero.max_life:
                        hero.life = hero.max_life

                    self._cost_and_cooldown(hero, self.cost, cooldown=5)
                    return True
                else:
                    text = "Es fliegen einige bunte Funken."
                    combat_log.add(text)
                    return False
            else:
                text = f"{hero.name} spricht die Verse, jedoch geschieht nichts."
                combat_log.add(text)
                return False
            
    def undo_ability(self, hero, enemy):
        hero.dodge -= self.power / 8


@register
class Ability10(Ability):#FROSTPFEIL

    def __init__(self):
        super().__init__("FROSTPFEIL", 20, 24, 340,
                        frost_arrow)
        
    def use_ability(self, hero, enemy, combat_log):
        if self.cool_down == 0:
            if hero.mana >= self.cost:
                text = f"{hero.name} schleudert ein Eisprojektil!"
                combat_log.add(text)

                self._cost_and_cooldown(hero, self.cost, cooldown=2)

                damage_taken = enemy_mental_dodge(self.power, enemy, combat_log)
                if damage_taken > 0:
                    text = f"{hero.name}'s Zauber zeitigt seine Wirkung"
                    combat_log.add(text)
                    FrostH2E(6, 3).buff(enemy)
                    return True
                else:
                    text = 'Der Zauber konnte nichts anrichten!'
                    combat_log.add(text)
                    return False
            else:
                text = 'Deine Macht reichte für eine kalte Briese.'
                combat_log.add(text)
                return False
        else:
            text = 'Die Finger sind noch zu vereist.'
            combat_log.add(text)
            return False


#IMAGES LOADED, EVERY ABILITY INSTANCE POITNS TO THESE
thunder = 'images/abilities/thunder.png'
double_strike = 'images/abilities/double_strike.png'
sword_dance = 'images/abilities/sword_dance.png'
#IMAGES LOADED, EVERY ABILITY INSTANCE POITNS TO THESE


class Ability11(Ability):#BLITZSCHLAG
    
    def __init__(self):
        super().__init__('Blitzschlag', 30, 30, 750,
                         thunder)
        
    def use_ability(self, hero, enemy, combat_log):
        if hero.mana >= self.cost:
            text = f"{hero.name} kanalisiert magische Kräfte."
            combat_log.add(text)
            text = f'Ein Blitz schiesst aus {hero.name} Fingern!'
            combat_log.add(text)

            damage_taken = enemy_mental_dodge(self.power, enemy, combat_log)
            if damage_taken > 0:
                text = f"{enemy.name} wurde geschockt."
                combat_log.add(text)
                ShockH2E(12, 3).buff(enemy)

            self._cost_and_cooldown(hero, self.cost)
            return True
        else:
            text = f'{hero.name} konzentriert sich doch nichts passiert.'
            combat_log.add(text)
            return False


class Ability12(Ability):#DOPPELSCHLAG

    def __init__(self):
        super().__init__('Doppelschlag', 1, 15, 750,
                        double_strike)
        
    def use_ability(self, hero, enemy, combat_log):
        if hero.mana >= self.cost:
            text = f'Gekonnt schwingt {hero.name} seine Waffe.'
            combat_log.add(text)

            hero.damage += self.power
            damage_taken = enemy_block_dodge(hero, enemy, combat_log)
            if damage_taken > 0:
                enemy_block_dodge(hero, enemy, combat_log)
            hero.damage -= self.power

            self._cost_and_cooldown(hero, self.cost)
            return True
        else:
            text = "Versuche es erstmal mit EINEM Schlag."
            combat_log.add(text)
            return False
        

class Ability13(Ability):#SCHWERTTANZ

    def __init__(self):
        super().__init__('Schwerttanz', 7, 33, 800,
                        sword_dance)
        
    def use_ability(self, hero, enemy, combat_log):
        if self.cool_down == 0:
            if hero.mana >= self.cost:
                text = 'Schweben wie ein Schmetterling'
                combat_log.add(text)
                text = 'Stechen wie eine Biene!'
                combat_log.add(text)

                hero.dodge += self.power#UNDO
                magic_number = random.randint(0, 3)
                AgileH2H(self.power - magic_number,
                         3 + magic_number).buff(hero)
                EmpoweredH2H(self.power + magic_number,
                         5 - magic_number).buff(hero)
                
                self._cost_and_cooldown(hero, self.cost, cooldown=5)
                return True
            else:
                text = f'{hero.name} fehlt die Ausdauer für diese Technik.'
                combat_log.add(text)
                return False
        else:
            text = f'{hero.name} befindet sich noch im Schwerttanz.'
            combat_log.add(text)
            return False
        
    def undo_ability(self, hero, enemy):
        hero.dodge -= self.power

