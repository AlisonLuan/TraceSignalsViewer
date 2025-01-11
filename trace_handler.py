import can

def load_trace(filepath):
    """
    Loads a trace file (.blf, .trc, .asc) and parses CAN messages.
    
    :param filepath: Path to the trace file
    :return: List of CAN messages from the trace file
    """
    try:
        # Select the appropriate reader based on file extension
        if filepath.endswith(".blf"):
            with open(filepath, 'rb') as file:
                log = can.io.BLFReader(file)
                messages = [msg for msg in log]
        elif filepath.endswith(".asc"):
            with open(filepath, 'r') as file:
                log = can.io.ASCReader(file)
                messages = [msg for msg in log]
        elif filepath.endswith(".trc"):
            with open(filepath, 'r') as file:
                log = can.io.TRCReader(file)
                messages = [msg for msg in log]
        else:
            raise ValueError("Unsupported file format. Supported formats are .blf, .asc, and .trc.")

        # Validate messages
        if not messages:
            raise ValueError("The trace file is empty or unsupported content.")

        return messages

    except Exception as e:
        raise ValueError(f"Error reading trace file {filepath}: {e}")
