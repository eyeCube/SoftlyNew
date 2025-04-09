import components
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item
import color
from const import *


# behold, the platonic ideals

player = Actor(
    weight=750,
    value=99,
    char=chr(ord('@')+256),
    color=(255, 255, 255),
    name="eyeCube",
    title="",
    ai_cls=components.ai.StationaryEntity, # everything actor must have an AI and a fighter, equipment, inventory, level, etc.
    equipment=Equipment(),
    fighter=Fighter(hp=0, av=0, dmg=0, light=0, vision=32, zeal=7, guts=5+2, tech=5-2, luck=5),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
)

omnibot = Actor(
    weight=500,
    value=98,
    char=chr(ord('d')+256),
    color=color.blue,
    name="omnibot",
    title="the ",
    ai_cls=components.ai.HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=0, av=0, atk=90, dmg=1, light=1, zeal=2, guts=3, tech=8, luck=5),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)
zetabie = Actor(
    weight=900,
    value=98,
    char=chr(ord('z')+256),
    color=color.dkgreen,
    name="zetabie",
    title="the ",
    ai_cls=components.ai.HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=0, av=1, atk=110, dmg=2, zeal=5, guts=5, tech=8, luck=5),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
)

confusion_scroll = Item(
    weight=10,
    value=1,
    char="~",
    color=(207, 63, 255),
    name="confusion scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)
fireball_scroll = Item(
    weight=10,
    value=1,
    char="~",
    color=(255, 0, 0),
    name="fireball scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)
health_potion = Item(
    weight=10,
    value=1,
    char="!",
    color=(127, 0, 255),
    name="health potion",
    consumable=consumable.HealingConsumable(amount=8),
)
lightning_scroll = Item(
    weight=10,
    value=1,
    char="~",
    color=(255, 255, 0),
    name="lightning scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)


'''
----------------------------

        BASIC LORE

----------------------------

    Currency is called Lyra
    2 Lyra == base amount of simple items
    Measurement is called slugs. 1 slug == 0.05 kg, so 10 slugs is a little over a pound (1.1 lb / 0.5kg)
    Common language is called Semblish
    The dyson sphere which encomppases everything you (and everyone in your life) has ever known
        name: the Globe
    
----------------------------

        FACTIONS

----------------------------

Indoreum
Strangers
Goru Clan
Goliaths
Paraxismecha
Rougots
Cats
Jackals
Corvids
Centipedes
Ants
Spiders
Rodents
Hetif Clan
Psionic Knights
Alchemists
Chimeras
Pandemics


----------------------------

        CHARACTER CLASSES

----------------------------

    Hero
        zeal: courage, Life, resistances, recruiting allies, resisting mental attacks
        Z 7
        G 5
        T 3
        L 5
        Wgt 1.6 Kiloslugs (1600 slugs == 80kg)
        Lyra 2
        LV 20

        Items:
            ZEALOUS luminous cape
            Polymer bascinet
            Luminous crumetal sword
            Polymer breastplate
            Torch x4
            Compass

        Skills:
            Combat training
            Unarmed combat
            Heavy armor
            Sword & dagger
            Shield & buckler
        
    Soldier
        guts: Melee weapons, breaking obstacles, courage, intimidation, resisting mental attacks
        Z 5
        G 7
        T 3
        L 4
        Wgt 1.5 Kiloslugs (1500 slugs == 75kg)
        Lyra 5
        LV 19

        Items:
            GUTSY sturdy crumetal buckler
            Sturdy crumetal spear
            Crumetal dagger
            Gambeson
            Polymer helmet
            Backpack
            MRE x5
            Torch x8

        Skills:
            Combat training
            Unarmed combat
            Light armor
            Spear & lance
            Shield & buckler
            Polearm
            
    Wizard
        tech: Tech, explosives, security camera operation, security door opening, hacking, bio-techno-hacking,
        Z 4
        G 3
        T 7
        L 4
        Wgt 1.3 Kiloslugs (1300 slugs == 65kg)
        Lyra 10
        LV 18

        Items:
            TECHY bejeweled wand
            Splicer array
            Wooden staff sling
            Small sling bullet x20 (4 slugs ea., 6 for the medium, 8 for the large sling bullets)
            Bejeweled robes
            Satchel
            Battery x2
            Strobe light

        Skills:
            
            
    Rogue
        luck: Ranged weapons, gambling, item find, dodging, jumping, climbing, acrobatics
        Z 4
        G 4
        T 3
        L 7
        Wgt 1.4 Kiloslugs (1400 slugs == 70kg)
        Lyra 15
        LV 18

        Items:
            LUCKY lacquered hood
            Lacquered crumetal dagger
            Improvised pistol
            Chitin armor
            Cloak
            Olen lantern
            Lockpick x2
            Pistol rounds x24
            Scavenged meal
            Tool

        Skills:
            Improvising guns
            Improvising blades
            Improvising traps
            Sword & dagger
            Marksman
            Pistol
            Silver tongue

        


----------------------------

        SKILLS

----------------------------

    Skills in the game (implement these AFTER you have a basic game / system going. You don't need these to have a fun game, it's just extra):

    > Engineering
        Comes with: Improvising melee weapons (unlocks basic recipes like clubs, hammers, spears, etc.)
        Improvising traps
        Improvising guns
        Improvising blades
        Improvising bombs
        Improvising batteries
        Cooking
        Cartridge pressing
        Bomb making
        Basket weaving
        Leatherworking
        Carpentry
        Pottery
        Whittling (plastic, wood, bone)
        Chitincraft
        Blacksmith
        Gunsmith
        Repair
        Robotics (req 12 T) (allows you to craft autonomous turrets, autonomous aerodrones, and omnibots / slugbots)
    
    > Combat training
        Comes with: Fighting (basic ability to dodge and fight acquired -- without it, you get significantly less DR per Luck stat point and less Atk bonus from Guts)
        Unarmed combat
        Sword & dagger
        Spear & javelin
        Polearm
        Axe
        Club & hammer
        Staff
        Shield & buckler

    > Pyrotechnics
        Comes with: Firemaking (basic ability to start a fire / campfire acquired)
        Explosives (TNT, bombs, grenades)
        Mines
        Grenade launchers
        Flame weapons (flamethrowers, molotov cocktails, etc.)

    > Marksman
        Comes with: Throwing (basic ability to throw acquired, also improves ranged accuracy bonus from Luck)
        Sling & staff sling
        Bow
        Rifle
        Pistol
        Shotgun

    > Technician (req 5 T)
        Comes with: Computers (basic access to computer terminals acquired -- can open and unlock doors and chests, access cameras, and interact remotely with machines)
        Energy weapons (req 7 T) (allows you to scale energy wpn damage and attack/accuracy based on tech; by default, energy weapons have no scaling)
        Hacking (req 11 T) (allows you to use terminals (and hand-held terminals!) to remotely attack a robot or cyborg in view.
            Destroyed robotic/cyborg foes killed in this way create an Embodied Computer Virus (a companion that follows and fights for you!)
        Ancient machinery (req 10 T) (for the purposes of operating ancient machines, your Tech stat is treated as if it were 8 points higher)

    > Persuasion (req 6 Z)
        Comes with: Silver tongue (opens up dialogue with Neutral creatures)
        Intimidating (req 6 G) (make a show of your intimidation stat against courage stat nearby foes)
        Swindler (req 10 T) (earn more Lyra from selling items -- almost as much as it costs you to buy them)
        Sleight of hand (req 10 L) (gain activated ability: pick pocket)
        Recruiter (req 14 L) (attempt to convert a creature to join you, rolling your Luck against theirs)


----------------------------

        WEAPONS

----------------------------

    improvised grenade
    improvised mine
    improvised pistol
    improvised shotgun

    laser pistol
    laser magnum
    laser rifle
    railgun
    grenade launcher
    flame thrower
    
    sling / slings class
    bow / bows class
    arrow / arrows class

    light sword
    light knife
    pneumatic spear / bombspear
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
    rapiers class
    glaive / glaives class

    ball cap
    bowler hat
    tiara
    crown
    hood
    skull cap
    helmet
    bascinet
    great helm
    bandana

    dresses / aprons
        cloth
    vests / combat vests
        cloth
        kevlar
        ceramic
    robes / coats
        cloth
    gambeson
        cloth
    scale armor
        polymer
        wood
        bone
        chitin
        ceramic
        crumetal
        alloy
    breastplate
        polymer
        bone
        chitin
        crumetal
        alloy
        allurite
    plate jacket
        polymer
        bone
        chitin
        crumetal
        alloy
        allurite
    buckler
        polymer
        wood
        chitin
        crumetal
        alloy
        allurite
    shield
        polymer
        wood
        chitin
        crumetal
        alloy
        allurite
    tower shield
        polymer
        wood
        chitin
        crumetal
        alloy
        allurite

    cape
    cloak
    satchel / purse / briefcase
    backpack




    
whenever legendary creature dies, it drops a gravestone instantly
    because it is "so respected by the universe"




strange ancient machines that can be broken / must be identified:
from left to right

1. battery recharger
	?: strange box / strange box that accepts batteries
	When powered with battery(s) inside, battery(s) gain charge until they are fully recharged after 60 turns
	Must be powered by mains
	Required TECH to identify and operate: 4
	Required TECH to repair: 8
	
2. luminous crystal
	?: strange rock / strange light-emitting rock
	While powered, emits light in radius of 60 m
	Must be powered by mains
	Required TECH to identify and operate: 3
	Required TECH to repair: 12
	
3. phase shifter
	?: strange tubes / strange machine with glass bulbs
	When interacted with while powered, you become invisible for 60 turns
	Must be powered by mains
	Required TECH to identify and operate: 13
	Required TECH to repair: 16
	
4. pneumatic refiller
	?: strange machine / strange machine with hoses
	Must be powered by mains
	Required TECH to identify and operate: 8
	Required TECH to repair: 10
	
5. oil or water (or other liquid) pump / basically a big supply of liquid!
	?: strange pipes / strange watertight pipes
	Must be powered by mains
	Required TECH to identify and operate: 5
	Required TECH to repair: 6
	
6. radio communicator
	?: strange box / strange box with cathode ray tube
	May be powered by battery or mains
	Required TECH to identify and operate: 4
	Required TECH to repair: 7
	
7. personal teleporter
	?: strange tubes / strange device with cathode ray tubes
	Must be powered by battery
	Required TECH to identify and operate: 12
	Required TECH to repair: 20
	
8. power station
	?: strange tube / strange electrified tube
	Required TECH to identify and operate: 4
	Required TECH to repair: 9
	

'''


weapons = {}

def initialize_all_weapons():
    initialize_swords()
    initialize_daggers()
    initialize_halberds()
    initialize_axes()
    
def initialize_swords():
    swords = {}
    for material in MATERIALS_WEAPONS:
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
                missile_range = max(1, 4 + MAT_THROW_RANGE[material]),
                reach = 1,
                twoh = False,
                )
            )})
    weapons.update({CLASS_SWORDS : swords})

