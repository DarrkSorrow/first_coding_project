import pygame
from time import sleep


class CombatLog:

    def __init__(self, screen, font):

        self.messages = []
        self.screen = screen
        self.font = font


    def add(self, text, isEnemy=False):

        text_tuple = (text, isEnemy)
        self.messages.append(text_tuple)
        self.draw()

        if len(self.messages) > 10:
            self.messages.pop(0)
        
        pygame.display.flip(), sleep(1.3)


    def draw(self):

        pygame.draw.rect(
            self.screen, (30, 30, 30), (0, 0, 420, 260))

        pygame.draw.rect(
            self.screen, (255, 255, 255), (0, 0, 420, 260), 2)
        
        y = 240
        #line is tuple (text, isEnemy)
        for line in reversed(self.messages[-10:]):
            if line[1] == True:
                text = self.font.render(line[0], True, (255, 123, 123))
            else:#Text gets rendered in white or red depending on isEnemy
                text = self.font.render(line[0], True, (255, 255, 255))

            self.screen.blit(text, (5, y))

            y -= 25


class Button:

    def __init__(self, x, y, width, height, text, key):

        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.key = key
        self.image = None


    def draw(self, screen, font):

        pygame.draw.rect(
            screen, (100, 100, 100), self.rect)

        pygame.draw.rect(
            screen, (255, 255, 255), self.rect, 2)

        lines = self.text.split("\n")    #text can be split with \n
        line_height = font.get_height()  #pygame render can only handle str type
        total_height = len(lines) * line_height
        start_y = self.rect.centery - total_height / 2 + line_height / 2

        for i, line in enumerate(lines):
        
            text_surface = font.render(
                line,
                True,
                (255, 255, 255))

            text_rect = text_surface.get_rect(
                center=(
                    self.rect.centerx,
                    start_y + i * line_height))

            if self.image is not None:
                screen.blit(self.image, self.rect)
                screen.blit(text_surface, text_rect)
            else:
                screen.blit(text_surface, text_rect)

    def clicked(self, mouse_position):

        return self.rect.collidepoint(mouse_position)


def boss_reward_and_buttons(hero, screen):

    font = pygame.font.SysFont(None, 34)
    text = 'DU HAST GESIEGT!'
    y = display_text(text, 75, screen, font)
    text = 'Wähle deine Belohnung'
    y = display_text(text, y, screen, font)

    life_reward = Button(150, 350,
        250, 100, '+100 Max-Hp, +10 Res', "1")
    
    mana_reward = Button(750, 350,
        250, 100, "+100 Max-Odem, +10 MentalRes.", "2")
    
    extra_item_slot = Button(150, 600,
        250, 100, "+1 Inventarplatz", "3")

    extra_ability_slot = Button(750, 600,
        250, 100, "+1 Fähigkeitensockel", "4")

    buttons = [life_reward, mana_reward, extra_item_slot,
               extra_ability_slot]

    return buttons


def display_text(text, y, screen, font):

    textrend = font.render(text, True, (0, 0, 0))
    screen.blit(textrend, (100, y))
    pygame.display.flip(), sleep(1.8)
    y += 32
    return y


def bond_fire_buttons(hero):
#from world
    button_heal = Button(475, 450,
    250, 70, f"+{round(hero.max_life / 2)} HP", "1")

    button_mana = Button(275, 600,
    250, 70, f"+{hero.max_mana} Odem", "2")

    button_xp = Button(675, 600,
    250, 70, f"+{round(hero.xp * 0.5)} XP", "3")

    buttons = [button_heal, button_mana, button_xp]

    return buttons


