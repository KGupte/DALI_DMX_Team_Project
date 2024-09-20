import array
import queue
import threading
import tkinter as tk
from ola.ClientWrapper import ClientWrapper

MAX_BRIGHTNESS = 255

"""
@brief Manages DMX output, visualization, and control.
"""

class DMXController:
	
	"""
    @brief Initializes the DMXController with a GUI and OLA client.
    @param root The root Tkinter window.
    @param assignment_registry The registry for device assignments.
    """
    def __init__(self, root, assignment_registry):
        self.universe = 1
        self.dmx_data = array.array('B', [0] * 512)
        self.channels_per_page = 16
        self.visual_current_page = 0
        self.wrapper = ClientWrapper()
        self.data_queue = queue.Queue()
        self.assignment_registry = assignment_registry
        self.create_visual_window(root)
        threading.Thread(target=self.run_ola_client, daemon=True).start()
        self.process_queue()

    """
    @brief Processes incoming DMX data from the queue.
    @return None
    """
    def process_queue(self):
        while not self.data_queue.empty():
            data = self.data_queue.get()
            for i in range(len(data)):
                self.dmx_data[i] = data[i]
                if i >= self.visual_current_page * self.channels_per_page and i < (self.visual_current_page + 1) * self.channels_per_page:
                    self.update_visual_display(i, data[i])
        self.visual_window.after(100, self.process_queue)

    """
    @brief Callback for DMX data sending status.
    @param status The status of the DMX send operation.
    @return None
    """
    def dmx_sent(self, status):
        if status.Succeeded():
            print("DMX data sent successfully.")
        else:
            print("DMX data failed to send.")

    """
    @brief Sends DMX data to the configured universe.
    @return None
    """
    def send_dmx(self):
        client = self.wrapper.Client()
        client.SendDmx(self.universe, self.dmx_data, self.dmx_sent)

    """
    @brief Updates the brightness of a specific DMX channel and sends DMX data.
    @param channel The DMX channel to update.
    @param value The brightness value to set.
    @return None
    """
    def update_brightness(self, channel, value):
        self.dmx_data[channel] = int(value)
        self.send_dmx()


    """
    @brief Creates a Tkinter window to visualize DMX data.
    @param root The root Tkinter window.
    @return None
    """
    def create_visual_window(self, root):
        self.visual_window = tk.Toplevel(root)
        self.visual_window.title("DMX Output Visualization")

        self.visual_labels = []
        for i in range(self.channels_per_page):
            frame = tk.Frame(self.visual_window, width=80, height=60, bg='lightgrey', relief='solid')
            frame.grid(row=i // 4, column=i % 4, padx=5, pady=5, sticky='nsew')

            label = tk.Label(frame, text="", bg='lightgrey', font=("Arial", 10), width=20, height=2)
            label.pack(expand=True, fill='both')

            self.visual_labels.append((frame, label))

        nav_frame = tk.Frame(self.visual_window)
        nav_frame.grid(row=4, column=0, columnspan=4, pady=10, sticky='ew')

        prev_button = tk.Button(nav_frame, text="Previous Page", command=lambda: self.update_visual_page(max(self.visual_current_page - 1, 0)))
        prev_button.pack(side="left", padx=10)

        next_button = tk.Button(nav_frame, text="Next Page", command=lambda: self.update_visual_page(min(self.visual_current_page + 1, (512 // self.channels_per_page) - 1)))
        next_button.pack(side="right", padx=10)

        self.visual_window.grid_rowconfigure(4, weight=1)
        self.visual_window.grid_columnconfigure(0, weight=1)

    """
    @brief Updates the visual display to the specified page of channels.
    @param page The page number to display.
    @return None
    """
    def update_visual_page(self, page):
        self.visual_current_page = page
        start_channel = self.visual_current_page * self.channels_per_page
        for i in range(self.channels_per_page):
            channel = start_channel + i
            if 0 <= channel < len(self.dmx_data):
                self.update_visual_display(channel, self.dmx_data[channel])
                self.visual_labels[i][1].config(text=f"Channel {channel + 1}")

    """
    @brief Updates a specific visual display element based on channel value.
    @param channel The DMX channel number.
    @param value The brightness value of the channel.
    @return None
    """
    def update_visual_display(self, channel, value):
        if channel not in self.assignment_registry['dali']:
            start_channel = self.visual_current_page * self.channels_per_page
            end_channel = start_channel + self.channels_per_page

            if start_channel <= channel < end_channel:
                relative_channel = channel % self.channels_per_page
                color_intensity = 255 - int((value / MAX_BRIGHTNESS) * 255)
                color = f'#{color_intensity:02x}{color_intensity:02x}{color_intensity:02x}'
                self.visual_labels[relative_channel][0].config(bg=color)
                self.visual_labels[relative_channel][1].config(bg=color)

    """
    @brief Callback for new data arriving in the DMX universe.
    @param data The new DMX data.
    @return None
    """
    def NewData(self, data):
        self.data_queue.put(list(data))


    """
    @brief Runs the OLA client to keep listening for DMX data.
    @return None
    """
    def run_ola_client(self):
        try:
            client = self.wrapper.Client()
            client.RegisterUniverse(self.universe, client.REGISTER, self.NewData)
            self.wrapper.Run()
        except Exception as e:
            print(f"Error in OLA client: {e}")
       
