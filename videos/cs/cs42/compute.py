"""Precompute everything numerical in Part 42 of *Computer Science, Built* ("The Browser and the Web").

    python -m videos.cs.cs42.compute              # everything missing
    python -m videos.cs.cs42.compute --force browser

Results are cached in ``.cache/cs42/<name>.json``; scenes call ``load(name)``.  The instruments are
``explainer/cs/web/`` (html, css, layout, events, js, vdom, platform); tests in tests/test_cs42_web.py.

Items:
    tokenize    the tokenizer's state on every character of a small snippet
    recover     six malformed inputs: the tree each produces and the repairs made
    specificity selectors sorted by specificity, and a cascade worked through
    matching    right-to-left against left-to-right selector matching over this series' README
    breaking    greedy against Knuth-Plass on a paragraph of Pride and Prejudice, and over 300 of its paragraphs
    kpgraph     the breakpoint graph of a short paragraph, with the optimal path
    flex        flex items growing and shrinking
    nesting     nested intrinsic sizing: layouts with and without a cache
    frames      a long task against the same work in chunks: frame timelines
    orderings   event-loop orderings for four programs
    ic          hidden classes and inline caches: monomorphic to megamorphic; transitions; deoptimization
    vdom        keyed against unkeyed list diffs; heuristic diff against tree edit distance; signals
    cache       an HTTP cache over an afternoon of requests
    crp         a page's critical rendering path (illustrative timings)
    cls         layout shifts grouped into session windows
    compress    gzip and other codecs on this repository's text
    cors        what the browser does with six cross-origin requests
    xss         an injected handler parsed by our parser, and the escaped version
    contrast    this series' palette against its background; the WCAG thresholds
    radio       a phone's radio: ten requests spread out against batched
    browser     the toy browser rendering this series' README
    relayout    incremental relayout: what one edited paragraph costs
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.tts import REPO_ROOT

CACHE = Cache("cs42")
load = CACHE.load

SNIPPET = '<p class=note>Hi <b>there</p>'
DARCY = None


def _readme():
    return (REPO_ROOT / "videos" / "cs" / "README.md").read_text()


def _paragraphs():
    from videos.cs.cs31.compute import _full_text
    t = _full_text().decode("latin-1")
    return [ln for ln in t.split("\n") if 110 < len(ln.split()) < 200]


def compute_tokenize() -> dict:
    from explainer.cs.web import html as H
    trace = []
    toks, errs = H.tokenize(SNIPPET, trace)
    return {"src": SNIPPET, "trace": trace, "tokens": [(k, t if isinstance(t, str) else
                                                        {"name": t["name"], "attrs": t["attrs"]}) for k, t in toks],
            "errors": errs}


def compute_recover() -> dict:
    from explainer.cs.web import html as H
    cases = ["<p>one<p>two", "<b><i>bold italic</b> italic?</i>", "<ul><li>a<li>b</ul>", "<div>a</span>b</div>",
             "<p>a < b and c > d", "<table><tr><td>x</table>"]
    out = []
    for c in cases:
        doc, errs, fixes = H.parse(c)
        out.append({"src": c, "outline": H.outline(doc), "errors": [e for e, _ in errs], "fixes": fixes})
    return {"cases": out}


def compute_specificity() -> dict:
    from explainer.cs.web import css as C, html as H
    sels = ["*", "p", "ul li", "p.lead", ".note p", "#main", "#main .note p", "div#main p.lead b", ".a.b.c",
            "html body div p"]
    ranked = sorted(sels, key=C.specificity)
    src = '<div id=main><div class=note><p class=lead>Hi <b>there</b></p></div><p>plain</p></div>'
    css = "p { color: grey }\n.note p { color: red }\n#main .note p { color: green }\np.lead { font-size: 18px }"
    doc, _, _ = H.parse(src)
    rules = C.parse_css(css)
    st = C.cascade(doc, rules)
    els = [n for n in doc.walk() if not n.tag.startswith("#")]
    rows = []
    for n in els:
        cands = [(s, C.specificity(s), order) for sels_, d, order in rules for s in sels_ if C.matches(n, s)]
        rows.append({"tag": n.tag, "attrs": n.attrs, "matched": cands, "style": st[id(n)]})
    return {"ranked": [(s, C.specificity(s)) for s in ranked], "src": src, "css": css, "elements": rows}


def compute_matching() -> dict:
    from explainer.cs.web import css as C, html as H
    readme, _, _ = H.parse(H.markdown_to_html(_readme()))
    page = C.synthetic_page(2000)
    sels = ["div .nav a", "ul li a.active", "section p span", ".card .title", "div div p", "div .warning b",
            "section ul li", ".note a", "div span.x", "li b"]
    depths = [C.depth(n) for n in page.walk()]
    return {"selectors": sels, "page": C.matching_cost(page, sels), "readme": C.matching_cost(readme, sels),
            "max_depth": max(depths), "mean_depth": sum(depths) / len(depths)}


def compute_breaking() -> dict:
    from explainer.cs.web import layout as L
    paras = _paragraphs()
    p = [x for x in paras if x.startswith('"Be not alarmed')][0]
    r = L.compare_breaking(p, line_width=360)
    better = same = 0
    ratio = []
    for q in paras[:300]:
        x = L.compare_breaking(q, line_width=360)
        gb, kb = x["greedy_stats"]["badness"], x["kp_stats"]["badness"]
        if kb < gb - 1e-9:
            better += 1
        else:
            same += 1
        ratio.append(kb / gb if gb else 1.0)
    ratio.sort()
    return {"paragraph": p, "words": r["words"], "widths": r["widths"], "space": r["space"], "line_width": 360,
            "greedy": r["greedy"], "kp": r["kp"], "greedy_stats": r["greedy_stats"], "kp_stats": r["kp_stats"],
            "corpus": {"paragraphs": better + same, "kp_better": better, "same": same,
                       "median_ratio": ratio[len(ratio) // 2]}}


def compute_kpgraph() -> dict:
    """Feasible breakpoints of a short paragraph and the optimal path."""
    from explainer.cs.web import layout as L
    text = ("It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in "
            "want of a wife.")
    f = L.font("serif", 16)
    words = text.split()
    widths = [L.width(w, f) for w in words]
    space = L.width(" ", f)
    lw = 190.0
    edges = []
    n = len(words)
    for i in range(n):
        w = -space
        for j in range(i + 1, n + 1):
            w += widths[j - 1] + space
            if w > lw:
                break
            slack = lw - w
            cost = 0.0 if j == n else 100 * (slack / lw) ** 3
            edges.append((i, j, cost))
    kp = L.knuth_plass(words, widths, space, lw)
    g = L.greedy(words, widths, space, lw)
    return {"words": words, "edges": edges, "kp": kp, "greedy": g, "line_width": lw,
            "kp_stats": L.line_stats(kp, widths, space, lw), "greedy_stats": L.line_stats(g, widths, space, lw)}


def compute_flex() -> dict:
    from explainer.cs.web import layout as L
    items = [(120, 1, 1), (200, 2, 1), (160, 0, 1)]
    return {"items": items, "cases": {w: L.flex(w, items) for w in (480, 720, 880, 360, 300)}}


def compute_nesting() -> dict:
    from explainer.cs.web import layout as L
    return {"rows": L.nesting_table()}


def compute_frames() -> dict:
    from explainer.cs.web import events as E
    return {"long": E.jank(120.0), "chunked": E.chunked(120.0, 8.0), "budget_ms": E.FRAME}


def compute_orderings() -> dict:
    from explainer.cs.web import events as E
    return E.ordering_examples()


def compute_ic() -> dict:
    from explainer.cs.web import js
    return {"sites": js.ic_experiment(), "transitions": js.transition_tree(),
            "deopt": js.deopt_trace([(1, 2), (3, 4), (5, 6), (7, 8), ("a", 1), (1, 2), (2, 3), (4, 5),
                                     (2 ** 31, 1), (1, 1), (2, 2), (3, 3)])}


def compute_vdom() -> dict:
    from explainer.cs.web import vdom as V
    return {"lists": V.list_experiment(100), "timing": V.diff_timing((10, 20, 40, 80, 120)),
            "signals": V.signals_demo()}


def compute_cache() -> dict:
    from explainer.cs.web import platform as P
    times = [0, 20, 45, 70, 130, 200, 260, 320, 400]
    return {"times": times, "plain": P.cache_sim(times, max_age=60, etag_changes=(300,)),
            "swr": P.cache_sim(times, max_age=60, swr=120, etag_changes=(300,))}


def compute_crp() -> dict:
    from explainer.cs.web import platform as P
    res = {"HTML": (120, 15, []), "CSS": (90, 10, ["HTML"]), "font": (110, 0, ["CSS"]),
           "JS (sync)": (140, 60, ["HTML"]), "hero image": (220, 0, ["HTML"])}
    base = P.critical_path({k: v for k, v in res.items() if k != "hero image"})
    deferred = dict(res)
    deferred["JS (sync)"] = (140, 60, ["HTML"])
    return {"resources": res, "blocking": base,
            "preloaded": P.critical_path({"HTML": (120, 15, []), "CSS": (90, 10, ["HTML"]),
                                          "font": (110, 0, ["HTML"])})}


def compute_cls() -> dict:
    from explainer.cs.web import platform as P
    shifts = [(0.8, 0.30, 0.10), (1.2, 0.25, 0.20), (1.6, 0.10, 0.05), (4.5, 0.50, 0.25), (9.0, 0.05, 0.05)]
    return {"shifts": shifts, **P.cls(shifts)}


def compute_compress() -> dict:
    import bz2
    import gzip
    import lzma
    files = ["videos/cs/README.md", "videos/cs/SYLLABUS.md", "explainer/cs/web/html.py"]
    out = []
    for f in files:
        b = (REPO_ROOT / f).read_bytes()
        row = {"file": f, "bytes": len(b), "gzip": len(gzip.compress(b, 9)), "bz2": len(bz2.compress(b, 9)),
               "xz": len(lzma.compress(b, preset=9))}
        try:
            import brotli
            row["brotli"] = len(brotli.compress(b, quality=11))
        except ImportError:
            pass
        out.append(row)
    return {"rows": out}


def compute_cors() -> dict:
    from explainer.cs.web import platform as P
    page = "https://shop.example/cart"
    cases = [("same origin", dict(target="https://shop.example/api/items")),
             ("another origin, no CORS header", dict(target="https://api.other.example/data")),
             ("another origin that allows us", dict(target="https://api.other.example/data",
                                                    allow_origin="https://shop.example")),
             ("a PUT with a JSON header", dict(target="https://api.other.example/data", method="PUT",
                                               headers=("X-Token",), allow_origin="https://shop.example",
                                               allow_methods=("PUT",), allow_headers=("X-Token",))),
             ("a PUT the server did not allow", dict(target="https://api.other.example/data", method="PUT")),
             ("cookies to an origin allowing *", dict(target="https://api.other.example/data", allow_origin="*",
                                                      credentials=True))]
    rows = [{"case": name, **P.cors(page, **kw)} for name, kw in cases]
    origins = [("https://a.example/x", "https://a.example/y"), ("https://a.example", "http://a.example"),
               ("https://a.example", "https://a.example:8443"), ("https://a.example", "https://b.a.example")]
    return {"rows": rows, "origins": [(a, b, P.same_origin(a, b)) for a, b in origins]}


def compute_xss() -> dict:
    import html as std
    from explainer.cs.web import html as H
    name = '<img src=x onerror="steal(document.cookie)">'
    raw = f"<p>Hello, {name}!</p>"
    esc = f"<p>Hello, {std.escape(name)}!</p>"
    d1, _, _ = H.parse(raw)
    d2, _, _ = H.parse(esc)
    handlers = [(n.tag, k, v) for n in d1.walk() for k, v in n.attrs.items() if k.startswith("on")]
    return {"name": name, "raw": raw, "escaped": esc, "raw_outline": H.outline(d1), "escaped_outline": H.outline(d2),
            "handlers": handlers}


def compute_contrast() -> dict:
    from explainer.style import C
    from explainer.cs.web import platform as P
    bg = "#121722"
    pal = {"DATA": C.CS_DATA, "HEAD": C.CS_HEAD, "YES": C.CS_TRUE, "NO": C.CS_FALSE, "LAM": "#9b8cd6",
           "KERN": "#d98c5f", "GREY_A": "#DDDDDD", "GREY_C": "#888888", "GREY_D": "#444444"}
    rows = []
    for k, v in pal.items():
        r = P.contrast(v, bg)
        rows.append({"name": k, "hex": v, "ratio": r, **P.wcag(r)})
    return {"bg": bg, "rows": rows, "grey_on_white": P.grey_threshold(), "black_white": P.contrast("#000000",
                                                                                                     "#ffffff"),
            "lum_bg": P.luminance(bg)}


def compute_radio() -> dict:
    from explainer.cs.web import platform as P
    return {"params": P.LTE, **P.batching(10, 20.0)}


def compute_browser() -> dict:
    from explainer.cs.web import layout as L
    out = CACHE.dir / "readme.png"
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    r = L.render_markdown(_readme(), str(out), page_width=900, limit=60, max_height=1400)
    return {**r, "png": str(out.relative_to(REPO_ROOT))}


def compute_relayout() -> dict:
    """With dirty bits, editing one paragraph re-breaks only its lines and shifts the blocks below it; without, the
    whole page is laid out again."""
    from explainer.cs.web import css, html, layout as L
    doc, _, _ = html.parse(html.markdown_to_html(_readme(), limit=60))
    styles = css.cascade(doc, css.parse_css(L.UA_CSS))
    boxes, h = L.layout(doc, 900, styles=styles)
    words = [len(b.runs) for b in boxes]
    k = len(boxes) // 2
    return {"blocks": len(boxes), "words": sum(words), "edited_block": k, "edited_words": words[k],
            "shifted_blocks": len(boxes) - k - 1}


def compute_pipeline() -> dict:
    """The toy browser's stages on the README, each timed (median of five runs, this machine), and what each stage
    produces at the top of the page; plus a render with every block's box outlined."""
    import statistics
    import time
    from explainer.cs.web import css, html, layout as L
    md = _readme()
    times = {k: [] for k in ("markdown", "tokenize", "tree", "cascade", "layout", "paint")}
    for _ in range(5):
        t0 = time.perf_counter()
        src = html.markdown_to_html(md, limit=60)
        t1 = time.perf_counter()
        toks, errs = html.tokenize(src)
        t2 = time.perf_counter()
        doc, fixes = html.build(toks)
        t3 = time.perf_counter()
        styles = css.cascade(doc, css.parse_css(L.UA_CSS))
        t4 = time.perf_counter()
        boxes, h = L.layout(doc, 900, styles=styles)
        t5 = time.perf_counter()
        out = CACHE.dir / "readme_boxes.png"
        L.paint(boxes, 900, min(h + 30, 1440), str(out), outline=True)
        t6 = time.perf_counter()
        for k, a, b in (("markdown", t0, t1), ("tokenize", t1, t2), ("tree", t2, t3), ("cascade", t3, t4),
                        ("layout", t4, t5), ("paint", t5, t6)):
            times[k].append((b - a) * 1e3)
    first = [n for n in doc.walk() if n.tag in ("h1", "p", "li", "code", "b")]
    seen, styled = set(), []
    for n in first:
        if n.tag not in seen:
            seen.add(n.tag)
            styled.append({"tag": n.tag, "style": styles[id(n)]})
    return {"ms": {k: statistics.median(v) for k, v in times.items()}, "markdown": md.splitlines()[:5],
            "html": src.splitlines()[:4], "tokens": len(toks), "outline": html.outline(doc)[:14], "styles": styled,
            "png": str(out.relative_to(REPO_ROOT))}


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
