"""Optimizations on SSA (Part 13, chapters 8–10).  Each pass returns how many things it changed.

* :func:`copyprop`: ``x = copy y`` (or a constant) — replace x by y everywhere, delete the copy.
* :func:`sccp`: sparse conditional constant propagation (Wegman and Zadeck 1991): constants found by running the
  program over the lattice ⊤ / constant / ⊥, following only edges that can execute; branches on constants folded
  and unreachable blocks deleted.
* :func:`dce`: dead-code elimination, mark and sweep from the instructions with effects.
* :func:`gvn`: value numbering over the dominator tree: a pure computation already available in a dominating block
  is replaced by that earlier value (commutative operands sorted).
* :func:`licm`: loop-invariant code motion: natural loops found from back edges (an edge to a block that dominates
  its source); pure instructions whose operands come from outside the loop move to a preheader.  Loads move too
  when the loop has no call and no store of the same width (the type-based aliasing rule, as C's strict aliasing).
* :func:`strength`: multiplication by a power of two becomes a shift; ``x * 1``, ``x + 0`` and friends disappear.
* :func:`inline`: before SSA, small non-recursive functions are copied into their callers.
"""
from __future__ import annotations

from explainer.cs.lang.compiler import interp
from explainer.cs.lang.compiler.ir import COMMUTE, Block, Func, I, Module, is_var, remove_unreachable
from explainer.cs.lang.compiler.ssa import dom_tree, dominates, dominators

TOP, BOT = "top", "bot"


def defs(f: Func) -> dict:
    return {i.dst: i for b in f.blocks for i in b.ins if i.dst}


def replace_uses(f: Func, mapping: dict):
    if not mapping:
        return

    def res(x):
        seen = 0
        while is_var(x) and x in mapping and seen < 100:
            x = mapping[x]
            seen += 1
        return x
    for b in f.blocks:
        for i in b.ins:
            i.args = [res(a) for a in i.args]


# ---------------------------------------------------------------------------
def copyprop(f: Func) -> int:
    mapping = {}
    for b in f.blocks:
        for i in b.ins:
            if i.op == "copy":
                mapping[i.dst] = i.args[0]
            elif i.op == "const":
                mapping[i.dst] = i.k
            elif i.op == "phi" and i.args and all(a == i.args[0] for a in i.args) and i.args[0] != i.dst:
                mapping[i.dst] = i.args[0]
    replace_uses(f, mapping)
    n = 0
    for b in f.blocks:
        keep = [i for i in b.ins if not (i.dst in mapping and i.op in ("copy", "const", "phi"))]
        n += len(b.ins) - len(keep)
        b.ins = keep
    return n


# ---------------------------------------------------------------------------
def _meet(a, b):
    if a == TOP:
        return b
    if b == TOP:
        return a
    if a == BOT or b == BOT or a != b:
        return BOT
    return a


