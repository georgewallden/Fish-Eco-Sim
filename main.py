import pygame
import sys
from config import *
from agent import Agent

# Extend screen for control panel
CONTROL_PANEL_WIDTH = 200
SCREEN_WIDTH_FULL = SCREEN_WIDTH + CONTROL_PANEL_WIDTH

# Simulation state
paused = False
pending_ticks = 0
tick_count = 0
fish = None
selected_agent = None

# Dropdown state
selected_tick_jump = 10
dropdown_visible = False
dropdown_rects = []

tick_jump_values = TICK_JUMP_VALUES

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH_FULL, SCREEN_HEIGHT))
pygame.display.set_caption("Ocean Simulation")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

def get_depth_color(row_index):
    depth_ratio = row_index / (GRID_ROWS - 1)
    base_r, base_g, base_b = OCEAN_BLUE
    r = int(base_r * (1 - depth_ratio * 1.0))
    g = int(base_g * (1 - depth_ratio * 0.9))
    b = int(base_b * (1 - depth_ratio * 0.7))
    return (max(r, 3), max(g, 8), max(b, 25))

def draw_grid(surface):
    for row in range(GRID_ROWS):
        row_color = get_depth_color(row)
        for col in range(GRID_COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, row_color, rect)
            pygame.draw.rect(surface, GRID_LINE_COLOR, rect, 1)

def draw_button(surface, rect, text, active=True):
    color = (180, 180, 180) if active else (100, 100, 100)
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, (0, 0, 0), rect, 2)
    label = font.render(text, True, (0, 0, 0))
    surface.blit(label, (rect.x + 10, rect.y + 8))

def draw_dropdown(surface):
    global dropdown_rects
    x = buttons["tick_10"].x
    y = buttons["tick_10"].bottom + 2
    width = buttons["tick_10"].width
    height = 30
    dropdown_rects = []

    for i, value in enumerate(tick_jump_values):
        rect = pygame.Rect(x, y + i * height, width, height)
        dropdown_rects.append((rect, value))
        pygame.draw.rect(surface, (200, 200, 200), rect)
        pygame.draw.rect(surface, (0, 0, 0), rect, 1)
        label = font.render(f"Run {value} Ticks", True, (0, 0, 0))
        surface.blit(label, (rect.x + 10, rect.y + 5))

def draw_panel(surface):
    panel_rect = pygame.Rect(SCREEN_WIDTH, 0, CONTROL_PANEL_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(surface, (220, 220, 240), panel_rect)

    draw_button(surface, buttons["start"], "Start", paused)
    draw_button(surface, buttons["pause"], "Pause", not paused)
    draw_button(surface, buttons["reset"], "Reset")
    draw_button(surface, buttons["tick_once"], "Tick Once")
    draw_button(surface, buttons["tick_10"], f"Run {selected_tick_jump} Ticks")

    label = font.render(f"Tick: {tick_count}", True, (0, 0, 0))
    surface.blit(label, (SCREEN_WIDTH + 10, 250))

    if selected_agent:
        surface.blit(font.render("Selected Agent:", True, (0, 0, 0)), (SCREEN_WIDTH + 10, 300))
        surface.blit(font.render(f"Pos: ({selected_agent.x}, {selected_agent.y})", True, (0, 0, 0)), (SCREEN_WIDTH + 10, 325))
        surface.blit(font.render(f"Dir: {selected_agent.direction}", True, (0, 0, 0)), (SCREEN_WIDTH + 10, 350))
        surface.blit(font.render(f"Speed: {selected_agent.move_interval_ticks} ticks", True, (0, 0, 0)), (SCREEN_WIDTH + 10, 375))

    if dropdown_visible:
        draw_dropdown(surface)

buttons = {
    "start": pygame.Rect(SCREEN_WIDTH + 20, 20, 160, 35),
    "pause": pygame.Rect(SCREEN_WIDTH + 20, 65, 160, 35),
    "reset": pygame.Rect(SCREEN_WIDTH + 20, 110, 160, 35),
    "tick_once": pygame.Rect(SCREEN_WIDTH + 20, 155, 160, 35),
    "tick_10": pygame.Rect(SCREEN_WIDTH + 20, 200, 160, 35),
}

def main():
    global paused, pending_ticks, tick_count, fish, selected_agent
    global selected_tick_jump, dropdown_visible

    fish = Agent(GRID_COLS // 2, GRID_ROWS // 2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons["start"].collidepoint(event.pos):
                    paused = False
                elif buttons["pause"].collidepoint(event.pos):
                    paused = True
                elif buttons["reset"].collidepoint(event.pos):
                    fish = Agent(GRID_COLS // 2, GRID_ROWS // 2)
                    tick_count = 0
                    selected_agent = None
                elif buttons["tick_once"].collidepoint(event.pos):
                    pending_ticks += 1
                elif buttons["tick_10"].collidepoint(event.pos):
                    if event.button == 1:
                        pending_ticks += selected_tick_jump
                    elif event.button == 3:
                        dropdown_visible = not dropdown_visible
                elif dropdown_visible:
                    for rect, value in dropdown_rects:
                        if rect.collidepoint(event.pos):
                            selected_tick_jump = value
                            dropdown_visible = False
                            break
                else:
                    mx, my = event.pos
                    if mx < SCREEN_WIDTH:
                        clicked_col = mx // CELL_SIZE
                        clicked_row = my // CELL_SIZE
                        if fish.x == clicked_col and fish.y == clicked_row:
                            selected_agent = fish
                        else:
                            selected_agent = None
                    dropdown_visible = False

        draw_grid(screen)

        # ✅ Only move agents when simulation is running
        if not paused or pending_ticks > 0:
            fish.move()
            tick_count += 1
            if pending_ticks > 0:
                pending_ticks -= 1

        fish.draw(screen, is_selected=(fish == selected_agent))
        draw_panel(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
