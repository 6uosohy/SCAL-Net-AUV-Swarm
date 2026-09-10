# Fig. 13 — total and average energy consumption by role group (CH vs CM) in
# deep search mode, over cluster configurations N = 1..5.
import os
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
import matplotlib.pyplot as plt
import numpy as np

from scalnet_data import DATA, energy_by_role, save

N_VALUES = range(1, 6)

total_ch, total_cm = [], []
for n in N_VALUES:
    ch, cm = energy_by_role(
        os.path.join(DATA, "deep_search_mode", f"energy_N{n}_realloc.json"))
    total_ch.append(sum(ch))
    # One CM per cluster — the convention the published figure uses.
    total_cm.append(sum(cm[::2]))

x = np.arange(1, len(total_ch) + 1)


def bars(ax, ch, cm, ylabel, title, ch_label, cm_label):
    ax.bar(x - 0.13, np.multiply(ch, 0.001), width=0.2, label=ch_label, color="gray")
    ax.bar(x + 0.13, np.multiply(cm, 0.001), width=0.2, label=cm_label, color="gray",
           hatch="\\\\\\")
    ax.legend(loc="upper left", fontsize=8)
    ax.set_xlim(0, len(ch) + 1)
    ax.set_xlabel("The number of clusters in a network [clusters]")
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontweight="bold")


fig, ax = plt.subplots(figsize=(6.4, 4.8))
bars(ax, total_ch, total_cm,
     "Total energy usage [kJ]", "Total energy usage per cluster",
     "$E_{group,CH}$", "$E_{group,CM}$")
fig.tight_layout()
save(fig, "fig13a_deepsearch_total_energy")
plt.close(fig)

avg_ch = [t / n for t, n in zip(total_ch, N_VALUES)]
avg_cm = [t / n for t, n in zip(total_cm, N_VALUES)]

fig, ax = plt.subplots(figsize=(6.4, 4.8))
bars(ax, avg_ch, avg_cm,
     "Average energy usage [kJ]", "Average energy usage per cluster",
     "$E_{avg,CH}$", "$E_{avg,CM}$")
fig.tight_layout()
save(fig, "fig13b_deepsearch_average_energy")
plt.close(fig)

print("  N :   E_group,CH   E_group,CM   E_avg,CH   E_avg,CM   [kJ]")
for i, n in enumerate(N_VALUES):
    print(f"  {n} : {total_ch[i]/1000:11.1f} {total_cm[i]/1000:12.1f} "
          f"{avg_ch[i]/1000:10.1f} {avg_cm[i]/1000:10.1f}")