def sccp(f: Func, stats: dict | None = None) -> int:
    lab = f.labels()
    users: dict = {}
    for b in f.blocks:
        for i in b.ins:
            for a in i.uses():
                users.setdefault(a, []).append((b.label, i))
    val = {p: BOT for p in f.params}
    execb = set()
    exece = set()
    flow = [(None, f.blocks[0].label)]
    ssaw = []
    visits = 0

    def get(x):
        return x if not is_var(x) else val.get(x, TOP)

    def evaluate(blab, i):
        if i.op == "phi":
            r = TOP
            for v, p in zip(i.args, i.k):
                if (p, blab) in exece:
                    r = _meet(r, get(v))
            return r
        if i.op == "const":
            return i.k
        if i.op == "copy":
            return get(i.args[0])
        if i.op == "bin":
            a, c = get(i.args[0]), get(i.args[1])
            if a == BOT or c == BOT:
                # x * 0 and x & 0 are 0 whatever x is
                if i.k in ("mul", "and") and 0 in (a, c):
                    return 0
                return BOT
            if a == TOP or c == TOP:
                return TOP
            return interp.binop(i.k, a, c)
        if i.op == "un":
            a = get(i.args[0])
            if a in (TOP, BOT):
                return a
            return interp.s32(-a) if i.k == "neg" else int(a == 0)
        return BOT

    def visit(blab, i):
        nonlocal visits
        visits += 1
        if i.dst:
            new = evaluate(blab, i)
            old = val.get(i.dst, TOP)
            if new != old:
                val[i.dst] = new if old == TOP or new == BOT else BOT
                for ub, ui in users.get(i.dst, []):
                    ssaw.append((ub, ui))
        elif i.op == "br":
            flow.append((blab, i.k))
        elif i.op == "cbr":
            c = get(i.args[0])
            if c == TOP:
                return
            if c == BOT:
                flow.extend([(blab, i.k[0]), (blab, i.k[1])])
            else:
                flow.append((blab, i.k[0] if c != 0 else i.k[1]))

    while flow or ssaw:
        while flow:
            e = flow.pop()
            if e in exece:
                continue
            exece.add(e)
            dst = e[1]
            first = dst not in execb
            execb.add(dst)
            for i in lab[dst].ins:
                if i.op == "phi" or first:
                    visit(dst, i)
        while ssaw:
            bl, i = ssaw.pop()
            if bl in execb:
                visit(bl, i)
    # rewrite
    changed = 0
    consts = {v: c for v, c in val.items() if c not in (TOP, BOT)}
    for b in f.blocks:
        if b.label not in execb:
            continue
        keep = []
        for i in b.ins:
            if i.dst in consts and i.op in ("const", "copy", "bin", "un", "phi"):
                changed += 1
                continue
            i.args = [consts.get(a, a) if is_var(a) else a for a in i.args]
            if i.op == "cbr" and not is_var(i.args[0]):
                tgt = i.k[0] if i.args[0] != 0 else i.k[1]
                i = I("br", k=tgt)
                changed += 1
            if i.op == "phi":
                pairs = [(v, p) for v, p in zip(i.args, i.k) if (p, b.label) in exece]
                i.args = [v for v, _ in pairs]
                i.k = [p for _, p in pairs]
            keep.append(i)
        b.ins = keep
    dead = len(f.blocks) - len(execb)
    f.blocks = [b for b in f.blocks if b.label in execb]
    # φs may now list predecessors that no longer branch here
    preds = f.preds()
    for b in f.blocks:
        for i in b.ins:
            if i.op == "phi":
                pairs = [(v, p) for v, p in zip(i.args, i.k) if p in preds[b.label]]
                i.args = [v for v, _ in pairs]
                i.k = [p for _, p in pairs]
    if stats is not None:
        stats["visits"] = stats.get("visits", 0) + visits
        stats["constants"] = stats.get("constants", 0) + len(consts)
        stats["dead_blocks"] = stats.get("dead_blocks", 0) + dead
    return changed + dead


# ---------------------------------------------------------------------------
def dce(f: Func) -> int:
    d = defs(f)
    live = set()
    work = []
    for b in f.blocks:
        for i in b.ins:
            if i.op in ("store", "call", "getc", "putc", "br", "cbr", "ret"):
                live.add(id(i))
                work.append(i)
    while work:
        i = work.pop()
        for a in i.uses():
            j = d.get(a)
            if j is not None and id(j) not in live:
                live.add(id(j))
                work.append(j)
    n = 0
    for b in f.blocks:
        keep = [i for i in b.ins if id(i) in live]
        n += len(b.ins) - len(keep)
        b.ins = keep
    return n


# ---------------------------------------------------------------------------
def _key(i: I):
    if i.op == "bin":
        a = list(i.args)
        if i.k in COMMUTE:
            a = sorted(a, key=repr)
        return ("bin", i.k, tuple(a))
    if i.op == "un":
        return ("un", i.k, tuple(i.args))
    if i.op in ("gaddr", "faddr"):
        return (i.op, i.k)
    return None


