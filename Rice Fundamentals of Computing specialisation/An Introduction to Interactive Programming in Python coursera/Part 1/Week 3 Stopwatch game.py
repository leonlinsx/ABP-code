# template for "Stopwatch: The Game"
# http://www.codeskulptor.org/#user47_Kt6TWuVb2G_2.py

import simplegui

# define global variables
width = 200
height = 200
position = [40, 110]

interval = 10  # Construct a timer with an associated interval of 0.1 seconds
counter = 0
total_stops = 0  # total and successful stops
succ_stops = 0

running = True  # True when the stopwatch is running and False when not

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
# include leading zeros
# unit tester here: http://codeskulptor.appspot.com/owltest/
def format(t):
    a = t // (60 * 10)
    remain = t % (60 * 10)
    b = remain // 100
    c = (remain // 10) % 10
    d = remain % 10
    
    return str(a) + ":" + str(b) + str(c) + "." + str(d)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()
    global running
    running = True
    
def stop():
    timer.stop()
    
    global running, total_stops, counter, succ_stops
    if running:
        total_stops += 1
        if counter % 10 == 0:
            succ_stops += 1
        running = False

def reset():
    global counter, running, total_stops, succ_stops
    counter = 0
    running = False
    total_stops = 0
    succ_stops = 0

# define event handler for timer with 0.1 sec interval
def tick():
    global counter
    print counter
    counter += 1

# define draw handler
def draw(canvas):
    global counter, position
    message = format(counter)
    canvas.draw_text(message, position, 50, "White")

    global total_stops, succ_stops
    score = str(succ_stops) + "/" + str(total_stops)
    canvas.draw_text(score, (150, 30), 25, "Red")
    
# create frame
frame = simplegui.create_frame("Home", width, height)

# create timer buttons
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)

# register event handlers
frame.set_draw_handler(draw)
timer = simplegui.create_timer(interval, tick)

# start frame
frame.start()
timer.stop()

# Please remember to review the grading rubric
