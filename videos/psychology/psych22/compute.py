"""Precompute every number in Part 22 of *Psychology, Built* ("Concepts and Categories").

    python -m videos.psychology.psych22.compute            # everything missing (a few minutes; fetches open data once)
    python -m videos.psychology.psych22.compute --force shj

Results are cached in ``.cache/psych22/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The models are
Psyche's (``explainer.psychology.psyche.concepts``); the data are Nosofsky et al.'s (1994) learning curves, Homa and
Vosburgh's (1976) prototype test, Ekman's (1954) colours, Rothkopf's (1957) Morse signals and Jane Austen's novels,
fetched from CRAN packages by ``explainer.psychology.opendata``.  Simulations use fixed seeds chosen in advance.

Items:
    birds        Psyche's bird table: family resemblance and similarity to the prototype, for each bird and a bat
    shj          the six problems: data; ALCOVE fitted with attention learning and without; a prototype network
    homa         Homa and Vosburgh's test: prototype, old and new items by distortion
    gcm54        the 5-4 structure: the context model's and the prototype model's predictions for every item
    ekman        Ekman's colours scaled into two dimensions: the colour circle; RSA against wavelength and cones
    morse        Rothkopf's Morse signals: generalization, a non-metric map, the exponential law, asymmetries
    regions      Shepard's consequential regions: the gradient for several priors on region size
    levels       category utility at three levels of an illustrative taxonomy
    numbers      the number game: generalization after three sets of examples
    network      spreading activation in a small semantic network
    austen       word vectors from Jane Austen: neighbours, analogies and a map of a few words
    cardsort     a simulated card sort of twelve groceries; the polythetic count of DSM-5 depression
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology import opendata
from explainer.psychology.psyche import concepts as K
from explainer.psychology.psyche import vision

CACHE = Cache("psych22")
load = CACHE.load


def compute_shj() -> dict:
    obs = opendata.nosof94()["error"]
    observed = {t: obs[t - 1] for t in range(1, 7)}
    att = K.fit_alcove_shj(observed, x0=(6.5, 3.0, 0.1, 0.3), orders=20)
    flat = K.fit_alcove_shj(observed, x0=(6.5, 2.0, 0.2, 0.0), orders=20, attention=False)
    out = {"observed": obs, "blocks": np.arange(1, 17)}
    for name, f in (("alcove", att), ("noattn", flat)):
        out[name] = np.array([f["pred"][t] for t in range(1, 7)])
        out[name + "_params"] = np.array([f["params"][k] for k in ("c", "phi", "lw", "la")])
        out[name + "_sse"] = f["sse"]
    out["delta"] = np.array([K.delta_rule_network(K.SHJ_TYPES[t], orders=40, rng=np.random.default_rng(1961))
                             for t in range(1, 7)])
    # attention at the end of learning, Types I, II and VI, at the fitted values
    c, phi, lw, la = out["alcove_params"]
    for t in (1, 2, 6):
        out[f"attention{t}"] = K.alcove_attention(K.SHJ_TYPES[t], c, phi, lw, la, rng=np.random.default_rng(3))
    return out


def compute_homa() -> dict:
    h = opendata.homa76()
    out = {}
    for cond in ("mixed", "uni-low"):
        for stim in ("proto", "low", "med", "high", "rand"):
            sel = (h["cond"] == cond) & (h["stim"] == stim)
            out[f"{cond}_{stim}"] = np.array(h["val"][sel], float)
    out["old_mixed"] = np.array([h["val"][(h["cond"] == "mixed") & (h["stim"] == s)][0]
                                 for s in ("old-low", "old-med", "old-high")], float)
    out["sizes"] = np.array([3, 6, 9])
    return out


def compute_gcm54() -> dict:
    A = np.array([[1, 1, 1, 0], [1, 0, 1, 0], [1, 0, 1, 1], [1, 1, 0, 1], [0, 1, 1, 1]], float)
    B = np.array([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]], float)
    T = np.array([[1, 0, 0, 1], [1, 0, 0, 0], [1, 1, 1, 1], [0, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 1], [0, 1, 0, 0]],
                 float)
    ex = np.vstack([A, B])
    lab = np.r_[np.zeros(5), np.ones(4)].astype(int)
    items = np.vstack([A, B, T])
    names = [f"A{i + 1}" for i in range(5)] + [f"B{i + 1}" for i in range(4)] + [f"T{i + 1}" for i in range(7)]
    out = {"items": items, "names": np.array(names)}
    for c in (1.0, 3.0):
        out[f"gcm_c{c:g}"] = K.gcm_prob(items, ex, lab, c=c)[:, 0]
        out[f"proto_c{c:g}"] = K.prototype_prob(items, ex, lab, c=c)[:, 0]
    return out


def compute_ekman() -> dict:
    e = opendata.ekman_1954()
    D = 1 - e["similarity"]
    nm = K.nonmetric_mds(D, 2, rng=np.random.default_rng(1954))
    cl, vals = K.classical_mds(D, 2)
    X = nm["X"] / np.abs(nm["X"]).max()
    hum = 1 - e["similarity"]
    wl = np.abs(e["nm"][:, None] - e["nm"][None])
    lms = np.array([vision.cone_excitations(vision.monochromatic(float(x))) for x in e["nm"]])
    lms = lms / lms.sum(1, keepdims=True)
    cone = np.sqrt(((lms[:, None] - lms[None]) ** 2).sum(-1))
    weights = np.array([0.25, 0.5, 1.0, 2.0, 4.0])
    hue = [K.rsa(hum, K.hue_angle_distances(e["nm"], w)) for w in weights]
    return {"nm": e["nm"], "X": X, "stress": nm["stress"], "classical_stress": K.stress(D, cl), "S": e["similarity"],
            "rsa_wavelength": K.rsa(hum, wl), "rsa_cones": K.rsa(hum, cone),
            "rsa_hue": K.rsa(hum, K.hue_angle_distances(e["nm"])),
            "hue_weights": weights, "rsa_hue_weights": np.array(hue)}


def compute_morse() -> dict:
    m = opendata.rothkopf_1957()
    P = m["same"]
    G = K.shepard_generalization(P)
    r = K.nonmetric_mds(1 - G, 2, rng=np.random.default_rng(1957))
    X = r["X"]
    dist = np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1))
    iu = np.triu_indices(36, 1)
    dist = dist / dist[iu].mean()
    law = K.fit_exponential_law(dist[iu], G[iu])
    g, d = G[iu], dist[iu]
    ok = g > 0
    kg = -np.sum(d[ok] ** 2 * np.log(g[ok])) / np.sum(d[ok] ** 4)
    res = np.log(g[ok]) + kg * d[ok] ** 2
    tot = np.log(g[ok]) - np.log(g[ok]).mean()
    asym = np.triu(P - P.T, 1)
    top = np.argsort(-np.abs(asym), axis=None)[:5]
    pairs = [(int(i), int(j), float(P[i, j]), float(P[j, i])) for i, j in zip(*np.unravel_index(top, asym.shape))]
    lengths = np.array([len(s) for s in m["signals"]])
    dur = np.array([K.morse_duration(s) for s in m["signals"]])
    asy = K.prominence_asymmetry(100 * P, dur)
    dashes = np.array([s.count("-") / len(s) for s in m["signals"]])
    return {"X": X / np.abs(X).max(), "stress": r["stress"], "dist": d, "gen": g, "k": law["k"], "r2_exp": law["r2_log"],
            "k_gauss": kg, "r2_gauss": float(1 - np.sum(res ** 2) / np.sum(tot ** 2)), "symbols": np.array(m["symbols"]),
            "signals": np.array(m["signals"]), "lengths": lengths, "dashes": dashes,
            "pairs": np.array([(a, b) for a, b, _, _ in pairs]), "pair_p": np.array([(x, y) for _, _, x, y in pairs]),
            "same_diag": np.diag(P), "durations": dur, "tversky_diff": asy["mean_diff"], "tversky_p": asy["sign_p"],
            "tversky": np.array([asy["pairs"], asy["more"], asy["fewer"], asy["ties"]]),
            "asym_mean": float(np.abs((P - P.T)[iu]).mean()), "off_mean": float(P[iu].mean())}


def compute_regions() -> dict:
    d = np.linspace(0, 4, 81)
    s = np.linspace(1e-3, 40, 8000)
    priors = {"erlang": s * np.exp(-s), "uniform": np.where(s < 4, 1.0, 0.0), "exponential": np.exp(-s),
              "gaussian": np.exp(-((s - 2) ** 2) / 0.5)}
    out = {"d": d, "exp": np.exp(-d)}
    for k, p in priors.items():
        g = K.consequential_region_gradient(d, s, p)
        out[k] = g
    return out


def compute_levels() -> dict:
    fs = np.arange(0, 5)
    U = np.array([K.level_utilities(*K.nested_world(f_super=int(f))) for f in fs])
    return {"f_super": fs, "U": U}


def compute_numbers() -> dict:
    sets = {"a": [16], "b": [16, 8, 2, 64], "c": [16, 23, 19, 20]}
    names, _, _ = K.number_game_hypotheses()
    out = {"n_math": sum(" to " not in h for h in names), "n_hyp": len(names)}
    for k, ex in sets.items():
        r = K.number_game(ex)
        out[k + "_gen"] = r["gen"]
        out[k + "_examples"] = np.array(ex)
        out[k + "_top"] = np.array([n for n, _ in r["top"]])
        out[k + "_top_p"] = np.array([p for _, p in r["top"]])
    return out


NET_NODES = ("animal", "bird", "fish", "robin", "canary", "penguin", "salmon", "fly", "wings", "swim", "sing",
             "red", "fire engine", "apple", "cherry")
NET_EDGES = (("animal", "bird"), ("animal", "fish"), ("bird", "robin"), ("bird", "canary"), ("bird", "penguin"),
             ("fish", "salmon"), ("bird", "fly"), ("bird", "wings"), ("fish", "swim"), ("penguin", "swim"),
             ("canary", "sing"), ("robin", "red"), ("red", "fire engine"), ("red", "apple"), ("red", "cherry"),
             ("apple", "cherry"))


def compute_network() -> dict:
    n = len(NET_NODES)
    A = np.zeros((n, n))
    for a, b in NET_EDGES:
        i, j = NET_NODES.index(a), NET_NODES.index(b)
        A[i, j] = A[j, i] = 1.0
    hist = K.spreading_activation(A, NET_NODES.index("robin"), steps=3, decay=0.5)
    return {"nodes": np.array(NET_NODES), "edges": np.array(NET_EDGES), "hist": hist}


AUSTEN_WORDS = ("letter", "morning", "sister", "happy", "money", "walk", "house", "ball")
ANALOGIES = (("brother", "sister", "father"), ("son", "daughter", "uncle"))
MAP_WORDS = ("sister", "brother", "mother", "father", "aunt", "uncle", "daughter", "son",
             "monday", "tuesday", "thursday", "saturday", "morning", "evening",
             "happy", "pleased", "cheerful", "unhappy", "miserable", "wretched")


def compute_austen() -> dict:
    tokens = opendata.austen()
    import collections

    cnt = collections.Counter(tokens)
    stop = set(K.STOPWORDS)
    vocab = [w for w, _ in cnt.most_common(6000) if w not in stop][:4000]
    C = K.cooccurrence(tokens, vocab, window=4)
    V = K.ppmi_svd(C, k=100)
    out = {"tokens": len(tokens), "vocab": len(vocab)}
    for w in AUSTEN_WORDS:
        nb = K.neighbours(V, vocab, w, 5)
        out["nb_" + w] = np.array([x for x, _ in nb])
        out["nbs_" + w] = np.array([s for _, s in nb])
    idx = [vocab.index(w) for w in MAP_WORDS]
    sub = V[idx]
    sims = sub @ sub.T
    X, _ = K.classical_mds(np.sqrt(np.clip(2 - 2 * sims, 0, None)), 2)
    for k, (x, y, z) in enumerate(ANALOGIES):
        out[f"analogy_{k}"] = np.array(K.analogy(V, vocab, x, y, z, 4))
    out["map_words"] = np.array(MAP_WORDS)
    out["map_X"] = X / np.abs(X).max()
    return out


# Psyche's illustrative bird table (features by common knowledge; not a published norm)
BIRD_FEATURES = ("feathers", "beak", "lays eggs", "flies", "sings", "small", "perches", "builds nests", "eats insects",
                 "swims", "large", "runs", "long neck")
BIRDS = {
    "robin": (1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0),
    "sparrow": (1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0),
    "canary": (1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0),
    "crow": (1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0),
    "owl": (1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0),
    "eagle": (1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0),
    "duck": (1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0),
    "swan": (1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1),
    "chicken": (1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0),
    "penguin": (1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0),
    "ostrich": (1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1),
}
BAT = (0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0)


def compute_birds() -> dict:
    names = list(BIRDS)
    F = np.array([BIRDS[n] for n in names], float)
    fr = (F * F.sum(0)).sum(1) - F.sum(1)  # each shared feature counts the other members that have it
    proto = F.mean(0)
    w = np.ones(F.shape[1]) / F.shape[1]
    sim = np.exp(-4.0 * np.abs(F - proto) @ w)
    bat_sim = float(np.exp(-4.0 * np.abs(np.array(BAT, float) - proto) @ w))
    return {"names": np.array(names), "features": np.array(BIRD_FEATURES), "F": F, "fr": fr, "proto": proto,
            "sim": sim, "bat_sim": bat_sim, "bat": np.array(BAT, float)}


# Psyche's illustrative grocery table (features by common knowledge)
FOOD_FEATURES = ("sweet", "grows on a plant", "red", "grows underground", "eaten raw", "cooked", "from an animal",
                 "liquid", "fermented", "baked", "a staple", "white", "for breakfast")
FOODS = {
    "apple": (1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1), "banana": (1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1),
    "cherry": (1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0), "carrot": (0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0),
    "potato": (0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0), "onion": (0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0),
    "milk": (0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1), "cheese": (0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0),
    "yoghurt": (0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1), "bread": (0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1),
    "pasta": (0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0), "rice": (0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0),
}


def compute_cardsort() -> dict:
    from scipy.cluster.hierarchy import dendrogram, linkage
    from scipy.spatial.distance import squareform

    names = list(FOODS)
    F = np.array([FOODS[n] for n in names], float)
    co = K.card_sort(F, 40, np.random.default_rng(22))
    Z = linkage(squareform(1 - co, checks=False), "average")
    dn = dendrogram(Z, no_plot=True, labels=names)
    return {"names": np.array(names), "co": co, "icoord": np.array(dn["icoord"]), "dcoord": np.array(dn["dcoord"]),
            "leaves": np.array(dn["ivl"]), "people": 40, "mdd_sets": K.polythetic_count(9, 5, 2)}


ITEMS = {
    "birds": compute_birds,
    "shj": compute_shj,
    "homa": compute_homa,
    "gcm54": compute_gcm54,
    "ekman": compute_ekman,
    "morse": compute_morse,
    "regions": compute_regions,
    "levels": compute_levels,
    "numbers": compute_numbers,
    "network": compute_network,
    "austen": compute_austen,
    "cardsort": compute_cardsort,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
