import pygame
from time import sleep
import random
import world, items, abilities, buttons_clog
from combat import hero_combat_stats


def start_event(hero, stage, screen):

    if stage == 0: #START ITEM
        event = event_0
        #increases eventStreak
        hero.game_state.events_in_row += 1
        hero.game_state.enemy_counter = 0 # reset
        event(hero, screen)
    
    elif stage > 0:
        magic_number = random.randint(1, 10)
        #b2b events, increases ambushChance
        magic_number += hero.game_state.events_in_row * 2
        if magic_number >= 10:
            return True
        else:
            events = (event_1, event_2, event_3, event_4, event_5,
                      event_6, event_7, event_8)
            event = random.choice(events)
            #no b2b same events
            while event in hero.game_state.last_events:
                event = random.choice(events)
            #saves last 3 events to not be repeated
            hero.game_state.last_events.append(event)
            #increases eventStreak
            hero.game_state.events_in_row += 1
            hero.game_state.enemy_counter = 0 # reset
            event(hero, screen)


def event_get_item(hero, item, screen):

    screen.fill((50, 50, 50))
    pygame.display.flip(), sleep(1)
    font = pygame.font.SysFont(None, 28)
    y = 100
    world.get_item(hero, item, screen, font, y)


def construct_intro(hero, intro, screen):

    screen.fill((255, 255, 0))
    world.hero_health_bar(hero, screen)
    world.hero_mana_bar(hero, screen)
    world.hero_xp
    hero_combat_stats(hero, screen)
    buttons_clog.dungeon_inventory(hero, screen)
    font = pygame.font.SysFont(None, 28)
    y = 100

    for i in intro:
         
        text = font.render(i, True, (0, 0, 0))
        screen.blit(text, (100, y))
        y += 32
        pygame.display.flip()
        sleep(1.7)


def display_outro(hero, raw_text, y, screen, font):

    world.hero_health_bar(hero, screen)
    world.hero_mana_bar(hero, screen)
    world.hero_xp
    text = font.render(raw_text, True, (0, 0, 0))
    screen.blit(text, (100, y))
    pygame.display.flip(), sleep(1.7)
    y += 32
    return y


def event_0(hero, screen):
    
    start = "Du kannst einen Gegenstand an dich nehmen."
    a = "Wähle mit Bedacht."

    intro = [start, a]

    item_1 = items.random_gear()
    item_2 = items.random_gear()
    while item_1.name == item_2.name:
        item_2 = items.random_gear()

    choice_1 = (f"{item_1.name}")
    choice_2 = (f"{item_2.name}")
    answers = [choice_1, choice_2]

    font = pygame.font.SysFont(None, 28)
    construct_intro(hero, intro, screen)
    buttons = buttons_clog.display_answers(answers, screen)
    pygame.display.flip()

    screen.fill((255, 255, 0))
    y = 100
    choice = buttons_clog.display_answers_clicked(buttons)
    match choice:
        case "1":
            item = item_1
            event_get_item(hero, item, screen)
        case "2":
            item = item_2
            event_get_item(hero, item, screen)
    return None


#Akt1 
def event_1(hero, screen):

    start = f"{hero.name} marschiert schnellen Fußes durch fremde Landschaften. "
    a = "Er stößt auf ein verlassenes Grubenhaus etwas abseits der Wege "
    b = "und entschließt sich das Gebäude zu untersuchen. "
    c = "Ihm ströhmt ein wohliger aromatischer Geruch entgegen, "
    d = "denn es steht eine kleine Holzwanne, mit warmem Aufguss, "
    e = "in dem, nun einladend aussehendem, Haus."

    intro = [start, a, b, c, d, e]

    choice_1 = ("1: Eine leere Phiole von den Regalen nehmen und"
        " sie mit dem Aufguss befüllen.")
    choice_2 = ("2: Sich entkleiden und in die Wanne steigen.") 
    answers = [choice_1, choice_2]
    
    font = pygame.font.SysFont(None, 28)
    construct_intro(hero, intro, screen)
    buttons = buttons_clog.display_answers(answers, screen)
    pygame.display.flip()
    screen.fill((255, 255, 0))
    y = 100

    choice = buttons_clog.display_answers_clicked(buttons)

    match choice:
        case "1":
            raw_text = "Du machst die Phiole voll und gehst weiter.."
            y = display_outro(hero, raw_text, y, screen, font)
            item = items.Item1()
            event_get_item(hero, item, screen)

        case "2":
            magic_number = random.choice((1, 2, 3))
            match magic_number:
                case 1:
                    hero.life = hero.max_life
                    raw_text = "Das Bad wirkt vitalisierend und kräftigt deinen Körper"
                    display_outro(hero, raw_text, y, screen, font)
                case 2:
                    hero.max_mana += 2
                    hero.mana = hero.max_mana
                    raw_text = "Das wohltuende Bad inspiriert dich über alle Maße."
                    display_outro(hero, raw_text, y, screen, font)
                case 3:
                    hero.life -= 12
                    raw_text = f"{hero.name} bekommt besorgniserregenden Ausschlag!"
                    display_outro(hero, raw_text, y, screen, font)
    return None


