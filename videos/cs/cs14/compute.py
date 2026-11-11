"""Precompute everything numerical in Part 14 of *Computer Science, Built* ("Lambda and Types").

    python -m videos.cs.cs14.compute              # everything missing
    python -m videos.cs.cs14.compute --force hm

Results are cached in ``.cache/cs14/<name>.json``; scenes call ``load(name)``.  The instruments are
``explainer/cs/lam.py`` (Part 1's terms, substitution and normal order) and ``explainer/cs/lang/lam/``: ``reduce``
(strategies, sharing, the reduction graph, de Bruijn, Church encodings), ``stlc`` (typing derivations, small-step
evaluation, the safety theorems checked), ``ml`` (the λ-core: Hindley–Milner inference and an evaluator, with the
Job written in it) and ``logic`` (proof search as program search, Kripke countermodels), tested in
tests/test_cs14_types.py.

Items:
    hook       the Job in the λ-core with every type inferred; 2 + 3 in pure λ
    subst      free and bound variables; a capture, and how renaming avoids it
    beta       2 + 3 step by step; Ω; a term with a normal form and an infinite path
    church     booleans, numerals and arithmetic, the predecessor by Kleene's trick: steps against n
    fix        Y unfolding; factorial through Y in normal order; Z under call-by-value
    strategies four strategies on K a Ω; how often an argument is evaluated by name, by need and by value
    confluence the whole reduction graph of small terms; complete developments; de Bruijn indices
    stlc       a typing derivation; a small-step trace with its rules; ill-typed terms that get stuck
    safety     progress and preservation on thousands of random well-typed terms; how long they run
    normal     untyped terms exhausting a finite step budget, compared with a typed sample; Ω is untypable
    hm         unification traced; let-polymorphism; errors; the Job's types; the doubly exponential let
    systemf    free theorems (map f ∘ rev = rev ∘ map f, …) checked on random lists in the λ-core
    curry      fifteen formulas: truth tables, programs found by proof search, Kripke countermodels
    linear     which classic combinators use their argument exactly once, at most once, at least once
    frontier   inference time and type size against let-nesting; inference time against program size
    rust       rustc on a use after move and a borrow conflict: affine types at work
    gradual    tsc --strict accepts an unsound covariant array and an any; node then fails
"""

from __future__ import annotations

import random
import time

import json
from pathlib import Path
from explainer.ai.cache import Cache
from explainer.cache_lock import locked_item

SCHEMAS = {"fix": 2, "systemf": 2, "safety": 2}


class TypesCache(Cache):
    @locked_item(lambda self, name: self.path(name))
    def load(self, name):
        if name in SCHEMAS and not cache_current(name, self.path(name)):
            self.save(name, ITEMS[name]())
        return super().load(name)


def cache_current(name, path=None):
    path = CACHE.path(name) if path is None else path
    return (name not in SCHEMAS or
            (path.exists() and json.loads(path.read_text()).get("schema") == SCHEMAS[name]))

CACHE = TypesCache("cs14")


def load(name):
    # Resolve the instance method at call time: cached-only QA must reject stale data first.
    return CACHE.load(name)


def _steps(t, strategy="normal", max_steps=5000):
    from explainer.cs.lang.lam import reduce as R
    return R.run(t, strategy, max_steps)


def compute_hook() -> dict:
    from explainer.cs.lam import church, normalize, show, unchurch
    from explainer.cs.lang.lam import ml as M
    from explainer.cs.lang.lam import reduce as R
    prog = M.parse(M.JOB_ML + "\n;; job text")
    types, body, I = M.infer_program(prog, env={"text": M.T("list", M.INT)})
    t = R.apply(R.lib("plus"), church(2), church(3))
    steps = normalize(t)
    return {"types": types, "unify_calls": I.unify_calls, "source": M.JOB_ML.strip().splitlines(),
            "plus": [show(s.term) for s in steps], "plus_value": unchurch(steps[-1].term)}


def compute_subst() -> dict:
    from explainer.cs.lam import App, Var, free, parse, show, subst
    t = parse(r"\x. f x y")
    cap = parse(r"\y. x")
    return {"free": sorted(free(t)), "term": show(t),
            "capture_naive": r"\y. y", "capture_right": show(subst(cap, "x", Var("y"))),
            "alpha": [show(parse(r"\x. x")), show(parse(r"\y. y"))]}


