# Fig. 14 — effective data throughput vs. swarm size, comparing SCAL-Net's deep
# search mode against a static-TDMA baseline and an analytical contention model.
#
# The two TDMA curves are the simulated dataRate scalars in data/throughput/.
# The contention curve has no simulation behind it; it is the slotted-ALOHA
# approximation of (12), evaluated at the Table 8 parameters.
import os
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
import matplotlib.pyplot as plt
import numpy as np

from scalnet_data import DATA, data_rate, save

# Table 8
D_S = 5000.0        # payload bits per uplink slot
T_DL = 3.0          # downlink slot, s
T_UL0 = 3.0         # intra-cluster uplink frame, N_CM x (T_Tx_pkt + T_guard_intra)
T_UL1 = 3.0         # CH uplink slot, T_Tx_pkt + T_guard

N = np.arange(1, 6)
deep = [data_rate(os.path.join(DATA, "throughput", f"throughput_N{n}_realloc.json"))
        for n in N]
static = [data_rate(os.path.join(DATA, "throughput", f"throughput_N{n}_static.json"))
          for n in N]

# Slotted ALOHA, (12). The offered-load term uses the full superframe slot
# budget T_dl + T_ul0 + T_ul1, which is what the published curve follows.
contention = D_S / (T_DL + T_UL0 + T_UL1) * N * np.exp(-(N - 1))

fig, ax = plt.subplots(figsize=(6.4, 4.8))
ax.plot(N, deep, "-^", color="k", markerfacecolor="k", markersize=7, linewidth=1.6,
        label="Proposed SCAL-Net (Deep Search)")
ax.plot(N, static, "--o", color="k", markerfacecolor="none", markersize=7,
        linewidth=1.6, label="Conventional Static TDMA (Baseline)")
ax.plot(N, contention, ":x", color="k", markersize=7, linewidth=1.6,
        label="Contention-based Protocol (Analysis)")

ax.set_xticks(N)
ax.set_xlabel("The number of clusters in a network ($N_{cluster}$)")
ax.set_ylabel("Throughput [bps]")
ax.set_title("Throughput comparison analysis", fontweight="bold")
ax.legend(loc="lower left", fontsize=9)
fig.tight_layout()
save(fig, "fig14_throughput")
plt.close(fig)

print("  N :  SCAL-Net   static  contention   [bps]")
for i, n in enumerate(N):
    print(f"  {n} : {deep[i]:9.1f} {static[i]:8.1f} {contention[i]:11.1f}")

# The simulated rates follow (13) and (11) exactly; report the residual so a
# reader can see the simulation and the closed form agree.
model_deep = N * D_S / (T_DL + N * (T_UL0 + T_UL1))
model_static = D_S / (T_DL + N * (T_UL0 + T_UL1))
print(f"  max |sim - model| : deep {np.abs(deep - model_deep).max():.3f} bps, "
      f"static {np.abs(static - model_static).max():.3f} bps")
