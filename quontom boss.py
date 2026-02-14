import turtle
import time
import random
import winsound
import math

# --- Setup ---
WIDTH, HEIGHT = 800, 600
wn = turtle.Screen()
wn.title("NEON BOSS BATTLE")
wn.bgcolor("#050505")
wn.setup(WIDTH, HEIGHT)
wn.tracer(0)

# --- Safe Sound ---
def play_sound(freq, dur):
    try: winsound.Beep(freq, dur)
    except: pass

# --- Actors ---
player = turtle.Turtle("square")
player.color("cyan")
player.penup()
player.goto(0, -200)

boss = turtle.Turtle("circle")
boss.shapesize(5, 5)
boss.color("magenta")
boss.penup()
boss.goto(0, 150)

# Projectiles & Objects
bullets = []
boss_attacks = []
powerups = []

# Stats
player_hp = 100
boss_hp = 500
player_speed = 8
boss_state = "IDLE"
attack_timer = 0

# UI Pen
ui = turtle.Turtle()
ui.hideturtle()
ui.penup()
ui.color("white")

# --- Controls ---
def l(): player.setx(player.xcor() - player_speed)
def r(): player.setx(player.xcor() + player_speed)
def shoot():
    b = turtle.Turtle("triangle")
    b.color("yellow")
    b.penup()
    b.setheading(90)
    b.goto(player.xcor(), player.ycor() + 20)
    bullets.append(b)
    play_sound(800, 20)

wn.listen()
wn.onkeypress(l, "a")
wn.onkeypress(r, "d")
wn.onkeypress(shoot, "space")

# --- Boss Logic ---
def boss_attack_logic():
    global boss_state, attack_timer
    if attack_timer <= 0:
        boss_state = random.choice(["LASER", "ORBS", "SLAM", "IDLE"])
        attack_timer = 40 # Duration of attack
        
        if boss_state == "ORBS":
            for i in range(-2, 3):
                atk = turtle.Turtle("circle")
                atk.color("orange")
                atk.penup()
                atk.goto(boss.xcor() + (i*40), boss.ycor())
                boss_attacks.append(atk)
    else:
        attack_timer -= 1

# --- Main Loop ---
while player_hp > 0 and boss_hp > 0:
    wn.update()
    boss_attack_logic()

    # Move Boss (Hovering)
    boss.setx(math.sin(time.time() * 2) * 200)

    # Player Bullets
    for b in bullets[:]:
        b.forward(15)
        if b.distance(boss) < 50:
            boss_hp -= 5
            bullets.remove(b)
            b.hideturtle()
            play_sound(400, 30)
        elif b.ycor() > 300:
            bullets.remove(b)
            b.hideturtle()

    # Boss Attacks
    for a in boss_attacks[:]:
        a.sety(a.ycor() - 7)
        if a.distance(player) < 30:
            player_hp -= 10
            boss_attacks.remove(a)
            a.hideturtle()
            play_sound(200, 100)
        elif a.ycor() < -300:
            boss_attacks.remove(a)
            a.hideturtle()

    # Powerup Spawn
    if random.random() < 0.01:
        p = turtle.Turtle("circle")
        p.color("lime")
        p.penup()
        p.goto(random.randint(-350, 350), 300)
        powerups.append(p)

    for p in powerups[:]:
        p.sety(p.ycor() - 5)
        if p.distance(player) < 30:
            player_hp = min(100, player_hp + 20)
            powerups.remove(p)
            p.hideturtle()
            play_sound(1200, 50)

    # UI Update
    ui.clear()
    ui.goto(-350, 260)
    ui.write(f"PLAYER HP: {player_hp}", font=("Courier", 16, "bold"))
    ui.goto(150, 260)
    ui.write(f"BOSS HP: {boss_hp}", font=("Courier", 16, "bold"))

    time.sleep(0.01)

# Game Over
ui.goto(-100, 0)
if boss_hp <= 0:
    ui.write("YOU WIN!", font=("Courier", 40, "bold"))
else:
    ui.write("GAME OVER", font=("Courier", 40, "bold"))

wn.update()
time.sleep(2)