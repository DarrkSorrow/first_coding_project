
class Buff:
    
    def __init__(self, name, power, duration):
        self.name = name
        self.power = power
        self.duration = duration
        self.clear = False
        self.active = False
        self.stun = False
    
    def __repr__(self):
        return self.name
    
    def count_down(self):
        self.duration -= 1
        if self.duration == 0:
            self.clear = True


# *** HERO --> HERO ***
            

class EmpoweredH2H(Buff):#START-FÄHIGKEIT

    def __init__(self, power, duration):
        super().__init__("gestärkt", power, duration)

    def buff(self, hero):
        hero.buffs.append(self)
        hero.damage += self.power

    def debuff(self, hero):
        hero.damage -= self.power
        hero.buffs.remove(self)


class HardenH2H(Buff):#Schild-Haltung

    def __init__(self, power, duration):
        super().__init__("schild", power, duration)

    def buff(self, hero):
        hero.buffs.append(self)
        hero.reduction += self.power

    def debuff(self, hero):
        hero.reduction -= self.power
        hero.buffs.remove(self)


class BerserkH2H(Buff):#Berserker

    def __init__(self, power, duration):
        super().__init__("berserk", power, duration)

    def buff(self, hero):
        hero.buffs.append(self)
        hero.critical += self.power * 2
        hero.damage += self.power

    def debuff(self, hero):
        hero.damage -= self.power
        hero.critical -= self.power * 2
        hero.buffs.remove(self)


class ClarityH2H(Buff):#Klarheit

    def __init__(self, power, duration):
        super().__init__('klarheit', power, duration)
        self.active = True

    def buff(self, hero):
        hero.buffs.append(self)

    def debuff(self, hero):
        hero.buffs.remove(self)

    def effekt(self, hero):
        hero.mana += self.power
        if hero.mana > hero.max_mana:
            hero.mana = hero.max_mana


class RegenerationH2H(Buff):#Heilung

    def __init__(self, power, duration):
        super().__init__('heilung', power, duration)
        self.active = True

    def buff(self, hero):
        hero.buffs.append(self)

    def debuff(self, hero):
        hero.buffs.remove(self)

    def effekt(self, hero):
        hero.life += self.power
        if hero.mana > hero.max_mana:
            hero.mana = hero.max_mana


class AgileH2H(Buff):

    def __init__(self, power, duration):
        super().__init__("agil", power, duration)

    def buff(self, hero):
        hero.buffs.append(self)
        hero.dodge += self.power

    def debuff(self, hero):
        hero.dodge -= self.power
        hero.buffs.remove(self)


# *** HERO --> ENEMY ***


class StunH2E(Buff):
    """self.power is int in percent"""
    def __init__(self, power, duration):
        super().__init__("STUN", power, duration)
        self.stun = True

    def buff(self, enemy):
        enemy.buffs.append(self)

    def debuff(self, enemy):
        enemy.buffs.remove(self)


class CrippleH2E(Buff):#Verkrüppelt

    def __init__(self, power, duration):
        super().__init__("Verkrüp.", power, duration)

    def buff(self, enemy):
        enemy.buffs.append(self)
        enemy.damage -= self.power

    def debuff(self, enemy):
        enemy.damage += self.power
        enemy.buffs.remove(self)


class PoisonH2E(Buff):#Vergiftet

    def __init__(self, power, duration):
        super().__init__("vergift.", power, duration)
        self.active = True

    def buff(self, enemy):
        enemy.buffs.append(self)

    def debuff(self, enemy):
        enemy.buffs.remove(self)

    def effekt(self, hero):
        hero.life -= self.power


class FrostH2E(Buff):#Frost

    def __init__(self, power, duration):
        super().__init__("frost", power, duration)

    def buff(self, enemy):
        enemy.buffs.append(self)
        enemy.speed -= self.power * 5
        enemy.reduction -= self.power 

    def debuff(self, enemy):
        enemy.reduction += self.power
        enemy.speed += self.power * 5
        enemy.buffs.remove(self)


class ShockH2E(Buff):#Shock

    def __init__(self, power, duration):
        super().__init__('zermürbt', power, duration)

    def buff(self, enemy):
        enemy.buffs.append(self)
        enemy.mental_resistance -= self.power

    def debuff(self, enemy):
        enemy.mental_resistance += self.power
        enemy.buffs.remove(self)


