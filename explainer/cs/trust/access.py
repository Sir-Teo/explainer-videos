"""Access control (Part 55, chapter 6): Lampson's access matrix (1971) and its two slicings -- access-control lists
down the columns, capability lists along the rows -- and why ambient authority invites the confused deputy (Hardy,
*The Confused Deputy*, 1988) where capabilities do not; the Bell-LaPadula secrecy model (1973), no read up and no
write down, over a small security lattice; and the HRU protection model (Harrison, Ruzzo and Ullman, *Protection in
operating systems*, CACM 1976), whose safety question -- can a right ever leak to a subject that should not have it
-- is undecidable in general (a reduction from the halting problem, Part 25), decidable only for restricted systems
(mono-operational commands).  Here we run a *bounded* safety search, which answers the question for a fixed budget.
"""

from __future__ import annotations

from collections import deque
from itertools import product

# ======================================================================================================================
# 1. Lampson's access matrix, ACLs and capabilities
# ======================================================================================================================

def access_matrix() -> dict:
    """A small protection state as a matrix of rights, and the two ways a system stores it: by column (an ACL per
    object, what every subject may do to it) and by row (a capability list per subject, what it may do to every
    object).  ACLs answer "who can touch this file?"; capabilities answer "what can this process reach?".
    """
    subjects = ["alice", "bob", "server"]
    objects = ["report.txt", "payroll.db", "socket"]
    M = {
        ("alice", "report.txt"): {"read", "write", "own"},
        ("alice", "payroll.db"): {"read"},
        ("bob", "report.txt"): {"read"},
        ("bob", "socket"): {"read", "write"},
        ("server", "payroll.db"): {"read", "write", "own"},
        ("server", "socket"): {"read", "write"},
    }
    acls = {o: {s: sorted(M[(s, o)]) for s in subjects if (s, o) in M} for o in objects}
    caps = {s: {o: sorted(M[(s, o)]) for o in objects if (s, o) in M} for s in subjects}
    return {"subjects": subjects, "objects": objects,
            "matrix": {f"{s}->{o}": sorted(r) for (s, o), r in M.items()},
            "acls_by_object": acls, "capabilities_by_subject": caps}


def confused_deputy() -> dict:
    """Hardy's confused deputy, as a scenario.  A compiler service (the deputy) runs with the ambient authority to
    write its billing records to BILL.  A client may ask it to write the compiler's debug output to a path the client
    names.  Under ambient authority the deputy uses *its own* rights for that write, so a client that names BILL as
    the output path makes the deputy overwrite the billing file -- the client borrowed an authority it never held.
    With capabilities the client must *hand the deputy a capability* for the output file; it has none for BILL, so it
    cannot ask for that write at all.  The authority to write BILL travels only as an unforgeable token, never as the
    deputy's ambient identity.
    """
    def ambient(output_path: str, deputy_rights):
        # the deputy writes using its own (ambient) rights, whatever path the client named
        return ("write" in deputy_rights.get(output_path, set())), "deputy's ambient authority"

    def capability(output_path: str, client_caps):
        # the client must present a capability for the path; the write uses only that authority
        return ("write" in client_caps.get(output_path, set())), "client's presented capability"

    deputy_rights = {"BILL": {"read", "write"}, "DEBUG": {"read", "write"}}
    client_caps = {"DEBUG": {"read", "write"}}            # the client can write DEBUG, nothing about BILL

    amb_ok, amb_why = ambient("BILL", deputy_rights)       # the attack: overwrite BILL via the deputy
    cap_ok, cap_why = capability("BILL", client_caps)      # the same request, denied
    return {
        "attack_target": "BILL",
        "ambient": {"write_happens": amb_ok, "authority_used": amb_why,
                    "verdict": "confused: billing file overwritten with the deputy's authority"},
        "capability": {"write_happens": cap_ok, "authority_used": cap_why,
                       "verdict": "denied: client holds no capability for BILL"},
        "lesson": "ambient authority lets a request pick up the deputy's rights; a capability binds authority to the "
                  "designation, so it cannot be borrowed by naming.",
    }


# ======================================================================================================================
# 2. Bell-LaPadula: no read up, no write down
# ======================================================================================================================

LEVELS = {"unclassified": 0, "confidential": 1, "secret": 2, "topsecret": 3}


