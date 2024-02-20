import tkinter as tk
from tkinter import ttk
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

def generate_report(main_window):
    # Connect to MySQL database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="EDCft0118!",
        database="seriousmd_appointment"
    )
    cursor = connection.cursor()

    # Create a new window for report generation
    report_window = tk.Toplevel(main_window)  # Use Toplevel instead of Tk()
    report_window.title("Popularity by space Report Generator")

    # Dropdown for selecting type
    type_options = ["City", "Province", "RegionName"]
    type_dropdown = ttk.Combobox(report_window, values=type_options)
    type_dropdown.grid(row=0, column=0)
    type_dropdown.set("Select Type")  # Default value

    # Dropdown for selecting value
    value_dropdown = ttk.Combobox(report_window)
    value_dropdown.grid(row=0, column=1)
    value_dropdown.set("Select Value")  # Default value

    # Label for displaying time elapsed
    elapsed_label = tk.Label(report_window, text="")
    elapsed_label.grid(row=2, column=0, columnspan=2)

    def load_value_options(event):
        # Get the selected type from the first dropdown
        selected_type = type_dropdown.get()

        # Execute SQL query to get distinct values for the selected type
        sql_query = f"SELECT DISTINCT {selected_type} FROM clinics"
        cursor.execute(sql_query)

        # Fetch all the distinct values
        distinct_values = cursor.fetchall()

        # Update the options in the second dropdown
        value_options = [value[0] for value in distinct_values]
        value_dropdown['values'] = value_options

    def generate_report():
        # Get values from the dropdowns
        selected_type = type_dropdown.get()
        selected_value = value_dropdown.get()

        # Replace placeholders in the SQL query based on the selected report type
        sql_query = f"""
            SELECT c.RegionName,
                   COUNT(CASE WHEN a.status = 'Complete' THEN 1 END) AS Complete_Count,
                   COUNT(CASE WHEN a.status = 'Queued' THEN 1 END) AS Queued_Count,
                   COUNT(CASE WHEN a.status = 'NoShow' THEN 1 END) AS NoShow_Count,
                   COUNT(CASE WHEN a.status = 'Serving' THEN 1 END) AS Serving_Count,
                   COUNT(CASE WHEN a.status = 'Cancel' THEN 1 END) AS Cancel_Count
            FROM appointments a
            JOIN clinics c ON a.clinicid = c.clinicid
            WHERE c.{selected_type} = '{selected_value}'
            GROUP BY c.RegionName;
        """

        # Measure the time elapsed during report generation
        start_time = time.time()

        # Execute the query
        cursor.execute(sql_query)

        # Fetch all the results
        results = cursor.fetchall()

        # Extract data for plotting
        labels = ['Complete', 'Queued', 'NoShow', 'Serving', 'Cancel']
        data = [results[0][i + 1] for i in range(5)]  # Skip the first column (RegionName)

        # Plot the bar chart
        fig, ax = plt.subplots()
        ax.bar(labels, data, color=['green', 'blue', 'orange', 'red', 'purple'])
        ax.set_xlabel('Appointment Status')
        ax.set_ylabel('Count')
        ax.set_title(f'Appointment Status Distribution for {selected_value}')

        # Display the bar chart in the tkinter window
        canvas = FigureCanvasTkAgg(fig, master=report_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=4, column=0, columnspan=3)

        # Calculate and display the time elapsed
        elapsed_time = time.time() - start_time
        elapsed_label.config(text=f"Time Elapsed: {elapsed_time:.2f} seconds")

    # Binding the event to dynamically load values based on the selected type
    type_dropdown.bind("<<ComboboxSelected>>", load_value_options)

    # Button to trigger report generation
    generate_button = tk.Button(report_window, text="Generate", command=generate_report)
    generate_button.grid(row=1, column=0, columnspan=2)

    # Start the tkinter event loop for the report window
    report_window.mainloop()

    # Close the database connection
    cursor.close()
    connection.close()
