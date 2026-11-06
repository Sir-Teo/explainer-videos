from __future__ import annotations

import math

from videos.philosophy.philosophy16.common import *  # noqa: F403


def fmt_n(n: int) -> str:
    return f"{n:,}".replace(",", "{,}")


class Lindley(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Lindley's paradox", r"Can significance favour the null?", lit=(1939, 1957), part=PART)
        with self.voiceover("Chapter seven. Lindley's paradox."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.paradox()
        self.why()
        self.prior()
        self.bounds()
        self.bem()

    def paradox(self):
        d = load("lindley")["lindley"]
        hc = history_card(1957, r"Dennis Lindley", r"`A Statistical Paradox'", width=5.0, color=HIST).to_corner(
            UL, buff=0.3)
        setup = label(r"always $z = 2$: \ $p = " + f"{d['rows'][0]['p']:.4f}" + r"$, \ `significant'; \ $H_1$: "
                      r"$\mu \sim N(0, 1)$, \ prior odds 1:1", font_size=21, color=WHITE).next_to(hc, DOWN,
                                                                                               buff=0.3).set_x(0)
        hd = [r"n", r"p", r"B_{01}", r"P(H_0 \mid x)"]
        rows = [[MathTex(fmt_n(r["n"]), font_size=24), MathTex(f"{r['p']:.3f}", font_size=24, color=BAD),
                 MathTex(f"{r['bf01']:.2f}", font_size=24, color=NULLC if r["bf01"] > 1 else ALTC),
                 MathTex(f"{r['post_null']:.3f}", font_size=24, color=NULLC if r["post_null"] > 0.5 else ALTC)]
                for r in d["rows"]]
        grid = ValueGrid(hd, rows, col_w=[2.4, 1.6, 1.8, 2.2], cell_h=0.5, font_size=24).next_to(setup, DOWN, buff=0.35)
        foot = label(r"the same $p$, \ ever stronger evidence \textit{for} the null", font_size=24,
                     color=GOAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Dennis Lindley's paradox of 1957, anticipated by Jeffreys, shows how far the schools can disagree. "
            "<bookmark mark='a'/>Suppose every study reports the same test statistic, z equals two: p of point zero "
            "four five, significant at five percent. The alternative says the mean is drawn from a standard normal "
            "prior, and the two hypotheses start at even odds. <bookmark mark='b'/>With ten observations, the Bayes "
            "factor mildly favours the alternative. <bookmark mark='c'/>With a thousand, it favours the null by four "
            "to one. <bookmark mark='d'/>With a million, by more than a hundred to one, and the posterior probability "
            "of the null is ninety-nine percent. <bookmark mark='e'/>The p-value never changed. The evidence, by "
            "Bayes's lights, swung from against the null to overwhelmingly for it."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(setup), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*grid.cell[0])))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in (1, 2)], lag_ratio=0.4))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in (3, 4, 5)], lag_ratio=0.4))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def why(self):
        head = label(r"Why: \ who predicted the data better?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        n = 1000
        se = 1 / math.sqrt(n)
        xobs = 2 * se
        ax = Axes(x_range=[-0.25, 0.25, 0.1], y_range=[0, 14, 5], x_length=9.0, y_length=3.6, tips=False,
                  axis_config={"color": GREY_C, "include_ticks": False}).move_to([0, -0.4, 0])

        def npdf(x, s):
            return math.exp(-x * x / (2 * s * s)) / (s * math.sqrt(2 * math.pi))
        s1 = math.sqrt(1 + se * se)
        f0 = ax.plot(lambda x: npdf(x, se), x_range=[-0.25, 0.25], color=NULLC, stroke_width=4)
        # the H1 predictive density is nearly flat at this scale: scale it to be visible, and say so
        f1 = ax.plot(lambda x: 30 * npdf(x, s1), x_range=[-0.25, 0.25], color=ALTC, stroke_width=4)
        obs = DashedLine(ax.c2p(xobs, 0), ax.c2p(xobs, 13.5), color=GOAL, stroke_width=2)
        ol = label(r"observed $\bar x = 2/\sqrt{n}$", font_size=19, color=GOAL).next_to(obs, UP, buff=0.05).shift(
            RIGHT * 0.9)
        l0 = label(r"$H_0$: \ $\bar x \sim N(0, 1/n)$", font_size=20, color=NULLC).move_to(ax.c2p(0.16, 6.5))
        l1 = label(r"$H_1$: \ $\bar x \sim N(0, 1 + 1/n)$ \ (drawn $30\times$ taller)", font_size=20,
                   color=ALTC).move_to(ax.c2p(-0.13, 10.4))
        b = (npdf(xobs, se) / npdf(xobs, s1))
        txt = stack([(r"$n = 1{,}000$: \ the observed mean is only " + f"{xobs:.3f}", WHITE),
                     (r"$H_0$ gave it density " + f"{npdf(xobs, se):.1f}" + r"; \ $H_1$, \ spread thin over effects "
                      r"of every size, \ " + f"{npdf(xobs, s1):.2f}", WHITE),
                     (r"ratio: \ $B_{01} = " + f"{b:.1f}" + r"$", GOAL)], font_size=21).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Why does this happen? Compare how well each hypothesis predicted the data. <bookmark mark='a'/>With a "
            "thousand observations, z of two means the observed mean is tiny: point zero six. "
            "<bookmark mark='b'/>The null predicted means close to zero, so it gave this one a reasonable "
            "probability density. <bookmark mark='c'/>The alternative spread its predictions over effects of every "
            "size, large and small, so it gave this particular small effect very little; here it is drawn thirty "
            "times taller just to be visible. <bookmark mark='d'/>The ratio is the Bayes factor: about four to one "
            "for the null. The p-value asks only whether the data are surprising under the null. The Bayes factor "
            "asks whether they are more surprising under the alternative. With large samples, a fixed p threshold "
            "lets ever smaller effects count as discoveries."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax))
            vo.wait_until("a")
            self.play(Create(obs), FadeIn(ol), FadeIn(txt[0]))
            vo.wait_until("b")
            self.play(Create(f0), FadeIn(l0))
            vo.wait_until("c")
            self.play(Create(f1), FadeIn(l1), FadeIn(txt[1]))
            vo.wait_until("d")
            self.play(FadeIn(txt[2]))
        self.clear_scene()

    def prior(self):
        d = load("lindley")["prior"]
        head = label(r"The same data, \ different priors on the effect", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        sub = label(r"$z = 2$, \ $n = " + str(d["n"]) + r"$; \ $H_1$: \ $\mu \sim N(0, \tau^2)$", font_size=22,
                    color=GREY_A).next_to(head, DOWN, buff=0.2)
        rows = d["rows"]
        ax = Axes(x_range=[0, len(rows), 1], y_range=[-1, 2, 1], x_length=8.4, y_length=3.6, tips=False,
                  axis_config={"color": GREY_C, "include_ticks": False}).move_to([-1.4, -1.0, 0])
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(len(rows), 0), color=GREY_B, stroke_width=1.5)
        bars = VGroup()
        for i, r in enumerate(rows):
            v = math.log10(r["bf01"])
            top, bot = ax.c2p(i + 0.5, max(v, 0)), ax.c2p(i + 0.5, min(v, 0))
            b = Rectangle(width=0.55, height=max(top[1] - bot[1], 0.02), stroke_width=0,
                          fill_color=NULLC if v > 0 else ALTC, fill_opacity=0.85).move_to(
                [top[0], (top[1] + bot[1]) / 2, 0])
            t = label(rf"{r['tau']:g}", font_size=16, color=GREY_B).move_to(ax.c2p(i + 0.5, -1.15))
            bars.add(VGroup(b, t))
        yl = VGroup(*[label(t, font_size=16, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1) for t, v in
                      ((r"1:10", -1), (r"1:1", 0), (r"10:1", 1), (r"100:1", 2))])
        tl = label(r"prior width $\tau$", font_size=18, color=GREY_B).next_to(ax, DOWN, buff=0.45)
        bl = label(r"$B_{01}$", font_size=20, color=GREY_B).next_to(ax.y_axis, UP, buff=0.1)
        side = stack([(r"favours $H_1$ \ at most " + f"{1 / d['min_bf01_normal']:.1f}" + r" : 1", ALTC),
                      (r"favours $H_0$ \ up to " + f"{max(r['bf01'] for r in rows):.0f}" + r" : 1", NULLC),
                      (r"no prior at all can beat \ $e^{z^2/2} = " + f"{d['max_bf10']:.2f}" + r"$ \ for $H_1$", GOAL),
                      (r"Edwards, \ Lindman and Savage \ (1963)", HIST)], font_size=20, aligned_edge=LEFT).move_to(
            [4.9, -0.6, 0])
        with self.voiceover(
            "But the Bayes factor depends on the prior for the effect under the alternative. "
            "<bookmark mark='a'/>Keep z equal to two with a hundred observations, and vary the prior's width tau. "
            "<bookmark mark='b'/>A very narrow prior barely differs from the null, and the Bayes factor is near one. "
            "Moderate widths favour the alternative, but never by more than about two to one. Wide priors favour the "
            "null, up to sixty-eight to one. <bookmark mark='c'/>And no prior whatever, not even a point mass placed "
            "exactly at the observed effect, can favour the alternative by more than e to the z squared over two: "
            "seven point four to one. Ward Edwards, Harold Lindman and Leonard Savage proved this bound in 1963. A "
            "significant result at five percent is, at best, modest evidence."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(ax), Create(zero), FadeIn(yl), FadeIn(tl), FadeIn(bl))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(b[0]), FadeIn(b[1])) for b in bars], lag_ratio=0.12),
                      FadeIn(side[0]), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.clear_scene()

    def bounds(self):
        d = load("lindley")["sellke"]
        head = label(r"How much is a $p$-value worth?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        eq = MathTex(r"B_{01} \;\ge\; -e\, p \ln p \qquad (p < 1/e)", font_size=36, color=GOAL).next_to(head, DOWN,
                                                                                                       buff=0.35)
        src = label(r"Sellke, \ Bayarri and Berger \ (2001): \ a bound over a wide class of alternatives",
                    font_size=20, color=HIST).next_to(eq, DOWN, buff=0.15)
        hd = [r"p", r"\text{minimum } B_{01}", r"\text{best odds against } H_0"]
        rows = [[MathTex(f"{r['p']:g}", font_size=26), MathTex(f"{r['bf01_min']:.3f}", font_size=26),
                 MathTex(f"{1 / r['bf01_min']:.1f} : 1", font_size=26, color=ALTC)] for r in d]
        grid = ValueGrid(hd, rows, col_w=[1.8, 3.0, 4.0], cell_h=0.55, font_size=24).next_to(src, DOWN, buff=0.4)
        foot = stack([(r"$p = 0.05$ is worth at most 2.5 to 1; \ hence the proposal of $p < 0.005$ \ (Benjamin et al., "
                       r"\ 2018)", WHITE),
                      (r"particle physics asks for $5\sigma$: \ $p \approx 3 \times 10^{-7}$ \ (the Higgs, \ 2012)",
                       GREY_A)], font_size=21).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Thomas Sellke, Maria Bayarri and James Berger turned this into a rule of thumb. "
            "<bookmark mark='a'/>For p below one over e, the Bayes factor for the null is at least minus e times p "
            "times the log of p, over a wide class of reasonable alternatives. <bookmark mark='b'/>So p equal to "
            "point zero five is worth odds of at most two and a half to one against the null. Point zero one is "
            "worth at most eight to one; point zero zero one, about fifty to one. <bookmark mark='c'/>This is why "
            "seventy-two statisticians and scientists proposed in 2018 to call results significant only below point "
            "zero zero five. <bookmark mark='d'/>Particle physicists already ask for five sigma, a p-value near three "
            "in ten million, before announcing a discovery, as they did for the Higgs boson in 2012."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(src))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule),
                      LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(len(rows))], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def bem(self):
        head = label(r"Bem's precognition, \ re-analysed", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Bem \ (2011)", r"nine experiments, \ eight significant: \ people `feel the future'", FISH),
            (r"Wagenmakers et al.\ \ (2011)", r"default Bayes factors: \ most experiments give anecdotal evidence, "
                                              r"\ some favour the null", BAYC),
            (r"Rouder and Morey \ (2011)", r"pooled, \ the data do favour an effect: \ but how plausible was psi "
                                           r"beforehand?", BAYC),
            (r"the lesson", r"small $p$-values from many modest studies \ need not be strong evidence; \ and "
                            r"extraordinary claims need extraordinary prior odds to overcome", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.4, x_text=-2.4)
        with self.voiceover(
            "Lindley's lesson was tested on the most famous result of the replication crisis. "
            "<bookmark mark='a'/>In 2011 Daryl Bem reported nine experiments, eight of them significant, suggesting "
            "that people can sense future events. <bookmark mark='b'/>Eric-Jan Wagenmakers and colleagues re-analysed "
            "them with default Bayes factors, and found that most gave only anecdotal evidence, and some favoured "
            "the null. <bookmark mark='c'/>Jeffrey Rouder and Richard Morey pooled the studies and found that the "
            "data, taken together, did favour an effect, and then asked how plausible precognition was beforehand. "
            "<bookmark mark='d'/>Significant results from many modest studies need not be strong evidence; and a "
            "claim that contradicts physics starts with prior odds that no such evidence can overcome."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