def gvn(f: Func) -> int:
    idom, _ = dominators(f)
    kids = dom_tree(idom)
    lab = f.labels()
    table: dict = {}
    mapping: dict = {}
    n = 0
    import sys
    sys.setrecursionlimit(max(sys.getrecursionlimit(), 10000))

    def walk(l):
        nonlocal n
        added = []
        b = lab[l]
        keep = []
        for i in b.ins:
            i.args = [mapping.get(a, a) if is_var(a) else a for a in i.args]
            k = _key(i)
            if k is not None:
                if k in table:
                    mapping[i.dst] = table[k]
                    n += 1
                    continue
                table[k] = i.dst
                added.append(k)
            keep.append(i)
        b.ins = keep
        for s in b.succs():
            for i in lab[s].ins:
                if i.op == "phi":
                    i.args = [mapping.get(a, a) if is_var(a) else a for a in i.args]
        for c in kids.get(l, []):
            walk(c)
        for k in added:
            del table[k]
    walk(f.blocks[0].label)
    replace_uses(f, mapping)
    return n


# ---------------------------------------------------------------------------
def natural_loops(f: Func, idom=None) -> list:
    """[(header, body set, latches)], innermost last; bodies of loops sharing a header are merged."""
    idom = idom or dominators(f)[0]
    preds = f.preds()
    loops: dict = {}
    for b in f.blocks:
        for s in b.succs():
            if s in idom and b.label in idom and dominates(idom, s, b.label):
                body, work = {s, b.label}, [b.label]
                while work:
                    x = work.pop()
                    if x == s:
                        continue
                    for p in preds[x]:
                        if p not in body:
                            body.add(p)
                            work.append(p)
                h = loops.setdefault(s, [set(), []])
                h[0] |= body
                h[1].append(b.label)
    out = [(h, body, latches) for h, (body, latches) in loops.items()]
    out.sort(key=lambda t: -len(t[1]))
    return out


def licm(f: Func, stats: dict | None = None) -> int:
    moved = 0
    for header, body, latches in natural_loops(f):
        preds = f.preds()
        outside = [p for p in preds[header] if p not in body]
        if len(outside) != 1:
            continue
        pre_label = f"{header}_pre"
        if pre_label not in f.labels():
            pre = Block(pre_label, [I("br", k=header)])
            op = f.block(outside[0])
            t = op.term
            if t.op == "br":
                t.k = pre_label
            elif t.op == "cbr":
                t.k = tuple(pre_label if x == header else x for x in t.k)
            for i in f.block(header).ins:
                if i.op == "phi":
                    i.k = [pre_label if p == outside[0] else p for p in i.k]
            f.blocks.insert(f.blocks.index(op) + 1, pre)
        pre = f.block(pre_label)
        lab = f.labels()
        inside = {d for l in body for d in (i.dst for i in lab[l].ins) if d}
        has_call = any(i.op in ("call", "getc", "putc") for l in body for i in lab[l].ins)
        store_sizes = {i.k[0] for l in body for i in lab[l].ins if i.op == "store"}
        changed = True
        while changed:
            changed = False
            for l in sorted(body):
                b = lab[l]
                keep = []
                for i in b.ins:
                    movable = i.op in ("bin", "un", "gaddr", "faddr", "const") and not (
                        i.op == "bin" and i.k in ("div", "rem"))
                    if i.op == "load" and not has_call and i.k[0] not in store_sizes:
                        movable = True
                    if movable and all(not is_var(a) or a not in inside for a in i.args):
                        pre.ins.insert(len(pre.ins) - 1, i)
                        inside.discard(i.dst)
                        moved += 1
                        changed = True
                    else:
                        keep.append(i)
                b.ins = keep
    if stats is not None:
        stats["hoisted"] = stats.get("hoisted", 0) + moved
    return moved


