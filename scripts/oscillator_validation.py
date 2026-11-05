"""Finite, synthetic checks of phase dynamics and normal attraction.

All times and frequencies are in arbitrary model units. No parameters are fitted
to neural recordings. Run from the repository root with
    python scripts/oscillator_validation.py
This does not run or calibrate the biological PCA/UMAP/Ripser pipeline.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass, replace
import importlib.metadata
import json
from pathlib import Path
import platform

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq


@dataclass(frozen=True)
class Parameters:
    omega1: float = 1.0
    omega2: float = np.sqrt(2.0)
    epsilon: float = 0.0
    radial_rate: float = 2.0
    radial_forcing: float = 0.0


def phase_rhs(_time, phase, p):
    coupling = p.epsilon * np.sin(phase[1] - phase[0])
    return np.array([p.omega1 + coupling, p.omega2 - coupling])


def amplitude_rhs(time, state, p):
    """State is (phi1, phi2, r1, r2); valid near positive radii."""
    angular = phase_rhs(time, state[:2], p)
    radial = -p.radial_rate * (state[2:] - 1.0)
    radial += p.radial_forcing * np.sin(state[:2])
    return np.r_[angular, radial]


def phase_distance(x, y):
    """Flat product-circle distance; handles the branch cut at +/- pi."""
    delta = np.arctan2(np.sin(np.asarray(x) - y), np.cos(np.asarray(x) - y))
    return np.linalg.norm(delta, axis=-1)


def locked_solution(p):
    """Stable 1:1 branch for nonnegative attractive coupling, if hyperbolic."""
    detuning = p.omega2 - p.omega1
    if p.epsilon <= 0 or abs(detuning) >= 2 * p.epsilon:
        return None
    delta = np.arcsin(detuning / (2 * p.epsilon))
    exponent = -np.sqrt(4 * p.epsilon**2 - detuning**2)
    return float(delta), float(exponent)


def critical_phase_difference(times, epsilon):
    """Exact critical solution for Delta omega=2*epsilon>0 and delta(0)=0.

    tan(delta/2) = epsilon*t/(1+epsilon*t), so approach to pi/2 is
    algebraic, with t*(pi/2-delta) tending to 1/epsilon.
    """
    times = np.asarray(times, dtype=float)
    if not np.isfinite(epsilon) or epsilon <= 0 or np.any(~np.isfinite(times)) or np.any(times < 0):
        raise ValueError("epsilon must be positive and times finite and nonnegative")
    # z/(1+z) avoids cancellation in 1-1/(1+z) for very small times.
    # If the positive product overflows, the limiting angle is already
    # indistinguishable from pi/2 at floating-point precision.
    with np.errstate(over="ignore"):
        scaled = epsilon * times
        ratio = np.divide(scaled, 1 + scaled, out=np.ones_like(scaled),
                          where=np.isfinite(scaled))
    return 2 * np.arctan(ratio)


def forced_radius_graph(phase, p):
    """Exact invariant graph for epsilon=0, not a generic persistence test."""
    if p.epsilon != 0:
        raise ValueError("The explicit graph requires independent phase dynamics")
    omega = np.array([p.omega1, p.omega2])
    return 1 + p.radial_forcing * (
        p.radial_rate * np.sin(phase) - omega * np.cos(phase)
    ) / (p.radial_rate**2 + omega**2)


def rk4(rhs, initial, duration, step, p):
    """Fixed RK4 with unwrapped angles and an exact integer number of steps."""
    if not (np.isfinite(step) and step > 0 and np.isfinite(duration) and duration > 0):
        raise ValueError("duration and step must be finite and positive")
    count = round(duration / step)
    if count < 1 or not np.isclose(count * step, duration, rtol=0, atol=1e-10):
        raise ValueError("duration must be an integer multiple of step")
    times = np.linspace(0, duration, count + 1)
    states = np.empty((count + 1, len(initial)))
    states[0] = initial
    for i in range(count):
        t, y = times[i], states[i]
        k1 = rhs(t, y, p)
        k2 = rhs(t + step / 2, y + step * k1 / 2, p)
        k3 = rhs(t + step / 2, y + step * k2 / 2, p)
        k4 = rhs(t + step, y + step * k3, p)
        states[i + 1] = y + step * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    if not np.all(np.isfinite(states)):
        raise FloatingPointError("nonfinite trajectory")
    return times, states


def reference(rhs, initial, duration, p, *, rtol=1e-12, atol=1e-13, max_step=0.1,
              method="DOP853"):
    solution = solve_ivp(
        lambda t, y: rhs(t, y, p), (0, duration), initial,
        method=method, rtol=rtol, atol=atol, max_step=max_step, dense_output=True,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    return solution


def convergence_study():
    rows = []
    for name, p, rhs, initial in [
        ("drifting", Parameters(epsilon=0.1), phase_rhs, [0.2, 0.9]),
        ("locked", Parameters(epsilon=0.6), phase_rhs, [0.2, 0.9]),
        ("radial", Parameters(), amplitude_rhs, [0.2, 0.9, 0.7, 1.3]),
        ("forced_radial", Parameters(radial_forcing=0.1), amplitude_rhs,
         [0.2, 0.9, 0.7, 1.3]),
    ]:
        ref = reference(rhs, initial, 20.0, p)
        previous = None
        for step in (0.08, 0.04, 0.02, 0.01):
            t, state = rk4(rhs, initial, 20.0, step, p)
            exact = ref.sol(t).T
            # Same unwrapped lift and initial condition: valid at finite horizon.
            error = float(np.max(np.abs(state - exact)))
            order = None if previous is None else float(np.log2(previous / error))
            rows.append(dict(case=name, step=step, max_abs_error=error,
                             observed_order=order))
            previous = error
    return rows


def run_validation(output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    base = Parameters()
    initial = np.array([0.2, 0.9])
    phase_cases = {
        "independent_irrational": base,
        "independent_rational": replace(base, omega2=1.5),
        "coupled_drifting": replace(base, epsilon=0.1),
        "synchronized": replace(base, epsilon=0.6),
    }
    phase_runs = {}
    for name, p in phase_cases.items():
        t, state = rk4(phase_rhs, initial, 200.0, 0.02, p)
        phase_runs[name] = state
        np.savetxt(output_dir / f"{name}.csv", np.c_[t, state], delimiter=",",
                   header="time,phi1_unwrapped,phi2_unwrapped", comments="")

    # Exact benchmark for independent rotations, including a rational return.
    analytic = initial + t[:, None] * [base.omega1, base.omega2]
    independent_error = float(np.max(np.abs(
        phase_runs["independent_irrational"] - analytic)))
    rational = phase_cases["independent_rational"]
    return_phase = initial + 4 * np.pi * np.array([rational.omega1, rational.omega2])
    rational_return = float(phase_distance(return_phase, initial))

    # Initial-condition kicks distinguish neutral phase directions from locking.
    kick = np.array([0.0, 0.2])
    _, independent_kick = rk4(phase_rhs, initial + kick, 200.0, 0.02, base)
    neutral_distance = phase_distance(independent_kick,
                                      phase_runs["independent_irrational"])
    locked = phase_cases["synchronized"]
    star, exponent = locked_solution(locked)
    small_initial = np.array([0.0, star + 1e-4])
    local_t, local_state = rk4(phase_rhs, small_initial, 6.0, 0.01, locked)
    local_error = np.abs(local_state[:, 1] - local_state[:, 0] - star)
    fitted_exponent = float(np.polyfit(local_t, np.log(local_error), 1)[0])
    _, kicked_locked = rk4(phase_rhs, initial + kick, 200.0, 0.02, locked)
    locked_state = phase_runs["synchronized"]
    common_offset = np.mean(kicked_locked - locked_state, axis=1)
    locked_delta_error = float(abs(np.arctan2(
        np.sin(locked_state[-1, 1] - locked_state[-1, 0] - star),
        np.cos(locked_state[-1, 1] - locked_state[-1, 0] - star))))

    # In the drifting case measure full slip periods, avoiding endpoint bias.
    drifting = phase_cases["coupled_drifting"]
    detuning = drifting.omega2 - drifting.omega1
    predicted_slip = np.sqrt(detuning**2 - (2 * drifting.epsilon)**2)
    period_quad, _ = quad(lambda d: 1 / (detuning - 2 * drifting.epsilon * np.sin(d)),
                          0, 2 * np.pi, epsabs=1e-11, epsrel=1e-11)
    slip_ref = reference(phase_rhs, initial, 200.0, drifting)
    delta0 = initial[1] - initial[0]
    delta_end = np.diff(slip_ref.y[:, -1])[0]
    targets = delta0 + 2 * np.pi * np.arange(1, int((delta_end - delta0) / (2*np.pi)) + 1)
    crossings = [brentq(lambda u: float(np.diff(slip_ref.sol(u))[0] - target),
                        0, 200, xtol=1e-11) for target in targets]
    measured_slip = float(2 * np.pi / np.mean(np.diff(crossings)))

    radial_runs = {}
    radial_metrics = {}
    for name, p in [("attracting_torus", base),
                    ("attracting_torus_with_locking", locked),
                    ("deformed_attracting_torus", replace(base, radial_forcing=0.1))]:
        r_initial = np.array([0.7, 1.3])
        r_t, state = rk4(amplitude_rhs, np.r_[initial, r_initial], 20.0, 0.02, p)
        graph = (forced_radius_graph(state[:, :2], p) if p.radial_forcing
                 else np.ones_like(state[:, :2]))
        residual = state[:, 2:] - graph
        initial_graph = forced_radius_graph(initial, p) if p.radial_forcing else np.ones(2)
        exact_residual = (r_initial - initial_graph)[None, :] * np.exp(
            -p.radial_rate * r_t[:, None])
        radial_runs[name] = (r_t, state, residual)
        radial_metrics[name] = {
            "parameters": asdict(p),
            "max_graph_residual_error": float(np.max(np.abs(residual - exact_residual))),
            "minimum_radius": float(state[:, 2:].min()),
        }
        np.savetxt(output_dir / f"{name}.csv", np.c_[r_t, state, residual], delimiter=",",
                   header="time,phi1_unwrapped,phi2_unwrapped,r1,r2,graph_error1,graph_error2",
                   comments="")

    # Identical flow on the unit torus can have attracting or repelling normals.
    sign_t = np.linspace(0, 3, 301)
    sign_columns = [sign_t]
    for rate in (2.0, 0.0, -2.0):
        p = replace(base, radial_rate=rate)
        sol = reference(amplitude_rhs, [0.2, 0.9, 1.001, 0.999], 3, p)
        normal_size = np.linalg.norm(sol.sol(sign_t).T[:, 2:] - 1, axis=1)
        sign_columns.append(normal_size)
    np.savetxt(output_dir / "normal_sign_controls.csv", np.column_stack(sign_columns),
               delimiter=",", header="time,normal_size_attracting,normal_size_neutral,normal_size_repelling",
               comments="")

    convergence = convergence_study()
    with (output_dir / "convergence.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=convergence[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(convergence)

    # Independent adaptive solvers and tighter tolerances, evaluated at common times.
    sample_times = np.linspace(0, 20, 1001)
    strict = reference(phase_rhs, initial, 20, locked, rtol=3e-14, atol=1e-14,
                       max_step=0.05).sol(sample_times)
    standard = reference(phase_rhs, initial, 20, locked).sol(sample_times)
    alternate = reference(phase_rhs, initial, 20, locked, method="RK45").sol(sample_times)

    # Exact threshold versus finite observation. A near-critical drift is slow.
    critical = abs(detuning) / 2
    threshold_rows = []
    for factor in (0.99, 1.0, 1.01):
        p = replace(base, epsilon=factor * critical)
        sol = reference(phase_rhs, [0.0, 0.0], 200, p)
        for horizon in (40.0, 200.0):
            phase = sol.sol(horizon)
            delta = float(phase[1] - phase[0])
            threshold_rows.append(dict(
                epsilon_factor=factor, horizon=horizon, delta_unwrapped=delta,
                instantaneous_delta_speed=float(detuning - 2*p.epsilon*np.sin(delta)),
                analytical_regime=("drift" if factor < 1 else "nonhyperbolic_threshold"
                                   if factor == 1 else "locked")))
    with (output_dir / "threshold.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=threshold_rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(threshold_rows)

    summary = {
        "kind": "synthetic mathematical validation, not biological evidence",
        "phase_cases": {name: asdict(p) for name, p in phase_cases.items()},
        "phase_initial": initial.tolist(), "duration": 200.0, "rk4_step": 0.02,
        "independent_max_unwrapped_error": independent_error,
        "rational_exact_return_distance_at_4pi": rational_return,
        "independent_kick_distance_range": [float(neutral_distance.min()),
                                             float(neutral_distance.max())],
        "locked_phase_difference": star, "locked_exponent_exact": exponent,
        "locked_exponent_finite_fit": fitted_exponent,
        "locked_final_phase_difference_error": locked_delta_error,
        "locked_common_phase_offset_after_kick": float(common_offset[-1]),
        "drift_mean_slip_exact": float(predicted_slip),
        "drift_mean_slip_quadrature": float(2*np.pi/period_quad),
        "drift_mean_slip_measured_full_cycles": measured_slip,
        "drift_full_cycle_crossings": len(crossings),
        "radial": radial_metrics,
        "adaptive_tolerance_difference": float(np.max(np.abs(standard - strict))),
        "adaptive_method_difference": float(np.max(np.abs(alternate - strict))),
        "convergence": convergence,
        "limitations": [
            "Finite trajectories cannot prove density, irrationality, or general persistence.",
            "sqrt(2) is an exact model assumption, represented approximately in floating point.",
            "Critical locking has zero linear exponent; finite slow drift can look locked.",
            "Return to a manifold or orbit does not imply return to the same timed phase.",
            "The forced radial example has an exact graph and does not validate generic perturbations.",
            "No PH recovery, neural fit, stochastic noise test, or thermodynamic measurement is made.",
        ],
        "environment": {"python": platform.python_version(), **{
            name: importlib.metadata.version(name) for name in ("numpy", "scipy", "matplotlib")}},
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import NullFormatter
    fig, axes = plt.subplots(2, 3, figsize=(12, 7.1), constrained_layout=True)
    for ax, (name, title) in zip(axes[0], [
        ("independent_irrational", "A  Independent rotations"),
        ("independent_rational", "B  Rational rotation ratio"),
        ("synchronized", "C  Phase locking"),
    ]):
        state = phase_runs[name][::5]
        ax.scatter(state[:, 0] % (2*np.pi), state[:, 1] % (2*np.pi), s=1,
                   alpha=0.55, color="#087e8b", rasterized=True)
        ax.set(xlabel=r"$\phi_1\;\mathrm{mod}\;2\pi$", ylabel=r"$\phi_2\;\mathrm{mod}\;2\pi$",
               xlim=(0, 2*np.pi), ylim=(0, 2*np.pi), title=title)
    ax = axes[1, 0]
    ax.plot(t[t <= 30], neutral_distance[t <= 30], label="Independent: phase kick")
    ax.semilogy(local_t, local_error, label="Locked: phase difference error")
    ax.set(xlabel="Model time", ylabel="Circular distance / local error (rad)",
           title="D  Neutral and contracting directions")
    ax.legend(fontsize=8)
    ax = axes[1, 1]
    for name, label in [("attracting_torus", "Unit torus"),
                        ("deformed_attracting_torus", "Forced invariant graph")]:
        rt, _, residual = radial_runs[name]
        norm = np.linalg.norm(residual, axis=1)
        mask = (norm > 1e-9) & (rt <= 8)
        ax.semilogy(rt[mask], norm[mask], label=label)
    rt = radial_runs["attracting_torus"][0]
    ax.semilogy(rt[rt <= 8], np.sqrt(0.18)*np.exp(-2*rt[rt <= 8]), "k--",
                label=r"Exact $\|r(0)-1\|e^{-2t}$")
    ax.set(xlabel="Model time", ylabel="Normal displacement", title="E  Explicit normal attraction")
    ax.legend(fontsize=8)
    ax = axes[1, 2]
    for case in ("drifting", "locked", "radial", "forced_radial"):
        items = [row for row in convergence if row["case"] == case]
        ax.loglog([row["step"] for row in items], [row["max_abs_error"] for row in items],
                  "o-", label=case.replace("_", " "))
    ax.set(xlabel="RK4 step", ylabel="Maximum absolute error", title="F  Step refinement, time 0 to 20")
    ax.set_xticks([0.01, 0.02, 0.04, 0.08], labels=["0.01", "0.02", "0.04", "0.08"])
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.legend(fontsize=8)
    fig.suptitle("Synthetic oscillator validation in arbitrary model units", fontsize=14)
    fig.savefig(output_dir / "oscillator_validation.png", dpi=170)
    plt.close(fig)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parents[1] / "outputs" / "oscillator_validation")
    args = parser.parse_args()
    results = run_validation(args.output_dir)
    print(json.dumps({key: results[key] for key in (
        "kind", "locked_phase_difference", "locked_exponent_exact",
        "drift_mean_slip_measured_full_cycles", "adaptive_tolerance_difference")}, indent=2))
