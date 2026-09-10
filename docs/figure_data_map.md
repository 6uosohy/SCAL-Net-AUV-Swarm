# Figure and data provenance

Every data-backed figure in the paper, the file it reads, and the script that
redraws it. Figures 1–10 are architecture and protocol diagrams with no data
behind them and are not reproduced here.

| Paper | Script | Reads | Output |
|---|---|---|---|
| Fig. 11 — Superframe period vs. $N_{cluster}$ | `make_fig11_superframe.py` | closed form, no data file | `fig11_superframe_period` |
| Fig. 12 — Search mode energy by role group | `make_fig12_search_energy.py` | `data/search_mode/energy_N{1..5}.json` | `fig12a_…`, `fig12b_…` |
| Fig. 13 — Deep search mode energy by role group | `make_fig13_deepsearch_energy.py` | `data/deep_search_mode/energy_N{1..5}_realloc.json` | `fig13a_…`, `fig13b_…` |
| Fig. 14 — Effective throughput comparison | `make_fig14_throughput.py` | `data/throughput/throughput_N{1..5}_{realloc,static}.json` | `fig14_throughput` |
| Fig. 15 — Cumulative energy, baseline operation | `make_fig15_16_energy_traces.py` | `data/dynamic_scenario/energy_trace_{ch,cm}.json` | `fig15a…d` |
| Fig. 16 — Cumulative energy, dynamic events | `make_fig15_16_energy_traces.py` | `data/dynamic_scenario/energy_trace_{ch,cm}.json` | `fig16a…d` |

## Reproduced values

The numbers each script prints, against the published figures.

**Fig. 11** — $T_{sf}$ = 9, 15, 21, 27, 33 s for $N_{cluster}$ = 1…5, exactly
$3.0 + 6.0 N_{cluster}$.

**Fig. 12, search mode** (kJ):

| $N$ | $E_{group,CH}$ | $E_{group,CM}$ | $E_{avg,CH}$ | $E_{avg,CM}$ |
|---|---|---|---|---|
| 1 | 80.6 | 6.5 | 80.6 | 6.5 |
| 2 | 106.1 | 8.0 | 53.0 | 4.0 |
| 3 | 122.8 | 8.9 | 40.9 | 3.0 |
| 4 | 137.5 | 9.4 | 34.4 | 2.4 |
| 5 | 153.5 | 9.9 | 30.7 | 2.0 |

**Fig. 13, deep search mode** (kJ):

| $N$ | $E_{group,CH}$ | $E_{group,CM}$ | $E_{avg,CH}$ | $E_{avg,CM}$ |
|---|---|---|---|---|
| 1 | 78.0 | 6.5 | 78.0 | 6.5 |
| 2 | 93.8 | 8.0 | 46.9 | 4.0 |
| 3 | 100.9 | 8.8 | 33.6 | 2.9 |
| 4 | 104.7 | 9.4 | 26.2 | 2.4 |
| 5 | 107.7 | 9.9 | 21.5 | 2.0 |

**Fig. 14** — see the table in the README. The two TDMA curves are simulated
`dataRate` scalars; they reproduce the closed forms (11) and (13) to within
0.15 bps.

## Two conventions worth knowing

### $E_{group,CM}$ counts one member per cluster

Each simulation run carries **two** cluster members per cluster
(`**.membersPerCluster = 2`), so for $N_{cluster} = 5$ the run records ten CM
energy scalars. The published $E_{group,CM}$ bars are the sum over **one member
per cluster**, i.e. half the CM population — for $N = 3$ search mode, 8.9 kJ
rather than the 17.7 kJ the six members consume together.

Read the bar as *the CM energy of a representative cluster slice* rather than a
whole-group total. `make_fig12_search_energy.py` and
`make_fig13_deepsearch_energy.py` follow the published convention so that the
regenerated figures match the paper; the full-population sum is one edit away
(`sum(cm)` instead of `sum(cm[::2])`) if you want it. The $E_{avg}$ bars are
unaffected — dividing either total by $N_{cluster}$ gives the same per-node
average, which is what the paper reports.

### The contention curve in Fig. 14

Equation (12) in the paper prints the slotted-ALOHA approximation as

$$R_{contention} \approx \frac{D_s}{T_{ul0} + T_{ul1}} \cdot N \cdot e^{-(N-1)}$$

Evaluated at the Table 8 parameters that gives 833 bps at $N = 1$, whereas the
plotted curve starts at 555 bps together with the other two schemes. The curve
that is actually drawn uses the full slot budget in the denominator,

$$R_{contention} \approx \frac{D_s}{T_{dl} + T_{ul0} + T_{ul1}} \cdot N \cdot e^{-(N-1)}$$

which reproduces all five plotted points (555.6, 408.8, 225.6, 110.6, 50.9 bps).
`make_fig14_throughput.py` uses the latter. The distinction does not change the
paper's argument — the exponential term is what drives the collapse — but it
does change the absolute values, so it is recorded here.

## Result file structure

Each file is the JSON export of a single OMNeT++ run, keyed by run id:

```
"General-0-20250825-14:02:48-62132": {
    "attributes": { configname, datetime, inifile, network, seedset, ... },
    "config":     [ the omnetpp.ini section for this run ],
    "scalars":    [ { module, name, value }, ... ]      // end-of-run values
    "vectors":    [ { module, name, time[], value[] } ] // time series
}
```

Modules are named `ClusterHead_<i>` and `member_<j>`. For $N_{cluster} = 5$ the
cluster heads are `ClusterHead_1`…`_5` and the members are `member_6`…`member_15`,
two per cluster in ascending order — `member_6` and `member_7` belong to cluster
1, and so on. `analysis/scalnet_data.py` resolves this mapping; the labels
`CM1_1`…`CM5_2` in Fig. 15–16 follow it.

Scalar files record `totalEnergy` per node (joules over the 8 hour run) or a
single `dataRate` on `ClusterHead_1` (bits per second). The dynamic-scenario
files record `totalEnergy` vectors sampled every 0.1 s over 850 s — 8,500
samples per node, five cluster heads and ten cluster members.
