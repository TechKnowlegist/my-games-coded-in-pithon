import turtle
import tkinter as tk
from tkinter import messagebox
import winsound
import time

# --- 1. ACCESSIBILITY & AUDIO ---
def play_sound(style):
    try:
        if style == "jump": winsound.Beep(600, 50)
        elif style == "msg": winsound.Beep(800, 100)
    except: pass

def show_dialog(character, message):
    play_sound("msg")
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(f"TRANSMISSION: {character}", message)
    root.destroy()

# --- 2. ENGINE SETUP ---
wn = turtle.Screen()
wn.bgcolor("#050510")
wn.setup(800, 600)
wn.tracer(0)

# Physics & Movement Variables
GRAVITY = -1.0
JUMP_STRENGTH = 16
MOVE_SPEED = 8  # How fast you move while holding keys
player_dy = 0
on_ground = False

# KEY STATES (This is the secret to smooth movement)
keys = {"a": False, "d": False, "space": False}

# Actors
player = turtle.Turtle("square")
player.color("cyan")
player.penup()
player.goto(-350, -200)

# Platforms: [x_start, y_top, width, height]
platforms = [
    [-400, -240, 800, 40],   
    [-50, -120, 150, 20],    
    [150, 0, 150, 20],       
    [-100, 120, 200, 20],    
    [100, 220, 100, 20]      
]

draw_pen = turtle.Turtle()
draw_pen.hideturtle()
draw_pen.penup()

def draw_world():
    draw_pen.clear()
    for p in platforms:
        draw_pen.goto(p[0], p[1] - p[3])
        draw_pen.color("#444466")
        draw_pen.begin_fill()
        for _ in range(2):
            draw_pen.forward(p[2])
            draw_pen.left(90)
            draw_pen.forward(p[3])
            draw_pen.left(90)
        draw_pen.end_fill()

# --- 3. KEYBOARD LISTENERS ---
def k_a_on(): keys["a"] = True
def k_a_off(): keys["a"] = False
def k_d_on(): keys["d"] = True
def k_d_off(): keys["d"] = False
def k_space_on(): keys["space"] = True
def k_space_off(): keys["space"] = False

wn.listen()
wn.onkeypress(k_a_on, "a")
wn.onkeyrelease(k_a_off, "a")
wn.onkeypress(k_d_on, "d")
wn.onkeyrelease(k_d_off, "d")
wn.onkeypress(k_space_on, "space")
wn.onkeyrelease(k_space_off, "space")

# --- 4. MAIN GAME LOOP ---
show_dialog("AURA", "I've optimized your movement processors, 707. You can now hold A or D to glide across the platforms.")

while True:
    wn.update()
    draw_world()
    
    # --- HANDLE CONTINUOUS MOVEMENT ---
    if keys["a"]:
        player.setx(player.xcor() - MOVE_SPEED)
    if keys["d"]:
        player.setx(player.xcor() + MOVE_SPEED)
    if keys["space"] and on_ground:
        player_dy = JUMP_STRENGTH
        on_ground = False
        play_sound("jump")

    # --- APPLY PHYSICS ---
    player_dy += GRAVITY
    player.sety(player.ycor() + player_dy)

    # --- COLLISION LOGIC ---
    on_ground = False
    for p in platforms:
        px, py, pw, ph = p
        if px < player.xcor() < px + pw:
            if py - 10 < player.ycor() < py + 5 and player_dy <= 0:
                player.sety(py)
                player_dy = 0
                on_ground = True

    # Boundary Safety
    if player.ycor() < -400:
        player.goto(-350, -200)
        player_dy = 0

    # Exit Condition
    if player.ycor() > 220 and 100 < player.xcor() < 200:
        show_dialog("AURA", "Smooth exit, 707. Proceeding to the Core...")
        break

    time.sleep(0.01)