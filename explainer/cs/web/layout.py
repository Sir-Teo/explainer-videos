"""Layout (Part 42): block and inline layout with greedy line breaking, Knuth and Plass's optimal line breaking by
dynamic programming, the flexbox grow/shrink algorithm, and a rasterizer that paints the result with real fonts."""

from __future__ import annotations

from dataclasses import dataclass, field

from PIL import Image, ImageDraw, ImageFont

FONTS = {"serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
         "serif-bold": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
         "mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
         "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
         "sans-bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
         "serif-italic": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
         "cjk": "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
         "cjk-bold": "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"}
_cache: dict = {}


def font(kind: str, size: int):
    k = (kind, size)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(FONTS[kind], size, index=2 if kind.startswith("cjk") else 0)
    return _cache[k]


def fallback(kind: str, word: str) -> str:
    """Font fallback, as a browser does it: a font without glyphs for a script hands the run to one that has
    them."""
    if any("\u3000" <= ch <= "\u9fff" or "\uff00" <= ch <= "\uffef" for ch in word):
        return "cjk-bold" if kind.endswith("bold") else "cjk"
    return kind


def width(word: str, f) -> float:
    return f.getlength(word)


# ---------------------------------------------------------------- line breaking

def greedy(words, widths, space: float, line_width: float):
    """First fit: put each word on the current line if it fits."""
    lines, cur, w = [], [], 0.0
    for i, ww in enumerate(widths):
        need = ww if not cur else w + space + ww
        if cur and need > line_width:
            lines.append(cur)
            cur, w = [i], ww
        else:
            cur.append(i)
            w = need
    if cur:
        lines.append(cur)
    return lines


def knuth_plass(words, widths, space: float, line_width: float):
    """Optimal breaks: minimize the sum over lines (except the last) of the cube of the shortfall ratio, plus a large
    penalty for overfull lines; dynamic programming over breakpoints, Part 19's paradigm."""
    n = len(widths)
    best = [0.0] + [float("inf")] * n
    prev = [0] * (n + 1)
    for j in range(1, n + 1):
        w = -space
        for i in range(j - 1, -1, -1):
            w += widths[i] + space
            if w > line_width and i < j - 1:
                break
            if j == n:
                cost = 0.0
            else:
                slack = line_width - w
                cost = 1e9 if slack < 0 else 100.0 * (slack / line_width) ** 3
            if best[i] + cost < best[j]:
                best[j] = best[i] + cost
                prev[j] = i
    lines, j = [], n
    while j > 0:
        i = prev[j]
        lines.append(list(range(i, j)))
        j = i
    return lines[::-1]


def line_stats(lines, widths, space, line_width):
    slack = []
    for k, ln in enumerate(lines):
        w = sum(widths[i] for i in ln) + space * (len(ln) - 1)
        if k < len(lines) - 1:
            slack.append(line_width - w)
    import statistics
    return {"lines": len(lines), "max_slack": max(slack) if slack else 0.0,
            "mean_slack": statistics.mean(slack) if slack else 0.0,
            "sd_slack": statistics.pstdev(slack) if slack else 0.0,
            "badness": sum(100 * (s / line_width) ** 3 for s in slack)}


def compare_breaking(text: str, line_width: float = 420.0, size: int = 16):
    f = font("serif", size)
    words = text.split()
    widths = [width(w, f) for w in words]
    space = width(" ", f)
    g = greedy(words, widths, space, line_width)
    k = knuth_plass(words, widths, space, line_width)
    return {"words": words, "widths": widths, "space": space, "line_width": line_width,
            "greedy": g, "kp": k, "greedy_stats": line_stats(g, widths, space, line_width),
            "kp_stats": line_stats(k, widths, space, line_width)}


# ---------------------------------------------------------------- flexbox

def flex(container: float, items):
    """The flexible-length algorithm, simplified: items (basis, grow, shrink).  Free space is shared by grow
    factors; negative free space is taken in proportion to shrink factor times basis."""
    basis = [b for b, _, _ in items]
    free = container - sum(basis)
    if free >= 0:
        g = sum(gr for _, gr, _ in items)
        sizes = [b + (free * gr / g if g else 0) for b, gr, _ in items]
    else:
        ws = sum(s * b for b, _, s in items)
        sizes = [b + (free * s * b / ws if ws else 0) for b, _, s in items]
    return {"free": free, "sizes": sizes}


# ---------------------------------------------------------------- block and inline layout, and painting

@dataclass
class Box:
    x: float
    y: float
    w: float
    h: float
    kind: str
    runs: list = field(default_factory=list)       # (x, y, text, font kind, size, color)
    color: str = "#000000"


