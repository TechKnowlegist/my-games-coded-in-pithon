import turtle
import random
import winsound
import time

# --- Game Setup ---
WIDTH, HEIGHT = 600, 600
wn = turtle.Screen()
wn.title("NEON HOPPER: PRO EDITION")
wn.bgcolor("black")
wn.setup(WIDTH, HEIGHT)
wn.tracer(0)

# Game State
level = 1
score = 0
high_score = 0
best_time = None
start_time = time.time()
max_y_reached = -280 # Used to prevent point farming
cars = []
colors = ["cyan", "magenta", "yellow", "orange", "deeppink"]

# --- UI Painter ---
ui = turtle.Turtle()
ui.hideturtle()
ui_color = "white"

def update_ui():
    ui.clear()
    ui.penup()
    ui.color(ui_color)
    
    # Left Side: Timer
    elapsed = round(time.time() - start_time, 1)
    ui.goto(-280, 260)
    ui.write(f"TIME: {elapsed}s", align="left", font=("Courier", 14, "bold"))
    
    # Middle: Current Score
    ui.goto(0, 260)
    ui.write(f"SCORE: {score}", align="center", font=("Courier", 14, "bold"))
    
    # Right Side: Highs
    ui.goto(280, 260)
    best_text = f"BEST: {best_time}s" if best_time else "BEST: --"
    ui.write(f"HI: {high_score} | {best_text}", align="right", font=("Courier", 10, "bold"))

# --- The Player ---
player = turtle.Turtle()
player.shape("square")
player.color("lime")
player.penup()
player.goto(0, -280)

# --- The Goal Line ---
goal_pen = turtle.Turtle()
goal_pen.hideturtle()
goal_pen.penup()

def draw_goal():
    goal_pen.clear()
    goal_pen.goto(-300, 240)
    goal_pen.pensize(5)
    for _ in range(15):
        goal_pen.color("lime")
        goal_pen.pendown()
        goal_pen.forward(20)
        goal_pen.penup()
        goal_pen.forward(20)

# --- Player Movement ---
def move_up():
    global score, max_y_reached
    player.sety(player.ycor() + 20)
    # Give point only if moving to a NEW higher spot
    if player.ycor() > max_y_reached:
        score += 1
        max_y_reached = player.ycor()

def move_down():
    if player.ycor() > -280:
        player.sety(player.ycor() - 20)

def move_left():
    if player.xcor() > -280:
        player.setx(player.xcor() - 20)

def move_right():
    if player.xcor() < 280:
        player.setx(player.xcor() - 20)

# --- Controls ---
wn.listen()
wn.onkeypress(move_up, "Up")
wn.onkeypress(move_down, "Down")
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")

# --- Car Factory ---
def create_car():
    if random.randint(1, 8) == 1:
        new_car = turtle.Turtle()
        new_car.shape("square")
        new_car.shapesize(stretch_wid=0.8, stretch_len=1.8)
        new_car.penup()
        new_car.color(random.choice(colors))
        # Cars spawn in lanes between start and finish
        lane_y = random.randint(-200, 220)
        new_car.goto(320, lane_y)
        new_car.move_speed = random.randint(3, 8) + (level * 0.3)
        cars.append(new_car)

# --- Main Game Loop ---
draw_goal()
print("PRO HOPPER STARTED!")

while True:
    time.sleep(0.02)
    wn.update()
    update_ui()
    
    create_car()
    
    # Move and check cars
    for car in cars[:]:
        car.backward(car.move_speed)
        
        # Collision
        if car.distance(player) < 22:
            winsound.Beep(200, 200)
            if score > high_score:
                high_score = score
            print(f"CRASH! Score: {score}")
            score = 0
            max_y_reached = -280
            player.goto(0, -280)
            start_time = time.time() # Reset timer on death

        # Cleanup
        if car.xcor() < -320:
            car.hideturtle()
            cars.remove(car)

    # Win Condition
    if player.ycor() > 230:
        elapsed = round(time.time() - start_time, 2)
        winsound.Beep(1000, 100)
        winsound.Beep(1300, 150)
        
        # Scoring
        score += 10
        if score > high_score:
            high_score = score
            
        # Best Time tracking
        if best_time is None or elapsed < best_time:
            best_time = elapsed
            print(f"NEW RECORD TIME: {best_time}s")
            
        print(f"Level {level} Clear! Total Score: {score}")
        
        level += 1
        player.goto(0, -280)
        max_y_reached = -280
        start_time = time.time() # Reset timer for new level
        
        for c in cars:
            c.hideturtle()
        cars.clear()