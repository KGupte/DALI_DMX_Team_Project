"""
 * @file dmx_handler.py
 * @brief Handles DMX data processing and communication with the OLA client.
 * 
 * This module manages sending DMX data to the specified universe, processing
 * incoming DMX data, and running the OLA client in a separate thread.
"""
import queue
from ola.ClientWrapper import ClientWrapper
from globals import dmx_data, universe, current_page, channels_per_page

wrapper = ClientWrapper()
data_queue = queue.Queue()

def send_dmx():
    """
     * @brief Send the current DMX data to the specified universe.
     * 
     * Creates a new OLA client instance and sends the DMX data buffer to the
     * specified universe. Calls the dmx_sent callback to handle the status of
     * the DMX data sending operation.
    """
    client = wrapper.Client()
    client.SendDmx(universe, dmx_data, dmx_sent)

def dmx_sent(status):
    """
     * @brief Callback function to handle the result of sending DMX data.
     * 
     * Prints a success or failure message based on the status of the DMX data
     * sending operation.
     * 
     * @param status The status object returned from the OLA client.
    """
    if status.Succeeded():
        print("DMX data sent successfully.")
    else:
        print("DMX data failed to send.")

def NewData(data):
    """
     * @brief Handle new DMX data received from the OLA client.
     * 
     * Puts the received DMX data into a queue for further processing.
     * 
     * @param data The DMX data received from the OLA client.
    """
    data_queue.put(list(data))  # Put the data in the queue

def process_queue(root):
    """
     * @brief Process DMX data from the queue and update the visual display.
     * 
     * Retrieves data from the queue and updates the DMX data buffer and visual
     * display for the channels on the current page.
     * 
     * @param root The Tkinter root window for scheduling further processing.
    """
    while not data_queue.empty():
        data = data_queue.get()
        for i in range(len(data)):
            dmx_data[i] = data[i]
            if i >= current_page * channels_per_page and i < (current_page + 1) * channels_per_page:
                # Import inside function to avoid circular import
                from shared import update_visual_display
                update_visual_display(i, data[i])
    root.after(100, process_queue, root)  # Check the queue again after 100ms

def run_ola_client():
    """
     * @brief Run the OLA client in a separate thread.
     * 
     * Registers the DMX universe with the OLA client and starts the OLA event
     * loop to receive DMX data. Handles exceptions during client setup.
    """
    try:
        client = wrapper.Client()
        client.RegisterUniverse(universe, client.REGISTER, NewData)
        wrapper.Run()  # This starts the OLA event loop
    except Exception as e:
        print(f"Error in OLA client: {e}")