# ---------------------------------------------------------------------------
def ivsr(f: Func, stats: dict | None = None) -> int:
    """Induction-variable strength reduction.  In a loop with a preheader, a basic induction variable is
    ``i = φ(i0 from outside, i + c from the latch)``.  A value that is ``i * k`` (or ``i << s``), or an induction
    variable plus something loop-invariant, is itself an induction variable with a known step; give it its own φ,
    start it in the preheader, step it beside ``i``, and the multiplication inside the loop disappears.  Repeats
    until nothing changes, so ``&table + i * 12`` becomes a pointer that steps by 12 (Allen, Cocke and Kennedy
    1981; Cooper, Simpson and Vick 2001)."""
    changed = 0
    counter = [0]
    for header, body, latches in natural_loops(f):
        lab = f.labels()
        pre_label = f"{header}_pre"
        if pre_label not in lab or len(latches) != 1:
            continue
        pre, latch = lab[pre_label], latches[0]
        d = defs(f)
        inside = {i.dst for l in body for i in lab[l].ins if i.dst}

        def invariant(x):
            return not is_var(x) or x not in inside
        # basic and derived induction variables: name -> (init operand, step int)
        ivs = {}
        for i in lab[header].ins:
            if i.op != "phi" or len(i.args) != 2 or set(i.k) != {pre_label, latch}:
                continue
            init = i.args[i.k.index(pre_label)]
            nxt = i.args[i.k.index(latch)]
            n = d.get(nxt)
            if n is not None and n.op == "bin" and n.k == "add" and n.args[0] == i.dst and not is_var(n.args[1]):
                ivs[i.dst] = (init, n.args[1], nxt)
        if not ivs:
            continue
        steppers = {nxt for _, _, nxt in ivs.values()}
        progress = True
        while progress:
            progress = False
            for l in sorted(body):
                for ins in list(lab[l].ins):
                    if ins.op != "bin" or ins.dst in ivs or ins.dst in steppers:
                        continue
                    a, b = ins.args
                    base = None
                    if ins.k in ("mul", "shl") and a in ivs and not is_var(b):
                        k = b if ins.k == "mul" else (1 << b)
                        init, step, nxt = ivs[a]
                        kind = ("scale", k)
                    elif ins.k == "add" and (a in ivs and invariant(b) or b in ivs and invariant(a)):
                        iv, base = (a, b) if a in ivs else (b, a)
                        init, step, nxt = ivs[iv]
                        k = 1
                        kind = ("offset", base)
                    else:
                        continue
                    # the new value's start, computed in the preheader
                    counter[0] += 1
                    nm = f"%iv{counter[0]}"
                    start = f"{nm}.0"
                    if kind[0] == "scale":
                        pre.ins.insert(len(pre.ins) - 1, I("bin", start, [init, k], "mul"))
                        new_step = step * k
                    else:
                        pre.ins.insert(len(pre.ins) - 1, I("bin", start, [init, base], "add"))
                        new_step = step
                    # its φ in the header and its step beside the original variable's
                    nxt_new = f"{nm}.n"
                    phi = I("phi", nm, [start, nxt_new], [pre_label, latch])
                    lab[header].ins.insert(0, phi)
                    stepper = d[nxt]
                    blk = next(lab[x] for x in body if stepper in lab[x].ins)
                    blk.ins.insert(blk.ins.index(stepper) + 1, I("bin", nxt_new, [nm, new_step], "add"))
                    # the old computation is now a copy of the new variable
                    ins.op, ins.args, ins.k = "copy", [nm], None
                    ivs[ins.dst] = (start, new_step, nxt_new)
                    ivs[nm] = (start, new_step, nxt_new)
                    steppers.add(nxt_new)
                    d[nxt_new] = blk.ins[blk.ins.index(stepper) + 1]
                    inside |= {nm, nxt_new}
                    changed += 1
                    progress = True
    if changed:
        copyprop(f)
        dce(f)
    if stats is not None:
        stats["reduced"] = stats.get("reduced", 0) + changed
    return changed


