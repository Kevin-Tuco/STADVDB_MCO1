import tkinter as tk
from tkinter import ttk
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import pandas as pd

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
    report_window = tk.Toplevel(main_window)
    report_window.title("Hospital Rankings Report Generator")

    # Dropdown for selecting type
    type_options = ["City", "Province", "RegionName", "none"]
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

        if selected_type == "none":
            # If "none" is selected, set value_dropdown to only have "none" as an option
            value_dropdown['values'] = ["none"]
            value_dropdown.set("none")
        else:
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

        # Build the SQL query based on the selected report type
        if selected_type == "none":
            sql_query = """
                SELECT c.hospitalname,
                       COUNT(a.apptid) AS CompleteAppointmentsCount
                FROM clinics c
                LEFT JOIN appointments a ON c.clinicid = a.clinicid
                WHERE c.hospitalname IS NOT NULL
                  AND a.status = 'Complete'
                GROUP BY c.clinicid, c.hospitalname
                ORDER BY CompleteAppointmentsCount DESC;
            """
        else:
            # Replace placeholders in the SQL query based on the selected type and value
            sql_query = f"""
                SELECT c.hospitalname,
                       COUNT(a.apptid) AS CompleteAppointmentsCount
                FROM clinics c
                LEFT JOIN appointments a ON c.clinicid = a.clinicid
                WHERE c.{selected_type} = '{selected_value}'
                  AND c.hospitalname IS NOT NULL
                  AND a.status = 'Complete'
                GROUP BY c.hospitalname
                ORDER BY CompleteAppointmentsCount DESC;
            """

        # Measure the time elapsed during report generation
        start_time = time.time()

        # Execute the query
        cursor.execute(sql_query)

        # Fetch all the results
        results = cursor.fetchall()

        # Create a DataFrame for displaying the table
        columns = ["Hospital Name", "Complete Appointments Count"]
        df = pd.DataFrame(results, columns=columns)

        # Create a table in the tkinter window
        table = ttk.Treeview(report_window, columns=columns, show="headings")

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=150)  # Adjust the width as needed

        for row in df.itertuples(index=False):
            table.insert("", "end", values=row)

        table.grid(row=4, column=0, columnspan=2)

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
