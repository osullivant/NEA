import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation as animation
from scipy import integrate
from progressbar import progressbar as prbar  # (use pip/conda install progressbar2, or rewrite line 116.)
from copy import copy
from wolfInputScreen import InputScreen


DEER = 0
WOLF = 1

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
STAY = 4

inputs = InputScreen()

# initial number of deer and wolves
ndeer = inputs.deer
nwolves = inputs.wolves

# size of the grid
gridxsize = gridysize = inputs.gridSize

# energy of a freshly spawned deer/wolf
calf = 10
cub = 10

# chance of a new wolf/deer being spawned at a gridpoint on a step
deer_newborn_chance = 0.10
wolf_newborn_chance = 0.01

# number of steps to simulate
steps = inputs.steps


class Animal(object):
    """
    Tracks the animal's position, energy, species (deer/wolf) and state (live/dead).
    """

    def __init__(self, x0, y0, init_energy, species):
        self.x = x0
        self.y = y0
        self.energy = init_energy
        self.species = species
        self.isDead = False

    def interact(self, other):
        """
        Interact with another animal:
            - If they're from the same species, ignore each other.
            - Wolf eats deer.
        """
        if self.species == DEER and other.species == WOLF:
            self.die()

        elif self.species == WOLF and other.species == DEER:
            other.die()

    def die(self):
        """R.I.P"""
        self.isDead = True

    def move(self, direction):
        """Move a step on the grid. Each step consumes 1 energy; if no energy left, die.
        If hitting the bounds of the grid, "bounce back", step to the opposite direction instead.

        Arguments:
            direction {int} -- direction to move: UP: 0, DOWN: 1, LEFT: 2, RIGHT: 3, STAY: 4
        """
        self.energy -= 1

        if direction == LEFT:
            self.x += 1 if self.x > 0 else -1  # "bounce back"
        if direction == RIGHT:
            self.x -= 1 if self.x < gridxsize - 1 else -1
        if direction == UP:
            self.y += 1 if self.y < gridysize - 1 else -1
        if direction == DOWN:
            self.y -= 1 if self.y > 0 else -1
        if direction == STAY:
            pass

        if self.energy <= 0:
            self.die()  # R.I.P.


animals = []  # this will contain all animals on the grid

# all possible coordinate pair (following https://stackoverflow.com/a/11144716/5099168)
xcoords = np.arange(gridxsize)
ycoords = np.arange(gridysize)
coords = np.transpose([np.tile(xcoords, len(ycoords)), np.repeat(ycoords, len(xcoords))])

# populate grid randomly, unique coordinates for all animals
randcoords = np.random.permutation(coords)
deercoords = randcoords[:ndeer]
wolfcoords = randcoords[ndeer:(ndeer + nwolves)]

for (x, y) in deercoords:
    animals.append(Animal(x0=x, y0=y, init_energy=calf, species=DEER))
for (x, y) in wolfcoords:
    animals.append(Animal(x0=x, y0=y, init_energy=cub, species=WOLF))

t_deercoordsx = []  # track the coordinates of the animals in each step in these arrays
t_deercoordsy = []
t_wolfcoordsx = []
t_wolfcoordsy = []

deernums, wolfnums = [ndeer], [nwolves]  # track the number of deer and wolves too

animfigs = []

