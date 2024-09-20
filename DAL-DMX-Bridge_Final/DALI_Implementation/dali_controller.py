from dali_light import DALILight
from dali_utils import manchester_encode

# DALI Command Constants
DALI_OFF = 0
DALI_UP = 1
DALI_DOWN = 2
DALI_MAX_LEVEL = 5
DALI_MIN_LEVEL = 6
DALI_RESET = 32
DALI_DTR_ACTUAL_LEVEL = 33
DALI_TERMINATE = 161
DALI_STORE_TO_DTR = 163

# Maximum brightness limit
MAX_BRIGHTNESS = 255

# Number of groups and scenes per light (ECG)
NUM_GROUPS = 16
NUM_SCENES = 16

class DALIController:
    """
    @brief This class manages the control of DALI lights and groups.
    """

    def __init__(self):
        """
        @brief Initialize the DALI controller with lights and groups.
        """
        self.lights = {}
        self.groups = {i: [] for i in range(NUM_GROUPS)}
        self.last_message = ""
        self.last_encoded_message = ""
        self.last_length = 0

    def create_light(self, address):
        """
        @brief Create a new DALI light with the given address.
        @param address Address of the light to be created.
        """
        if address in self.lights:
            print(f"Light {address} already exists.")
        else:
            self.lights[address] = DALILight(address)
            print(f"Light {address} created.")

    def assign_light_to_group(self, address, group_id):
        """
        @brief Assign a light to a specific group.
        @param address The address of the light.
        @param group_id The group ID to assign the light to.
        """
        if address in self.lights and 0 <= group_id < NUM_GROUPS:
            light = self.lights[address]
            light.add_to_group(group_id)
            if address not in self.groups[group_id]:
                self.groups[group_id].append(address)
            print(f"Assigned light {address} to group {group_id}.")
        elif address in self.lights and group_id == -1:
            light = self.lights[address]
            for group in self.groups:
                if address in self.groups[group]:
                    self.groups[group].remove(address)
            light.remove_from_all_groups()
            print(f"Light {address} removed from all groups.")
        else:
            print(f"Light {address} or group {group_id} is invalid.")

    def send_command_to_group(self, group_id, command):
        """
        @brief Send a command to all lights in a group.
        @param group_id The ID of the group.
        @param command The command to be sent to the group.
        """
        if group_id in self.groups and self.groups[group_id]:
            for address in self.groups[group_id]:
                light = self.lights.get(address)
                if light:
                    self.process_command(light, command)
            print(f"Command {command} sent to group {group_id}.")
        else:
            print(f"Group {group_id} not found or no lights in the group.")

    def send_command(self, address_byte, data_byte):
        """
        @brief Send a command to a DALI device or group.
        @param address_byte Address byte to send.
        @param data_byte Data byte to send.
        """
        self.last_message = self._encode_message(address_byte, data_byte)
        self.last_encoded_message = manchester_encode(address_byte) + manchester_encode(data_byte)
        self.last_length = len(self.last_encoded_message)

        if (address_byte >> 1) == 0x3F:  # Broadcast Address
            print("Command sent to all DALI lights (Broadcast).")
            for light in self.lights.values():
                self.process_command(light, data_byte)
        elif 0x80 <= address_byte < 0xA0:  # Group Address Range
            group = (address_byte - 0x80) >> 1
            self.send_command_to_group(group, data_byte)
        else:
            active_light = self.lights.get(address_byte >> 1)
            if active_light:
                self.process_command(active_light, data_byte)
            else:
                print("No active light found for address.")

    def send_scene_command(self, scene_num):
        """
        @brief Send a scene command to all lights and set the brightness levels.
        @param scene_num The scene number.
        """
        print(f"Scene {scene_num} command sent.")
        for light in self.lights.values():
            brightness = light.get_scene_brightness(scene_num)
            light.set_arc_power(brightness)
            print(f"Light {light.address} set to brightness {brightness} for scene {scene_num}.")

    def _encode_message(self, address_byte, data_byte):
        """
        @brief Encode the DALI message.
        @param address_byte The address byte.
        @param data_byte The data byte.
        @return Encoded message as string.
        """
        return f"Addr: {address_byte >> 1}, Cmd: {data_byte}"

    def process_command(self, light, command):
        """
        @brief Process a command for a specific light.
        @param light The DALI light object.
        @param command The command to be processed.
        """
        if command == DALI_OFF:
            light.set_arc_power(0)
        elif command == DALI_UP:
            light.set_arc_power(min(light.arc_power_level + 10, MAX_BRIGHTNESS))
        elif command == DALI_DOWN:
            light.set_arc_power(max(light.arc_power_level - 10, 0))
        elif command == DALI_MAX_LEVEL:
            light.set_arc_power(MAX_BRIGHTNESS)
        elif command == DALI_MIN_LEVEL:
            light.set_arc_power(0)
        elif command == DALI_RESET:
            light.set_arc_power(0)
        elif command == DALI_DTR_ACTUAL_LEVEL:
            print(f"Light {light.address}: Current power level is {light.arc_power_level}.")
        elif command == DALI_TERMINATE:
            print("Terminating all DALI lights.")
            for l in self.lights.values():
                l.set_arc_power(0)
        elif command == DALI_STORE_TO_DTR:
            print(f"Storing data to DTR for Light {light.address}.")
        else:
            print("Command not recognized or not implemented.")

    def get_last_message(self):
        """
        @brief Return the last transmitted message.
        @return The last message as a string.
        """
        return self.last_message

    def get_last_encoded_message(self):
        """
        @brief Return the last Manchester encoded message.
        @return The encoded message as a string.
        """
        return self.last_encoded_message

    def get_last_message_length(self):
        """
        @brief Return the length of the last encoded message.
        @return Length of the message.
        """
        return self.last_length
