# SCAL-Net — simulation results for a scalable, adaptive AUV-swarm network

Campaign results and analysis code behind the IEEE Access paper on **SCAL-Net**,
a three-tier clustering architecture (Gateway → Cluster Heads → Cluster Members)
with a mission-adaptive TDMA protocol for autonomous underwater vehicle swarms.

> **Paper:** S. Kim, H. Lee, S. Park, J. Kim, B. Ahn, and T. Im, *"SCAL-Net: A
> Scalable and Adaptive Hierarchical Network Framework for Autonomous Underwater
> Vehicle Swarms,"* **IEEE Access**, vol. 14, pp. 2166–2187, 2026.
> **DOI: [10.1109/ACCESS.2025.3649806](https://doi.org/10.1109/ACCESS.2025.3649806)**
> — open access, CC BY 4.0.
>
> This repository holds the data and plotting code behind the paper's published
> figures. The OMNeT++ simulation model itself is **not** part of this
> repository — see [What is not here](#what-is-not-here).

---

## The problem SCAL-Net addresses

An AUV swarm surveying a wide area and one inspecting a small patch at high
resolution want opposite things from the network. Wide-area survey wants
scalability and long battery life; precision inspection wants concentrated
throughput on one cluster. Static TDMA gives the first and not the second;
contention-based protocols collapse as the swarm grows.

SCAL-Net runs one adaptive TDMA protocol across four operational modes —
Initialization, Search, Deep Search, Error. In **Deep Search Mode** the gateway
reallocates the idle uplink slots of inactive clusters to the one active
cluster, so throughput *rises* with swarm size instead of falling.

## Headline results

Throughput at the Table 8 parameters, in bits per second:

| $N_{cluster}$ | SCAL-Net (Deep Search) | Static TDMA | Contention (analysis) |
|---|---|---|---|
| 1 | 555.5 | 555.5 | 555.6 |
| 2 | 666.5 | 333.3 | 408.8 |
| 3 | 714.1 | 238.0 | 225.6 |
| 4 | 740.7 | 185.2 | 110.6 |
| 5 | **757.6** | 151.5 | 50.9 |

Static TDMA falls as `1/N` and the contention model collapses exponentially,
while slot reallocation lets SCAL-Net climb to **5.0×** the static baseline at
five clusters.

The superframe period stays exactly linear, $T_{sf} = 3.0 + 6.0 N_{cluster}$
seconds, so update latency is predictable as the swarm scales. Energy stays
concentrated in the cluster heads, which carry the long-range link to the
gateway at 20 W against the members' 2 W.

## Repository layout

```
data/
  search_mode/        per-node energy totals, N = 1..5          → Fig. 12
  deep_search_mode/   the same under slot reallocation          → Fig. 13
  throughput/         effective data rate, reallocated & static → Fig. 14
  dynamic_scenario/   0.1 s energy traces over an 850 s mission → Fig. 15, 16
analysis/
  scalnet_data.py     loaders for the OMNeT++ JSON exports
  make_fig*.py        one script per published figure
figures/              regenerated output (PDF + PNG)
docs/
  SIMULATION.md       the simulated system, parameters, and energy model
  figure_data_map.md  which file and which script produced each figure
```

Every result file is the JSON export of one OMNeT++ run and carries its own
`config` block — the `omnetpp.ini` section that produced it — so each figure can
be traced back to the exact configuration behind it.

## Quick start

```bash
pip install numpy scipy matplotlib
cd analysis
python make_fig11_superframe.py
python make_fig12_search_energy.py
python make_fig13_deepsearch_energy.py
python make_fig14_throughput.py
python make_fig15_16_energy_traces.py
```

Each script prints the numbers it plots and writes a vector PDF plus a 200 dpi
PNG into `figures/`. No MATLAB, no simulator, no network access.

## What is not here

| Item | Why |
|---|---|
| The OMNeT++ simulation model (C++ node classes, NED files, `omnetpp.ini`) | Developed under a defence research programme and not ours to release. The per-run configuration is preserved inside each result file. |
| Raw `.vec` traces for the scalability sweep | Roughly 1 GB of per-event records that no published figure draws on. The scalar exports that do back the figures are included in full. |
| The manuscript | Open access at the DOI above. |

## How closely the figures reproduce

`analysis/` regenerates every data-backed figure in the paper from the committed
result files, and the printed numbers match the published ones. The scripts are
a clean reimplementation rather than the originals, so a regenerated figure
matches the published one in data and layout but not pixel for pixel; the
published panels also carry editorial callouts (cycle boxes in Fig. 15, the
error-node arrow in Fig. 16) that are drawn on top and not reproduced here.
[`docs/figure_data_map.md`](docs/figure_data_map.md) records this figure by
figure, including one convention in Fig. 12–13 worth knowing about before
reading the numbers.

Figures 1–10 are architecture and protocol diagrams with no data behind them,
and are not part of this repository.

## Citation

```bibtex
@article{kim2026scalnet,
  author  = {Kim, Seunggyu and Lee, Hyosong and Park, Sunghyun and
             Kim, Junho and Ahn, Byoungsun and Im, Taeho},
  title   = {{SCAL-Net}: A Scalable and Adaptive Hierarchical Network
             Framework for Autonomous Underwater Vehicle Swarms},
  journal = {IEEE Access},
  volume  = {14},
  pages   = {2166--2187},
  year    = {2026},
  doi     = {10.1109/ACCESS.2025.3649806}
}
```

## Funding

Supported by the Korea Research Institute for Defense Technology Planning and
Advancement (KRIT), funded by the Korean Government (DAPA), through *Multi AUV
Operation Technology for Mine Detection* (2023–2028), Grant KRIT-CT-23-035.

## License

Analysis code: **MIT** (see [`LICENSE`](LICENSE)). The result data and the
figures derived from it are released under **CC BY 4.0**, matching the open
access terms of the paper.
