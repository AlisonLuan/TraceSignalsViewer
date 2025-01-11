import os
import tkinter as tk
from tkinter import filedialog
import cantools
from cantools.database.can import Message, Signal

def convert_dbc_to_sym(dbc_path, sym_path):
    """Convert a DBC file to a SYM file."""
    db = cantools.database.load_file(dbc_path)

    with open(sym_path, "w") as sym_file:
        sym_file.write("FormatVersion=6.0 // Do not edit this line!\n")
        sym_file.write("Title=\"" + os.path.basename(dbc_path) + "\"\n")
        sym_file.write("\n")

        for message in db.messages:
            sym_file.write(f"[{message.name}]\n")
            sym_file.write(f"ID={message.frame_id:03X}h\n")
            sym_file.write(f"Len={message.length}\n")

            for signal in message.signals:
                min_value = signal.minimum if signal.minimum is not None else 0
                max_value = signal.maximum if signal.maximum is not None else (2 ** signal.length - 1)
                unit = signal.unit if signal.unit else ""
                unit = unit.replace("\"", "\"\"")  # Escape quotes
                sym_file.write(
                    f"Var={signal.name} unsigned {signal.length} -m /f:{signal.scale} /o:{signal.offset} /max:{max_value}\n"
                )

    print(f"SYM file created at: {sym_path}")

def convert_sym_to_dbc(sym_path, dbc_path):
    """Convert a SYM file to a DBC file."""
    messages = []

    with open(sym_path, "r") as sym_file:
        lines = sym_file.readlines()

    current_message = None
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        print(f"Processing line {line_num}: {line}")  # Debug message

        if line.startswith("FormatVersion") or line.startswith("Title"):
            continue

        if line.startswith("[") and line.endswith("]"):
            if current_message:
                messages.append(current_message)
            message_name = line[1:-1]
            print(f"Starting new message: {message_name}")  # Debug message
            current_message = {
                "name": message_name,
                "id": None,
                "length": None,
                "signals": []
            }
        elif line.startswith("ID="):
            current_message["id"] = int(line.split("=")[1][:-1], 16)
            print(f"Set ID: {current_message['id']}")  # Debug message
        elif line.startswith("Len="):
            current_message["length"] = int(line.split("=")[1])
            print(f"Set Length: {current_message['length']}")  # Debug message
        elif line.startswith("Var="):
            try:
                parts = line.split()
                print(f"Parts: {parts}")  # Debug message
                signal_name = parts[0].split("=")[1]
                start_bit, signal_length = map(int, parts[2].split(","))
                scale = float(parts[4].split(":")[1].replace(",", "."))
                offset = float(parts[5].split(":")[1].replace(",", "."))
                maximum = float(parts[6].split(":")[1].replace(",", "."))

                print(f"Creating signal: {signal_name}, start: {start_bit}, length: {signal_length}")  # Debug message

                # Create the signal without unsupported arguments
                signal = Signal(
                    name=signal_name,
                    start=start_bit,
                    length=signal_length,
                    byte_order="little_endian",  # Default for SYM files
                    is_signed=False  # SYM signals are unsigned
                )

                # Set scale, offset, and maximum separately
                signal.scale = scale
                signal.offset = offset
                signal.maximum = maximum

                current_message["signals"].append(signal)
            except Exception as e:
                print(f"Error parsing line {line_num}: {line}\n{e}")  # Debug message

    if current_message:
        messages.append(current_message)

    db = cantools.database.Database()

    for msg in messages:
        print(f"Adding message to database: {msg['name']}")  # Debug message
        db.messages.append(
            Message(
                frame_id=msg["id"],
                name=msg["name"],
                length=msg["length"],
                signals=msg["signals"]
            )
        )

    with open(dbc_path, "w") as dbc_file:
        dbc_file.write(db.as_dbc_string())

    print(f"DBC file created at: {dbc_path}")

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    file_path = filedialog.askopenfilename(
        title="Select a file to convert",
        filetypes=[("DBC or SYM files", "*.dbc;*.sym")]
    )

    if not file_path:
        print("No file selected. Exiting.")
        return

    output_path = os.path.splitext(file_path)[0] + (".sym" if file_path.endswith(".dbc") else ".dbc")

    if file_path.endswith(".dbc"):
        convert_dbc_to_sym(file_path, output_path)
    elif file_path.endswith(".sym"):
        convert_sym_to_dbc(file_path, output_path)
    else:
        print("Unsupported file type. Please select a .dbc or .sym file.")

if __name__ == "__main__":
    main()
