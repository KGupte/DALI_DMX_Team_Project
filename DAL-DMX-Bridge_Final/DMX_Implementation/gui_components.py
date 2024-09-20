"""
 * @file gui_components.py
 * @brief Provides functions to create and manage GUI components for the DMX Controller.
"""
import tkinter as tk
from globals import dmx_data, current_page, channels_per_page
from shared import format_dmx_bit_structure, update_brightness, visual_state

def create_input_controls(root, sliders, labels):
    """
     * @brief Create sliders and labels for DMX input controls.
     * 
     * Sets up a series of sliders and labels for each DMX channel on the
     * current page. Sliders are used to adjust the brightness of each channel.
     * 
     * @param root The Tkinter root window.
     * @param sliders List to store references to slider widgets.
     * @param labels List to store references to label widgets.
    """
    for i in range(channels_per_page):
        frame = tk.Frame(root)
        frame.pack()
        
        label = tk.Label(frame, text=f"Channel {i + 1}")
        label.pack(side="left")
        labels.append(label)
        
        slider = tk.Scale(frame, from_=0, to=255, orient='horizontal',
                          command=lambda value, ch=i: update_brightness(ch + current_page * channels_per_page, value, text_display))
        slider.pack(side="right")
        sliders.append(slider)

def create_visual_window(root):
    """
     * @brief Create the visual display window for DMX output.
     * 
     * Initializes the visual display window with frames and labels to represent
     * each DMX channel on the current page. Sets up navigation buttons for
     * paging through the visual display.
     * 
     * @param root The Tkinter root window to which the visual window will be attached.
    """
    global visual_window, text_display
    visual_window = tk.Toplevel(root)
    visual_window.title("DMX Output Visualization")
    visual_window.geometry("600x500")  # Increase window height for better visibility

    visual_frame = tk.Frame(visual_window)
    visual_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    visual_labels = []
    for i in range(channels_per_page):
        frame = tk.Frame(visual_frame, width=140, height=80, bg='white', relief='solid')
        frame.grid(row=i // 4, column=i % 4, padx=10, pady=10, sticky='nsew')

        label = tk.Label(frame, text="", bg='white', font=("Arial", 12))
        label.pack(expand=True, fill='both')
        visual_labels.append((frame, label))

    # Set visual labels in the singleton
    visual_state.set_visual_labels(visual_labels)

    text_display = tk.Text(visual_window, height=10, bg='lightgrey', font=("Arial", 10))
    text_display.grid(row=2, column=0, padx=20, pady=10, sticky='ew')

    nav_frame = tk.Frame(visual_window)
    nav_frame.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

    prev_button = tk.Button(nav_frame, text="Previous Page", command=lambda: update_visual_page(max(visual_state.get_visual_current_page() - 1, 0)))
    prev_button.pack(side="left", padx=10)

    next_button = tk.Button(nav_frame, text="Next Page", command=lambda: update_visual_page(min(visual_state.get_visual_current_page() + 1, (512 // channels_per_page) - 1)))
    next_button.pack(side="right", padx=10)

    visual_window.grid_rowconfigure(0, weight=1)
    visual_window.grid_rowconfigure(1, weight=0)
    visual_window.grid_columnconfigure(0, weight=1)

    for i in range(channels_per_page):
        visual_frame.grid_rowconfigure(i // 4, weight=1)
        visual_frame.grid_columnconfigure(i % 4, weight=1)

def update_page(page, sliders, labels):
    """
     * @brief Update the sliders and labels to reflect the DMX channels for the current page.
     * 
     * Adjusts the sliders and labels to match the DMX data for the channels on
     * the specified page. Also updates the visual display for the channels.
     * 
     * @param page The page number to update.
     * @param sliders List of slider widgets to be updated.
     * @param labels List of label widgets to be updated.
    """
    global current_page
    current_page = page
    start_channel = current_page * channels_per_page

    for i in range(min(channels_per_page, len(sliders), len(labels))):
        channel = start_channel + i
        if channel < len(dmx_data):
            sliders[i].set(dmx_data[channel])
            labels[i].config(text=f"Channel {channel + 1}")
            # Import inside function to avoid circular import
            from shared import update_visual_display
            update_visual_display(channel, dmx_data[channel])

def update_visual_page(page):
    """
     * @brief Update the visual display to show the correct channels for the current page.
     * 
     * Adjusts the visual representation of the DMX channels based on the specified
     * page number. Updates the labels with the current channel data.
     * 
     * @param page The page number to update in the visual display.
    """
    state = visual_state
    state.set_visual_current_page(page)
    start_channel = page * channels_per_page
    for i in range(channels_per_page):
        channel = start_channel + i
        if 0 <= channel < len(dmx_data):
            # Import inside function to avoid circular import
            from shared import update_visual_display
            update_visual_display(channel, dmx_data[channel])
            visual_labels = state.get_visual_labels()
            visual_labels[i][1].config(text=f"Channel {channel+1}")
