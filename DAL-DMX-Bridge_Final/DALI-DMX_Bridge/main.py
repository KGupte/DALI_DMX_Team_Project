import tkinter as tk
from lighting_control_app.dmx_controller import DMXController
from lighting_control_app.dali_controller import DALIController
from lighting_control_app.logging_config import configure_logging
from lighting_control_app.utils import manchester_encode, translate_command_to_brightness
from lighting_control_app.constants import DALI_OFF, DALI_UP, DALI_DOWN, DALI_MAX_LEVEL, DALI_MIN_LEVEL
from tkinter import messagebox

"""
@brief This class handles the lighting control application that integrates DMX and DALI controllers.
"""

class LightingControlApp:

    """
    @brief Initializes the LightingControlApp with DMX and DALI controllers and GUI components.
    @param root The root Tkinter window.
    """
    def __init__(self, root):
        self.root = root
        self.assignment_registry = {'dali': set(), 'dmx': set()}
        self.dmx_controller = DMXController(root, self.assignment_registry)
        self.dali_controller = DALIController(root, self.assignment_registry)
        self.create_main_controls()

        self.display_frame = tk.Frame(self.root)
        self.display_frame.pack(pady=10)
        self.text_area = tk.Text(self.display_frame, height=10, width=50)
        self.text_area.pack()

    """
    @brief Creates the main controls for the application GUI, including options and buttons.
    """
    def create_main_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=20)

        tk.Label(control_frame, text="Device Address:").grid(row=0, column=0)
        self.device_address_entry = tk.Entry(control_frame)
        self.device_address_entry.grid(row=0, column=1)

        tk.Label(control_frame, text="Command:").grid(row=1, column=0)
        self.command_var = tk.StringVar(value="Off")
        """
        Commands are mapped according to DALI
        """
        command_mapping = {
            "Off": DALI_OFF,
            "Up": DALI_UP,
            "Down": DALI_DOWN,
            "Full": DALI_MAX_LEVEL,
            "Low": DALI_MIN_LEVEL
        }
        command_options = list(command_mapping.keys())
        tk.OptionMenu(control_frame, self.command_var, *command_options).grid(row=1, column=1)

        tk.Label(control_frame, text="Assign as:").grid(row=2, column=0)
        self.assign_var = tk.StringVar(value="DMX")
        tk.OptionMenu(control_frame, self.assign_var, "DMX", "DALI").grid(row=2, column=1)

        tk.Button(control_frame, text="Assign and Send", command=lambda: self.assign_and_send_command(command_mapping)).grid(row=3, column=1, pady=10)

    """
    @brief Updates the text display area with the provided message.
    @param message The message to display.
    """

    def update_display(self, message):
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)

    """
    @brief Assigns a command to a DMX or DALI device and sends it.
    @param command_mapping Dictionary mapping command names to DALI command values.
    @return None
    """

    def assign_and_send_command(self, command_mapping):
        try:
            address = int(self.device_address_entry.get())
            command_str = self.command_var.get()
            command = command_mapping[command_str]
            assign_to = self.assign_var.get()

            if assign_to == "DALI":
                if address not in self.assignment_registry['dmx']:
                    if address not in self.assignment_registry['dali']:
                        self.dali_controller.create_light(address)
                    self.dali_controller.send_dali_command(address, command)

                    address_byte = address & 0x3F  
                    address_bits = format(address_byte, '06b')
                    command_bits = format(command, '08b')
                    start_bit = "1"
                    stop_bits = "01"

                    dali_sequence = f"{start_bit}{address_bits}{command_bits}{stop_bits}"
                    manchester_sequence = manchester_encode(int(dali_sequence, 2))

                    self.update_display(
                        f"DALI command to {address} ->\n"
                        f"Start bit: {start_bit}, Address bits: {address_bits}, "
                        f"Command bits: {command_bits}, Stop bits: {stop_bits}\n"
                        f"Manchester Encoded: {manchester_sequence}"
                    )

            elif assign_to == "DMX":
                if address not in self.assignment_registry['dali']:
                    if address not in self.assignment_registry['dmx']:
                        self.assignment_registry['dmx'].add(address)
                    start_channel = (address - 1) * 4

                    channel_range = f"Channels {start_channel} to {start_channel + 3}"
                    start_code = '00000000'
                    channel_data_bits = [format(self.dmx_controller.dmx_data[ch], '08b') for ch in range(start_channel, start_channel + 4)]
                    channel_data_str = " ".join(channel_data_bits)

                    dmx_sequence = f"Break, MAB: 1, Start Code: {start_code}, {channel_range}: {channel_data_str}, Stop Bits: 00"

                    self.update_display(
                        f"DMX command -> {dmx_sequence}\n"
                        f"Address encoded: {manchester_encode(address)}, Command encoded: {manchester_encode(command)}"
                    )
                    
                    for ch in range(start_channel, start_channel + 4):
                        brightness = translate_command_to_brightness(self.dmx_controller, command, ch)
                        self.dmx_controller.update_brightness(ch, brightness)
                else:
                    messagebox.showerror("Assignment Error", f"Address {address} is already assigned to a DALI light.")
        except ValueError:
            messagebox.showerror("Input Error", "Invalid input for address or command.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Lighting Control System")
    logging_configure = configure_logging()
    app = LightingControlApp(root)
    root.mainloop()
                
