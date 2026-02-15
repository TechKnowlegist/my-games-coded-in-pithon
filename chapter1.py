import turtle
import tkinter as tk
from tkinter import messagebox
import winsound
import time

# --- 1. ACCESSIBILITY & AUDIO ---
def play_sound(style):
    try:
        if style == "msg": winsound.Beep(800, 100)
        elif style == "wall": winsound.Beep(200, 150)
        elif style == "item": winsound.Beep(1000, 200)
        elif style == "step": winsound.Beep(400, 50) # Subtle feedback for movement
    except: pass

def show_dialog(title, message):
    play_sound("msg")
    # Native Windows box for screen reader focus
    messagebox.showinfo(title, message)

# --- 2. GAME ENGINE SETUP ---
wn = turtle.Screen()
wn.bgcolor("black")
wn.setup(800, 600)
wn.tracer(0)

player = turtle.Turtle("square")
player.color("cyan")
player.penup()

# Obstacles (The Walls of the Archive)
walls = []
# Items/NPCs
fragment = turtle.Turtle("triangle")
fragment.color("yellow")
fragment.penup()
fragment.hideturtle()

def create_wall(x, y, w, h):
    wall = turtle.Turtle("square")
    wall.shapesize(h/20, w/20) # Turtle shapes are 20x20 by default
    wall.color("#333333") # Dark grey
    wall.penup()
    wall.goto(x, y)
    walls.append(wall)

# --- 3. STORY LEVELS ---
def start_chapter_1():
    global walls, fragment
    player.goto(-300, -200)
    
    show_dialog("CHAPTER 1: THE SILICON GHOST", 
                "LOG 001: Power restored. You are Unit 707. "
                "The Archive is dark. Move north-east to find the primary console.")
    
    # Create a simple maze layout
    create_wall(-100, 0, 400, 20)  # Horizontal bar
    create_wall(100, -150, 20, 200) # Vertical bar
    
    fragment.goto(300, 200)
    fragment.showturtle()

# --- 4. MOVEMENT LOGIC ---
def move(dx, dy):
    play_sound("step")
    old_x, old_y = player.xcor(), player.ycor()
    player.setx(old_x + dx)
    player.sety(old_y + dy)
    
    # Wall Collision Detection
    for wall in walls:
        # Check if player is hitting the wall's rectangular bounds
        w_width = wall.shapesize()[1] * 20
        w_height = wall.shapesize()[0] * 20
        if abs(player.xcor() - wall.xcor()) < (w_width/2 + 10) and \
           abs(player.ycor() - wall.ycor()) < (w_height/2 + 10):
            play_sound("wall")
            player.goto(old_x, old_y) # Stop the player
            # Screen readers don't need a popup for every wall hit, 
            # the low beep is enough feedback.

wn.listen()
wn.onkeypress(lambda: move(0, 40), "w")
wn.onkeypress(lambda: move(0, -40), "s")
wn.onkeypress(lambda: move(-40, 0), "a")
wn.onkeypress(lambda: move(40, 0), "d")

# --- 5. MAIN LOOP ---
start_chapter_1()

story_state = "searching"

while True:
    wn.update()
    
    # Check if we found the fragment
    if player.distance(fragment) < 30 and story_state == "searching":
        play_sound("item")
        show_dialog("CONSOLE ACCESS", 
                    "A voice crackles through your speakers: 'Finally... a spark in the dark. "
                    "Unit 707, do you remember the war?'")
        
        # Change the level for the next part of the story
        story_state = "found"
        fragment.color("lime")
        show_dialog("OBJECTIVE UPDATED", "The Exit Port is now open to the North. Proceed to Chapter 2.")
        
        # New Goal Location
        fragment.goto(0, 250)
    
    # Check for level exit
    if story_state == "found" and player.distance(0, 250) < 30:
        show_dialog("TRANSITION", "Entering the Data Stream... Chapter 2 loading.")
        break

    time.sleep(0.01)