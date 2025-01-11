import tkinter as tk
from tkinter import filedialog, messagebox
from trace_handler import load_trace
from dbc_handler import load_dbc, translate_trace
from dbc_sym_converter import convert_sym_to_dbc
from plotter import plot_signals
import os

class HMI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Trace Signal Viewer")
        self.root.geometry("800x600")

        self.trace_file = None
        self.dbc_file = None
        self.translated_data = None

        self.setup_ui()

    def setup_ui(self):
        self.load_trace_btn = tk.Button(self.root, text="Load Trace", command=self.load_trace_file)
        self.load_trace_btn.pack(pady=10)

        self.load_dbc_btn = tk.Button(self.root, text="Load DBC/SYM", command=self.load_dbc_or_sym_file, state=tk.DISABLED)
        self.load_dbc_btn.pack(pady=10)

        self.plot_signals_btn = tk.Button(self.root, text="Plot Signals", command=self.plot_signals, state=tk.DISABLED)
        self.plot_signals_btn.pack(pady=10)

        self.console = tk.Text(self.root, height=20, width=90)
        self.console.pack(pady=10)

    def log_to_console(self, message):
        self.console.delete(1.0, tk.END)
        self.console.insert(tk.END, message)
        self.console.see(tk.END)

    def load_trace_file(self):
        filepath = filedialog.askopenfilename(filetypes=[
            ("Supported Trace Files", "*.blf;*.trc;*.asc"),
            ("BLF Files", "*.blf"),
            ("TRC Files", "*.trc"),
            ("ASC Files", "*.asc")
        ])
        if not filepath:
            return
        self.trace_file = filepath
        try:
            trace_data = load_trace(filepath)
            
            # Format trace data line by line
            formatted_data = ""
            for index, msg in enumerate(trace_data, start=1):
                formatted_data += f"{index}. Timestamp: {msg.timestamp}, ID: {msg.arbitration_id}, Data: {msg.data.hex()}\n"
            
            self.log_to_console(f"Raw Trace Data (Line by Line):\n{formatted_data}")
            messagebox.showinfo("Success", "Trace file loaded successfully.")
            self.load_dbc_btn.config(state=tk.NORMAL)  # Enable "Load DBC/SYM" button
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load trace file: {e}")

    def load_dbc_or_sym_file(self):
        filepath = filedialog.askopenfilename(filetypes=[
            ("DBC or SYM Files", "*.dbc;*.sym"),
            ("DBC Files", "*.dbc"),
            ("SYM Files", "*.sym")
        ])
        if not filepath:
            return

        try:
            if filepath.endswith(".sym"):
                # Convert SYM to temporary DBC file
                temp_dbc_path = os.path.splitext(filepath)[0] + "_converted.dbc"
                convert_sym_to_dbc(filepath, temp_dbc_path)
                filepath = temp_dbc_path

            self.dbc_file = filepath

            if self.trace_file:
                trace_data = load_trace(self.trace_file)
                self.translated_data = translate_trace(trace_data, filepath)
                
                # Format translated data line by line
                formatted_data = ""
                for index, (timestamp, signals) in enumerate(self.translated_data, start=1):
                    formatted_data += f"{index}. Timestamp: {timestamp}, Signals: {signals}\n"
                
                self.log_to_console(f"Translated Data (Line by Line):\n{formatted_data}")
                messagebox.showinfo("Success", "File loaded and trace translated successfully.")
                self.plot_signals_btn.config(state=tk.NORMAL)  # Enable "Plot Signals" button
            else:
                messagebox.showerror("Error", "Please load a trace file first.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

    def plot_signals(self):
        if not self.translated_data:
            messagebox.showerror("Error", "No translated data available to plot.")
            return
        plot_signals(self.translated_data)

    def run(self):
        self.root.mainloop()