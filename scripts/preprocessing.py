"""
Preprocessing module for Hafting et al. (2005) grid cell data.
Loads MAT files, extracts position and spike timestamps,
flattens arrays, removes NaNs, and aligns spikes to position.

Author: Christopher Ezernack
"""

import os
import argparse
from pathlib import Path
import numpy as np
import scipy.io as sio


def load_mat_file(filepath):
    """Load a single MAT file and return the raw dictionary."""
    return sio.loadmat(filepath)


def extract_position(mat_data):
    """
    Extract position timestamps, x, and y from a MAT file dictionary.
    Flattens arrays and removes NaN entries.
    Returns (timestamps, x, y) as 1D arrays with NaNs removed.
    """
    ts = mat_data["pos_timeStamps"].flatten()
    x = mat_data["pos_x"].flatten()
    y = mat_data["pos_y"].flatten()

    if not (ts.shape == x.shape == y.shape):
        raise ValueError("Position timestamps and coordinates must have matching lengths")
    valid = np.isfinite(ts) & np.isfinite(x) & np.isfinite(y)
    return ts[valid], x[valid], y[valid]


def extract_spike_times(mat_data):
    """
    Extract spike timestamps for all neurons in a MAT file.
    Identifies neuron keys by looking for timestamp-like fields
    that are not position data.
    Returns a dict: {neuron_id: 1D array of spike times (NaN-free)}.
    """
    neurons = {}
    pos_keys = {"pos_timeStamps", "pos_x", "pos_y"}

    for key in mat_data:
        if key.startswith("__") or key in pos_keys:
            continue
        val = mat_data[key]
        if isinstance(val, np.ndarray) and val.dtype in [np.float64, np.float32]:
            spikes = val.flatten()
            spikes = spikes[np.isfinite(spikes)]
            neuron_id = key.replace("_timeStamps", "")
            neurons[neuron_id] = spikes

    return neurons


def align_spikes_to_position(pos_ts, spike_times):
    """
    For each spike, find the nearest position timestamp index.
    Returns an array of position indices corresponding to each spike.
    Only includes finite spikes within the position recording window. Exact
    halfway ties select the earlier sample. This nearest-sample assignment
    does not interpolate trajectories across missing tracking intervals.
    """
    pos_ts = np.asarray(pos_ts, dtype=float)
    spike_times = np.asarray(spike_times, dtype=float)
    if pos_ts.ndim != 1 or not len(pos_ts) or not np.all(np.isfinite(pos_ts)) or np.any(np.diff(pos_ts) <= 0):
        raise ValueError("Position timestamps must be finite and strictly increasing")
    if spike_times.ndim != 1:
        raise ValueError("Spike times must be a 1D array")
    mask = np.isfinite(spike_times) & (spike_times >= pos_ts[0]) & (spike_times <= pos_ts[-1])
    valid_spikes = spike_times[mask]
    right = np.clip(np.searchsorted(pos_ts, valid_spikes, side="left"), 0, len(pos_ts) - 1)
    left = np.maximum(right - 1, 0)
    indices = np.where(valid_spikes - pos_ts[left] <= pos_ts[right] - valid_spikes, left, right)
    return valid_spikes, indices


def load_all_data(data_dir):
    """
    Load all MAT files from data_dir.
    Returns a list of session dicts, each containing:
        - filename: source file name
        - pos_ts, pos_x, pos_y: cleaned position arrays
        - neurons: dict of {neuron_id: {spike_times, pos_indices}}
    """
    sessions = []

    for fname in sorted(os.listdir(data_dir)):
        if not fname.endswith(".mat"):
            continue

        filepath = os.path.join(data_dir, fname)
        mat_data = load_mat_file(filepath)

        pos_ts, pos_x, pos_y = extract_position(mat_data)
        raw_neurons = extract_spike_times(mat_data)

        neurons = {}
        for nid, spk in raw_neurons.items():
            valid_spikes, pos_idx = align_spikes_to_position(pos_ts, spk)
            neurons[nid] = {
                "spike_times": valid_spikes,
                "pos_indices": pos_idx,
                "spike_x": pos_x[pos_idx],
                "spike_y": pos_y[pos_idx],
            }

        session = {
            "filename": fname,
            "pos_ts": pos_ts,
            "pos_x": pos_x,
            "pos_y": pos_y,
            "neurons": neurons,
        }
        sessions.append(session)
        print(f"Loaded {fname}: {len(pos_ts)} position samples, "
              f"{len(neurons)} neurons")

    return sessions


