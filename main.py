# main.py
# Launches the 2D emergent ecosystem simulation

import pygame
import sys
# Import necessary constants from the config file
# Import TOTAL_SCREEN_WIDTH as well since it's used for display setup
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PANEL_WIDTH, TOTAL_SCREEN_WIDTH

# Import core simulation components
from world import SimulationWorld # Manages the world state and updates

# Import UI components and initialization function
# init_ui must be called after pygame.init()
from ui import draw_ui, handle_ui_event, init_ui


# --- Initialize Pygame and Core Modules ---
# This must be called BEFORE using any pygame modules like font, display, etc.
pygame.init()
print("Pygame library initialized successfully.") # Optional message to confirm initialization

# --- Set up the Display and Clock ---
# These require pygame.init() to be called first
# Set the display mode, including space for the UI panel using TOTAL_SCREEN_WIDTH
screen = pygame.display.set_mode((TOTAL_SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fish Eco Sim") # Set window title
clock = pygame.time.Clock() # Create a Clock object to manage frame rate

# --- Initialize UI Components (especially fonts) ---
# Call the UI initialization function *after* pygame.init()
init_ui()
print("User Interface components initialized.") # Optional message to confirm UI setup


def main():
    """
    The main function that runs the simulation loop.
    This function is executed when the script is run directly.
    """
    print("Starting main simulation loop.") # Optional message indicating the start of the loop

    # Create an instance of the SimulationWorld.
    # This sets up the initial grid, agents, and food.
    world = SimulationWorld()

    running = True # This boolean variable controls whether the main loop is active

    # --- Main Simulation Loop ---
    while running:
        # --- Event Handling ---
        # Process all events that have occurred since the last frame (e.g., mouse clicks, key presses, window close).
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # If the user clicks the window close button, set running to False to exit the loop.
                running = False

            # Pass the event to the UI event handler.
            # This allows buttons, dropdowns, and agent selection clicks to be processed by the UI logic.
            # If the UI handles the event (e.e., a button is clicked), handle_ui_event should return True.
            if handle_ui_event(event, world):
                continue # Skip subsequent event processing for this specific event

            # --- Handle other non-UI game-specific events here if needed ---
            # Example: If you add keyboard controls for zooming or moving the view, handle them here.


        # --- World Update ---
        # Only update the world if the simulation is not paused
        # The world.update() method contains the logic to check SimulationState.is_running()
        world.update()

        # --- Drawing ---
        # Clear the screen (optional, but good practice if not drawing a full background)
        # screen.fill((0, 0, 0)) # Black background example - might conflict with grid drawing

        # Draw the simulation grid background and all agents/food within the grid area.
        world.draw(screen)

        # Draw the User Interface panel and any elements that overlay the simulation or panel,
        # such as buttons, text displays, and the dropdown menu.
        draw_ui(screen, world)

        # --- Update Display ---
        # Make everything that has been drawn visible on the screen.
        pygame.display.flip() # Updates the entire screen. Use pygame.display.update() for partial updates if performance is critical.

        # --- Cap Frame Rate ---
        # Limit the speed of the loop to the desired frames per second.
        # This ensures the simulation doesn't run too fast and manages CPU usage.
        clock.tick(FPS)

    # --- End of Main Simulation Loop ---

    # --- Quit Pygame ---
    # Once the main loop finishes (e.g., user closed the window), uninitialize Pygame.
    pygame.quit()
    print("Pygame library quit.") # Optional message to confirm Pygame shutdown
    sys.exit() # Exit the Python script


# --- Script Entry Point ---
# Check if this script is being run directly (not imported as a module).
# If it is, call the main function to start the simulation.
if __name__ == "__main__":
    main()