import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
import time

# Global Variabel
power_status = "Off"
swing_status = "Off"
fan_status = "Low"
mode_status = "Normal"
timer_status = "Off"
temperature_status = 23

# Fungsi dan Prosedur
def power():
    global power_status
    if power_status == "Off":
        power_status = "On"
    else:
        power_status = "Off"
        reset()  
    update_display()

def power_check():
    return power_status == "On"

def swing():
    global swing_status
    if power_check():
        swing_status = "On" if swing_status == "Off" else "Off"
        update_display()
    else:
        messagebox.showwarning("Warning", "Your power is off, cannot continue command.")

def fan():
    global fan_status
    if power_check():
        if fan_status == "Low":
            fan_status = "Medium"
        elif fan_status == "Medium":
            fan_status = "High"
        else:
            fan_status = "Low"
        update_display()
    else:
        messagebox.showwarning("Warning", "Your power is off, cannot continue command.")

def mode():
    global mode_status
    if power_check():
        modes = ["Normal", "Cool", "Dry", "Fan", "Turbo", "Quiet", "Sleep", "Auto"]
        current_index = modes.index(mode_status)
        mode_status = modes[(current_index + 1) % len(modes)]
        update_display()
    else:
        messagebox.showwarning("Warning", "Your power is off, cannot continue command.")

def timer_thread(duration_minutes):
    global power_status, timer_status
    time.sleep(duration_minutes * 60)
    reset()
    update_display()

def reset():
    global power_status, swing_status, fan_status, mode_status, timer_status, temperature_status
    power_status = "Off"
    swing_status = "Off"
    fan_status = "Low"
    mode_status = "Normal"
    timer_status = "Off"
    temperature_status = 23

def timer():
    global timer_status
    if power_check():
        try:
            duration_minutes = int(timer_entry.get())
            timer_entry.delete(0, tk.END)
            timer_status = f"{duration_minutes} min"
            threading.Thread(target=timer_thread, args=(duration_minutes,), daemon=True).start()
            update_display()
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid number for the timer.")
    else:
        messagebox.showwarning("Warning", "Your power is off, cannot continue command.")

def temperature_up():
    global temperature_status
    if power_check():
        if temperature_status < 32:
            temperature_status += 1
        update_display()
    else:
        messagebox.showwarning("Warning", "Your power is off, cannot continue command.")

def temperature_down():
    global temperature_status
    if power_check():
        if temperature_status > 16:
            temperature_status -= 1
        update_display()
    else:
        messagebox.showwarning("Warning", "Your power is off, cannot continue command.")

def update_display():
    if power_status == "Off":
        display_label.config(image=power_image, text="")
        control_frame.pack_forget()
    else:
        display_label.config(image="", text=f"Power: {power_status}\n"
                                            f"Temperature: {temperature_status} °C\n"
                                            f"Swing: {swing_status}\n"
                                            f"Fan: {fan_status}\n"
                                            f"Mode: {mode_status}\n"
                                            f"Timer: {timer_status}",
                             font=("Helvetica Neue", 14), justify="left", fg="black", bg="lightgrey")
        control_frame.pack(pady=10)

# Setup GUI
root = tk.Tk()
root.title("Remote AC")
root.configure(bg="#2E2E2E")  # Dark background

window_width = 400
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
offset_x = (screen_width - window_width) // 2
offset_y = (screen_height - window_height) // 2 - 50  
root.geometry(f"{window_width}x{window_height}+{offset_x}+{offset_y}")

power_image_file = "Power.png"
try:
    power_image = ImageTk.PhotoImage(Image.open(power_image_file).resize((150, 150)))
except FileNotFoundError:
    power_image = None

display_label = tk.Label(root, bg="lightgrey")
display_label.pack(pady=20)
control_frame = tk.Frame(root, bg="lightgrey")
power_button = tk.Button(root, text="Power", command=power, bg="red", fg="white", font=("Helvetica Neue", 12))
power_button.pack(pady=5)

# Temperature Control Fram
temp_frame = tk.Frame(control_frame, bg="lightgrey")
temp_frame.pack(pady=5)
temp_up_button = tk.Button(temp_frame, text="Temperature Up", command=temperature_up, bg="white", fg="black", font=("Helvetica Neue", 12))
temp_up_button.pack(side="left", padx=5)
temp_down_button = tk.Button(temp_frame, text="Temperature Down", command=temperature_down, bg="white", fg="black", font=("Helvetica Neue", 12))
temp_down_button.pack(side="left", padx=5)

# Swing Button
swing_button = tk.Button(control_frame, text="Swing", command=swing, bg="white", fg="black", font=("Helvetica Neue", 12))
swing_button.pack(pady=5)

# Mode and Fan Control Frame
mode_fan_frame = tk.Frame(control_frame, bg="lightgrey")
mode_fan_frame.pack(pady=5)
fan_button = tk.Button(mode_fan_frame, text="Fan Speed", command=fan, bg="white", fg="black", font=("Helvetica Neue", 12))
fan_button.pack(side="left", padx=5)
mode_button = tk.Button(mode_fan_frame, text="Change Mode", command=mode, bg="white", fg="black", font=("Helvetica Neue", 12))
mode_button.pack(side="left", padx=5)

# Timer Control
timer_label = tk.Label(control_frame, text="Set Timer (minutes):", bg="lightgrey", font=("Helvetica Neue", 12))
timer_label.pack(pady=5)
timer_entry = tk.Entry(control_frame, font=("Helvetica Neue", 12))
timer_entry.pack(pady=5)
timer_button = tk.Button(control_frame, text="Set Timer", command=timer, bg="white", fg="black", font=("Helvetica Neue", 12))
timer_button.pack(pady=5)

# Update Display
update_display()

# Start the GUI event loop
root.mainloop()