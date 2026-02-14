import pygame
import random
import sys

# --- 1. INITIALIZATION ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NEON CHROMA: FOG MODE")
clock = pygame.time.Clock()

# --- 2. GAME VARIABLES ---
TILE_SIZE = 40
COLS, ROWS = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE

def generate_random_maze():
    # 1 = Wall, 0 = Path
    new_maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    for r in range(1, ROWS - 1):
        for c in range(1, COLS - 1):
            if random.random() > 0.3: # 70% chance of path
                new_maze[r][c] = 0
    
    # Ensure Start and End are clear
    new_maze[1][1] = 0
    new_maze[ROWS-2][COLS-2] = 2 # Goal
    return new_maze

def get_random_color():
    return (random.randint(100, 255), random.randint(50, 255), random.randint(100, 255))

# Initial State
maze = generate_random_maze()
wall_color = get_random_color()
player_rect = pygame.Rect(TILE_SIZE + 5, TILE_SIZE + 5, 25, 25)
flashlight_radius = 150

# Create a "Darkness" surface for the flashlight effect
fog_surface = pygame.Surface((WIDTH, HEIGHT))

# --- 3. MAIN LOOP ---
running = True
while running:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: # Press R to Reset Maze
                maze = generate_random_maze()
                wall_color = get_random_color()
                player_rect.topleft = (TILE_SIZE + 5, TILE_SIZE + 5)

    # Movement Logic
    keys = pygame.key.get_pressed()
    spd = 4
    dx, dy = 0, 0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -spd
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = spd
    if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -spd
    if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = spd

    # Collision X
    player_rect.x += dx
    for r in range(ROWS):
        for c in range(COLS):
            if maze[r][c] == 1:
                wall = pygame.Rect(c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if player_rect.colliderect(wall):
                    if dx > 0: player_rect.right = wall.left
                    if dx < 0: player_rect.left = wall.right

    # Collision Y
    player_rect.y += dy
    for r in range(ROWS):
        for c in range(COLS):
            if maze[r][c] == 1:
                wall = pygame.Rect(c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if player_rect.colliderect(wall):
                    if dy > 0: player_rect.bottom = wall.top
                    if dy < 0: player_rect.top = wall.bottom

    # Win Condition
    grid_x, grid_y = player_rect.centerx // TILE_SIZE, player_rect.centery // TILE_SIZE
    if maze[grid_y][grid_x] == 2:
        maze = generate_random_maze()
        wall_color = get_random_color()
        player_rect.topleft = (TILE_SIZE + 5, TILE_SIZE + 5)

    # --- 4. RENDERING ---
    screen.fill((5, 5, 15)) # Background

    # Draw Maze
    for r in range(ROWS):
        for c in range(COLS):
            rect = (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if maze[r][c] == 1:
                pygame.draw.rect(screen, wall_color, rect)
            elif maze[r][c] == 2:
                pygame.draw.rect(screen, (0, 255, 0), rect)

    # Draw Player
    pygame.draw.rect(screen, (0, 255, 255), player_rect)

    # --- 5. THE FLASHLIGHT EFFECT ---
    fog_surface.fill((0, 0, 0)) # Fill with total black
    # Cut a hole in the darkness
    pygame.draw.circle(fog_surface, (255, 255, 255), player_rect.center, flashlight_radius)
    # Set the white circle as transparent
    fog_surface.set_colorkey((255, 255, 255))
    # Draw the darkness over everything
    screen.blit(fog_surface, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()