def initialize_daggers():
    daggers = {}
    for material in MATERIALS_WEAPONS:
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
                missile_range = max(1, 4 + MAT_THROW_RANGE[material]),
                reach = 1,
                twoh = False,
                )
            )})
    weapons.update({CLASS_DAGGERS : daggers})
    
def initialize_halberds():
    halberds = {}
    for material in MATERIALS_WEAPONS:
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
                missile_range = max(1, 2 + MAT_THROW_RANGE[material]),
                reach = 2,
                twoh = True,
                )
            )})
    weapons.update({CLASS_HALBERDS : halberds})
    
def initialize_axes():
    axes = {}
    for material in MATERIALS_WEAPONS:
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
                missile_range = max(1, 4 + MAT_THROW_RANGE[material]),
                reach = 1,
                twoh = False,
                )
            )})
    weapons.update({CLASS_AXES : axes})
    
def initialize_spears():
    spears = {}
    for material in MATERIALS_WEAPONS:
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
                missile_range = max(1, 6 + MAT_THROW_RANGE[material]),
                reach = 1,
                twoh = False,
                )
            )})
    weapons.update({CLASS_SPEARS : spears})




torch = Item(
    value=2,
    char="/",
    color=(136, 160, 24),
    name="torch",
    equippable=equippable.MeleeWeapon(light=4, damage=1, attack=10, scary=1, beauty=1, missile_range=5, reach=1, twoh=False),
)

gambeson = Item(
    value=2,
    char=chr(147),
    color=(139, 139, 139),
    name="gambeson",
    equippable=equippable.Armor(
        av = 1, dr = 10
        ),
)

scale_mail = Item(
    value=2,
    char=chr(148), color=color.crumetal, name="Scale Mail", equippable=equippable.Armor(
        av = 2, dr = -5
        )
)
