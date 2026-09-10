# Fig. 15 and Fig. 16 — cumulative energy consumption traces for the dynamic
# mission scenario (N_cluster = 5), recorded every 0.1 s over 850 s.
#
#   Fig. 15  (a) CH overall      (b) CM overall
#            (c) CH init+search  (d) CM init+search
#   Fig. 16  (a) CH deep search  (b) CM deep search
#            (c) CH error mode   (d) CM error mode
#
# The published panels are these plots with callouts drawn on top (cycle boxes
# in Fig. 15, the error-node arrow in Fig. 16); the annotations are editorial
# and are not reproduced here.
import os
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
import matplotlib.pyplot as plt

from scalnet_data import DATA, traces, save

# Mode windows read off the scenario timeline, in seconds.
WINDOWS = {
    "overall": (None, None),
    "init_search": (0, 135),      # initialization then search mode
    "deep_search": (237, 432),    # deep search, with slot reallocation
    "error": (530, 640),          # error mode and recovery
}

# The published zoom panels crop the y-axis so the reporting nodes stay legible;
# the active cluster runs far above the rest and is left off the top. Panels not
# listed here autoscale.
YLIMS = {
    ("ch", "init_search"): (0, 145),
    ("ch", "deep_search"): (150, 325),
    ("cm", "deep_search"): (12, 21),
    ("ch", "error"): (365, 705),
}


def label_for(module):
    """`ClusterHead_3` -> CH3;  `member_9` -> CM2_2 (two members per cluster)."""
    idx = int(module.split("_")[1].split(".")[0])
    if module.startswith("ClusterHead"):
        return f"CH{idx}"
    k = idx - 6                      # member_6 is the first CM
    return f"CM{k // 2 + 1}_{k % 2 + 1}"


def panel(role, window, stem):
    path = os.path.join(DATA, "dynamic_scenario", f"energy_trace_{role}.json")
    t0, t1 = WINDOWS[window]
    fig, ax = plt.subplots(figsize=(6.4, 4.8))
    for module, times, values in traces(path):
        xs, ys = times, values
        if t0 is not None:
            pairs = [(x, y) for x, y in zip(times, values) if t0 <= x <= t1]
            if not pairs:
                continue
            xs, ys = zip(*pairs)
        ax.plot(xs, ys, linewidth=1.0, label=label_for(module))
    ncol = 2 if role == "cm" else 1
    ax.legend(loc="upper left", fontsize=8, ncol=ncol)
    ax.set_xlabel("Simulation Time[s]")
    ax.set_ylabel("TotalEnergy Usage[J]")
    ax.set_title("Total energy", fontweight="bold")
    if t0 is not None:
        ax.set_xlim(t0, t1)
    if (role, window) in YLIMS:
        ax.set_ylim(*YLIMS[(role, window)])
    fig.tight_layout()
    save(fig, stem)
    plt.close(fig)


panel("ch", "overall", "fig15a_ch_overall")
panel("cm", "overall", "fig15b_cm_overall")
panel("ch", "init_search", "fig15c_ch_init_search")
panel("cm", "init_search", "fig15d_cm_init_search")
panel("ch", "deep_search", "fig16a_ch_deep_search")
panel("cm", "deep_search", "fig16b_cm_deep_search")
panel("ch", "error", "fig16c_ch_error")
panel("cm", "error", "fig16d_cm_error")

for role in ("ch", "cm"):
    ts = traces(os.path.join(DATA, "dynamic_scenario", f"energy_trace_{role}.json"))
    print(f"  {role.upper()}: {len(ts)} nodes, {len(ts[0][1])} samples, "
          f"t = {ts[0][1][0]}..{ts[0][1][-1]} s, "
          f"final = {min(v[-1] for _, _, v in ts):.1f}..{max(v[-1] for _, _, v in ts):.1f} J")
