"""Precompute every number in Part 7 of *Psychology, Built* ("The Brain").

    python -m videos.psychology.psych7.compute            # everything missing (under a minute), into .cache/psych7/
    python -m videos.psychology.psych7.compute --force lesionmap

Results are cached in ``.cache/psych7/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The models are
Psyche's (``explainer.psychology.psyche.brain``); the published figures they are set beside come from the
Archive.  Every random choice is seeded.

Items:
    tour          the brain in numbers: neurons, the cortex's share of them, mass and energy, and the arithmetic of
                  the ten-percent myth
    massaction    Lashley's result from a model cortex in which every job has a place: errors against the amount
                  removed, for a task with one place and for a task that can be done six ways
    aphasia       Wernicke and Lichtheim's diagram as an architecture: what each lesion does to understanding,
                  speaking and repeating, for complete and partial damage
    dissociation  patients under a one-resource and a two-resource model: who is impaired on what, with noiseless
                  and noisy tests; the chance that a screen of N patients shows a double dissociation
    maps          cortical magnification: millimetres per degree, distance along a meridian, the share of the map
                  within each eccentricity, and a chart of letters that each take the same length of cortex
    blindspot     where the blind spot falls on a screen, and the viewing distance that puts a mark on it
    memory        the memory architecture intact and without its hippocampal system; a skill learned over three
                  days by a model with and without that system
    hemispheres   what a whole-brain "type" and what local lateralization each predict for 1,011 people
    practice      one patient against eight controls, by z and by the modified t test; the chance that a healthy
                  person fails at least one of k tests
    lesionmap     lesion-symptom mapping on a sheet fed by one artery, and on a sheet with lesions anywhere:
                  overlap, the map, and the displacement of its centre over thirty studies
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology import archive
from explainer.psychology.psyche import brain as B

CACHE = Cache("psych7")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


# ---------------------------------------------------------------------------
def compute_tour() -> dict:
    a, e = archive.AZEVEDO_2009.data, archive.RAICHLE_2002.data
    resting_watts = 80.0  # a resting adult's power, to the nearest ten watts; see the README's open checks
    return {"neurons": a["neurons"], "neurons_sd": a["neurons_sd"], "cortex_share": a["cortex_share"],
            "cortex_neurons": a["neurons"] * a["cortex_share"], "mass_share": e["mass_share"],
            "energy_share": e["energy_share"], "resting_watts": resting_watts,
            "brain_watts": resting_watts * e["energy_share"],
            "times_fair_share": e["energy_share"] / e["mass_share"],
            # the myth's arithmetic: if a tenth did the work, that tenth would be running at ten times the rate
            "watts_if_tenth": resting_watts * e["energy_share"], "tenth_mass_share": e["mass_share"] / 10,
            "tenth_times_fair_share": e["energy_share"] / (e["mass_share"] / 10)}


def compute_massaction() -> dict:
    one = B.maze_lesions((5,), rng=rng(77))
    many = B.maze_lesions((0, 2, 4, 6, 8, 10), rng=rng(77))
    out = {"regions": one["regions"], "routes_many": 6}
    for name, d in (("one", one), ("many", many)):
        out[f"{name}_size"], out[f"{name}_errors"], out[f"{name}_hit"] = d["size"], d["errors"], d["hit"]
        out[f"{name}_r_size"], out[f"{name}_r_place"] = d["r_size"], d["r_place"]
        out[f"{name}_spread"] = d["spread_within_size"]
        sizes = np.unique(d["size"])
        out[f"{name}_mean_by_size"] = np.array([d["errors"][d["size"] == k].mean() for k in sizes])
    out["sizes"] = np.unique(one["size"])
    return out


def compute_aphasia() -> dict:
    arch = B.LICHTHEIM
    tasks = list(arch.tasks)
    full = arch.table(B.APHASIAS)
    half = arch.table({k: {m: 0.5 for m in v} for k, v in B.APHASIAS.items()})
    return {"modules": list(arch.modules), "tasks": tasks, "routes": {t: list(r) for t, r in arch.tasks.items()},
            "lesions": list(B.APHASIAS), "full": np.array([[full[k][t] for t in tasks] for k in B.APHASIAS]),
            "half": np.array([[half[k][t] for t in tasks] for k in B.APHASIAS]),
            "intact": [arch.performance()[t] for t in tasks],
            "double": arch.dissociates("speak", "understand speech")["double"]}


def compute_dissociation() -> dict:
    noises = np.array([0.0, 0.02, 0.04, 0.05, 0.06, 0.08, 0.10])
    out = {"noises": noises, "control_sd": 0.05}
    for model in ("one", "two"):
        rows = [B.dissociations(model, noise=float(s), rng=rng(70)) for s in noises]
        for key in ("a_only", "b_only", "both", "neither"):
            out[f"{model}_{key}"] = np.array([r[key] for r in rows])
    screened = np.arange(1, 201)
    for name, s in (("quiet", 0.0), ("typical", 0.05), ("noisy", 0.10)):
        d = B.dissociations("one", noise=s, rng=rng(70))
        out[f"chance_{name}"] = np.array([B.chance_of_double(d["a_only"], d["b_only"], int(n)) for n in screened])
        out[f"b_only_{name}"] = d["b_only"]
    out["screened"] = screened
    two = B.dissociations("two", noise=0.05, rng=rng(70))
    out["chance_two"] = np.array([B.chance_of_double(two["a_only"], two["b_only"], int(n)) for n in screened])
    # a cloud of patients under each model, for the picture: 300 of them, tests as noisy as the controls vary
    for model in ("one", "two"):
        d = B.dissociations(model, patients=300, noise=0.05, rng=rng(71))
        out[f"cloud_{model}"] = np.column_stack([d["a"], d["b"]])
        out[f"cloud_{model}_kind"] = d["impaired_a"].astype(int) + 2 * d["impaired_b"].astype(int)
    ca, cb = (float(B._score(1.0, t, 0.12)) for t in (0.55, 0.35))
    out["cut_a"], out["cut_b"] = ca - 2 * 0.05, cb - 2 * 0.05
    # the curves of the one-resource model: score on each task against what the lesion leaves
    r = np.linspace(0, 1, 101)
    out["resource"], out["curve_a"], out["curve_b"] = r, B._score(r, 0.55, 0.12), B._score(r, 0.35, 0.12)
    return out


def compute_maps() -> dict:
    e = np.linspace(0, 40, 401)
    marks = np.array([1.0, 2.5, 5.0, 10.0, 15.0, 30.0, 60.0])
    # letters that each cover the same length of cortex: height proportional to 1 / M
    ecc = np.array([1.0, 2.0, 4.0, 8.0, 16.0])
    return {"ecc": e, "m": B.magnification(e), "distance": B.cortical_distance(e), "share": B.area_share(np.maximum(e, 1e-9)),
            "marks": marks, "share_at": B.area_share(marks), "m0": float(B.magnification(0.0)),
            "m_at": B.magnification(marks), "area_total": float(B.cortical_area(90.0)),
            "letter_ecc": ecc, "letter_size": 1.0 / B.magnification(ecc) * B.magnification(1.0),
            "thumb_deg": 2.0, "share_thumb": float(B.area_share(1.0))}


def compute_blindspot() -> dict:
    d = B.blind_spot(1.0)
    return {"centre_deg": 15.0, "width_deg": 5.5, "near": d["near"], "centre": d["centre"], "far": d["far"],
            "width": d["width"], "distance_per_separation": 1.0 / d["centre"],
            "at_57": B.blind_spot(57.0)["width"], "at_57_centre": B.blind_spot(57.0)["centre"]}


def compute_memory() -> dict:
    arch = B.MEMORY
    tasks = list(arch.tasks)
    intact, hm = arch.performance(), arch.performance({"hippocampal system": 1.0})
    # a skill learned over three days of ten trials: errors fall as a power of practice, with a little lost
    # overnight.  The skill system is untouched by the lesion, so the two curves differ only by their noise.
    g = rng(72)
    trials = np.arange(1, 31)

    def curve():
        base = 6.0 + 26.0 * trials ** -0.6
        overnight = np.where((trials - 1) % 10 == 0, 1.12, 1.0)
        return np.maximum(base * overnight + 1.3 * g.standard_normal(len(trials)), 0.0)

    return {"tasks": tasks, "intact": [intact[t] for t in tasks], "hm": [hm[t] for t in tasks], "trials": trials,
            "errors_intact": curve(), "errors_hm": curve(), "recalls_sessions_intact": 1.0, "recalls_sessions_hm": 0.0}


def compute_hemispheres() -> dict:
    n, k = archive.NIELSEN_2013.data["people"], 20
    g = rng(73)
    local = g.standard_normal((n, k))
    types = 0.7 * g.standard_normal((n, 1)) + np.sqrt(1 - 0.49) * g.standard_normal((n, k))

    def summary(x):
        c = np.corrcoef(x, rowvar=False)
        off = c[~np.eye(k, dtype=bool)]
        return c, float(off.mean()), x.mean(axis=1)

    cl, ml, il = summary(local)
    ct, mt, it = summary(types)
    edges = np.linspace(-2.5, 2.5, 41)
    return {"people": n, "connections": k, "corr_local": cl, "corr_types": ct, "mean_r_local": ml, "mean_r_types": mt,
            "edges": edges, "index_local": np.histogram(il, edges, density=True)[0],
            "index_types": np.histogram(it, edges, density=True)[0], "sd_local": float(il.std()),
            "sd_types": float(it.std())}


def compute_practice() -> dict:
    # eight healthy people of the patient's age on a 40-point test, and the patient's score
    controls = np.array([34.0, 31.0, 38.0, 29.0, 35.0, 33.0, 36.0, 30.0])
    case = 24.0
    ch = B.crawford_howell(case, controls)
    from scipy import stats

    k = np.arange(1, 31)
    return {"controls": controls, "case": case, "mean": float(controls.mean()), "sd": float(controls.std(ddof=1)),
            "z": ch["z"], "p_z": float(stats.norm.cdf(ch["z"])), "t": ch["t"], "df": ch["df"], "p_t": ch["p"],
            "one_in_z": float(1 / stats.norm.cdf(ch["z"])), "one_in_t": float(1 / ch["p"]),
            "k": k, "at_least_one": 1 - 0.95 ** k, "ten": float(1 - 0.95 ** 10), "twenty": float(1 - 0.95 ** 20)}


def compute_lesionmap() -> dict:
    out = {}
    for name, vasc in (("artery", True), ("anywhere", False)):
        one = B.lesion_study(rng=rng(75), vascular=vasc)
        many = [B.lesion_study(rng=rng(760 + s), vascular=vasc) for s in range(30)]
        shift = np.array([m["shift"] for m in many])
        out[f"{name}_overlap"], out[f"{name}_tmap"] = one["overlap"], np.nan_to_num(one["tmap"], nan=0.0)
        out[f"{name}_top"], out[f"{name}_centre"], out[f"{name}_peak"] = one["top"], one["centre"], one["peak"]
        out[f"{name}_displacement"] = np.array([m["displacement"] for m in many])
        out[f"{name}_shift"] = shift
        out[f"{name}_mean_displacement"] = float(np.mean([m["displacement"] for m in many]))
        out[f"{name}_mean_shift"] = shift.mean(axis=0)
        out[f"{name}_top_inside"] = float(np.mean([m["top_inside"] for m in many]))
        out[f"{name}_example"] = one["lesions"][:6]
    one = B.lesion_study(rng=rng(75))
    out["critical"], out["patients"], out["size"] = one["critical"], 400, 40
    out["critical_centre"], out["trunk_row"] = (22, 26), 20
    return out


ITEMS = {
    "tour": compute_tour,
    "massaction": compute_massaction,
    "aphasia": compute_aphasia,
    "dissociation": compute_dissociation,
    "maps": compute_maps,
    "blindspot": compute_blindspot,
    "memory": compute_memory,
    "hemispheres": compute_hemispheres,
    "practice": compute_practice,
    "lesionmap": compute_lesionmap,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
