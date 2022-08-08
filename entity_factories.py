from components.ai import HostileEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from entity import Actor, Item, Effect
from components.inventory import Inventory

# player
player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=2, base_power=5, base_mass=2),
    inventory=Inventory(capacity=26),
    speed = 100,
)


# npcs
skirmisher = Actor(
	char="s",
	color=(63, 127, 63),
	name="Skirmisher",
	ai_cls=HostileEnemy,
	equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=1, base_power=4, base_mass=1),
    inventory=Inventory(capacity=1), 
    speed = 120,
)

fighter = Actor(
	char="T",
	color=(255, 0, 0),
	name="Fighter",
	ai_cls=HostileEnemy,
	equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=2, base_power=5, base_mass=3),
    inventory=Inventory(capacity=2), 
    speed = 80,
)


# consumables
repair_kit = Item(
    char="!",
    color=(255, 0, 100),
    name="Repair Kit",
    consumable=consumable.HealingConsumable(amount=4),
)

lightning_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="Lightning Missile",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=15),
)

targeted_EMP = Item(
    char="~",
    color=(207, 63, 255),
    name="Targeted EMP",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)

missile = Item(
    char="~",
    color=(255, 0, 0),
    name="Missile",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=5),
)


# equipment
dagger_laser = Item(
    char="/", color=(0, 191, 255), name="D-class laser", equippable=equippable.DaggerClassLaser()
)

sword_laser = Item(char="/", color=(0, 191, 255), name="S-class laser", equippable=equippable.SwordClassLaser())

basic_armor = Item(
    char="[",
    color=(139, 69, 19),
    name="Basic Armoring",
    equippable=equippable.BasicArmor(),
)

Deflector_Shields_Armor = Item(
    char="[", color=(139, 69, 19), name="Deflector Shields", equippable=equippable.DeflectorShieldsArmor()
)


