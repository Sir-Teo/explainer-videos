from __future__ import annotations

import numpy as np

from videos.stats.stats48.common import *  # noqa: F403


class Entropy(VoiceoverScene):
    def construct(self):
        self.card()
        self.definitions()
        self.brackets()
        self.chart()
        self.examples()

    def card(self):
        card = chapter_card(3, r"Entropy and bracketing", r"Measuring a class by how many balls it takes to cover it", part=PART)
        with self.voiceover("Chapter three. Entropy and bracketing: measuring a class by how many balls it takes to cover it."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definitions(self):
        rows = [
            cmath(r"N(\varepsilon, \mathcal F, \|\cdot\|)", r"=", r"\text{the fewest } \varepsilon\text{-balls that cover } \mathcal F", font_size=32),
            cmath(r"N_{[\,]}(\varepsilon, \mathcal F, L_2(P))", r"=", r"\text{the fewest brackets } [l, u], \ \|u - l\| \le \varepsilon, \ \text{that cover } \mathcal F", font_size=28),
            cmath(r"l \le f \le u", r"\Rightarrow", r"P_n l - P l - \varepsilon \le P_n f - P f \le P_n u - P u + \varepsilon", font_size=30),
            cmath(r"N_{[\,]}(\varepsilon) < \infty \ \forall \varepsilon", r"\Rightarrow", r"\text{Glivenko--Cantelli}, \ \text{with no combinatorics}", font_size=30),
        ]
        rows[1][-1].set_color(CLASSC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"the covering number; \ its log: the entropy"), why(r"bracketing: \ balls with a floor and a ceiling"),
                why(r"sandwich $f$, \ then use the ordinary LLN"), why(r"Blum (1955), \ DeHardt (1971)")]
        with self.voiceover(
            "<bookmark mark='a'/> VC dimension counts patterns. A finer measure of size asks how many balls of radius "
            "epsilon it takes to cover the class in some norm. That is the covering number; its logarithm is the metric "
            "entropy, a name Kolmogorov chose deliberately. <bookmark mark='b'/> A variant uses brackets: pairs of "
            "functions, a floor l and a ceiling u, at most epsilon apart in L two of P, such that every function in the "
            "class lies between the floor and the ceiling of some bracket. <bookmark mark='c'/> Brackets turn a uniform "
            "statement into finitely many ordinary ones: a function sandwiched between l and u has its empirical gap "
            "sandwiched between theirs, up to epsilon. <bookmark mark='d'/> So finitely many brackets at every epsilon "
            "already make the class Glivenko–Cantelli, by the ordinary law of large numbers applied to the brackets."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def brackets(self):
        A = axes([0, 1], [0, 1.08], x_length=7.4, y_length=4.4, xlabel=r"$u = F(x)$", ylabel=r"$\mathbf 1\{x \le t\}$, \ $F(t) \in [t_{j-1}, t_j]$",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        knots = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
        j = 2
        lo = VGroup(Line(ax.c2p(0, 0.98), ax.c2p(knots[j], 0.98), color=EMPC, stroke_width=5), Line(ax.c2p(knots[j], 0.0), ax.c2p(1, 0.0), color=EMPC, stroke_width=5))
        hi = VGroup(Line(ax.c2p(0, 1.02), ax.c2p(knots[j + 1], 1.02), color=BADC, stroke_width=5), Line(ax.c2p(knots[j + 1], 0.04), ax.c2p(1, 0.04), color=BADC, stroke_width=5))
        f = VGroup(Line(ax.c2p(0, 1.0), ax.c2p(0.5, 1.0), color=CLASSC, stroke_width=3), Line(ax.c2p(0.5, 0.02), ax.c2p(1, 0.02), color=CLASSC, stroke_width=3))
        ticks = VGroup(*[DashedLine(ax.c2p(k, 0), ax.c2p(k, 1.05), color=GREY_D, stroke_width=1.5) for k in knots[1:-1]])
        shade = Rectangle(width=ax.c2p(knots[j + 1], 0)[0] - ax.c2p(knots[j], 0)[0], height=ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1],
                          fill_color=CLASSC, fill_opacity=0.15, stroke_width=0).move_to(ax.c2p((knots[j] + knots[j + 1]) / 2, 0.5))
        side = fit_rows(VGroup(
            label(r"cut $[0, 1]$ at $t_j$ with $P$-mass $\varepsilon^2$ each", font_size=22),
            label(r"blue floor: \ $\mathbf 1\{x \le t_{j-1}\}$", font_size=22, color=EMPC),
            label(r"red ceiling: \ $\mathbf 1\{x < t_j\}$", font_size=22, color=BADC),
            label(r"gold: \ any $t$ in between", font_size=22, color=CLASSC),
            label(r"$\|u - l\|_{L_2} = \varepsilon$: \ $N_{[\,]} = \lceil 1/\varepsilon^2 \rceil$", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The half-lines show how brackets work. Cut the line at points that split the probability "
            "into pieces of mass epsilon squared. <bookmark mark='b'/> The floor of a bracket is the indicator of the "
            "half-line up to the left cut, <bookmark mark='c'/> and its ceiling the indicator up to the right cut. <bookmark "
            "mark='d'/> Every half-line ending in between lies between them. <bookmark mark='e'/> The two differ only on a "
            "piece of probability epsilon squared, so they are epsilon apart in L two, and one over epsilon squared brackets "
            "cover the whole class. That is the proof of the Glivenko–Cantelli theorem in four lines."
        ) as vo:
            self.play(FadeIn(A), FadeIn(ticks), FadeIn(exact_tag(r"exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(shade))
            vo.wait_until("b")
            self.play(Create(lo), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(hi), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(f), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def chart(self):
        d = load("entropy")
        A = axes([0, 21], [0, 6.5], x_length=7.4, y_length=4.4, xlabel=r"$1/\varepsilon$", ylabel=r"$\log N(\varepsilon)$",
                 xticks=[0, 5, 10, 15, 20], yticks=[0, 2, 4, 6], center=[-2.5, 0.2, 0])
        ax = A.ax
        ie = 1 / np.asarray(d["eps"])
        il = 1 / np.asarray(d["eps_l"])
        ch = VGroup(polyline(ax, ie, d["hl_log"], EMPC, 4), *[Dot(ax.c2p(a, b), radius=0.08, color=EMPC) for a, b in zip(ie, d["hl_log"])])
        cl = VGroup(polyline(ax, il, d["lip_log"], BADC, 4), *[Dot(ax.c2p(a, b), radius=0.08, color=BADC) for a, b in zip(il, d["lip_log"])])
        u = np.linspace(2.4, 21, 100)
        ref = polyline(ax, u, np.log(u ** 2 / 2), GREY_B, 2)
        side = fit_rows(VGroup(
            label(r"greedy $\varepsilon$-nets, \ counted", font_size=22),
            label(r"blue: \ half-lines in $L_2$: \ $\log N \approx 2\log(1/\varepsilon)$", font_size=22, color=EMPC),
            label(r"red: \ 20,000 random 1-Lipschitz functions, \ sup norm", font_size=22, color=BADC),
            label(r"red grows like $1/\varepsilon$: \ a much bigger class", font_size=22, color=BADC),
            label(r"VC-like: \ $\log(1/\varepsilon)$; \ smooth: \ $(1/\varepsilon)^{d/\alpha}$", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> We can count nets directly, greedily: pick an uncovered function, remove everything "
            f"within epsilon of it, and repeat. <bookmark mark='b'/> For the half-lines in L two, the number of balls grows "
            f"like one over epsilon squared, so the entropy grows only like two log one over epsilon: at epsilon one "
            f"twentieth, {d['hl'][-1]} balls. <bookmark mark='c'/> For a sample of twenty thousand random one-Lipschitz "
            f"functions on the unit interval, in the supremum norm, <bookmark mark='d'/> the entropy grows like one over "
            f"epsilon itself, linearly on this chart: at epsilon point oh eight, {d['lip'][-1]} balls, and the true class "
            f"needs vastly more. <bookmark mark='e'/> These are the two regimes. VC-type classes have logarithmic entropy; "
            f"smoothness classes of functions of d variables with alpha derivatives have entropy one over epsilon to the d "
            f"over alpha."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"counted: \ greedy nets")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ch), Create(ref), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def examples(self):
        rows = [[r"class", r"$\log N_{[\,]}(\varepsilon, L_2)$", r"Donsker?"],
                [r"half-lines; \ a VC class of dimension $V$", r"$\asymp V \log(1/\varepsilon)$", r"yes"],
                [r"monotone functions into $[0, 1]$", r"$\asymp 1/\varepsilon$", r"yes"],
                [r"1-Lipschitz on $[0, 1]$", r"$\asymp 1/\varepsilon$", r"yes"],
                [r"$\alpha$-smooth on $[0, 1]^d$ \ (Hölder, \ Sobolev)", r"$\asymp (1/\varepsilon)^{d/\alpha}$", r"iff $\alpha > d/2$"],
                [r"convex sets in $\mathbb R^d$ \ (Bronshtein; \ Dudley)", r"$\asymp (1/\varepsilon)^{d-1}$", r"$d = 2$: yes; \ $d \ge 4$: no"]]
        tab = table_rows(rows, font_size=26, col_buff=0.7, row_buff=0.33, colors=[GREY_B, None, None, None, CLASSC, BADC])
        if tab.width > 12.6:
            tab.width = 12.6
        tab.move_to([0, 0.7, 0])
        foot = label(r"chapter 5's rule: \ Donsker when $\int_0^1 \sqrt{\log N_{[\,]}(\varepsilon)}\,d\varepsilon < \infty$, \ i.e. entropy $\ll 1/\varepsilon^2$", font_size=24, color=S.ACCENT).move_to([0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A small catalogue. VC classes have entropy V log one over epsilon. Monotone functions with "
            "values in the unit interval, and Lipschitz functions, have entropy of order one over epsilon; for Lipschitz functions "
            "the result goes back to Kolmogorov and Tikhomirov in 1959. Smooth functions of d variables with alpha derivatives have one over epsilon to "
            "the d over alpha. And the convex sets in d dimensions, with bracketing in L two, have one over epsilon to the "
            "d minus one. <bookmark mark='b'/> Chapter five will show that a class is Donsker, satisfying a uniform central "
            "limit theorem, when the root of the bracketing entropy is integrable at zero: when the entropy grows more slowly "
            "than one over epsilon squared. That is why smoothness must beat half the dimension, and why, as Dudley showed, "
            "the convex sets are Donsker in the plane but not in four or more dimensions."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()
