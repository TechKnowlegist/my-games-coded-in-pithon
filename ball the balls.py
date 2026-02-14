import turtle
import time
import math
import winsound

# --- Setup ---
WIDTH, HEIGHT = 600, 400
wn = turtle.Screen()
wn.title("NEON HOOPS: THREE-POINT SHOOTOUT")
wn.bgcolor("black")
wn.setup(WIDTH, HEIGHT)
wn.tracer(0)

# Game State
score = 0
high_score = 0
time_left = 60
is_shooting = False
power = 0
start_time = time.time()

# --- The Ball ---
ball = turtle.Turtle()
ball.shape("circle")
ball.color("orange")
ball.penup()
ball.goto(-220, -140)
ball.dx = 0
ball.dy = 0

# --- The Hoop & Backboard ---
drawer = turtle.Turtle()
drawer.hideturtle()
drawer.penup()

def draw_hoop():
    drawer.clear()
    # Backboard
    drawer.goto(220, 20)
    drawer.color("white")
    drawer.pensize(5)
    drawer.pendown()
    for _ in range(2):
        drawer.forward(10); drawer.left(90); drawer.forward(80); drawer.left(90)
    drawer.penup()
    
    # Rim (The Target)
    drawer.goto(180, 40)
    drawer.color("red")
    drawer.pendown()
    drawer.forward(40)
    drawer.penup()

# --- UI ---
ui = turtle.Turtle()
ui.hideturtle()
ui.penup()
ui.color("white")

def update_ui():
    ui.clear()
    ui.goto(-240, 160)
    ui.write(f"SCORE: {score}", font=("Courier", 16, "bold"))
    ui.goto(100, 160)
    ui.write(f"TIME: {int(time_left)}s", font=("Courier", 16, "bold"))
    
    if not is_shooting and power > 0:
        ui.goto(-240, -180)
        ui.color("yellow")
        ui.write(f"POWER: {'|' * (power//2)}", font=("Courier", 14, "bold"))

# --- Shooting Logic ---
def charge_power():
    global power
    if not is_shooting and time_left > 0:
        if power < 40:
            power += 1
            winsound.Beep(200 + (power * 10), 20)

def release_shot():
    global is_shooting, power
    if not is_shooting and power > 0:
        is_shooting = True
        ball.dx = power * 0.4
        ball.dy = power * 0.8
        winsound.Beep(600, 100)

def reset_ball():
    global is_shooting, power
    is_shooting = False
    power = 0
    ball.goto(-220, -140)
    ball.dx = 0
    ball.dy = 0

# --- Controls ---
wn.listen()
wn.onkeypress(charge_power, "space")
wn.onkeyrelease(release_shot, "space")

# --- Main Game Loop ---
draw_hoop()
last_time = time.time()

while time_left > 0:
    wn.update()
    current_loop_time = time.time()
    dt = current_loop_time - last_time
    last_time = current_loop_time
    
    time_left -= dt
    update_ui()
    
    if is_shooting:
        # Physics: Gravity pulls the ball down
        ball.dy -= 1.5 # Gravity constant
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)
        
        # Check for Scoring (The Net)
        if 180 < ball.xcor() < 220 and 30 < ball.ycor() < 50 and ball.dy < 0:
            score += 3
            winsound.Beep(1000, 100)
            winsound.Beep(1200, 100)
            print(f"SWISH! Score: {score}")
            reset_ball()
            
        # Check for hitting Backboard
        if ball.xcor() > 215 and 20 < ball.ycor() < 100:
            ball.dx *= -0.5 # Bounce back
            winsound.Beep(300, 50)

        # Reset if ball goes off screen or hits floor
        if ball.ycor() < -150 or ball.xcor() > 300:
            reset_ball()
            
    time.sleep(0.01)

# Game Over Screen
ui.clear()
ui.goto(0, 0)
ui.color("lime")
ui.write(f"GAME OVER!\nFINAL SCORE: {score}\nAlt+F4 to Close", align="center", font=("Courier", 24, "bold"))
wn.update()