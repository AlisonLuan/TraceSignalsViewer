import can

def load_trace(filepath):
    """
    Loads a BLF file and parses CAN messages.
    
    :param filepath: Path to the .blf file
    :return: List of CAN messages from the BLF file
    """
    if not filepath.endswith(".blf"):
        raise ValueError("Only .blf files are supported for trace loading.")
    
    try:
        with open(filepath, 'rb') as blf_file:
            # Use the python-can BLFReader
            log = can.io.BLFReader(blf_file)
            messages = [msg for msg in log]
            
            if log.object_count == 0:
                raise ValueError("The BLF file is empty.")
            
        return messages
    except Exception as e:
        raise ValueError(f"Error reading BLF file: {e}")
