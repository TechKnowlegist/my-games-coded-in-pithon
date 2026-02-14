import turtle
import random
import winsound
import time
import math

# --- Setup ---
WIDTH, HEIGHT = 500, 700
wn = turtle.Screen()
wn.title("NEON GRAND PRIX: STABLE STEER")
wn.bgcolor("#111")
wn.setup(WIDTH, HEIGHT)
wn.tracer(0)

# Game State
speed = 0
current_lap = 1
total_laps = 3
lap_start_time = time.time()
lap_times = []
distance_in_lap = 0
LAP_DISTANCE = 6000 
has_shield = False
finished = False

# Road State
road_x = 0

# --- The Player ---
player = turtle.Turtle()
player.shape("square")
player.shapesize(2, 1)
player.color("cyan")
player.penup()
player.goto(0, -250)

# --- Rivals & Items ---
rivals = []
for _ in range(2):
    r = turtle.Turtle()
    r.shape("square")
    r.shapesize(2, 1)
    r.color("red")
    r.penup()
    r.goto(random.randint(-100, 100), 500)
    rivals.append(r)

item = turtle.Turtle()
item.shape("circle")
item.penup()
item.hideturtle()
item_type = "" 

# --- Drawing Pens ---
road_pen = turtle.Turtle()
road_pen.hideturtle()
ui = turtle.Turtle()
ui.hideturtle()

def draw_checkered_line(y_pos):
    road_pen.penup()
    for x in range(-150, 150, 20):
        road_pen.goto(x + road_x, y_pos)
        road_pen.color("white" if (x//20)%2==0 else "black")
        road_pen.begin_fill()
        for _ in range(4): road_pen.forward(20); road_pen.right(90)
        road_pen.end_fill()

def draw_frame():
    global road_x
    road_pen.clear()
    # Reduced twist speed slightly for better control
    road_x = math.sin(time.time() * 0.6) * 110 
    
    # Grass
    road_pen.penup()
    for side in [-250, 150]:
        road_pen.goto(side + road_x, -350); road_pen.color("green"); road_pen.begin_fill()
        for _ in range(2): road_pen.forward(100); road_pen.left(90); road_pen.forward(700); road_pen.left(90)
        road_pen.end_fill()

    if distance_in_lap > (LAP_DISTANCE - 500):
        draw_checkered_line(300 - (distance_in_lap % 500))

def update_ui():
    ui.clear()
    ui.color("white")
    ui.goto(-230, 310); ui.write(f"LAP: {current_lap}/{total_laps}", font=("Courier", 14, "bold"))
    ui.goto(100, 310); ui.write(f"TIME: {round(time.time()-lap_start_time, 1)}s", font=("Courier", 14, "bold"))
    if has_shield:
        ui.goto(0, 280); ui.color("blue"); ui.write("SHIELD ACTIVE", align="center", font=("Courier", 12, "bold"))

def spawn_item():
    global item_type
    if not item.isvisible():
        item_type = random.choice(["boost", "shield", "slip"])
        colors = {"boost": "red", "shield": "blue", "slip": "green"}
        item.color(colors[item_type])
        item.goto(road_x + random.randint(-80, 80), 400)
        item.showturtle()

def move_entities():
    global speed, has_shield, distance_in_lap, current_lap, finished, lap_start_time
    
    # Item Logic
    if item.isvisible():
        item.sety(item.ycor() - (speed + 2))
        if item.distance(player) < 30:
            if item_type == "boost": speed = 25; winsound.Beep(800, 100)
            elif item_type == "shield": has_shield = True; player.color("blue"); winsound.Beep(600, 100)
            elif item_type == "slip": speed = 2; winsound.Beep(200, 300)
            item.hideturtle()
        if item.ycor() < -400: item.hideturtle()

    # AI Rivals
    for r in rivals:
        r.sety(r.ycor() - (speed + 2))
        # Improved AI: They stay centered better
        target_x = road_x + (rivals.index(r) * 40 - 20)
        if r.xcor() < target_x: r.setx(r.xcor() + 3)
        else: r.setx(r.xcor() - 3)
        
        if r.distance(player) < 30:
            if has_shield:
                has_shield = False; player.color("cyan"); r.goto(road_x, 500)
                winsound.Beep(400, 100)
            else:
                speed = 0; player.setx(road_x); winsound.Beep(150, 500)

        if r.ycor() < -400: r.goto(road_x + random.randint(-60, 60), 500)

# --- Controls (Increased Steering) ---
def left(): player.setx(player.xcor() - 25)
def right(): player.setx(player.xcor() + 25)
def fast(): global speed; speed = min(speed + 2, 22)
def slow(): global speed; speed = max(speed - 2, 0)

wn.onkeypress(left, "Left"); wn.onkeypress(right, "Right")
wn.onkeypress(fast, "Up"); wn.onkeypress(slow, "Down")
wn.listen()

# --- Main Loop ---
while not finished:
    wn.update()
    draw_frame()
    update_ui()
    move_entities()
    spawn_item()
    
    # FIX: Automatic road tracking (Helps you stay on the road)
    if player.xcor() < road_x - 10: player.setx(player.xcor() + 1)
    if player.xcor() > road_x + 10: player.setx(player.xcor() - 1)

    distance_in_lap += speed
    if distance_in_lap >= LAP_DISTANCE:
        lap_times.append(round(time.time() - lap_start_time, 2))
        if current_lap < total_laps:
            current_lap += 1; distance_in_lap = 0; lap_start_time = time.time()
            winsound.Beep(1000, 200)
        else:
            finished = True

    # Off Road Check (Pushes you back in)
    if player.xcor() - road_x > 130: 
        player.setx(player.xcor() - 5)
        speed = max(speed - 1, 2)
    elif player.xcor() - road_x < -130:
        player.setx(player.xcor() + 5)
        speed = max(speed - 1, 2)

    time.sleep(0.02)

# Final Result
ui.clear(); ui.goto(0,0); ui.color("lime")
ui.write(f"RACE FINISHED!\nBest Lap: {min(lap_times)}s\nAlt+F4 to Close", align="center", font=("Courier", 20, "bold"))
wn.update()