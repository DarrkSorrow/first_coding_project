
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


class BerserkH2H(Buff):#Berserker
#Muss weg
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
        if hero.life > hero.max_life:
            hero.life = hero.max_life


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


class CrippleH2E(Buff):#Verkrüppelt

    def __init__(self, power, duration):
        super().__init__("Verkrüp.", power, duration)

    def buff(self, enemy):
        enemy.buffs.append(self)
        enemy.damage -= self.power

    def debuff(self, enemy):
        enemy.damage += self.power
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


# *** ENEMY --> HERO ***


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


#*** --- *** --- *** --- *** --- ***


class Shock(Buff):#Shock

    def __init__(self, power, duration):
        super().__init__('zermürbt', power, duration)

    def buff(self, subject):
        subject.buffs.append(self)
        subject.mental_reduction -= self.power

    def debuff(self, subject):
        subject.mental_reduction += self.power
        subject.buffs.remove(self)


class FireSeal(Buff):

    def __init__(self, power, duration):
        super().__init__("Feuermal", power, duration)
        self.active = True

    def buff(self, subject):
        subject.buffs.append(self)

    def debuff(self, subject):
        subject.buffs.remove(self)
        
    def effekt(self, subject):
        subject.life -= self.power


class Slow(Buff):

    def __init__(self, power, duration):
        super().__init__("langsam", power, duration)

    def buff(self, subject):
        subject.buffs.append(self)
        subject.speed -= self.power

    def debuff(self, subject):
        subject.speed += self.power
        subject.buffs.remove(self)


class Poison(Buff):

    def __init__(self, power, duration):
        super().__init__("vergift.", power, duration)
        self.active = True

    def buff(self, subject):
        subject.buffs.append(self)

    def debuff(self, subject):
        subject.buffs.remove(self)

    def effekt(self, subject):
        subject.life -= self.power


class Accuracy(Buff):

    def __init__(self, power, duration):
        super().__init__("", power, duration)

    def buff(self, subject):
        subject.buffs.append(self)
        subject.accuracy += self.power

    def debuff(self, subject):
        subject.accuracy -= self.power
        subject.buffs.remove(self)


class Empowered(Buff):

    def __init__(self, power, duration):
        super().__init__("gestärkt", power, duration)

    def buff(self, subject):
        subject.buffs.append(self)
        subject.damage += self.power

    def debuff(self, subject):
        subject.damage -= self.power
        subject.buffs.remove(self)


class Deadly(Buff):

    def __init__(self, power, duration):
        super().__init__('tötl.', power, duration)

    def buff(self, subject):
        subject.buffs.append(self)
        subject.critical += self.power

    def debuff(self, subject):
        subject.critical -= self.power
        subject.buffs.remove(self)


class AbilityPower(Buff):
    """Only Hero can have this attribute"""
    def __init__(self, power, duration):
        super().__init__("Magie", power, duration)

    def buff(self, subject):
        subject.buffs.append(self)
        subject.magic_power += self.power

    def debuff(self, subject):
        subject.magic_power -= self.power
        subject.buffs.remove(self)


class Stun(Buff):
    """self.power is int in percent"""
    def __init__(self, power, duration):
        super().__init__("STUN", power, duration)
        self.stun = True

    def buff(self, subject):
        subject.buffs.append(self)

    def debuff(self, subject):
        subject.buffs.remove(self)


class Barrier(Buff):

    def __init__(self, power, duration):
        super().__init__('Barriere', power, duration)

    def buff(self, subject):
        subject.buffs.append(self)
        subject.mental_reduction += self.power

    def debuff(self, subject):
        subject.mental_reduction += self.power
        subject.buffs.remove(self)


class Illusion(Buff):

    def __init__(self, power, duration):
        super().__init__("Illusion", power, duration)

    def buff(self, subject):
        subject.buffs.append(self)
        subject.dodge += self.power 
        subject.mental_reduction += self.power

    def debuff(self, subject):
        subject.mental_reduction -= self.power
        subject.dodge -= self.power
        subject.buffs.remove(self)


class Harden(Buff):

    def __init__(self, power, duration):
        super().__init__("Schild", power, duration)

    def buff(self, subject):
        subject.buffs.append(self)
        subject.reduction += self.power

    def debuff(self, subject):
        subject.reduction -= self.power
        subject.buffs.remove(self)


class Frost(Buff):

    def __init__(self, power, duration):
        super().__init__("Frost", power, duration)

    def buff(self, subject):
        subject.buffs.append(self)
        subject.speed -= self.power * 4
        subject.reduction -= self.power 

    def debuff(self, subject):
        subject.reduction += self.power
        subject.speed += self.power * 4
        subject.buffs.remove(self)


class MinusDodge(Buff):

    def __init__(self, power, duration):
        super().__init__("träge", power, duration)

    def buff(self, subject):
        subject.buffs.append(self)
        subject.dodge -= self.power

    def debuff(self, subject):
        subject.dodge += self.power
        subject.buffs.remove(self)

