"""Analytic benchmarks for synthetic dynamics, not empirical neural tests."""

from dataclasses import replace
from pathlib import Path
import sys
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from oscillator_validation import (Parameters, amplitude_rhs, convergence_study,
                                   forced_radius_graph, locked_solution,
                                   phase_distance, phase_rhs, reference, rk4)


class OscillatorTests(unittest.TestCase):
    def test_independent_solution_and_neutral_phase_kick(self):
        p = Parameters()
        t, y = rk4(phase_rhs, [0.2, 0.9], 20, 0.02, p)
        expected = np.array([0.2, 0.9]) + t[:, None] * [1, np.sqrt(2)]
        np.testing.assert_allclose(y, expected, rtol=0, atol=2e-11)
        _, kicked = rk4(phase_rhs, [0.2, 1.1], 20, 0.02, p)
        np.testing.assert_allclose(phase_distance(kicked, y), 0.2, rtol=0, atol=2e-11)

    def test_rational_return_and_circular_metric(self):
        initial = np.array([0.2, 0.9])
        returned = initial + 4*np.pi*np.array([1, 1.5])
        self.assertLess(phase_distance(initial, returned), 1e-14)
        self.assertAlmostEqual(phase_distance([np.pi-0.01, 0], [-np.pi+0.01, 0]), 0.02)

    def test_locked_branch_and_unstable_branch_have_opposite_stability(self):
        p = Parameters(epsilon=0.6)
        delta, exponent = locked_solution(p)
        f = lambda d: p.omega2-p.omega1 - 2*p.epsilon*np.sin(d)
        self.assertAlmostEqual(f(delta), 0)
        self.assertAlmostEqual(f(np.pi-delta), 0)
        self.assertLess(-2*p.epsilon*np.cos(delta), 0)
        self.assertGreater(-2*p.epsilon*np.cos(np.pi-delta), 0)
        self.assertAlmostEqual(exponent, -2*p.epsilon*np.cos(delta))
        _, y = rk4(phase_rhs, [0.2, 0.9], 40, 0.02, p)
        self.assertLess(abs(y[-1, 1]-y[-1, 0]-delta), 1e-10)

    def test_locking_leaves_common_phase_neutral(self):
        p = Parameters(epsilon=0.6)
        _, y = rk4(phase_rhs, [0.2, 0.9], 30, 0.02, p)
        _, kicked = rk4(phase_rhs, [0.2, 1.1], 30, 0.02, p)
        np.testing.assert_allclose(np.mean(kicked-y, axis=1), 0.1, rtol=0, atol=1e-11)
        self.assertGreater(phase_distance(kicked[-1], y[-1]), 0.1)

    def test_drift_and_nonhyperbolic_threshold(self):
        p = Parameters()
        critical = (p.omega2-p.omega1)/2
        self.assertIsNone(locked_solution(replace(p, epsilon=0.99*critical)))
        self.assertIsNone(locked_solution(replace(p, epsilon=critical)))
        self.assertIsNotNone(locked_solution(replace(p, epsilon=1.01*critical)))
        q = replace(p, epsilon=0.1)
        t, y = rk4(phase_rhs, [0.2, 0.9], 40, 0.02, q)
        self.assertTrue(np.all(np.diff(y[:, 1]-y[:, 0]) > 0))
        # Mean phase is an exact linear integral of the symmetric coupling.
        np.testing.assert_allclose(y.mean(axis=1), 0.55 + t*(1+np.sqrt(2))/2,
                                   rtol=0, atol=1e-11)

    def test_slip_rate_matches_full_cycle_times_in_both_directions(self):
        from scipy.optimize import brentq
        for omega in ((1, np.sqrt(2)), (np.sqrt(2), 1)):
            p = Parameters(omega1=omega[0], omega2=omega[1], epsilon=0.1)
            sign = np.sign(p.omega2-p.omega1)
            sol = reference(phase_rhs, [0.2, 0.9], 50, p)
            roots = [brentq(lambda t: np.diff(sol.sol(t))[0] - (0.7+sign*cycle*2*np.pi),
                            0, 50, xtol=1e-11) for cycle in (1, 2)]
            measured = sign*2*np.pi/(roots[1]-roots[0])
            exact = sign*np.sqrt((p.omega2-p.omega1)**2-4*p.epsilon**2)
            self.assertAlmostEqual(measured, exact, places=10)

    def test_radial_contraction_and_exact_deformed_torus(self):
        for alpha in (0.0, 0.1):
            p = Parameters(radial_forcing=alpha)
            initial = np.array([0.2, 0.9, 0.7, 1.3])
            t, y = rk4(amplitude_rhs, initial, 8, 0.01, p)
            residual = y[:, 2:]-forced_radius_graph(y[:, :2], p)
            expected = (initial[2:]-forced_radius_graph(initial[:2], p))*np.exp(-2*t[:, None])
            np.testing.assert_allclose(residual, expected, rtol=0, atol=3e-10)
            self.assertGreater(y[:, 2:].min(), 0)

    def test_same_torus_flow_can_have_opposite_normal_stability(self):
        on_torus = np.array([0.2, 0.9, 1.0, 1.0])
        common = amplitude_rhs(0, on_torus, Parameters())
        for rate in (2.0, 0.0, -2.0):
            p = Parameters(radial_rate=rate)
            np.testing.assert_allclose(amplitude_rhs(0, on_torus, p), common)
            t, y = rk4(amplitude_rhs, [0.2, 0.9, 1.001, 0.999], 1, 0.01, p)
            expected = np.array([0.001, -0.001])*np.exp(-rate*t[:, None])
            np.testing.assert_allclose(y[:, 2:]-1, expected, rtol=0, atol=2e-11)
        p = Parameters(epsilon=0.6)
        t, y = rk4(amplitude_rhs, [0.2, 0.9, 0.7, 1.3], 20, 0.01, p)
        delta, _ = locked_solution(p)
        self.assertLess(abs(y[-1, 1]-y[-1, 0]-delta), 1e-9)
        np.testing.assert_allclose(y[:, 2:]-1, [-0.3, 0.3]*np.exp(-2*t[:, None]),
                                   rtol=0, atol=2e-10)

    def test_fourth_order_refinement_against_adaptive_solver(self):
        rows = convergence_study()
        for case in {row["case"] for row in rows}:
            subset = [row for row in rows if row["case"] == case]
            for row in subset[1:3]:
                self.assertGreater(row["observed_order"], 3.7, (case, row))
                self.assertLess(row["observed_order"], 4.3, (case, row))
            self.assertLess(subset[-1]["max_abs_error"], 2e-9)

    def test_independent_adaptive_solvers(self):
        p = Parameters(epsilon=0.6)
        t = np.linspace(0, 20, 401)
        a = reference(phase_rhs, [0.2, 0.9], 20, p).sol(t)
        b = reference(phase_rhs, [0.2, 0.9], 20, p, method="RK45").sol(t)
        np.testing.assert_allclose(a, b, rtol=0, atol=1e-9)

    def test_rk4_rejects_invalid_grid(self):
        for duration, step in [(1, 0.3), (0, 0.1), (1, 0), (1, np.nan)]:
            with self.assertRaises(ValueError):
                rk4(phase_rhs, [0.2, 0.9], duration, step, Parameters())

    def test_large_rk4_step_can_lose_normal_stability(self):
        initial = np.array([0.2, 0.9, 0.99, 1.01])
        _, y = rk4(amplitude_rhs, initial, 3, 1.5, Parameters())
        # lambda*h = 3 is outside the negative-real-axis RK4 stability interval.
        # The exact normal mode decays, while this deliberately coarse run grows.
        self.assertGreater(np.linalg.norm(y[-1, 2:]-1), np.linalg.norm(initial[2:]-1))


if __name__ == "__main__":
    unittest.main()
