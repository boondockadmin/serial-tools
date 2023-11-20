import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class SerialAppGUI:
    def __init__(self, root, connect_callback, disconnect_callback, send_data_callback, start_plotting_callback):
        self.root = root
        self.root.title("Serial Communication")
        root.geometry("800x600")

        # Dropdown for COM Port
        self.com_port_label = ttk.Label(root, text="COM Port:")
        self.com_port_label.pack()
        self.com_port = ttk.Combobox(root)
        self.com_port['values'] = ['COM1', 'COM2', 'COM3', 'COM4']  # Update with available COM ports
        self.com_port.pack()
 
        # Connect Button
        self.connect_button = ttk.Button(root, text="Connect", command=lambda: connect_callback(self.com_port.get()))
        self.connect_button.pack(side=tk.LEFT)

        # Disconnect Button
        self.disconnect_button = ttk.Button(root, text="Disconnect", command=disconnect_callback)
        self.disconnect_button.pack(side=tk.RIGHT)

        # Text Display Area
        self.text_display = tk.Text(root, height=20, width=100)
        self.text_display.pack()

        # Text Input Box
        self.input_text = tk.Entry(root)
        self.input_text.pack()

        # Submit Button
        self.submit_button = ttk.Button(root, text="Send", command=lambda: send_data_callback(self.input_text.get()))
        self.submit_button.pack()

        # Plot Button
        self.plot_button = ttk.Button(root, text="Plot", command=start_plotting_callback)
        self.plot_button.pack()

        # Matplotlib Figure
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack()

    def update_display(self, data):
        self.text_display.insert(tk.END, data)
        self.text_display.see(tk.END)  # Scroll to the bottom

    def get_ax(self):
        return self.ax
