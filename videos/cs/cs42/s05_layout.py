from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs42.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, load, mono, tag_box

SERIF = "DejaVu Serif"
DESC = set("gjpqy")            # letters that hang below the baseline
COMMA = set(",;")


def _dashed(w, h, color, sw=1.2, dash=0.08):
    """A dashed rectangle outline."""
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=sw)
    return DashedVMobject(r, num_dashes=max(8, int(2 * (w + h) / (2 * dash))))


class _Setter:
    """Words drawn as boxes at their measured widths (DejaVu Serif 16 px, scaled to scene units), the text inside
    each box sized so that its own width matches the measurement, every word on a common baseline."""

    def __init__(self, ref_word: str, ref_px: float, s: float):
        self.s = s
        self.fs = 16 * s * ref_px / Text(ref_word, font=SERIF, font_size=16).width
        hx = Text("x", font=SERIF, font_size=self.fs).height
        self.d_g = Text("xg", font=SERIF, font_size=self.fs).height - hx
        self.d_c = Text("x,", font=SERIF, font_size=self.fs).height - hx
        self.h = Text("Hg", font=SERIF, font_size=self.fs).height + 0.06

    def word(self, w: str, px: float, x: float, y: float, color, text_color=WHITE):
        """A word box of px pixels with its left edge at x and its baseline band centred on y."""
        box = Rectangle(width=px * self.s, height=self.h, stroke_color=color, stroke_width=0.8, fill_color=color,
                        fill_opacity=0.14).move_to([x + px * self.s / 2, y, 0])
        t = Text(w, font=SERIF, font_size=self.fs, color=text_color)
        drop = self.d_g if set(w) & DESC else (self.d_c if set(w) & COMMA else 0.0)
        base = y - self.h / 2 + 0.03 + self.d_g
        t.move_to([box.get_center()[0], 0, 0]).align_to([0, base - drop, 0], DOWN)
        return VGroup(box, t)

    def paragraph(self, words, widths, space, lines, lw, pitch, color, x0=0.0, y0=0.0):
        """Set lines (lists of word indices) from (x0, y0) down; each row is VGroup(words..., slack bar)."""
        rows = VGroup()
        slacks = []
        for k, ln in enumerate(lines):
            y = y0 - k * pitch
            x, row = x0, VGroup()
            for i in ln:
                row.add(self.word(words[i], widths[i], x, y, color))
                x += (widths[i] + space) * self.s
            used = sum(widths[i] for i in ln) + space * (len(ln) - 1)
            slack = lw - used
            slacks.append(slack)
            end = x0 + used * self.s
            bar = Rectangle(width=max(slack * self.s, 0.01), height=self.h * 0.5, stroke_width=0,
                            fill_color=NO if k < len(lines) - 1 else GREY_D, fill_opacity=0.35)
            bar.move_to([end + slack * self.s / 2, y, 0])
            row.add(bar)
            rows.add(row)
        margin = DashedLine([x0 + lw * self.s, y0 + pitch * 0.6, 0],
                            [x0 + lw * self.s, y0 - (len(lines) - 0.4) * pitch, 0], color=GREY_B, stroke_width=1.2,
                            dash_length=0.06)
        return rows, margin, slacks


