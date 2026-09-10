# Fig. 11 — superframe period as a function of the number of clusters.
#
# There is no simulation output behind this one. The superframe period follows
# directly from the TDMA schedule of Section III-B,
#
#     T_sf = T_dl + (T_ul0 + T_ul1) * N_cluster
#
# which at the Table 8 parameters is 3.0 + 6.0 * N_cluster seconds.
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
import matplotlib.pyplot as plt
import numpy as np

from scalnet_data import save

# Table 8
T_DL = 3.0          # downlink slot, s
T_UL0 = 3.0         # intra-cluster uplink frame, N_CM x (T_Tx_pkt + T_guard_intra)
T_UL1 = 3.0         # CH uplink slot, T_Tx_pkt + T_guard

N = np.arange(1, 6)
T_sf = T_DL + (T_UL0 + T_UL1) * N

fig, ax = plt.subplots(figsize=(6.4, 4.8))
ax.plot(N, T_sf, "-o", color="tab:blue", markersize=6, linewidth=1.6)
ax.set_xticks(N)
ax.set_xlabel("The number of clusters in a network [clusters]")
ax.set_ylabel("Superframe period [s]")
ax.set_title("Superframe period per cluster", fontweight="bold")
ax.set_ylim(0, T_sf.max() * 1.1)
ax.grid(True, color="0.9", linewidth=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
save(fig, "fig11_superframe_period")
plt.close(fig)

print("  N :  T_sf [s]")
for n, t in zip(N, T_sf):
    print(f"  {n} : {t:8.1f}")
