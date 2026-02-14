import turtle
import random
import winsound
import time

# --- Game Setup ---
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 25 
COLS, ROWS = 15, 15

wn = turtle.Screen()
wn.title("NEON TREK: LIVE SPEEDRUN")
wn.bgcolor("black")
wn.setup(WIDTH, HEIGHT)
wn.tracer(0)

# Game State
mazes_completed = 0
has_teleport = False
player_pos = [0, 0]
maze_data = []
start_time = 0
best_time = None
waiting_for_input = False

# --- Drawing Tools ---
painter = turtle.Turtle()
painter.hideturtle()
painter.speed(0)
painter.penup()

ui_painter = turtle.Turtle()
ui_painter.hideturtle()
ui_painter.speed(0)
ui_painter.penup()
ui_painter.color("white")

# Separate turtle for the live timer so it can clear independently
timer_painter = turtle.Turtle()
timer_painter.hideturtle()
timer_painter.speed(0)
timer_painter.penup()
timer_painter.color("cyan")

player = turtle.Turtle()
player.shape("square")
player.color("white")
player.penup()

def draw_star(x, y, size, color):
    painter.goto(x, y - (size // 4)) 
    painter.color(color)
    painter.setheading(0)
    painter.begin_fill()
    for i in range(5):
        painter.forward(size)
        painter.right(144)
    painter.end_fill()

def draw_finish_line(x, y, size):
    half = size / 2
    positions = [(x, y), (x + half, y - half)]
    white_spots = [(x + half, y), (x, y - half)]
    painter.color("lime")
    for pos in positions:
        painter.goto(pos)
        painter.begin_fill()
        for _ in range(4):
            painter.forward(half)
            painter.right(90)
        painter.end_fill()
    painter.color("white")
    for pos in white_spots:
        painter.goto(pos)
        painter.begin_fill()
        for _ in range(4):
            painter.forward(half)
            painter.right(90)
        painter.end_fill()

def generate_maze():
    global maze_data, wall_color
    maze_data = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    neon_colors = ["cyan", "magenta", "deepskyblue", "red", "gold", "springgreen", "deeppink", "orange", "chartreuse"]
    wall_color = random.choice(neon_colors)
    stack = [(0, 0)]
    maze_data[0][0] = 0
    while stack:
        cx, cy = stack[-1]
        neighbors = []
        for dx, dy in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and maze_data[ny][nx] == 1:
                neighbors.append((nx, ny))
        if neighbors:
            nx, ny = random.choice(neighbors)
            maze_data[cy + (ny - cy)//2][cx + (nx - cx)//2] = 0
            maze_data[ny][nx] = 0
            stack.append((nx, ny))
        else:
            stack.pop()
    maze_data[ROWS-1][COLS-1] = 3 
    sx, sy = random.randrange(1, COLS, 2), random.randrange(1, ROWS, 2)
    maze_data[sy][sx] = 2 

def draw_game():
    painter.clear()
    ui_painter.clear()
    
    # Top Right UI
    ui_painter.goto(180, 260)
    ui_painter.write(f"MAZES: {mazes_completed}", align="center", font=("Courier", 14, "bold"))
    
    # Best Time UI
    if best_time is not None:
        ui_painter.goto(180, 240)
        ui_painter.color("gold")
        ui_painter.write(f"BEST: {best_time}s", align="center", font=("Courier", 12, "bold"))
        ui_painter.color("white")

    if has_teleport:
        ui_painter.goto(0, 260)
        ui_painter.color("yellow")
        ui_painter.write("STAR POWER ACTIVE!", align="center", font=("Courier", 14, "italic"))
        ui_painter.color("white")

    for y in range(ROWS):
        for x in range(COLS):
            sx = -180 + (x * GRID_SIZE)
            sy = 180 - (y * GRID_SIZE)
            if maze_data[y][x] == 1:
                painter.goto(sx, sy)
                painter.color(wall_color)
                painter.begin_fill()
                for _ in range(4): painter.forward(GRID_SIZE - 2); painter.right(90)
                painter.end_fill()
            elif maze_data[y][x] == 2:
                draw_star(sx + 2, sy - (GRID_SIZE // 2) + 5, 22, "yellow")
            elif maze_data[y][x] == 3:
                draw_finish_line(sx, sy, GRID_SIZE - 2)
    wn.update()

def update_timer():
    if not waiting_for_input:
        timer_painter.clear()
        elapsed = round(time.time() - start_time, 1)
        timer_painter.goto(-240, 260)
        timer_painter.write(f"TIME: {elapsed}s", align="left", font=("Courier", 16, "bold"))
        # Call this function again in 100ms
        wn.ontimer(update_timer, 100)

def start_new_level():
    global player_pos, has_teleport, start_time, waiting_for_input
    generate_maze()
    player_pos = [0, 0]
    has_teleport = False 
    waiting_for_input = False
    draw_game()
    update_player_vis()
    start_time = time.time()
    update_timer() # Start the live timer loop
    winsound.Beep(800, 100)

def update_player_vis():
    px, py = player_pos
    player.goto(-180 + (px * GRID_SIZE) + (GRID_SIZE//2), 180 - (py * GRID_SIZE) - (GRID_SIZE//2))
    wn.update()

def move(dx, dy):
    global has_teleport, mazes_completed, player_pos, waiting_for_input, best_time
    
    if waiting_for_input:
        start_new_level()
        return

    nx, ny = player_pos[0] + dx, player_pos[1] + dy
    if 0 <= nx < COLS and 0 <= ny < ROWS:
        cell = maze_data[ny][nx]
        if cell == 1:
            if has_teleport:
                winsound.Beep(400, 100)
                has_teleport = False 
                player_pos = [nx, ny]
                draw_game() 
            else:
                winsound.Beep(200, 50) 
        else:
            player_pos = [nx, ny]
            if cell == 2:
                has_teleport = True
                maze_data[ny][nx] = 0 
                winsound.Beep(1200, 200)
                draw_game()
            elif cell == 3:
                # VICTORY
                elapsed = round(time.time() - start_time, 2)
                waiting_for_input = True
                mazes_completed += 1
                
                # Update Best Time
                if best_time is None or elapsed < best_time:
                    best_time = elapsed
                    print(f"NEW RECORD! {elapsed} seconds!")
                
                ui_painter.goto(0, 0)
                ui_painter.color("lime")
                ui_painter.write(f"MAZE CLEAR!\nTIME: {elapsed}s\nPress Arrow to Next", align="center", font=("Courier", 20, "bold"))
                winsound.Beep(1000, 150); winsound.Beep(1200, 150)

    update_player_vis()

# --- Bindings ---
wn.onkeypress(lambda: move(0, -1), "Up")
wn.onkeypress(lambda: move(0, 1), "Down")
wn.onkeypress(lambda: move(-1, 0), "Left")
wn.onkeypress(lambda: move(1, 0), "Right")
wn.listen()

start_new_level()
wn.mainloop()