def select_session(sessions, session_name=None):
    """Select one recording file; never identify neurons across files by name."""
    if session_name is not None:
        selected = [s for s in sessions if s["filename"] == session_name]
        if len(selected) != 1:
            raise ValueError(f"Expected one recording named {session_name!r}")
        return selected[0]
    if len(sessions) != 1:
        raise ValueError("Select one simultaneous recording with --session; "
                         "timestamps from separate files must not be pooled")
    return sessions[0]


def analysis_context():
    """Shared CLI selection and separate output namespace for each recording."""
    root = Path(__file__).resolve().parents[1]
    choices = sorted(p.name for p in (root / "data").glob("*.mat"))
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", required=True, choices=choices)
    args = parser.parse_args()
    sessions = load_all_data(root / "data")
    selected = select_session(sessions, args.session)
    output = root / "outputs" / "sessions" / Path(args.session).stem
    output.mkdir(parents=True, exist_ok=True)
    print(f"Recording: {args.session}; outputs: {output}")
    return [selected], str(output)


def build_activity_matrix(sessions, bin_size=0.02, *, session_name=None):
    """
    Build a population activity matrix shaped (timepoints, neurons).
    Requires one simultaneous recording or an explicit session_name selection.
    Bins spike counts into time bins of bin_size seconds.
    Returns (activity_matrix, neuron_ids, time_bins).
    """
    if not np.isfinite(bin_size) or bin_size <= 0:
        raise ValueError("bin_size must be finite and positive")
    session = select_session(sessions, session_name)
    all_neurons = {nid: ndata["spike_times"]
                   for nid, ndata in session["neurons"].items()}
    pos_ts = session["pos_ts"]
    if len(pos_ts) < 2 or not np.all(np.isfinite(pos_ts)) or np.any(np.diff(pos_ts) <= 0):
        raise ValueError("Position timestamps must be finite and strictly increasing")
    t_start = pos_ts[0]
    t_end = pos_ts[-1]
    # Use only complete bins; the right edge of the last bin is included.
    n_full_bins = int(np.floor((t_end - t_start) / bin_size + 1e-10))
    if n_full_bins < 1:
        raise ValueError("Recording must contain at least one complete time bin")
    time_bins = t_start + np.arange(n_full_bins + 1) * bin_size
    n_bins = len(time_bins) - 1

    neuron_ids = sorted(all_neurons.keys())
    n_neurons = len(neuron_ids)

    activity = np.zeros((n_bins, n_neurons), dtype=np.float32)
    for j, nid in enumerate(neuron_ids):
        spk = all_neurons[nid]
        spk = spk[(spk >= t_start) & (spk <= time_bins[-1])]
        counts, _ = np.histogram(spk, bins=time_bins)
        activity[:, j] = counts / bin_size

    return activity, neuron_ids, time_bins[:-1]


if __name__ == "__main__":
    sessions, out_dir = analysis_context()
    print(f"\nTotal sessions loaded: {len(sessions)}")
    total_neurons = sum(len(s["neurons"]) for s in sessions)
    print(f"Total neuron recordings: {total_neurons}")

    activity, neuron_ids, time_bins = build_activity_matrix(sessions)
    print(f"\nActivity matrix shape: {activity.shape}")
    print(f"  (timepoints={activity.shape[0]}, neurons={activity.shape[1]})")
    print(f"Neuron IDs: {neuron_ids}")

    np.save(os.path.join(out_dir, "activity_matrix.npy"), activity)
    np.savetxt(os.path.join(out_dir, "activity_matrix.csv"), activity,
               delimiter=",", header=",".join(neuron_ids), comments="")
    print(f"Saved activity_matrix.npy and activity_matrix.csv")
