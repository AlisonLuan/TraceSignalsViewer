from can.io.blf import BLFWriter
from can.io.trc import TRCWriter
from can.io.asc import ASCWriter
from can import Message
import cantools
import random
import time

# Step 1: Load the provided DBC file
dbc_file = "example.dbc"
db = cantools.database.load_file(dbc_file)
print(f"Loaded DBC file: {dbc_file}")

# Step 2: Specify output files
blf_file = "example.blf"
trc_file = "example.trc"
asc_file = "example.asc"

# Step 3: Generate frames and write to BLF, TRC, and ASC
fake_timestamp = time.time()  # Initialize a starting timestamp
messages = []  # Collect all generated messages for TRC and ASC writing

# Create a BLF file writer
with BLFWriter(blf_file) as blf_writer:
    # Create TRC and ASC writers
    with TRCWriter(trc_file) as trc_writer, ASCWriter(asc_file) as asc_writer:
        # Generate frames for the messages in the DBC file
        for i in range(5000):  # Simulating 5000 frames
            for message in db.messages:
                if message.name == "ExampleMessage1":
                    # Clamp Speed to [0, 25.5] based on 8-bit range
                    speed_min, speed_max = 0, 25.5
                    rpm_min, rpm_max = 0, 8000  # DBC-defined range for RPM

                    # Generate randomized values within valid limits
                    speed = random.uniform(speed_min, speed_max)
                    rpm = random.uniform(rpm_min, rpm_max)

                    # Encode the signals into a CAN message
                    data = message.encode({"Speed": speed, "RPM": rpm})
                    msg = Message(
                        arbitration_id=message.frame_id,
                        data=data,
                        is_extended_id=False,
                        timestamp=fake_timestamp  # Use the fake timestamp
                    )
                    # Write the message to BLF, TRC, and ASC
                    blf_writer.on_message_received(msg)
                    trc_writer.on_message_received(msg)
                    asc_writer.on_message_received(msg)
                    messages.append(msg)  # Store for additional processing if needed

                elif message.name == "ExampleMessage2":
                    # Clamp Temperature and Voltage to valid ranges
                    temperature_min, temperature_max = 0, 215  # Adjusted range for unsigned 8-bit
                    voltage_min, voltage_max = 0, 65.535       # DBC-defined range for Voltage

                    # Generate randomized values within valid limits
                    temperature = random.uniform(temperature_min, temperature_max)
                    voltage = random.uniform(voltage_min, voltage_max)

                    # Encode the signals into a CAN message
                    data = message.encode({"Temperature": temperature, "Voltage": voltage})
                    msg = Message(
                        arbitration_id=message.frame_id,
                        data=data,
                        is_extended_id=False,
                        timestamp=fake_timestamp  # Use the fake timestamp
                    )
                    # Write the message to BLF, TRC, and ASC
                    blf_writer.on_message_received(msg)
                    trc_writer.on_message_received(msg)
                    asc_writer.on_message_received(msg)
                    messages.append(msg)  # Store for additional processing if needed

                # Increment the fake timestamp by 50 ms (0.05 seconds)
                fake_timestamp += 0.05

print(f"BLF trace file created: {blf_file}")
print(f"TRC trace file created: {trc_file}")
print(f"ASC trace file created: {asc_file}")
