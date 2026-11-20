from __future__ import annotations

from videos.economics.econ24.common import *  # noqa: F403

CASES = (("benefit up", r"benefit $b$: \ 0.4 $\to$ 0.5", BENEFIT),
         ("productivity up", r"productivity $p$: \ $+5\%$", MATCH),
         ("separations up", r"separations $s$: \ $\times 1.5$", SEP),
         ("bargaining up", r"worker's share $\beta$: \ 0.5 $\to$ 0.6", WAGE))


class Bargaining(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Nash bargaining and the split of the surplus", r"What sets the wage when there is no market "
             r"price, \ and what moves unemployment?", "Chapter seven. Nash bargaining and the split of the surplus.",
             lit={1950: r"Nash", 1982: r"Rubinstein", 1986: r"Binmore, Rubinstein and Wolinsky"},
             scale=("firm", "market"), horizon=("a month",))
        self.surplus()
        self.wage()
        self.statics()
        self.shift()

    def surplus(self):
        rows = VGroup(
            label(r"once a worker and a firm have met, \ walking away costs both of them another search",
                  font_size=23, color=GREY_A),
            MathTex(r"S \;=\; \underbrace{(\mathcal{W} - \mathcal{U})}_{\text{worker's gain}} \;+\; "
                    r"\underbrace{(\mathcal{J} - \mathcal{V})}_{\text{firm's gain}}", font_size=44, color=WHITE),
            label(r"a \emph{surplus}: \ no market price divides it; \ any wage between the two walk-away points works",
                  font_size=22, color=E.ACCENT),
            MathTex(r"\max_w \;(\mathcal{W} - \mathcal{U})^{\beta}\,(\mathcal{J} - \mathcal{V})^{1-\beta}"
                    r"\quad\Longrightarrow\quad \mathcal{W} - \mathcal{U} = \beta\, S", font_size=42, color=WAGE),
            label(r"Nash's solution, \ 1950: \ the worker gets a share $\beta$ of the surplus; \ Rubinstein's "
                  r"alternating offers \ (Part 11) \ give the same split", font_size=21, color=GREY_B),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        with self.voiceover(
            "In the Beveridge picture there is no auctioneer. So what sets the wage? <bookmark mark='a'/> Once a "
            "worker and a firm have found each other, both are better off together than apart: walking away means "
            "searching again. <bookmark mark='b'/> The match creates a surplus, the worker's gain over staying "
            "unemployed plus the firm's gain over an empty vacancy. <bookmark mark='c'/> Any wage that leaves both "
            "gains positive would be accepted. Nothing in the market picks one. <bookmark mark='d'/> The model "
            "uses John Nash's bargaining solution: the wage that maximizes the product of the two gains, weighted "
            "by beta and one minus beta. The worker ends up with a share beta of the surplus. "
            "<bookmark mark='e'/> Ariel Rubinstein's game of alternating offers, from Part eleven, gives the same "
            "split when offers come quickly, with beta reflecting how patient each side is."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def wage(self):
        d = load("dmp")
        st = d["steady"]
        rows = VGroup(
            MathTex(r"w \;=\; (1-\beta)\,b \;+\; \beta\,(p + c\,\theta)", font_size=54, color=WAGE),
            label(r"a weighted average of the worker's fallback and what the worker is worth to the firm",
                  font_size=23, color=GREY_A),
            label(r"$c\,\theta$: \ in a tight market, \ the firm saves the expected cost of finding someone else, \ "
                  r"and the worker gets a share", font_size=22, color=TIGHT),
            MathTex(rf"w^* = (0.5)(0.4) + (0.5)\big(1 + (0.3)({st['theta']:.2f})\big) = {st['w']:.3f}",
                    font_size=40, color=E.ACCENT),
            label(r"put it into job creation: \ one equation in $\theta$ alone", font_size=22, color=GREY_B),
            MathTex(r"\frac{(r+s)\,c}{q(\theta)} \;+\; \beta\,c\,\theta \;=\; (1-\beta)\,(p - b)", font_size=44,
                    color=JOB),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        with self.voiceover(
            "Work out the share, and the wage comes out simply. <bookmark mark='a'/> It is a weighted average: one "
            "minus beta times the benefit the worker would get while unemployed, plus beta times what the worker "
            "is worth to the firm. <bookmark mark='b'/> What the worker is worth includes output, p, and something "
            "more: c times theta. In a tight market, a firm that lets this worker go faces a long, costly search for "
            "another, and the worker captures part of that saving. That is why the wage curve slopes up. "
            "<bookmark mark='c'/> On the Island, half of four-tenths, plus half of one plus 0.3 times "
            f"{st['theta']:.2f}: {st['w']:.3f}. <bookmark mark='d'/> Substitute the wage into job creation and the "
            "whole model collapses to one equation in tightness. <bookmark mark='e'/> On the left, the expected "
            "cost of a hire plus the worker's share of the search cost saved; on the right, the firm's share of "
            "the gap between output and the benefit. Every comparative static in this part comes from this line."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def statics(self):
        d = load("dmp")
        base = d["steady"]["u"]
        ax = plane([-0.6, 4.6], [0, 6], center=LEFT * 1.9 + DOWN * 0.3, x_length=8.4, y_length=4.8,
                   xticks=[], yticks=[0, 1, 2, 3, 4, 5, 6], ylabel=r"steady-state unemployment, \ \%",
                   yfmt=lambda v: f"{v:.0f}", font_size=16)
        base_line = seg(ax, -0.6, 100 * base, 4.6, 100 * base, color=WORKER, width=2, dashed=True)
        base_l = label(rf"the Island: \ {pc(base)}", font_size=18, color=WORKER).next_to(
            ax.ax.c2p(-0.6, 100 * base), UP, buff=0.1).shift(RIGHT * 1.0)
        bars, names, vals = VGroup(), VGroup(), VGroup()
        for k, (key, name, c) in enumerate(CASES):
            u = d["statics"][key]["steady"]["u"]
            x = 0.4 + 1.25 * k
            lo, hi = ax.ax.c2p(x, 0), ax.ax.c2p(x, 100 * u)
            bars.add(Rectangle(width=0.85, height=hi[1] - lo[1], fill_color=c, fill_opacity=0.8,
                               stroke_width=0).move_to((lo + hi) / 2))
            vals.add(label(pc(u), font_size=20, color=c).next_to(bars[-1], UP, buff=0.08))
            names.add(label(name, font_size=15, color=c).next_to(lo, DOWN, buff=0.15))
        side = VGroup(
            label(r"benefits raise the fallback \\ and the wage: \ fewer vacancies", font_size=19, color=BENEFIT),
            label(r"productivity raises output \\ more than the wage", font_size=19, color=MATCH),
            label(r"more separations: \\ a leakier tub", font_size=19, color=SEP),
            label(r"a bigger worker share: \\ less left for firms", font_size=19, color=WAGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            f"Now move the dials, one at a time, from the Island's {100 * base:.1f} percent. "
            "<bookmark mark='a'/> Raise the benefit from four-tenths to a half: the worker's fallback improves, the "
            "wage rises, firms open fewer vacancies, and unemployment rises to "
            f"{100 * d['statics']['benefit up']['steady']['u']:.1f} percent. <bookmark mark='b'/> Raise "
            "productivity by five percent: output rises by more than the wage, so firms open more vacancies, and "
            f"unemployment falls to {100 * d['statics']['productivity up']['steady']['u']:.1f}. "
            "<bookmark mark='c'/> Make jobs half again as likely to end: the tub leaks faster, and unemployment "
            f"rises to {100 * d['statics']['separations up']['steady']['u']:.1f}, even though tightness hardly "
            "moves. <bookmark mark='d'/> Give workers a bigger share of the surplus: each hire is worth less to "
            f"firms, and unemployment rises to {100 * d['statics']['bargaining up']['steady']['u']:.1f}. Notice which "
            "change moves unemployment least: productivity, the shock that most theories of the business cycle rely on."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(base_line), FadeIn(base_l), FadeIn(tag), run_time=0.8)
            for mk, k in zip("abcd", range(4)):
                vo.wait_until(mk)
                self.play(GrowFromEdge(bars[k], DOWN), FadeIn(vals[k]), FadeIn(names[k]), FadeIn(side[k]))
        self.clear_scene()

    def shift(self):
        d = load("dmp")
        st, cv = d["steady"], d["curves"]
        bu = d["statics"]["benefit up"]
        ax = plane([0, 4], [0.85, 1.05], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.2, y_length=5.0,
                   xticks=[0, 1, 2, 3, 4], yticks=[0.85, 0.9, 0.95, 1.0, 1.05], xlabel=r"tightness $\theta$",
                   ylabel=r"wage $w$", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}", font_size=16)
        jc = path(ax, cv["theta"], cv["jc"], color=JOB, width=4, yr=(0.85, 1.05))
        wc = path(ax, cv["theta"], cv["wc"], color=WAGE, width=4, yr=(0.85, 1.05))
        wc2 = path(ax, bu["curves"]["theta"], bu["curves"]["wc"], color=BENEFIT, width=4, yr=(0.85, 1.05))
        e0 = dot(ax, st["theta"], st["w"], color=E.ACCENT, r=0.09)
        e1 = dot(ax, bu["steady"]["theta"], bu["steady"]["w"], color=BENEFIT, r=0.09)
        side = VGroup(
            label(r"a higher benefit \\ shifts the wage curve up", font_size=21, color=BENEFIT),
            label(rf"tightness: \ {st['theta']:.2f} $\to$ {bu['steady']['theta']:.2f}", font_size=21, color=TIGHT),
            label(rf"wage: \ {st['w']:.3f} $\to$ {bu['steady']['w']:.3f}", font_size=21, color=WAGE),
            label(r"job creation is nearly flat: \\ a small change in the wage \\ moves tightness a lot", font_size=20,
                  color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is the first of those in the picture. <bookmark mark='a'/> A higher benefit shifts the wage curve "
            f"up. <bookmark mark='b'/> The crossing slides left: tightness falls from {st['theta']:.2f} to "
            f"{bu['steady']['theta']:.2f}. <bookmark mark='c'/> And the wage barely rises, from {st['w']:.3f} to "
            f"{bu['steady']['w']:.3f}. <bookmark mark='d'/> Because job creation is nearly flat, a tiny change in the "
            "wage moves tightness a lot. That flatness is what the profit margin, p minus w, controls, and it will "
            "decide the puzzle in chapter nine."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(jc), Create(wc), FadeIn(e0), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(wc2), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(GrowFromCenter(e1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