def merchant_buttons(hero, screen):

    abilities_displayed(hero, screen)
    
    i = len(hero.inventory) + len(hero.pockets)
    consumable_1 = Button(750, 700,
                    120, 70, '', i + 1)
    consumable_2 = Button(900, 700, 
                    120, 70, '', i + 2)
    consumable_3 = Button(1050, 700,
                    120, 70, '', i + 3)
    gear_1 = Button(900, 600,
                    120, 70, '', i + 4)
    gear_2 = Button(1050, 600,
                    120, 70, '', i + 5)
    spell = Button(1000, 500,
                   180, 70, '', i + 6)
    shop_exit = Button(1050, 30,
                    120, 70, '', i + 7)
    shop_offering = [consumable_1, consumable_2, consumable_3,
                     gear_1, gear_2, spell, shop_exit]

    hero_inventory = dungeon_inventory(hero, screen)

    return shop_offering, hero_inventory


def yes_no_button(screen, font):
#from abilities, world uses it too now
    yes = Button(300, 500, 
        100, 100, "JA", "1")
    
    no = Button(500, 500,
        100, 100, "NEIN", "2")
    
    buttons = [yes, no]

    for button in buttons:
        button.draw(screen, font)

    pygame.display.flip()
    return buttons


def display_answers(answers, screen):
#From event
    font = pygame.font.SysFont(None, 24)

    button_1 = Button(200, 500,
    900, 50, " ", "1")

    button_2 = Button(200, 550,
    900, 50, " ", "2")

    button_3 = Button(200, 600,
    900, 50, " ", "3")

    button_4 = Button(200, 650,
    900, 50, " ", "4")

    buttons = [button_1, button_2, button_3, button_4]

    while len(buttons) != len(answers):
        del buttons[-1]

    i = 0
    for button in buttons:
        answer = answers[i]
        button.text = answer
        button.draw(screen, font)
        i += 1
    
    return buttons


def buttons_right_bottom_corn():

    font = pygame.font.SysFont(None, 20)

    attack_button = Button(840, 560,
                           180, 80, "Angreifen", "0")
    defend_button = Button(1020, 560,
                           180, 80, "Verteidigen", "1")
    ability_button = Button(840, 640,
                            180, 80, "Fähigkeiten", "2")
    inventory_button = Button(1020, 640,
                              180, 80, "Inventar", "3")
    extra_1 = Button(840, 720,
                     180, 80, "", "4")
    extra_2 = Button(1020, 720,
                     180, 80, "", "5")
    extra_3 = Button(660, 560,
                     180, 80, "", "6")
    extra_4 = Button(660, 640,
                     180, 80, "", "7")
    extra_5 = Button(660, 720,
                     180, 80, "", "8")

    buttons = [attack_button, defend_button, ability_button,
            inventory_button, extra_1, extra_2, extra_3,
            extra_4, extra_5]

    return buttons, font


def choose_ability(hero, action, screen):

    buttons, font = buttons_right_bottom_corn()
    button_keys = ("a", "b", "c", "d")

    for button, key in zip(buttons, button_keys):
        button.key = key# button.key must be in abcd

    while len(buttons) != len(hero.abilities):
        del buttons[-1]
    
    for i, button in enumerate(buttons):
        spell = hero.abilities[i]
        button.text = f"{spell.name}\n"
        button.text += f"ODEM:({str(spell.cost)})\n"
        if spell.cool_down > 0:
            button.text += f"COOLD.({str(spell.cool_down)})"

    for button in buttons:
        button.draw(screen, font)

    pygame.display.flip()

    action = display_answers_clicked(buttons)
    return action


def item_buttons(hero, screen):
#from world
    buttons, font = buttons_right_bottom_corn()

    i = 0
    for item in hero.inventory:
        buttons[i].text = item.name
        buttons[i].key = i
        buttons[i].draw(screen, font)
        i += 1

    for x, item in enumerate(hero.pockets):
        buttons[i].text = item.name
        buttons[i].key = hero.max_inventory + x
        buttons[i].draw(screen, font)
        i += 1
    
    while len(buttons) != len(hero.inventory) + len(hero.pockets):
        del buttons[-1]

    return buttons


