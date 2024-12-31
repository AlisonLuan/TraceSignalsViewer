import tkinter as tk
from tkinter import simpledialog, Toplevel, Listbox, Scrollbar, Button, messagebox
import matplotlib.pyplot as plt

def plot_signals(translated_data):
    """
    Allows the user to select and plot multiple signals from the translated data using a multi-selection listbox.

    :param translated_data: List of tuples containing timestamp and decoded signals
    """
    # Extract unique signal names from the translated data
    signal_names = set()
    for _, signals in translated_data:
        signal_names.update(signals.keys())

    # If no signals are available, show an error message
    if not signal_names:
        messagebox.showerror("Error", "No signals available to plot.")
        return

    # Create a selection window
    def show_selection_window():
        # Get selected signals
        selected_indices = signal_listbox.curselection()
        selected_signals = [signal_listbox.get(i) for i in selected_indices]

        if not selected_signals:
            messagebox.showwarning("Warning", "No signals selected for plotting.")
            return

        # Plot the selected signals
        plt.figure(figsize=(10, 6))
        for signal in selected_signals:
            timestamps = []
            values = []
            for timestamp, signals in translated_data:
                if signal in signals:
                    timestamps.append(timestamp)
                    values.append(signals[signal])
            if timestamps and values:
                plt.plot(timestamps, values, label=signal)

        plt.xlabel("Time")
        plt.ylabel("Signal Value")
        plt.title("Signal Plot")
        plt.legend()
        plt.show()

        # Close the selection window after plotting
        selection_window.destroy()

    # Create a new Toplevel window for signal selection
    selection_window = Toplevel()
    selection_window.title("Select Signals to Plot")
    selection_window.geometry("300x400")

    # Add a scrollbar for the listbox
    scrollbar = Scrollbar(selection_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Add a listbox for signal selection
    signal_listbox = Listbox(selection_window, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar.set, width=40, height=20)
    for signal in sorted(signal_names):
        signal_listbox.insert(tk.END, signal)
    signal_listbox.pack(pady=5)

    # Configure scrollbar
    scrollbar.config(command=signal_listbox.yview)

    # Add a button to confirm selection
    select_button = Button(selection_window, text="Plot Selected Signals", command=show_selection_window)
    select_button.pack(pady=10)

    # Run the selection window
    selection_window.grab_set()
    selection_window.mainloop()
