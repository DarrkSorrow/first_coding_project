import pygame
import random, abilities


def random_enemy(hero, stage):
    match stage:
        case 0:
            enemies = (EasyPool1, EasyPool2)
        case 1 | 2:
            enemies = (Minion1, Minion2, Minion3, Minion4,
                       Minion5, Minion6, Minion7)
    enemy = random.choice(enemies)
    #no b2b the same enemy
    while enemy is hero.game_state.last_enemy:
        enemy = random.choice(enemies)
    hero.game_state.last_enemy = enemy # saves last enemy 
    hero.game_state.events_in_row = 0 # reset event counter
    hero.game_state.enemy_counter += 1 # increase enemy streak
    return enemy()


def random_elite(hero, stage):
    enemies = (Elite1, Elite2, Elite3)
    enemy = random.choice(enemies)
    #no b2b the same enemy
    while enemy is hero.game_state.last_enemy:
        enemy = random.choice(enemies)
    hero.game_state.last_enemy = enemy # saves last enemy 
    hero.game_state.events_in_row = 0 # reset event counter
    hero.game_state.enemy_counter = 0 # reset enemy counter
    return enemy()


def random_boss(hero, stage):
    enemies = (Boss1, Boss1)
    enemy = random.choice(enemies)
    hero.game_state.events_in_row = 0 # reset event counter
    hero.game_state.enemy_counter = 0 # reset enemy counter
    return enemy()


#IMAGES LOADED, EVERY ENEMY INSTANCE POITNS TO THESE
easy_pool_1 = 'images/akt1_easy_riesenratte.png'
easy_pool_2 = 'images/akt1_easy_grüner_schleim.png'
minion_1 = 'images/akt1_normal_skelett_diener.png'
minion_2 = 'images/akt1_normal_grüner_goblin.png'
minion_3 = 'images/akt1_normal_irrlicht.png'
minion_4 = 'images/akt1_normal_schwarzer_goblin.png'
minion_5 = 'images/akt1_normal_steingolem.png'
minion_6 = 'images/akt1_normal_räuber.png'
minion_7 = 'images/akt1_normal_abenteurer.png'
elite_1 = 'images/akt1_elite_junger_höhlentroll.png'
elite_2 = 'images/akt1_elite_panzer_schildkröte.png'
elite_3 = 'images/akt1_elite_schwarzer_schwertkämpfer.png'
boss_1 = 'images/akt1_boss_infernodämon.png'
#IMAGES LOADED, EVERY ENEMY INSTANCE POITNS TO THESE