def item_in_combat(hero, enemy, screen):

    buttons, font = buttons_right_bottom_corn()

    i = 0
    for item in hero.inventory:
        if item.active:
            buttons[i].text = item.name
            buttons[i].key = i
            buttons[i].draw(screen, font)
            i += 1

    for x, item in enumerate(hero.pockets):
        buttons[i].text = item.name
        buttons[i].key = hero.max_inventory + x
        buttons[i].draw(screen, font)
        i += 1

    while len(buttons) != i:
        del buttons[-1]

    pygame.display.flip()
    item = display_answers_clicked(buttons)
    return int(item)


def choose_item(hero, screen):
#from event
    buttons, font = buttons_right_bottom_corn()
    
    while len(buttons) != len(hero.inventory) + len(hero.pockets):
        del buttons[-1]
   
    i = 0
    for button in buttons:
        if i < hero.max_inventory:
            item = hero.inventory[i]
        else:
            item = hero.pockets[i - hero.max_inventory]
        button.text = item.name
        button.draw(screen, font)
        i += 1
    pygame.display.flip()

    return buttons


def combat_buttons(screen):
    """Attack, defense, ability, item"""
    buttons, font = buttons_right_bottom_corn()

    while len(buttons) != 4:#4 general buttons,
        del buttons[-1]     #they dont change at all

    for button in buttons:
        button.draw(screen, font)
    pygame.display.flip()

    action = display_answers_clicked(buttons)
    return action


def dungeon_inventory(hero, screen):

    font = pygame.font.SysFont(None, 20)
    buttons = []
    c, i, x, y = 0, 0, 1095, 255

    for slot in range(hero.max_inventory + hero.pocket_size):

        pygame.draw.rect(screen, (100, 100+c, 250-c),
                         (x, y, 50, 50))#Empty Slots
        
        if i < len(hero.inventory):
            button = Button(x, y,
                50, 50, " ", f"{str(i)}")
            item = hero.inventory[i]
            button.image = item.image
            button.text = item.symbol
            button.draw(screen, font)
            buttons.append(button)

        elif 0 <= i - hero.max_inventory < len(hero.pockets):
            button = Button(x, y,
                50, 50, " ", f"{str(i)}")
            item = hero.pockets[i - hero.max_inventory]
            button.image = item.image
            button.text = item.symbol
            button.draw(screen, font)
            buttons.append(button)
        
        i += 1
        if slot % 2 == 0:
            x += 50
        else:
            x -= 50
            y += 50

        if i == hero.max_inventory:
            c += 150#changes rgb tupel in this func
    
    return buttons


def abilities_displayed(hero, screen):

    x, y = 380, 715
    for slot in range(hero.max_abilities):#SLOTS
        pygame.draw.rect(screen, (250, 100, 100),
                         (x, y, 65, 65))

        if slot < len(hero.abilities):#ABILITIES
            ability = hero.abilities[slot]
            ability.draw(screen, x, y)

            if hero.abilities[slot].cool_down > 0:#displays cooldown
                font = pygame.font.SysFont(None, 40)
                overlay = pygame.Surface((65, 65), pygame.SRCALPHA)
                overlay.fill((100, 100, 200, 150))
                screen.blit(overlay, (x, y))
                text = str(hero.abilities[slot].cool_down)
                text = font.render(str(hero.abilities[slot].cool_down),
                                    True, (255, 255, 255))
                screen.blit(text, (x+25, y+20))#centers cooldown-number 

        x += 65
    

def dungeon_buttons_clicked(hero, buttons, screen, event):

    font = pygame.font.SysFont(None, 20)
    
    for button in buttons:
        if button.clicked(event.pos):
            i = int(button.key)
            if i >= len(hero.inventory):
                item = hero.pockets[i - hero.max_inventory]
            else:
                item = hero.inventory[i]
            if item.dungeon:
                item.use_item(hero, None, None)


def display_answers_clicked(buttons):
    """returns button.key if pressed"""
    choice = " "
    while choice == " ":
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.clicked(event.pos):
                        choice = button.key
    return choice
