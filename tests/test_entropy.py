"""Analytic entropy cases and missing-data semantics, not biological tests."""

from pathlib import Path
import sys
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from entropy import (activity_entropy_summary, neural_entropy, spatial_entropy,
                     temporal_entropy, weight_entropy)


class EntropyTests(unittest.TestCase):
    def test_known_distributions_and_exact_zero_terms(self):
        self.assertEqual(float(weight_entropy([0, 7, 0])), 0)
        self.assertEqual(float(weight_entropy([1, 1, 1, 1])), 2)
        self.assertAlmostEqual(float(weight_entropy([1, 3])), 0.8112781244591328)

    def test_scaling_and_large_finite_weights(self):
        for scale in (1e-300, 1, 1e300):
            self.assertAlmostEqual(float(weight_entropy(np.array([1, 3])*scale)),
                                   0.8112781244591328)

    def test_silence_is_undefined_and_summary_reports_denominator(self):
        entropy = neural_entropy([[0, 0], [1, 1], [0, 2]])
        self.assertTrue(np.isnan(entropy[0]))
        np.testing.assert_array_equal(entropy[1:], [1, 0])
        stats = activity_entropy_summary(entropy)
        self.assertEqual(stats["total_time_bins"], 3)
        self.assertEqual(stats["defined_time_bins"], 2)
        self.assertEqual(stats["undefined_time_bins"], 1)
        self.assertEqual(stats["mean_neural_entropy"], 0.5)
        self.assertTrue(np.isnan(activity_entropy_summary([np.nan])["mean_neural_entropy"]))

    def test_unobserved_spatial_bins_are_not_measured_zeros(self):
        self.assertEqual(spatial_entropy([[np.nan, 1], [1, 0]]), 1)
        for values in ([[0, 0]], [[np.nan, np.nan]]):
            self.assertTrue(np.isnan(spatial_entropy(values)))

    def test_window_count_and_remainder(self):
        # 101 samples: one 2-sample window followed by 99 1-sample windows.
        p = np.r_[2, np.ones(99)] / 101
        expected = -np.sum(p*np.log2(p))
        result = temporal_entropy(np.ones(101), n_bins=100)
        self.assertAlmostEqual(result, expected)
        self.assertLessEqual(result, np.log2(100))
        self.assertAlmostEqual(temporal_entropy(np.ones(6), n_bins=3), np.log2(3))
        self.assertEqual(temporal_entropy([1, 1], n_bins=100), 1)

    def test_allocation_entropy_cannot_identify_window_order(self):
        a = [1, 2, 0, 0, 3, 0]
        b = [0, 0, 3, 0, 1, 2]
        self.assertEqual(temporal_entropy(a, n_bins=3), temporal_entropy(b, n_bins=3))
        self.assertTrue(np.isnan(temporal_entropy([0, 0])))
        self.assertTrue(np.isnan(temporal_entropy([])))

    def test_invalid_weights_and_window_counts_fail(self):
        for weights in ([1, -1], [1, np.inf], [1, np.nan]):
            with self.assertRaises(ValueError):
                weight_entropy(weights)
            with self.assertRaises(ValueError):
                temporal_entropy(weights)
        for count in (0, -1, 1.5, np.nan, True):
            with self.assertRaises(ValueError):
                temporal_entropy([1, 1], count)
        with self.assertRaises(ValueError):
            neural_entropy([1, 1])
        with self.assertRaises(ValueError):
            spatial_entropy([1, np.inf])


if __name__ == "__main__":
    unittest.main()