def compute_beta() -> dict:
    from explainer.cs.lam import church, normalize, parse, show, tex
    from explainer.cs.lang.lam import reduce as R
    t = R.apply(R.lib("plus"), church(2), church(3))
    steps = normalize(t)
    om = R.lib("omega")
    om1 = R.step(om)
    k = parse(r"(\x y. y) ((\x. x x) (\x. x x)) z")
    return {"plus": [{"term": show(s.term), "tex": tex(s.term, redex=s.redex)} for s in steps],
            "omega": [show(om), show(om1)], "omega_same": om1 == om,
            "k": show(k), "k_normal": _steps(k, "normal")[0], "k_applicative": _steps(k, "applicative", 300)[0]}


def compute_church() -> dict:
    from explainer.cs.lam import church, show, unchurch
    from explainer.cs.lang.lam import reduce as R
    L = R.lib
    ops = []
    for name, f, args in (("plus", lambda a, b: a + b, (3, 4)), ("times", lambda a, b: a * b, (3, 4)),
                          ("pow", lambda a, b: a ** b, (2, 3))):
        k, t = _steps(R.apply(L(name), church(args[0]), church(args[1])))
        ops.append({"op": name, "args": args, "value": unchurch(t), "want": f(*args), "steps": k})
    pred = []
    for n in range(0, 11):
        k, t = _steps(R.apply(L("pred"), church(n)))
        pred.append({"n": n, "value": unchurch(t), "steps": k})
    bools = []
    for a in ("true", "false"):
        for b in ("true", "false"):
            for op in ("and", "or"):
                k, t = _steps(R.apply(L(op), L(a), L(b)))
                bools.append({"op": op, "a": a, "b": b, "result": "true" if t == L("true") else
                              ("false" if t == L("false") else show(t)), "steps": k})
    return {"ops": ops, "pred": pred, "bools": bools, "lib": {k: R.LIB[k] for k in
                                                               ("true", "false", "and", "or", "not", "succ", "plus",
                                                                "times", "pow", "pair", "fst", "snd", "pred",
                                                                "nil", "cons")}}


def compute_fix() -> dict:
    from explainer.cs.lam import App, Var, church, parse, show, unchurch
    from explainer.cs.lang.lam import reduce as R
    L = R.lib
    yf = App(L("Y"), Var("g"))
    s1 = R.step(yf)
    s2 = R.step(s1)
    # factorial through Y, with the Church library inlined
    F = parse(r"\fact n. (\b x y. b x y) ((\n. n (\z t f. f) (\t f. t)) n) (\f x. f x) "
              r"((\m n f. m (n f)) n (fact ((" + R.LIB["pred"] + r") n)))")
    rows = []
    for n in range(0, 5):
        k, t = _steps(R.apply(L("Y"), F, church(n)), "normal", 200000)
        rows.append({"n": n, "value": unchurch(t), "steps": k})
    # Returning a closure is weaker than successfully evaluating a factorial call.
    observations = {}
    for name, term in (("Y F", App(L("Y"), F)), ("Z F", App(L("Z"), F)),
                       ("Z F 0", R.apply(L("Z"), F, church(0)))):
        try:
            R.lazy_eval(term, "value", fuel=20000)
            observations[name] = "closure returned"
        except R.Diverge:
            observations[name] = "fuel limit reached"
    strict = []
    for n in range(4):
        value, stats = R.read_number(R.apply(L("Z"), delayed_factorial(), church(n)), "value")
        strict.append({"n": n, "value": value, "beta": stats["beta"], "evals": stats["evals"]})
    return {"schema": SCHEMAS["fix"], "unfold": [show(yf), show(s1), show(s2)], "fact": rows,
            "closure_observations": observations, "fuel": 20000, "strict_fact": strict,
            "strict_function": show(delayed_factorial()), "Y": R.LIB["Y"], "Z": R.LIB["Z"]}


def delayed_factorial():
    """A Church factorial functional with both conditional branches delayed for CBV."""
    from explainer.cs.lam import Lam, Var, church
    from explainer.cs.lang.lam import reduce as R
    n, fact = Var("n"), Var("fact")
    unit = Lam("u", Var("u"))
    return Lam("fact", Lam("n", R.apply(
        R.apply(R.lib("iszero"), n),
        Lam("unused", church(1)),
        Lam("unused", R.apply(R.lib("times"), n, R.apply(fact, R.apply(R.lib("pred"), n)))),
        unit)))



