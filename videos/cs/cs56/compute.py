"""Precompute everything numerical in Part 56 of *Computer Science, Built* ("Spectral Graphs and Expanders").

    python -m videos.cs.cs56.compute              # everything missing
    python -m videos.cs.cs56.compute --force mixing

Results are cached in ``.cache/cs56/<name>.json``; scenes call ``load(name)``.  The instrument is
``explainer/cs/spectral/spectra.py``; tests in tests/test_cs56_spectral.py.

Items:
    partition   two planted communities: the Fiedler vector against the truth; the sweep cut
    cheeger     Cheeger's inequality on 60 small random graphs, conductance found by brute force
    mixing      lazy random walks on a cycle, a grid, a random 4-regular graph and a barbell: TV against the bound
    series      spectra of Part 18's city grid, Part 36's internet and the novels' word graph
    regular     random d-regular graphs against the Ramanujan bound 2 sqrt(d - 1); the expander mixing lemma
    zigzag      a zig-zag product built and its second eigenvalue against the RVW bound
    commute     commute time = 2 m R_eff on a 5 x 5 grid, against simulated walks
    solver      CG on an ill-conditioned dense Laplacian, plain and preconditioned by its spectral sparsifier
"""

from __future__ import annotations

from explainer.ai.cache import Cache

CACHE = Cache("cs56")
load = CACHE.load


def _S():
    from explainer.cs.spectral import spectra
    return spectra


def compute_partition() -> dict:
    return _S().partition_experiment()


def compute_cheeger() -> dict:
    return {"rows": _S().cheeger_check()}


def compute_mixing() -> dict:
    return _S().mixing_experiment()


def compute_series() -> dict:
    return _S().series_graphs()


def compute_regular() -> dict:
    return {"rows": [{k: float(v) for k, v in r.items()} for r in _S().regular_spectra()]}


def compute_zigzag() -> dict:
    return _S().zigzag_experiment()


def compute_commute() -> dict:
    S = _S()
    return S.commute_check(S.grid(5, 5), 0, 24)


def compute_solver() -> dict:
    return _S().solver_experiment()


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
