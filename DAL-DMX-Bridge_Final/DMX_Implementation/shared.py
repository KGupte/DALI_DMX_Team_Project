""""
 * @file shared.py
 * @brief Provides shared functions for formatting DMX data and updating the visual display.
 * 
 * Contains utility functions to format DMX bit structures for display and update
 * the visual representation of DMX channels.
"""
import tkinter as tk
from globals import dmx_data, channels_per_page  # Import dmx_data from globals
from dmx_handler import send_dmx

class VisualState:
    """ Singleton class to hold the state of visual labels and page. """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VisualState, cls).__new__(cls)
            cls._instance.visual_labels = []
            cls._instance.visual_current_page = 0
        return cls._instance

    def set_visual_labels(self, labels):
        self.visual_labels = labels

    def get_visual_labels(self):
        return self.visual_labels

    def set_visual_current_page(self, page):
        self.visual_current_page = page

    def get_visual_current_page(self):
        return self.visual_current_page

visual_state = VisualState()

def format_dmx_bit_structure(channel, value):
    """
     * @brief Format the DMX bit structure for display.
     * 
     * Creates a formatted string representing the DMX bit structure for a specific
     * channel. Includes simulated break and Mark After Break bits.
     * 
     * @param channel The DMX channel number.
     * @param value The brightness value of the channel.
     * 
     * @return A formatted string representing the DMX bit structure.
    """
    break_bits = '0' * 22  # Simulate the DMX break with 22 zeros
    mab_bits = '11'        # Simulate the Mark After Break with a couple of ones
    channel_data = format(value, '08b')  # Convert value to 8-bit binary
    return (f"Channel {channel + 1}:\n"
            f"Break: {break_bits}\n"
            f"MAB: {mab_bits}\n"
            f"Data: {channel_data}\n\n")

def update_visual_display(channel, value):
    """
     * @brief Update the channel visual display based on single channel brightness.
     * 
     * Updates the visual display for a specific DMX channel based on its brightness
     * value. Adjusts the color to represent the brightness level.
     * 
     * @param channel The DMX channel number.
     * @param value The brightness value of the channel.
    """
    state = visual_state
    visual_labels = state.get_visual_labels()
    visual_current_page = state.get_visual_current_page()

    if visual_labels is None:
        print("Visual labels not initialized.")
        return

    #print(f"Updating visual display for channel {channel} with value {value}")  # Debugging

    relative_channel = channel - visual_current_page * channels_per_page
    grey_value = 255 - int(value)
    color = f'#{grey_value:02x}{grey_value:02x}{grey_value:02x}'
    
    if 0 <= relative_channel < len(visual_labels):
        visual_labels[relative_channel][0].config(bg=color)
        visual_labels[relative_channel][1].config(bg=color)
        #print(f"Color set to {color}")  # Debugging

def update_brightness(channel, value, text_display=None):
    """
     * @brief Update the brightness of a specific DMX channel.
     * 
     * Adjusts the brightness value for a given DMX channel and sends the updated
     * DMX data. Optionally updates a text display with the formatted DMX bit structure.
     * 
     * @param channel The DMX channel number.
     * @param value The new brightness value for the channel.
     * @param text_display (Optional) The Tkinter Text widget to update with DMX bit structure.
    """
    dmx_data[channel] = int(value)
    send_dmx()  # Send the updated DMX data

    # Update the DMX Bit Structure Display
    bit_sequence = format_dmx_bit_structure(channel, int(value))
    if text_display:
        text_display.insert(tk.END, bit_sequence)  # Append instead of overwriting
        text_display.see(tk.END)  # Auto-scroll to the latest entry to keep view updated
    print(bit_sequence)
