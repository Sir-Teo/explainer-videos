from __future__ import annotations

import numpy as np

from videos.psychology.psych9.common import *  # noqa: F403


class Loci(VoiceoverScene):
    def construct(self):
        self.card()
        self.quarrel()
        self.sum()
        self.variance()
        self.regression()

    def card(self):
        card = chapter_card(2, r"From peas to bell curves", r"How can discrete genes make a continuous trait?",
                            lit={1918: r"Fisher"}, part=PART, scale=("molecule", "person"), marr=("how",))
        with self.voiceover(
            "Chapter two. From peas to bell curves."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _bars(self, k, p, center, width, height, color):
        c = np.asarray(center, float)
        top = float(p.max())
        w = width / len(k)
        g = VGroup(Line(c + LEFT * width / 2 + DOWN * height / 2, c + RIGHT * width / 2 + DOWN * height / 2, color=GREY_B,
                        stroke_width=2))
        for i, pi in enumerate(p):
            h = max(height * float(pi) / top, 0.004)
            g.add(Rectangle(width=w * 0.86, height=h, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to(
                c + np.array([-width / 2 + (i + 0.5) * w, -height / 2 + h / 2, 0])))
        return g

    def quarrel(self):
        head = heading(r"1900: \ a quarrel about inheritance")
        peas = self._bars(np.arange(2), np.array([0.25, 0.75]), [-4.3, 0.5, 0], 2.6, 2.6, GENE)
        pl = VGroup(label(r"short", font_size=29, color=GENE), label(r"tall", font_size=29, color=GENE)).arrange(RIGHT, buff=0.75)
        pl.next_to(peas, DOWN, buff=0.12)
        pt = label(r"Mendel's peas: \ two kinds", font_size=31, color=GENE).next_to(peas, UP, buff=0.2)
        x = np.linspace(-3, 3, 200)
        bell = VMobject(color=DATA, stroke_width=4).set_points_as_corners(
            [np.array([0.9 + 0.55 * xi, -0.8 + 2.6 * np.exp(-xi * xi / 2), 0]) for xi in x])
        base = Line([-0.8, -0.8, 0], [2.6, -0.8, 0], color=GREY_B, stroke_width=2)
        bt = label(r"people's heights: \ every value", font_size=31, color=DATA).move_to([0.9, pt.get_center()[1], 0])
        rows = rows_of([
            (r"Mendel's factors, our genes, come in discrete versions", GENE),
            (r"but height, or a test score, varies continuously", DATA),
            (r"two schools argue for nearly twenty years", WHITE),
            (r"1918: \ Ronald Fisher shows that both are right", P.ACCENT),
        ], 4.0, 30, 0.32).move_to([5.0, -0.3, 0])
        keep_in_frame(rows)
        src = historical_tag(archive.FISHER_1918.cite)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Galton's question ran straight into a puzzle. In 1900 biologists rediscovered Gregor Mendel's "
            "experiments on peas. Mendel's factors, which we now call genes, come in discrete versions. A "
            "pea plant is tall or it's short, with nothing in between. <bookmark mark='a'/> But the traits "
            "Galton cared about aren't like that. Height, or a score on a test, takes every value, in a "
            "bell curve. <bookmark mark='b'/> For nearly twenty years two schools argued. One said "
            "inheritance is Mendel's discrete factors. The other said it's continuous, and measured it "
            "with Galton's correlations. <bookmark mark='c'/> In 1918 a young statistician, Ronald Fisher, "
            "showed that both were right."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(peas), FadeIn(pl), FadeIn(pt), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(bell), FadeIn(base), FadeIn(bt), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def sum(self):
        d = load("loci")
        head = heading(r"Add up enough genes, \ and the steps disappear")
        panels = VGroup()
        for i, L in enumerate((1, 2, 5, 50)):
            x = -5.1 + 3.4 * i
            bars = self._bars(d[f"k_{L}"], d[f"p_{L}"], [x, 0.3, 0], 2.9, 2.6, GENE)
            name = label(rf"{L} gene" + (r"s" if L > 1 else r""), font_size=32, color=GENE).next_to(bars, UP, buff=0.2)
            kinds = label(rf"{2 * L + 1} kinds of people", font_size=28, color=GREY_A).next_to(bars, DOWN, buff=0.15)
            panels.add(VGroup(bars, name, kinds))
        end = rows_of([
            (r"Each gene is still one of Mendel's factors: \ a plus or a minus, two copies each.", WHITE),
            (r"Fisher then worked out how alike relatives must be if this is true. \ That makes the subject computable.",
             P.ACCENT),
        ], 12.4, 31, 0.2).to_edge(DOWN, buff=0.55)
        tag = psyche_tag(r"computed: equal effects, both versions equally common")
        with self.voiceover(
            "Suppose a trait is influenced by one gene, which comes in two versions, a plus and a minus. "
            "Everyone carries two copies, so there are three kinds of people: no pluses, one, or two. "
            "<bookmark mark='a'/> Now two genes whose effects add. Five kinds. <bookmark mark='b'/> Five "
            "genes: eleven kinds. <bookmark mark='c'/> Fifty genes, and the steps are too fine to see. It's "
            "a bell curve, built entirely out of Mendel's discrete factors. <bookmark mark='d'/> Add the "
            "effects of the environment, which blur the steps further, and you have the distributions we "
            "actually measure. Fisher's paper went further. It worked out how alike relatives should be "
            "if this picture is true. And that's what makes the whole subject computable."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(panels[0]))
            for mark_, pn in zip("abc", panels[1:]):
                vo.wait_until(mark_)
                self.play(FadeIn(pn, shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(end[0]), FadeIn(end[1]))
        self.clear_scene()

    def variance(self):
        head = heading(r"The bookkeeping: \ a score in three parts")
        parts = [(r"A", r"the added-up effects of a person's genes", GENE),
                 (r"C", r"what children in one family share: \ the home, the street, the school", HOME),
                 (r"E", r"everything else: \ what differs even between children in one home, \ luck, \ measurement error",
                  OWN)]
        eq = VGroup(label(r"score", font_size=44), label(r"$=$", font_size=44), label(r"A", font_size=50, color=GENE),
                    label(r"$+$", font_size=44), label(r"C", font_size=50, color=HOME), label(r"$+$", font_size=44),
                    label(r"E", font_size=50, color=OWN)).arrange(RIGHT, buff=0.35).move_to([0, 2.2, 0])
        rows = VGroup(*[VGroup(label(k, font_size=38, color=c), wrapped_label(t, 10.4, 30, WHITE)).arrange(RIGHT, buff=0.45)
                        for k, t, c in parts]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.45, 0])
        bar = share_bar([0.5, 0.2, 0.3], [GENE, HOME, OWN], width=8.0, height=0.6, names=[r"A", r"C", r"E"], font_size=30)
        bar.move_to([-1.6, -1.75, 0])
        bl = label(r"the variance of the scores, shared out", font_size=28, color=GREY_A).next_to(bar, UP, buff=0.12)
        h2 = VGroup(label(r"heritability", font_size=32, color=GENE),
                    label(r"$h^2$ \ $=$ \ A's share", font_size=34, color=GENE)).arrange(
            DOWN, buff=0.15).move_to([4.9, -1.75, 0])
        end = wrapped_label(r"It describes how the people in a population differ from one another. \ It is not a fact "
                            r"about any one of them.", 12.4, 31, P.ACCENT).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here's the bookkeeping Fisher introduced. A person's score is a sum of three parts. "
            "<bookmark mark='a'/> A: the added-up effects of their genes. C, for common: everything in the "
            "environment that children in the same family share. And E: everything else, including luck "
            "and the error of the measurement. <bookmark mark='b'/> If the parts are independent, their "
            "variances add. So the variance of the scores can be shared out among the three. "
            "<bookmark mark='c'/> The share that belongs to A is called the heritability, written h "
            "squared. <bookmark mark='d'/> Notice what kind of thing it is. It's a property of a "
            "population: of how people differ from one another. It isn't a property of a person. Keep "
            "that in mind until chapter six."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.8), run_time=6.0)
            vo.wait_until("b")
            self.play(FadeIn(bar), FadeIn(bl))
            vo.wait_until("c")
            self.play(FadeIn(h2), Indicate(bar.parts[0], color=WHITE, scale_factor=1.05))
            vo.wait_until("d")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def regression(self):
        d = load("loci")
        head = heading(r"Galton's regression, \ and what its slope means")
        A = axes([-2.6, 2.6], [-2.6, 2.6], x_length=5.2, y_length=4.6, xticks=[-2, 0, 2], yticks=[-2, 0, 2],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"the parents' average", ylabel=r"their child",
                 center=[-3.7, -0.5, 0])
        ax = A.ax
        pts = scatter(ax, d["mid"], d["child"], OWN, radius=0.025, opacity=0.5)
        same = DashedLine(ax.c2p(-2.5, -2.5), ax.c2p(2.5, 2.5), color=GREY_B, stroke_width=2)
        sl = label(r"child $=$ parents", font_size=26, color=GREY_B).next_to(ax.c2p(2.5, 2.5), RIGHT, buff=0.12)
        xs = np.array([-2.5, 2.5])
        fit = Line(ax.c2p(xs[0], d["slope"] * xs[0] + d["intercept"]), ax.c2p(xs[1], d["slope"] * xs[1] + d["intercept"]),
                   color=GENE, stroke_width=5)
        rows = rows_of([
            (r"children of tall parents are tall, \ but less so: \ they fall back toward the average", WHITE),
            (rf"if parents pass on only genes, \ the slope is the heritability: \ ${d['slope']:.2f}$ here, \ and we "
             rf"planted ${d['h2']:.1f}$", GENE),
            (rf"parents 1 unit above average: \ children ${d['tall_child']:.2f}$ above, on average", GENE),
            (r"in real families parents pass on a home as well, \ and the slope mixes the two", BAD),
        ], 5.7, 30, 0.3).move_to([3.85, -0.4, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"simulated: families in which only genes are passed on")
        with self.voiceover(
            "One prediction of the model was already in Galton's notebooks. Measure both parents, average "
            "them, and measure their grown-up children. <bookmark mark='a'/> The children of tall parents "
            "are tall, but less so than their parents. They fall back toward the average. Galton called it "
            "regression, and that's where the word in statistics comes from. <bookmark mark='b'/> Under "
            "Fisher's model the slope of this line has a meaning. If parents pass on their genes and "
            f"nothing else, the slope is the heritability. Here it's {d['slope']:.2f}, and we planted "
            f"{d['h2']:.1f}. <bookmark mark='c'/> Parents one unit above the average have children who "
            f"are, on average, {d['tall_child']:.2f} above. <bookmark mark='d'/> But in real families "
            "parents pass on a home as well, and then the slope mixes the two. To pull them apart we "
            "need a sharper tool."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(pts, lag_ratio=0.001), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(same), FadeIn(sl), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()
