
class Buff:
    
    def __init__(self, name, power, duration):
        self.name = name
        self.power = power
        self.duration = duration
        self.clear = False
        self.active = False
    
    def __repr__(self):
        return self.name
    
    def count_down(self):
        self.duration -= 1
        if self.duration == 0:
            self.clear = True


#ITEM BUFFS
class ItemBuff1(Buff):#Berserker
    def __init__(self, power, duration):
        super().__init__("berserk", power, duration)
    def buff(self, hero):
        hero.buffs.append(self)
        hero.critical += self.power * 6
        hero.damage += self.power
    def debuff(self, hero):
        hero.damage -= self.power
        hero.critical -= self.power * 6
        hero.buffs.remove(self)


class ItemBuff2(Buff):#Brand
    def __init__(self, power, duration):
        super().__init__("brand", power, duration)
        self.active = True
    def buff(self, enemy):
        enemy.buffs.append(self)
    def debuff(self, enemy):
        enemy.buffs.remove(self)
    def effekt(self, enemy):#deals x-perc of max_life as tick-dmg
        enemy.life -= round(enemy.max_life * self.power / 100)


class ItemBuff3(Buff):#Klarheit
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


#HERO BUFFS
class HeroBuff1(Buff):#START-FÄHIGKEIT
    def __init__(self, power, duration):
        super().__init__("gestärkt", power, duration)
    def buff(self, hero):
        hero.buffs.append(self)
        hero.damage += self.power
        hero.speed += self.power * 2
    def debuff(self, hero):
        hero.speed -= self.power * 2
        hero.damage -= self.power
        hero.buffs.remove(self)


class HeroBuff2(Buff):#Schild-Haltung
    def __init__(self, power, duration):
        super().__init__("schild", power, duration)
    def buff(self, hero):
        hero.buffs.append(self)
        hero.reduction += self.power
    def debuff(self, hero):
        hero.reduction -= self.power
        hero.buffs.remove(self)


#HERO DEBUFFS
class HeroDebuff1(Buff):#Verkrüppelt
    def __init__(self, power, duration):
        super().__init__("Verkrüp.", power, duration)
    def buff(self, enemy):
        enemy.buffs.append(self)
        enemy.damage -= self.power
    def debuff(self, enemy):
        enemy.damage += self.power
        enemy.buffs.remove(self)


class HeroDebuff2(Buff):#Vergiftet
    def __init__(self, power, duration):
        super().__init__("vergift.", power, duration)
        self.active = True
    def buff(self, enemy):
        enemy.buffs.append(self)
    def debuff(self, enemy):
        enemy.buffs.remove(self)
    def effekt(self, hero):
        hero.life -= self.power


class HeroDebuff3(Buff):#Frost
    def __init__(self, power, duration):
        super().__init__("frost", power, duration)
    def buff(self, enemy):
        enemy.buffs.append(self)
        enemy.speed -= self.power * 6
        enemy.reduction -= self.power 
    def debuff(self, enemy):
        enemy.reduction += self.power
        enemy.speed += self.power * 6
        enemy.buffs.remove(self)


#ENEMY BUFFS
class EnemyBuff1(Buff):#Stabil
    def __init__(self, power, duration):
        super().__init__("stabil", power, duration)
    def buff(self, enemy):
        enemy.buffs.append(self)
        enemy.reduction += self.power
    def debuff(self, enemy):
        enemy.reduction -= self.power
        enemy.buffs.remove(self)


class EnemyBuff2(Buff):#Adrenalin
    def __init__(self, power, duration):
        super().__init__("adrenal.", power, duration)
    def buff(self, enemy):
        enemy.buffs.append(self)
        enemy.speed += self.power * 4
        enemy.dodge += self.power
    def debuff(self, enemy):
        enemy.dodge -= self.power
        enemy.speed -= self.power * 4
        enemy.buffs.remove(self)


class EnemyBuff3(Buff):#Illusion
    def __init__(self, power, duration):
        super().__init__("illusion", power, duration)
    def buff(self, enemy):
        enemy.buffs.append(self)
        enemy.dodge += self.power 
        enemy.mental_reduction += self.power * 3
    def debuff(self, enemy):
        enemy.mental_reduction -= self.power * 3
        enemy.dodge -= self.power
        enemy.buffs.remove(self)


class EnemyBuff4(Buff):#WÄCHTER GOLEM
    def __init__(self):
        super().__init__("bollwerk", 20, 2)
    def buff(self, enemy):
        enemy.buffs.append(self)
        enemy.reduction += self.power
        enemy.mental_reduction += self.power
        enemy.damage += self.power / 2
    def debuff(self, enemy):
        enemy.damage -= self.power / 2
        enemy.mental_reduction -= self.power
        enemy.reduction -= self.power
        enemy.buffs.remove(self)


#ENEMY DEBUFF
class EnemyDebuff1(Buff):#Zögern
    def __init__(self, power, duration):
        super().__init__("zögern", power, duration)
    def buff(self, hero):
        hero.buffs.append(self)
        hero.damage -= self.power
        hero.speed -= self.power * 2
    def debuff(self, hero):
        hero.speed += self.power * 2
        hero.damage += self.power
        hero.buffs.remove(self)


class EnemyDebuff2(Buff):#Verlangsamt
    def __init__(self, power, duration):
        super().__init__("langsam", power, duration)
    def buff(self, hero):
        hero.buffs.append(self)
        hero.damage -= self.power
        hero.speed -= self.power * 4
    def debuff(self, hero):
        hero.speed += self.power * 4
        hero.damage += self.power
        hero.buffs.remove(self)


class EnemyDebuff3(Buff):#Feuersiegel
    def __init__(self, power, duration):
        super().__init__("Feuermal", power, duration)
        self.active = True
    def buff(self, hero):
        hero.buffs.append(self)
    def debuff(self, hero):
        hero.buffs.remove(self)
    def effekt(self, hero):
        hero.life -= self.power