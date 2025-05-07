# main.py
#
# Description:
# This file serves as the entry point for the Fish Eco Sim application.
# It is responsible for initializing the Pygame library, setting up the display
# window, creating the main simulation world instance, and running the primary
# game loop. It orchestrates the interaction between Pygame events, the simulation
# logic (world updates), and the user interface drawing.
#
# Key responsibilities of this file:
# - Initialize the Pygame library.
# - Set up and manage the display window and frame rate.
# - Create the instance of the SimulationWorld.
# - Run the main application loop (event handling, world update, drawing).
# - Handle basic event types (like closing the window).
# - Pass relevant events to the UI for handling.
# - Shut down Pygame gracefully upon exit.
#
# Design Philosophy/Notes:
# - Keeps the main loop structure simple and high-level, delegating complex
#   logic to the 'world' and 'ui' modules.
# - Acts as a central hub for the three main phases of a game loop: input,
#   update, and draw.
# - Initializes critical components (Pygame, UI) before entering the loop.

# Imports Description:
# This section lists the modules imported by main.py and their purpose.
# - pygame: The core library for creating the game window, handling events, drawing, etc.
# - sys: Used for exiting the application gracefully.
# - config: Imports constants needed for display setup (width, height, FPS, panel size).
# - world.SimulationWorld: Imports the main simulation manager class responsible for the game state.
# - ui.draw_ui, ui.handle_ui_event, ui.init_ui: Imports functions for UI setup, drawing the UI, and processing UI-related events.

# Code Block Descriptions:
# This section provides detailed blueprints for the code blocks implemented below.
# These blocks are executed sequentially when the script runs.

# 1. Pygame Initialization and Setup
# Description:
# Initializes the Pygame library, sets up the main display window with the specified
# dimensions and title, creates a clock object to control the frame rate, and
# calls the UI initialization function (which sets up UI fonts, etc.). This block
# must be executed before most other Pygame functions are used.
# Inputs: None.
# Where Inputs Typically Come From: Constants defined in config.py.
# Restrictions on Inputs: None.
# Other Relevant Info: Executed directly when the script is imported or run.
#
# Description of Algorithm/Process:
# 1. Call `pygame.init()` to initialize all Pygame modules.
# 2. Set the display mode using `pygame.display.set_mode()`, using the total width from config.
# 3. Set the window title using `pygame.display.set_caption()`.
# 4. Create a `pygame.time.Clock()` instance.
# 5. Call the `init_ui()` function from the ui module to perform UI-specific initialization.
# 6. Optional: Print confirmation messages.
#
# Description of Output:
# None. Side effects include creating the game window, initializing Pygame state,
# and setting up the clock and UI resources.

# 2. Function: main
# Description:
# Contains the primary simulation loop that runs as long as the application is open.
# It manages the flow of the simulation tick: handling user input/events, updating
# the simulation world state, and drawing the current state to the screen.
# Inputs: None.
# Where Inputs Typically Come From: Called by the script entry point (`if __name__ == "__main__":`).
# Restrictions on Inputs: None.
# Other Relevant Info: This function defines the core rhythm of the simulation.
#
# Description of Algorithm/Process:
# 1. Create an instance of the `SimulationWorld` class to initialize the game state.
# 2. Initialize a boolean variable `running` to `True` to control the loop.
# 3. Enter a `while running:` loop.
# 4. --- Event Handling ---
#    a. Iterate through all pending events in `pygame.event.get()`.
#    b. If a `pygame.QUIT` event is found (window close button), set `running` to `False`.
#    c. Pass the event to `handle_ui_event()` from the ui module. If it returns `True` (meaning the UI handled the event), skip the rest of the event processing for this event.
#    d. (Placeholder) Handle any other non-UI events if needed.
# 5. --- World Update ---
#    a. Call `world.update()` to advance the simulation logic by one tick (agents move, eat, age, food spawns, etc.). The `world.update` method internally checks if the simulation is paused or stepping before executing logic.
# 6. --- Drawing ---
#    a. Call `world.draw(screen)` to draw the simulation grid, agents, and food onto the display surface.
#    b. Call `draw_ui(screen, world)` to draw the UI panel, buttons, and selected agent info onto the display surface, overlaying the world drawing.
# 7. --- Update Display ---
#    a. Call `pygame.display.flip()` to make all drawn elements visible on the screen.
# 8. --- Cap Frame Rate ---
#    a. Call `clock.tick(FPS)` to limit the loop's execution speed to the configured frames per second.
# 9. Once the loop condition `running` becomes `False`, exit the loop.
# 10. Call `pygame.quit()` to uninitialize Pygame.
# 11. Call `sys.exit()` to terminate the script.
#
# Description of Output:
# None. The primary output is the visual simulation displayed in the Pygame window,
# updated each frame. Side effects include modifying the state of the SimulationWorld
# object and handling application shutdown.

# 3. Script Entry Point
# Description:
# Standard Python construct to check if the script is being run directly (as opposed
# to being imported as a module). If it is the main script, it calls the `main()`
# function to start the application.
# Inputs: None.
# Where Inputs Typically Come From: Implicit from the way the script is executed by the Python interpreter.
# Restrictions on Inputs: None.
# Other Relevant Info: Ensures the `main()` function is only called when intended.
#
# Description of Algorithm/Process:
# 1. Check if the special variable `__name__` is equal to the string `"__main__"`.
# 2. If the condition is true, call the `main()` function.
#
# Description of Output:
# None. The output is the execution flow being passed to the `main()` function if
# the script is run directly.


# --- START CODE IMPLEMENTATION ---

# Imports:
# Standard library imports first
import pygame
import sys

# Local package imports
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PANEL_WIDTH, TOTAL_SCREEN_WIDTH
from world import SimulationWorld # Manages the world state and updates
from ui import draw_ui, handle_ui_event, init_ui # UI components and initialization function


### 1. Pygame Initialization and Setup Implementation ###
pygame.init()
print("Pygame library initialized successfully.")

screen = pygame.display.set_mode((TOTAL_SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fish Eco Sim")
clock = pygame.time.Clock()

init_ui()
print("User Interface components initialized.")


### 2. Function: main Implementation ###
def main():
    print("Starting main simulation loop.")

    world = SimulationWorld()
    running = True

    # --- Main Simulation Loop ---
    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if handle_ui_event(event, world):
                continue # Skip subsequent event processing for this specific event

            # --- Handle other non-UI game-specific events here if needed ---

        # --- World Update ---
        world.update() # Update the world if simulation state allows

        # --- Drawing ---
        world.draw(screen)
        draw_ui(screen, world)

        # --- Update Display ---
        pygame.display.flip()

        # --- Cap Frame Rate ---
        clock.tick(FPS)

    # --- End of Main Simulation Loop ---

    # --- Quit Pygame ---
    pygame.quit()
    print("Pygame library quit.")
    sys.exit()


### 3. Script Entry Point Implementation ###
if __name__ == "__main__":
    main()

# --- END CODE IMPLEMENTATION ---