STYLE = {"h1": ("serif-bold", 30, "#e8c15a", 18), "h2": ("serif-bold", 23, "#e8c15a", 14),
         "h3": ("serif-bold", 19, "#e8c15a", 10), "p": ("serif", 15, "#dddddd", 10),
         "li": ("serif", 15, "#dddddd", 4)}


UA_CSS = """
h1 { font-size: 30px; font-weight: bold; color: #e8c15a; margin-bottom: 18px }
h2 { font-size: 23px; font-weight: bold; color: #e8c15a; margin-bottom: 14px }
h3 { font-size: 19px; font-weight: bold; color: #e8c15a; margin-bottom: 10px }
p, li { font-size: 15px; color: #dddddd; margin-bottom: 10px }
li { margin-bottom: 4px }
code { color: #8fc7ff }
b { color: #ffffff; font-weight: bold }
"""


def _px(v, default):
    try:
        return int(float(str(v).replace("px", "")))
    except (TypeError, ValueError):
        return default


def style_of(styles, el):
    """(font kind, size, color, margin) from computed styles, or the built-in table."""
    if styles is None or id(el) not in styles:
        return STYLE.get(el.tag, STYLE["p"])
    st = styles[id(el)]
    kind = "serif-bold" if st.get("font-weight") == "bold" else "serif"
    return (kind, _px(st.get("font-size"), 15), st.get("color", "#dddddd"), _px(st.get("margin-bottom"), 10))


def layout(doc, page_width: int = 900, margin: int = 36, max_height: int = 1400, styles=None):
    """Block layout down the page; inside each block, inline layout of words (with bold, italic and code runs) by
    greedy line breaking.  With computed styles from the cascade, sizes, colours and margins come from CSS.  Returns
    boxes and the content height."""
    boxes = []
    y = margin
    for node in doc.children:
        if node.tag.startswith("#"):
            continue
        items = [(node, False)] if node.tag != "ul" else [(c, True) for c in node.children if c.tag == "li"]
        for el, bullet in items:
            kind, size, color, gap = style_of(styles, el)
            x0 = margin + (22 if bullet else 0)
            runs = []
            words = []

            ended_space = [True]

            def collect(n, bold=False, ital=False, code=False):
                if n.tag == "#text":
                    for k, w in enumerate(n.text.split()):
                        glue = k == 0 and not n.text[:1].isspace() and not ended_space[0]
                        words.append((w, bold, ital, code, glue))
                    ended_space[0] = n.text[-1:].isspace()
                    return
                for c in n.children:
                    collect(c, bold or n.tag == "b", ital or n.tag == "i", code or n.tag == "code")
            collect(el)
            line_h = int(size * 1.45)
            x, ly = x0, y
            sp = 0.0
            for w, bold, ital, code, glue in words:
                fk = "mono" if code else ("serif-bold" if bold else ("serif-italic" if ital else kind))
                fk = fallback(fk, w)
                sz = size - 1 if code else size
                f = font(fk, sz)
                ww = f.getlength(w)
                if glue:                 # no space in the source between this run and the last: no space here
                    x -= sp
                sp = f.getlength(" ")
                if x > x0 and x + ww > page_width - margin:
                    x, ly = x0, ly + line_h
                runs.append((x, ly, w, fk, sz, "#8fc7ff" if code else ("#ffffff" if bold else color)))
                x += ww + sp
            h = ly - y + line_h
            if bullet:
                runs.append((margin + 6, y, "•", "serif", size, color))
            boxes.append(Box(margin, y, page_width - 2 * margin, h, el.tag, runs))
            y += h + gap
            if y > max_height:
                return boxes, y
    return boxes, y


def render_markdown(md: str, path: str, page_width: int = 900, limit: int | None = 60, max_height: int = 1400):
    """The toy browser end to end: Markdown to HTML, HTML to a DOM, the cascade, layout and paint."""
    from explainer.cs.web import css, html
    doc, errors, fixes = html.parse(html.markdown_to_html(md, limit=limit))
    styles = css.cascade(doc, css.parse_css(UA_CSS))
    boxes, h = layout(doc, page_width, styles=styles, max_height=max_height)
    paint(boxes, page_width, min(h + 30, max_height + 40), path)
    return {"nodes": sum(1 for _ in doc.walk()), "boxes": len(boxes), "height": h, "errors": errors, "fixes": fixes,
            "words": sum(len(b.runs) for b in boxes)}


def paint(boxes, page_width: int, height: int, path: str, bg="#121722", outline=False):
    im = Image.new("RGB", (page_width, int(height)), bg)
    d = ImageDraw.Draw(im)
    for b in boxes:
        if outline:
            d.rectangle([b.x, b.y, b.x + b.w, b.y + b.h], outline="#3a4560")
        for x, y, t, fk, sz, col in b.runs:
            d.text((x, y), t, font=font(fk, sz), fill=col)
    im.save(path)
    return path