def compute_strategies() -> dict:
    from explainer.cs.lam import App, Var, church, parse, show
    from explainer.cs.lang.lam import reduce as R
    L = R.lib
    k = R.apply(parse(r"\x y. x"), Var("a"), L("omega"))
    table = []
    for s in ("normal", "applicative", "name", "value"):
        n, t = R.run(k, s, max_steps=300)
        table.append({"strategy": s, "steps": n, "result": show(t) if n is not None else None})
    share = []
    for label, body in (("x used 3 times", r"\pl x. pl x (pl x x)"), ("x used once", r"\pl x. x"),
                        ("x never used", r"\pl x. (\f z. z)")):
        term = R.apply(R.apply(parse(body), L("plus")), R.apply(L("times"), church(3), church(3)))
        row = {"label": label}
        for mode in ("name", "need", "value"):
            v, st = R.read_number(term, mode)
            row[mode] = {"value": v, "beta": st["beta"], "evals": st["evals"]}
        share.append(row)
    return {"k": show(k), "table": table, "share": share}


def compute_confluence() -> dict:
    from explainer.cs.lam import parse, show
    from explainer.cs.lang.lam import reduce as R
    out = {}
    for name, src in (("small", r"(\x. x x) ((\y. y) z)"), ("pair", r"(\x y. y x) ((\a. a) b) ((\c. c) d)")):
        nodes, edges, normal = R.graph(parse(src))
        out[name] = {"nodes": [show(n) for n in nodes], "edges": [[i, j] for i, j, _ in edges], "normal": normal,
                     "confluent": R.confluent(parse(src)),
                     "develop": show(R.develop(parse(src)))}
    big = parse(r"(\x. x x) ((\y. (\z. z) y) ((\w. w) v))")
    nodes, edges, normal = R.graph(big, limit=500)
    depth = {0: 0}
    for i, j, _ in edges:                     # breadth-first order: a node's depth is set by its first parent
        if j not in depth:
            depth[j] = depth[i] + 1
    out["big"] = {"source": show(big), "nodes": len(nodes), "edges": len(edges), "normal": len(normal),
                  "confluent": R.confluent(big, 500), "edge_list": [[i, j] for i, j, _ in edges],
                  "depth": [depth[k] for k in range(len(nodes))], "normal_index": normal}
    db = {}
    for src in (r"\x. x", r"\f x. f (f x)", r"\x y. y x", r"\f. (\x. f (x x)) (\x. f (x x))"):
        db[show(parse(src))] = R.show_db(R.debruijn(parse(src)))
    out["debruijn"] = db
    return out


def compute_stlc() -> dict:
    from explainer.cs.lang.lam import stlc as S
    t = S.parse(r"(\f:Nat->Nat. \x:Nat. f (f x)) (\y:Nat. succ y) 3")
    T, d = S.typecheck(t)

    def view(d):
        rule, ctx, term, typ, prem = d
        return {"rule": rule, "ctx": {k: S.ttex(v) for k, v in ctx.items()}, "term": S.show(term),
                "type": S.ttex(typ), "premises": [view(p) for p in prem]}
    small = S.parse(r"(\x:Nat. succ x) 2")
    T2, d2 = S.typecheck(small)
    return {"term": S.show(t), "type": S.tshow(T), "size": S.deriv_size(d),
            "small": S.show(small), "small_deriv": view(d2),
            "trace": [{"term": S.show(u), "rule": r} for u, r in S.trace(t)],
            "stuck": S.stuck_examples()}


def compute_safety() -> dict:
    from explainer.cs.lang.lam import stlc as S
    t0 = time.time()
    r = S.safety(5000, 6, seed=14)
    rng = random.Random(14)
    hist = {}
    for i in range(5000):
        T = [S.BOOL, S.NAT, S.arrow(S.NAT, S.NAT), S.arrow(S.BOOL, S.NAT)][i % 4]
        t = S.gen(T, 6, rng)
        k = len(S.trace(t)) - 1
        hist[k] = hist.get(k, 0) + 1
    r["hist"] = sorted(hist.items())
    assert sum(hist.values()) == r["terms"]
    assert sum(k*v for k,v in hist.items()) == r["steps_checked"]
    assert max(hist) == r["max_steps"]
    r.update(schema=SCHEMAS["safety"], generator_seed=14, generator_depth=6,
             type_cycle=["Bool", "Nat", "Nat->Nat", "Bool->Nat"])
    r["seconds"] = time.time() - t0
    return r


