import psutil
import tkinter as tk
import time
import threading
import ctypes
import pyautogui

# Constants for Windows API
GWL_STYLE = -16
GWL_EXSTYLE = -20
WS_MINIMIZEBOX = 0x00020000
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020

def get_taskbar_pixel_color():
    screen_width, screen_height = pyautogui.size()
    pixel_color = pyautogui.pixel(screen_width - 10, screen_height - 10)
    return '#%02x%02x%02x' % pixel_color

def get_taskbar_height():
    user32 = ctypes.windll.user32
    screen_height = user32.GetSystemMetrics(1)
    work_height = user32.GetSystemMetrics(17)
    return screen_height - work_height

def format_speed(bytes_per_sec):
    kbps = bytes_per_sec / 1024
    if kbps < 1000:
        return f"{kbps:.0f} Kbps"
    else:
        return f"{kbps / 1024:.1f} Mbps"

def update_speed():
    global prev_sent, prev_recv
    while True:
        time.sleep(1)
        counters = psutil.net_io_counters()
        new_sent = counters.bytes_sent
        new_recv = counters.bytes_recv

        upload = new_sent - prev_sent
        download = new_recv - prev_recv

        prev_sent, prev_recv = new_sent, new_recv

        upload_str = format_speed(upload)
        download_str = format_speed(download)

        speed_str = f"↓ {download_str}  ↑ {upload_str}"
        
        def update_ui():
            speed_label.config(text=speed_str)
            text_width = speed_label.winfo_reqwidth()
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            taskbar_height = get_taskbar_height()
            x = screen_width - text_width - 10
            y = screen_height - taskbar_height - window_height + 25
            root.geometry(f"{text_width}x{window_height}+{x}+{y}")
            # Update window position for mouse detection
            global window_x, window_y, window_width
            window_x = x
            window_y = y
            window_width = text_width
        
        root.after(0, update_ui)

def update_taskbar_color():
    new_bg = get_taskbar_pixel_color()
    speed_label.config(bg=new_bg)
    root.after(100, update_taskbar_color)

def check_mouse_position():
    global last_visible_state
    try:
        # Get current mouse position
        mouse_x, mouse_y = pyautogui.position()
        
        # Check if mouse is in window area
        in_window = (window_x <= mouse_x <= window_x + window_width and 
                     window_y <= mouse_y <= window_y + window_height)
        
        # New behavior: 
        # - Hide when mouse enters window
        # - Show when mouse is over window position and window is hidden
        if in_window:
            if last_visible_state:  # Was visible, now hide
                root.attributes("-alpha", 0.0)
                last_visible_state = False
        else:
            if not last_visible_state:  # Was hidden, now show
                root.attributes("-alpha", 0.85)
                last_visible_state = True
            
    except Exception:
        pass
    
    root.after(100, check_mouse_position)

# Initialize previous stats
prev_sent = psutil.net_io_counters().bytes_sent
prev_recv = psutil.net_io_counters().bytes_recv

# GUI setup
root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-alpha", 0.85)  # Start visible

# Get window handle
hwnd = ctypes.windll.user32.GetParent(root.winfo_id())

# Remove minimize capability
style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
style = style & ~WS_MINIMIZEBOX
ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)

# Make window a tool window and click-through
ex_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
ex_style |= WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOOLWINDOW
ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex_style)

# Window dimensions
window_height = 26
window_x, window_y, window_width = 0, 0, 180
last_visible_state = True  # Track if window is currently visible

# Initial bg color
bg_color = get_taskbar_pixel_color()
speed_label = tk.Label(root, text="Starting...", font=("Segoe UI", 9, "bold"),
                       fg="white", bg=bg_color, anchor="center")
speed_label.pack(fill=tk.BOTH, expand=True)

# Start updating speed in a background thread
threading.Thread(target=update_speed, daemon=True).start()

# Start updating taskbar color
root.after(100, update_taskbar_color)

# Start mouse position checking
root.after(100, check_mouse_position)

root.mainloop()