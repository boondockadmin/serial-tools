import serial
import threading

class SerialComm:
    def __init__(self, display_callback):
        self.ser = None
        self.display_callback = display_callback

    def connect(self, port):
        try:
            self.ser = serial.Serial(port, 115200)
            threading.Thread(target=self.read_data, daemon=True).start()
        except Exception as e:
            self.display_callback(f"Error: {e}")

    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.display_callback("Disconnected from the serial port\n")

    def send_data(self, data):
        if self.ser and self.ser.is_open:
            data_with_newline = data + '\r\n'
            self.ser.write(data_with_newline.encode())

    def read_data(self):
        while True:
            if self.ser:
                try:
                    data = self.ser.readline().decode()
                    self.display_callback(data)
                except:
                    break
