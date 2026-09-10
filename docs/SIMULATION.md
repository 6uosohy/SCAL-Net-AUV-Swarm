# The simulated system

What the result files in `data/` describe, so the numbers can be read without
the simulation model in hand. Everything here is from the paper; nothing is
inferred from the model source.

## Architecture

Three tiers. One **Gateway (GW)** on the surface, $N_{cluster}$ **Cluster Heads
(CHs)**, and two **Cluster Members (CMs)** per cluster. CHs carry the long-range
acoustic link to the GW; CMs report to their own CH over a short range. The
swarm therefore holds $1 + 3 N_{cluster}$ vehicles, three to sixteen across the
configurations studied.

Roles set the power budget, and that is where the energy asymmetry in Fig. 12
and Fig. 13 comes from: a CH transmits at 20 W, a CM at 2 W.

## TDMA superframe

One superframe is a downlink slot followed by one uplink frame per cluster:

$$T_{sf} = T_{dl} + (T_{ul0} + T_{ul1}) \cdot N_{cluster}$$

with $T_{ul0}$ the intra-cluster frame in which the CMs report to their CH, and
$T_{ul1}$ the CH's own uplink to the GW. At the parameters below,
$T_{dl} = T_{ul0} = T_{ul1} = 3.0$ s, so $T_{sf} = 3.0 + 6.0 N_{cluster}$
seconds — the straight line in Fig. 11, and the reason update latency is
predictable as the swarm grows.

## Operational modes

| Mode | What the network is doing |
|---|---|
| Initialization | GW discovers nodes and assigns cluster membership |
| Search | Wide-area survey. Every cluster reports on its own fixed slot |
| Deep Search | Precision inspection. The GW reallocates the idle uplink slots of inactive clusters to the one active cluster |
| Error | A node has stopped responding; the GW runs timeout and recovery |

Deep Search Mode is the mechanism behind Fig. 14. Because the active cluster
gets $N_{cluster}$ slot-times per superframe instead of one, its throughput
*rises* with swarm size where a static schedule's falls.

## Parameters

From Table 8 of the paper. These are the values the committed runs used; each
result file also carries its own `omnetpp.ini` section under `config`.

| Category | Parameter | Value |
|---|---|---|
| Network | Simulated space | 2 km × 1 km, 2D |
| | $N_{cluster}$ | 1, 2, 3, 4, 5 |
| | $N_{CM}$ per cluster | 2 |
| Deployment | AUV mobility | macroscopic formation maintenance |
| | Inter-cluster spacing | 100 m |
| | GW ↔ CH distance | 2 km |
| PHY / MAC | Payload per slot $D_s$ | 5,000 bits |
| | Speed of sound $v_{sound}$ | 1,500 m/s |
| | $T_{dl}$ | $T_{Tx\_pkt} + T_{guard}$ = 3.0 s |
| | $T_{ul0}$ | $N_{CM} \times (T_{Tx\_pkt} + T_{guard\_intra})$ = 3.0 s |
| | $T_{ul1}$ | $T_{Tx\_pkt} + T_{guard}$ = 3.0 s |
| | $T_{Tx\_pkt}$ | 1.0 s |
| | $T_{guard}$ | 2.0 s |
| | $T_{guard\_intra}$ | 0.5 s |
| Energy | $P_{Tx\_CH}$ | 20.0 W |
| | $P_{Tx\_CM}$ | 2.0 W |
| | $P_{listen}$ | 1.0 W |
| | $P_{idle}$ | 0.01 W |
| Duration | Total simulated time | 28,800 s (8 hours) |

The channel model is deliberately simple: propagation delay proportional to
distance at 1,500 m/s, no multipath, no fading. The paper is explicit that this
is to isolate protocol behaviour rather than to model the acoustic channel.
Perfect chip synchronisation is assumed. The intra-cluster guard time of 0.5 s
is far larger than the ≈0.067 s propagation delay over 100 m, deliberately, to
absorb positional drift and clock offset.

## Energy model

For each vehicle $i$, over the analysis period:

$$E_i = (T_{Tx,i} \times P_{Tx,i}) + (T_{Rx,i} \times P_{listen}) + (T_{idle,i} \times P_{idle})$$

$P_{Tx,i}$ is $P_{Tx\_CH}$ or $P_{Tx\_CM}$ depending on the node's role.
Receiving and overhearing are charged at the same $P_{listen}$ for every node.
The state durations follow from the TDMA schedule, which is why the traces in
Fig. 15 and Fig. 16 rise in steps rather than smoothly: a vehicle draws power
during its assigned slots and idles at 0.01 W the rest of the time.

## The dynamic scenario

`data/dynamic_scenario/` holds one 850 s run at $N_{cluster} = 5$, sampled every
0.1 s, that walks the swarm through all four modes in sequence. The windows the
published panels zoom into:

| Window | Time | Shows |
|---|---|---|
| Initialization + Search | 0 – 135 s | the baseline duty cycle, one step per cluster per superframe |
| Deep Search | 237 – 432 s | slot reallocation — the active cluster's CH pulls away from the rest |
| Error | 530 – 640 s | a node stops responding, the GW times out and recovers |

In the zoomed panels the active cluster runs far above the others, so the
published figures crop the y-axis to keep the remaining nodes legible;
`make_fig15_16_energy_traces.py` reproduces those limits.

Note the run length: 850 s here against the 28,800 s of the scalability and
energy sweeps. This scenario exists to show mode transitions, not to measure
steady-state energy.
