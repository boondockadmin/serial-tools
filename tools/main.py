import tkinter as tk
from GUI import SerialAppGUI
from SerialComm import SerialComm
from Plotting import Plotting

def main():
    root = tk.Tk()
    app = SerialAppGUI(root, connect, disconnect, send_data, start_plotting)
    serial_comm = SerialComm(display_callback)
    plotting = Plotting(app.get_ax())

    def connect(port):
        serial_comm.connect(port)

    def disconnect():
        serial_comm.disconnect()

    def send_data(data):
        serial_comm.send_data(data)

    def start_plotting():
        plotting.start_plotting()

    def display_callback(data):
        app.update_display(data)
        # Assuming data is in 'x,y' format
        try:
            x, y = map(float, data.split(','))
            plotting.add_data(x, y)
        except ValueError:
            pass  # Handle non-numeric data or incorrect format

    root.mainloop()

if __name__ == "__main__":
    main()
