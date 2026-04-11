"""
Ablation studies for grid cell analysis pipeline.
Compares: (1) no smoothing, (2) reduced neurons, (3) randomized spikes.
Outputs comparison CSVs and figures.

Author: Christopher Ezernack
"""

import os
import sys
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.ndimage import gaussian_filter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
from preprocessing import load_all_data, build_activity_matrix
from entropy import neural_entropy


def ablation_no_smoothing(sessions, out_dir):
    """
    Ablation 1: Build rate maps without Gaussian smoothing.
    Compare spatial structure to smoothed maps.
    """
    print("\n--- Ablation 1: No Smoothing ---")
    rm_dir = os.path.join(out_dir, "no_smoothing")
    os.makedirs(rm_dir, exist_ok=True)

    session = sessions[0]
    pos_x = session["pos_x"]
    pos_y = session["pos_y"]
    pos_t = session["pos_ts"]

    x_range = (np.nanmin(pos_x), np.nanmax(pos_x))
    y_range = (np.nanmin(pos_y), np.nanmax(pos_y))
    n_bins = 50
    dt = np.median(np.diff(pos_t))

    results = []
    for nid, ndata in session["neurons"].items():
        spike_x = ndata["spike_x"]
        spike_y = ndata["spike_y"]

        occupancy, xedges, yedges = np.histogram2d(
            pos_x, pos_y, bins=n_bins, range=[x_range, y_range])
        spike_count, _, _ = np.histogram2d(
            spike_x, spike_y, bins=n_bins, range=[x_range, y_range])

        occupancy_time = occupancy * dt
        occupancy_time[occupancy_time == 0] = np.nan

        rate_map_raw = spike_count / occupancy_time
        rate_map_raw = np.nan_to_num(rate_map_raw, nan=0.0)

        rate_map_smooth = gaussian_filter(rate_map_raw, sigma=2.0)

        peak_raw = np.max(rate_map_raw)
        peak_smooth = np.max(rate_map_smooth)
        results.append({
            "neuron": nid,
            "peak_raw": peak_raw,
            "peak_smooth": peak_smooth,
            "ratio": peak_raw / max(peak_smooth, 1e-6)
        })

        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        axes[0].imshow(rate_map_raw.T, origin="lower", cmap="hot",
                       aspect="equal")
        axes[0].set_title(f"{nid}: No Smoothing")
        axes[1].imshow(rate_map_smooth.T, origin="lower", cmap="hot",
                       aspect="equal")
        axes[1].set_title(f"{nid}: Gaussian Smoothed")
        plt.tight_layout()
        plt.savefig(os.path.join(rm_dir, f"compare_{nid}.png"),
                    dpi=100, bbox_inches="tight")
        plt.close(fig)
        break  # One example is sufficient

    with open(os.path.join(rm_dir, "smoothing_comparison.csv"), "w") as f:
        f.write("neuron,peak_raw_hz,peak_smooth_hz,ratio\n")
        for r in results:
            f.write(f"{r['neuron']},{r['peak_raw']:.4f},"
                    f"{r['peak_smooth']:.4f},{r['ratio']:.4f}\n")

    print(f"  Saved to {rm_dir}")
    return results


def ablation_reduced_neurons(activity, neuron_ids, out_dir):
    """
    Ablation 2: Use only a subset of neurons and compare PCA variance.
    """
    print("\n--- Ablation 2: Reduced Neurons ---")
    rd_dir = os.path.join(out_dir, "reduced_neurons")
    os.makedirs(rd_dir, exist_ok=True)

    n_neurons = activity.shape[1]
    subsets = [3, 5, 7, 10, n_neurons]
    subsets = [s for s in subsets if s <= n_neurons]

    results = []
    for n in subsets:
        sub = activity[:, :n]
        scaler = StandardScaler()
        scaled = scaler.fit_transform(sub)
        n_comp = min(3, n)
        pca = PCA(n_components=n_comp)
        pca.fit(scaled)
        var3 = np.sum(pca.explained_variance_ratio_[:n_comp])
        results.append({
            "n_neurons": n,
            "cumulative_var_3pc": var3,
            "pc1_var": pca.explained_variance_ratio_[0]
        })
        print(f"  {n} neurons: cumulative var (top {n_comp} PCs) = {var3:.4f}")

    with open(os.path.join(rd_dir, "reduced_neurons_comparison.csv"), "w") as f:
        f.write("n_neurons,cumulative_var_3pc,pc1_var\n")
        for r in results:
            f.write(f"{r['n_neurons']},{r['cumulative_var_3pc']:.6f},"
                    f"{r['pc1_var']:.6f}\n")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot([r["n_neurons"] for r in results],
            [r["cumulative_var_3pc"] for r in results],
            "o-", color="steelblue")
    ax.set_xlabel("Number of Neurons")
    ax.set_ylabel("Cumulative Variance (top 3 PCs)")
    ax.set_title("PCA Variance vs. Neuron Count")
    plt.tight_layout()
    plt.savefig(os.path.join(rd_dir, "reduced_neurons_pca.png"),
                dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"  Saved to {rd_dir}")
    return results


