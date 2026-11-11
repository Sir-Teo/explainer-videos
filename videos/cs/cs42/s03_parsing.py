from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs42.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, module_box, mono, tag_box

# the tokenizer's states as our instrument names them (explainer/cs/web/html.py), placed for the diagram
STATES = {
    "data": (-5.6, 0.1),
    "tag open": (-2.8, 0.1),
    "end tag open": (-2.8, -1.5),
    "tag name": (0.0, 0.1),
    "before attribute name": (2.8, 0.1),
    "attribute name": (5.6, 0.1),
    "before attribute value": (4.2, -1.5),
}
NAMES = {"before attribute name": r"before attribute\\name", "before attribute value": r"before attribute\\value"}
SW, SH = 1.95, 0.78


def spans(src, trace):
    """Which characters of ``src`` each step of the trace consumes (an unquoted attribute value is read whole, and
    a character can be reconsumed in a new state, as the instrument does)."""
    i, out = 0, []
    for state, c in trace:
        if c == "":
            out.append([len(src)])
            continue
        if state == "before attribute value" and c not in "\"'":
            j = i
            while j < len(src) and src[j] not in " \t\n>":
                j += 1
            out.append(list(range(i, j)))
            i = j
        elif state == "attribute name" and c in " \t\n/>":
            out.append([i])
        else:
            out.append([i])
            i += 1
    return out


def tree_of(tokens):
    """The open-element stack run over the tokens (as the tree builder does for this snippet): the nodes as
    (label, parent index, kind), and the stack events."""
    nodes, stack, events = [("document", None, "doc")], [0], []
    for kind, t in tokens:
        if kind == "start":
            a = "".join(f" {k}={v}" for k, v in t["attrs"].items())
            nodes.append((f"<{t['name']}{a}>", stack[-1], "el"))
            stack.append(len(nodes) - 1)
            events.append(("push", len(nodes) - 1))
        elif kind == "text":
            nodes.append((repr(t), stack[-1], "text"))
            events.append(("text", len(nodes) - 1))
        else:
            name = t["name"]
            pops = []
            while nodes[stack[-1]][0].split()[0].strip("<>") != name:
                pops.append(stack.pop())
            pops.append(stack.pop())
            events.append(("pop", pops))
    return nodes, events


def outline_tree(lines, x0, y0, step=0.4, hi=()):
    """Draw an outline (two spaces per level) as boxes with elbow connectors; ``hi``: line indices to emphasise."""
    g, boxes, depth = VGroup(), [], []
    for k, ln in enumerate(lines):
        d = (len(ln) - len(ln.lstrip(" "))) // 2
        s = ln.strip()
        is_text = s.startswith("'")
        col = HEAD if k in hi else (GREY_A if is_text else DATA)
        b = tag_box(s, color=col, size=16, h=0.32)
        b.move_to([x0 + d * 0.5, y0 - k * step, 0], aligned_edge=LEFT)
        boxes.append(b)
        depth.append(d)
        g.add(b)
        for p in range(k - 1, -1, -1):           # the parent: the nearest line above, one level out
            if depth[p] == d - 1:
                px = boxes[p].get_left()[0] + 0.16
                el = VMobject(stroke_color=GREY_C, stroke_width=1.5).set_points_as_corners(
                    [[px, boxes[p].get_bottom()[1], 0], [px, b.get_y(), 0], [b.get_left()[0], b.get_y(), 0]])
                g.add(el)
                break
    return g


