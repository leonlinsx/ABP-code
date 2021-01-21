# program template for Spaceship
# http://www.codeskulptor.org/#user47_ZOZeh5qArO_6.py
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
ANGLE_INC = 0.1
ACC_CONSTANT = 0.1
FRICTION = 0.01
MISS_CONSTANT = 2

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        # canvas.draw_image(image, center_source, width_height_source, center_dest, width_height_dest, rotation)
        if self.thrust:
            canvas.draw_image(self.image, (self.image_center[0] + self.image_size[0], self.image_center[1]), self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        # the pos, angle, friction, thrust updates are all within this
        # update pos and angles, wrap screen if out of it
        self.pos[0] += self.vel[0]
        if self.pos[0] < 0 or self.pos[0] > WIDTH:
            self.pos[0] %= WIDTH
        self.pos[1] += self.vel[1]
        if self.pos[1] < 0 or self.pos[1] > HEIGHT:
            self.pos[1] %= HEIGHT
        self.angle += self.angle_vel
        
        # friction update
        self.vel[0] *= (1 - FRICTION)
        self.vel[1] *= (1 - FRICTION)
        
        # thrust update
        # calculate forward vector pointing in the direction ship facing
        fwd_vector = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += fwd_vector[0] * ACC_CONSTANT
            self.vel[1] += fwd_vector[1] * ACC_CONSTANT
    
    def change_angle(self, angle):
        self.angle_vel += angle
        
    def thruster_toggle(self, toggle):
        # toggle thrust boolean and sound
        if toggle:
            self.thrust = True
            ship_thrust_sound.play()
        else:
            self.thrust = False
            ship_thrust_sound.rewind()
            
    def shoot(self):
        # spawn new missile 
        # The missile's initial position should be the tip of your ship's "cannon". 
        # Its velocity should be the sum of the ship's velocity 
        # and a multiple of the ship's forward vector.
        global a_missile
        fwd_vector = angle_to_vector(self.angle)  # vector is [1, 0], [0, 1], [-1, 0], [0, -1] from E to N direction
        miss_pos = (self.pos[0] + fwd_vector[0] * self.image_size[0] * 0.5, self.pos[1] + fwd_vector[1] * self.image_size[1] * 0.5)
        miss_vel = (self.vel[0] + fwd_vector[0] * MISS_CONSTANT, self.vel[1] + fwd_vector[1] * MISS_CONSTANT)
        a_missile = Sprite(miss_pos, miss_vel, 0, 0, missile_image, missile_info, missile_sound)
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        # pos and angle updates, wrap screen
        self.pos[0] += self.vel[0]
        if self.pos[0] < 0 or self.pos[0] > WIDTH:
            self.pos[0] %= WIDTH
        self.pos[1] += self.vel[1]
        if self.pos[1] < 0 or self.pos[1] > HEIGHT:
            self.pos[1] %= HEIGHT
        self.angle += self.angle_vel
        
        # assume rocks/missiles do not accelerate or experience friction

           
def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # draw lives and scores
    canvas.draw_text("Lives", (50, 50), 30, "White")
    canvas.draw_text(str(lives), (50, 80), 30, "White")
    canvas.draw_text("Score", (WIDTH - 100, 50), 30, "White")
    canvas.draw_text(str(score), (WIDTH - 100, 80), 30, "White")
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()

# movement handlers    
def keydown(key):
    if simplegui.KEY_MAP["left"] == key:
        my_ship.change_angle(-ANGLE_INC)
    elif simplegui.KEY_MAP["right"] == key:
        my_ship.change_angle(ANGLE_INC)
    elif simplegui.KEY_MAP["up"] == key:
        my_ship.thruster_toggle(True)
    elif simplegui.KEY_MAP["space"] == key:
        my_ship.shoot()

def keyup(key):
    if simplegui.KEY_MAP["left"] == key:
        my_ship.change_angle(ANGLE_INC)
    elif simplegui.KEY_MAP["right"] == key:
        my_ship.change_angle(-ANGLE_INC)
    elif simplegui.KEY_MAP["up"] == key:
        my_ship.thruster_toggle(False)
    
# timer handler that spawns a rock    
# Choose a velocity, position, and angular velocity randomly for the rock
def rock_spawner():
    global a_rock
    rock_pos = (random.randrange(0, WIDTH), random.randrange(0, HEIGHT))
    rock_vel = (random.randrange(-2, 2), random.randrange(-2, 2))
    rock_angle = random.randrange(6)
    # spin both directions
    rock_angle_vel = random.random() / 5
    if random.random() > 0.5:
        rock_angle_vel *= -1 
    a_rock = Sprite(rock_pos, rock_vel, rock_angle, rock_angle_vel, asteroid_image, asteroid_info)
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [1, 1], 0, ship_image, ship_info)  # pos, vel, angle
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()