def event_2(hero, screen):

    start = f"In der entfernung zeichnen sich Umrisse eines Mannes, im Dunst, ab. "
    a = f"{hero.name} und der Fremde näheren sich immer mehr an, " 
    b = "der Dunst schwindet und der Fremde scheint freundlich gesinnt. "
    c = ' "Hey Fremder, was ist dir wichtiger? Macht oder Wissen?" '

    intro = [start, a, b, c]

    choice_1 = "1: Macht (+ KLEINE BRANDBOMBE)"
    choice_2 = "2: Wissen (+ XP)"
    answers = [choice_1, choice_2]

    font = pygame.font.SysFont(None, 28)
    construct_intro(hero, intro, screen)
    buttons = buttons_clog.display_answers(answers, screen)
    pygame.display.flip()
    screen.fill((255, 255, 0))
    y = 100

    choice = buttons_clog.display_answers_clicked(buttons)

    match choice:
        case "1":
            raw_text = f"Der Fremde zwinkert und drückt {hero.name} etwas in die Hand."
            y = display_outro(hero, raw_text, y, screen, font) 
            item = items.Item3()
            raw_text = 'Der Fremde geht weiter...'
            display_outro(hero, raw_text, y, screen, font)
            event_get_item(hero, item, screen)

        case "2":
            raw_text = f"{hero.name} blinzelt und es scheint als wäre der Fremde nie da gewesen."
            y = display_outro(hero, raw_text, y, screen, font)
            raw_text = "+60 XP"
            y = display_outro(hero, raw_text, y, screen, font)
            hero.xp += 60
            raw_text = f'{hero.name} geht weiter...'
            display_outro(hero, raw_text, y, screen, font)
    return None