class Parsing(VoiceoverScene):
    def construct(self):
        self.card()
        self.tokenizer()
        self.builder()
        self.implicit()
        self.misnested()
        self.grammar()

    def card(self):
        card = chapter_card(2, r"Parsing HTML", r"How do you parse a language in which nothing is an error?",
                            lit=(1951, 2014), extra=((2014, r"HTML5: \ the parsing algorithm becomes a standard"),),
                            part=PART)
        with self.voiceover("Chapter two. Parsing HTML."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def tokenizer(self):
        tk = load("tokenize")
        src, trace, tokens = tk["src"], tk["trace"], tk["tokens"]
        head = label(r"The tokenizer is a state machine", font_size=36).to_edge(UP, buff=0.3)
        # the tape
        cw = 0.4
        tape = VGroup()
        for ch in src:
            sq = Square(cw * 0.95, stroke_color=GREY_C, stroke_width=1.2)
            t = mono("·" if ch == " " else ch, size=18, color=GREY_D if ch == " " else WHITE)
            tape.add(VGroup(sq, t.move_to(sq)))
        eof = Rectangle(width=0.8, height=cw * 0.95, stroke_color=GREY_C, stroke_width=1.2)
        tape.add(VGroup(eof, label(r"end", font_size=16, color=GREY_B).move_to(eof)))
        tape.arrange(RIGHT, buff=0.02).move_to([0, 2.62, 0])
        cursor = SurroundingRectangle(tape[0], buff=0.03, color=HEAD, stroke_width=3)
        # the states and their transitions
        nodes = {}
        for name, (x, y) in STATES.items():
            box = RoundedRectangle(width=SW, height=SH, corner_radius=0.15, stroke_color=GREY_B, stroke_width=2,
                                   fill_color=HEAD, fill_opacity=0.0).move_to([x, y, 0])
            t = wrapped_label(NAMES.get(name, name), SW - 0.2, font_size=17, color=WHITE).move_to(box)
            nodes[name] = VGroup(box, t)

        def rim(a, b):
            ca, cb = np.array([*STATES[a], 0.0]), np.array([*STATES[b], 0.0])
            d = cb - ca
            t = min(SW / 2 / abs(d[0]) if d[0] else 9, SH / 2 / abs(d[1]) if d[1] else 9)
            return ca + d * (t + 0.03), cb - d * (t + 0.03)

        edges = VGroup()
        for a, b, txt in (("data", "tag open", "<"), ("tag open", "tag name", "a-z"), ("tag open", "end tag open", "/"),
                          ("end tag open", "tag name", "a-z"), ("tag name", "before attribute name", "space"),
                          ("before attribute name", "attribute name", "a-z"),
                          ("attribute name", "before attribute value", "="),
                          ("before attribute value", "before attribute name", "value")):
            p, q = rim(a, b)
            ar = Arrow(p, q, buff=0, stroke_width=2, color=GREY_B, tip_length=0.16,
                       max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=8)
            lab = mono(txt, size=16, color=KERN)
            d = (q - p) / np.linalg.norm(q - p)
            off = (0.22 if abs(d[1]) < 0.1 else 0.34) * (1 if d[0] >= 0 else -1)
            lab.move_to((p + q) / 2 + np.array([-d[1], d[0], 0]) * off)
            edges.add(VGroup(ar, lab))
        for a, ang in (("tag name", 0.9), ("before attribute name", 1.2)):
            p = nodes[a][0].get_top() + LEFT * 0.3
            q = nodes["data"][0].get_top() + RIGHT * (0.45 if a == "tag name" else -0.35)
            ar = CurvedArrow(p, q, angle=ang, color=YES, stroke_width=2, tip_length=0.18)
            lab = mono(">  emit the tag", size=16, color=YES).next_to(ar.point_from_proportion(0.5), UP, buff=0.05)
            if a == "tag name":
                lab = mono(">", size=16, color=YES).next_to(ar.point_from_proportion(0.5), DOWN, buff=0.06)
            edges.add(VGroup(ar, lab))
        stay = label(r"other characters keep the state", font_size=16, color=GREY_B).next_to(
            nodes["data"], DOWN, buff=0.15)
        # the tokens, as they are emitted
        def tok(kind, t):
            if kind == "text":
                return tag_box(f"text {t!r}", color=GREY_A, size=16, h=0.4)
            a = "".join(f" {k}={v}" for k, v in t["attrs"].items())
            return tag_box(f"{kind} {t['name']}{a}", color=DATA if kind == "start" else LAM, size=16, h=0.4)
        toks = VGroup(*[tok(k, t) for k, t in tokens]).arrange(RIGHT, buff=0.25).move_to([0.6, -2.55, 0])
        toks_t = label(r"tokens:", font_size=18, color=GREY_B).next_to(toks, LEFT, buff=0.25)
        foot = wrapped_label(r"a finite automaton \ (Part 12) \ with an output; \ the standard's tokenizer has "
                             r"about 80 states, \ and every character has a transition in every one", 12.4,
                             font_size=19, color=HEAD).to_edge(DOWN, buff=0.25)
        span = spans(src, trace)
        with self.voiceover(
            "An HTML parser has two stages. The first, the tokenizer, is a finite automaton like those of Part 12, "
            "reading one character at a time. <bookmark mark='a'/> Here it reads a paragraph with a class, a word, "
            "and a bold word that is never closed. In the data state, characters are text. A less-than sign moves it "
            "to tag open, a letter to tag name, a space to the attributes, an equals sign to a value, and each "
            "greater-than sign back to data, emitting a token. <bookmark mark='b'/> Out come five tokens. <bookmark "
            "mark='c'/> Nothing here can fail: an unexpected character has a transition too, written down by the "
            "standard, whose tokenizer has about eighty states."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tape), *[FadeIn(n) for n in nodes.values()], FadeIn(toks_t))
            self.play(Create(edges), FadeIn(stay), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(cursor), nodes["data"][0].animate.set_fill(HEAD, opacity=0.45), run_time=0.4)
            cur, ti, done = "data", 0, set()
            for (state, c), sp in zip(trace, span):
                anims = []
                if state != cur:
                    anims += [nodes[cur][0].animate.set_fill(HEAD, opacity=0.0),
                              nodes[state][0].animate.set_fill(HEAD, opacity=0.45)]
                    cur = state
                target = VGroup(*[tape[k] for k in sp])
                anims.append(cursor.animate.surround(target, buff=0.03))
                anims += [tape[k][1].animate.set_opacity(0.35) for k in sp if k < len(src) and k not in done]
                done |= set(sp)
                self.play(*anims, run_time=0.32)
                emit = ti < len(tokens) and (
                    (tokens[ti][0] in ("start", "end") and c == ">" and state in ("tag name",
                                                                                  "before attribute name"))
                    or (tokens[ti][0] == "text" and state == "data" and c in ("<", "")))
                if emit:
                    self.play(FadeIn(toks[ti], shift=DOWN * 0.2), run_time=0.35)
                    ti += 1
            vo.wait_until("b")
            self.play(LaggedStart(*[Circumscribe(t, color=WHITE, buff=0.05) for t in toks], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def builder(self):
        tk = load("tokenize")
        tokens = tk["tokens"]
        nodes, events = tree_of(tokens)
        head = label(r"The tree builder keeps a stack", font_size=36).to_edge(UP, buff=0.3)

        def tok(kind, t):
            if kind == "text":
                return tag_box(f"text {t!r}", color=GREY_A, size=16, h=0.42)
            a = "".join(f" {k}={v}" for k, v in t["attrs"].items())
            return tag_box(f"{kind} {t['name']}{a}", color=DATA if kind == "start" else LAM, size=16, h=0.42)
        toks = VGroup(*[tok(k, t) for k, t in tokens]).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        toks.move_to([-5.0, 0.5, 0]).to_edge(LEFT, buff=0.4)
        toks_t = label(r"tokens", font_size=19, color=GREY_B).next_to(toks, UP, buff=0.25)
        # the stack: a floor, and boxes that sit on it
        floor_y = -1.5
        floor = Line([-2.6, floor_y, 0], [-0.4, floor_y, 0], color=GREY_B, stroke_width=3)
        stack_t = label(r"open elements", font_size=19, color=GREY_B).move_to([-1.5, 2.2, 0])
        stack_n = label(r"the memory Part 12 adds\\to an automaton for nesting", font_size=16,
                        color=GREY_B).next_to(floor, DOWN, buff=0.2)
        # the DOM: leaves in slots, parents over their children
        kids = {i: [j for j, (_, p, _) in enumerate(nodes) if p == i] for i in range(len(nodes))}
        dep = {0: 0}
        for j, (_, p, _) in enumerate(nodes):
            if p is not None:
                dep[j] = dep[p] + 1
        xs, slot = {}, [0]

        def place(i):
            if not kids[i]:
                xs[i] = slot[0]
                slot[0] += 1
            else:
                for c in kids[i]:
                    place(c)
                xs[i] = sum(xs[c] for c in kids[i]) / len(kids[i])
        place(0)
        dom = {}
        for j, (txt, p, kind) in enumerate(nodes):
            col = GREY_B if kind == "doc" else (GREY_A if kind == "text" else DATA)
            dom[j] = tag_box(txt if kind != "doc" else "Document", color=col, size=16, h=0.42).move_to(
                [2.4 + xs[j] * 2.6, 1.9 - dep[j] * 1.05, 0])
        dlines = {j: Line(dom[p][0].get_bottom(), dom[j][0].get_top(), color=GREY_C, stroke_width=1.5)
                  for j, (_, p, _) in enumerate(nodes) if p is not None}
        dom_t = label(r"the DOM", font_size=19, color=GREY_B).next_to(dom[0], LEFT, buff=0.4)
        fix = mono("</p> also closes <b>", size=16, color=NO).move_to([-1.5, -2.35, 0])
        cap = wrapped_label(r"the \textbf{DOM}: \ a tree of node objects \ (the document, \ elements, \ text) \ that "
                            r"scripts read and change, \ and that style, \ layout and paint work from", 12.4,
                            font_size=19, color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The second stage, the tree builder, keeps a stack of open elements, the memory that Part 12 added to "
            "automata to handle nesting. <bookmark mark='a'/> A start tag creates an element, attaches it to the "
            "element on top of the stack, and pushes it; text is attached to the top. <bookmark mark='b'/> Then the "
            "paragraph's end tag arrives while bold is still open. A grammar would reject the input here. The tree "
            "builder pops bold too, closing it for the author, and then the paragraph. <bookmark mark='c'/> What "
            "remains is the DOM, the document object model: a tree of node objects that scripts read and change, and "
            "that everything else in this part works from."
        ) as vo:
            self.play(FadeIn(head), FadeIn(toks), FadeIn(toks_t), Create(floor), FadeIn(stack_t), FadeIn(stack_n),
                      FadeIn(dom[0]), FadeIn(dom_t))
            vo.wait_until("a")
            on, k = [], 0
            for ev in events:
                hl = SurroundingRectangle(toks[k], buff=0.06, color=HEAD, stroke_width=2.5)
                self.play(Create(hl), run_time=0.3)
                if ev[0] == "push":
                    j = ev[1]
                    box = tag_box(nodes[j][0], color=DATA, size=16, w=2.0, h=0.45)
                    box.move_to([-1.5, floor_y + 0.3 + len(on) * 0.52, 0])
                    on.append(box)
                    self.play(FadeIn(box, shift=DOWN * 0.4), FadeIn(dom[j]), Create(dlines[j]), run_time=0.7)
                elif ev[0] == "text":
                    j = ev[1]
                    self.play(Circumscribe(on[-1], color=WHITE, buff=0.05), FadeIn(dom[j]), Create(dlines[j]),
                              run_time=0.7)
                else:
                    vo.wait_until("b")
                    for n_ in ev[1]:
                        box = on.pop()
                        first = n_ != ev[1][-1]
                        if first:
                            self.play(FadeIn(fix), box[0].animate.set_stroke(NO), run_time=0.5)
                        self.play(FadeOut(box, shift=UP * 0.4), Circumscribe(dom[n_], color=NO if first else LAM,
                                                                             buff=0.05), run_time=0.7)
                self.play(FadeOut(hl), run_time=0.2)
                k += 1
            vo.wait_until("c")
            self.play(FadeIn(cap), *[Circumscribe(d, color=WHITE, buff=0.05) for d in dom.values()])
        self.wait(0.4)
        self.clear_scene()

    def _cases(self, idx, hi):
        """Rows of (source, tree, repairs) for the recover cases ``idx``."""
        cases = load("recover")["cases"]
        rows = VGroup()
        for i in idx:
            c = cases[i]
            s = mono(c["src"], size=18, color=WHITE)
            tree = outline_tree(c["outline"], 0, 0, hi=hi.get(i, ()))
            msgs = [mono(f, size=16, color=YES) for f in c["fixes"]]
            for e in c["errors"]:
                cut = e.find("-", len(e) // 2)
                msgs += [mono("parse error:", size=16, color=NO), mono(e[:cut + 1], size=16, color=NO),
                         mono(e[cut + 1:], size=16, color=NO)]
            fx = VGroup(*msgs).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            rows.add(VGroup(s, tree, fx))
        y = 2.75
        for r in rows:
            h = max(r[1].height, r[2].height)
            r[1].move_to([-1.2, y - h / 2, 0], aligned_edge=LEFT).align_to([0, y, 0], UP)
            r[0].move_to([-6.6, r[1].get_y(), 0], aligned_edge=LEFT)
            r[2].move_to([3.0, r[1].get_y(), 0], aligned_edge=LEFT)
            ar = Arrow(r[0].get_right() + RIGHT * 0.1, [r[1].get_left()[0] - 0.1, r[1].get_y(), 0], buff=0,
                       stroke_width=2, color=GREY_C, max_tip_length_to_length_ratio=0.25)
            if ar.get_length() < 0.3:
                ar = VGroup()
            r.add(ar)
            y -= h + 0.45
        return rows

    def implicit(self):
        head = label(r"Closing what the author left open", font_size=36).to_edge(UP, buff=0.3)
        rows = self._cases((0, 2, 5), {})
        tb = note(r"a real browser also inserts a \texttt{tbody} here; \ our parser does not", font_size=17).next_to(
            rows[2][2], DOWN, buff=0.15).align_to(rows[2][2], LEFT)
        if tb.get_right()[0] > 6.9:
            tb.shift(LEFT * (tb.get_right()[0] - 6.9))
        with self.voiceover(
            "Most of the tree builder's rules close elements the author left open. <bookmark mark='a'/> A paragraph "
            "cannot contain a paragraph, so a p start tag closes the open p, and the two become siblings. <bookmark "
            "mark='b'/> A list item closes the previous item, and the end of the list closes the last one. <bookmark "
            "mark='c'/> An end tag closes everything above its match on the stack: the end of the table ends the cell"
            " and the row too. A real browser also inserts a table body element here, which our simplified parser "
            "leaves out. The standard writes all of these rules down."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(r[0]) for r in rows])
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(Indicate(r[0], color=HEAD, scale_factor=1.05), GrowArrow(r[3]) if len(r[3].points) else
                          Wait(0.1))
                self.play(FadeIn(r[1], shift=RIGHT * 0.2), FadeIn(r[2]))
            self.play(FadeIn(tb))
        self.wait(0.4)
        self.clear_scene()

    def misnested(self):
        head = label(r"Misnesting and strays", font_size=36).to_edge(UP, buff=0.3)
        rows = self._cases((1, 3, 4), {1: (3,)})
        adopt = wrapped_label(r"the standard's \textbf{adoption agency algorithm} handles overlapping formatting "
                              r"elements in general; \ ours is the simple case: \ close the \texttt{i}, \ then "
                              r"reopen a new one", 12.4, font_size=19, color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Misnested tags are harder. <bookmark mark='a'/> Here bold opens, then italic, but bold closes first. Our"
            " tree builder closes the italic along with the bold, then opens a new italic element, so the last words "
            "stay italic, as the author meant: a simplified case of the standard's adoption agency algorithm. "
            "<bookmark mark='b'/> An end tag with nothing to match, like this stray span, is ignored. <bookmark "
            "mark='c'/> And a less-than sign that does not begin a tag is a parse error with a defined outcome: it is"
            " text. Every input gives a tree, and every browser that follows the standard gives the same one."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(r[0]) for r in rows])
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(Indicate(r[0], color=HEAD, scale_factor=1.05), GrowArrow(r[3]) if len(r[3].points) else
                          Wait(0.1))
                self.play(FadeIn(r[1], shift=RIGHT * 0.2), FadeIn(r[2]))
                if mk == "a":
                    self.play(FadeIn(adopt))
        self.wait(0.4)
        self.clear_scene()

    def grammar(self):
        head = label(r"Why not a grammar?", font_size=36).to_edge(UP, buff=0.3)

        def box(t, col, w=2.5, h=0.75):
            return module_box(t, col, w=w, h=h, font=18)
        top_t = label(r"a language with a grammar \ (Parts 12 and 13)", font_size=20, color=GREY_A).move_to(
            [-2.6, 2.45, 0])
        src = box(r"source text", DATA).move_to([-5.4, 1.55, 0])
        par = box(r"parser \ (LR table)", LAM).move_to([-1.9, 1.55, 0])
        ok = box(r"a tree", YES, w=2.0).move_to([1.5, 2.0, 0])
        err = box(r"syntax error: \ stop", NO, w=2.6).move_to([1.8, 1.05, 0])
        a1 = Arrow(src.get_right(), par.get_left(), buff=0.1, stroke_width=2, color=GREY_B)
        a2 = Arrow(par.get_right(), ok.get_left(), buff=0.1, stroke_width=2, color=YES)
        a3 = Arrow(par.get_right(), err.get_left(), buff=0.1, stroke_width=2, color=NO)
        bot_t = label(r"HTML", font_size=20, color=GREY_A).move_to([-5.4, 0.25, 0])
        byt = box(r"any characters", DATA, w=2.1).move_to([-5.6, -0.55, 0])
        tok = box(r"tokenizer: \ about 80 states", HEAD, w=2.8).move_to([-2.45, -0.55, 0])
        tb = box(r"tree builder: \ stack, \ insertion mode", KERN, w=3.1).move_to([1.4, -0.55, 0])
        dom = box(r"a DOM, \ always", YES, w=1.9).move_to([5.0, -0.55, 0])
        b1 = Arrow(byt.get_right(), tok.get_left(), buff=0.08, stroke_width=2, color=GREY_B)
        b2 = Arrow(tok.get_right(), tb.get_left(), buff=0.08, stroke_width=2, color=GREY_B)
        b3 = Arrow(tb.get_right(), dom.get_left(), buff=0.08, stroke_width=2, color=YES)
        b2t = label(r"tokens", font_size=16, color=GREY_B).next_to(b2, UP, buff=0.05)
        modes = label(r"modes such as \textit{in body}, \ \textit{in table}, \ \textit{in select}", font_size=17,
                      color=KERN).next_to(tb, DOWN, buff=0.15)
        back = CurvedArrow(tb.get_bottom() + LEFT * 1.0 + DOWN * 0.45, tok.get_bottom() + DOWN * 0.05, angle=-1.2,
                           color=NO, stroke_width=2.5, tip_length=0.18)
        back_t = mono("<script>document.write('<p>more')</script>", size=16, color=NO).next_to(
            back, DOWN, buff=0.1)
        back_n = label(r"a running script can add characters to the input: \ the parser must be re-entrant",
                       font_size=18, color=NO).next_to(back_t, DOWN, buff=0.1)
        cap = wrapped_label(r"the error handling is part of the specification, \ so every browser builds the same tree "
                            r"from the same broken page", 12.4, font_size=20, color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "So why not write a grammar for HTML, and use the parsers of Parts 12 and 13? <bookmark mark='a'/> A "
            "parser built from a grammar also answers yes or no: input outside the language is a syntax error, and a "
            "compiler stops. A browser cannot stop. Real pages are full of errors, and a reader blames the browser "
            "that shows nothing. <bookmark mark='b'/> So the standard defines HTML by its parsing algorithm: a "
            "tokenizer of about eighty states, and a tree builder whose every step depends on its stack and on an "
            "insertion mode, such as in body or in table. <bookmark mark='c'/> Nor is the input fixed. A script "
            "running in the middle of parsing can call document dot write and insert new characters right after "
            "itself, so the parser must pause, run the script, and carry on."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(top_t), FadeIn(src), FadeIn(par), GrowArrow(a1))
            self.play(GrowArrow(a2), FadeIn(ok), GrowArrow(a3), FadeIn(err))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in (bot_t, byt, b1, tok, b2, b2t, tb, modes, b3, dom)],
                                  lag_ratio=0.25), run_time=3)
            vo.wait_until("c")
            self.play(Create(back), FadeIn(back_t), FadeIn(back_n))
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM, YES, KERN)
