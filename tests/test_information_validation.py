"""Counterexamples separating dynamical stability from information claims."""

from pathlib import Path
import sys
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from information_validation import quantized_binary_information
from oscillator_validation import (Parameters, critical_phase_difference,
                                   phase_rhs, reference)


class InformationBoundaryTests(unittest.TestCase):
    def test_critical_solution_preserves_initial_slope_at_small_times(self):
        times = np.array([0.0, 1e-18, 1e-15, 1e-12])
        epsilon = 0.2
        delta = critical_phase_difference(times, epsilon)
        self.assertEqual(delta[0], 0)
        self.assertTrue(np.all(delta[1:] > 0))
        # The differential equation gives delta'(0) = 2*epsilon.
        np.testing.assert_allclose(delta[1:]/times[1:], 2*epsilon,
                                   rtol=1e-11, atol=0)

    def test_critical_solution_handles_extreme_finite_positive_products(self):
        with np.errstate(all="raise"):
            tiny = critical_phase_difference(1e100, 1e-300)
            late = critical_phase_difference(1e308, 2.0)
        self.assertAlmostEqual(float(tiny)/1e-200, 2.0, places=14)
        self.assertEqual(float(late), np.pi/2)

    def test_quantizer_rejects_unrepresentable_bin_labels(self):
        for width in (np.nextafter(0.0, 1.0), 1e-18):
            with self.assertRaises(FloatingPointError):
                quantized_binary_information([0.0], width=width)

    def test_exact_contraction_retains_distinction_but_quantization_can_lose_it(self):
        positions, bins, bits = quantized_binary_information([0, 0.5, 1.5, 3])
        self.assertTrue(np.all(positions[:, 1] > positions[:, 0]))
        np.testing.assert_array_equal(bits, [1, 1, 0, 0])
        self.assertEqual(bins[-1, 0], bins[-1, 1])

    def test_resolution_changes_information_at_same_physical_state(self):
        coarse, _, coarse_bits = quantized_binary_information([1.1], width=0.1)
        fine, _, fine_bits = quantized_binary_information([1.1], width=0.05)
        np.testing.assert_array_equal(coarse, fine)
        self.assertEqual(coarse_bits[0], 0)
        self.assertEqual(fine_bits[0], 1)

    def test_projection_of_one_phase_fails_autonomous_closure(self):
        p = Parameters(epsilon=0.6)
        a, b = [0, 0], [0, np.pi/2]
        self.assertEqual(a[0], b[0])
        self.assertAlmostEqual(phase_rhs(0, b, p)[0]-phase_rhs(0, a, p)[0], 0.6)
        x = reference(phase_rhs, a, 0.1, p).y[0, -1]
        y = reference(phase_rhs, b, 0.1, p).y[0, -1]
        self.assertGreater(abs(y-x), 0.05)

    def test_sum_phase_has_closed_dynamics_despite_coupling(self):
        p = Parameters(epsilon=0.6)
        t = np.linspace(0, 20, 101)
        for initial in ([0, 0], [0.4, -0.4]):
            summed = reference(phase_rhs, initial, 20, p).sol(t).sum(axis=0)
            np.testing.assert_allclose(summed, (p.omega1+p.omega2)*t, rtol=0, atol=1e-11)

    def test_critical_solution_is_algebraic_not_exponential_locking(self):
        epsilon = (np.sqrt(2)-1)/2
        p = Parameters(epsilon=epsilon)
        t = np.linspace(0, 200, 1001)
        y = reference(phase_rhs, [0, 0], 200, p).sol(t)
        np.testing.assert_allclose(y[1]-y[0], critical_phase_difference(t, epsilon),
                                   rtol=0, atol=2e-11)
        late = np.array([1e4, 1e5, 1e6])
        scaled = late*(np.pi/2-critical_phase_difference(late, epsilon))
        self.assertLess(abs(scaled[-1]-1/epsilon), 2e-5)
        self.assertTrue(np.all(np.diff(scaled) > 0))
        # On the other side the vector field initially moves AWAY from pi/2.
        self.assertGreater(2*epsilon*(1-np.sin(np.pi/2+0.01)), 0)


if __name__ == "__main__":
    unittest.main()