def event_3(hero, screen):

    start = f"{hero.name} geht, in einer kleinen Siedlung, eine kleine Treppe "
    a = "hinunter was so aussieht wie eine Schenke. Es wirkt schummrig "
    b = f"doch {hero.name} findet einen gemütlichen Platz für sich. "
    c = "In einer der hinteren Ecken siehst du Männer hockend und schreiend "
    d = "um einen Hahnenkampf versammelt. "
    e = '"NEUE RUNDE NEUE EINSÄTZE!!! NEUE RUNDE NEUE EINSÄTZE!!!"'

    intro = [start, a, b, c, d, e]

    choice_1 = "1: Nicht wetten. Deines Weges gehen."
    choice_2 = "2: Einsatz abgeben (Wähle ein Item aus deinem Inventar)"
    answers = [choice_1, choice_2]
    
    font = pygame.font.SysFont(None, 28)
    construct_intro(hero, intro, screen)
    buttons = buttons_clog.display_answers(answers, screen)
    pygame.display.flip()
    screen.fill((255, 255, 0))
    y = 100

    choice = buttons_clog.display_answers_clicked(buttons)

    match choice:
        case "1":
            raw_text = f"{hero.name} schaut noch eine Weile zu und beobachtet das Treiben."
            display_outro(hero, raw_text, y, screen, font)
            return None #Prevents rst of code to be exec.
        
        case "2":
            if hero.inventory == []:
                raw_text = f"Der Buchmacher akzeptiert {hero.name}'s paar Kupferlinge nicht."
                y = display_outro(hero, raw_text, y, screen, font)
                raw_text = f"{hero.name} geht, nach einer Weile, seines Weges."
                y = display_outro(hero, raw_text, y, screen, font)
                return None #Prevents rst of code to be exec.
            else:
                raw_text = "Welchen Gegenstand als Einsatz setzen?"
                y = display_outro(hero, raw_text, y, screen, font)
                buttons = buttons_clog.choose_item(hero, screen)
                choice = " "
                while choice not in range(len(hero.inventory)):
                    choice = buttons_clog.display_answers_clicked(buttons)
                    choice = int(choice)
                hero.inventory[choice].unequip(hero)
                raw_text = f"{hero.name} hat seinen Einsatz abgegeben."
                y = display_outro(hero, raw_text, y, screen, font)
    
    raw_text = "Die Hühner kämpfen!!!"
    y = display_outro(hero, raw_text, y, screen, font)
    magic_number = random.randint(0, 10)
    if magic_number <= 3:
        raw_text = "Das Huhn, auf das du gesetzt hast, siegte!!"
        y = display_outro(hero, raw_text, y, screen, font)
        raw_text = "Der Buchmacher überreicht dir den Hauptpreis."
        y = display_outro(hero, raw_text, y, screen, font)
        prize_pool = (items.SimpleWarmogs(), items.SimpleArmor(), items.LifeStone())
        item = random.choice(prize_pool)
        event_get_item(hero, item, screen)
    else:
        raw_text = "Leider verloren..."
        y = display_outro(hero, raw_text, y, screen, font)
        raw_text = "Du ziehst von Dannen und schwörst dem Glückspiel ab."
        y = display_outro(hero, raw_text, y, screen, font)
    return None


def event_4(hero, screen):

    start = f"{hero.name} erreicht eine kleine Lichtung tief im Wald. "
    a = "In ihrer Mitte erhebt sich ein uralter steinerner Altar, "
    b = "überwuchert von Moos und den Wurzeln längst vergessener Bäume. "
    c = "Auf der Opferplatte liegen einige alte Goldmünzen. "
    d = "Daneben steht eine schlichte Tonschale, gefüllt mit einer "
    e = "dunklen, leicht schimmernden Flüssigkeit. "
    f = '...Jeder Wunsch verlangt seinen Preis...'

    intro = [start, a, b, c, d, e, f]

    choice_1 = "1: Aus der Schale trinken."
    choice_2 = "2: Die Goldmünzen an dich nehmen."
    choice_3 = "3: Den Altar respektvoll verlassen."
    answers = [choice_1, choice_2, choice_3]

    font = pygame.font.SysFont(None, 28)
    construct_intro(hero, intro, screen)
    buttons = buttons_clog.display_answers(answers, screen)
    pygame.display.flip()
    screen.fill((255, 255, 0))
    y = 100

    choice = buttons_clog.display_answers_clicked(buttons)

    match choice:
        case "1":
            magic_number = random.randint(1, 3)
            match magic_number:
                case 1:
                    hero.life += 50
                    if hero.life > hero.max_life:
                        hero.life = hero.max_life
                    raw_text = "Der Trank erfüllt deinen Körper mit neuer Lebenskraft."
                    y = display_outro(hero, raw_text, y, screen, font)
                case 2:
                    hero.max_mana += 2
                    hero.mana += 50
                    if hero.mana > hero.max_mana:
                        hero.mana = hero.max_mana
                    raw_text = "Ein warmer Schauer durchströmt deinen Geist."
                    y = display_outro(hero, raw_text, y, screen, font)
                case 3:
                    hero.life -= 8
                    raw_text = "Der Trank war verdorben!"
                    y = display_outro(hero, raw_text, y, screen, font)
                    if hero.life <= 0:
                        raw_text = f"{hero.name} bricht regungslos zusammen..."
                        display_outro(hero, raw_text, y, screen, font)

        case "2":
            magic_number = random.randint(0, 10)
            if magic_number <= 4:
                raw_text = "Zwischen den Münzen findest du einen wertvollen Gegenstand."
                y = display_outro(hero, raw_text, y, screen, font)
                item = items.random_item()
                event_get_item(hero, item, screen)
            elif magic_number <= 9:
                raw_text = "Die Münzen zerfallen augenblicklich zu Staub."
                y = display_outro(hero, raw_text, y, screen, font)
                raw_text = "Offenbar war der Schatz niemals echt."
                display_outro(hero, raw_text, y, screen, font)
            else:
                raw_text = "Der Boden beginnt zu beben!"
                y = display_outro(hero, raw_text, y, screen, font)
                raw_text = "Der Altar fordert seinen Tribut."
                y = display_outro(hero, raw_text, y, screen, font)
                damage = int(hero.life * 0.3)
                hero.life -= damage
                raw_text = f"-{damage} Leben"
                display_outro(hero, raw_text, y, screen, font)

        case "3":
            raw_text = "Du verbeugst dich leicht vor dem uralten Monument."
            y = display_outro(hero, raw_text, y, screen, font)
            raw_text = "Als du den Wald verlässt, fühlst du dich merkwürdig klar."
            y = display_outro(hero, raw_text, y, screen, font)
            hero.xp += 40
            raw_text = "+40 XP"
            display_outro(hero, raw_text, y, screen, font)
    return None


