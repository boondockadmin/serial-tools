import tkinter as tk
from tkinter import ttk
import serial
import threading
 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation

class SerialApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Serial Communication")
        root.geometry("800x600")  # Set the window size to your desired dimensions, e.g., 400x300 pixels

        # Serial connection
        self.ser = None

        # Dropdown for COM Port
        self.com_port_label = ttk.Label(root, text="COM Port:")
        self.com_port_label.pack()
        self.com_port = ttk.Combobox(root)
        self.com_port['values'] = ['COM1', 'COM2', 'COM3', 'COM4']  # Update with available COM ports
        self.com_port.pack()
 

        # Connect Button
        self.connect_button = ttk.Button(root, text="Connect", command=self.connect)
        self.connect_button.pack(side=tk.LEFT)

        # Disconnect Button
        self.disconnect_button = ttk.Button(root, text="Disconnect", command=self.disconnect)
        self.disconnect_button.pack(side=tk.RIGHT)


        # Text Display Area
        self.text_display = tk.Text(root, height=20, width=100)
        self.text_display.pack()

        # Text Input Box
        self.input_text = tk.Entry(root)
        self.input_text.pack()

        # Submit Button
        self.submit_button = ttk.Button(root, text="Send", command=self.send_data)
        self.submit_button.pack()

        
        # Plot Button
        self.plot_button = ttk.Button(root, text="Plot", command=self.start_plotting)
        self.plot_button.pack()

        # Matplotlib Figure
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack()

        # Variables for plotting
        self.x_data = []
        self.y_data = []

        self.plotting = False

    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.update_display("Disconnected from the serial port\n")

    def start_plotting(self):
        self.plotting = True
        self.ax.clear()
        self.ax.set_xlabel('X-axis')
        self.ax.set_ylabel('Y-axis')
        self.ani = animation.FuncAnimation(self.fig, self.update_plot, interval=1000)
        self.canvas.draw()

    def update_plot(self, frame):
        if self.plotting and self.ser and self.ser.is_open:
            line = self.ser.readline().decode().strip()
            if line:
                try:
                    x, y = map(float, line.split(','))
                    self.x_data.append(x)
                    self.y_data.append(y)
                    self.ax.clear()
                    self.ax.plot(self.x_data, self.y_data)
                    self.canvas.draw()
                except ValueError:
                    pass  # or handle the error


    def connect(self):
        try:
            self.ser = serial.Serial(self.com_port.get(), 115200)
            threading.Thread(target=self.read_data, daemon=True).start()
        except Exception as e:
            self.update_display(f"Error: {e}")
            self.text_display.see(tk.END)  # Scroll to the bottom
    def read_data(self):
        while True:
            if self.ser:
                try:
                    data = self.ser.readline().decode()
                    self.update_display(data)
                    self.text_display.see(tk.END)  # Scroll to the bottom
                except:
                    break

    def send_data(self):
        if self.ser and self.ser.is_open:
            data = self.input_text.get()
            # Appending carriage return and newline
            data_with_newline = data + '\r\n'
            self.ser.write(data_with_newline.encode())


    def update_display(self, data):
        self.text_display.insert(tk.END, data)
        self.text_display.see(tk.END)  # Scroll to the bottom

# Create the main window
root = tk.Tk()
app = SerialApp(root)
root.mainloop()