for i in prbar(range(steps), max_value=steps,
               redirect_stdout=True):  # NOTE: substitute with for i in range(steps) if progressbar2 is not installed

    # step with each animal in a random direction
    directions = np.random.randint(0, 5, size=len(animals))
    for animal, direction in zip(animals, directions):
        animal.move(direction)

    # generate newborn deer...
    deer_is_born_here = np.random.rand(len(coords)) <= deer_newborn_chance
    newdeer = coords[deer_is_born_here]
    for (x, y) in newdeer:
        animals.append(Animal(x0=x, y0=y, init_energy=calf, species=DEER))

    # ...  and wolves
    wolf_is_born_here = np.random.rand(len(coords)) <= wolf_newborn_chance
    newwolves = coords[wolf_is_born_here]
    for (x, y) in newwolves:
        animals.append(Animal(x0=x, y0=y, init_energy=cub, species=WOLF))

    # interact if two animals are at the same coordinates
    for j, animal1 in enumerate(animals):
        for animal2 in animals[j:]:
            if (animal1.x == animal2.x and
                    animal1.y == animal2.y):
                animal1.interact(animal2)

    # clean up corpses
    dead_indexes = []
    for j, animal in enumerate(animals):
        if animal.isDead:
            dead_indexes.append(j)
    animals = list(np.delete(animals, dead_indexes))

    # count animals and log
    wolfnum, deernum = 0, 0
    for animal in animals:
        if animal.species == DEER:
            deernum += 1
        elif animal.species == WOLF:
            wolfnum += 1
    deernums.append(deernum)
    wolfnums.append(wolfnum)
    # print(deernum, wolfnum, len(dead_indexes))

    # get and log animal coordinates
    deercsx = []
    deercsy = []
    wolfcsx = []
    wolfcsy = []
    for animal in animals:
        if animal.species == DEER:
            deercsx.append(animal.x)
            deercsy.append(animal.y)
            # ax.plot(, animal.y, 'bo')
        elif animal.species == WOLF:
            wolfcsx.append(animal.x)
            wolfcsy.append(animal.y)
            # ax.plot(animal.x, animal.y, 'ro')

    t_deercoordsx.append(deercsx)
    t_deercoordsy.append(deercsy)
    t_wolfcoordsx.append(wolfcsx)
    t_wolfcoordsy.append(wolfcsy)

# Display the movement on an animation
fig, ax = plt.subplots()
fig.suptitle("Wolf/Deer Ecosystem")
ax.set_xlim(0, gridxsize - 1)
ax.set_ylim(0, gridysize - 1)
ax.set_xticks(xcoords)
ax.set_yticks(ycoords)
plt.grid(True)

deerpc, = ax.plot(t_deercoordsx[0], t_deercoordsy[0], label='deer', color="brown")
wolfpc, = ax.plot(t_wolfcoordsx[0], t_wolfcoordsy[0], label='wolf', color="gray")
fig.legend()

txt = ax.text(0.1, 0.1, '', ha='center', va='center', alpha=0.8,
              transform=ax.transAxes, fontdict={'color': 'black', 'backgroundcolor': 'white', 'size': 10})


# initialize the animation:
def anim_init():
    deerpc.set_data(t_deercoordsx[0], t_deercoordsy[0])
    wolfpc.set_data(t_wolfcoordsx[0], t_wolfcoordsy[0])
    txt.set_text('deer: {}\nwolves:{}'.format(deernums[0], wolfnums[0]))
    return deerpc, wolfpc, txt


# update the plot to the i-th frame:
def animate(i):
    deerpc.set_data(t_deercoordsx[i], t_deercoordsy[i])
    wolfpc.set_data(t_wolfcoordsx[i], t_wolfcoordsy[i])
    txt.set_text('deer: {}\nwolves:{}'.format(deernums[i], wolfnums[i]))
    return deerpc, wolfpc, txt


# construct and display the animation
im_ani = animation.FuncAnimation(fig, animate, init_func=anim_init, frames=steps,
                                 interval=100, repeat=False, save_count=10, blit=True)
plt.show()

# plot population vs time
plt.plot(deernums, label="deer", color="brown")
plt.plot(wolfnums, label="wolves", color="gray")
plt.xlabel('t')
plt.ylabel('population')
plt.suptitle("Population VS time")
plt.legend()
plt.show()

# plot deer vs wolves
plt.suptitle("Deer vs wolf population")
plt.plot(deernums, wolfnums, color="green")
plt.xlabel('deer')
plt.ylabel('wolves')
plt.show()
