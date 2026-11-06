from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs42.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load, mono,
                                   tag_box)


class Perf(VoiceoverScene):
    def construct(self):
        self.card()
        self.crp()
        self.vitals()
        self.cls()
        self.bytes_()
        self.http()

    def card(self):
        card = chapter_card(10, r"Web performance", r"What does a page wait for before it can paint?",
                            lit=(2015, 2020, 2022), extra=((2015, r"HTTP/2"), (2020, r"Core Web Vitals"),
                                                           (2022, r"HTTP/3 over QUIC")), part=PART)
        with self.voiceover("Chapter ten. Web performance."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def crp(self):
        c = load("crp")
        res, blk, pre = c["resources"], c["blocking"], c["preloaded"]
        assert blk["path"] == ["HTML", "CSS", "font"] and pre["path"] == ["HTML", "font"]
        head = label(r"The critical rendering path", font_size=36).to_edge(UP, buff=0.3)
        x0, k = -4.0, 0.025                                     # ms -> scene units

        def X(t):
            return x0 + t * k
        names = list(res)                                       # HTML, CSS, font, JS (sync), hero image
        ys = {n: 2.0 - 0.68 * i for i, n in enumerate(names)}

        def start(n, fin):
            f, e, deps = res[n]
            return fin[n] - f - e if n in fin else max(fin[d] for d in deps)

        def span(t0, t1, y, col, op=0.85):
            return Rectangle(width=max(0.02, (t1 - t0) * k), height=0.34, stroke_width=0, fill_color=col,
                             fill_opacity=op).move_to([X((t0 + t1) / 2), y, 0])

        def bars(n, s):
            f, e, _ = res[n]
            g = VGroup(span(s, s + f, ys[n], DATA, 0.4 if n == "hero image" else 0.85))
            if e:
                g.add(span(s + f, s + f + e, ys[n], KERN))
            return g
        st = {n: start(n, blk["finish"]) for n in names}
        rows = {n: bars(n, st[n]) for n in names}
        ends = {n: st[n] + res[n][0] + res[n][1] for n in names}
        rnames = {n: label(n, font_size=19, color=GREY_A).next_to([x0, ys[n], 0], LEFT, buff=0.3) for n in names}
        fins = {n: label(rf"{ends[n]:.0f} ms", font_size=17, color=GREY_A).next_to(rows[n], RIGHT, buff=0.12)
                for n in names}
        for f in fins.values():                                 # the first-paint line passes behind them
            f.add_background_rectangle(color=BACKGROUND, opacity=1, buff=0.04)
        hero_note = label(r"not render-blocking", font_size=16, color=WHITE).move_to(rows["hero image"])
        ya = -1.15
        axis = Line([X(0), ya, 0], [X(400), ya, 0], color=GREY_C, stroke_width=1.5)
        ticks = VGroup(*[VGroup(Line([X(t), ya - 0.06, 0], [X(t), ya + 0.06, 0], color=GREY_C),
                                label(rf"{t} ms", font_size=16, color=GREY_B).move_to([X(t), ya - 0.25, 0]))
                         for t in range(0, 401, 100)])
        legend = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=col, fill_opacity=0.85),
                                 label(t, font_size=17, color=GREY_A)).arrange(RIGHT, buff=0.12)
                          for t, col in ((r"fetch", DATA), (r"parse or execute", KERN))],
                        note(r"illustrative timings", font_size=17)).arrange(RIGHT, buff=0.4)
        legend.move_to([0, 2.65, 0]).align_to(rnames["hero image"], LEFT)

        def lit(path, rws):
            return VGroup(*[SurroundingRectangle(rws[n], color=HEAD, buff=0.05, stroke_width=3) for n in path])

        def paint_line(t):
            ln = DashedLine([X(t), 2.4, 0], [X(t), ya, 0], color=HEAD, stroke_width=2.5)
            tx = label(rf"first paint: \ {t:.0f} ms", font_size=19, color=HEAD).next_to(ln, UP, buff=0.08)
            return VGroup(ln, tx)
        path1 = lit(blk["path"], rows)
        fp1 = paint_line(blk["first_paint"])
        notes = VGroup(
            wrapped_label(r"first paint waits for every render-blocking resource; \ the longest chain, \ HTML $\to$ "
                          r"CSS $\to$ font, \ is the \textbf{critical path} \ (Part 41's build graph, \ with time "
                          r"on the edges)", 12.6, font_size=19, color=HEAD),
            wrapped_label(rf"defer the script and preload the font from the HTML: \ the path becomes HTML $\to$ font "
                          rf"and first paint moves to {pre['first_paint']:.0f} ms; \ preloading alone would leave "
                          rf"the script's {blk['finish']['JS (sync)']:.0f} ms", 12.6, font_size=19, color=YES),
            wrapped_label(r"browsers also rank their fetches: \ stylesheets and fonts high, \ images low; \ "
                          r"\texttt{fetchpriority=high} lifts the one image that matters most", 12.6, font_size=19,
                          color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)
        # the improved page: the font's fetch starts when the HTML is read; the script no longer blocks
        font_shift = (start("font", pre["finish"]) - st["font"]) * k
        with self.voiceover(
            "Before a page can show anything, the browser must fetch and process everything that blocks rendering. "
            "Here is one page as a dependency graph, with illustrative timings. <bookmark mark='a'/> The HTML arrives "
            "first. It names a stylesheet and a synchronous script, and the stylesheet names a font, so each fetch "
            "waits for the file that mentions it. <bookmark mark='b'/> First paint waits for all of them, and the "
            "longest chain, HTML, CSS, font, is the critical path: three hundred and forty-five milliseconds. It is "
            "Part 41's build graph, with time on the edges. <bookmark mark='c'/> Now defer the script, and preload the"
            " font from the HTML. The font starts a hundred milliseconds earlier, and first paint moves to two hundred"
            " and forty-five. <bookmark mark='d'/> Browsers also rank their fetches, stylesheets and fonts high, "
            "images low, and a page can raise the one image that matters most."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(ticks), FadeIn(VGroup(*rnames.values())), FadeIn(legend))
            vo.wait_until("a")
            for wave in (["HTML"], ["CSS", "JS (sync)", "hero image"], ["font"]):
                self.play(*[GrowFromEdge(rows[n], LEFT) for n in wave], run_time=0.8)
                self.play(*[FadeIn(fins[n]) for n in wave], *([FadeIn(hero_note)] if "hero image" in wave else []),
                          run_time=0.4)
            vo.wait_until("b")
            self.play(Create(path1), FadeIn(fp1), FadeIn(notes[0]))
            self.bring_to_front(*fins.values())
            vo.wait_until("c")
            js = names[3]
            new_js = label(r"JS (defer)", font_size=19, color=GREY_B).move_to(rnames[js], aligned_edge=RIGHT)
            new_fin = label(rf"{pre['finish']['font']:.0f} ms", font_size=17, color=GREY_A)
            new_fin.add_background_rectangle(color=BACKGROUND, opacity=1, buff=0.04)
            new_fin.next_to(rows["font"].copy().shift(RIGHT * font_shift), RIGHT, buff=0.12)
            self.play(FadeOut(path1), rows[js].animate.set_opacity(0.2), fins[js].animate.set_opacity(0.3),
                      Transform(rnames[js], new_js))
            self.play(rows["font"].animate.shift(RIGHT * font_shift), Transform(fins["font"], new_fin))
            path2 = lit(pre["path"], rows)
            fp2 = paint_line(pre["first_paint"])
            self.play(Create(path2), Transform(fp1, fp2), FadeIn(notes[1]))
            self.bring_to_front(*fins.values())
            vo.wait_until("d")
            self.play(FadeIn(notes[2]), Indicate(rows["hero image"], color=HEAD, scale_factor=1.05))
        self.wait(0.4)
        self.clear_scene()

    def vitals(self):
        head = label(r"Core Web Vitals", font_size=36).to_edge(UP, buff=0.3)
        specs = [(r"LCP", r"Largest Contentful Paint",
                  r"when the biggest image or block of text is drawn: \ \textbf{loading}", (r"2.5 s", r"4 s"), DATA),
                 (r"INP", r"Interaction to Next Paint",
                  r"from a tap or key press to the next frame: \ \textbf{responsiveness}", (r"200 ms", r"500 ms"),
                  LAM),
                 (r"CLS", r"Cumulative Layout Shift",
                  r"how much the page jumps while you read it: \ \textbf{stability}", (r"0.1", r"0.25"), KERN)]

        def band(th):
            rects = VGroup(*[Rectangle(width=w, height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.8)
                             for w, col in ((1.5, YES), (2.1, HEAD), (1.5, NO))]).arrange(RIGHT, buff=0)
            txt = VGroup(*[label(t, font_size=16, color=BLACK).move_to(r)
                           for t, r in zip((r"good", r"needs improvement", r"poor"), rects)])
            tk = VGroup(*[label(t, font_size=17, color=GREY_A).next_to(rects[i].get_corner(DR), DOWN, buff=0.1)
                          for i, t in enumerate(th)])
            return VGroup(rects, txt, tk)
        rows = VGroup()
        for i, (ab, full, desc, th, col) in enumerate(specs):
            y = 1.85 - 1.3 * i
            name = VGroup(label(ab, font_size=30, color=col), label(full, font_size=18, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08).move_to([-5.3, y, 0]).to_edge(LEFT, buff=0.35)
            d = wrapped_label(desc, 3.9, font_size=19, color=WHITE).move_to([0, y, 0]).align_to([-3.0, 0, 0], LEFT)
            b = band(th).move_to([4.1, y - 0.1, 0])
            rows.add(VGroup(name, d, b))
        notes = VGroup(
            wrapped_label(r"Google, \ 2020: \ measured in real users' browsers; \ a page passes when 75\% of its "
                          r"visits are good", 12.6, font_size=20, color=WHITE),
            wrapped_label(r"INP replaced \textbf{First Input Delay} in March 2024: \ FID timed only the wait before "
                          r"the first interaction began, \ not the whole delay of every one", 12.6, font_size=20,
                          color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In 2020 Google named three Core Web Vitals, measured in real users' browsers. <bookmark mark='a'/> "
            "Largest Contentful Paint is the time until the biggest image or block of text is drawn; under two and "
            "a half seconds is good. <bookmark mark='b'/> Interaction to Next Paint is the delay from a tap or a key "
            "press to the next frame. In March 2024 it replaced First Input Delay, which timed only the wait before "
            "the first interaction began. Under two hundred milliseconds is good. <bookmark mark='c'/> Cumulative "
            "Layout Shift measures how much the page jumps while you read it; under a tenth is good. "
            "<bookmark mark='d'/> A page passes when three visits in four are good."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[0]))
        self.wait(0.4)
        self.clear_scene()

    def cls(self):
        d = load("cls")
        shifts, windows = d["shifts"], d["windows"]
        head = label(r"Layout shift, \ scored", font_size=36).to_edge(UP, buff=0.3)
        # one shift: the element before (dashed) and after (solid); impact = the union's share of the viewport
        vp = Rectangle(width=1.7, height=1.9, stroke_color=GREY_B, stroke_width=2).move_to([-5.7, 1.95, 0])
        before = DashedVMobject(Rectangle(width=1.3, height=0.42, stroke_color=GREY_A, stroke_width=2),
                                num_dashes=24).move_to([-5.8, 2.5, 0])
        after = Rectangle(width=1.3, height=0.42, stroke_color=KERN, stroke_width=2.5, fill_color=KERN,
                          fill_opacity=0.35).move_to([-5.8, 1.85, 0])
        union = Rectangle(width=1.3, height=before.get_top()[1] - after.get_bottom()[1], stroke_width=0,
                          fill_color=KERN, fill_opacity=0.15).move_to([-5.8, (before.get_top()[1] +
                                                                              after.get_bottom()[1]) / 2, 0])
        dist = Arrow([-4.98, 2.5, 0], [-4.98, 1.85, 0], buff=0, stroke_width=2.5, color=HEAD,
                     max_tip_length_to_length_ratio=0.25)
        formula = MathTex(r"\text{shift score} = \text{impact fraction} \times \text{distance fraction}",
                          font_size=30, color=WHITE).move_to([0.9, 2.6, 0])
        expl = VGroup(
            wrapped_label(r"\textbf{impact fraction}: \ the share of the viewport covered by the moving element, \ "
                          r"before and after", 9.0, font_size=19, color=KERN),
            wrapped_label(r"\textbf{distance fraction}: \ how far it moved, \ as a share of the viewport's larger "
                          r"side", 9.0, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(formula, DOWN, buff=0.22).align_to(formula, LEFT)
        # the timeline of five shifts
        base_y, hk = -0.95, 10.0

        def X(t):
            return -5.6 + 1.2 * t
        axis = Line([X(0), base_y, 0], [X(10), base_y, 0], color=GREY_C, stroke_width=1.5)
        ticks = VGroup(*[label(rf"{t} s", font_size=16, color=GREY_B).move_to([X(t), base_y - 0.22, 0])
                         for t in range(0, 11, 2)])
        scores = [i * dd for _, i, dd in shifts]
        sbars = VGroup(*[Rectangle(width=0.22, height=max(0.02, s * hk), stroke_width=0, fill_color=KERN,
                                   fill_opacity=0.85).move_to([X(t), base_y + max(0.02, s * hk) / 2, 0])
                         for (t, _, _), s in zip(shifts, scores)])
        svals = VGroup(*[label(f"{s:g}", font_size=16, color=GREY_A).next_to(b, UP, buff=0.08)
                         for b, s in zip(sbars, scores)])
        # session windows: a new window after a gap of 1 s, or once a window has lasted 5 s
        groups, cur = [], []
        for k, (t, _, _) in enumerate(shifts):
            if cur and (t - shifts[cur[-1]][0] >= 1.0 or t - shifts[cur[0]][0] >= 5.0):
                groups.append(cur)
                cur = []
            cur.append(k)
        groups.append(cur)
        assert [round(sum(scores[k] for k in g), 9) for g in groups] == [round(w, 9) for w in windows]
        worst = max(range(len(windows)), key=lambda j: windows[j])
        brackets = VGroup()
        for j, g in enumerate(groups):
            xa, xb = X(shifts[g[0]][0]) - 0.25, X(shifts[g[-1]][0]) + 0.25
            col = HEAD if j == worst else GREY_A
            y = base_y - 0.55
            br = VGroup(Line([xa, y, 0], [xb, y, 0], color=col, stroke_width=2.5),
                        Line([xa, y, 0], [xa, y + 0.12, 0], color=col, stroke_width=2.5),
                        Line([xb, y, 0], [xb, y + 0.12, 0], color=col, stroke_width=2.5))
            br.add(label(rf"window {j + 1}: \ {windows[j]:g}", font_size=17, color=col).next_to(br, DOWN, buff=0.1))
            brackets.add(br)
        ill = note(r"illustrative shifts", font_size=17).move_to([5.6, 0.45, 0])
        score = wrapped_label(rf"CLS is the \textbf{{worst window}}: \ {d['score']:g}, \ above 0.1, \ so "
                              r"\textit{needs improvement}; \ the usual culprits: \ images without a width and "
                              r"height, \ late fonts and adverts", 12.6, font_size=20,
                              color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Layout shift has its own arithmetic. <bookmark mark='a'/> When a visible element moves, the shift scores "
            "its impact fraction, the share of the viewport it covers before and after, times its distance fraction, "
            "how far it moved. <bookmark mark='b'/> Here are five shifts in a page's first ten seconds. <bookmark "
            "mark='c'/> They are grouped into session windows, which close after a gap of a second, or after five "
            "seconds in all. Ours form three, worth point zero eight five, point one two five, and point zero zero two"
            " five. <bookmark mark='d'/> The score is the worst window, point one two five, which needs improvement. "
            "The usual culprits are images without a width and height, and late fonts and adverts."
        ) as vo:
            self.play(FadeIn(head), Create(vp), Create(before))
            vo.wait_until("a")
            self.play(TransformFromCopy(before, after), FadeIn(union), GrowArrow(dist), Write(formula))
            self.play(FadeIn(expl))
            vo.wait_until("b")
            self.play(Create(axis), FadeIn(ticks), FadeIn(ill))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in sbars], lag_ratio=0.3), FadeIn(svals))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b) for b in brackets], lag_ratio=0.5), run_time=2)
            vo.wait_until("d")
            self.play(Indicate(brackets[worst], color=HEAD), FadeIn(score))
        self.wait(0.4)
        self.clear_scene()

    def bytes_(self):
        rows = load("compress")["rows"]
        head = label(r"Fewer bytes", font_size=36).to_edge(UP, buff=0.3)
        codecs = (("gzip", DATA), ("bz2", LAM), ("xz", KERN))
        full = 4.0
        groups = VGroup()
        for r in rows:
            title = VGroup(mono(r["file"].split("/")[-1], size=17, color=WHITE),
                           label(rf"{r['bytes']:,} bytes", font_size=17, color=GREY_B)).arrange(RIGHT, buff=0.25)
            g = VGroup(title)
            for c, col in codecs:
                frac = r[c] / r["bytes"]
                ref = Rectangle(width=full, height=0.24, stroke_color=GREY_D, stroke_width=1)
                bar = Rectangle(width=full * frac, height=0.24, stroke_width=0, fill_color=col, fill_opacity=0.85)
                bar.align_to(ref, LEFT)
                name = label(c, font_size=17, color=col).next_to(ref, LEFT, buff=0.15)
                name.align_to(ref.get_left() + LEFT * 0.75, LEFT)
                val = label(rf"{100 * frac:.1f}\%", font_size=16, color=col).next_to(ref, RIGHT, buff=0.12)
                g.add(VGroup(name, ref, bar, val))
            g[1:].arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            g[0].next_to(g[1:], UP, buff=0.12).align_to(g[1:], LEFT)
            groups.add(g)
        groups.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([-3.6, 0.35, 0]).to_edge(LEFT, buff=0.35)
        src = note(r"measured on this repository's files; \ Brotli is not installed here", font_size=17)
        src.next_to(groups, DOWN, buff=0.2).align_to(groups, LEFT)
        # images: one picture in three widths; the browser picks by the layout width and the screen's density
        ws = (480, 960, 1920)
        pics = VGroup(*[Rectangle(width=w / 800, height=w / 800 * 9 / 16, stroke_color=YES if w == 480 else GREY_B,
                                  stroke_width=2, fill_color=YES if w == 480 else GREY_D, fill_opacity=0.25)
                        for w in ws]).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        plabs = VGroup(*[mono(f"{w}w", size=16, color=YES if w == 480 else GREY_A).next_to(p, DOWN, buff=0.08)
                         for w, p in zip(ws, pics)])
        img = code_block(['<img src="cat-960.avif" alt="A cat asleep"', '  srcset="cat-480.avif 480w,',
                          '          cat-960.avif 960w,', '          cat-1920.avif 1920w"',
                          '  sizes="100vw" loading="lazy"', '  width="1920" height="1080">'], size=16)
        right = VGroup(VGroup(pics, plabs), img).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        right.move_to([3.6, 0.9, 0]).to_edge(RIGHT, buff=0.35)
        inotes = VGroup(
            wrapped_label(r"\textbf{AVIF} and \textbf{WebP}: \ smaller files at the same quality", 5.6,
                          font_size=18, color=WHITE),
            wrapped_label(r"\texttt{srcset}: \ a small screen fetches the small file; \ \texttt{loading=lazy}: \ "
                          r"wait until it is near the viewport; \ \texttt{width}, \texttt{height}: \ reserve its "
                          r"space, \ no layout shift", 5.6, font_size=18, color=YES),
            note(r"illustrative markup", font_size=17),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(right, DOWN, buff=0.25).align_to(right, LEFT)
        syl = rows[1]
        pct = round(100 * syl["gzip"] / syl["bytes"])
        with self.voiceover(
            f"Fewer bytes arrive sooner. <bookmark mark='a'/> We measured three of this series' own files. Gzip, which"
            f" every browser accepts, shrinks the syllabus to {pct} per cent of its size. Bzip2 and xz do better, but "
            f"browsers do not accept them, and the web's newer codec, Brotli, is not installed here, so we have no "
            f"figure for it. <bookmark mark='b'/> Images are usually most of the bytes. AVIF and WebP are smaller at "
            f"the same quality; a source set lets a small screen fetch a small file; lazy loading waits until an image"
            f" is near; and a width and height reserve its space."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            for g in groups:
                self.play(FadeIn(g[0]), *[FadeIn(VGroup(b[0], b[1])) for b in g[1:]], run_time=0.5)
                self.play(*[GrowFromEdge(b[2], LEFT) for b in g[1:]], *[FadeIn(b[3]) for b in g[1:]], run_time=0.8)
            self.play(FadeIn(src))
            vo.wait_until("b")
            self.play(FadeIn(pics), FadeIn(plabs), FadeIn(img))
            self.play(FadeIn(inotes))
        self.wait(0.4)
        self.clear_scene()

    def http(self):
        head = label(r"HTTP/2 and HTTP/3", font_size=36).to_edge(UP, buff=0.3)
        streams = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]
        scol = (DATA, LAM, YES)
        lost = 3
        x0, step = -2.9, 0.64

        def lane(y):
            sq = VGroup(*[Square(0.5, stroke_width=0, fill_color=scol[s], fill_opacity=0.85).move_to(
                [x0 + i * step, y, 0]) for i, s in enumerate(streams)])
            wire = Line([x0 - 0.45, y, 0], [x0 + 12.4 * step, y, 0], color=GREY_D, stroke_width=1.5)
            return wire, sq
        y2, y3 = 1.25, -0.9
        w2, l2 = lane(y2)
        w3, l3 = lane(y3)
        names = VGroup(
            VGroup(label(r"HTTP/2", font_size=24, color=WHITE), label(r"over TCP \ (2015)", font_size=17,
                                                                     color=GREY_B)).arrange(DOWN, buff=0.06),
            VGroup(label(r"HTTP/3", font_size=24, color=WHITE), label(r"over QUIC \ (2022)", font_size=17,
                                                                     color=GREY_B)).arrange(DOWN, buff=0.06))
        names[0].move_to([-5.4, y2, 0])
        names[1].move_to([-5.4, y3, 0])
        legend = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=c, fill_opacity=0.85),
                                 label(t, font_size=17, color=GREY_A)).arrange(RIGHT, buff=0.1)
                          for t, c in zip((r"stream 1: \ HTML", r"stream 2: \ CSS", r"stream 3: \ an image"), scol)],
                        note(r"illustrative", font_size=17)).arrange(RIGHT, buff=0.45).move_to([0.6, 2.5, 0])

        def cross(sq):
            return VGroup(Line(sq.get_corner(UL), sq.get_corner(DR), color=NO, stroke_width=4),
                          Line(sq.get_corner(DL), sq.get_corner(UR), color=NO, stroke_width=4))
        x2, x3 = cross(l2[lost]), cross(l3[lost])
        cap2 = wrapped_label(r"one connection, \ streams interleaved as frames; \ TCP delivers bytes in order, \ so "
                             r"one lost packet stalls \textbf{every} stream: \ head-of-line blocking \ (Part 37)", 9.6,
                             font_size=19, color=NO).next_to(l2, DOWN, buff=0.22).align_to(l2, LEFT)
        cap3 = wrapped_label(r"QUIC, \ on UDP, \ keeps order only \textit{within} a stream: \ a loss stalls just its "
                             r"own; \ its handshake includes TLS 1.3 \ (Part 30), \ one round trip fewer", 9.6,
                             font_size=19, color=YES).next_to(l3, DOWN, buff=0.22).align_to(l3, LEFT)
        h1 = wrapped_label(r"before them, \ HTTP/1.1 carried one request at a time per connection, \ so browsers "
                           r"opened about six connections to each host", 12.6, font_size=19,
                           color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Then the connection itself. <bookmark mark='a'/> HTTP one point one carries one request at a time per "
            "connection, so browsers opened about six connections to each host. HTTP/2, in 2015, multiplexes many "
            "streams over a single TCP connection, as interleaved frames. <bookmark mark='b'/> But TCP delivers "
            "bytes strictly in order, so when one packet is lost, every stream waits for its retransmission: "
            "head-of-line blocking, from Part 37. <bookmark mark='c'/> HTTP/3, standardised in 2022, runs over QUIC "
            "on UDP, which keeps order only within each stream. A loss now stalls only the stream it belongs to, "
            "and the handshake folds in TLS, from Part 30, saving a round trip."
        ) as vo:
            self.play(FadeIn(head), FadeIn(names[0]), Create(w2), FadeIn(legend))
            vo.wait_until("a")
            self.play(FadeIn(h1), LaggedStart(*[FadeIn(s, shift=RIGHT * 0.2) for s in l2], lag_ratio=0.15),
                      run_time=2)
            vo.wait_until("b")
            self.play(Create(x2), l2[lost].animate.set_opacity(0.3))
            self.play(*[l2[i].animate.set_opacity(0.25) for i in range(lost + 1, len(streams))], FadeIn(cap2))
            vo.wait_until("c")
            self.play(FadeIn(names[1]), Create(w3), LaggedStart(*[FadeIn(s, shift=RIGHT * 0.2) for s in l3],
                                                                 lag_ratio=0.1), run_time=1.6)
            self.play(Create(x3), l3[lost].animate.set_opacity(0.3))
            self.play(*[l3[i].animate.set_opacity(0.25) for i in range(lost + 1, len(streams))
                        if streams[i] == streams[lost]], FadeIn(cap3))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, grid_table, tag_box)
