import turtle
import time
import winsound
import random
import math

# --- Setup ---
WIDTH, HEIGHT = 800, 600
wn = turtle.Screen()
wn.title("NEON CHROMA: BOUNCERS & POWERUPS FIXED")
wn.bgcolor("#050505")
wn.setup(WIDTH, HEIGHT)
wn.tracer(0)

# Constants
BASE_GRAVITY = -1.1
JUMP_STRENGTH = 15
BOUNCE_STRENGTH = 28
BASE_SPEED = 7

# Game State
player_dx, player_dy = 0, 0
jumps_left, max_jumps = 2, 2
level_count, score = 0, 0
best_time = None
level_start_time = time.time()

platforms = []  # [x, y, w, h, type, move_x, move_y, start_x, start_y]
bouncers = []   # [x, y, plat_index, dir, offset_x]
powerups = []   # [x, y, type, active]
mega_coin = {"x": 0, "y": 0, "active": False}

inventory = None 
shield_active = False
shield_timer = 0
is_sliding = False
plat_color = "#FF00FF"

# --- Actors ---
player = turtle.Turtle()
player.shape("square")
player.color("cyan")
player.penup()

draw_pen = turtle.Turtle()
draw_pen.hideturtle()
draw_pen.penup()

ui = turtle.Turtle()
ui.hideturtle()
ui.penup()
ui.color("white")

def generate_level():
    global platforms, bouncers, powerups, mega_coin, level_count, is_sliding, level_start_time, score, best_time, plat_color, inventory, shield_active, max_jumps
    
    if level_count > 0:
        elapsed = round(time.time() - level_start_time, 2)
        score += 500 + max(0, 1000 - int(elapsed * 20))
        if best_time is None or elapsed < best_time:
            best_time = elapsed
            winsound.Beep(2000, 50)

    # Random Theme
    plat_color = "#{:02x}{:02x}{:02x}".format(random.randint(150, 255), random.randint(100, 200), random.randint(150, 255))
    platforms, bouncers, powerups = [], [], []
    level_count += 1
    is_sliding, shield_active, max_jumps = False, False, 2
    level_start_time = time.time()
    
    # Start Platform
    platforms.append([-380, -100, 150, 20, "normal", 0, 0, -380, -100])
    
    current_x = -200
    while current_x < 280:
        width = max(100 - (level_count * 3), 50)
        gap = random.randint(110, min(150 + (level_count * 10), 250))
        current_x += gap
        height = random.randint(-180, 80)
        
        p_type = "normal"
        mx, my = 0, 0
        roll = random.random()
        if roll < 0.1: p_type = "tramp"
        elif roll < 0.2: p_type = "ramp"
        elif roll < 0.4: mx = random.randint(40, 80)
        elif roll < 0.6: my = random.randint(50, 100)
            
        platforms.append([current_x, height, width, 20, p_type, mx, my, current_x, height])
        p_idx = len(platforms) - 1

        # Spawn Bouncer (Level 2+)
        if level_count >= 2 and p_type == "normal" and random.random() < 0.5:
            bouncers.append([current_x + 5, height + 20, p_idx, 1, 5]) # x, y, plat_idx, dir, offset_x
            
        # Spawn Power-up
        if random.random() < 0.3:
            p_kind = random.choice(["triple", "shield", "dash"])
            powerups.append([current_x + width/2, height + 30, p_kind, True])

    # Mega Coin
    target_plat = random.choice(platforms[2:])
    mega_coin = {"x": target_plat[0] + 10, "y": target_plat[1] + 60, "active": True}

    player.goto(-350, 0)
    player_dy = 0
    winsound.Beep(600, 50)

def draw_world():
    draw_pen.clear()
    # Green Goal Wall
    draw_pen.goto(370, -300); draw_pen.color("#00FF00"); draw_pen.begin_fill()
    for _ in range(2): draw_pen.forward(30); draw_pen.left(90); draw_pen.forward(600); draw_pen.left(90)
    draw_pen.end_fill()

    for p in platforms:
        c = "yellow" if p[4]=="tramp" else ("#3366FF" if p[4]=="ramp" else plat_color)
        draw_pen.goto(p[0], p[1]); draw_pen.color(c); draw_pen.begin_fill()
        for _ in range(2): draw_pen.forward(p[2]); draw_pen.left(90); draw_pen.forward(p[3]); draw_pen.left(90)
        draw_pen.end_fill()

    for b in bouncers:
        draw_pen.goto(b[0], b[1]); draw_pen.color("red"); draw_pen.begin_fill()
        for _ in range(4): draw_pen.forward(15); draw_pen.left(90)
        draw_pen.end_fill()

    for p in powerups:
        if p[3]:
            colors = {"triple": "blue", "shield": "cyan", "dash": "orange"}
            draw_pen.goto(p[0], p[1]); draw_pen.color(colors[p[2]]); draw_pen.begin_fill()
            draw_pen.circle(8); draw_pen.end_fill()

    if mega_coin["active"]:
        draw_pen.goto(mega_coin["x"], mega_coin["y"]); draw_pen.color("white"); draw_pen.begin_fill()
        for _ in range(4): draw_pen.forward(20); draw_pen.left(90)
        draw_pen.end_fill()