def event_5(hero, screen):

    start = f"{hero.name} erblickt einen steinernen Torbogen, "
    a = "der scheinbar mitten im Nichts errichtet wurde. "
    b = "Unter dem Tor sitzt eine verhüllte Gestalt regungslos auf einem Hocker. "
    c = 'Als du näher kommst, hebt sie langsam den Kopf. '
    d = '"Hey Jungchen soll ich dir ein Geheimnis verraten..." '
    e = '[Ein Teil deiner Lebenskraft gegen Wissen, das nur Wenige besitzen.]'

    intro = [start, a, b, c, d, e]

    choice_1 = "1: Den Handel eingehen. (-6 MAX HP, lerne eine Fähigkeit)"
    choice_2 = "2: Das Angebot ablehnen und weiterziehen."
    answers = [choice_1, choice_2]

    font = pygame.font.SysFont(None, 28)
    construct_intro(hero, intro, screen)
    buttons = buttons_clog.display_answers(answers, screen)
    pygame.display.flip()
    screen.fill((255, 255, 0))
    y = 100

    choice = buttons_clog.display_answers_clicked(buttons)

    match choice:
        case "1":
            hero.max_life -= 6
            if hero.life > hero.max_life:
                hero.life = hero.max_life
            raw_text = "Die Gestalt legt ihre kalte Hand auf deine Stirn. "
            y = display_outro(hero, raw_text, y, screen, font)
            raw_text = "Ein stechender Schmerz durchfährt deinen Körper."
            y = display_outro(hero, raw_text, y, screen, font)
            raw_text = "-6 MAX HP"
            y = display_outro(hero, raw_text, y, screen, font)
            raw_text = "Doch zugleich strömt fremdes Wissen in deinen Geist."
            y = display_outro(hero, raw_text, y, screen, font)
            raw_text = "Als du wieder zu dir kommst, ist der Torbogen verlassen."
            y = display_outro(hero, raw_text, y, screen, font)

            already_learned = False
            for ability in hero.abilities:
                if isinstance(ability, abilities.Ability1):
                    already_learned = True

            if already_learned:
                raw_text = '"...Ich spüre du bist der Auserwählte..."'
                y = display_outro(hero, raw_text, y, screen, font)
                raw_text = '"...Ich lehre dich die wahre Technik..."'
                y = display_outro(hero, raw_text, y, screen, font)
                ability = abilities.Ability5()
            else:
                ability = abilities.Ability1()
            abilities.abilities_from_events(hero, ability, screen)

        case "2":
            raw_text = f"{hero.name} bedankt sich höflich und geht weiter."
            y = display_outro(hero, raw_text, y, screen, font)
            raw_text = 'Noch in der Ferne hallt seine Stimme nach: '
            y = display_outro(hero, raw_text, y, screen, font)
            raw_text = '"Nicht jeder erkennt eine Gelegenheit..."'
            display_outro(hero, raw_text, y, screen, font)
    return None


