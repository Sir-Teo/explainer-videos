"""Precompute everything in Part 26 of *Philosophy, Built* ("The Quantum Puzzle").

    python -m videos.philosophy.philosophy26.compute            # everything missing (seconds)

Items:
    born        the Born rule on a qubit, sampled
    chsh        Bell and CHSH: local strategies, the singlet's value, Tsirelson's bound, the correlation curve
    game        the CHSH game: all 16 classical strategies and the quantum strategy simulated
    ghz         GHZ: eigenvalues and all 64 local assignments
    pm          the Peres--Mermin square: operator products and all 512 assignments
    pbr         the PBR measurement's probability table
    decohere    a qubit recorded by n environment qubits
    bohm        Bohmian trajectories through two slits
    grw         GRW localization rates and a simulated hit
    mzi         a Mach--Zehnder interferometer, with and without a which-path marker
    uncert      uncertainty on a qubit: Robertson's bound and the sum of variances
    mixtures    proper and improper mixtures: half a singlet against a coin flip
    mermin      Mermin's device: instruction sets against the quantum agreement rate
    prbox       the PR box: no-signalling and S = 4
    cabello     Kochen--Specker by parity: 18 vectors, 9 bases, 2^18 assignments
    branches    many worlds: branch counting against Born weights
    friend      Wigner's friend: unitary against collapse, tested
    ghzgame     the GHZ game: 64 classical strategies and the GHZ strategy
    toy         Spekkens' toy theory: states, measurements, overlaps
    triad       the Price List for Maudlin's measurement problem
    fr          the Price List for Frauchiger--Renner
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import prop
from explainer.philosophy.reasoner import quantum as Q

CACHE = Cache("philosophy26")
load = CACHE.load

TRIAD = [
    ("C", r"the wavefunction of a system is complete: \ it says everything about it"),
    ("L", r"the wavefunction always evolves by the linear Schrödinger equation"),
    ("D", r"measurements always have single, \ definite outcomes"),
]

FR = [
    ("Q", r"quantum theory applies to everything, \ agents and their labs included"),
    ("C", r"an agent may rely on what another agent, \ reasoning by the theory, \ has concluded"),
    ("S", r"each measurement has one outcome, \ for whoever made it"),
]


def _pl(items):
    claims = {k: prop.Var(k) for k, _ in items}
    bg = [prop.Not(prop.And(*[prop.Var(k) for k, _ in items]))]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t in items], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


ITEMS = {"born": Q.born, "chsh": Q.chsh, "game": Q.chsh_game, "ghz": Q.ghz, "pm": Q.peres_mermin, "pbr": Q.pbr,
         "decohere": Q.decoherence, "bohm": Q.bohm, "grw": Q.grw, "mzi": Q.interferometer,
         "uncert": Q.uncertainty, "mixtures": Q.mixtures, "mermin": Q.mermin_device, "prbox": Q.pr_box,
         "cabello": Q.cabello18, "branches": Q.branch_count, "friend": Q.wigner_friend, "ghzgame": Q.ghz_game,
         "toy": Q.spekkens, "triad": lambda: _pl(TRIAD),
         "fr": lambda: _pl(FR)}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
