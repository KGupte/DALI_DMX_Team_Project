# Number of groups and scenes per light (ECG)
NUM_SCENES = 16

class DALILight:
    """
    @brief This class represents a DALI light, allowing control over its brightness and scenes.
    """

    def __init__(self, address):
        """
        @brief Initialize a new DALI light.
        @param address The address of the light.
        """
        self.address = address
        self.arc_power_level = 0
        self.scenes = [0] * NUM_SCENES
        self.groups = set()

    def set_arc_power(self, level):
        """
        @brief Set the brightness level of the light.
        @param level Brightness level (0-255).
        """
        self.arc_power_level = level
        print(f"Light {self.address}: Arc power set to {level}.")

    def add_to_group(self, group_id):
        """
        @brief Add the light to a specific group.
        @param group_id Group ID to add the light to.
        """
        self.groups.add(group_id)
        print(f"Light {self.address} added to group {group_id}.")

    def remove_from_all_groups(self):
        """
        @brief Remove the light from all assigned groups.
        """
        self.groups.clear()
        print(f"Light {self.address} removed from all groups.")

    def set_scene_brightness(self, scene_num, brightness):
        """
        @brief Set the brightness level for a specific scene.
        @param scene_num The scene number.
        @param brightness The brightness level (0-255).
        """
        if 0 <= scene_num < NUM_SCENES:
            self.scenes[scene_num] = brightness
            print(f"Scene {scene_num} for light {self.address} set to brightness {brightness}.")
        else:
            print(f"Invalid scene number {scene_num} for light {self.address}.")

    def get_scene_brightness(self, scene_num):
        """
        @brief Get the brightness level for a specific scene.
        @param scene_num The scene number.
        @return The brightness level for the scene.
        """
        if 0 <= scene_num < NUM_SCENES:
            return self.scenes[scene_num]
        else:
            print(f"Invalid scene number {scene_num}.")
            return 0
