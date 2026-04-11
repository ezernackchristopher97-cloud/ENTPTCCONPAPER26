"""
Rate map construction for grid cell data.
Computes occupancy-normalized, Gaussian-smoothed firing rate maps
for each neuron. Outputs npy, csv, and png per neuron.

Author: Christopher Ezernack
"""

import os
import sys
import numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
from preprocessing import load_all_data


def compute_rate_map(spike_x, spike_y, pos_x, pos_y, pos_ts,
                     n_bins=50, sigma=2.0):
    """
    Compute an occupancy-normalized, Gaussian-smoothed firing rate map.

    Parameters:
        spike_x, spike_y: 1D arrays of spike positions
        pos_x, pos_y: 1D arrays of all position samples
        pos_ts: 1D array of position timestamps (for computing dt)
        n_bins: number of spatial bins per dimension
        sigma: Gaussian smoothing kernel width in bins

    Returns:
        rate_map: 2D array (n_bins, n_bins) of firing rates in Hz
        x_edges, y_edges: bin edge arrays
    """
    x_min, x_max = np.nanmin(pos_x), np.nanmax(pos_x)
    y_min, y_max = np.nanmin(pos_y), np.nanmax(pos_y)

    x_edges = np.linspace(x_min, x_max, n_bins + 1)
    y_edges = np.linspace(y_min, y_max, n_bins + 1)

    dt = np.median(np.diff(pos_ts))

    spike_map, _, _ = np.histogram2d(spike_x, spike_y,
                                     bins=[x_edges, y_edges])

    occupancy, _, _ = np.histogram2d(pos_x, pos_y,
                                     bins=[x_edges, y_edges])
    occupancy_time = occupancy * dt

    spike_map_smooth = gaussian_filter(spike_map.astype(float), sigma=sigma)
    occupancy_smooth = gaussian_filter(occupancy_time, sigma=sigma)

    min_occ = 0.01
    rate_map = np.zeros_like(spike_map_smooth)
    valid = occupancy_smooth > min_occ
    rate_map[valid] = spike_map_smooth[valid] / occupancy_smooth[valid]
    rate_map[~valid] = np.nan

    return rate_map, x_edges, y_edges


def save_rate_map(rate_map, neuron_id, out_dir, x_edges, y_edges):
    """Save rate map as npy, csv, and png."""
    base = os.path.join(out_dir, f"rate_map_{neuron_id}")

    np.save(f"{base}.npy", rate_map)

    np.savetxt(f"{base}.csv", rate_map, delimiter=",",
               fmt="%.4f", comments="")

    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    masked = np.ma.masked_invalid(rate_map.T)
    im = ax.pcolormesh(x_edges, y_edges, masked,
                       cmap="jet", shading="flat")
    ax.set_aspect("equal")
    ax.set_xlabel("X position (cm)")
    ax.set_ylabel("Y position (cm)")
    ax.set_title(f"Rate Map: {neuron_id}")
    plt.colorbar(im, ax=ax, label="Firing rate (Hz)")
    plt.tight_layout()
    plt.savefig(f"{base}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def build_all_rate_maps(sessions, out_dir, n_bins=50, sigma=2.0):
    """Build and save rate maps for all neurons across all sessions."""
    os.makedirs(out_dir, exist_ok=True)
    all_maps = {}

    for sess in sessions:
        pos_ts = sess["pos_ts"]
        pos_x = sess["pos_x"]
        pos_y = sess["pos_y"]

        for nid, ndata in sess["neurons"].items():
            rate_map, x_edges, y_edges = compute_rate_map(
                ndata["spike_x"], ndata["spike_y"],
                pos_x, pos_y, pos_ts,
                n_bins=n_bins, sigma=sigma
            )
            save_rate_map(rate_map, nid, out_dir, x_edges, y_edges)
            all_maps[nid] = rate_map
            print(f"  Rate map saved for {nid}: "
                  f"peak={np.nanmax(rate_map):.1f} Hz, "
                  f"mean={np.nanmean(rate_map):.1f} Hz")

    return all_maps


def build_rate_maps_flat_csv(all_maps, out_dir):
    """Save a flat CSV with all rate maps (one row per neuron)."""
    neuron_ids = sorted(all_maps.keys())
    n_bins = list(all_maps.values())[0].shape[0]
    flat = np.zeros((len(neuron_ids), n_bins * n_bins))
    for i, nid in enumerate(neuron_ids):
        rm = all_maps[nid].copy()
        rm[np.isnan(rm)] = 0.0
        flat[i] = rm.flatten()

    header = ",".join([f"bin_{j}" for j in range(n_bins * n_bins)])
    rows = []
    for i, nid in enumerate(neuron_ids):
        rows.append(f"{nid}," + ",".join(f"{v:.4f}" for v in flat[i]))

    with open(os.path.join(out_dir, "..", "rate_maps_flat.csv"), "w") as f:
        f.write("neuron_id," + header + "\n")
        for row in rows:
            f.write(row + "\n")

    print(f"Saved rate_maps_flat.csv ({len(neuron_ids)} neurons)")


if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    out_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "rate_maps")

    sessions = load_all_data(data_dir)
    print(f"\nBuilding rate maps...")
    all_maps = build_all_rate_maps(sessions, out_dir)
    build_rate_maps_flat_csv(all_maps, out_dir)
    print(f"\nDone. {len(all_maps)} rate maps generated.")