def compute_normal() -> dict:
    """Random closed untyped terms: how many reach a normal form; and the same for well-typed terms."""
    from explainer.cs.lam import App, Lam, Var
    from explainer.cs.lang.lam import reduce as R
    from explainer.cs.lang.lam import ml as M

    rng = random.Random(7)

    def gen(depth, env):
        r = rng.random()
        if depth <= 0:
            return Var(rng.choice(env)) if env else Lam("v0", Var("v0"))
        if env and r < 0.3:
            return Var(rng.choice(env))
        if r < 0.6:
            x = f"v{len(env)}"
            return Lam(x, gen(depth - 1, env + [x]))
        return App(gen(depth - 1, env), gen(depth - 1, env))
    stop = diverge = 0
    for _ in range(2000):
        t = gen(7, [])
        n, _ = R.run(t, "normal", max_steps=400, max_size=3000)
        if n is None:
            diverge += 1
        else:
            stop += 1
    om = None
    try:
        M.infer_expr(M.parse_expr("fun x -> x x"))
    except M.TypeErr as e:
        om = str(e)
    return {"untyped_terms": 2000, "untyped_stop": stop, "untyped_no_stop": diverge, "omega_error": om}


def compute_hm() -> dict:
    from explainer.cs.lang.lam import ml as M
    out = {}
    t, I = M.infer_expr(M.parse_expr("fun f x -> f (f x)"), trace=True)
    out["twice"] = {"type": M.show_type(t), "trace": I.trace}
    t, I = M.infer_expr(M.parse_expr("fun f g x -> f (g x)"), trace=True)
    out["compose"] = {"type": M.show_type(t), "trace": I.trace}
    cases = []
    for src in ("let id = fun x -> x in (id 1, id true)", "fun id -> (id 1, id true)", "fun x -> x x",
                "fun x -> x + 1", "fun x -> if x then 1 else 0", "fun l -> match l with [] -> 0 | h :: t -> h + 1",
                "1 + true"):
        try:
            t, _ = M.infer_expr(M.parse_expr(src))
            cases.append({"src": src, "type": M.show_type(t), "error": None})
        except M.TypeErr as e:
            cases.append({"src": src, "type": None, "error": str(e)})
    out["cases"] = cases
    prog = M.parse(M.JOB_ML + "\n;; job text")
    types, body, I = M.infer_program(prog, env={"text": M.T("list", M.INT)})
    out["job"] = {"types": types, "body": body, "unify_calls": I.unify_calls}
    rows = []
    for n in range(1, 6):
        t0 = time.time()
        t, I = M.infer_expr(M.parse_expr(M.exp_let(n)))
        dt = time.time() - t0
        rows.append({"n": n, "log2_size": M.type_size(t).bit_length() - 1, "unify_calls": I.unify_calls, "seconds": dt,
                     "shown": M.show_type(t) if n <= 2 else None})
    out["exp"] = rows
    out["exp_source"] = M.exp_let(3).splitlines()
    return out