class FireH2E(Buff):#Brand

    def __init__(self, power, duration):
        super().__init__("brand", power, duration)
        self.active = True

    def buff(self, enemy):
        enemy.buffs.append(self)

    def debuff(self, enemy):
        enemy.buffs.remove(self)

    def effekt(self, enemy):#deals x-perc of max_life as tick-dmg
        enemy.life -= round(enemy.max_life * self.power / 100)


# *** ENEMY --> ENEMY ***
        

class HardenE2E(Buff):#Stabil

    def __init__(self, power, duration):
        super().__init__("stabil", power, duration)

    def buff(self, enemy):
        enemy.buffs.append(self)
        enemy.reduction += self.power

    def debuff(self, enemy):
        enemy.reduction -= self.power
        enemy.buffs.remove(self)


class AdrenalinE2E(Buff):#Adrenalin

    def __init__(self, power, duration):
        super().__init__("adrenal.", power, duration)

    def buff(self, enemy):
        enemy.buffs.append(self)
        enemy.speed += self.power
        enemy.dodge += self.power

    def debuff(self, enemy):
        enemy.dodge -= self.power
        enemy.speed -= self.power
        enemy.buffs.remove(self)


class HasteE2E(Buff):

    def __init__(self, power, duration):
        super().__init__('Hast', power, duration)

    def buff(self, enemy):
        enemy.buffs.append(self)
        enemy.speed += self.power

    def debuff(self, enemy):
        enemy.speed -= self.power
        enemy.buffs.remove(self)


class IllusionE2E(Buff):#Illusion

    def __init__(self, power, duration):
        super().__init__("illusion", power, duration)

    def buff(self, enemy):
        enemy.buffs.append(self)
        enemy.dodge += self.power 
        enemy.mental_reduction += self.power

    def debuff(self, enemy):
        enemy.mental_reduction -= self.power
        enemy.dodge -= self.power
        enemy.buffs.remove(self)


class FullDefenseE2E(Buff):

    def __init__(self, power, duration):
        super().__init__("bollwerk", power, duration)

    def buff(self, enemy):
        enemy.buffs.append(self)
        enemy.reduction += self.power
        enemy.mental_reduction += self.power

    def debuff(self, enemy):
        enemy.mental_reduction -= self.power
        enemy.reduction -= self.power
        enemy.buffs.remove(self)


class AccuracyE2E(Buff):

    def __init__(self, power, duration):
        super().__init__("", power, duration)

    def buff(self, enemy):
        enemy.buffs.append(self)
        enemy.accuracy += self.power

    def debuff(self, enemy):
        enemy.accuracy -= self.power
        enemy.buffs.remove(self)



# *** ENEMY --> HERO ***


class StunE2H(Buff):
    """self.power is int in percent"""
    def __init__(self, power, duration):
        super().__init__("STUN", power, duration)
        self.stun = True

    def buff(self, hero):
        hero.buffs.append(self)

    def debuff(self, hero):
        hero.buffs.remove(self)


class WeakE2H(Buff):

    def __init__(self, power, duration):
        super().__init__("schwäche", power, duration)

    def buff(self, hero):
        hero.buffs.append(self)
        hero.damage -= self.power
        hero.speed -= self.power

    def debuff(self, hero):
        hero.speed += self.power
        hero.damage += self.power
        hero.buffs.remove(self)


class SlowE2H(Buff):#Verlangsamt

    def __init__(self, power, duration):
        super().__init__("langsam", power, duration)

    def buff(self, hero):
        hero.buffs.append(self)
        hero.speed -= self.power

    def debuff(self, hero):
        hero.speed += self.power
        hero.buffs.remove(self)


class FireSealE2H(Buff):#Feuersiegel

    def __init__(self, power, duration):
        super().__init__("Feuermal", power, duration)
        self.active = True

    def buff(self, hero):
        hero.buffs.append(self)

    def debuff(self, hero):
        hero.buffs.remove(self)
        
    def effekt(self, hero):
        hero.life -= self.power
class PoisonE2H(Buff):#like FireSealE2H

    def __init__(self, power, duration):
        super().__init__("vergift.", power, duration)
        self.active = True

    def buff(self, hero):
        hero.buffs.append(self)

    def debuff(self, hero):
        hero.buffs.remove(self)
        
    def effekt(self, hero):
        hero.life -= self.power