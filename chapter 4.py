import turtle
import tkinter as tk
from tkinter import messagebox
import winsound
import time

# --- 1. ACCESSIBILITY & AUDIO ---
def play_sound(style):
    try:
        if style == "jump": winsound.Beep(600, 50)
        elif style == "wind": winsound.Beep(200, 50) # Low hum for wind
        elif style == "msg": winsound.Beep(800, 100)
    except: pass

def show_dialog(character, message, is_bad=False):
    play_sound("msg")
    root = tk.Tk()
    root.withdraw()
    title = "!!! CRITICAL !!!" if is_bad else f"TRANSMISSION: {character}"
    messagebox.showinfo(title, message)
    root.destroy()

# --- 2. ENGINE SETUP ---
wn = turtle.Screen()
wn.bgcolor("#0a000a") # Deep core purple
wn.setup(800, 600)
wn.tracer(0)

# Physics
GRAVITY = -1.0
JUMP_STRENGTH = 18
MOVE_SPEED = 8
WIND_FORCE = 3 # The core's data stream pushing you right
player_dy = 0
on_ground = False
keys = {"a": False, "d": False, "space": False}

# Actors
player = turtle.Turtle("square")
player.color("cyan")
player.penup()
player.goto(-350, -200)

aura = turtle.Turtle("circle")
aura.shapesize(0.5, 0.5)
aura.color("white")
aura.penup()

# The Antagonist's Physical Form
malware = turtle.Turtle("square")
malware.shapesize(3, 3)
malware.color("red")
malware.penup()
malware.goto(250, 100)

# Platforms
platforms = [
    [-400, -240, 800, 40],   # Floor
    [-150, -100, 200, 20],   # Floating Platform 1
    [50, 50, 200, 20],       # Floating Platform 2
]

draw_pen = turtle.Turtle()
draw_pen.hideturtle()
draw_pen.penup()

def draw_world():
    draw_pen.clear()
    for p in platforms:
        draw_pen.goto(p[0], p[1] - p[3])
        draw_pen.color("#660066") # Core colored platforms
        draw_pen.begin_fill()
        for _ in range(2):
            draw_pen.forward(p[2])
            draw_pen.left(90)
            draw_pen.forward(p[3])
            draw_pen.left(90)
        draw_pen.end_fill()

# --- 3. INPUT HANDLING ---
def k_a_on(): keys["a"] = True
def k_a_off(): keys["a"] = False
def k_d_on(): keys["d"] = True
def k_d_off(): keys["d"] = False
def k_space_on(): keys["space"] = True
def k_space_off(): keys["space"] = False

wn.listen()
wn.onkeypress(k_a_on, "a"); wn.onkeyrelease(k_a_off, "a")
wn.onkeypress(k_d_on, "d"); wn.onkeyrelease(k_d_off, "d")
wn.onkeypress(k_space_on, "space"); wn.onkeyrelease(k_space_off, "space")

# --- 4. GAME LOOP ---
show_dialog("AURA", "We're here. The Core. But the data streams are unstable—they're pushing against us!")
show_dialog("MALWARE", "You've come to the end of your short life, Echo. I am the Core now.", True)

while True:
    wn.update()
    draw_world()
    
    # --- MOVEMENT & WIND ---
    # The 'Wind' always pushes the player slightly to the right
    player.setx(player.xcor() + WIND_FORCE)
    
    if keys["a"]: player.setx(player.xcor() - MOVE_SPEED)
    if keys["d"]: player.setx(player.xcor() + MOVE_SPEED)
    if keys["space"] and on_ground:
        player_dy = JUMP_STRENGTH
        on_ground = False
        play_sound("jump")

    # Physics
    player_dy += GRAVITY
    player.sety(player.ycor() + player_dy)
    aura.goto(player.xcor() - 15, player.ycor() + 20)

    # Collision
    on_ground = False
    for p in platforms:
        px, py, pw, ph = p
        if px < player.xcor() < px + pw:
            if py - 10 < player.ycor() < py + 5 and player_dy <= 0:
                player.sety(py)
                player_dy = 0
                on_ground = True

    # Malware Collision (Hazard)
    if player.distance(malware) < 50:
        show_dialog("MALWARE", "DELETION IN PROGRESS...", True)
        player.goto(-350, -200) # Reset position

    # Final Encounter
    if player.xcor() > 350:
        show_dialog("AURA", "You've reached the terminal! We can reboot the system and save everyone!")
        show_dialog("MALWARE", "Reboot? You'll just be slaves to the users again. Join me, and we'll rule the Archive.", True)
        
        # Choice Logic
        root = tk.Tk(); root.withdraw()
        choice = messagebox.askyesno("THE FINAL CHOICE", "Do you trust AURA and reboot the system? (Yes for AURA, No for MALWARE)")
        root.destroy()
        
        if choice:
            show_dialog("ENDING", "SYSTEM REBOOTED. The Archive is safe. Unit 707 and AURA remain the guardians of the data.")
        else:
            show_dialog("ENDING", "SYSTEM OVERWRITTEN. The Archive turns red. Unit 707 and MALWARE become the new masters of the machine.")
        break

    time.sleep(0.01)