def event_6(hero, screen):

    start = f"{hero.name} erreicht einen verlassenen Wachposten. "
    a = "Am alten Wachposten stehen Händler nebeneinander aufgebaut. "
    b = "Ein Händler hat es mit seinen Waren,"
    c = f"{hero.name} besonders angetan."
    d = 'Als du näher kommst, siehst du ein wetter gegärbtes freundliches Gesicht.'
    e = '"Ich handle nicht mit Gold... nur mit Dingen von wahrem Wert."'

    intro = [start, a, b, c, d, e]

    choice_1 = "1: Du misstraust dem Angebot und lehnst dankend ab."
    choice_2 = '2: Einen "Tropfen" Blut eintauschen. (-16 HP und -4 MAX-HP)'
    answers = [choice_1, choice_2]

    for item in hero.inventory:
        if isinstance(item, items.SimpleWarmogs):
            choice_3 = ("3: Dem Händler den seltenen Gegenstand zeigen (Rüstung der Lebenskraft).")
            answers.append(choice_3)
            break

    font = pygame.font.SysFont(None, 28)
    construct_intro(hero, intro, screen)
    buttons = buttons_clog.display_answers(answers, screen)
    pygame.display.flip()
    screen.fill((255, 255, 0))
    y = 100

    choice = buttons_clog.display_answers_clicked(buttons)

    match choice:
        case "1":
            raw_text = "Der Händler nickt dir schweigend zu."
            y = display_outro(hero, raw_text, y, screen, font)
            raw_text = f"{hero.name} setzt seinen Weg fort."
            display_outro(hero, raw_text, y, screen, font)

        case "2":
            hero.life -= 16
            hero.max_life -= 4
            if hero.life < 1:
                hero.life = 1
            raw_text = "Der Händler ritzt dir mit einer feinen Nadel in den Finger."
            y = display_outro(hero, raw_text, y, screen, font)
            raw_text = '"Ein fairer Handel.", murmelt der Alte und durchsucht seinen Karren.'
            y = display_outro(hero, raw_text, y, screen, font)
            item = items.RitualDagger()
            event_get_item(hero, item, screen)

        case "3":
                raw_text = "Die Augen des Händlers beginnen zu leuchten."
                y = display_outro(hero, raw_text, y, screen, font)
                raw_text = '"Ein Artefakt aus der Kluft der Beschwörer."'
                y = display_outro(hero, raw_text, y, screen, font)
                for item in hero.inventory: ##trade item
                    if isinstance(item, items.SimpleWarmogs):
                        item.unequip(hero)
                        break #trade item
                raw_text = ("Der Händler nimmt den Gegenstand entgegen ")
                y = display_outro(hero, raw_text, y, screen, font)
                raw_text = ("und reicht dir stattdessen einen sorgfältig eingewickelten Dolch.")
                y = display_outro(hero, raw_text, y, screen, font)
                item = items.RitualDagger()
                event_get_item(hero, item, screen)
    return None


def event_7(hero, screen):

    start = f"{hero.name} erkennt in den Büschen den Schein eines kleinen Feuers. "
    a = "Daneben sitzt ein erschöpfter Mann in einer zerschlissenen Robe. "
    b = "Vor ihm stehen einige leere Phiolen und getrocknete Kräuter. "
    c = f"Als {hero.name} näher kommt, hebt der Fremde langsam den Kopf. "
    d = '"Du siehst aus, als könntest du etwas Hilfe gebrauchen."'
    e = '"Mal sehen, was wir noch tun können."'

    intro = [start, a, b, c, d, e]

    choice_1 = "1: Den heilenden Trank trinken. (+65 Leben)"
    choice_2 = "2: Die Kräuter des Heilers einnehmen. (+4 Max. Leben)"
    choice_3 = "3: Die schnelle Heilung erlernen. (-40 Speed)"
    answers = [choice_1, choice_2, choice_3]

    font = pygame.font.SysFont(None, 28)
    construct_intro(hero, intro, screen)
    buttons = buttons_clog.display_answers(answers, screen)
    pygame.display.flip()
    screen.fill((255, 255, 0))
    y = 100

    choice = buttons_clog.display_answers_clicked(buttons)

    match choice:
        case "1":
            hero.life += 65
            if hero.life > hero.max_life:
                hero.life = hero.max_life
            raw_text = "Der Heiler reicht dir die Schale zum trinken. "
            y = display_outro(hero, raw_text, y, screen, font)
            raw_text = "Ein wohltuendes Gefühl überkommt dich."
            y = display_outro(hero, raw_text, y, screen, font)
            raw_text = "+65 Leben"
            display_outro(hero, raw_text, y, screen, font)

        case "2":
            hero.max_life += 4
            raw_text = "Du kaust die bitteren Kräuter des Heilers. "
            y = display_outro(hero, raw_text, y, screen, font)
            raw_text = "Dein Körper fühlt sich kräftiger an."
            y = display_outro(hero, raw_text, y, screen, font)
            raw_text = "+4 Max. Leben"
            display_outro(hero, raw_text, y, screen, font)

        case "3":
            hero.speed -= 40
            if hero.speed < 0:
                hero.speed = 0
            raw_text = f"{hero.name} lernt mit dem Fremden die Heilkunst."
            y = display_outro(hero, raw_text, y, screen, font)
            raw_text = "Es dauerte so lange"
            y = display_outro(hero, raw_text, y, screen, font)
            raw_text = "es kam dir vor wie ein Jahrzehnt. "
            y = display_outro(hero, raw_text, y, screen, font)
            raw_text = "-40 Speed"
            y = display_outro(hero, raw_text, y, screen, font)
            ability = abilities.Ability9()
            abilities.abilities_from_events(hero, ability, screen)
    return None


