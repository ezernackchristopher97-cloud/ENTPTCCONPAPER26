"""
Entropy metrics for grid cell population activity.
Computes neural entropy, spatial entropy, and temporal entropy.
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
from preprocessing import load_all_data, build_activity_matrix


def neural_entropy(activity):
    """
    Compute neural entropy for each time bin.
    For each time bin, normalize the population vector to a probability
    distribution and compute Shannon entropy.
    activity: (timepoints, neurons)
    Returns: (timepoints,) array of entropy values.
    """
    eps = 1e-12
    row_sums = activity.sum(axis=1, keepdims=True)
    row_sums = np.where(row_sums == 0, 1.0, row_sums)
    p = activity / row_sums
    p = np.clip(p, eps, 1.0)
    H = -np.sum(p * np.log2(p), axis=1)
    return H


def spatial_entropy(rate_map):
    """
    Compute spatial entropy of a single neuron's rate map.
    Measures how uniformly the neuron fires across spatial bins.
    rate_map: 2D array (nx, ny) of firing rates.
    Returns: scalar entropy value.
    """
    eps = 1e-12
    flat = rate_map.flatten()
    flat = flat[flat > 0]
    if len(flat) == 0:
        return 0.0
    total = flat.sum()
    p = flat / total
    p = np.clip(p, eps, 1.0)
    H = -np.sum(p * np.log2(p))
    return H


def temporal_entropy(spike_train, n_bins=100):
    """
    Compute temporal entropy of a single neuron's spike train.
    Divides the recording into n_bins time windows and computes
    Shannon entropy of the spike count distribution.
    spike_train: 1D array of spike counts per time bin.
    Returns: scalar entropy value.
    """
    eps = 1e-12
    n = len(spike_train)
    if n == 0:
        return 0.0

    bin_size = max(1, n // n_bins)
    binned = []
    for i in range(0, n, bin_size):
        binned.append(spike_train[i:i+bin_size].sum())
    binned = np.array(binned)

    total = binned.sum()
    if total == 0:
        return 0.0
    p = binned / total
    p = np.clip(p, eps, 1.0)
    H = -np.sum(p * np.log2(p))
    return H


def save_entropy_results(neural_H, spatial_H_dict, temporal_H_dict,
                         neuron_ids, out_dir):
    """Save all entropy metrics to CSV and figures."""
    os.makedirs(out_dir, exist_ok=True)

    with open(os.path.join(out_dir, "entropy_metrics.csv"), "w") as f:
        f.write("neuron_id,spatial_entropy,temporal_entropy,"
                "mean_neural_entropy\n")
        mean_neural = float(np.mean(neural_H))
        for nid in neuron_ids:
            sp = spatial_H_dict.get(nid, 0.0)
            tp = temporal_H_dict.get(nid, 0.0)
            f.write(f"{nid},{sp:.6f},{tp:.6f},{mean_neural:.6f}\n")

    np.save(os.path.join(out_dir, "neural_entropy_timeseries.npy"), neural_H)

    with open(os.path.join(out_dir, "neural_entropy_summary.csv"), "w") as f:
        f.write("metric,value\n")
        f.write(f"mean_neural_entropy,{np.mean(neural_H):.6f}\n")
        f.write(f"std_neural_entropy,{np.std(neural_H):.6f}\n")
        f.write(f"min_neural_entropy,{np.min(neural_H):.6f}\n")
        f.write(f"max_neural_entropy,{np.max(neural_H):.6f}\n")
        f.write(f"median_neural_entropy,{np.median(neural_H):.6f}\n")

    fig, ax = plt.subplots(figsize=(10, 3))
    step = max(1, len(neural_H) // 5000)
    ax.plot(np.arange(0, len(neural_H), step) * 0.02,
            neural_H[::step], linewidth=0.5, color="steelblue")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Neural Entropy (bits)")
    ax.set_title("Population Neural Entropy Over Time")
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
    axes[1].set_xlabel("Temporal Entropy (bits)")
    axes[1].set_title("Temporal Entropy per Neuron")

    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "entropy_per_neuron.png"),
                dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    out_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "entropy")
    rate_map_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "rate_maps")

    sessions = load_all_data(data_dir)
    activity, neuron_ids, time_bins = build_activity_matrix(sessions)

    print("Computing neural entropy...")
    neural_H = neural_entropy(activity)
    print(f"  Mean neural entropy: {np.mean(neural_H):.4f} bits")
    print(f"  Std neural entropy: {np.std(neural_H):.4f} bits")

    print("\nComputing spatial entropy from rate maps...")
    spatial_H_dict = {}
    for nid in neuron_ids:
        rm_path = os.path.join(rate_map_dir, f"rate_map_{nid}.npy")
        if os.path.exists(rm_path):
            rm = np.load(rm_path)
            spatial_H_dict[nid] = spatial_entropy(rm)
            print(f"  {nid}: spatial_H = {spatial_H_dict[nid]:.4f} bits")
        else:
            spatial_H_dict[nid] = 0.0
            print(f"  {nid}: rate map not found, spatial_H = 0.0")

    print("\nComputing temporal entropy...")
    temporal_H_dict = {}
    for i, nid in enumerate(neuron_ids):
        spike_train = activity[:, i]
        temporal_H_dict[nid] = temporal_entropy(spike_train, n_bins=100)
        print(f"  {nid}: temporal_H = {temporal_H_dict[nid]:.4f} bits")

    save_entropy_results(neural_H, spatial_H_dict, temporal_H_dict,
                         neuron_ids, out_dir)
    print("\nAll entropy outputs saved.")
