import os
import tempfile
import unittest

import cantools

from dbc_sym_converter import convert_dbc_to_sym, convert_sym_to_dbc

class ConverterRoundTripTest(unittest.TestCase):
    def test_round_trip_messages(self):
        with tempfile.TemporaryDirectory() as tmp:
            sym_path = os.path.join(tmp, "out.sym")
            dbc_round_path = os.path.join(tmp, "round.dbc")

            convert_dbc_to_sym("example.dbc", sym_path)
            convert_sym_to_dbc(sym_path, dbc_round_path)

            orig_db = cantools.database.load_file("example.dbc")
            round_db = cantools.database.load_file(dbc_round_path)

            self.assertEqual(len(orig_db.messages), len(round_db.messages))
            for orig_msg, round_msg in zip(orig_db.messages, round_db.messages):
                self.assertEqual(orig_msg.frame_id, round_msg.frame_id)
                self.assertEqual(orig_msg.name, round_msg.name)
                self.assertEqual(orig_msg.length, round_msg.length)
                self.assertEqual(len(orig_msg.signals), len(round_msg.signals))
                for orig_sig, round_sig in zip(orig_msg.signals, round_msg.signals):
                    self.assertEqual(orig_sig.name, round_sig.name)
                    self.assertEqual(orig_sig.start, round_sig.start)
                    self.assertEqual(orig_sig.length, round_sig.length)

if __name__ == "__main__":
    unittest.main()