class Enemy:
    
    def __init__(self, name, life, max_life, damage, speed,
                 image_path,
                 reduction=0, dodge=5, mental_reduction=0,
                 magic_power=0, critical=0):
        self.name = name
        self.life, self.max_life = life, max_life
        self.damage = damage
        self.speed = speed
        self.reduction, self.dodge = reduction, dodge
        self.mental_reduction = mental_reduction
        self.magic_power = magic_power
        self.critical = critical
        self.over_hp = 0
        self.buffs = []

        self.image = pygame.image.load(
            image_path).convert_alpha()
        self.image =pygame.transform.scale(self.image, (300, 300))
        self.rect = self.image.get_rect()
        self.rect.center = (650, 250)
        
        self.font = pygame.font.SysFont(None, 40)

    def blitme(self, screen):
        """Draw enemy sprite at middle position"""
        screen.blit(self.image, self.rect)

    def _overhp_over_hp(self, hero, hp_loss):    
        hp_loss -= hero.over_hp
        if hp_loss >= 0:
            hero.over_hp = 0
        else: #when hp_loss negative -> then over_hp > 0
            hero.over_hp = abs(hp_loss)
            hp_loss = 0
        return hp_loss

    def basic_attack(self, hero, combat_log):
        magic_number = random.randint(0, 100)
        if magic_number < hero.dodge:
            text = "Du konntest ausweichen!!!"
            combat_log.add(text, True)
        else:
            block = (1 - hero.reduction / 100)
            if block > 1:
                block = 1
            crit_factor = self._critical_hit(combat_log)
            hp_loss = round(self.damage * crit_factor * block)
            if hp_loss < 0:
                hp_loss = 0
            hp_loss = self._overhp_over_hp(hero, hp_loss)
            hero.life -= hp_loss
            text = f"{hero.name} erleidet {hp_loss} Schaden!"
            combat_log.add(text, True)

    def _critical_hit(self, combat_log):
        magic_number = random.randint(0, 100)
        if magic_number < self.critical:
            text = "KRITISCHER TREFFER!!"
            combat_log.add(text)
            crit_factor = 1.5
        else:
            crit_factor = 1
        return crit_factor

    def basic_magic(self, hero, combat_log):
        magic_number = random.randint(0, 200)
        if magic_number < hero.dodge:
            text = "Du konntest Magie ausweichen!!!"
            combat_log.add(text, True)
        else:
            block = (1 - hero.mental_reduction / 100)
            if block > 1:
                block = 1
            hp_loss = round(self.magic_power * block)
            if hp_loss < 0:
                hp_loss = 0
            hp_loss = self._overhp_over_hp(hero, hp_loss)
            hero.life -= hp_loss
            text = f"{hero.name} erleidet {hp_loss} Schaden!"
            combat_log.add(text, True)

    def mana_burn(self, hero, combat_log):
        magic_number = random.randint(0, 150)
        if magic_number < hero.dodge:
            text = "Du konntest widerstehen."
            combat_log.add(text, True)
        else:
            block = (1 - hero.mental_reduction / 100)
            if block > 1:
                block = 1
            mana_loss = round(self.magic_power * block)
            if mana_loss < 0:
                mana_loss = 0
            hero.mana -= mana_loss
            if hero.mana <= 0:
                hero.mana = 0
            text = f"{hero.name} verliert {mana_loss} ODEM!"
            combat_log.add(text, True)

    def block(self, power, combat_log):
        self.over_hp += power
        text = f"{self.name} + {power} Schild"
        combat_log.add(text, True)

    def heal_self(self, power, combat_log):
        self.life += power
        if self.life > self.max_life:
            self.life = self.max_life
        text = f"{self.name} heilt sich +{power}HP."
        combat_log.add(text, True)

    def decay_over_hp(self):
        if self.over_hp == 1:
            self.over_hp = 0
        else:
            self.over_hp = round(self.over_hp * 0.7)


class EasyPool1(Enemy):#v1

    def __init__(self):
        super().__init__("GROSSE RATTE", 33, 33, 16, 55,
                        easy_pool_1 , dodge=7,
                        critical=3)
        
    def _frenzy(self, combat_log):#ENEMY-MOVE
        text = f"{self.name} wird schneller."
        combat_log.add(text, True)
        abilities.EnemyBuff2(5, 3).buff(self)

    def _random(self, hero, combat_log):
        magic_number = random.choice((1, 2))
        match magic_number:
            case 1:
                self.basic_attack(hero, combat_log)
            case 2:
                self._frenzy(combat_log)

    def enemy_ai(self, hero, key, combat_log):
        match key:
            case 1:
                self._random(hero, combat_log)
            case 2:
                self._frenzy(combat_log)
            case 3:
                self._random(hero, combat_log)
            case 4:
                self.basic_attack(hero, combat_log)

    def enemy_intend(self, step, hero):
        if step == 0:
            intend, key = "Atk / Buff", 1
        elif step % 2 == 1:
            intend, key = "Buff", 2
        elif step % 4 == 0:
            intend, key = "Atk / Buff", 3
        else:
            intend, key = "Atk", 4
        text = self.font.render(intend, True, (0, 0, 0))
        return text, key


class EasyPool2(Enemy):#v1
    def __init__(self):
        super().__init__("MAGISCHER SCHLEIM", 35, 35, 16, 14,
                        easy_pool_2)
        
    def _slime(self, hero, combat_log):#ENEMY-MOVE
        abilities.EnemyDebuff2(5, 4).buff(hero)
        heal = 3
        self.life += heal
        if self.life > self.max_life:
            self.life = self.max_life
        text = f"{self.name} verschießt Schleim. +{heal}HP"
        combat_log.add(text, True)

    def enemy_ai(self, hero, key, combat_log):
        match key:
            case 1:
                self._slime(hero, combat_log)
            case 2:
                self.basic_attack(hero, combat_log)
            case 3:
                self.basic_attack(hero, combat_log)

    def enemy_intend(self, step, hero):
        if step % 2 == 0:
            intend, key = "Debuff", 1
        elif hero.damage < 5:
            intend, key = "Atk", 2
        else:
            intend, key = "Atk", 3
        text = self.font.render(intend, True, (0, 0, 0))
        return text, key


