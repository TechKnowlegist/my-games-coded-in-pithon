import turtle
import tkinter as tk
from tkinter import messagebox
import winsound
import time

# --- 1. ACCESSIBILITY & AUDIO ---
def play_sound(style):
    try:
        if style == "aura": winsound.Beep(900, 100)
        elif style == "malware": winsound.Beep(200, 400)
        elif style == "msg": winsound.Beep(600, 100)
        elif style == "step": winsound.Beep(450, 40)
    except: pass

def show_dialog(character, message, is_bad=False):
    """Real Windows dialog boxes for screen readers."""
    if is_bad:
        play_sound("malware")
        title = f"!!! WARNING: {character} !!!"
    else:
        play_sound("aura")
        title = f"TRANSMISSION: {character}"
    
    messagebox.showinfo(title, message)

# --- 2. ENGINE SETUP ---
wn = turtle.Screen()
wn.bgcolor("black")
wn.setup(800, 600)
wn.tracer(0)

# The Protagonist (Player)
player = turtle.Turtle("square")
player.color("cyan")
player.penup()

# The Companion (AURA)
aura = turtle.Turtle("circle")
aura.shapesize(0.5, 0.5)
aura.color("white")
aura.penup()

# Environmental Objects
walls = []
console = turtle.Turtle("triangle")
console.color("yellow")
console.penup()
console.hideturtle()

def create_wall(x, y, w, h):
    wall = turtle.Turtle("square")
    wall.shapesize(h/20, w/20)
    wall.color("#222222")
    wall.penup()
    wall.goto(x, y)
    walls.append(wall)

# --- 3. STORY EVENTS ---
def move_aura():
    """Aura follows the player with a slight delay."""
    # Aura stays slightly to the left and above the player
    aura.goto(player.xcor() - 25, player.ycor() + 25)

def start_chapter_1():
    player.goto(-320, -240)
    move_aura()
    
    show_dialog("AURA", "Unit 707? Can you hear me? It's AURA. Your memory banks are corrupted, but I'm here to help you get out.")
    
    show_dialog("MALWARE", "Look at the little ghosts playing in the dark. You don't belong here, 707. You're just scrap metal.", True)
    
    # Level Layout
    create_wall(0, -100, 20, 400) # Center Pillar
    console.goto(300, 200)
    console.showturtle()

# --- 4. MOVEMENT ---
def move(dx, dy):
    play_sound("step")
    old_x, old_y = player.xcor(), player.ycor()
    player.setx(old_x + dx)
    player.sety(old_y + dy)
    move_aura() # Aura moves when you move
    
    # Wall Collision
    for wall in walls:
        w_width = wall.shapesize()[1] * 20
        w_height = wall.shapesize()[0] * 20
        if abs(player.xcor() - wall.xcor()) < (w_width/2 + 10) and \
           abs(player.ycor() - wall.ycor()) < (w_height/2 + 10):
            player.goto(old_x, old_y)
            move_aura()

wn.listen()
wn.onkeypress(lambda: move(0, 40), "w")
wn.onkeypress(lambda: move(0, -40), "s")
wn.onkeypress(lambda: move(-40, 0), "a")
wn.onkeypress(lambda: move(40, 0), "d")

# --- 5. MAIN LOOP ---
start_chapter_1()
story_step = 0

while True:
    wn.update()
    
    # Interaction Logic
    if player.distance(console) < 40 and story_step == 0:
        show_dialog("AURA", "This is it! The Archive Console. Plug in your interface cable.")
        
        show_dialog("MALWARE", "If you touch that console, I'll fry your circuits, Echo. Last warning.", True)
        
        show_dialog("AURA", "Don't listen to him. He's just a virus. I've unlocked the path to the Core Sector to the North!")
        
        console.color("lime")
        story_step = 1
        # Move goal to the exit
        console.goto(0, 260)

    if story_step == 1 and player.ycor() > 240:
        show_dialog("AURA", "We're through! Keep moving, 707. I can feel the system heating up.")
        break

    time.sleep(0.01)