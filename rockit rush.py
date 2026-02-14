import turtle
import time
import random

# Game Setup
score = 0
high_score = 0
delay = 0.01 # Faster loop for smoother movement

# Screen configuration
wn = turtle.Screen()
wn.title("Meteor Dodge")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)

# The Player (Defender)
player = turtle.Turtle()
player.speed(0)
player.shape("square")
player.color("cyan")
player.penup()
player.goto(0, -250)

# The Meteor
meteor = turtle.Turtle()
meteor.speed(0)
meteor.shape("circle")
meteor.color("red")
meteor.penup()
meteor.goto(0, 300)

# Movement functions
def go_left():
    x = player.xcor()
    if x > -280:
        player.setx(x - 30)

def go_right():
    x = player.xcor()
    if x < 280:
        player.setx(x + 30)

# Key bindings
wn.listen()
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

print("Game Started! Use Left and Right arrows to dodge the meteors.")

# Main game loop
while True:
    wn.update()

    # Move the meteor down
    y = meteor.ycor()
    meteor.sety(y - 5) # Gravity effect

    # Check if meteor hit the bottom
    if meteor.ycor() < -300:
        meteor.goto(random.randint(-280, 280), 300)
        score += 1
        print(f"Score: {score} | High Score: {high_score}")

    # Check for collision with player
    if meteor.distance(player) < 25:
        print(f"CRASH! You hit a meteor. Final Score: {score}")
        
        # Update high score
        if score > high_score:
            high_score = score
            print(f"NEW HIGH SCORE: {high_score}")
        
        time.sleep(1)
        score = 0
        player.goto(0, -250)
        meteor.goto(0, 300)

    time.sleep(delay)