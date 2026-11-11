"""Precompute everything numerical in Part 53 of *Computer Science, Built* ("Quantum Computation").

    python -m videos.cs.cs53.compute              # everything missing
    python -m videos.cs.cs53.compute --force shor

Results are cached in ``.cache/cs53/<name>.json``; scenes call ``load(name)``.  The instruments are in
``explainer/cs/quantum/`` (sim, algorithms, qec); tests in tests/test_cs53_quantum.py.

Items:
    landauer    kT ln 2 at room temperature
    bloch       Bloch-sphere trajectories of H, T, S and Rx
    bell        the Bell state's amplitudes
    chsh        the CHSH game: quantum cos^2(pi/8) against classical 3/4
    cloning     a CNOT "copying" |+>: fidelity 1/2
    dj          Deutsch-Jozsa on four qubits: amplitudes before and after, P(all zeros)
    bv          Bernstein-Vazirani: the secret in one query
    simon       Simon's problem: the y's and the recovered secret
    qft         the QFT circuit against the FFT: agreement and gate counts
    phase       phase estimation of theta = 0.3 with six counting qubits
    shor15      order finding for 7 mod 15, and the factors
    shor21      order finding for 2 mod 21, and the factors
    grover      success probability against iterations (N = 64); amplitude snapshots
    gscale      Grover's iterations against N, and classical search
    bb84        key distribution with and without an eavesdropper
    code3       the three-qubit bit-flip code: syndromes and correction
    repetition  logical against physical error rate for distances 1 to 11; Lambda
"""

from __future__ import annotations

from explainer.ai.cache import Cache

CACHE = Cache("cs53")
load = CACHE.load


def _A():
    from explainer.cs.quantum import algorithms
    return algorithms


def compute_landauer() -> dict:
    return _A().landauer()


def compute_bloch() -> dict:
    from explainer.cs.quantum import sim
    return sim.bloch_paths()


def compute_bell() -> dict:
    return _A().bell()


def compute_chsh() -> dict:
    return _A().chsh()


def compute_cloning() -> dict:
    return _A().no_cloning()


def compute_dj() -> dict:
    return _A().deutsch_jozsa()


def compute_bv() -> dict:
    return _A().bernstein_vazirani()


def compute_simon() -> dict:
    return _A().simon()


def compute_qft() -> dict:
    return {"rows": [_A().qft_check(n) for n in (2, 3, 4, 6, 8)]}


def compute_phase() -> dict:
    return _A().phase_estimation()


def compute_shor15() -> dict:
    return _A().shor(15, 7)


def compute_shor21() -> dict:
    return _A().shor(21, 2)


def compute_grover() -> dict:
    return _A().grover()


def compute_gscale() -> dict:
    return {"rows": _A().grover_scaling()}


def compute_bb84() -> dict:
    return {"honest": _A().bb84(), "eve": _A().bb84(eve=True)}


def compute_code3() -> dict:
    from explainer.cs.quantum import qec
    return {"cases": [qec.three_qubit(flip=f) for f in (None, 0, 1, 2)]}


def compute_repetition() -> dict:
    from explainer.cs.quantum import qec
    return qec.repetition()


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