# ---------------------------------------------------------------------------
def strength(f: Func) -> int:
    n = 0
    mapping = {}
    for b in f.blocks:
        keep = []
        for i in b.ins:
            if i.op == "bin":
                a, c = i.args
                if i.k in COMMUTE and not is_var(a) and is_var(c):
                    i.args = [c, a]
                    a, c = c, a
                if i.k == "mul" and not is_var(c) and c > 0 and c & (c - 1) == 0:
                    if c == 1:
                        mapping[i.dst] = a
                        n += 1
                        continue
                    i.k, i.args = "shl", [a, c.bit_length() - 1]
                    n += 1
                elif i.k in ("add", "sub", "or", "xor", "shl", "shr", "sar") and c == 0:
                    mapping[i.dst] = a
                    n += 1
                    continue
            keep.append(i)
        b.ins = keep
    replace_uses(f, mapping)
    return n


# ---------------------------------------------------------------------------
def inline(m: Module, limit: int = 40) -> int:
    """Copy small, non-recursive callees into their callers (on the non-SSA IR, before any other pass)."""
    funcs = {f.name: f for f in m.funcs}
    calls = {f.name: {i.k for i in f.instructions() if i.op == "call"} for f in m.funcs}

    def recursive(name, seen=()):
        return any(c == name or (c in calls and c not in seen and recursive(name, seen + (c,)))
                   for c in calls.get(name, ()))
    small = {n for n, f in funcs.items() if f.count() <= limit and not recursive(n) and n != "main"
             and not f.slots}
    done = 0
    for f in m.funcs:
        k = 0
        while True:
            site = None
            for bi, b in enumerate(f.blocks):
                for ii, i in enumerate(b.ins):
                    if i.op == "call" and i.k in small and i.k != f.name:
                        site = (bi, ii, i)
                        break
                if site:
                    break
            if not site:
                break
            bi, ii, call = site
            k += 1
            g = funcs[call.k]
            pre = f"{call.k}{k}_"
            ren = lambda v: f"%{pre}{v[1:]}" if is_var(v) else v
            b = f.blocks[bi]
            after = Block(f"{pre}ret", b.ins[ii + 1:])
            b.ins = b.ins[:ii]
            for p, a in zip(g.params, call.args):
                b.ins.append(I("copy", ren(p), [a]))
            b.ins.append(I("br", k=pre + g.blocks[0].label))
            new = []
            for gb in g.blocks:
                nb = Block(pre + gb.label)
                for gi in gb.ins:
                    if gi.op == "ret":
                        if call.dst:
                            nb.ins.append(I("copy", call.dst, [ren(gi.args[0]) if gi.args else 0]))
                        nb.ins.append(I("br", k=after.label))
                        continue
                    ni = I(gi.op, ren(gi.dst) if gi.dst else None, [ren(a) for a in gi.args], gi.k)
                    if gi.op == "br":
                        ni.k = pre + gi.k
                    elif gi.op == "cbr":
                        ni.k = tuple(pre + x for x in gi.k)
                    nb.ins.append(ni)
                new.append(nb)
            f.blocks[bi + 1:bi + 1] = new + [after]
            done += 1
        remove_unreachable(f)
    return done


# ---------------------------------------------------------------------------
PIPELINE = ("copyprop", "sccp", "copyprop", "strength", "gvn", "licm", "ivsr", "sccp", "copyprop", "gvn", "dce")


def optimize(f: Func, passes=PIPELINE, stats: dict | None = None) -> dict:
    counts = {}
    for p in passes:
        fn = globals()[p]
        if p in ("sccp", "licm", "ivsr"):
            r = fn(f, stats)
        else:
            r = fn(f)
        counts[p] = counts.get(p, 0) + r
    return counts
