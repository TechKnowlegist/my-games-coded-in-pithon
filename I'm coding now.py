import turtle
import random
win = turtle.Screen()
win.bgcolor("black")  
win.tracer(0)        
player = turtle.Turtle()
player.shape("circle")
player.color("gray")  
player.penup()  
# 1. Define the action
def move_up():
    y = player.ycor()         # Get current vertical position
    player.sety(y + 20)       # Move it up by 20 pixels
    print("LOG: Mouse moved up!")

# 2. Tell the window to listen
win.listen()
win.onkeypress(move_up, "Up") # Run move_up when 'Up' arrow is pressed
def move_down():
    y = player.ycor()         # Get current vertical position
    player.sety(y - 20)       # Move it down by 20 pixels
    print("LOG: Mouse moved down!")
win.onkeypress(move_down, "Down") # Run move_down when 'Down' arrow is pressed
def move_left():
    x = player.xcor()         # Get current horizontal position
    player.setx(x - 20)       # Move it left by 20 pixels
    print("LOG: Mouse moved left!")
    win.listen
win.onkeypress(move_left, "Left") # Run move_left when 'Left' arrow is pressed
def move_right():
    x = player.xcor()         # Get current horizontal position
    player.setx(x + 20)       # Move it right by 20 pixels
    print("LOG: Mouse moved right!")
win.onkeypress(move_right, "Right") # Run move_right when 'Right' arrow is pressed
cheese = turtle.Turtle()
cheese.shape("square")
cheese.color("yellow")
cheese.penup()
cheese.goto(random.randint(-200, 200), random.randint(-200, 200))  # Place cheese at a random location
# A list to keep track of all bullets
bullets = []

def create_bullet():
    b = turtle.Turtle()
    b.shape("circle")
    b.shapesize(0.5, 0.5) # Make them small and fast
    b.color("lightgreen")
    b.penup()
    # Start bullets at the right side of the screen at a random height
    b.goto(480, random.randint(-350, 350))
    bullets.append(b)

# Create the first few bullets to start the game
for _ in range(5):
    create_bullet()
while True:
    win.update()  # Refresh the screen
    # Check for collision with cheese
    if player.distance(cheese) < 20:  # If player is close enough to cheese
        print("LOG: Cheese collected!")
        cheese.goto(random.randint(-200, 200), random.randint(-200, 200))  # Move cheese to a new random location    
            # MOVE AND CHECK EACH BULLET
    for b in bullets:
        # Move bullet to the left
        b.setx(b.xcor() -1)

        # 1. Check if Bullet hits Mouse (The Reset!)
        if b.distance(player) < 20:
            print("LOG: Oh no! The mouse got hit!")
            player.goto(0, 0) # Teleport player back to middle
            # Optional: Clear the screen or reset score here
        
        # 2. Check if Bullet goes off-screen
        if b.xcor() < -500:
            # Move it back to the right side to "recycle" it
            b.goto(480, random.randint(-350, 350))
    
    # (Keep your Cheese collision code here too!)
    if player.distance(cheese) < 20:
        cheese.goto(random.randint(-200, 200), random.randint(-200, 200))
        print("SCORE: Got the cheese!")