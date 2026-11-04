from __future__ import annotations

import numpy as np

from videos.stats.stats3.common import *  # noqa: F403

LS, MLE = S.RESID, S.LIK


class Tails(VoiceoverScene, TreeMixin):
    def construct(self):
        self.card()
        self.pareto()
        self.zipf()
        self.pareto_rule()
        self.fitting()

    def card(self):
        card = chapter_card(10, r"Heavy tails", r"Power laws, and how not to fit them", lit=(), part=PART)
        with self.voiceover("Chapter ten. Heavy tails."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def pareto(self):
        dfn = definition_card(r"Pareto (power-law) tail", r"$P(X > x) = (x_{\min} / x)^{\alpha}$ \ for $x \ge x_{\min}$: "
                              r"\ the tail falls like a power, \ not exponentially", color=CONT, width=6.4,
                              font_size=24).move_to([-3.2, 2.2, 0])
        A = axes([0, 3], [-6, 0.2], x_length=6.0, y_length=4.0, xlabel=r"$\log_{10} x$", ylabel=r"$\log_{10} P(X > x)$",
                 xticks=[0, 1, 2, 3], yticks=[-6, -4, -2, 0], center=[-3.0, -1.4, 0])
        ax = A.ax
        lx = np.linspace(0, 3, 200)
        par = curve(ax, lx, -2 * lx, MLE, 3)
        ex = curve(ax, lx, np.clip(np.log10(np.exp(-(10 ** lx - 1) / 2)), -6, 0), GREY_A, 3)
        leg = legend([(MLE, r"Pareto, $\alpha = 2$: \ a straight line"), (GREY_A, r"exponential: \ falls off a cliff")],
                     font_size=22).move_to([3.4, 0.6, 0])
        facts = VGroup(label(r"moments of order $\ge \alpha$ are infinite \ (Part 1's incomes, $\alpha \approx 2$)",
                             font_size=22, color=GREY_A),
                       label(r"$\log X$ is exponential: \ chapter 7's arrow", font_size=22, color=GREY_A))
        facts.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, -1.2, 0])
        for f_ in facts:
            if f_.width > 6.6:
                f_.width = 6.6
        with self.voiceover(
            "Part 1 met heavy tails in the World's incomes. Here's the distribution behind them. "
            "<bookmark mark='a'/> A Pareto tail: the chance of exceeding x falls like a power of x, not "
            "exponentially. <bookmark mark='b'/> On log–log axes a power law is a straight line with slope minus "
            "alpha, while an exponential tail falls off a cliff. <bookmark mark='c'/> Moments of order alpha and "
            "above are infinite, which is why the World's incomes, with alpha near two, have an unstable variance. "
            "And the logarithm of a Pareto variable is exponential: the arrow we drew in chapter seven."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(dfn))
            vo.wait_until("b")
            self.play(FadeIn(A), Create(par), Create(ex), FadeIn(leg))
            vo.wait_until("c")
            self.play(FadeIn(facts))
        self.clear_scene()

    def zipf(self):
        d = load("tails")
        pops, ranks = np.asarray(d["pops"]), np.asarray(d["ranks"])
        A = axes([0, 2.4], [2.5, 5.5], x_length=7.0, y_length=4.4, xlabel=r"$\log_{10}$ rank", ylabel=r"$\log_{10}$ population",
                 xticks=[0, 1, 2], yticks=[3, 4, 5], center=[-2.4, -0.4, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(np.log10(r), np.log10(p)), radius=0.04, color=S.WORLD) for r, p in zip(ranks, pops)])
        fit = Line(ax.c2p(0, np.log10(pops[0])), ax.c2p(np.log10(150), np.log10(pops[0]) + d["slope_rank"] * np.log10(150)),
                   color=S.ACCENT, stroke_width=3)
        lab = MathTex(rf"\text{{slope}} \approx {d['slope_rank']:.2f}", font_size=30, color=S.ACCENT).move_to([4.2, 1.8, 0])
        hc = label(r"Zipf's law for cities: \ Auerbach (1913), Zipf (1949)", font_size=24, color=GREY_A).move_to([4.2, 0.9, 0])
        honest = label(r"the World was \emph{built} with Zipf weights \ (Part 1): \ here we only read them back",
                       font_size=22, color=GREY_B).move_to([4.2, 0.0, 0])
        for t in (hc, honest):
            if t.width > 5.6:
                t.width = 5.6
        tag = simulated_tag(r"simulated: the World's 200 towns")
        with self.voiceover(
            "A power law also shows up as Zipf's law. <bookmark mark='a'/> Rank the World's two hundred towns by "
            "population and plot log population against log rank. <bookmark mark='b'/> The points fall near a line "
            f"with slope about {d['slope_rank']:.2f}: the second-largest town has about half the population of the "
            "largest, the tenth about a tenth. Felix Auerbach noticed this for German cities in 1913, and George "
            "Zipf for cities and words in 1949. <bookmark mark='c'/> In the World it's no discovery: we built the "
            "towns with Zipf weights in Part 1, and we're only reading them back."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dt) for dt in dots], lag_ratio=0.005), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(lab), FadeIn(hc))
            vo.wait_until("c")
            self.play(FadeIn(honest))
        self.clear_scene()

    def pareto_rule(self):
        d = load("tails")
        qs = np.asarray(d["qs"])
        A = axes([0, 1], [0, 1], x_length=5.0, y_length=5.0, xlabel=r"top share of people", ylabel=r"share of income",
                 xticks=[0, 0.2, 0.5, 1], yticks=[0, 0.5, 0.8, 1], center=[-3.6, -0.4, 0])
        ax = A.ax
        cols = {"1.16": S.RESID, "2.0": S.ACCENT, "3.0": S.LIK}
        cvs = VGroup(*[curve(ax, qs, np.asarray(d["lorenz_par"][a]), c, 3) for a, c in cols.items()])
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=GREY_D, stroke_width=1.5)
        p80 = Dot(ax.c2p(0.2, 0.2 ** (1 - 1 / 1.16)), radius=0.08, color=S.RESID)
        f = MathTex(r"\text{share of the top } q", r"=", r"q^{\,1 - 1/\alpha}", font_size=32).move_to([3.4, 2.6, 0])
        f[2].set_color(EXACT)
        leg = legend([(S.RESID, r"$\alpha = 1.16$: \ the 80/20 rule"), (S.ACCENT, r"$\alpha = 2$"),
                      (S.LIK, r"$\alpha = 3$")], font_size=22).move_to([3.4, 1.2, 0])
        sh = d["shares"]
        world = VGroup(MathTex(rf"\text{{World: top 1\%}}\ {100 * sh['0.01']:.1f}\%", font_size=26, color=S.WORLD),
                       MathTex(rf"\text{{top 10\%}}\ {100 * sh['0.1']:.1f}\%,\ \ \text{{top 20\%}}\ {100 * sh['0.2']:.1f}\%",
                               font_size=26, color=S.WORLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.4, -0.6, 0])
        nt = label(r"80/20 needs a very heavy tail; \ the World's incomes are far less concentrated", font_size=22,
                   color=GREY_B).move_to([3.4, -1.8, 0])
        if nt.width > 6.0:
            nt.width = 6.0
        tag = simulated_tag()
        with self.voiceover(
            "Pareto's own observation was about concentration. <bookmark mark='a'/> For a Pareto tail with exponent "
            "alpha, the richest fraction q of people hold a share q to the one minus one over alpha of the total. "
            "<bookmark mark='b'/> With alpha about one point one six, the top twenty percent hold eighty percent: "
            "the famous eighty–twenty rule. Heavier tails, smaller alpha, concentrate more. <bookmark mark='c'/> "
            f"In the World, the top twenty percent of adults earn {100 * sh['0.2']:.0f} percent of all income, and "
            f"the top one percent {100 * sh['0.01']:.1f}. Far from eighty–twenty: most of the World's incomes come "
            "from its log-normal body, and only a thin slice from the Pareto tail."
        ) as vo:
            self.play(FadeIn(A), Create(diag), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in cvs], lag_ratio=0.3), FadeIn(leg), FadeIn(p80), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(world), FadeIn(nt))
        self.clear_scene()

    def fitting(self):
        d = load("tails")
        mid, h = np.asarray(d["ex_mid"]), np.asarray(d["ex_h"])
        A = axes([0, 3], [-7, 0.5], x_length=5.4, y_length=3.6, xlabel=r"$\log_{10} x$", ylabel=r"$\log_{10}$ density",
                 xticks=[0, 1, 2, 3], yticks=[-6, -4, -2, 0], center=[-3.6, 0.3, 0])
        ax = A.ax
        lm, lh = np.log10(mid), np.log10(h)
        pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=GREY_A) for a, b in zip(lm, lh) if -7 < b < 0.5])
        slope, icpt = np.polyfit(lm, lh, 1)
        ls_line = Line(ax.c2p(0, icpt), ax.c2p(3, icpt + 3 * slope), color=LS, stroke_width=3)
        tl = label(rf"one sample of {d['n']}, \ density $\propto x^{{-\alpha}}$, \ $\alpha = {d['alpha']}$", font_size=22, color=GREY_B).next_to(A, UP, buff=0.1)
        B = axes([1.6, 3.0], [0, 7], x_length=5.6, y_length=3.0, xlabel=r"estimated $\alpha$ \ (400 samples)",
                 xticks=[1.8, 2.2, 2.5, 2.8], center=[3.6, -1.8, 0])
        B.ax.y_axis.set_opacity(0)
        ed = np.linspace(1.6, 3.0, 57)
        hls = hist_bars(B.ax, ed, np.histogram(np.asarray(d["ls"]), ed)[0] / (400 * np.diff(ed)), color=LS, opacity=0.7)
        hml = hist_bars(B.ax, ed, np.histogram(np.asarray(d["mle"]), ed)[0] / (400 * np.diff(ed)), color=MLE, opacity=0.7)
        tline = Line(B.ax.c2p(2.5, 0), B.ax.c2p(2.5, 7), color=S.TRUTH, stroke_width=3)
        leg = VGroup(MathTex(rf"\text{{log--log least squares: }} {d['ls_mean']:.2f} \pm {d['ls_sd']:.2f}", font_size=24,
                             color=LS),
                     MathTex(rf"\text{{maximum likelihood: }} {d['mle_mean']:.2f} \pm {d['mle_sd']:.2f}", font_size=24,
                             color=MLE),
                     MathTex(r"\hat\alpha = 1 + n \Big/ \sum_i \log(x_i / x_{\min})", font_size=26, color=MLE))
        leg.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.6, 2.2, 0])
        hc = note(r"Clauset, Shalizi \& Newman (2009), \emph{SIAM Review}: \ many published power laws do not survive "
                  r"a proper test").to_edge(DOWN, buff=0.25)
        if hc.width > 13:
            hc.width = 13
        tag = note(r"simulated").to_corner(DL, buff=0.3).shift(UP * 0.4)
        with self.voiceover(
            "Power laws are easy to claim and hard to establish. <bookmark mark='a'/> The tempting method: draw a "
            "histogram on log–log axes and fit a straight line by least squares. Here's one simulated sample of five "
            "hundred from a power law whose density falls like x to the minus two and a half; in this convention, "
            "the tail exponent of the card above is one less. <bookmark mark='b'/> Repeat that four hundred times. "
            f"The least-squares slopes, red, average {d['ls_mean']:.2f}: biased, and noisy. <bookmark mark='c'/> The "
            f"maximum likelihood estimate, green, a closed formula, averages {d['mle_mean']:.2f}, with half the "
            "spread. <bookmark mark='d'/> Aaron Clauset, Cosma Shalizi and Mark Newman showed in 2009 that the "
            "log–log method is systematically misleading, and that many published power laws, tested properly, "
            "were no better than a log-normal. A straight line on a log–log plot is a hypothesis, not a proof."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(pts), FadeIn(tl), FadeIn(tag))
            self.play(Create(ls_line))
            vo.wait_until("b")
            self.play(FadeIn(B), Create(tline), FadeIn(hls), FadeIn(leg[0]))
            vo.wait_until("c")
            self.play(FadeIn(hml), FadeIn(leg[1:]))
            vo.wait_until("d")
            self.play(FadeIn(hc))
        self.clear_scene()
