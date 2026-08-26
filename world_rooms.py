import pygame
from random import choices

class Room:

    def __init__(self, name, image=None):

        self.name = name
        self.fight = False
        self.event = False
        self.warp = False
        self.elite = False
        self.boss = False
        self.rest = False
        self.enter = True
        self.color = (150, 150, 150)
        self.image = image

        if image is not None:
            self.image = pygame.image.load(image)
            self.image =pygame.transform.scale(self.image, (70, 70))
            self.rect = self.image.get_rect()

    def __repr__(self):
        return self.name
    
    def get_color(self, inside):
        if inside:
            return (255, 255, 255)
        else:
            return self.color


enemy_room = 'images/rooms/enemy_room.png'
warp_room = 'images/rooms/warp_room.png'
event_room = 'images/rooms/event_room.png'
elite_room = 'images/rooms/elite_room.png'
bond_fire = 'images/rooms/bond_fire.png'
no_room = 'images/rooms/no_room.png'
        

class EmptyRoom(Room):
    def __init__(self):
        super().__init__("LEERER RAUM")
        self.color = (50, 50, 50)
        
        
class EnemyRoom(Room):
    def __init__(self):
        super().__init__("GEGNERRAUM", enemy_room)
        self.color = (250, 0, 0)
        self.fight = True


class WarpRoom(Room):
    def __init__(self):
        super().__init__("WARP", warp_room)
        self.color = (0, 0, 250)
        self.warp = True


class EventRoom(Room):
    def __init__(self):
        super().__init__("DUNKLER RAUM", event_room)
        self.color = (255, 255, 0)
        self.event = True


class EliteRoom(Room):
    def __init__(self):
        super().__init__("ELITERAUM", elite_room)
        self.color = (250, 0, 250)
        self.elite = True


class BossRoom(Room):
    def __init__(self):
        super().__init__("BOSSRAUM")
        self.color = (200, 100, 100)
        self.boss = True


class BondFire(Room):
    def __init__(self):
        super().__init__("LAGERPLATZ", bond_fire)
        self.color = (50, 200, 40)
        self.rest = True


class NoRoom(Room):
    def __init__(self):
        super().__init__("WAND", no_room)
        self.color = (0, 0, 0)
        self.enter = False


o, e, w = EmptyRoom(), EnemyRoom(), WarpRoom()
r, b, q = EventRoom(), EliteRoom(), BossRoom()
ü, n, x = BondFire(), NoRoom(), None


def dungeon_by_stage(stage): 

    if stage == 0:
        dungeon =  [[o, o, e],
                    [o, n, r],
                    [e, n, w]]
        
    elif stage in (1, 4, 7):
        dungeon = procedual_dungeon(stage)

    elif stage in (2, 5, 8):
        dungeon = procedual_dungeon_elite(stage)

    elif stage in (3, 6, 9):
        dungeon = [[o, o, ü, q]]
    
    return dungeon


def procedual_dungeon(stage):

    rnd_room = choices(
        population=[o, e, r],
        weights=[35, 45, 20],
        k=21) #Sets number of tuples

    template = [[o, o, x, e, r],
                [o, o, x, x, e],
                [x, x, n, x, x],
                [e, x, x, ü, e],
                [r, e, x, e, w]]
    
    template = set_no_rooms(template, l=2)
    template = set_rooms(template, rnd_room)
    return template 


def procedual_dungeon_elite(stage):
    
    rnd_room = choices(
        population=[o, e, r],
        weights=[37, 50, 13],
        k=30) #Sets number of tuples

    template = [[o, o, x, e, r],
                [o, o, x, x, e],
                [x, x, n, x, x],
                [e, x, x, ü, b],
                [r, e, x, b, w]]

    template = set_no_rooms(template, l=2)
    template = set_rooms(template, rnd_room)
    return template


def set_rooms(template, rnd_room):

    i = 0
    for row in range(len(template)):
        for column in range(len(template[row])):
            if template[row][column] == x:
                template[row][column] = rnd_room[i]
                i += 1
    return template


def set_no_rooms(template, l):
    """Function to limit NoRoom generation"""
    rnd_room = choices(
        population=[x, n],
        weights=[70, 30],
        k=30)
    
    a = 0
    k = 0

    for i, y in enumerate(template):
        for j, z in enumerate(y):
            if template[i][j] == x:
                template[i][j] = rnd_room[a]
                a += 1
                if template[i][j] == n:
                    k += 1
                    if k == l:
                        return template                    
    return template