class Layout(VoiceoverScene):
    def construct(self):
        self.card()
        self.flow()
        self.flexbox()
        self.grid()
        self.breaking()
        self.graph()
        self.relayout()

    def card(self):
        card = chapter_card(4, r"Layout", r"Where does every box go, and where does every line break?",
                            lit=(1981, 2017), extra=((1981, r"Knuth and Plass: \ total-fit line breaking"),
                                                     (1996, r"CSS1: \ the box model"),
                                                     (2017, r"CSS grid ships in browsers")), part=PART)
        with self.voiceover("Chapter four. Layout."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ the box model and normal flow
    def flow(self):
        head = label(r"Boxes, \ and normal flow", font_size=36).to_edge(UP, buff=0.3)
        c = [-3.7, 0.3, 0]
        margin = _dashed(5.4, 3.9, GREY_B, sw=1.5, dash=0.1).move_to(c)
        border = Rectangle(width=4.4, height=2.9, stroke_color=KERN, stroke_width=6).move_to(c)
        padding = Rectangle(width=4.3, height=2.8, stroke_width=0, fill_color=LAM, fill_opacity=0.22).move_to(c)
        content = Rectangle(width=2.8, height=1.4, stroke_width=0, fill_color=DATA, fill_opacity=0.45).move_to(c)
        names = VGroup(
            label(r"content", font_size=20, color=WHITE).move_to(content),
            label(r"padding", font_size=18, color=LAM).next_to(content, UP, buff=0.12),
            label(r"border", font_size=18, color=KERN).next_to(border, UP, buff=0.06).align_to(border, RIGHT),
            label(r"margin", font_size=18, color=GREY_B).next_to(margin.get_corner(UL), DR, buff=0.08),
        )
        model = VGroup(margin, padding, border, content, names)

        # normal flow: three blocks stack; inside the middle one, inline boxes fill line boxes and wrap
        fx, fw = 0.9, 5.6
        top = 2.2
        blk = [Rectangle(width=fw, height=h, stroke_color=GREY_B, stroke_width=1.5) for h in (0.6, 1.6, 0.6)]
        y = top
        for b in blk:
            b.move_to([fx + fw / 2, y - b.height / 2, 0])
            y -= b.height + 0.25
        bnames = VGroup(*[label(t, font_size=16, color=GREY_B).next_to(b, LEFT, buff=0.1) for t, b in
                          zip((r"block", r"block", r"block"), blk)])
        words = "inline boxes flow along a line and wrap onto the next line box when the line is full".split()
        pad, lh, inl = 0.15, 0.42, VGroup()
        x, row = fx + pad, 0
        for w in words:
            t = Text(w, font=SERIF, font_size=18, color=WHITE)
            wd = t.width + 0.12
            if x + wd > fx + fw - pad:
                x, row = fx + pad, row + 1
            yy = blk[1].get_top()[1] - pad - lh / 2 - row * lh
            r = Rectangle(width=wd, height=0.32, stroke_color=DATA, stroke_width=1, fill_color=DATA,
                          fill_opacity=0.14).move_to([x + wd / 2, yy, 0])
            inl.add(VGroup(r, t.move_to(r)))
            x += wd + 0.08
        lineboxes = VGroup(*[_dashed(fw - 2 * pad + 0.06, lh - 0.04, HEAD, sw=1, dash=0.06).move_to(
            [fx + fw / 2, blk[1].get_top()[1] - pad - lh / 2 - k * lh, 0]) for k in range(row + 1)])
        notes = VGroup(
            wrapped_label(r"every element is a box: \ content, \ padding, \ border, \ margin", 5.6, font_size=19,
                          color=WHITE),
            wrapped_label(r"\textbf{blocks} stack down the page, \ each as wide as its container; \ "
                          r"\textbf{inlines} flow along line boxes and wrap", 6.4, font_size=19, color=HEAD),
        )
        notes[0].next_to(margin, DOWN, buff=0.3)
        notes[1].next_to(blk[2], DOWN, buff=0.35).align_to(blk[2], LEFT)
        illus = note(r"illustrative boxes", font_size=16).to_corner(DR, buff=0.2)
        with self.voiceover(
            "Layout gives every element a box: where it goes, and how big it is. <bookmark mark='a'/> A box "
            "is its content, then padding, a border, and a margin that keeps neighbours away. <bookmark "
            "mark='b'/> In normal flow, blocks stack down the page, each as wide as its container: widths "
            "flow down the tree, heights come back up. <bookmark mark='c'/> Inside a block, inline boxes flow"
            " along a line and wrap into the next line box."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(margin), Create(border), FadeIn(padding), FadeIn(content), FadeIn(names),
                      FadeIn(notes[0]), FadeIn(illus))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, UP) for b in blk], lag_ratio=0.4), FadeIn(bnames))
            vo.wait_until("c")
            self.play(FadeIn(lineboxes), FadeIn(notes[1]))
            self.play(LaggedStart(*[FadeIn(w, shift=RIGHT * 0.2) for w in inl], lag_ratio=0.25), run_time=3)
        _ = model
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ flexbox: distributing free space
    def flexbox(self):
        f = load("flex")
        items = f["items"]
        cases = f["cases"]
        order = ["480", "720", "880", "360", "300"]
        head = label(r"Flexbox: \ sharing out the free space", font_size=36).to_edge(UP, buff=0.3)
        s, x0, yc, hh = 0.0125, -5.5, 0.85, 0.75
        cols = [DATA, LAM, KERN]
        basis = [b for b, _, _ in items]

        def row(case):
            sizes = cases[case]["sizes"]
            g, x = VGroup(), x0
            for k, (sz, (b, gr, sh)) in enumerate(zip(sizes, items)):
                r = Rectangle(width=sz * s, height=hh, stroke_color=cols[k], stroke_width=2, fill_color=cols[k],
                              fill_opacity=0.3).move_to([x + sz * s / 2, yc, 0])
                n = mono(f"{sz:.0f}", size=18, color=WHITE).move_to(r)
                d = sz - b
                delta = mono(f"{d:+.0f}" if abs(d) > 1e-9 else "0", size=16,
                             color=YES if d > 1e-9 else (NO if d < -1e-9 else GREY_B)).next_to(r, DOWN, buff=0.12)
                g.add(VGroup(r, n, delta))
                x += sz * s
            return g

        def box(case):
            w = int(case) * s
            return Rectangle(width=w, height=hh + 0.16, stroke_color=WHITE, stroke_width=2).move_to(
                [x0 + w / 2, yc, 0])

        def caption(case):
            fr = cases[case]["free"]
            col = YES if fr > 0 else (NO if fr < 0 else GREY_A)
            sign = "+" if fr > 0 else ""
            return VGroup(label(rf"container {case} px", font_size=20, color=WHITE),
                          label(rf"free space ${sign}{fr}$ px", font_size=20, color=col)).arrange(
                RIGHT, buff=0.5).move_to([0, yc + 1.2, 0]).align_to([x0, 0, 0], LEFT)

        legend = VGroup(*[label(rf"basis {b}, \ grow {gr}, \ shrink {sh}", font_size=17, color=cols[k])
                          for k, (b, gr, sh) in enumerate(items)]).arrange(RIGHT, buff=0.45).move_to([0, -0.45, 0])
        ghostnote = label(r"under each item: \ its change from the basis", font_size=16, color=GREY_B).next_to(
            legend, DOWN, buff=0.15)
        notes = VGroup(
            wrapped_label(rf"free space $=$ container $-$ sum of bases \ ($= {sum(basis)}$ px here)", 12.4,
                          font_size=20, color=WHITE),
            wrapped_label(r"free space $> 0$: \ each item grows by its share of the free space in proportion to its "
                          r"grow factor; \ the third, \ grow 0, \ stays at 160", 12.4, font_size=20, color=YES),
            wrapped_label(r"free space $< 0$: \ the overflow is taken in proportion to shrink $\times$ basis, \ so "
                          r"large items give up more", 12.4, font_size=20, color=NO),
            wrapped_label(r"the specification then clamps items to their minimum and maximum sizes and repeats "
                          r"the share-out among those left unfrozen", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(ghostnote, DOWN, buff=0.5)
        notes.set_x(0)
        cur, frame, cap = row("480"), box("480"), caption("480")
        with self.voiceover(
            "Flexbox shares out space. <bookmark mark='a'/> Three items with bases of one hundred and twenty,"
            " two hundred and one hundred and sixty pixels, and grow factors of one, two and zero, fill four "
            "hundred and eighty pixels. <bookmark mark='b'/> At seven hundred and twenty, two hundred and "
            "forty pixels are free: one share to the first, two to the second, none to the third. <bookmark "
            "mark='c'/> At eight hundred and eighty, four hundred are shared the same way. <bookmark "
            "mark='d'/> At three hundred and sixty, a hundred and twenty are missing, taken in proportion to "
            "shrink factor times basis, so the widest gives up most. <bookmark mark='e'/> At three hundred, "
            "each loses three eighths. <bookmark mark='f'/> Items that hit a size limit are frozen, and the "
            "rest share again."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            rects = VGroup(*[it[0] for it in cur])
            texts = VGroup(*[VGroup(it[1], it[2]) for it in cur])
            self.play(Create(frame), FadeIn(rects), FadeIn(texts), FadeIn(cap), FadeIn(legend), FadeIn(ghostnote),
                      FadeIn(notes[0]))
            for mk, case in zip("bcde", order[1:]):
                vo.wait_until(mk)
                new, nframe, ncap = row(case), box(case), caption(case)
                ntexts = VGroup(*[VGroup(it[1], it[2]) for it in new])
                extra = [FadeIn(notes[1])] if mk == "b" else ([FadeIn(notes[2])] if mk == "d" else [])
                self.play(Transform(rects, VGroup(*[it[0] for it in new])), Transform(frame, nframe),
                          FadeOut(texts), FadeOut(cap), *extra, run_time=1.5)
                self.play(FadeIn(ntexts), FadeIn(ncap), run_time=0.5)
                texts, cap = ntexts, ncap
            vo.wait_until("f")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ grid
    def grid(self):
        head = label(r"Grid: \ tracks in two dimensions", font_size=36).to_edge(UP, buff=0.3)
        W, H, s = 800, 400, 0.0078
        fixed, frs = 200, [1, 2]
        unit = (W - fixed) / sum(frs)
        colw = [fixed] + [k * unit for k in frs]
        rowh = [80, H - 80]
        x0, y0 = -6.3, 2.0
        xs = [x0]
        for w in colw:
            xs.append(xs[-1] + w * s)
        ys = [y0]
        for h in rowh:
            ys.append(ys[-1] - h * s)
        lines = VGroup(*[DashedLine([x, y0, 0], [x, ys[-1], 0], color=GREY_B, stroke_width=1.2, dash_length=0.08)
                         for x in xs],
                       *[DashedLine([x0, y, 0], [xs[-1], y, 0], color=GREY_B, stroke_width=1.2, dash_length=0.08)
                         for y in ys])
        tw = VGroup(*[label(t, font_size=17, color=HEAD).move_to([(xs[k] + xs[k + 1]) / 2, y0 + 0.25, 0])
                      for k, t in enumerate((r"200px $\to$ 200", r"1fr $\to$ 200", r"2fr $\to$ 400"))])

        def area(c0, c1, r0, r1, name, col):
            r = Rectangle(width=xs[c1] - xs[c0] - 0.08, height=ys[r0] - ys[r1] - 0.08, stroke_color=col,
                          stroke_width=2, fill_color=col, fill_opacity=0.25)
            r.move_to([(xs[c0] + xs[c1]) / 2, (ys[r0] + ys[r1]) / 2, 0])
            return VGroup(r, label(name, font_size=18, color=WHITE).move_to(r))
        areas = VGroup(area(0, 3, 0, 1, r"header: \ all three columns", DATA), area(0, 1, 1, 2, r"sidebar", LAM),
                       area(1, 3, 1, 2, r"main: \ columns 2--3", KERN))
        css = code_block(["grid-template-columns:", "    200px 1fr 2fr;", "grid-template-rows: 80px 1fr;"],
                         size=16).next_to(VGroup(lines, areas), DOWN, buff=0.35).align_to([x0, 0, 0], LEFT)
        notes = VGroup(
            wrapped_label(r"columns and rows are \textbf{tracks}; \ items are placed on the grid lines between them, "
                          r"\ spanning as many as they need", 5.4, font_size=19, color=WHITE),
            wrapped_label(rf"\texttt{{fr}} is a share of what is left: \ in 800 px, \ the fixed 200 leaves 600, \ "
                          rf"so one fr is {unit:.0f} px", 5.4, font_size=19, color=HEAD),
            wrapped_label(r"flexbox shares space along one line; \ grid sizes rows and columns together, \ so "
                          r"items line up in both directions", 5.4, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, 0.2, 0])
        illus = note(r"illustrative grid", font_size=16).to_corner(DR, buff=0.2)
        with self.voiceover(
            "Grid is the two-dimensional version. <bookmark mark='a'/> Columns and rows are tracks, and items"
            " span the grid lines between them. <bookmark mark='b'/> A track can be fixed, or a fraction of "
            "what is left: in eight hundred pixels, a fixed two hundred leaves six hundred, so one fraction "
            "is two hundred. <bookmark mark='c'/> Rows and columns are sized together, so items line up both "
            "ways."
        ) as vo:
            self.play(FadeIn(head), Create(lines), FadeIn(css), FadeIn(illus))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(a) for a in areas], lag_ratio=0.4), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(tw), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ greedy against Knuth-Plass
    def breaking(self):
        b = load("breaking")
        words, widths, space, lw = b["words"], b["widths"], b["space"], b["line_width"]
        gs, ks, corpus = b["greedy_stats"], b["kp_stats"], b["corpus"]
        head = label(r"Breaking a paragraph into lines", font_size=36).to_edge(UP, buff=0.3)
        ref = max(range(len(words)), key=lambda i: widths[i])
        st = _Setter(words[ref], widths[ref], 0.0150)
        pitch, y0 = 0.3, 2.35
        cols = VGroup()
        sets = []
        for x0, lines, col, title in ((-6.0, b["greedy"], NO, r"greedy: \ first fit"),
                                      (0.6, b["kp"], YES, r"Knuth--Plass: \ total fit")):
            rows, margin, slacks = st.paragraph(words, widths, space, lines, lw, pitch, col, x0=x0, y0=y0)
            t = label(title, font_size=21, color=col).move_to([x0 + lw * st.s / 2, y0 + 0.42, 0])
            worst = max(range(len(slacks) - 1), key=lambda k: slacks[k])
            sets.append((rows, margin, t, worst, slacks))
            cols.add(VGroup(t, margin, rows))
        diff = [k for k, (a, c) in enumerate(zip(b["greedy"], b["kp"])) if a != c]
        hl = VGroup(*[SurroundingRectangle(VGroup(*sets[j][0][k]), color=HEAD, buff=0.03, stroke_width=1.5)
                      for j in (0, 1) for k in diff])
        worst = VGroup(*[SurroundingRectangle(sets[j][0][sets[j][3]][-1], color=WHITE, buff=0.03, stroke_width=2)
                         for j in (0, 1)])
        stats = VGroup(*[label(rf"{x['lines']} lines; \ worst line {x['max_slack']:.1f} px short; \ badness "
                               rf"{x['badness']:.2f}", font_size=18, color=c).move_to(
            [x0 + lw * st.s / 2, y0 - 17 * pitch - 0.05, 0]) for x, c, x0 in ((gs, NO, -6.0), (ks, YES, 0.6))])
        corp = label(rf"over {corpus['paragraphs']} paragraphs of the novel: \ Knuth--Plass strictly better on "
                     rf"{corpus['kp_better']}, \ median badness ratio {corpus['median_ratio']:.2f}", font_size=18,
                     color=HEAD).to_edge(DOWN, buff=0.15)
        src = label(r"Darcy's letter, \ \textit{Pride and Prejudice}: \ 114 words, \ DejaVu Serif 16 px, \ "
                    r"360 px line", font_size=16, color=GREY_B).next_to(stats, DOWN, buff=0.12)
        src.set_x(0)
        assert len(words) == 114
        with self.voiceover(
            "How should a paragraph break into lines? <bookmark mark='a'/> The greedy rule, which browsers "
            "have traditionally used, puts each word on the current line if it fits. Here is Darcy's letter "
            "from Pride and Prejudice at three hundred and sixty pixels; red bars show each line's shortfall."
            " <bookmark mark='b'/> Knuth and Plass, in 1981, for TeX, chose all the breaks at once, "
            "minimising the sum of the lines' cubed shortfalls. <bookmark mark='c'/> Both use seventeen lines"
            " and differ on three. Greedy's worst line is seventy-seven point eight pixels short, against "
            "fifty-four point eight, and badness falls from two point four to one point eight six. <bookmark "
            "mark='d'/> Over three hundred paragraphs of the novel, total fit wins on two hundred and "
            "eighty-four."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            rows, margin, t = sets[0][:3]
            self.play(FadeIn(t), Create(margin))
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15), run_time=3)
            vo.wait_until("b")
            rows, margin, t = sets[1][:3]
            self.play(FadeIn(t), Create(margin))
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15), run_time=3)
            vo.wait_until("c")
            self.play(Create(hl), FadeIn(stats), FadeIn(src))
            self.play(Create(worst))
            vo.wait_until("d")
            self.play(FadeIn(corp))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the breakpoint graph
    def graph(self):
        k = load("kpgraph")
        words, edges, lw = k["words"], k["edges"], k["line_width"]
        space = load("breaking")["space"]                  # the same face and size, so the same space
        n = len(words)
        cost = {(i, j): c for i, j, c in edges}
        # each single-word edge (i, i+1) has cost 100 (slack / line)^3, so it gives back word i's width
        widths = [lw - lw * (cost[(i, i + 1)] / 100) ** (1 / 3) for i in range(n - 1)]
        tw = [Text(w, font=SERIF, font_size=16).width for w in words[-2:]]
        widths.append(tw[1] * widths[-1] / tw[0])           # the last word's edge is free; place it by its text
        head = label(r"Line breaking as a shortest path", font_size=36).to_edge(UP, buff=0.3)
        s = 12.9 / (sum(widths) + space * (n - 1))
        ref = max(range(n - 1), key=lambda i: widths[i])
        st = _Setter(words[ref], widths[ref], s)
        x0, yw = -6.45, 0.55
        xs, x, row = [], x0, VGroup()
        for i, w in enumerate(words):
            xs.append(x - space * s / 2 if i else x)
            row.add(st.word(w, widths[i], x, yw, GREY_B))
            x += (widths[i] + space) * s
        xs.append(x - space * s)
        up, dn = yw + st.h / 2 + 0.12, yw - st.h / 2 - 0.12
        nodes = VGroup(*[Dot([xx, up, 0], radius=0.045, color=GREY_A) for xx in xs])
        nodes_dn = VGroup(*[Dot([xx, dn, 0], radius=0.045, color=GREY_A) for xx in xs])

        def arc(i, j, y, col, wdt, above=True):
            return ArcBetweenPoints([xs[i], y, 0], [xs[j], y, 0], angle=-0.7 * PI if above else 0.7 * PI,
                                    color=col, stroke_width=wdt)
        allarcs = VGroup(*[arc(i, j, up, GREY_C, 1.0) for i, j, _ in edges]).set_stroke(opacity=0.5)
        kp_lines, g_lines = k["kp"], k["greedy"]
        kp_arcs = VGroup(*[arc(ln[0], ln[-1] + 1, up, YES, 4) for ln in kp_lines])
        g_arcs = VGroup(*[arc(ln[0], ln[-1] + 1, dn, NO, 4, above=False) for ln in g_lines])
        legend = label(rf"{len(edges)} edges: \ one for every line that fits in {lw:.0f} px", font_size=19,
                       color=GREY_A).next_to(head, DOWN, buff=0.2)

        # the two settings, with each line's cost
        st2 = _Setter(words[ref], widths[ref], 0.0158)
        pitch = 0.3

        def setting(lines, col, x0, title):
            rows, margin, _ = st2.paragraph(words, widths, space, lines, lw, pitch, col, x0=x0, y0=-1.45)
            costs = VGroup(*[mono(f"{cost[(ln[0], ln[-1] + 1)]:.2f}", size=16, color=col).move_to(
                [x0 + lw * st2.s + 0.45, -1.45 - q * pitch, 0]) for q, ln in enumerate(lines)])
            tot = sum(cost[(ln[0], ln[-1] + 1)] for ln in lines)
            t = label(rf"{title}: \ total {tot:.2f}", font_size=19, color=col).move_to(
                [x0 + lw * st2.s / 2 + 0.3, -1.0, 0])
            return VGroup(t, margin, rows, costs), tot
        kp_set, kp_tot = setting(kp_lines, YES, -6.6, r"shortest path")
        g_set, g_tot = setting(g_lines, NO, -2.4, r"greedy")
        assert abs(kp_tot - k["kp_stats"]["badness"]) < 1e-6 and abs(g_tot - k["greedy_stats"]["badness"]) < 1e-6
        notes = VGroup(
            wrapped_label(r"a node between every two words; \ an edge if the words between them fit on one line, "
                          r"\ weighted by that line's badness", 4.6, font_size=19, color=WHITE),
            wrapped_label(r"the best paragraph is the cheapest path from the first node to the last: \ dynamic "
                          r"programming over breakpoints, \ Part 19", 4.6, font_size=19, color=YES),
            wrapped_label(r"greedy fills line two with ``that a'' \ and leaves line three badly short", 4.6,
                          font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.4, -2.2, 0])
        src = note(r"the novel's opening sentence at a 190 px line", font_size=16).to_corner(DR, buff=0.15)
        with self.voiceover(
            "Knuth and Plass saw this as a graph. <bookmark mark='a'/> Put a node between every two words of "
            "the novel's opening sentence, and an edge wherever the words between two nodes fit on a line of "
            "one hundred and ninety pixels: eighty-seven edges, each weighted by its line's badness. "
            "<bookmark mark='b'/> The best paragraph is the cheapest path from first node to last, found by "
            "the dynamic programming of Part 19: the best cost to each node from the best costs before it. "
            "Its total is five point four one. <bookmark mark='c'/> Greedy squeezes that a onto line two and "
            "is left with a third line far too short: eight point five three. Locally best is globally worse."
        ) as vo:
            self.play(FadeIn(head), FadeIn(row), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(nodes), FadeIn(legend), FadeIn(notes[0]))
            self.play(Create(allarcs), run_time=2.5)
            vo.wait_until("b")
            self.play(allarcs.animate.set_stroke(opacity=0.18), Create(kp_arcs), run_time=1.5)
            self.play(FadeIn(kp_set), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(nodes_dn), Create(g_arcs), run_time=1.5)
            self.play(FadeIn(g_set), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ incremental relayout
    def relayout(self):
        r = load("relayout")
        nb, ke = r["blocks"], r["edited_block"]
        head = label(r"Incremental relayout", font_size=36).to_edge(UP, buff=0.3)
        bw, bh, pitch, y0, x0 = 3.6, 0.15, 0.215, 2.4, -6.4
        page = VGroup(*[Rectangle(width=bw, height=bh, stroke_width=0, fill_color=GREY_C, fill_opacity=0.7).move_to(
            [x0 + bw / 2, y0 - q * pitch, 0]) for q in range(nb)])
        frame = Rectangle(width=bw + 0.3, height=nb * pitch + 0.45, stroke_color=GREY_B, stroke_width=1.2).move_to(
            [x0 + bw / 2, y0 - (nb - 1) * pitch / 2 - 0.1, 0])
        ptitle = label(rf"the README: \ {nb} blocks, \ {r['words']} words", font_size=17, color=GREY_A).next_to(
            frame, UP, buff=0.08)
        schem = note(r"block heights schematic", font_size=16).next_to(frame, DOWN, buff=0.1)
        # the box tree: html, body, the blocks, and the edited block's line boxes
        html = tag_box("html", color=GREY_A, size=16).move_to([2.6, 2.4, 0])
        body = tag_box("body", color=GREY_A, size=16).move_to([2.6, 1.45, 0])
        kx = [-1.4 + q * (8.0 / (nb - 1)) for q in range(nb)]
        kids = VGroup(*[Dot([x, 0.4, 0], radius=0.07, color=GREY_B) for x in kx])
        e1 = Line(html.get_bottom(), body.get_top(), color=GREY_C, stroke_width=1.5)
        e2 = VGroup(*[Line(body.get_bottom(), d.get_center(), color=GREY_D, stroke_width=1) for d in kids])
        text = tag_box(rf"{r['edited_words']} words", color=HEAD, size=16).move_to([kx[ke], -0.5, 0])
        e3 = Line(kids[ke].get_center(), text.get_top(), color=GREY_C, stroke_width=1.5)
        flags = VGroup(
            label(r"needs layout", font_size=16, color=NO).next_to(text, RIGHT, buff=0.15),
            label(r"child needs layout", font_size=16, color=NO).next_to(body, RIGHT, buff=0.15),
            label(r"child needs layout", font_size=16, color=NO).next_to(html, RIGHT, buff=0.15),
        )
        notes = VGroup(
            wrapped_label(rf"an edit marks its box dirty, \ and a ``child needs layout'' bit climbs to the root; \ "
                          rf"layout then walks only the marked path", 8.0, font_size=19, color=WHITE),
            wrapped_label(rf"one paragraph's {r['edited_words']} words are broken again; \ the {r['shifted_blocks']} "
                          rf"blocks below only move; \ the rest of the {r['words']} words are untouched", 8.0,
                          font_size=19, color=YES),
            wrapped_label(r"reading a size from script, \ such as \texttt{offsetHeight}, \ forces this layout to "
                          r"happen at once: \ interleaved reads and writes cause layout thrashing", 8.0, font_size=19,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([2.6, -2.3, 0])
        grow = 0.12
        with self.voiceover(
            "Laying out the whole page on every change would waste the frame. <bookmark mark='a'/> So engines"
            " keep dirty bits: an edit marks its box, and a bit saying a child needs layout climbs to the "
            "root. <bookmark mark='b'/> Layout walks only the marked path. Editing one paragraph of our toy "
            "browser's README re-breaks its twenty-two words and moves the eleven blocks below; the rest of "
            "the seven hundred and eighty-six words are untouched. <bookmark mark='c'/> The catch: reading a "
            "size from script forces pending layout at once, so alternating reads and writes lays out the "
            "page again and again."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(page), FadeIn(ptitle), FadeIn(schem), FadeIn(html),
                      FadeIn(body),
                      Create(e1), Create(e2), FadeIn(kids))
            vo.wait_until("a")
            self.play(Create(e3), FadeIn(text), page[ke].animate.set_fill(HEAD, 1), kids[ke].animate.set_color(HEAD))
            for f in flags:
                self.play(FadeIn(f, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(page[ke].animate.stretch_to_fit_height(bh + grow).shift(DOWN * grow / 2),
                      *[page[q].animate.shift(DOWN * grow).set_fill(YES, 0.8) for q in range(ke + 1, nb)],
                      *[kids[q].animate.set_color(YES) for q in range(ke + 1, nb)], run_time=1.5)
            self.play(FadeIn(notes[1]), FadeOut(flags))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM)
