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
    report_window = tk.Toplevel(main_window)
    report_window.title("Virtual vs Non-Virtual Report Generator")

    # Dropdown for selecting year
    year_options = []  # Dynamically load options using SQL statement
    year_dropdown = ttk.Combobox(report_window, values=year_options)
    year_dropdown.grid(row=0, column=0)
    year_dropdown.set("Select Year")  # Default value

    # Dropdown for selecting month
    month_options = ["all", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    month_dropdown = ttk.Combobox(report_window, values=month_options)
    month_dropdown.grid(row=0, column=1)
    month_dropdown.set("Select Month")  # Default value

    # Label for displaying time elapsed
    elapsed_label = tk.Label(report_window, text="")
    elapsed_label.grid(row=2, column=0, columnspan=2)

    def load_year_options():
        # Execute SQL query to get distinct years from the appointments table
        sql_query = "SELECT DISTINCT YEAR(TimeQueued) FROM appointments"
        cursor.execute(sql_query)

        # Fetch all the distinct years
        distinct_years = cursor.fetchall()

        # Update the options in the year dropdown
        year_options = [year[0] for year in distinct_years]
        year_dropdown['values'] = year_options

    def generate_report():
        # Get values from the dropdowns
        selected_year = year_dropdown.get()
        selected_month_name = month_dropdown.get()

        # Convert month name to numeric value
        month_name_to_number = {
            'January': 1,
            'February': 2,
            'March': 3,
            'April': 4,
            'May': 5,
            'June': 6,
            'July': 7,
            'August': 8,
            'September': 9,
            'October': 10,
            'November': 11,
            'December': 12
        }

        selected_month = month_name_to_number.get(selected_month_name)

        # Replace placeholders in the SQL query based on the selected report type
        if selected_month_name == "all":
            sql_query = f"""
                SELECT
                    CASE MONTH(TimeQueued)
                        WHEN 1 THEN 'January'
                        WHEN 2 THEN 'February'
                        WHEN 3 THEN 'March'
                        WHEN 4 THEN 'April'
                        WHEN 5 THEN 'May'
                        WHEN 6 THEN 'June'
                        WHEN 7 THEN 'July'
                        WHEN 8 THEN 'August'
                        WHEN 9 THEN 'September'
                        WHEN 10 THEN 'October'
                        WHEN 11 THEN 'November'
                        WHEN 12 THEN 'December'
                    END AS Month,
                    is_Virtual,
                    COUNT(*) AS VirtualCount
                FROM
                    appointments
                WHERE
                    YEAR(TimeQueued) = {selected_year}
                GROUP BY
                    Month,
                    is_Virtual;
            """
        else:
            sql_query = f"""
                SELECT
                    CASE MONTH(TimeQueued)
                        WHEN 1 THEN 'January'
                        WHEN 2 THEN 'February'
                        WHEN 3 THEN 'March'
                        WHEN 4 THEN 'April'
                        WHEN 5 THEN 'May'
                        WHEN 6 THEN 'June'
                        WHEN 7 THEN 'July'
                        WHEN 8 THEN 'August'
                        WHEN 9 THEN 'September'
                        WHEN 10 THEN 'October'
                        WHEN 11 THEN 'November'
                        WHEN 12 THEN 'December'
                    END AS Month,
                    is_Virtual,
                    COUNT(*) AS VirtualCount
                FROM
                    appointments
                WHERE
                    YEAR(TimeQueued) = {selected_year}
                    AND MONTH(TimeQueued) = {selected_month}
                GROUP BY
                    Month,
                    is_Virtual;
            """

        # Measure the time elapsed during report generation
        start_time = time.time()

        # Execute the query
        cursor.execute(sql_query)

        # Fetch all the results
        results = cursor.fetchall()

        # Pivot the data for plotting
        pivoted_data = {}
        for row in results:
            month = row[0]
            is_virtual = row[1]
            virtual_count = row[2]

            if month not in pivoted_data:
                pivoted_data[month] = {}

            pivoted_data[month][is_virtual] = virtual_count

         # Plot the chart
        fig, ax = plt.subplots()

        if selected_month_name == "all":
            # Exclude "all" from the chart
            month_options_display = month_options[1:]
            
            # Plot a line for each is_Virtual value over all months
            for is_virtual in ['TRUE', 'FALSE']:
                counts = [pivoted_data.get(month, {}).get(is_virtual, 0) for month in month_options_display]
                ax.plot(month_options_display, counts, label='Virtual' if is_virtual == 'TRUE' else 'Non-Virtual')
        else:
            # Plot a bar chart for the selected month
            for is_virtual in ['TRUE', 'FALSE']:
                count = pivoted_data.get(selected_month_name, {}).get(is_virtual, 0)
                ax.bar('Virtual' if is_virtual == 'TRUE' else 'Non-Virtual', count)

        ax.set_xlabel('Month' if selected_month_name == "all" else 'Is Virtual')
        ax.set_ylabel('Count')
        ax.set_title(f'Appointment Virtual vs Non-Virtual Distribution for {selected_year}')
        ax.legend()

        if selected_month_name == "all":
            ax.set_xticks(month_options_display)
            ax.set_xticklabels(month_options_display, rotation=45, ha="right")  # Rotate labels for better readability

        # Display the chart in the tkinter window
        canvas = FigureCanvasTkAgg(fig, master=report_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=4, column=0, columnspan=2)

        # Calculate and display the time elapsed
        elapsed_time = time.time() - start_time
        elapsed_label.config(text=f"Time Elapsed: {elapsed_time:.2f} seconds")

    # Load year options when the window is created
    load_year_options()

    # Button to trigger report generation
    generate_button = tk.Button(report_window, text="Generate", command=generate_report)
    generate_button.grid(row=1, column=0, columnspan=2)

    # Start the tkinter event loop for the report window
    report_window.mainloop()

    # Close the database connection
    cursor.close()
    connection.close()