class Minion1(Enemy):#v1

    def __init__(self):
        super().__init__("SKELETTDIENER", 60, 60, 21, 20,
                         minion_1)
        
    def _unholy_aura(self, combat_log):#ENEMY-MOVE
        self.life += 7
        if self.life > self.max_life:
            self.life = self.max_life
        text = f"{self.name} kanalisiert unheilige Kräfte."
        combat_log.add(text, True)

    def enemy_ai(self, hero, key, combat_log):
        match key:
            case 1:
                self.basic_attack(hero, combat_log)
            case 2:
                self._unholy_aura(combat_log)

    def enemy_intend(self, step, hero):
        if step % 2 == 0:
            intend, key = "Atk", 1
        else:
            intend, key = "Heal", 2
        text = self.font.render(intend, True, (0, 0, 0))
        return text, key


class Minion2(Enemy):#v1

    def __init__(self):
        super().__init__("GRÜNER GOBLIN", 40, 40, 25, 45,
                         minion_2)
        self.nerfed = False
        
    def _throw_rock(self, hero, combat_log):#ENEMY-MOVE
        text = f"{self.name} greift nach einem Stein.."
        combat_log.add(text, True)
        self.damage -= 6
        self.basic_attack(hero, combat_log)
        self.damage += 6
        abilities.EnemyDebuff1(5, 2).buff(hero)

    def enemy_ai(self, hero, key, combat_log):
        if self.life < self.max_life / 2 and not self.nerfed:
            text = f"{self.name} hat sich verausgabt.."
            combat_log.add(text, True)
            self.damage -= 12
            self.speed -= 25
            self.nerfed = True
        match key:
            case 1:
                magic_number = random.choice((1, 2))
                match magic_number:
                    case 1:
                        self.basic_attack(hero, combat_log)
                    case 2:
                        self._throw_rock(hero, combat_log)
            case 2:
                self.basic_attack(hero, combat_log)

    def enemy_intend(self, step, hero):
        if self.life > self.max_life / 2:
            intend, key = "Atk+", 2
        else:
            intend, key = "Atk", 1
        text = self.font.render(intend, True, (0, 0, 0))
        return text, key


class Minion3(Enemy):#v1

    def __init__(self):
        super().__init__("IRRLICHT", 33, 33, 15, 30,
                        minion_3,
                        reduction = 25, dodge=10, mental_reduction=30,
                        magic_power=7)

    def _magical_erruption(self, hero, combat_log):
        text = 'Das Wesen strahlt heftig!'
        combat_log.add(text, True)
        self.magic_power = hero.mana
        self.basic_magic(hero, combat_log)
        self.life = 0
        
    def enemy_ai(self, hero, key, combat_log):
        match key:
            case 1:
                self._magical_erruption(hero, combat_log)
            case 2:
                self.basic_attack(hero, combat_log)
                self.reduction += 25
                text = f"{self.name} wechselt in die Geisterwelt."
                combat_log.add(text, True)
            case 3:
                if hero.mana > 0:
                    self.mana_burn(hero, combat_log)
                    text = f"{self.name} entzieht die magische Essenz."
                    combat_log.add(text, True)
                    self.reduction -= 25
                    text = f"{self.name} materialisiert sich."
                    combat_log.add(text, True)
                else:
                    self.basic_magic(hero, combat_log)
                    text = f"{hero.name} ist ausgesaugt und nimmt Schaden."
                    combat_log.add(text, True)
                    self.reduction -= 25
                    text = f"{self.name} materialisiert sich."
                    combat_log.add(text, True)

    def enemy_intend(self, step, hero):
        if step == 6:
            intend, key = 'Finale', 1
        elif step % 2 == 0:
            intend, key = "Atk", 2
        else:
            intend, key = "Mag", 3
        text = self.font.render(intend, True, (0, 0, 0))
        return text, key


