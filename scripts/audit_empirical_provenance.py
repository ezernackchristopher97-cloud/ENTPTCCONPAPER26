"""Inventory retained data and diagnostics without claiming attractor recovery.

Legacy outputs are read, never regenerated or overwritten. The legacy activity
matrix is reproduced only to identify its invalid cross-recording construction.
No missing Gardner analysis, H2 result, or noise-floor calibration is invented.
"""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import scipy.io as sio

from entropy import spatial_entropy
from preprocessing import load_all_data, build_activity_matrix


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(root):
    sessions = load_all_data(root / "data")
    inventory = []
    for session in sessions:
        path = root / "data" / session["filename"]
        raw = sio.loadmat(path)
        activity, ids, _ = build_activity_matrix([session])
        inventory.append({
            "file": session["filename"], "sha256": sha256(path),
            "tracking_array_sha256": {
                field: hashlib.sha256(raw[field].tobytes(order="C")).hexdigest()
                for field in ("pos_timeStamps", "pos_x", "pos_y")
            },
            "raw_position_samples": int(raw["pos_timeStamps"].size),
            "finite_position_samples": int(len(session["pos_ts"])),
            "neuron_labels": ids, "neuron_count": len(ids),
            "session_activity_shape_20ms": list(activity.shape),
        })

    # Faithful reconstruction of the old pooling rule, for provenance only.
    # This function deliberately does NOT feed any new biological analysis.
    chosen = max(sessions, key=lambda s: len(s["neurons"]))
    start, end = chosen["pos_ts"][[0, -1]]
    edges = np.arange(start, end, 0.02)
    pooled = {}
    for session in sessions:
        for nid, data in session["neurons"].items():
            pooled.setdefault(nid, []).extend(data["spike_times"])
    legacy = np.empty((len(edges) - 1, len(pooled)), dtype=np.float32)
    for j, nid in enumerate(sorted(pooled)):
        times = np.asarray(pooled[nid])
        times = times[(times >= start) & (times < end)]
        legacy[:, j] = np.histogram(times, bins=edges)[0] / 0.02
    saved = np.load(root / "outputs" / "activity_matrix.npy")

    topology = {}
    for name in ("pca", "umap"):
        path = root / "outputs" / "topology" / f"diagram_H1_{name}.csv"
        diagram = np.loadtxt(path, delimiter=",", skiprows=1)
        persistence = np.sort(diagram[:, 1] - diagram[:, 0])[::-1]
        topology[name] = {
            "file": str(path.relative_to(root)), "sha256": sha256(path),
            "n_finite_H1": len(persistence), "top_five": persistence[:5].tolist(),
            "top_to_third_ratio": float(persistence[0] / persistence[2]),
            "valid_simultaneous_population_evidence": False,
        }
    maps = sorted((root / "outputs" / "rate_maps").glob("*.npy"))
    entropies = {p.stem: float(spatial_entropy(np.load(p))) for p in maps}
    return {
        "kind": "repository provenance audit; no new attractor evidence",
        "sessions": inventory,
        "total_cell_recordings_across_files": sum(row["neuron_count"] for row in inventory),
        "distinct_neuron_labels_across_files": len(pooled),
        "legacy_activity": {
            "shape": list(saved.shape),
            "sha256": sha256(root / "outputs" / "activity_matrix.npy"),
            "matches_old_cross_session_pooling_exactly": bool(np.array_equal(legacy, saved)),
            "valid_simultaneous_population_evidence": False,
        },
        "legacy_topology": topology,
        "retained_rate_map_count": len(maps),
        "retained_spatial_entropy_bits": entropies,
        "retained_mean_spatial_entropy_bits": float(np.mean(list(entropies.values()))),
        "retained_population_entropy_summary": (root / "outputs" / "entropy" /
                                                  "neural_entropy_summary.csv").read_text(),
        "H2_output_files": [str(p.relative_to(root)) for p in
                            sorted((root / "outputs").rglob("*H2*"))],
        "missing_reported_figure": not (root / "paper" / "figures" /
                                        "fig_persistence_buildspec.png").exists(),
        "limits": [
            "Separate files are treated as separate recordings without evidence of shared acquisition.",
            "Distinct labels are not a verified count of distinct biological neurons.",
            "Legacy rate maps can overwrite repeated labels across trials.",
            "No Gardner Rat R Day 1 Module 2 raw recording or matching analysis is retained here.",
            "Legacy H1 diagnostics have no calibrated noise floor and do not establish T2.",
            "Unresolved or unavailable H2 is not evidence that the biological torus is absent.",
        ],
    }


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=root / "outputs" / "claim_audit" / "empirical_provenance.json")
    args = parser.parse_args()
    result = audit(root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in (
        "kind", "total_cell_recordings_across_files", "distinct_neuron_labels_across_files",
        "retained_rate_map_count", "retained_mean_spatial_entropy_bits", "H2_output_files")}, indent=2))
