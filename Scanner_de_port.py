import tkinter as tk
from tkinter import ttk
from datetime import datetime
import threading
import socket

def get_target():
    hostname = target_entry.get()
    target = socket.gethostbyname(hostname)
    result_label.config(text=f'Scan Target  > {target}')
    return target

def scan_port(target, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        test = s.connect_ex((target, port))
        if test == 0:
            result_text.insert(tk.END, f'Port {port} is [open]\n')

def port_scanner():
    try:
        target = get_target()
        port_list = list(range(1, 1024))
        thread_list = []

        start_time = datetime.now()

        for port in port_list:
            scan = threading.Thread(target=scan_port, args=(target, port))
            thread_list.append(scan)
            scan.daemon = True
            scan.start()

        for scan in thread_list:
            scan.join()
    except:
        result_text.insert(tk.END, "Something went wrong !\n")
    else:
        end_time = datetime.now()
        result_text.insert(tk.END, f"Scanning completed in {end_time - start_time}\n")

def start_scan():
    result_text.delete(1.0, tk.END)
    threading.Thread(target=port_scanner).start()

# Create the main window
root = tk.Tk()
root.title("Port Scanner")

# Create and place widgets
target_label = tk.Label(root, text="Enter target hostname (or IP address):")
target_label.pack(pady=10)

target_entry = tk.Entry(root)
target_entry.pack()

get_target_button = tk.Button(root, text="Get Target", command=get_target)
get_target_button.pack(pady=5)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

scan_button = tk.Button(root, text="Start Scan", command=start_scan)
scan_button.pack(pady=5)

result_text = tk.Text(root, height=10, width=40)
result_text.pack(pady=10)

# Start the GUI event loop
root.mainloop()