def event_8(hero, screen):

    start = f"{hero.name} wandert auf einer gut befestigten Straße, "
    a = "auf dem ihm ein schwer beladener Händler entgegenkommt. "
    b = "Nach einem kurzen Gespräch bemerkt der Händler, "
    c = "dass er einen ungewöhnlichen Gegenstand bei sich trägt. "
    d = f"{hero.name} interessiert sich sofort für diesen Gegenstand. "
    e = '"Ein seltenes Stück. Ich habe lange gebraucht, um es zu finden."'

    intro = [start, a, b, c, d, e]

    his_jam = items.Item5 #Berserker Blut
    choice_1 = "1: Du interessierst dich doch nicht für das Artefakt."
    choice_2 = f'Dem Händler {his_jam.item_name} überlassen.'
    choice_3 = 'Den Händler mit Pyromagie beeindrucken.'
    choice_4 = "3: Das Item rauben.(min 65 Spd)"
    answers = [choice_1, choice_2, choice_3, choice_4]

    font = pygame.font.SysFont(None, 28)
    construct_intro(hero, intro, screen)
    buttons = buttons_clog.display_answers(answers, screen)
    pygame.display.flip()
    screen.fill((255, 255, 0))
    y = 100

    choice = buttons_clog.display_answers_clicked(buttons)

    got_item = True
    match choice:
        case "1":
            raw_text = f"{hero.name} hat es sich anders überlegt."
            y = display_outro(hero, raw_text, y, screen, font)
            raw_text = f"{hero.name} fragt den Händler noch nach dem Weg."
            display_outro(hero, raw_text, y, screen, font)
            got_item = False

        case "2":
            item_given = False
            for item in hero.inventory: #trade item
                if isinstance(item, his_jam):
                    item.unequip(hero)
                    raw_text = "Der Händler erwägt dein Angebot mit Interesse."
                    y = display_outro(hero, raw_text, y, screen, font)
                    raw_text = "Sag niemandem, dass ich sowas besitze."
                    y = display_outro(hero, raw_text, y, screen, font)
                    raw_text = "Ich kann damit gut Dampf ablassen!"
                    y = display_outro(hero, raw_text, y, screen, font)
                    item_given = True
                    break #trade item
            if not item_given:
                raw_text = 'Du durchsuchst deine Taschen,'
                y = display_outro(hero, raw_text, y, screen, font)
                raw_text = 'Aber kannst nichts finden, '
                y = display_outro(hero, raw_text, y, screen, font)
                raw_text = 'was den Händler interessiert.'
                y = display_outro(hero, raw_text, y, screen, font)
                got_item = False

        case "3":
            trick_shown = False
            for spell in hero.abilities:
                if isinstance(spell, abilities.Ability4):
                    hero.mana -= 5
                    if hero.mana < 0:
                        hero.mana = 0
                    raw_text = "Der Händler ist entzückt von deinem Zauber."
                    y = display_outro(hero, raw_text, y, screen, font)
                    raw_text = '"So etwas habe ich noch nie gesehen! '
                    y = display_outro(hero, raw_text, y, screen, font)
                    raw_text = '"Weist du was, ich gebe dir den Helm!"'
                    y = display_outro(hero, raw_text, y, screen, font)
                    trick_shown = True
                    break
            if not trick_shown:
                raw_text = f'{hero.name} verucht den Händler zu bespaßen'
                y = display_outro(hero, raw_text, y, screen, font)
                raw_text = 'Der Händler zeigt sich aber unbeeindruckt.'
                y = display_outro(hero, raw_text, y, screen, font)
                got_item = False

        case "4":
            if hero.speed >= 65:
                raw_text = f"{hero.name} erkennt seine Chance."
                y = display_outro(hero, raw_text, y, screen, font)
                raw_text = "Mit einem schnellen Griff entreißt du dem Händler "
                y = display_outro(hero, raw_text, y, screen, font)
                raw_text = "den Helm und rennst so schenll du kannst davon."
                y = display_outro(hero, raw_text, y, screen, font)
            else:
                raw_text = f'{hero.name} überlegt kurz, entscheidet sich '
                y = display_outro(hero, raw_text, y, screen, font)
                raw_text = f'jedoch dagegen, {hero.name} hat nicht'
                y = display_outro(hero, raw_text, y, screen, font)
                raw_text = 'genügend Vertrauen in seine Fähigkeiten.'
                y = display_outro(hero, raw_text, y, screen, font)
                got_item = False
    if got_item:
        item = items.KhansHat()
        event_get_item(hero, item, screen)
    else:
        raw_text = 'Der Händler wippt nervös hin und her.'
        y = display_outro(hero, raw_text, y, screen, font)
        raw_text = '"Ich glaube ich sollte gehen. Bis dann!"'
        y = display_outro(hero, raw_text, y, screen, font)
        raw_text = 'Zügig entfernt sich der Händler von dir.'
        y = display_outro(hero, raw_text, y, screen, font)
    return None