def update_physics():
    global player_dx, player_dy, jumps_left, is_sliding, score, inventory, shield_active, shield_timer, max_jumps
    
    # Platform Motion
    spd = 1 + (level_count * 0.05)
    for p in platforms:
        if p[5] > 0: p[0] = p[7] + math.sin(time.time() * spd) * p[5]
        if p[6] > 0: p[1] = p[8] + math.sin(time.time() * spd) * p[6]

    # Bouncer AI Fix: Stick to platforms and patrol
    b_spd = 2 + (level_count * 0.3)
    for b in bouncers:
        plat = platforms[b[2]]
        b[4] += b[3] * b_spd # update offset_x
        b[0] = plat[0] + b[4]
        b[1] = plat[1] + 20
        if b[4] <= 0 or b[4] >= plat[2] - 15: b[3] *= -1 # Reverse direction

    # Shield logic
    if shield_timer > 0: shield_timer -= 1
    else: shield_active = False

    player_dy += BASE_GRAVITY
    player.sety(player.ycor() + player_dy)
    player.setx(player.xcor() + player_dx)

    # Collision
    on_plat = False
    for p in platforms:
        if p[0]-10 < player.xcor() < p[0]+p[2]+10:
            if p[1] < player.ycor() < p[1]+p[3]+10 and player_dy <= 0:
                if p[4] == "tramp": 
                    player_dy = BOUNCE_STRENGTH
                    winsound.Beep(800, 20)
                else:
                    player.sety(p[1]+p[3]); player_dy = 0
                jumps_left, on_plat, is_sliding = max_jumps, True, (p[4] == "ramp")
                if p[5] > 0: player.setx(player.xcor() + (math.cos(time.time() * spd) * 2))

    if not on_plat: is_sliding = False

    # Bouncer Collision
    for b in bouncers:
        if abs(player.xcor() - b[0]) < 20 and abs(player.ycor() - b[1]) < 25:
            if not shield_active:
                winsound.Beep(200, 50)
                player_dy = 10
                player.setx(player.xcor() + (-50 if player.xcor() < b[0] else 50))

    # Powerup Pickup
    for p in powerups:
        if p[3] and player.distance(p[0], p[1]) < 25:
            p[3], inventory = False, p[2]
            winsound.Beep(1000, 30)

# --- Controls ---
def use_power():
    global inventory, max_jumps, shield_active, shield_timer, player_dy
    if not inventory: return
    if inventory == "triple": max_jumps = 3
    elif inventory == "shield": shield_active = True; shield_timer = 200
    elif inventory == "dash": player.setx(player.xcor() + (160 if player_dx >= 0 else -160))
    inventory = None
    winsound.Beep(1200, 40)

def l(): global player_dx; player_dx = -BASE_SPEED
def r(): global player_dx; player_dx = BASE_SPEED
def s(): global player_dx; player_dx = 0
def j():
    global player_dy, jumps_left
    if jumps_left > 0: player_dy = JUMP_STRENGTH; jumps_left -= 1; winsound.Beep(500, 30)

wn.listen()
wn.onkeypress(l, "a"); wn.onkeypress(r, "d"); wn.onkeyrelease(s, "a"); wn.onkeyrelease(s, "d")
wn.onkeypress(j, "space"); wn.onkeypress(use_power, "s")

generate_level()

while True:
    wn.update()
    update_physics()
    draw_world()
    
    elapsed = round(time.time() - level_start_time, 1)
    ui.clear(); ui.goto(-380, 260)
    ui.write(f"LVL: {level_count}  INV: {inventory if inventory else 'EMPTY'}", font=("Courier", 14, "bold"))
    ui.goto(380, 260); bt = f"BEST: {best_time}s" if best_time else "BEST: --"
    ui.write(f"TIME: {elapsed}s  {bt}", align="right", font=("Courier", 14, "bold"))

    if player.ycor() < -300: 
        player.goto(-350, 0); player_dy = 0
        score = max(0, score - 50)
        winsound.Beep(150, 100)

    if player.xcor() > 365: generate_level()
    time.sleep(0.01)