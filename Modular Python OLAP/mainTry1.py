import tkinter as tk
from tkinter import ttk
import report_type_1
import report_type_2
import report_type_3
import report_type_4
import report_type_5

def show_report_type_1():
    report_type_1.generate_report(window)  # Update the function name

def show_report_type_2():
    report_type_2.generate_report(window)
    
def show_report_type_3():
    report_type_3.generate_report(window)
    
def show_report_type_4():
    report_type_4.generate_report(window)
    
def show_report_type_5():
    report_type_5.generate_report(window)

# Create the main tkinter window
window = tk.Tk()
window.title("Report Generator")

# Button to show Report Type 1
report_type_1_button = tk.Button(window, text="Popularity by Space", command=show_report_type_1)
report_type_1_button.grid(row=0, column=0)

# Button to show Report Type 2
report_type_2_button = tk.Button(window, text="Popularity by Time", command=show_report_type_2)
report_type_2_button.grid(row=1, column=0)

# Button to show Report Type 3
report_type_2_button = tk.Button(window, text="Virtual Use by Time", command=show_report_type_3)
report_type_2_button.grid(row=2, column=0)

# Button to show Report Type 4
report_type_2_button = tk.Button(window, text="Application Type by Time", command=show_report_type_4)
report_type_2_button.grid(row=3, column=0)

# Button to show Report Type 5
report_type_2_button = tk.Button(window, text="Hospital Rankings Based on Completed Appointments by Space", command=show_report_type_5)
report_type_2_button.grid(row=4, column=0)

# Start the tkinter event loop
window.mainloop()
