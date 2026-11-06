"""Precompute everything numerical in Part 55 of *Computer Science, Built* ("Trusting Trust", the finale).

    python -m videos.cs.cs55.compute              # everything missing

Results are cached in ``.cache/cs55/<name>.json``; scenes call ``load(name)``.  The instruments are in
``explainer/cs/trust/`` (memory, auth, access, web, trojan); tests in tests/test_cs55_memory.py and
tests/test_cs55_trojan.py.

Items:
    defences    Part 11's stack smash under every combination of canary, NX and ASLR
    aslr        ASLR entropy of typical layouts; a fixed exploit against 2^6 placements
    rop         gadgets found in a Pebble binary and a chain that prints "pwned" with NX on
    borrow      a toy borrow checker on ten programs
    passwords   entropy, guessing times, and a Zipf model of human passwords
    totp        HOTP and TOTP against the RFC 4226 and 6238 test vectors
    ns          Needham-Schroeder: Lowe's attack found by exhaustive search, and the fix
    access      the access matrix, the confused deputy, Bell-LaPadula and an HRU leak
    sql         SQL injection on Part 35's engine, and bound parameters
    xss         an unescaped template against an escaped one
    trojan      Thompson's trojan compiler: stages, the fixpoint, the backdoor
    ddc         diverse double-compiling on a clean and a trojaned compiler
    repro       reproducible builds: normalized against unnormalized
    job         ledger row 20: the Job as one line of Python on this machine
    open        the open problems the series met (shared with Part 61)
"""

from __future__ import annotations

import json

from explainer.ai.cache import Cache

CACHE = Cache("cs55")
load = CACHE.load


def compute_defences() -> dict:
    from explainer.cs.trust import memory
    return {"rows": memory.defense_matrix()}


def compute_aslr() -> dict:
    from explainer.cs.trust import memory
    return {"entropy": memory.aslr_entropy(), "experiment": memory.aslr_experiment()}


def compute_rop() -> dict:
    from explainer.cs.trust import memory
    return memory.rop_demo()


def compute_borrow() -> dict:
    from explainer.cs.trust import memory
    return {"rows": memory.borrow_examples()}


def compute_passwords() -> dict:
    from explainer.cs.trust import auth
    return {"table": auth.guessing_table(), "zipf": auth.zipf_cracked()}


def compute_totp() -> dict:
    from explainer.cs.trust import auth
    return {"hotp": auth.hotp_vectors(), "totp": auth.totp_vectors()}


def compute_ns() -> dict:
    from explainer.cs.trust import auth
    return {"flawed": auth.needham_schroeder(False), "fixed": auth.needham_schroeder(True)}


def compute_access() -> dict:
    from explainer.cs.trust import access
    return {"matrix": access.access_matrix(), "deputy": access.confused_deputy(), "blp": access.bell_lapadula(),
            "hru_leak": access.hru_safety(access.leaking_system(), "read"),
            "hru_safe": access.hru_safety(access.safe_system(), "read")}


def compute_sql() -> dict:
    from explainer.cs.trust import web
    return web.injection_report()


def compute_xss() -> dict:
    from explainer.cs.trust import web
    return web.xss_report("<script>steal(document.cookie)</script>")


def compute_trojan() -> dict:
    from explainer.cs.trust import trojan
    return trojan.thompson_report()


def compute_ddc() -> dict:
    from explainer.cs.trust import trojan
    return trojan.ddc_report()


def compute_repro() -> dict:
    from explainer.cs.trust import trojan
    return trojan.reproducible_report()


def compute_job() -> dict:
    """Ledger row 20: the thirty novels counted by Counter and a regular expression in Python on this machine, the
    median of 15 runs, against Part 6's 281 seconds on one Pebble."""
    from explainer.cs.research.method import job_timing
    t = job_timing(runs=15)
    led = json.loads((Cache("cs50").dir / "ledger.json").read_text())
    led = [x for x in led if x["part"] != 55]
    led.append({"part": 55, "label": r"one line of Python, \ this machine", "seconds": t["median"], "native": True,
                "ci_median": list(t["ci_median"])})
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    (CACHE.dir / "ledger.json").write_text(json.dumps(led, indent=1))
    return {"timing": {k: v for k, v in t.items() if k != "times"}, "times": t["times"], "ledger": led}


def compute_open() -> dict:
    from explainer.cs.research.method import open_problems
    return {"rows": open_problems()}


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
