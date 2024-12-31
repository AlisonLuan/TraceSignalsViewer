import tkinter as tk
from tkinter import filedialog, messagebox
from trace_handler import load_trace
from dbc_handler import load_dbc, translate_trace
from plotter import plot_signals

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

        self.load_dbc_btn = tk.Button(self.root, text="Load DBC", command=self.load_dbc_file, state=tk.DISABLED)
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
        filepath = filedialog.askopenfilename(filetypes=[("BLF Files", "*.blf")])
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
            self.load_dbc_btn.config(state=tk.NORMAL)  # Enable "Load DBC" button
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_dbc_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("DBC Files", "*.dbc")])
        if not filepath:
            return
        self.dbc_file = filepath
        try:
            if self.trace_file:
                trace_data = load_trace(self.trace_file)
                self.translated_data = translate_trace(trace_data, filepath)
                
                # Format translated data line by line
                formatted_data = ""
                for index, (timestamp, signals) in enumerate(self.translated_data, start=1):
                    formatted_data += f"{index}. Timestamp: {timestamp}, Signals: {signals}\n"
                
                self.log_to_console(f"Translated Data (Line by Line):\n{formatted_data}")
                messagebox.showinfo("Success", "DBC file loaded and trace translated successfully.")
                self.plot_signals_btn.config(state=tk.NORMAL)  # Enable "Plot Signals" button
            else:
                messagebox.showerror("Error", "Please load a trace file first.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def plot_signals(self):
        if not self.translated_data:
            messagebox.showerror("Error", "No translated data available to plot.")
            return
        plot_signals(self.translated_data)

    def run(self):
        self.root.mainloop()
