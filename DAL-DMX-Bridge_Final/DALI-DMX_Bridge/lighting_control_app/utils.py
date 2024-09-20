from .constants import DALI_OFF, DALI_UP, DALI_DOWN, DALI_MAX_LEVEL, DALI_MIN_LEVEL

"""
@brief Encodes a byte using Manchester encoding.
@param data_value The data value to encode.
@return The Manchester encoded string representing the data value.
"""
def manchester_encode(data_value):
    bit_string = format(data_value, '08b')
    manchester_encoded = []
    for bit in bit_string:
        if bit == '1':
            manchester_encoded.append('10')
        else:
            manchester_encoded.append('01')
    return ''.join(manchester_encoded)

"""
@brief Translates a DALI command to a DMX brightness value for a specific channel.
@param dmx_controller The DMX controller instance.
@param command The DALI command to translate.
@param channel The DMX channel affected.
@return The calculated brightness value.
"""
def translate_command_to_brightness(dmx_controller, command, channel):
    current_brightness = dmx_controller.dmx_data[channel]
    if command == DALI_OFF:
        return 0
    elif command == DALI_UP:
        return min(255, current_brightness + 25)
    elif command == DALI_DOWN:
        return max(0, current_brightness - 25)
    elif command == DALI_MAX_LEVEL:
        return 255
    elif command == DALI_MIN_LEVEL:
        return 26
    return current_brightness
