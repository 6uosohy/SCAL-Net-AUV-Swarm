"""Loaders for the OMNeT++ result files in `data/`.

Every file is the JSON export of one OMNeT++ run: `attributes` (run metadata),
`config` (the omnetpp.ini section that produced it), and either `scalars`
(end-of-run values) or `vectors` (time series). Nodes are identified by module
name — `ClusterHead_<i>` for a cluster head, `member_<j>` for a cluster member.
"""
import json
import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(_HERE)
DATA = os.path.join(ROOT, "data")
FIGURES = os.path.join(ROOT, "figures")


def _run(path):
    """Return the single run record inside an OMNeT++ JSON export."""
    with open(path, encoding="utf-8") as f:
        doc = json.load(f)
    return doc[next(iter(doc))]


def scalars(path, name=None):
    """[(module, value)] for one scalar name, in file order."""
    out = []
    for s in _run(path).get("scalars", []):
        if name is None or s["name"] == name:
            out.append((s["module"].split(".", 1)[1], s["value"]))
    return out


def energy_by_role(path):
    """(cluster_head_values, cluster_member_values) for one run, in module order."""
    ch, cm = [], []
    for module, value in scalars(path, "totalEnergy"):
        (ch if module.startswith("ClusterHead") else cm).append(value)
    return ch, cm


def data_rate(path):
    """The single dataRate scalar recorded on ClusterHead_1."""
    return scalars(path, "dataRate")[0][1]


def _node_sort_key(module):
    m = re.search(r"_(\d+)\.", module)
    return int(m.group(1)) if m else 0


def traces(path):
    """[(module, times, values)] for every totalEnergy vector, node-number order."""
    out = []
    for v in _run(path).get("vectors", []):
        if v.get("name") != "totalEnergy":
            continue
        out.append((v["module"].split(".", 1)[1], v["time"], v["value"]))
    out.sort(key=lambda t: _node_sort_key(t[0]))
    return out


def save(fig, stem):
    """Write `figures/<stem>.pdf` and `.png`, and report the path."""
    os.makedirs(FIGURES, exist_ok=True)
    pdf = os.path.join(FIGURES, stem + ".pdf")
    fig.savefig(pdf)
    fig.savefig(os.path.join(FIGURES, stem + ".png"), dpi=200)
    print("saved:", pdf)
