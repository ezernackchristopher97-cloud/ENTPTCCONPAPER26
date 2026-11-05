"""Synthetic checks of contraction, observation resolution, and projection.

No neural recordings, fitted parameters, noise model, or thermodynamic
measurements enter these calculations. All dynamical quantities use arbitrary
model units. Exact identities are stated separately from finite numerical error.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.constants import Boltzmann, Planck, elementary_charge

from entropy import weight_entropy
from oscillator_validation import (Parameters, amplitude_rhs, critical_phase_difference,
                                   phase_rhs, reference)


def quantized_binary_information(times, *, rate=2.0, width=0.1):
    """I(B;Q(x_B(t))) for equiprobable B and x_B(0) in {0.25,0.75}.

    The noiseless deterministic quantizer Q(x)=floor(x/width) is specified
    explicitly. Its output entropy equals mutual information since H(Q|B)=0.
    The two-point distribution is enumerated, not statistically estimated.
    Positions and bin boundaries still use floating-point arithmetic.
    """
    times = np.asarray(times, dtype=float)
    if np.any(~np.isfinite(times)) or np.any(times < 0):
        raise ValueError("times must be finite and nonnegative")
    if not np.isfinite(rate) or rate <= 0 or not np.isfinite(width) or width <= 0:
        raise ValueError("rate and width must be finite and positive")
    positions = np.exp(-rate*times[..., None]) * np.array([0.25, 0.75])
    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        scaled = positions / width
    # Beyond 2**53, adjacent integer bin labels are not all representable.
    # In particular, inf == inf must not be reported as lost information.
    if np.any(~np.isfinite(scaled)) or np.any(scaled >= 2**53):
        raise FloatingPointError("Quantizer bins exceed float precision; increase width")
    bins = np.floor(scaled)
    bits = np.where(bins[..., 0] == bins[..., 1], 0.0, 1.0)
    return positions, bins, bits


def run_validation(output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    t = np.linspace(0, 3, 301)
    positions, bins, bits = quantized_binary_information(t)
    _, _, finer_bits = quantized_binary_information(t, width=0.05)
    np.savetxt(output_dir / "information_resolution.csv",
               np.c_[t, positions, positions[:, 1]-positions[:, 0], bins, bits, finer_bits],
               delimiter=",", comments="",
               header="time,x_label0,x_label1,separation,bin_label0,bin_label1,information_bits_width_0.1,information_bits_width_0.05")

    # Check the contracting flow against two independent numerical trajectories.
    p = Parameters()
    trajectories = [reference(amplitude_rhs, [0.2, 0.9, 1+x, 1.1], 3, p).sol(t)
                    for x in (0.25, 0.75)]
    numerical_positions = np.column_stack([y[2]-1 for y in trajectories])
    finite_inverse = numerical_positions*np.exp(2*t[:, None])

    # A shared first phase does not determine its derivative under coupling.
    coupled = Parameters(epsilon=0.6)
    same_observation_states = [np.array([0.0, 0.0]), np.array([0.0, np.pi/2])]
    projected_velocities = [float(phase_rhs(0, y, coupled)[0]) for y in same_observation_states]

    # The SUM of circular phases does have autonomous dynamics. Avoid treating
    # their average as a globally single-valued circular coordinate.
    sum_runs = [reference(phase_rhs, y, 20, coupled) for y in ([0.0, 0.0], [0.4, -0.4])]
    factor_t = np.linspace(0, 20, 1001)
    sum_phases = np.array([sol.sol(factor_t).sum(axis=0) for sol in sum_runs])
    expected_sum = (coupled.omega1+coupled.omega2)*factor_t
    sum_error = np.abs(np.angle(np.exp(1j*(sum_phases-expected_sum))))

    # At critical coupling the recovery rate is not a negative constant.
    critical_epsilon = (p.omega2-p.omega1)/2
    critical = Parameters(epsilon=critical_epsilon)
    critical_t = np.linspace(0, 200, 2001)
    critical_sol = reference(phase_rhs, [0, 0], 200, critical).sol(critical_t)
    numerical_delta = critical_sol[1]-critical_sol[0]
    exact_delta = critical_phase_difference(critical_t, critical_epsilon)
    np.savetxt(output_dir / "critical_locking.csv",
               np.c_[critical_t, numerical_delta, exact_delta, np.pi/2-exact_delta],
               delimiter=",", comments="",
               header="time,numerical_delta,exact_delta,distance_below_pi_over_2")

    result = {
        "kind": "synthetic mathematical checks, not biological or thermodynamic evidence",
        "binary_label_entropy_bits": float(weight_entropy([1, 1])),
        "finite_time_exact_observation_information_bits": 1.0,
        "exact_information_basis": "Two distinct initial values remain distinct for every finite t under x(t)=exp(-2t)x(0).",
        "quantizer": "floor(x/width), widths 0.1 and 0.05 in arbitrary units",
        "zero_bin_entry_times": {str(width): float(np.log(0.75/width)/2) for width in (0.1, 0.05)},
        "max_numerical_position_error": float(np.max(np.abs(numerical_positions-positions))),
        "max_finite_inverse_error": float(np.max(np.abs(finite_inverse-[0.25, 0.75]))),
        "nonautonomous_projection_phi1_velocities": projected_velocities,
        "autonomous_sum_phase_max_circular_error": float(sum_error.max()),
        "critical_phase_difference_max_error": float(np.max(np.abs(numerical_delta-exact_delta))),
        "critical_asymptotic_scaled_error": "t*(pi/2-delta(t)) -> 1/epsilon, analytically",
        "unit_checks": {
            "photon_energy_meV_at_0.1_and_10_THz": (Planck*np.array([1e11, 1e13])/elementary_charge*1e3).tolist(),
            "kBT_meV_at_310K": float(Boltzmann*310/elementary_charge*1e3),
            "decades_from_1kHz_to_1GHz_and_10THz": np.log10(np.array([1e9, 1e13])/1e3).tolist(),
        },
        "limits": [
            "Quantized information depends on resolution, bin alignment, and the chosen initial distribution.",
            "Exponential contraction can become numerically indistinguishable at long times; the finite-time injectivity statement is analytic.",
            "No neural memory time, entropy production rate, or cross-scale coupling is inferred.",
        ],
    }
    (output_dir / "summary.json").write_text(json.dumps(result, indent=2)+"\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parents[1] / "outputs" / "information_validation")
    args = parser.parse_args()
    print(json.dumps(run_validation(args.output_dir), indent=2))