class Minion4(Enemy):#v1

    def __init__(self):
        super().__init__("SCHWARZER GOBLIN", 47, 47, 15, 25,
                        minion_4,
                        mental_reduction=25, dodge=10, 
                        magic_power=20)
        
    def _illusion(self, combat_log):#ENEMY-MOVE
        text = f"Deine Augen scheinen dich zu trügen."
        combat_log.add(text, True)
        abilities.EnemyBuff3(8, 3).buff(self)

    def _random(self, hero, combat_log):
        magic_number = random.randint(0, 100)
        if magic_number <= 45:
            self.basic_attack(hero, combat_log)
        elif 45 < magic_number <= 59:
            self.basic_magic(hero, combat_log)
        else:
            self._illusion(combat_log)

    def enemy_ai(self, hero, key, combat_log):
        match key:
            case 1:
                self.basic_attack(hero, combat_log)
            case 2:
                text = f"{self.name}'s Kraft wächst weiter."
                combat_log.add(text, True)
                self.damage += 6
                self.block(7, combat_log)
            case 3:
                self._random(self, hero, combat_log)

    def enemy_intend(self, step, hero):
        if step == 0:
            intend, key = "Atk", 1
        elif step % 3 == 0:
            intend, key = "Pwr+", 2
        else:
            intend, key = "?", 3
        text = self.font.render(intend, True, (0, 0, 0))
        return text, key


class Minion5(Enemy):#v1

    def __init__(self):
        super().__init__('STEINGOLEM', 50, 50, 16, 10,
                        minion_5,
                        reduction=35, dodge=0)
        
    def fortify(self, combat_log):#ENEMY-MOVE
        text = f"{self.name}'s Struktur verfestigt sich."
        combat_log.add(text, True)
        abilities.EnemyBuff1(15, 2).buff(self)

    def enemy_ai(self, hero, key, combat_log):
        match key:
            case 1:
                self.basic_attack(hero, combat_log)
            case 2:
                magic_number = random.randint(0, 1)
                if magic_number == 1:
                    self.fortify(combat_log)
                else:
                    self.basic_attack(hero, combat_log)
            case 3:
                magic_number = random.randint(0, 1)
                if magic_number == 1:
                    self.block(12, combat_log)
                else:
                    self.basic_attack(hero, combat_log)

    def enemy_intend(self, step, hero):
        if step % 3 == 0:
            intend, key = "Atk", 1
        elif self.life > self.max_life * 0.6:
            intend, key = "Atk / BUFF", 2
        else:
            intend, key = "Atk / BLOCK", 3
        text = self.font.render(intend, True, (0, 0, 0))
        return text, key
    

class Minion6(Enemy):#v1

    def __init__(self):
        super().__init__('RÄUBER', 40, 55, 16, 40,
                        minion_6,
                        reduction=5,
                        critical=5)
        
    def enemy_ai(self, hero, key, combat_log):
        match key:
            case 1:
                self.damage += 5
                text = f"{self.name} zieht eine zweite Waffe."
                combat_log.add(text, True)
                self.block(10, combat_log)
            case 2:
                self.block(20, combat_log)
            case 3:
                self.basic_attack(hero, combat_log)
            case 4:
                self.heal_self(21, combat_log)
            case 5:
                self.block(12, combat_log)

    def enemy_intend(self, step, hero):
        if step == 0:
            if hero.damage > 20:
                intend, key = 'Pwr+', 1
            else:
                intend, key = 'Block', 2
        elif step % 2 == 1:
            intend, key = 'Atk', 3
        else:
            if hero.life > self.life * 2:
                intend, key = 'Heal', 4
            else:
                intend, key = 'Block', 5
        text = self.font.render(intend, True, (0, 0, 0))
        return text, key


class Minion7(Enemy):#v1

    def __init__(self):
        super().__init__('ABENTEURER', 43, 43, 17, 36, 
                        minion_7, 
                        reduction=20, mental_reduction=10,
                        magic_power=11)
        
    def enemy_ai(self, hero, key, combat_log):
        match key:
            case 1:
                self.basic_attack(hero, combat_log)
            case 2:
                self.basic_magic(hero, combat_log)
            case 3:
                self.speed += 50
                self.dodge += 5
                text = f"{self.name} wechselt seine Strategie."
                combat_log.add(text, True)
                self.block(8, combat_log)
            case 4:
                magic_number = random.randint(0, 1)
                if magic_number == 1:
                    self.block(15, combat_log)
                else:
                    if self.damage > self.magic_power + 1:
                        self.basic_attack(hero, combat_log)
                    else:
                        self.basic_magic(hero, combat_log)

    def enemy_intend(self, step, hero):
        if step == 0:
            intend, key = 'Atk', 1
        elif step == 1:
            intend, key = 'Mag', 2
        elif hero.speed > 50 and self.speed < 50:
            intend, key = 'Pwr+', 3
        elif step > 1:
            intend, key = 'Atk / Block', 4
        text = self.font.render(intend, True, (0, 0, 0))
        return text, key


