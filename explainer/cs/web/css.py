"""A small CSS engine (Part 42): selectors with tag, class, id and descendant combinators; specificity as the
lexicographic triple (ids, classes, tags); the cascade by origin, specificity and order; inheritance; and the cost
of matching selectors right to left against left to right."""

from __future__ import annotations

import re

INHERITED = {"color", "font-size", "font-weight", "font-style", "font-family", "line-height", "text-align"}


def parse_css(src: str):
    """Rules as (selectors, declarations, order)."""
    rules = []
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    for k, m in enumerate(re.finditer(r"([^{}]+)\{([^}]*)\}", src)):
        sels = [s.strip() for s in m.group(1).split(",") if s.strip()]
        decls = {}
        for d in m.group(2).split(";"):
            if ":" in d:
                p, v = d.split(":", 1)
                decls[p.strip()] = v.strip()
        rules.append((sels, decls, k))
    return rules


def compound(s: str):
    """A compound selector like div.note#main -> (tag or None, classes, ids)."""
    tag = re.match(r"^[a-z0-9*]+", s)
    return (tag.group(0) if tag and tag.group(0) != "*" else None, re.findall(r"\.([\w-]+)", s),
            re.findall(r"#([\w-]+)", s))


def specificity(sel: str):
    a = b = c = 0
    for part in sel.split():
        t, cls, ids = compound(part)
        a += len(ids)
        b += len(cls)
        c += 1 if t else 0
    return (a, b, c)


def _matches_compound(node, comp):
    t, cls, ids = comp
    if node is None or node.tag.startswith("#"):
        return False
    if t and node.tag != t:
        return False
    have = node.attrs.get("class", "").split()
    if any(c not in have for c in cls):
        return False
    if ids and node.attrs.get("id") not in ids:
        return False
    return True


def matches(node, sel: str, counter=None):
    """Right to left: test the last compound on the node itself, then walk up for each earlier compound."""
    parts = [compound(p) for p in sel.split()]
    if counter is not None:
        counter[0] += 1
    if not _matches_compound(node, parts[-1]):
        return False
    anc = node.parent
    for comp in reversed(parts[:-1]):
        while anc is not None and not _matches_compound(anc, comp):
            if counter is not None:
                counter[0] += 1
            anc = anc.parent
        if anc is None:
            return False
        anc = anc.parent
    return True


def cascade(doc, rules, ua=None):
    """Computed style for every element: user-agent rules first, then author rules ordered by specificity and source
    order; inherited properties copied from the parent when unset."""
    ua = ua or []
    out = {}
    for node in doc.walk():
        if node.tag.startswith("#"):
            continue
        cands = []
        for origin, rs in ((0, ua), (1, rules)):
            for sels, decls, order in rs:
                for s in sels:
                    if matches(node, s):
                        cands.append(((origin, specificity(s), order), decls))
        style = {}
        for _, decls in sorted(cands, key=lambda x: x[0]):
            style.update(decls)
        style.update(_inline(node))
        par = out.get(id(node.parent), {})
        for p in INHERITED:
            if p not in style and p in par:
                style[p] = par[p]
        out[id(node)] = style
    return out


def _inline(node):
    s = node.attrs.get("style", "")
    d = {}
    for part in s.split(";"):
        if ":" in part:
            k, v = part.split(":", 1)
            d[k.strip()] = v.strip()
    return d


def matching_cost(doc, selectors):
    """How many element tests each strategy makes over the whole document.  Right to left starts from each element
    and fails fast on the last compound; left to right starts from every element matching the first compound and
    searches its whole subtree."""
    rl = [0]
    lr = 0
    nodes = [n for n in doc.walk() if not n.tag.startswith("#")]
    for s in selectors:
        for n in nodes:
            matches(n, s, rl)
        parts = [compound(p) for p in s.split()]
        for n in nodes:
            lr += 1
            if _matches_compound(n, parts[0]) and len(parts) > 1:
                lr += sum(1 for d in n.walk() if not d.tag.startswith("#")) - 1
    return {"right_to_left": rl[0], "left_to_right": lr, "elements": len(nodes), "selectors": len(selectors)}


def synthetic_page(n=2000, seed=0):
    """A deep page shaped like a real one: nested div and section wrappers, lists, paragraphs and inline spans, with
    a few classes; n elements."""
    import random
    from explainer.cs.web.html import Node
    rng = random.Random(seed)
    doc = Node("#document")
    body = doc.append(Node("body"))
    open_ = [(body, 1)]
    count = 1
    classes = ["card", "title", "nav", "item", "active", "note", "warning", "x", "y"]
    while count < n:
        par, d = rng.choice(open_[-40:])
        tag = rng.choice(["div", "div", "div", "section", "ul", "li", "p", "span", "a", "b"])
        attrs = {"class": rng.choice(classes)} if rng.random() < 0.3 else {}
        el = par.append(Node(tag, attrs=attrs))
        count += 1
        if tag in ("div", "section", "ul", "li", "p") and d < 24:
            open_.append((el, d + 1))
    return doc


def depth(node):
    d, x = 0, node
    while x.parent is not None:
        d += 1
        x = x.parent
    return d