#Akt 2
def event_9(hero, screen):

    start = 'In den Gassen der Stadt trifft du auf zwielichtige Gestalten'
    a = 'Sie greifen dich nicht an mustern dich aber genau'
    b = 'Einer von ihnen spricht dich an:'
    c = '"Hey, hast du Lust auf einen Kampf?!"'
    d = '"Keine Sorge kleiner, wir kämpfen fair."'

    intro = [start, a, b, c, d]

    choice_1 = 'Du lehnst ab und versuchst zügig dich wieder zu entfernen.'
    choice_2 = 'Du akzeptierst den Kampf und machst dich bereit!'
    choice_3 = 'Du forderst seinen größeren stärkeren Kollegen heraus.[Elite] '
    answers = [choice_1, choice_2, choice_3]

    font = pygame.font.SysFont(None, 28)
    construct_intro(hero, intro, screen)
    buttons = buttons_clog.display_answers(answers, screen)
    pygame.display.flip()
    screen.fill((255, 255, 0))
    y = 100

    choice = buttons_clog.display_answers_clicked(buttons)
    match choice:
        case "1":
            hero.xp -= 5
            raw_text = 'Du versuchst zu erklären,'
            y = display_outro(hero, raw_text, y, screen, font)
            raw_text = 'dass du dir die Wade unglücklicherweise gezerrt hast'
            y = display_outro(hero, raw_text, y, screen, font)
            raw_text = 'Du verabschiedest dich und gehst zielstrebig davon.'
            y = display_outro(hero, raw_text, y, screen, font)
            raw_text = 'Die Fremden schauen dir noch schelmisch hinterher.'
            y = display_outro(hero, raw_text, y, screen, font)
            raw_text = '-5 XP'
            y = display_outro(hero, raw_text, y, screen, font)

        case "2":
            raw_text = 'Dein Herausforderer macht sich bereit.'
            y = display_outro(hero, raw_text, y, screen, font)
            #Gegner wird geladen und der Kampf beginnt

        case "3":
            raw_text = 'Mein Name ist KARIM.'
            y = display_outro(hero, raw_text, y, screen, font)
            raw_text = 'Mach dich auf Schmerzen gefasst.'
            y = display_outro(hero, raw_text, y, screen, font)
            #Gegner wird geladen und der Kampf beginnt