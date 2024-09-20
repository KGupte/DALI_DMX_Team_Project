import array

"""
 * @file globals.py
 * @brief Contains global variables used throughout the DMX Controller application.
 * 
 * Defines and initializes global variables related to DMX data, universe, and page settings.
"""
dmx_data = array.array('B', [0] * 512)  # DMX output buffer
current_page = 0
visual_current_page = 0
universe = 1
channels_per_page = 16