def dominates(a: tuple, b: tuple) -> bool:
    """Lattice order on labels (level, categories): a dominates b iff a's level >= b's and a's categories include
    b's."""
    (la, ca), (lb, cb) = a, b
    return LEVELS[la] >= LEVELS[lb] and set(cb) <= set(ca)


def bell_lapadula_can_read(subject: tuple, obj: tuple) -> bool:
    """Simple security property (no read up): a subject may read an object only if it dominates the object's label."""
    return dominates(subject, obj)


def bell_lapadula_can_write(subject: tuple, obj: tuple) -> bool:
    """The star-property (no write down): a subject may write an object only if the object dominates the subject, so
    information never flows to a lower label."""
    return dominates(obj, subject)


def bell_lapadula() -> dict:
    """Check reads and writes over a small lattice, and show a flow the model forbids: a top-secret process cannot
    write to an unclassified file (which would leak secrets downward), and cannot be fooled into reading it... it
    *can* read down but not write down; the dangerous direction, high -> low, is blocked by the star-property.
    """
    secret_eng = ("secret", {"ENG"})
    unclass_pub = ("unclassified", set())
    topsecret = ("topsecret", {"ENG", "OPS"})
    confidential_ops = ("confidential", {"OPS"})

    checks = [
        {"what": "secret/ENG reads unclassified doc", "op": "read",
         "subject": "secret/ENG", "object": "unclassified", "allowed": bell_lapadula_can_read(secret_eng, unclass_pub)},
        {"what": "secret/ENG reads topsecret doc (read up)", "op": "read",
         "subject": "secret/ENG", "object": "topsecret/ENG,OPS", "allowed": bell_lapadula_can_read(secret_eng, topsecret)},
        {"what": "secret/ENG writes unclassified doc (write down)", "op": "write",
         "subject": "secret/ENG", "object": "unclassified", "allowed": bell_lapadula_can_write(secret_eng, unclass_pub)},
        {"what": "unclassified writes secret doc (write up, allowed)", "op": "write",
         "subject": "unclassified", "object": "secret/ENG", "allowed": bell_lapadula_can_write(unclass_pub, secret_eng)},
        {"what": "secret/ENG reads confidential/OPS (category not held)", "op": "read",
         "subject": "secret/ENG", "object": "confidential/OPS",
         "allowed": bell_lapadula_can_read(secret_eng, confidential_ops)},
    ]
    forbidden = {"what": "topsecret process copies a secret into an unclassified file", "op": "write",
                 "subject": "topsecret/ENG,OPS", "object": "unclassified",
                 "allowed": bell_lapadula_can_write(topsecret, unclass_pub),
                 "why": "the star-property blocks the high -> low flow that would leak the secret"}
    return {"levels": LEVELS, "checks": checks, "forbidden_flow": forbidden}


# ======================================================================================================================
# 3. HRU: a protection system and a bounded safety search
# ======================================================================================================================
#
# A configuration is (subjects, objects, matrix) with matrix a frozenset of (subject, object, right).  A command has
# formal parameters, a conjunction of conditions "right in [s, o]", and a body of primitive operations.

def _apply(config, ops, env):
    subjects, objects, M = set(config[0]), set(config[1]), set(config[2])
    for op in ops:
        kind = op[0]
        if kind == "enter":
            M.add((env[op[2]], env[op[3]], op[1]))
        elif kind == "delete":
            M.discard((env[op[2]], env[op[3]], op[1]))
        elif kind == "create_subject":
            subjects.add(env[op[1]])
        elif kind == "create_object":
            objects.add(env[op[1]])
        elif kind == "destroy_subject":
            s = env[op[1]]
            subjects.discard(s)
            M = {t for t in M if t[0] != s and t[1] != s}
        elif kind == "destroy_object":
            o = env[op[1]]
            objects.discard(o)
            M = {t for t in M if t[1] != o}
        else:  # pragma: no cover
            raise ValueError(f"unknown op {op}")
    return (frozenset(subjects), frozenset(objects), frozenset(M))