class Elite1(Enemy):#v1

    def __init__(self):
        super().__init__("JUNGER HÖHLENTROLL", 100, 100, 32, 38,
                        elite_1,
                        reduction=10)
        self.nerfed = False
        
    def _war_cry(self, hero, combat_log):#ENEMY-MOVE
        text = f"{self.name} brüllt dich zornig an!"
        combat_log.add(text, True)
        abilities.EnemyDebuff1(7, 3).buff(hero)

    def enemy_ai(self, hero, key, combat_log):
        if self.life < self.max_life * 0.35 and not self.nerfed:
            self.damage -= 10
            self.nerfed = True
            text = f"{self.name} ist schächer geworden."
            combat_log.add(text, True)
        match key:
            case 1:
                text = f"{self.name} schlägt mit Brutalität zu!"
                combat_log.add(text, True)
                self.damage += 14
                self.basic_attack(hero, combat_log)
                self.damage -= 14
            case 2:
                self._war_cry(hero, combat_log)
            case 3:
                magic_number = random.randint(0, 100)
                if magic_number <= 65:
                    self.basic_attack(hero, combat_log)
                else:
                    self._war_cry(hero, combat_log)

    def enemy_intend(self, step, hero):
        if step == 0:
            intend, key = "Atk+", 1
        elif step == 1:
            intend, key = "Debuff", 2
        else:
            intend, key = "Atk / Debuff", 3
        text = self.font.render(intend, True, (0, 0, 0))
        return text, key


class Elite2(Enemy):#v1

    def __init__(self):
        super().__init__("PANZER-SCHILDKRÖTE", 200, 200, 23, 10,
                        elite_2,
                        reduction=10)
        
    def _harden_or_burst(self, hero, combat_log):
        if self.life <= self.max_life * 0.25:
            text = f"{self.name} zerberstet in einem lauten Knall!"
            combat_log.add(text, True)
            self.life = 0
            hero.life -= 18
            text = f"{hero.name} kriegt einige Fragmente ab!" 
            combat_log.add(text, True)
        else:
            text = "Der Panzer verfestigt sich."
            combat_log.add(text, True)
            abilities.EnemyBuff1(30, 3).buff(self)

    def _random(self, hero, combat_log):
        magic_number = random.choice((1, 2, 3))
        match magic_number:
            case 1:
                self.basic_attack(hero, combat_log)
            case 2:
                self._harden_or_burst(hero, combat_log)
            case 3:
                self.block(20, combat_log)

    def enemy_ai(self, hero, key, combat_log):
        match key:
            case 1:
                self.basic_attack(hero, combat_log)
            case 2:
                self.harden_or_burst(hero, combat_log)
            case 3:
                self.basic_attack(hero, combat_log)
            case 4:
                self.block(15, combat_log)
            case 5:
                self._random(hero, combat_log)

    def enemy_intend(self, step, hero):
        if step == 0:
            intend, key = "Atk", 1
        elif self.life >= self.max_life * 0.9:
            intend, key = "Buff", 2
        elif self.life >= self.max_life * 0.7:
            intend, key = "Atk", 3
        elif self.life >= self.max_life * 0.6:
            intend, key = "Block", 4
        else:
            intend, key = "?", 5
        text = self.font.render(intend, True, (0, 0, 0))
        return text, key
    

class Elite3(Enemy):#v1

    def __init__(self):
        super().__init__('SCHWARZER SCHWERTKÄMPFER', 160, 160, 20, 70,
                        elite_3,
                        reduction=10,
                        critical=5)
        
    def ability_1(self, combat_log):
        text = "Der Kämpfer ist kaum zu erkennen!" 
        combat_log.add(text, True)
        abilities.EnemyBuff3(20, 2).buff(self)

    def ability_2(self, hero, combat_log):
        text = f"{hero.name}'s Kraft schwindet." 
        combat_log.add(text, True)
        abilities.EnemyDebuff2(10, 2).buff(hero)

    def enemy_ai(self, hero, key, combat_log):
        magic_number = random.choice((1, 2))
        match key:
            case 1:
                self.block(20, combat_log)
            case 2:
                if magic_number == 1:
                    self.basic_attack(hero, combat_log)
                else:
                    self.ability_1(combat_log)
            case 3:
                if magic_number == 1:
                    self.basic_attack(hero, combat_log)
                else:
                    self.ability_2(hero, combat_log)
            case 4:
                if magic_number == 1:
                    self.basic_attack(hero, combat_log)
                else:
                    self.block(20, combat_log)

    def enemy_intend(self, step, hero):
        if step == 0:
            intend, key = "Block", 1
        elif step % 3 == 2:
            intend, key = "Atk / Buff", 2
        elif step % 3 == 1:
            intend, key = "Atk / Debuff", 3
        elif step % 3 == 0:
            intend, key = "Atk / Block", 4
        text = self.font.render(intend, True, (0, 0, 0))
        return text, key
                

