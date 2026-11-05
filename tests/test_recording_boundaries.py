"""Prevent unrelated recordings from becoming one fictitious population."""

from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from preprocessing import (align_spikes_to_position, build_activity_matrix,
                           extract_position, select_session)
from rate_maps import build_all_rate_maps


def session(name, spikes, nid="cell"):
    return {"filename": name, "pos_ts": np.array([0.0, 0.1, 0.2, 0.3]),
            "neurons": {nid: {"spike_times": np.array(spikes)}}}


class RecordingTests(unittest.TestCase):
    def test_spikes_use_nearest_position_not_always_next_position(self):
        spikes, indices = align_spikes_to_position([0, 1, 2],
                                                  [-1, 0, 0.2, 0.5, 0.9, 1, 2, 3, np.nan])
        np.testing.assert_array_equal(spikes, [0, 0.2, 0.5, 0.9, 1, 2])
        np.testing.assert_array_equal(indices, [0, 0, 0, 1, 1, 2])
        for timestamps in ([], [0, 0], [1, 0], [0, np.inf]):
            with self.assertRaises(ValueError):
                align_spikes_to_position(timestamps, [0.1])

    def test_position_cleaning_removes_all_nonfinite_coordinates(self):
        raw = {"pos_timeStamps": np.array([0, 1, 2, 3]),
               "pos_x": np.array([0, np.inf, 1, 2]),
               "pos_y": np.array([0, 1, np.nan, 2])}
        ts, x, y = extract_position(raw)
        np.testing.assert_array_equal(ts, [0, 3])
        np.testing.assert_array_equal(x, [0, 2])
        np.testing.assert_array_equal(y, [0, 2])

    def test_multiple_recordings_require_selection_even_with_unique_ids(self):
        for second_id in ("cell", "other"):
            with self.assertRaisesRegex(ValueError, "separate files must not be pooled"):
                build_activity_matrix([session("a.mat", [0.01]),
                                       session("b.mat", [0.02], second_id)])

    def test_selection_does_not_concatenate_same_named_cells(self):
        sessions = [session("a.mat", [0.01]), session("b.mat", [0.02, 0.03])]
        matrix, ids, times = build_activity_matrix(sessions, 0.1, session_name="a.mat")
        np.testing.assert_array_equal(matrix[:, 0], [10, 0, 0])
        np.testing.assert_allclose(times, [0, 0.1, 0.2])
        self.assertEqual(ids, ["cell"])

    def test_missing_and_empty_recordings_fail(self):
        with self.assertRaises(ValueError):
            select_session([])
        with self.assertRaises(ValueError):
            select_session([session("a.mat", [])], "missing.mat")

    def test_rate_map_builder_rejects_cross_trial_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                build_all_rate_maps([session("a.mat", []), session("b.mat", [])], tmp)

    def test_invalid_bins_or_timestamps_fail(self):
        for size in (0, -0.1, np.nan, 1):
            with self.assertRaises(ValueError):
                build_activity_matrix([session("a.mat", [])], size)
        bad = session("a.mat", [])
        bad["pos_ts"] = np.array([0.0, 0.0])
        with self.assertRaises(ValueError):
            build_activity_matrix([bad])


if __name__ == "__main__":
    unittest.main()
