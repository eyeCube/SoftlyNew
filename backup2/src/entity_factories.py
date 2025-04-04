from components.ai import HostileEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item
import color
from const import *


player = Actor(
    value=99,
    char=chr(ord('@')+256),
    color=(255, 255, 255),
    name="eyeCube",
    title="",
    ai_cls=None,
    equipment=Equipment(),
    fighter=Fighter(hp=30, av=0, dmg=2, light=4),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
)

omnibot = Actor(
    value=0,
    char=chr(ord('d')+256),
    color=color.blue,
    name="omnibot",
    title="the ",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, av=0, dmg=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)
zetabie = Actor(
    value=0,
    char=chr(ord('z')+256),
    color=color.dkgreen,
    name="zetabie",
    title="the ",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, av=1, dmg=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
)

confusion_scroll = Item(
    value=1,
    char="~",
    color=(207, 63, 255),
    name="confusion scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)
fireball_scroll = Item(
    value=1,
    char="~",
    color=(255, 0, 0),
    name="fireball scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)
health_potion = Item(
    value=1,
    char="!",
    color=(127, 0, 255),
    name="health potion",
    consumable=consumable.HealingConsumable(amount=8),
)
lightning_scroll = Item(
    value=1,
    char="~",
    color=(255, 255, 0),
    name="lightning scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)


'''
    Hero
        zeal: courage, Life, resistances, recruiting allies, resisting mental attacks
    Soldier
        guts: Melee weapons, breaking obstacles, courage, intimidation, resisting mental attacks
    Wizard
        tech: Tech, explosives, security camera operation, security door opening, hacking, bio-techno-hacking, 
    Rogue
        luck: Ranged weapons, gambling, item find, dodging, jumping, climbing, acrobatics
        



    improvised grenade
    improvised mine
    improvised pistol
    improvised shotgun

    laser pistol
    laser magnum
    laser rifle
    railgun
    grenade launcher
    
    sling / slings class
    bow / bows class
    arrow / arrows class

    light sword
    light knife
    bombspear
    bombhammer
    light baton
    light staff
    stun stick
    stun rod
    taser / nailgun

    auto rifle
    auto pistol
    
    pistol / pistols class (rapid firing, medium power, accurate)
    revolver / revolvers class (moderately slow firing, very high power, inaccurate)
    shotgun / shotguns class (slow firing, extremely high power, slightly inaccurate)
    rifle / rifles class (slow firing, very high power, very accurate)
    carbine / carbines class (moderately rapid firing, high power, accurate)
    sniper rifle / sniper rifles class (slow firing, high power, extremely accurate, expensive ammo, low ammo capacity)
    
    grenades
    mines
    pistol rounds
    rifle rounds
    stones / metal balls (sling ammo)
    shotgun shells
    
    sword / straight swords class
    dagger / knives class
    halberd / poleaxe class
    waraxe / axes class
    baton / batons class
    bo staff / staves class
    club / maces class
    warhammer / hammers class
    lucerne / polehammers class
    saber / curved swords class
    longsword / longswords class
    spear / spears class
    lance / lances and rapiers class
    glaive / glaives class
'''


weapons = {}

def initialize_all_weapons():
    initialize_swords()
    initialize_daggers()
    initialize_halberds()
    initialize_axes()
    
def initialize_swords():
    swords = {}
    for material in MATERIALS:
        swords.update({material : Item(
            durability = round(16 * MAT_DURABILITY[material]),
            value = MAT_VALUE[material],
            weight = round(10 * MAT_WEIGHT[material]),
            char=chr(ICON_SWORD), color=MAT_COLORS[material],
            name=f"{MAT_NAMES[material]} sword",
            equippable=equippable.MeleeWeapon(
                damage = 2 + MAT_DAMAGE[material],
                attack = 30 + MAT_ATTACK[material],
                dr = 8 + MAT_DODGE[material],
                scary  = 1 + MAT_SCARY[material],
                beauty = 0 + MAT_BEAUTY[material],
                acc_range = max(1, 4 + MAT_THROW_RANGE[material]),
                reach = 1,
                twoh = False,
                )
            )})
    weapons.update({CLASS_SWORDS : swords})

def initialize_daggers():
    daggers = {}
    for material in MATERIALS:
        daggers.update({material : Item(
            durability = round(32 * MAT_DURABILITY[material]),
            value = MAT_VALUE[material],
            weight = round(5 * MAT_WEIGHT[material]),
            char=chr(ICON_DAGGER), color=MAT_COLORS[material],
            name=f"{MAT_NAMES[material]} dagger",
            equippable=equippable.MeleeWeapon(
                damage = 1 + MAT_DAMAGE[material],
                attack = 40 + MAT_ATTACK[material],
                dr = 5 + MAT_DODGE[material],
                scary  = 1 + MAT_SCARY[material],
                beauty = 0 + MAT_BEAUTY[material],
                acc_range = max(1, 4 + MAT_THROW_RANGE[material]),
                reach = 1,
                twoh = False,
                )
            )})
    weapons.update({CLASS_DAGGERS : daggers})
    
def initialize_halberds():
    halberds = {}
    for material in MATERIALS:
        halberds.update({material : Item(
            durability = round(48 * MAT_DURABILITY[material]),
            value = 2 * MAT_VALUE[material],
            weight = round(50 * MAT_WEIGHT[material]),
            char=chr(ICON_HALBERD), color=MAT_COLORS[material],
            name=f"{MAT_NAMES[material]} halberd",
            equippable=equippable.MeleeWeapon(
                damage = 6 + MAT_DAMAGE[material],
                attack = 10 + MAT_ATTACK[material],
                dr = 3 + MAT_DODGE[material],
                scary  = 2 + MAT_SCARY[material],
                beauty = 0 + MAT_BEAUTY[material],
                acc_range = max(1, 2 + MAT_THROW_RANGE[material]),
                reach = 2,
                twoh = True,
                )
            )})
    weapons.update({CLASS_HALBERDS : halberds})
    
def initialize_axes():
    axes = {}
    for material in MATERIALS:
        axes.update({material : Item(
            durability = round(32 * MAT_DURABILITY[material]),
            value = MAT_VALUE[material],
            weight = round(10 * MAT_WEIGHT[material]),
            char=chr(ICON_AXE), color=MAT_COLORS[material],
            name=f"{MAT_NAMES[material]} axe",
            equippable=equippable.MeleeWeapon(
                damage = 3 + MAT_DAMAGE[material],
                attack = 20 + MAT_ATTACK[material],
                dr = 3 + MAT_DODGE[material],
                scary  = 1 + MAT_SCARY[material],
                beauty = 0 + MAT_BEAUTY[material],
                acc_range = max(1, 4 + MAT_THROW_RANGE[material]),
                reach = 1,
                twoh = False,
                )
            )})
    weapons.update({CLASS_AXES : axes})
    
def initialize_spears():
    spears = {}
    for material in MATERIALS:
        spears.update({material : Item(
            durability = round(48 * MAT_DURABILITY[material]),
            value = MAT_VALUE[material],
            weight = round(30 * MAT_WEIGHT[material]),
            char=chr(ICON_SPEAR), color=MAT_COLORS[material],
            name=f"{MAT_NAMES[material]} spear",
            equippable=equippable.MeleeWeapon(
                damage = 2 + MAT_DAMAGE[material],
                attack = 40 + MAT_ATTACK[material],
                dr = 0 + MAT_DODGE[material],
                scary  = 1 + MAT_SCARY[material],
                beauty = 0 + MAT_BEAUTY[material],
                acc_range = max(1, 6 + MAT_THROW_RANGE[material]),
                reach = 1,
                twoh = False,
                )
            )})
    weapons.update({CLASS_SPEARS : spears})





leather_armor = Item(
    value=2,
    char="[",
    color=(139, 69, 19),
    name="leather armor",
    equippable=equippable.Armor(av=1),
)

chain_mail = Item(
    value=2,
    char="[", color=(139, 69, 19), name="Chain Mail", equippable=equippable.Armor(av=2)
)
