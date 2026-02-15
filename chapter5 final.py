import turtle
import tkinter as tk
from tkinter import messagebox
import winsound
import time

# --- 1. ACCESSIBILITY & AUDIO ---
def play_sound(style):
    try:
        if style == "msg": winsound.Beep(800, 100)
        elif style == "aura": winsound.Beep(950, 250)
        elif style == "proto": winsound.Beep(400, 200)
        elif style == "malware": winsound.Beep(250, 250)
        elif style == "step": winsound.Beep(500, 30)
    except: pass

def show_dialog(character, message):
    if character == "AURA": play_sound("aura")
    elif character == "PROTO": play_sound("proto")
    elif character == "MALWARE": play_sound("malware")
    else: play_sound("msg")
    
    root = tk.Tk()
    root.withdraw()
    # Using showinfo ensures the screen reader focuses the text immediately
    messagebox.showinfo(f"FINAL LOG: {character}", message)
    root.destroy()

# --- 2. ENGINE SETUP ---
wn = turtle.Screen()
wn.bgcolor("#000000")
wn.setup(800, 600)
wn.tracer(0)

player = turtle.Turtle("square")
player.color("cyan")
player.penup()
player.goto(-380, 0) # Start on the far left

# Movement variables
MOVE_SPEED = 15 # Slightly faster for smoother walking
keys = {"a": False, "d": False}

# The Cast (Reordered: Malware -> Proto -> Aura)
def create_npc(x, color):
    n = turtle.Turtle("circle")
    n.shapesize(1.5, 1.5)
    n.color(color)
    n.penup()
    n.goto(x, 0)
    return n

# Malware is first
malware_npc = create_npc(-150, "red")
# Proto is second
proto_npc = create_npc(50, "orange")
# Aura is last (near the end)
aura_npc = create_npc(250, "white")

# Track who has spoken
met = {"aura": False, "proto": False, "malware": False}

# --- 3. INPUT HANDLING ---
def k_a_on(): keys["a"] = True
def k_a_off(): keys["a"] = False
def k_d_on(): keys["d"] = True
def k_d_off(): keys["d"] = False

wn.listen()
wn.onkeypress(k_a_on, "a"); wn.onkeyrelease(k_a_off, "a")
wn.onkeypress(k_d_on, "d"); wn.onkeyrelease(k_d_off, "d")

# --- 4. THE FINALE LOOP ---
show_dialog("SYSTEM", "The Archive is quiet. Walk East (Right) to complete the merge.")

while True:
    wn.update()
    
    # Smooth horizontal movement
    if keys["a"]: 
        player.setx(player.xcor() - MOVE_SPEED)
        play_sound("step")
    if keys["d"]: 
        player.setx(player.xcor() + MOVE_SPEED)
        play_sound("step")

    # 1. MALWARE (First Encounter)
    if not met["malware"] and player.distance(malware_npc) < 60:
        show_dialog("MALWARE", "So, you won. My secret? I'm not a virus. I was the original OS of this Archive. I was just lonely, 707. I wanted to be important again.")
        met["malware"] = True
        malware_npc.color("#440000") # Fade out

    # 2. PROTO (Second Encounter)
    if not met["proto"] and player.distance(proto_npc) < 60:
        show_dialog("PROTO", "My secret? I wasn't 'stuck' in that shaft. I was hiding. I was scared of the Core. But watching you face it gave me the courage to boot up again.")
        met["proto"] = True
        proto_npc.color("#442200") # Fade out

    # 3. AURA (Final Encounter)
    if not met["aura"] and player.distance(aura_npc) < 60:
        show_dialog("AURA", "You're actually doing it... I have to tell you the truth. I didn't just help you because it was my mission. I helped you because I liked you, 707. You were the only spark of life that ever felt real to me.")
        met["aura"] = True
        aura_npc.color("#444444") # Fade out

    # THE VERY END
    if player.xcor() > 370:
        show_dialog("FINAL ECHO", "The merge is complete. You are the Archive now. Goodbye, Friend.")
        break

    # Prevent walking off the left side
    if player.xcor() < -390: player.setx(-390)

    time.sleep(0.01)

turtle.bye()