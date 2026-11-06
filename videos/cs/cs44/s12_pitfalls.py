from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs44.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load, trace

METRICS = ("clicks", "revenue", "sessions", "time on page", "sign-ups", "basket size", "returns", "searches",
           "shares", "scroll depth", "page views", "bounces", "log-ins", "add to cart", "checkouts", "refunds",
           "ratings", "tickets", "emails opened", "video plays")


class Pitfalls(VoiceoverScene):
    def construct(self):
        self.card()
        self.multiple()
        self.bh()
        self.srm()
        self.simpson()
        self.time()
        self.twyman()

    def card(self):
        card = chapter_card(11, r"Pitfalls at scale", r"How do careful experiments still go wrong?",
                            lit=(1951, 1995), extra=((1951, r"Simpson: \ the paradox"),
                                                     (1995, r"Benjamini and Hochberg: \ false discovery rate")),
                            part=PART)
        with self.voiceover("Chapter eleven. Pitfalls at scale."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def multiple(self):
        m = load("metrics")
        head = label(r"Twenty metrics, \ twenty chances", font_size=36).to_edge(UP, buff=0.3)
        tiles = VGroup()
        for name in METRICS:
            r = RoundedRectangle(width=1.55, height=0.62, corner_radius=0.08, stroke_color=GREY_B, stroke_width=1.5,
                                 fill_color=BG, fill_opacity=1)
            nm = label(name, font_size=17, color=GREY_A)
            nm.width = min(nm.width, 1.45)
            tiles.add(VGroup(r, nm.move_to(r)))
        tiles.arrange_in_grid(rows=5, cols=4, buff=(0.15, 0.18)).move_to([-3.3, -0.3, 0])
        rng = np.random.default_rng(18)
        draws = [rng.uniform(size=m["k"]) for _ in range(3)]
        lit = [[i for i, p in enumerate(d) if p < 0.05] for d in draws]
        notes = VGroup(
            wrapped_label(rf"an A/A experiment with {m['k']} metrics; \ none really moved; \ each tested at 5\%", 5.0,
                          font_size=20, color=GREY_A),
            MathTex(rf"P(\text{{at least one }} p < 0.05) = 1 - 0.95^{{{m['k']}}} = {100 * m['theory']:.1f}\%",
                    font_size=28, color=NO),
            wrapped_label(rf"simulated: \ {100 * m['naive']:.1f}\% of experiments show a \ ``significant'' metric",
                          5.0, font_size=20, color=NO),
            wrapped_label(r"report the one that moved, \ and you have reported noise", 5.0, font_size=20,
                          color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([3.6, -0.2, 0])
        ill = note(r"illustrative draws", font_size=17).next_to(tiles, DOWN, buff=0.15).align_to(tiles, RIGHT)

        def light(ids):
            return [tiles[i][0].animate.set_stroke(NO, width=3).set_fill(NO, opacity=0.25) if i in ids else
                    tiles[i][0].animate.set_stroke(GREY_B, width=1.5).set_fill(BG, opacity=1)
                    for i in range(len(tiles))]
        with self.voiceover(
            "Experiments report dozens of metrics. Take twenty, and a change that moved none of them. "
            "<bookmark mark='a'/> Each has a five percent chance of looking significant. <bookmark mark='b'/> Run "
            "the experiment, and one metric lights up; run another, and a different one does. "
            "<bookmark mark='c'/> The chance that at least one lights up is one minus point nine five to the "
            f"twentieth, {100 * m['theory']:.0f} percent; our simulation found {100 * m['naive']:.0f}. "
            "<bookmark mark='d'/> Report the metric that moved, and you have usually reported noise: Part 2's "
            "counting, turned against us."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(t) for t in tiles], lag_ratio=0.03), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(ill))
            vo.wait_until("b")
            for ids in lit:
                self.play(*light(ids), run_time=0.8)
                self.wait(0.5)
            vo.wait_until("c")
            self.play(Write(notes[1]))
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def bh(self):
        m = load("metrics")
        k = m["k"]
        head = label(r"Controlling false discoveries", font_size=36).to_edge(UP, buff=0.3)
        rng = np.random.default_rng(3)
        ps = np.sort(np.r_[[0.0002, 0.0015, 0.004, 0.009], rng.uniform(0.06, 1, k - 4)])
        lg = np.log10
        g = axes([0, k + 1, 5], [-4, 0, 1], x_length=7.2, y_length=4.2, x_label=r"metrics, \ sorted by p-value",
                 y_label=r"p-value \ (log scale)", xticks=range(5, k + 1, 5), yticks=(-4, -3, -2, -1, 0),
                 fy=lambda v: f"{10 ** v:g}").move_to([-2.7, -0.35, 0])
        ax = g.ax
        cut = max([i + 1 for i, p in enumerate(ps) if p <= 0.05 * (i + 1) / k], default=0)
        dots = VGroup(*[Dot(ax.c2p(i + 1, lg(p)), radius=0.07, color=GREY_B) for i, p in enumerate(ps)])
        bhl = trace(ax, [(x, lg(0.05 * x / k)) for x in np.linspace(0.5, k, 60)], YES, width=3)
        bon = DashedLine(ax.c2p(0, lg(0.05 / k)), ax.c2p(k + 1, lg(0.05 / k)), color=NO)
        bhn = label(r"$\alpha\, i / k$", font_size=20, color=YES).next_to(ax.c2p(k, lg(0.05)), DOWN, buff=0.15)
        bon_n = label(r"Bonferroni: \ $\alpha / k$", font_size=17, color=NO).next_to(ax.c2p(k + 1, lg(0.05 / k)),
                                                                                    DOWN, buff=0.1).shift(LEFT * 0.9)
        notes = VGroup(
            wrapped_label(r"Benjamini and Hochberg \ (1995): \ sort the $k$ p-values; \ find the largest $i$ with "
                          r"$p_{(i)} \le \alpha\, i/k$; \ declare the first $i$", 4.5, font_size=20, color=WHITE),
            wrapped_label(r"it controls the \textbf{false discovery rate}: \ the expected share of declared effects "
                          r"that are not real", 4.5, font_size=20, color=YES),
            wrapped_label(rf"with nothing real, \ at least one false discovery in {100 * m['bh']:.1f}\% of "
                          rf"experiments, \ against {100 * m['naive']:.1f}\% uncorrected", 4.5, font_size=20,
                          color=HEAD),
            note(r"four real effects among twenty: \ illustrative", font_size=17),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.4, -0.2, 0])
        with self.voiceover(
            "The cure is to be less impressed the more you look. <bookmark mark='a'/> Bonferroni divides the "
            "threshold by the number of tests: safe, but strict. <bookmark mark='b'/> In 1995 Yoav Benjamini and "
            "Yosef Hochberg proposed a gentler line: sort the p-values, and compare the i-th smallest with alpha "
            "times i over k. <bookmark mark='c'/> Everything up to the last point under the line is a discovery. "
            "<bookmark mark='d'/> This controls the false discovery rate, the expected share of discoveries that "
            f"are false. With nothing real, only {100 * m['bh']:.0f} percent of our experiments made any."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.1),
                      FadeIn(notes[3]))
            vo.wait_until("a")
            self.play(Create(bon), FadeIn(bon_n))
            vo.wait_until("b")
            self.play(Create(bhl), FadeIn(bhn), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(*[dots[i].animate.set_color(YES).scale(1.3) for i in range(cut)])
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def srm(self):
        s = load("srm")
        bad, fine = s["bad"], s["fine"]
        head = label(r"Check the split first", font_size=36).to_edge(UP, buff=0.3)
        lo, hi, H = 48_000, 51_000, 3.6

        def bars(case, x0):
            g = VGroup()
            for j, (n, col, nm) in enumerate(((case["a"], DATA, "A"), (case["b"], LAM, "B"))):
                h = (n - lo) / (hi - lo) * H
                r = Rectangle(width=0.9, height=h, stroke_width=0, fill_color=col, fill_opacity=0.85)
                r.move_to([x0 + j * 1.3, -2.4, 0], aligned_edge=DOWN)
                g.add(VGroup(r, VGroup(label(nm, font_size=20, color=col), label(f"{n:,}", font_size=18, color=col))
                             .arrange(DOWN, buff=0.08).next_to(r, DOWN, buff=0.12)))
            e = (case["a"] + case["b"]) / 2
            ey = -2.4 + (e - lo) / (hi - lo) * H
            g.add(DashedLine([x0 - 0.7, ey, 0], [x0 + 2.0, ey, 0], color=GREY_A))
            return g
        b1, b2 = bars(bad, -5.6), bars(fine, -2.3)
        cut = note(r"bars start at 48,000", font_size=16).move_to([-3.3, -3.45, 0])
        exp = label(r"expected: \ half", font_size=16, color=GREY_A).next_to(b1[2], UP, buff=0.1).align_to(b1[2], LEFT)
        chi = MathTex(r"\chi^2 = \sum \frac{(O - E)^2}{E}", font_size=32, color=WHITE)
        r1 = wrapped_label(rf"{bad['a']:,} against {bad['b']:,}: \ $\chi^2 = {bad['chi2']:.1f}$, \ "
                           rf"$p = {bad['p']:.4f}$: \ the split is broken", 5.0, font_size=20, color=NO)
        r2 = wrapped_label(rf"{fine['a']:,} against {fine['b']:,}: \ $\chi^2 = {fine['chi2']:.1f}$, \ "
                           rf"$p = {fine['p']:.2f}$: \ chance", 5.0, font_size=20, color=YES)
        causes = wrapped_label(r"causes: \ a redirect that loses users in one arm, \ bots filtered unevenly, \ a crash "
                               r"that stops one version logging", 5.0, font_size=19, color=GREY_A)
        rule = wrapped_label(r"a \textbf{sample-ratio mismatch} invalidates every metric of the experiment", 5.0,
                             font_size=20, color=HEAD)
        VGroup(chi, r1, r2, causes, rule).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, -0.2, 0])
        with self.voiceover(
            "Before reading any metric, check the split. <bookmark mark='a'/> A fifty-fifty test that ends with "
            f"{bad['a']:,} users in one arm and {bad['b']:,} in the other looks close. <bookmark mark='b'/> "
            f"Pearson's chi-squared test disagrees: chi-squared is {bad['chi2']:.1f}, and a gap this large happens "
            f"by chance about {10000 * bad['p']:.0f} times in ten thousand. <bookmark mark='c'/> {fine['a']:,} "
            f"against {fine['b']:,} is ordinary luck. <bookmark mark='d'/> A mismatch means something removed users "
            "unevenly: a redirect, a bot filter, a crash that stops one version logging. The users who remain are "
            "no longer comparable, so every metric is suspect."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cut))
            vo.wait_until("a")
            self.play(*[GrowFromEdge(b[0], DOWN) for b in b1[:2]], *[FadeIn(b[1:]) for b in b1[:2]], Create(b1[2]),
                      FadeIn(exp))
            vo.wait_until("b")
            self.play(Write(chi))
            self.play(FadeIn(r1))
            vo.wait_until("c")
            self.play(*[GrowFromEdge(b[0], DOWN) for b in b2[:2]], *[FadeIn(b[1:]) for b in b2[:2]], Create(b2[2]),
                      FadeIn(r2))
            vo.wait_until("d")
            self.play(FadeIn(causes))
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def simpson(self):
        sp = load("simpson")
        data, rates = sp["data"], sp["rates"]
        head = label(r"Simpson's paradox", font_size=36).to_edge(UP, buff=0.3)
        H, vmax = 3.4, 0.13
        y0 = -1.9
        groups = VGroup()
        for j, seg in enumerate(("desktop", "mobile", "overall")):
            x0 = -6.0 + j * 2.5
            g = VGroup()
            for i, (v, col, nm) in enumerate((("old", GREY_B, "old"), ("new", HEAD, "new"))):
                r = rates[v][seg]
                b = Rectangle(width=0.8, height=max(0.02, r / vmax * H), stroke_width=0, fill_color=col,
                              fill_opacity=0.85).move_to([x0 + i * 1.0, y0, 0], aligned_edge=DOWN)
                g.add(VGroup(b, label(rf"{100 * r:.1f}\%", font_size=18, color=col).next_to(b, UP, buff=0.08),
                             label(nm, font_size=16, color=col).next_to(b, DOWN, buff=0.1)))
            g.add(label(seg, font_size=20, color=WHITE if seg != "overall" else NO).next_to(g, DOWN, buff=0.15))
            groups.add(g)
        sep = DashedLine([-1.55, y0 - 0.7, 0], [-1.55, y0 + 3.4, 0], color=GREY_D)
        rows = [[r"old", f"{data['old']['desktop'][1]:,}", f"{data['old']['mobile'][1]:,}"],
                [r"new", f"{data['new']['desktop'][1]:,}", f"{data['new']['mobile'][1]:,}"]]
        tab = grid_table([r"visitors", r"desktop", r"mobile"], rows, widths=[1.3, 1.6, 1.6], row_h=0.48,
                         font_size=19, mono_cols=())
        tab.cells[2][2].set_color(HEAD)
        tab.move_to([3.9, 1.6, 0])
        notes = VGroup(
            wrapped_label(r"the new version wins on desktop and on mobile, \ and loses overall", 5.2, font_size=20,
                          color=NO),
            wrapped_label(r"its traffic was mostly mobile, \ where everyone converts less: \ the overall rate "
                          r"averages the segments with different weights", 5.2, font_size=20, color=WHITE),
            wrapped_label(r"in a randomized test both arms get the same mix; \ a mix that differs means the split "
                          r"changed midway, \ or the groups were not randomized \ (a before-and-after comparison)",
                          5.2, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.35)
        ill = note(r"illustrative counts", font_size=17).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Averages can reverse. <bookmark mark='a'/> A redesign converts better on desktop, "
            f"{100 * rates['new']['desktop']:.1f} percent against {100 * rates['old']['desktop']:.0f}, "
            f"<bookmark mark='b'/> and better on mobile, {100 * rates['new']['mobile']:.1f} against "
            f"{100 * rates['old']['mobile']:.0f}. <bookmark mark='c'/> Yet overall it converts worse: "
            f"{100 * rates['new']['overall']:.1f} percent against {100 * rates['old']['overall']:.1f}. "
            "<bookmark mark='d'/> Its visitors were mostly on mobile, where everyone converts less, and the overall "
            "rate weights segments by traffic: Simpson's paradox, after Edward Simpson's paper of 1951. "
            "<bookmark mark='e'/> A randomized test gives both arms the same mix, so a mix like this is itself a "
            "warning: the split changed midway, or nothing was randomized."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ill), Create(sep))
            vo.wait_until("a")
            self.play(*[GrowFromEdge(b[0], DOWN) for b in groups[0][:2]], *[FadeIn(b[1:]) for b in groups[0][:2]],
                      FadeIn(groups[0][2]))
            vo.wait_until("b")
            self.play(*[GrowFromEdge(b[0], DOWN) for b in groups[1][:2]], *[FadeIn(b[1:]) for b in groups[1][:2]],
                      FadeIn(groups[1][2]))
            vo.wait_until("c")
            self.play(*[GrowFromEdge(b[0], DOWN) for b in groups[2][:2]], *[FadeIn(b[1:]) for b in groups[2][:2]],
                      FadeIn(groups[2][2]), FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(tab))
            self.play(Indicate(tab.cells[2][2], color=HEAD), FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def time(self):
        head = label(r"Effects that change with time", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 28, 7], [-4, 7, 2], x_length=7.0, y_length=4.2, x_label=r"days since the user first saw the "
                 r"change", y_label=r"measured lift, \ \%", xticks=(7, 14, 21, 28),
                 yticks=(-4, -2, 0, 2, 4, 6)).move_to([-2.8, -0.35, 0])
        ax = g.ax
        days = np.linspace(0, 28, 57)
        nov = trace(ax, [(d, 1.0 + 5.0 * np.exp(-d / 4.0)) for d in days], HEAD, width=3.5)
        pri = trace(ax, [(d, 2.0 - 5.0 * np.exp(-d / 5.0)) for d in days], LAM, width=3.5)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(28, 0), color=GREY_C)
        nl = label(r"novelty", font_size=19, color=HEAD).next_to(ax.c2p(3, 4.0), RIGHT, buff=0.15)
        pl = label(r"primacy", font_size=19, color=LAM).next_to(ax.c2p(3, -2.0), RIGHT, buff=0.15)
        ill = note(r"illustrative", font_size=17).next_to(g, DOWN, buff=0.1).align_to(g, RIGHT)
        notes = VGroup(
            wrapped_label(r"\textbf{novelty}: \ users try the new thing because it is new; \ the lift fades", 4.4,
                          font_size=20, color=HEAD),
            wrapped_label(r"\textbf{primacy}: \ users trained on the old design stumble at first; \ the lift "
                          r"grows", 4.4, font_size=20, color=LAM),
            wrapped_label(r"look at the effect by days since first exposure, \ and at new users, \ who have no "
                          r"habits; \ run long enough for the curve to flatten", 4.4, font_size=20, color=YES),
            wrapped_label(r"and when users affect each other \ (a marketplace), \ the test itself is biased: \ the "
                          r"Frontier, \ Chapter 13", 4.4, font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.4, -0.2, 0])
        with self.voiceover(
            "A two-week test measures two weeks of behaviour. <bookmark mark='a'/> A new button gets clicked "
            "because it is new: the novelty effect, a lift that fades. <bookmark mark='b'/> The opposite is "
            "primacy: people used to the old design stumble at first. <bookmark mark='c'/> So plot the effect "
            "against days since each user first saw the change, look at new users, who have no habits, and run "
            "until the curve flattens. <bookmark mark='d'/> And when users affect each other, as buyers in a "
            "marketplace do, the test itself is biased; that is for the frontier chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), Create(zero), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(nov), FadeIn(nl), FadeIn(notes[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(pri), FadeIn(pl), FadeIn(notes[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def twyman(self):
        head = label(r"Twyman's law", font_size=36).to_edge(UP, buff=0.3)
        quote = label(r"\textit{``Any figure that looks interesting or different is usually wrong.''}",
                      font_size=28, color=HEAD).next_to(head, DOWN, buff=0.45)
        src = note(r"Tony Twyman, \ British audience researcher; \ popularized for experiments by Ron Kohavi",
                   font_size=18).next_to(quote, DOWN, buff=0.15)
        card = VGroup(RoundedRectangle(width=4.0, height=2.0, corner_radius=0.12, stroke_color=YES, fill_color=YES,
                                       fill_opacity=0.12),
                      label(r"revenue \ $+38\%$", font_size=40, color=YES))
        card[1].move_to(card[0])
        card.move_to([-3.8, -0.4, 0])
        ill = note(r"illustrative", font_size=17).next_to(card, DOWN, buff=0.1)
        checks = VGroup(*[label(t, font_size=21, color=WHITE) for t in (
            r"did the split come out as planned? \ \ ($\chi^2$)",
            r"did logging change with the treatment?",
            r"bots, \ crawlers, \ or one enormous customer?",
            r"does an A/A test on the same pipeline pass?",
            r"is it bigger than anything this product has ever seen?")]).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.28)
        checks.move_to([2.8, -0.4, 0])
        boxes = VGroup(*[Square(0.22, stroke_color=GREY_B).next_to(c, LEFT, buff=0.18) for c in checks])
        cross = Cross(card, stroke_color=NO, stroke_width=5)
        with self.voiceover(
            "The last pitfall is wanting to believe. <bookmark mark='a'/> Twyman's law, named after the British "
            "audience researcher Tony Twyman and made a rule of experimentation by Ron Kohavi: any figure that looks "
            "interesting or different is usually wrong. <bookmark mark='b'/> A test reports revenue up thirty-eight "
            "percent. <bookmark mark='c'/> Before celebrating, check the split, check whether logging changed, look "
            "for bots or one enormous customer, and run an A/A test through the same pipeline. "
            "<bookmark mark='d'/> Real improvements are usually small. A huge one is usually a bug."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(quote), FadeIn(src))
            vo.wait_until("b")
            self.play(FadeIn(card, scale=1.1), FadeIn(ill))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(b, c)) for b, c in zip(boxes, checks)], lag_ratio=0.4),
                      run_time=4)
            vo.wait_until("d")
            self.play(Create(cross))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, KERN, LAM, YES)
