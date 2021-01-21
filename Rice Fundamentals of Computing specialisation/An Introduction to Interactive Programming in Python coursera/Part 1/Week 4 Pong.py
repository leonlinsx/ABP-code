# Implementation of classic arcade game Pong
# http://www.codeskulptor.org/#user47_EAuhK0Ngy5_30.py

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
PAD_SPEED = 5
BALL_SPEED_INC = 1.1  # how much to increase by each time hit paddle

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    # pixels per update (1/60 seconds)
    # unsure why the course had such a large velocity initialisation
    hor = random.randrange(120, 240) / 50
    ver = random.randrange(60, 180) / 50
    # RIGHT is True
    if direction:
        ball_vel = [hor, -ver]  
    else:
        ball_vel = [-hor, -ver]
        
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    # adjust score before ball created
    score1 = 0
    score2 = 0
    
    spawn_ball(RIGHT)
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = 0
    paddle2_vel = 0

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")  # left gutter
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")  # right gutter
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # for ceiling and floor rebounds
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
    # draw ball
    # center_point, radius, line_width, line_color, fill
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel > HALF_PAD_HEIGHT:
        if paddle1_pos + paddle1_vel < HEIGHT - HALF_PAD_HEIGHT:	
            paddle1_pos += paddle1_vel

    if paddle2_pos + paddle2_vel > HALF_PAD_HEIGHT:
        if paddle2_pos + paddle2_vel < HEIGHT - HALF_PAD_HEIGHT:	
            paddle2_pos += paddle2_vel
    
    # draw paddles
    # point1, point2, line_width, line_color
    left1 = (HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT)
    left2 = (HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT)
    canvas.draw_line(left1, left2, PAD_WIDTH, "White")
    right1 = (WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT)
    right2 = (WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT)
    canvas.draw_line(right1, right2, PAD_WIDTH, "White")
    
    # determine whether hits gutter
    # determine whether paddle and ball collide
    # reminder the ball has a radius
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        if ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] = ball_vel[0] * BALL_SPEED_INC
        else:  # if hit gutter adn not paddle
            score2 += 1
            spawn_ball(RIGHT)
    elif ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
        if ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] = ball_vel[0] * BALL_SPEED_INC
        else:
            score1 += 1
            spawn_ball(LEFT)
    
    # draw scores
    canvas.draw_text(str(score1), (150, 70), 50, "White")
    canvas.draw_text(str(score2), (450, 70), 50, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= PAD_SPEED
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel += PAD_SPEED
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= PAD_SPEED
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel += PAD_SPEED

# to not continuously increase velocity
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game)

# start frame
new_game()
frame.start()