def ablation_randomized_spikes(activity, neuron_ids, out_dir):
    """
    Ablation 3: Shuffle spike times and compare manifold structure.
    """
    print("\n--- Ablation 3: Randomized Spikes ---")
    rs_dir = os.path.join(out_dir, "randomized_spikes")
    os.makedirs(rs_dir, exist_ok=True)

    rng = np.random.RandomState(42)
    shuffled = activity.copy()
    for col in range(shuffled.shape[1]):
        rng.shuffle(shuffled[:, col])

    scaler = StandardScaler()

    real_scaled = scaler.fit_transform(activity)
    pca_real = PCA(n_components=3)
    emb_real = pca_real.fit_transform(real_scaled)

    shuf_scaled = scaler.fit_transform(shuffled)
    pca_shuf = PCA(n_components=3)
    emb_shuf = pca_shuf.fit_transform(shuf_scaled)

    H_real = neural_entropy(activity)
    H_shuf = neural_entropy(shuffled)

    results = {
        "real_var3": np.sum(pca_real.explained_variance_ratio_[:3]),
        "shuf_var3": np.sum(pca_shuf.explained_variance_ratio_[:3]),
        "real_mean_entropy": np.mean(H_real),
        "shuf_mean_entropy": np.mean(H_shuf),
    }

    with open(os.path.join(rs_dir, "randomized_comparison.csv"), "w") as f:
        f.write("metric,real,shuffled\n")
        f.write(f"cumulative_var_3pc,{results['real_var3']:.6f},"
                f"{results['shuf_var3']:.6f}\n")
        f.write(f"mean_neural_entropy,{results['real_mean_entropy']:.6f},"
                f"{results['shuf_mean_entropy']:.6f}\n")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    step = max(1, len(emb_real) // 5000)
    axes[0].scatter(emb_real[::step, 0], emb_real[::step, 1],
                    c=np.arange(0, len(emb_real), step), cmap="viridis",
                    s=1, alpha=0.5)
    axes[0].set_xlabel("PC1")
    axes[0].set_ylabel("PC2")
    axes[0].set_title(f"Real Data (var={results['real_var3']:.3f})")

    axes[1].scatter(emb_shuf[::step, 0], emb_shuf[::step, 1],
                    c=np.arange(0, len(emb_shuf), step), cmap="viridis",
                    s=1, alpha=0.5)
    axes[1].set_xlabel("PC1")
    axes[1].set_ylabel("PC2")
    axes[1].set_title(f"Shuffled Data (var={results['shuf_var3']:.3f})")

    plt.tight_layout()
    plt.savefig(os.path.join(rs_dir, "real_vs_shuffled_pca.png"),
                dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"  Real var (3 PCs): {results['real_var3']:.4f}")
    print(f"  Shuffled var (3 PCs): {results['shuf_var3']:.4f}")
    print(f"  Real mean entropy: {results['real_mean_entropy']:.4f}")
    print(f"  Shuffled mean entropy: {results['shuf_mean_entropy']:.4f}")
    print(f"  Saved to {rs_dir}")
    return results


if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    out_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "ablation")

    sessions = load_all_data(data_dir)
    activity, neuron_ids, time_bins = build_activity_matrix(sessions)

    ablation_no_smoothing(sessions, out_dir)
    ablation_reduced_neurons(activity, neuron_ids, out_dir)
    ablation_randomized_spikes(activity, neuron_ids, out_dir)

    print("\nAll ablation studies complete.")