def _enabled(config, command, fresh):
    """Yield (env, label) for every parameter instantiation whose conditions hold.  Formal params bind to existing
    subjects/objects; a param named 'new*' binds to a single fresh name (bounded creation)."""
    subjects, objects, M = config
    params = command["params"]
    domains = []
    for p in params:
        if p.startswith("new"):
            domains.append([fresh])
        else:
            domains.append(sorted(set(subjects) | set(objects)))
    for combo in product(*domains):
        env = dict(zip(params, combo))
        ok = all((env[s], env[o], r) in M for (r, s, o) in command["conditions"])
        if ok:
            label = f"{command['name']}(" + ", ".join(f"{p}={env[p]}" for p in params) + ")"
            yield env, label


def hru_safety(system: dict, right: str, max_subjects: int = 4, max_objects: int = 4,
               limit: int = 200_000) -> dict:
    """Bounded safety: starting from ``system['initial']``, apply ``system['commands']`` in every way, and ask
    whether ``right`` can ever be entered into a cell that did not already hold it in the initial configuration.
    Creation is bounded by ``max_subjects``/``max_objects``.  Within the budget this is a decision; the general
    question is undecidable (HRU 1976), so a "safe" answer here means "no leak within the bound".
    """
    init = (frozenset(system["initial"][0]), frozenset(system["initial"][1]), frozenset(system["initial"][2]))
    init_cells = {(s, o) for (s, o, r) in init[2] if r == right}
    start = init
    parent = {start: None}
    q = deque([start])
    leak_state = None

    def leaks(config):
        for (s, o, r) in config[2]:
            if r == right and (s, o) not in init_cells:
                return (s, o)
        return None

    found = leaks(start)
    while q and leak_state is None:
        config = q.popleft()
        for command in system["commands"]:
            creates = any(op[0] in ("create_subject", "create_object") for op in command["body"])
            if creates and (len(config[0]) >= max_subjects or len(config[1]) >= max_objects):
                # allow object creates up to max_objects, subject creates up to max_subjects
                if any(op[0] == "create_subject" for op in command["body"]) and len(config[0]) >= max_subjects:
                    continue
                if any(op[0] == "create_object" for op in command["body"]) and len(config[1]) >= max_objects:
                    continue
            fresh = f"n{len(config[0]) + len(config[1])}"
            for env, label in _enabled(config, command, fresh):
                nxt = _apply(config, command["body"], env)
                if nxt not in parent:
                    parent[nxt] = (config, label)
                    hit = leaks(nxt)
                    if hit is not None:
                        parent.setdefault(nxt, (config, label))
                        leak_state = nxt
                        found = hit
                        break
                    q.append(nxt)
                    if len(parent) > limit:
                        raise RuntimeError("state space too large")
            if leak_state is not None:
                break

    trace = None
    if leak_state is not None:
        steps, cur = [], leak_state
        while parent[cur] is not None:
            p, label = parent[cur]
            steps.append(label)
            cur = p
        trace = steps[::-1]
    return {"right": right, "leaks": leak_state is not None, "leaked_cell": found if leak_state is not None else None,
            "trace": trace, "states_explored": len(parent)}


def leaking_system() -> dict:
    """A tiny system that leaks: the owner of a file can grant ``read`` on it, and can hand ownership to anyone, so
    ``read`` reaches a subject that started with nothing."""
    initial = (
        ["alice", "eve"],
        ["secret"],
        [("alice", "secret", "own"), ("alice", "secret", "read")],
    )
    commands = [
        {"name": "grant_read", "params": ["s", "o", "t"],
         "conditions": [("own", "s", "o")],
         "body": [("enter", "read", "t", "o")]},
        {"name": "grant_own", "params": ["s", "o", "t"],
         "conditions": [("own", "s", "o")],
         "body": [("enter", "own", "t", "o")]},
    ]
    return {"initial": initial, "commands": commands}


def safe_system() -> dict:
    """A tiny system that cannot leak ``read``: the only command deletes rights, so no reachable configuration ever
    enters ``read`` into a new cell (safety holds, and here it is even provable, not just within the bound)."""
    initial = (
        ["alice"],
        ["doc"],
        [("alice", "doc", "own")],
    )
    commands = [
        {"name": "revoke_own", "params": ["s", "o"],
         "conditions": [("own", "s", "o")],
         "body": [("delete", "own", "s", "o")]},
    ]
    return {"initial": initial, "commands": commands}
