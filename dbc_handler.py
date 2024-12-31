import cantools

def load_dbc(filepath):
    try:
        dbc = cantools.database.load_file(filepath)
        return dbc
    except Exception as e:
        raise ValueError(f"Error loading DBC file: {str(e)}")

def translate_trace(trace_data, dbc_filepath):
    """
    Translates a list of CAN messages using a DBC file.

    :param trace_data: List of CAN messages
    :param dbc_filepath: Path to the DBC file
    :return: List of tuples containing timestamp and decoded signals
    """
    dbc = load_dbc(dbc_filepath)  # Load the DBC file
    translated = []

    for message in trace_data:
        try:
            # Decode the message using the DBC
            decoded = dbc.decode_message(message.arbitration_id, message.data)
            translated.append((message.timestamp, decoded))
        except Exception:
            # Skip messages that can't be decoded
            continue

    return translated
