import turtle
import time
import random
import math

# --- Setup ---
WIDTH, HEIGHT = 800, 600
wn = turtle.Screen()
wn.title("CHROMA SURVIVOR: NEON TURTLE")
wn.bgcolor("#020205")
wn.setup(WIDTH, HEIGHT)
wn.tracer(0)
def trigger_pulse():
    global pulse_charge, boss_hp
    if pulse_charge >= 3: # Only works if you've collected 3 power-ups
        play_sound(1500, 100) # High pitch blast
        # Clear all current boss attacks
        for a in boss_attacks:
            a.hideturtle()
        boss_attacks.clear()
        # Damage the boss
        boss_hp -= 50
        pulse_charge = 0 # Reset charge
# --- Game Stats ---
score = 0
player_hp = 100
enemies = []
particles = []

# --- Player ---
player = turtle.Turtle()
player.shape("triangle")
player.color("#00ffff")
player.penup()
player.speed(0)

# --- Drawing Pen (For UI and Effects) ---
pen = turtle.Turtle()
pen.hideturtle()
pen.penup()

def spawn_enemy():
    e = turtle.Turtle()
    e.shape("square")
    e.color("#ff0055")
    e.penup()
    # Spawn at a random edge
    side = random.randint(1, 4)
    if side == 1: e.goto(-400, random.randint(-300, 300))
    if side == 2: e.goto(400, random.randint(-300, 300))
    if side == 3: e.goto(random.randint(-400, 400), 300)
    if side == 4: e.goto(random.randint(-400, 400), -300)
    enemies.append(e)

# --- Controls ---
def move_up(): player.sety(player.ycor() + 20)
def move_down(): player.sety(player.ycor() - 20)
def move_left(): player.setx(player.xcor() - 20)
def move_right(): player.setx(player.xcor() + 20)

wn.listen()
wn.onkeypress(move_up, "w")
wn.onkeypress(move_down, "s")
wn.onkeypress(move_left, "a")
wn.onkeypress(move_right, "d")

# --- Main Game Loop ---
start_time = time.time()
while player_hp > 0:
    wn.update()
    
    # Spawn enemies faster as time goes on
    if random.random() < 0.05 + (score * 0.001):
        spawn_enemy()

    # Move Enemies towards Player
    for e in enemies[:]:
        # Calculate angle to player
        angle = e.towards(player)
        e.setheading(angle)
        e.forward(2 + (score * 0.01)) # Get faster as score grows
        
        # Collision check
        if e.distance(player) < 20:
            player_hp -= 1
            player.color("white") # Flash on hit
            e.goto(1000, 1000) # Teleport away
            enemies.remove(e)
        else:
            player.color("#00ffff")

    # Clean up far-away enemies
    if len(enemies) > 50:
        old_e = enemies.pop(0)
        old_e.hideturtle()

    # Score increases by surviving
    score += 1

    # UI
    pen.clear()
    pen.color("white")
    pen.goto(-380, 260)
    pen.write(f"SCORE: {score}   HP: {player_hp}", font=("Courier", 18, "bold"))
    
    # Border Wrap
    if player.xcor() > 400: player.setx(-400)
    if player.xcor() < -400: player.setx(400)
    if player.ycor() > 300: player.sety(-300)
    if player.ycor() < -300: player.sety(300)

    time.sleep(0.01)

# Game Over
pen.goto(-100, 0)
pen.write("VOIDED", font=("Courier", 40, "bold"))
wn.update()
time.sleep(3)