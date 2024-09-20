import tkinter as tk
from .dali_light import DALILight
from .constants import DALI_OFF, DALI_UP, DALI_DOWN, DALI_MAX_LEVEL, DALI_MIN_LEVEL


MAX_BRIGHTNESS = 255

"""
@brief Manages DALI lighting, organizing lights by address and controlling them.
"""
class DALIController:

    """
    @brief Initializes the DALIController with lights and a GUI.
    @param root The root Tkinter window.
    @param assignment_registry The registry for device assignments.
    """	
    def __init__(self, root, assignment_registry):
        self.lights = {}
        self.assignment_registry = assignment_registry
        self.lights_per_page = 16
        self.visual_current_page = 0
        self.create_visual_window(root)

    """
    @brief Creates a new light with a specified address.
    @param address The address to assign to the new light.
    @return None
    """
    def create_light(self, address):
        if address not in self.lights and address not in self.assignment_registry['dmx']:
            self.lights[address] = DALILight(address)
            self.assignment_registry['dali'].add(address)
            print(f"Light {address} created.")
        else:
            print(f"Address {address} already in use by another device.")

    """
    @brief Sends a command to a DALI light by address.
    @param dali_address The address of the DALI light.
    @param command The command to send.
    @return None
    """
    def send_dali_command(self, dali_address, command):
        light = self.lights.get(dali_address)
        if light:
            light.process_command(command)
            print(f"Sent command {command} to DALI light {dali_address}.")
            self.update_dali_display(dali_address, light.arc_power_level)
        else:
            print(f"No DALI light found at address {dali_address}.")

    """
    @brief Creates the Tkinter window to visualize DALI lights.
    @param root The root Tkinter window.
    @return None
    """
    def create_visual_window(self, root):
        self.visual_window = tk.Toplevel(root)
        self.visual_window.title("DALI Output Visualization")

        self.visual_labels = []
        for i in range(self.lights_per_page):
            label = tk.Label(self.visual_window, text="", bg='lightgrey', font=("Arial", 10), width=20, height=2, relief='solid')
            label.grid(row=i // 4, column=i % 4, padx=5, pady=5)
            self.visual_labels.append(label)

        nav_frame = tk.Frame(self.visual_window)
        nav_frame.grid(row=4, column=0, columnspan=4, pady=10)

        prev_button = tk.Button(nav_frame, text="Previous Page", command=lambda: self.update_visual_page(max(self.visual_current_page - 1, 0)))
        prev_button.pack(side="left", padx=10)

        next_button = tk.Button(nav_frame, text="Next Page", command=lambda: self.update_visual_page(min(self.visual_current_page + 1, (64 // self.lights_per_page) - 1)))
        next_button.pack(side="right", padx=10)

        self.update_visual_page(0)

    """
    @brief Updates the visual page to show the current set of lights.
    @param page The page number to display.
    @return None
    """
    def update_visual_page(self, page):
        self.visual_current_page = page
        start_address = self.visual_current_page * self.lights_per_page + 1
        for i in range(self.lights_per_page):
            address = start_address + i
            if address <= 64:
                self.visual_labels[i].config(text=f"Light {address}")
                light = self.lights.get(address)
                if light:
                    self.update_dali_display(address, light.arc_power_level)
                else:
                    self.visual_labels[i].config(bg='lightgrey')
            else:
                self.visual_labels[i].config(text="", bg='lightgrey')

    """
    @brief Refreshes the visual display for a specified light and brightness level.
    @param address The address of the DALI light.
    @param arc_power_level The power level for the light.
    @return None
    """
    def update_dali_display(self, address, arc_power_level):
        start_address = self.visual_current_page * self.lights_per_page + 1
        if start_address <= address < start_address + self.lights_per_page:
            relative_address = (address - start_address) % self.lights_per_page
            color_intensity = 255 - int((arc_power_level / MAX_BRIGHTNESS) * 255)
            color = f'#{color_intensity:02x}{color_intensity:02x}{color_intensity:02x}'
            self.visual_labels[relative_address].config(bg=color)
