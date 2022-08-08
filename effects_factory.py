from entity import Effect

laser_beam = Effect(
    char="|",
    color=(255, 0, 0),
    name="laser beam",
    lifetime_in_turns=20,
    speed = 100,
)

explosion = Effect(
	char="*",
	color=(255, 0, 0),
    name="explosion",
    lifetime_in_turns=1,
    speed = 100,
)