def compute_systemf() -> dict:
    """Finite shape-only map-commutation checks and explicit failures outside parametricity."""
    from explainer.cs.lang.lam import ml as M
    lib = r"""
let rec map f l = match l with [] -> [] | h :: t -> f h :: map f t
let rec rev_onto l acc = match l with [] -> acc | h :: t -> rev_onto t (h :: acc)
let rev l = rev_onto l []
let rec take n l = if n = 0 then [] else (match l with [] -> [] | h :: t -> h :: take (n - 1) t)
let rec evens l = match l with [] -> [] | h :: t -> (match t with [] -> [h] | h2 :: t2 -> h :: evens t2)
let rec dup l = match l with [] -> [] | h :: t -> h :: h :: dup t
"""
    gs = {"rev": "rev", "take 3": "take 3", "evens": "evens", "dup": "dup"}
    rng = random.Random(11)
    out = []
    for name, g in gs.items():
        prog = M.parse(lib + f";; fun f -> fun l -> (map f ({g} l), {g} (map f l))")
        types, body, _ = M.infer_program(M.parse(lib + f";; {g}"))
        ok = 0
        trials = 200
        for _ in range(trials):
            l = [rng.randrange(-50, 50) for _ in range(rng.randrange(0, 9))]
            a, b = rng.randrange(-5, 6), rng.randrange(-5, 6)
            f = (lambda x, a=a, b=b: a * x + b)
            fn = M.evaluate(prog)
            # apply the closure from Python: build a tiny program instead
            p2 = M.parse(lib + f";; (map f ({g} l), {g} (map f l))")
            r = M.evaluate(p2, env={"f": f, "l": M.from_list(l)})
            ok += M.to_list(r[0]) == M.to_list(r[1])
        out.append({"g": name, "type": body, "trials": trials, "held": ok})
    # a function of type int list -> int list is free to break it
    p3 = M.parse(lib + ";; (map f (map (fun x -> x + 1) l), map (fun x -> x + 1) (map f l))")
    r = M.evaluate(p3, env={"f": lambda x: 2 * x, "l": M.from_list([1, 2, 3])})
    out.append({"g": "add one (int list -> int list)", "type": "int list -> int list", "trials": 1,
                "held": int(M.to_list(r[0]) == M.to_list(r[1]))})
    # This toy core permits unrestricted structural equality. Its printed polymorphic
    # type alone therefore does not establish System F relational parametricity.
    source = EQUALITY_SELECTOR
    types, _, _ = M.infer_program(M.parse(source + ";; g"))
    pair = M.evaluate(M.parse(source + ";; (g l, g mapped)"),
                      env={"l": M.from_list([1, 2]), "mapped": M.from_list([0, 0])})
    left = [0 for _ in M.to_list(pair[0])]
    right = M.to_list(pair[1])
    out.append({"g": "g", "type": types[0][1], "trials": 1,
                "held": int(left == right)})
    return {"schema": SCHEMAS["systemf"], "rows": out,
            "equality_counterexample": {"source": source, "input": [1, 2], "mapped_input": [0, 0],
                                        "map_after_g": left, "g_after_map": right}}


EQUALITY_SELECTOR = ("let g l = match l with [] -> [] | h :: t -> "
                     "match t with [] -> [] | j :: rest -> if h = j then [h] else []\n")


def compute_curry() -> dict:
    from explainer.cs.lang.lam import logic as LG
    return {"rows": LG.table()}


def compute_linear() -> dict:
    from explainer.cs.lam import parse, show

    def uses(t, x):
        k = t[0]
        if k == "var":
            return 1 if t[1] == x else 0
        if k == "lam":
            return 0 if t[1] == x else uses(t[2], x)
        return uses(t[1], x) + uses(t[2], x)

    def kind(t):
        counts = []
        while t[0] == "lam":
            counts.append(uses(t[2], t[1]))
            t = t[2]
        if all(c == 1 for c in counts):
            return counts, "linear"
        if all(c <= 1 for c in counts):
            return counts, "affine"
        if all(c >= 1 for c in counts):
            return counts, "relevant"
        return counts, "unrestricted"
    rows = []
    for name, src in (("I", r"\x. x"), ("B (compose)", r"\f g x. f (g x)"), ("C (flip)", r"\f x y. f y x"),
                      ("K (const)", r"\x y. x"), ("W (duplicate)", r"\f x. f x x"),
                      ("S", r"\x y z. x z (y z)")):
        counts, k = kind(parse(src))
        rows.append({"name": name, "term": show(parse(src)), "uses": counts, "kind": k})
    return {"rows": rows}


def compute_frontier() -> dict:
    from explainer.cs.lang.lam import ml as M
    rows = []
    for n in range(1, 9):
        t0 = time.time()
        t, I = M.infer_expr(M.parse_expr(M.exp_let(n)))
        rows.append({"n": n, "seconds": time.time() - t0, "log2_size": M.type_size(t).bit_length() - 1,
                     "unify_calls": I.unify_calls})
    # inference time against program size: k copies of the Job's definitions (later ones shadow earlier ones)
    sizes = []
    for k in (1, 2, 4, 8, 16, 32):
        prog = M.parse(M.JOB_ML * k + "\n;; 0")
        t0 = time.time()
        _, _, I = M.infer_program(prog)
        sizes.append({"copies": k, "defs": len(prog["defs"]), "seconds": time.time() - t0,
                      "unify_calls": I.unify_calls})
    return {"exp": rows, "scale": sizes}


