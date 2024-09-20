from .constants import DALI_OFF, DALI_UP, DALI_DOWN, DALI_MAX_LEVEL, DALI_MIN_LEVEL


MAX_BRIGHTNESS = 255
    
"""
@brief Represents a DALI light, storing its address and brightness state.
"""

class DALILight:

    """
    @brief Initializes a DALI light with a given address.
    @param address The address of the DALI light.
    """
    def __init__(self, address):
        self.address = address
        self.arc_power_level = 0

    """
    @brief Processes a DALI command to adjust the brightness level.
    @param command The command to process.
    @return None
    """
    def process_command(self, command):
        if command == DALI_OFF:
            self.arc_power_level = 0
        elif command == DALI_UP:
            self.arc_power_level = min(self.arc_power_level + 10, MAX_BRIGHTNESS)
        elif command == DALI_DOWN:
            self.arc_power_level = max(self.arc_power_level - 10, 0)
        elif command == DALI_MAX_LEVEL:
            self.arc_power_level = MAX_BRIGHTNESS
        elif command == DALI_MIN_LEVEL:
            self.arc_power_level = 0
        print(f"Light {self.address}: Power level set to {self.arc_power_level}.")
