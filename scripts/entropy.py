"""
Descriptive Shannon entropies of explicitly normalized nonnegative weights.
These are activity-share, spatial-rate, and time-window allocation statistics,
not joint population entropy, entropy rates, or thermodynamic entropy.
Exports results to CSV.

Author: Christopher Ezernack
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
from preprocessing import analysis_context, build_activity_matrix


def weight_entropy(weights, axis=-1):
    """Shannon entropy in bits; zero total mass is undefined (NaN).

    Zero probabilities contribute exactly zero. Scaling by the largest weight
    before summing avoids overflow for otherwise finite input weights.
    """
    values = np.asarray(weights, dtype=float)
    if values.ndim == 0 or not np.all(np.isfinite(values)) or np.any(values < 0):
        raise ValueError("weights must be an array of finite nonnegative values")
    largest = np.max(values, axis=axis, keepdims=True, initial=0)
    scaled = np.divide(values, largest, out=np.zeros_like(values), where=largest > 0)
    total = scaled.sum(axis=axis, keepdims=True)
    probabilities = np.divide(scaled, total, out=np.zeros_like(scaled), where=total > 0)
    logs = np.zeros_like(probabilities)
    np.log2(probabilities, out=logs, where=probabilities > 0)
    result = -np.sum(probabilities * logs, axis=axis)
    return np.where(np.squeeze(total, axis=axis) > 0, result, np.nan)


def neural_entropy(activity):
    """Entropy of neuron activity shares per time bin; silent bins are NaN.

    The neuron label is the categorical variable, conditional on positive total
    activity. This is not the entropy of the joint population random process.
    """
    activity = np.asarray(activity, dtype=float)
    if activity.ndim != 2:
        raise ValueError("activity must have shape (timepoints, neurons)")
    return weight_entropy(activity, axis=1)


def spatial_entropy(rate_map):
    """
    Compute spatial entropy of a single neuron's rate map.
    Measures how uniformly the neuron fires across spatial bins.
    rate_map: 2D array (nx, ny) of firing rates.
    Returns: scalar entropy value.
    """
    # NaN marks unobserved spatial bins; it is not a zero-rate measurement.
    flat = np.asarray(rate_map, dtype=float).ravel()
    return float(weight_entropy(flat[~np.isnan(flat)]))


def temporal_entropy(spike_train, n_bins=100):
    """
    Entropy of activity mass allocated to contiguous time windows, in bits.

    Input samples must be equally spaced counts or rates with a common bin
    width. Split into min(n_bins, sample_count) nonempty windows whose sample
    counts differ by at most one. Every sample is used exactly once. This is
    not an entropy rate, count-histogram entropy, or information-persistence
    measure: permuting complete windows leaves it unchanged. No activity gives
    NaN because the normalized allocation distribution is undefined.
    """
    values = np.asarray(spike_train, dtype=float)
    if values.ndim != 1 or not np.all(np.isfinite(values)) or np.any(values < 0):
        raise ValueError("spike_train must be a finite nonnegative 1D array")
    if isinstance(n_bins, (bool, np.bool_)) or not isinstance(n_bins, (int, np.integer)) or n_bins < 1:
        raise ValueError("n_bins must be a positive integer")
    if values.size == 0 or values.max() == 0:
        return float("nan")
    scaled = values / values.max()
    windows = np.array_split(scaled, min(n_bins, len(scaled)))
    return float(weight_entropy([window.sum() for window in windows]))


def activity_entropy_summary(neural_H):
    """Summaries conditional on defined bins, with the denominator reported."""
    values = np.asarray(neural_H, dtype=float)
    valid = values[np.isfinite(values)]
    stats = {"total_time_bins": values.size, "defined_time_bins": valid.size,
             "undefined_time_bins": values.size - valid.size}
    for name, function in (("mean", np.mean), ("std", np.std), ("min", np.min),
                           ("max", np.max), ("median", np.median)):
        stats[f"{name}_neural_entropy"] = float(function(valid)) if valid.size else float("nan")
    return stats


def save_entropy_results(neural_H, spatial_H_dict, temporal_H_dict,
                         neuron_ids, out_dir):
    """Save all entropy metrics to CSV and figures."""
    os.makedirs(out_dir, exist_ok=True)

    with open(os.path.join(out_dir, "entropy_metrics.csv"), "w") as f:
        f.write("neuron_id,spatial_entropy,temporal_entropy,"
                "mean_neural_entropy\n")
        summary = activity_entropy_summary(neural_H)
        mean_neural = summary["mean_neural_entropy"]
        for nid in neuron_ids:
            sp = spatial_H_dict.get(nid, np.nan)
            tp = temporal_H_dict.get(nid, np.nan)
            f.write(f"{nid},{sp:.6f},{tp:.6f},{mean_neural:.6f}\n")

    np.save(os.path.join(out_dir, "neural_entropy_timeseries.npy"), neural_H)

    with open(os.path.join(out_dir, "neural_entropy_summary.csv"), "w") as f:
        f.write("metric,value\n")
        for metric, value in summary.items():
            f.write(f"{metric},{value}\n")

    fig, ax = plt.subplots(figsize=(10, 3))
    step = max(1, len(neural_H) // 5000)
    ax.plot(np.arange(0, len(neural_H), step) * 0.02,
            neural_H[::step], linewidth=0.5, color="steelblue")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Activity-share entropy (bits)")
    ax.set_title("Neuron Activity Shares; Silent Bins Undefined")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "neural_entropy_timeseries.png"),
                dpi=150, bbox_inches="tight")
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    nids = sorted(spatial_H_dict.keys())
    sp_vals = [spatial_H_dict[n] for n in nids]
    axes[0].barh(range(len(nids)), sp_vals, color="coral")
    axes[0].set_yticks(range(len(nids)))
    axes[0].set_yticklabels(nids, fontsize=7)
    axes[0].set_xlabel("Spatial Entropy (bits)")
    axes[0].set_title("Spatial Entropy per Neuron")

    tp_vals = [temporal_H_dict[n] for n in nids]
    axes[1].barh(range(len(nids)), tp_vals, color="mediumpurple")
    axes[1].set_yticks(range(len(nids)))
    axes[1].set_yticklabels(nids, fontsize=7)
    axes[1].set_xlabel("Time-window allocation entropy (bits)")
    axes[1].set_title("Activity Allocation per Neuron")

    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "entropy_per_neuron.png"),
                dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    sessions, out_root = analysis_context()
    out_dir = os.path.join(out_root, "entropy")
    rate_map_dir = os.path.join(out_root, "rate_maps")
    activity, neuron_ids, time_bins = build_activity_matrix(sessions)

    print("Computing neural entropy...")
    neural_H = neural_entropy(activity)
    print(f"  Activity-share summary: {activity_entropy_summary(neural_H)}")

    print("\nComputing spatial entropy from rate maps...")
    spatial_H_dict = {}
    for nid in neuron_ids:
        rm_path = os.path.join(rate_map_dir, f"rate_map_{nid}.npy")
        if os.path.exists(rm_path):
            rm = np.load(rm_path)
            spatial_H_dict[nid] = spatial_entropy(rm)
            print(f"  {nid}: spatial_H = {spatial_H_dict[nid]:.4f} bits")
        else:
            spatial_H_dict[nid] = np.nan
            print(f"  {nid}: rate map not found, spatial_H = undefined")

    print("\nComputing temporal entropy...")
    temporal_H_dict = {}
    for i, nid in enumerate(neuron_ids):
        spike_train = activity[:, i]
        temporal_H_dict[nid] = temporal_entropy(spike_train, n_bins=100)
        print(f"  {nid}: temporal_H = {temporal_H_dict[nid]:.4f} bits")

    save_entropy_results(neural_H, spatial_H_dict, temporal_H_dict,
                         neuron_ids, out_dir)
    print("\nAll entropy outputs saved.")
