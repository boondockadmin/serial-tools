import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import serial.tools.list_ports
import subprocess
import requests

def download_file(url, local_filename):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return local_filename
    except Exception as e:
        print(f"Failed to download file: {e}")
        return None


def flash_firmware(foldername):
    selected_port = port_var.get()
    selected_firmware = foldername + "/firmware.bin"
    selected_partition = foldername + "/partitions.bin"
    selected_bootloader = foldername + "/bootloader.bin"
   
    if not selected_port or not selected_firmware:
        return
   
    #esptool.py --chip esp32 --port %COMPORT% --baud 921600 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 40m --flash_size detect 0x1000 bootloader.bin 0x10000 firmware.bin 0x8000 partitions.bin

    command = [
        "esptool",
        "--chip", "esp32",
        "--port", selected_port,
        "--before", "default_reset",
        "--after", "hard_reset",
        "write_flash", "-z","--flash_mode", "dio", "--flash_freq", "40m", "--flash_size", "detect", "0x1000",
        selected_bootloader, "0x10000", selected_firmware, "0x8000", selected_partition
       
    ]
   
    try:
        subprocess.run(command, check=True)
        result_label.config(text="Flashing successful.")
    except subprocess.CalledProcessError:
        result_label.config(text="Flashing failed.")

# Initialize the GUI window
root = tk.Tk()
root.title("Boondock Flash firmware tool")
root.geometry("400x300")  # Set the window size to your desired dimensions, e.g., 400x300 pixels

# Help
help1_label = ttk.Label(root, text="Please install Python libraries with commands")
help1_label.pack()

help2_label = ttk.Label(root, text="pip install esptool")
help2_label.pack()

help3_label = ttk.Label(root, text="pip install requests")
help3_label.pack()

help4_label = ttk.Label(root, text="pip install pyserial")
help4_label.pack()

help5_label = ttk.Label(root, text="pip install tk")
help5_label.pack()

help6_label = ttk.Label(root, text="====================================")
help6_label.pack()


# Create a dropdown for serial ports
port_var = tk.StringVar()
port_label = ttk.Label(root, text="Select Serial Port:")
port_label.pack()

available_ports = [port.device for port in serial.tools.list_ports.comports()]
port_menu = ttk.OptionMenu(root, port_var, None, *available_ports)
port_menu.pack()


# Create a button to start flashing
flash_daily = ttk.Button(root, text="Flash Nightly Build", command=lambda: flash_firmware("daily"))
flash_daily.pack()

flash_stable = ttk.Button(root, text="Flash Stable Build", command=lambda: flash_firmware("stable"))
flash_stable.pack()

flash_debug = ttk.Button(root, text="Flash Debug Build", command=lambda: flash_firmware("debug"))
flash_debug.pack()


# Create a label to show the result
result_label = ttk.Label(root, text="")
result_label.pack()



download_file("https://www.boondockecho.com/firmware/daily/partitions.bin", "daily/partitions.bin")
download_file("https://www.boondockecho.com/firmware/daily/firmware.bin", "daily/firmware.bin")
download_file("https://www.boondockecho.com/firmware/daily/bootloader.bin", "daily/bootloader.bin")

download_file("https://www.boondockecho.com/firmware/stable/partitions.bin", "stable/partitions.bin")
download_file("https://www.boondockecho.com/firmware/stable/firmware.bin", "stable/firmware.bin")
download_file("https://www.boondockecho.com/firmware/stable/bootloader.bin", "stable/bootloader.bin")

download_file("https://www.boondockecho.com/firmware/debug/partitions.bin", "debug/partitions.bin")
download_file("https://www.boondockecho.com/firmware/debug/firmware.bin", "debug/firmware.bin")
download_file("https://www.boondockecho.com/firmware/debug/bootloader.bin", "debug/bootloader.bin")

# Run the GUI event loop
root.mainloop()
