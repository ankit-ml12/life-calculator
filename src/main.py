import tkinter as tk
from datetime import datetime
import time
import subprocess
import threading

START_DATE = datetime(1999, 2, 14)

# Store previous values for flip animation
prev_values_80 = {'years': 0, 'months': 0, 'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0}
prev_values_30 = {'years': 0, 'months': 0, 'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0}

# Inactivity tracking
last_activity_time = time.time()
is_window_on_top = False

def calculate_elapsed_time():
    """Calculate elapsed time from birth date - same for both timers"""
    now = datetime.now()
    elapsed = now - START_DATE
    
    total_seconds = int(elapsed.total_seconds())
    years, remaining_secs = divmod(total_seconds, 31536000)  # 365 days * 24 hours * 3600 seconds
    months, remaining_secs = divmod(remaining_secs, 2592000)  # 30 days * 24 hours * 3600 seconds
    days, remaining_secs = divmod(remaining_secs, 86400)     # 24 hours * 3600 seconds
    hours, remaining_secs = divmod(remaining_secs, 3600)     # 3600 seconds
    minutes, seconds = divmod(remaining_secs, 60)
    
    return years, months, days, hours, minutes, seconds

def calculate_remaining_time(target_years):
    """Calculate remaining time until target age"""
    now = datetime.now()
    target_date = datetime(START_DATE.year + target_years, START_DATE.month, START_DATE.day)
    
    if now >= target_date:
        return 0, 0, 0, 0, 0, 0
    
    remaining = target_date - now
    total_seconds = int(remaining.total_seconds())
    
    years, remaining_secs = divmod(total_seconds, 31536000)
    months, remaining_secs = divmod(remaining_secs, 2592000)
    days, remaining_secs = divmod(remaining_secs, 86400)
    hours, remaining_secs = divmod(remaining_secs, 3600)
    minutes, seconds = divmod(remaining_secs, 60)
    
    return years, months, days, hours, minutes, seconds

def get_idle_time():
    """Get system idle time in seconds"""
    try:
        result = subprocess.run(['xprintidle'], capture_output=True, text=True)
        if result.returncode == 0:
            return int(result.stdout.strip()) / 1000  # Convert ms to seconds
    except:
        pass
    return 0

def check_inactivity():
    """Check if system is inactive and bring window to top"""
    global is_window_on_top
    
    idle_time = get_idle_time()
    
    if idle_time > 120:  # 2 minutes = 120 seconds
        if not is_window_on_top:
            root.attributes('-topmost', True)
            root.lift()
            is_window_on_top = True
    else:
        if is_window_on_top:
            root.attributes('-topmost', False)
            is_window_on_top = False
    
    # Check again in 10 seconds
    root.after(10000, check_inactivity)

def flip_animation(number_label, unit_label, old_value, new_value):
    """Create flip animation effect when value changes"""
    if old_value != new_value:
        # Flash effect - brief color change
        original_bg = number_label.cget('bg')
        original_fg = number_label.cget('fg')
        
        # Flash white briefly for flip effect
        number_label.config(bg='#ffffff', fg='#000000')
        root.after(80, lambda: number_label.config(bg=original_bg, fg=original_fg))
        
        # Update with new value
        number_label.config(text=f"{new_value:02d}")
    else:
        # No change, just update normally
        number_label.config(text=f"{new_value:02d}")

def update_display():
    global prev_values_80, prev_values_30
    
    # Calculate elapsed time (same for both displays)
    elapsed_y, elapsed_m, elapsed_d, elapsed_h, elapsed_min, elapsed_s = calculate_elapsed_time()
    
    # Calculate remaining time for 80 years
    remain_80_y, remain_80_m, remain_80_d, remain_80_h, remain_80_min, remain_80_s = calculate_remaining_time(80)
    
    # Calculate remaining time for 30 years  
    remain_30_y, remain_30_m, remain_30_d, remain_30_h, remain_30_min, remain_30_s = calculate_remaining_time(30)
    
    # Top shows remaining time until 80, Bottom shows remaining time until 30
    current_80 = {'years': remain_80_y, 'months': remain_80_m, 'days': remain_80_d, 
                  'hours': remain_80_h, 'minutes': remain_80_min, 'seconds': remain_80_s}
    current_30 = {'years': remain_30_y, 'months': remain_30_m, 'days': remain_30_d, 
                  'hours': remain_30_h, 'minutes': remain_30_min, 'seconds': remain_30_s}
    
    # Update 80 year countdown blocks with flip animation
    top_blocks = [
        (top_year_num, top_year_unit, prev_values_80['years'], current_80['years']),
        (top_month_num, top_month_unit, prev_values_80['months'], current_80['months']), 
        (top_day_num, top_day_unit, prev_values_80['days'], current_80['days']),
        (top_hour_num, top_hour_unit, prev_values_80['hours'], current_80['hours']),
        (top_min_num, top_min_unit, prev_values_80['minutes'], current_80['minutes']),
        (top_sec_num, top_sec_unit, prev_values_80['seconds'], current_80['seconds'])
    ]
    
    for num_label, unit_label, old_val, new_val in top_blocks:
        flip_animation(num_label, unit_label, old_val, new_val)
    
    # Update 30 year countdown blocks with flip animation
    bottom_blocks = [
        (bottom_year_num, bottom_year_unit, prev_values_30['years'], current_30['years']),
        (bottom_month_num, bottom_month_unit, prev_values_30['months'], current_30['months']),
        (bottom_day_num, bottom_day_unit, prev_values_30['days'], current_30['days']), 
        (bottom_hour_num, bottom_hour_unit, prev_values_30['hours'], current_30['hours']),
        (bottom_min_num, bottom_min_unit, prev_values_30['minutes'], current_30['minutes']),
        (bottom_sec_num, bottom_sec_unit, prev_values_30['seconds'], current_30['seconds'])
    ]
    
    for num_label, unit_label, old_val, new_val in bottom_blocks:
        flip_animation(num_label, unit_label, old_val, new_val)
    
    # Store current values for next comparison
    prev_values_80 = current_80.copy()
    prev_values_30 = current_30.copy()
    
    # Schedule next update
    root.after(1000, update_display)

# Create main window
root = tk.Tk()
root.title("Life Calculator")
root.configure(bg='#000000')
root.geometry("900x500")
root.resizable(True, True)

# Create main container
main_frame = tk.Frame(root, bg='#000000')
main_frame.pack(expand=True, fill='both', padx=5, pady=5)

def create_flip_block(parent, fg_color):
    """Create a flip clock block with number and unit label"""
    container = tk.Frame(parent, bg='#000000')
    container.pack(side='left', padx=1, pady=1, fill='both', expand=True)
    
    # Large number display (flip clock style) - bigger size
    number_label = tk.Label(container, 
                           font=('Arial', 48, 'bold'), 
                           bg='#333333', 
                           fg=fg_color, 
                           relief='solid', 
                           bd=1,
                           width=4,
                           height=3,
                           text="00")
    number_label.pack(fill='both', expand=True)
    
    # Small unit label below
    unit_label = tk.Label(container,
                         font=('Arial', 9, 'normal'),
                         bg='#000000',
                         fg='#666666',
                         text="UNIT")
    unit_label.pack(pady=(1, 0))
    
    return number_label, unit_label

# TOP SECTION - 80 YEAR COUNTDOWN
top_frame = tk.Frame(main_frame, bg='#000000')
top_frame.pack(fill='both', expand=True, pady=(0, 5))

# Top blocks container - horizontal layout
top_blocks_frame = tk.Frame(top_frame, bg='#000000')
top_blocks_frame.pack(fill='both', expand=True)

# Create flip blocks for top row (80 year countdown) - WHITE text
top_year_num, top_year_unit = create_flip_block(top_blocks_frame, '#ffffff')
top_year_unit.config(text="YEARS")

top_month_num, top_month_unit = create_flip_block(top_blocks_frame, '#ffffff')
top_month_unit.config(text="MONTHS")

top_day_num, top_day_unit = create_flip_block(top_blocks_frame, '#ffffff')
top_day_unit.config(text="DAYS")

top_hour_num, top_hour_unit = create_flip_block(top_blocks_frame, '#ffffff')
top_hour_unit.config(text="HOURS")

top_min_num, top_min_unit = create_flip_block(top_blocks_frame, '#ffffff')
top_min_unit.config(text="MINUTES")

top_sec_num, top_sec_unit = create_flip_block(top_blocks_frame, '#ffffff')
top_sec_unit.config(text="SECONDS")

# SEPARATOR LINE
separator = tk.Frame(main_frame, bg='#333333', height=1)
separator.pack(fill='x', pady=5)

# BOTTOM SECTION - 30 YEAR COUNTDOWN
bottom_frame = tk.Frame(main_frame, bg='#000000')
bottom_frame.pack(fill='both', expand=True, pady=(5, 0))

# Bottom blocks container - horizontal layout
bottom_blocks_frame = tk.Frame(bottom_frame, bg='#000000')
bottom_blocks_frame.pack(fill='both', expand=True)

# Create flip blocks for bottom row (30 year countdown) - WHITE text
bottom_year_num, bottom_year_unit = create_flip_block(bottom_blocks_frame, '#ffffff')
bottom_year_unit.config(text="YEARS")

bottom_month_num, bottom_month_unit = create_flip_block(bottom_blocks_frame, '#ffffff')
bottom_month_unit.config(text="MONTHS")

bottom_day_num, bottom_day_unit = create_flip_block(bottom_blocks_frame, '#ffffff')
bottom_day_unit.config(text="DAYS")

bottom_hour_num, bottom_hour_unit = create_flip_block(bottom_blocks_frame, '#ffffff')
bottom_hour_unit.config(text="HOURS")

bottom_min_num, bottom_min_unit = create_flip_block(bottom_blocks_frame, '#ffffff')
bottom_min_unit.config(text="MINUTES")

bottom_sec_num, bottom_sec_unit = create_flip_block(bottom_blocks_frame, '#ffffff')
bottom_sec_unit.config(text="SECONDS")

# Start the timer
update_display()

# Start inactivity checking
check_inactivity()

# Start the GUI
root.mainloop()