class Boss1(Enemy):#v1

    def __init__(self):
        super().__init__("INFERNO-DÄMON", 330, 330, 12, 50,
                        boss_1,
                        reduction=10, dodge=10, mental_reduction=10,
                        magic_power=6)
        
    def enemy_ai(self, hero, key, combat_log):
        match key:
            case 1:
                text = f"{self.name} erwacht!"
                combat_log.add(text, True)
            case 2:
                text = f"Die Kreatur beschwört ein Feuersiegel auf {hero.name}'s Haut."
                combat_log.add(text, True)
                abilities.EnemyDebuff3(6, 4).buff(hero)
            case 3:
                text = f"{self.name} holt zum Schlag aus!"
                combat_log.add(text, True)
                self.basic_attack(hero, combat_log)
            case 4:
                text = f"{self.name} schleudert einen Feuerpfeil!"
                combat_log.add(text, True)
                self.basic_magic(hero, combat_log)
            case 5:
                text = f"Die Macht von {self.name} erhöht sich."
                combat_log.add(text, True)
                self.damage += 6

    def enemy_intend(self, step, hero):
        if step == 0:
            intend, key = "zz..", 1
        elif step % 4 == 1:
            intend, key = "DEBUFF+", 2
        elif step % 4 == 2:
            intend, key = "Atk", 3
        elif step % 4 == 3:
            intend, key = "Mag", 4
        elif step % 4 == 0:
            intend, key = "Pwr++", 5
        text = self.font.render(intend, True, (0, 0, 0))
        return text, key


#IMAGES LOADED, EVERY ENEMY INSTANCE POITNS TO THESE
act2_minion_1 = ''
act2_minion_2 = ''
act2_minion_3 = ''
act2_minion_4 = ''
#IMAGES LOADED, EVERY ENEMY INSTANCE POITNS TO THESE


class Act2Minion1(Enemy):#Not in rotation yet
    def __init__(self):
        super().__init__("UNTOTER KRIEGER", 80, 80, 21, 50,
                        act2_minion_1, 
                        reduction=10)
    def enemy_ai(self, hero, step, combat_log):
        if step % 2 == 0:
            if self.life < round(self.max_life * 0.4):
                self.heal_self(22, combat_log)
            else:
                self.basic_attack(hero, combat_log)
        elif step % 2 == 1:
            self.mana_burn(hero, combat_log)
    def enemy_intend(self, step, hero):
        if step % 2 == 0:
            if self.life < round(self.max_life * 0.4):
                intend = 'Heal'
            else:
                intend = 'Atk'
        elif step % 2 == 1:
            intend = 'Mag'
        text = self.font.render(intend, True, (0, 0, 0))
        return text


class Act2Minion1(Enemy):#Not in rotation yet
    def __init__(self):
        super().__init__('WÄCHTER GOLEM', 100, 100, 15, 24, 
                         act2_minion_2, 
                         reduction=10, mental_reduction=10, 
                         magic_power=50)
    def enemy_ai(self, hero, step, combat_log):
        if step == 0:
            self.block(50, combat_log)
        if step % 2 == 1:
            magic_number = random.randint((1, 2))
            if magic_number == 1:
                self.basic_attack
            else:
                abilities.EnemyBuff4().buff(self)
        else:
            if hero.life > 100:
                self.basic_magic(hero, combat_log)
            else:
                self.basic_attack(hero, combat_log)
    def enemy_intend(self, step, hero):
        if step == 0:
            intend = 'Block+'
        if step % 2 == 1:
            intend = 'Atk / Buff'
        else:
            if hero.life > 100:
                intend = 'Mag+'
            else:
                intend = 'Atk'
        text = self.font.render(intend, True, (0, 0, 0))
        return text