RUST_MOVE = r"""fn main() {
    let word = String::from("truth");
    let kept = word;               // ownership moves to kept
    println!("{}", word);          // word was moved
    println!("{}", kept);
}
"""

RUST_BORROW = r"""fn main() {
    let mut counts = vec![1, 2, 3];
    let first = &counts[0];        // a shared borrow
    counts.push(4);                // a mutation while it is alive
    println!("{}", first);
}
"""

TS_COVARIANT = r"""class Animal { name = "animal"; }
class Dog extends Animal { bark(): string { return "woof"; } }
class Cat extends Animal { }

const dogs: Dog[] = [new Dog()];
const animals: Animal[] = dogs;     // allowed: arrays are covariant
animals.push(new Cat());            // allowed: a Cat is an Animal
console.log(dogs[1].bark());        // type-checks; fails when it runs
"""

TS_ANY = r"""function len(s: string): number { return s.length; }
const x: any = 42;
console.log(len(x) + 1);            // any switches the checker off: NaN at run time
"""


def compute_rust() -> dict:
    import subprocess
    import tempfile
    from pathlib import Path
    out = {}
    with tempfile.TemporaryDirectory() as d:
        for name, src in (("move", RUST_MOVE), ("borrow", RUST_BORROW)):
            f = Path(d) / f"{name}.rs"
            f.write_text(src)
            r = subprocess.run(["rustc", "--edition", "2021", "-o", str(Path(d) / name), str(f)], capture_output=True,
                               text=True)
            lines = [l for l in r.stderr.splitlines() if l.strip()]
            out[name] = {"source": src.strip().splitlines(), "ok": r.returncode == 0,
                         "error": next((l for l in lines if l.startswith("error")), None),
                         "notes": [l.strip() for l in lines if "value moved" in l or "borrow" in l or "move occurs"
                                   in l][:4]}
        ver = subprocess.run(["rustc", "--version"], capture_output=True, text=True).stdout.strip()
    out["version"] = ver
    return out


def compute_gradual() -> dict:
    import subprocess
    import tempfile
    from pathlib import Path
    out = {}
    with tempfile.TemporaryDirectory() as d:
        for name, src in (("covariant", TS_COVARIANT), ("any", TS_ANY)):
            f = Path(d) / f"{name}.ts"
            f.write_text(src)
            tc = subprocess.run(["tsc", "--strict", "--target", "es2020", "--outDir", d, str(f)], capture_output=True,
                                text=True)
            run = subprocess.run(["node", str(Path(d) / f"{name}.js")], capture_output=True, text=True)
            err = [l for l in run.stderr.splitlines() if "Error" in l]
            out[name] = {"source": src.strip().splitlines(), "tsc_errors": tc.stdout.strip() or None,
                         "stdout": run.stdout.strip(), "runtime_error": err[0].strip() if err else None}
        out["tsc"] = subprocess.run(["tsc", "--version"], capture_output=True, text=True).stdout.strip()
        out["node"] = subprocess.run(["node", "--version"], capture_output=True, text=True).stdout.strip()
    return out


ITEMS = {
    "hook": compute_hook, "subst": compute_subst, "beta": compute_beta, "church": compute_church,
    "fix": compute_fix, "strategies": compute_strategies, "confluence": compute_confluence, "stlc": compute_stlc,
    "safety": compute_safety, "normal": compute_normal, "hm": compute_hm, "systemf": compute_systemf,
    "curry": compute_curry, "linear": compute_linear, "frontier": compute_frontier,
    "rust": compute_rust, "gradual": compute_gradual,
}

if __name__ == "__main__":
    # Upgrade only the three changed schemas; preserve the other fourteen original payloads.
    for name in SCHEMAS:
        if CACHE.path(name).exists() and not cache_current(name, CACHE.path(name)):
            CACHE.load(name)
    CACHE.main(ITEMS, __doc__)
