import turtle
import time
import random

# --- Setup ---
WIDTH, HEIGHT = 800, 600
wn = turtle.Screen()
wn.title("NEON SYNTH: TURTLE EDITION")
wn.bgcolor("#0a001a") # Deep dark purple
wn.setup(WIDTH, HEIGHT)
wn.tracer(0)

# Physics Variables
GRAVITY = -0.8
PLAYER_SPEED = 5
JUMP_FORCE = 16

# Game State
player_dx = 0
player_dy = 0
on_ground = False

# --- Actors ---
player = turtle.Turtle()
player.shape("square")
player.color("#00ffff") # Neon Cyan
player.penup()
player.goto(-300, 0)

# Platform Data [x, y, width, height]
platforms = [
    [-400, -250, 800, 40],  # Floor
    [-100, -100, 200, 20],  # Middle Plat
    [150, 0, 150, 20],      # Right Plat
    [-250, 100, 100, 20],   # Left Plat
    [50, 200, 100, 20]      # Top Plat
]

draw_pen = turtle.Turtle()
draw_pen.hideturtle()
draw_pen.penup()

def draw_platforms():
    draw_pen.clear()
    for p in platforms:
        draw_pen.goto(p[0], p[1])
        draw_pen.color("#ff00ff") # Neon Pink
        draw_pen.begin_fill()
        for _ in range(2):
            draw_pen.forward(p[2])
            draw_pen.left(90)
            draw_pen.forward(p[3])
            draw_pen.left(90)
        draw_pen.end_fill()

# --- Controls ---
def go_left():
    global player_dx
    player_dx = -PLAYER_SPEED

def go_right():
    global player_dx
    player_dx = PLAYER_SPEED

def stop():
    global player_dx
    player_dx = 0

def jump():
    global player_dy, on_ground
    if on_ground:
        player_dy = JUMP_FORCE
        on_ground = False

wn.listen()
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
wn.onkeyrelease(stop, "a")
wn.onkeyrelease(stop, "d")
wn.onkeypress(jump, "space")

# --- Main Game Loop ---
while True:
    wn.update()
    
    # 1. Apply Physics
    player_dy += GRAVITY
    player.setx(player.xcor() + player_dx)
    player.sety(player.ycor() + player_dy)

    # 2. Collision Detection
    on_ground = False
    for p in platforms:
        px, py, pw, ph = p
        
        # Check if player is over the platform horizontally
        if px - 10 < player.xcor() < px + pw + 10:
            # Check if player is landing on top of the platform
            if py + ph - 5 < player.ycor() < py + ph + 10 and player_dy <= 0:
                player.sety(py + ph)
                player_dy = 0
                on_ground = True

    # 3. Screen Boundaries
    if player.ycor() < -300: # Fall off bottom
        player.goto(-300, 0)
        player_dy = 0
    
    if player.xcor() > 400: player.setx(-400)
    if player.xcor() < -400: player.setx(400)

    draw_platforms()
    time.sleep(0.01)