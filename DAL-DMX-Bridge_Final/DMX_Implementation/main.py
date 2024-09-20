"""
 * @file main.py
 * @brief Main application entry point for the DMX Controller.
 * 
 * This script sets up the main Tkinter GUI window, creates input controls,
 * and starts the OLA client to handle DMX data.
"""
import tkinter as tk
import threading
from gui_components import create_input_controls, create_visual_window, update_page, update_visual_page
from globals import dmx_data, current_page, visual_current_page, universe, channels_per_page
from dmx_handler import run_ola_client, process_queue

"""
 * @brief Initialize the Tkinter GUI and start the application.
 * 
 * Creates input controls for DMX channels, sets up navigation buttons,
 * initializes the visual display window, and starts the DMX receiver
 * in a separate thread. Also begins processing the DMX data queue.
"""
# Tkinter GUI setup
root = tk.Tk()
root.title("DMX Controller")

# Lists to hold slider references
sliders = []
labels = []

# Create input controls for one page of channels
create_input_controls(root, sliders, labels)

# Navigation controls
prev_button = tk.Button(root, text="Previous Page", command=lambda: update_page(max(current_page - 1, 0), sliders, labels))
prev_button.pack(side="left")

next_button = tk.Button(root, text="Next Page", command=lambda: update_page(min(current_page + 1, (512 // channels_per_page) - 1), sliders, labels))
next_button.pack(side="right")

# Create the visual display window
create_visual_window(root)

# Start with the first page in the visual window
update_visual_page(0)

# Start with the first page
update_page(0, sliders, labels)

# Start the DMX receiver in a separate thread
threading.Thread(target=run_ola_client, daemon=True).start()

# Start processing the queue
root.after(100, process_queue, root)

# Start the Tkinter main loop
root.mainloop()
