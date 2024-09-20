import tkinter as tk
from tkinter import messagebox
from dali_controller import DALIController

# Constants
NUM_GROUPS = 16
MAX_BRIGHTNESS = 255

class DALIApp:
    """
    @brief This class defines the Tkinter-based GUI application for controlling DALI lights.
    """

    def __init__(self):
        """
        @brief Initialize the GUI components and DALI controller.
        """
        self.controller = DALIController()
        self.root = tk.Tk()
        self.root.title("DALI Light Control")

        # Command mapping
        self.command_map = {
            "Off": 0,
            "Up": 1,
            "Down": 2,
            "Max Level": 5,
            "Min Level": 6,
            "Reset": 32,
            "Query Actual Level": 33,
            "Terminate": 161,
            "Store to DTR": 163
        }

        self.create_widgets()
        self.create_light_matrix()

    def create_widgets(self):
        """
        @brief Create the main widgets for the DALI control interface.
        """
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(pady=10)

        # Entry for light address
        tk.Label(self.info_frame, text="Light Address:").pack(side=tk.LEFT, padx=5)
        self.address_entry = tk.Entry(self.info_frame, width=5)
        self.address_entry.pack(side=tk.LEFT, padx=5)

        # Button to create a light at a specific address
        tk.Button(self.info_frame, text="Add Light", command=self.add_light).pack(side=tk.LEFT, padx=5)

        # Entry for scene number
        tk.Label(self.info_frame, text="Scene Number (0-15):").pack(side=tk.LEFT, padx=5)
        self.scene_entry = tk.Entry(self.info_frame, width=5)
        self.scene_entry.pack(side=tk.LEFT, padx=5)
        self.scene_entry.insert(0, "0")  # Default scene number

        # Button to send scene command
        tk.Button(self.info_frame, text="Send Scene Command", command=self.send_scene_command).pack(side=tk.LEFT, padx=5)

        # Drop-down for controlling individual or group
        self.control_var = tk.StringVar(self.root)
        self.control_var.set("Individual")

        # Drop-down for commands
        self.command_var = tk.StringVar(self.root)
        self.command_var.set("Off")
        self.command_menu = tk.OptionMenu(self.info_frame, self.command_var, *self.command_map.keys())
        self.command_menu.pack(side=tk.LEFT, padx=5)

        # Individual Control Button
        tk.Button(self.info_frame, text="Send Individual Command", command=self.send_command).pack(side=tk.LEFT, padx=5)

        # Group entry for sending group commands
        tk.Label(self.info_frame, text="Group Number (0-15):").pack(side=tk.LEFT, padx=5)
        self.group_entry = tk.Entry(self.info_frame, width=5)
        self.group_entry.pack(side=tk.LEFT, padx=5)

        # Button to send group command
        tk.Button(self.info_frame, text="Send Group Command", command=self.send_group_command).pack(side=tk.LEFT, padx=5)

        # Display frame
        self.display_frame = tk.Frame(self.root)
        self.display_frame.pack(pady=10)
        self.text_area = tk.Text(self.display_frame, height=10, width=50)
        self.text_area.pack()

        # Bit Information Frame
        self.bit_info_frame = tk.Frame(self.root)
        self.bit_info_frame.pack(pady=10)
        self.bit_info_label = tk.Label(self.bit_info_frame, text="DALI Bit Information:")
        self.bit_info_label.pack()

        # Exit button
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def create_light_matrix(self):
        """
        @brief Create a matrix (grid) of buttons representing the lights and settings buttons.
        """
        self.light_matrix = tk.Frame(self.root)
        self.light_matrix.pack(pady=10)
        self.buttons = []

        for i in range(64):
            light_frame = tk.Frame(self.light_matrix)
            light_frame.grid(row=i // 8, column=i % 8, padx=5, pady=5)

            # Create the visual light indicator button
            light_button = tk.Button(light_frame, text=f"L{i}", width=5, height=2, state=tk.DISABLED)
            light_button.pack(side=tk.LEFT)
            self.buttons.append(light_button)

            # Create the small button for setting group and scene
            settings_button = tk.Button(light_frame, text="⚙️", command=lambda idx=i: self.open_scene_and_group_settings(idx), width=2)
            settings_button.pack(side=tk.RIGHT)

    def open_scene_and_group_settings(self, address):
        """
        @brief Open a window to set scene brightness levels and group assignment for a specific light.
        @param address Address of the light to configure.
        """
        if address not in self.controller.lights:
            self.controller.create_light(address)

        light = self.controller.lights[address]
        settings_window = tk.Toplevel(self.root)
        settings_window.title(f"Settings for Light {address}")

        # Scene Settings
        tk.Label(settings_window, text="Scene Settings").grid(row=0, column=0, columnspan=3)
        for scene_num in range(16):
            tk.Label(settings_window, text=f"Scene {scene_num} Brightness:").grid(row=scene_num + 1, column=0)
            brightness_entry = tk.Entry(settings_window, width=5)
            brightness_entry.insert(0, light.get_scene_brightness(scene_num))
            brightness_entry.grid(row=scene_num + 1, column=1)

            tk.Button(settings_window, text="Set", command=lambda sn=scene_num, be=brightness_entry: self.set_scene_brightness(address, sn, be)).grid(row=scene_num + 1, column=2)

        # Group Settings
        tk.Label(settings_window, text="Group Assignment").grid(row=17, column=0, columnspan=3)
        tk.Label(settings_window, text="Assign Group (0-15 or -1 to remove):").grid(row=18, column=0)
        group_entry = tk.Entry(settings_window, width=5)
        group_entry.grid(row=18, column=1)

        tk.Button(settings_window, text="Set Group", command=lambda: self.set_group_assignment(address, group_entry)).grid(row=18, column=2)

    def set_scene_brightness(self, address, scene_num, brightness_entry):
        """
        @brief Set the brightness for a specific scene for a light (store in memory only).
        @param address Address of the light.
        @param scene_num Scene number to be configured.
        @param brightness_entry The entry widget containing brightness value.
        """
        try:
            brightness = int(brightness_entry.get())
            if 0 <= brightness <= 255:
                self.controller.lights[address].set_scene_brightness(scene_num, brightness)
                self.update_display(f"Stored scene {scene_num} brightness to {brightness} for light {address}.")
            else:
                messagebox.showerror("Error", "Brightness must be between 0 and 255.")
        except ValueError:
            messagebox.showerror("Error", "Invalid brightness value entered.")

    def set_group_assignment(self, address, group_entry):
        """
        @brief Assign a group to a light based on user input.
        @param address Address of the light.
        @param group_entry The entry widget containing the group ID.
        """
        try:
            group_id = int(group_entry.get())
            if -1 <= group_id < NUM_GROUPS:
                self.controller.assign_light_to_group(address, group_id)
                if group_id == -1:
                    self.update_display(f"Removed light {address} from all groups.")
                else:
                    self.update_display(f"Assigned light {address} to group {group_id}.")
            else:
                messagebox.showerror("Error", "Group ID must be between 0 and 15, or -1 to remove from all groups.")
        except ValueError:
            messagebox.showerror("Error", "Invalid group ID entered.")

    def send_scene_command(self):
        """
        @brief Send a scene command and apply the corresponding brightness level for the scene.
        """
        try:
            scene_num = int(self.scene_entry.get())
            if 0 <= scene_num < 16:
                self.controller.send_scene_command(scene_num)
                for light in self.controller.lights.values():
                    self.update_light_button(light.address, light.arc_power_level)
                self.update_display(f"Sent scene {scene_num} command.")
            else:
                messagebox.showerror("Error", "Scene number must be between 0 and 15.")
        except ValueError:
            messagebox.showerror("Error", "Invalid scene number entered.")

    def add_light(self):
        """
        @brief Add a new light based on the address entered.
        """
        try:
            address = int(self.address_entry.get())
            if 0 <= address < 64:
                self.controller.create_light(address)
                self.update_light_button(address, self.controller.lights[address].arc_power_level)
                self.update_display(f"Light {address} added.")
            else:
                messagebox.showerror("Error", "Address must be between 0 and 63.")
        except ValueError:
            messagebox.showerror("Error", "Invalid address entered.")

    def send_command(self):
        """
        @brief Send a command to a DALI light.
        """
        try:
            address = int(self.address_entry.get())
            command = self.command_var.get()
            if 0 <= address < 64:
                self.controller.send_command(address << 1, self.command_map[command])  # Individual control
                self.update_light_button(address, self.controller.lights[address].arc_power_level)
                self.update_display(f"Sent command {command} to light {address}.")
                self.update_bit_info(address << 1, self.command_map[command])
            else:
                messagebox.showerror("Error", "Address must be between 0 and 63.")
        except ValueError:
            messagebox.showerror("Error", "Invalid address entered.")

    def send_group_command(self):
        """
        @brief Send a group command based on the selected command and group number.
        """
        try:
            group_id = int(self.group_entry.get())
            if 0 <= group_id < NUM_GROUPS:
                command = self.command_var.get()
                self.controller.send_command_to_group(group_id, self.command_map[command])
                for address in self.controller.groups.get(group_id, []):
                    self.update_light_button(address, self.controller.lights[address].arc_power_level)
                self.update_display(f"Sent group command {command} to group {group_id}.")
                self.update_bit_info(0x80 | (group_id << 1), self.command_map[command])
            else:
                messagebox.showerror("Error", "Group must be between 0 and 15.")
        except ValueError:
            messagebox.showerror("Error", "Invalid group number entered.")

    def update_bit_info(self, address_byte, data_byte):
        """
        @brief Update the bit information in the display.
        @param address_byte The address byte to be displayed.
        @param data_byte The data byte to be displayed.
        """
        start_bit = 1
        stop_bits = 11
        message = self.controller.get_last_message()
        encoded_message = self.controller.get_last_encoded_message()
        length = self.controller.get_last_message_length()

        bit_info = (
            f"DALI Frame Information:\n"
            f"Start Bit: {start_bit}\n"
            f"Address Byte: {address_byte:08b}\n"
            f"Data Byte: {data_byte:08b}\n"
            f"Stop Bits: {stop_bits}\n\n"
            f"Manchester Encoded: {encoded_message}\n"
            f"Message Length: {length} bits\n"
            f"Bit Rate: 1200 bits/sec"
        )
        self.bit_info_label.config(text=bit_info)

    def update_light_button(self, address, arc_power):
        """
        @brief Update the button appearance based on the light's brightness level.
        @param address Address of the light to update.
        @param arc_power The brightness level to set.
        """
        color_intensity = int((arc_power / MAX_BRIGHTNESS) * 255)
        color = f"#{color_intensity:02x}{color_intensity:02x}{color_intensity:02x}"  # Grayscale
        button = self.buttons[address]
        button.config(state=tk.NORMAL if arc_power > 0 else tk.DISABLED)
        button.config(bg=color)

    def update_display(self, message):
        """
        @brief Update the display with the given message.
        @param message The message to be displayed.
        """
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)

    def run(self):
        """
        @brief Run the Tkinter main application loop.
        """
        self.root.mainloop()
