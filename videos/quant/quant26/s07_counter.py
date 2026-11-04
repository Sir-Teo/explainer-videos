from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import pit
from videos.quant.quant26.common import BAD, HURDLE, NOISE, PART, RULE, ask, comma, fit_right, house_lab, load


class Counter(VoiceoverScene):
    def construct(self):
        k, s = load("counter"), load("select")
        self.card()
        self.registry()
        self.byparts(k)
        self.hurdle(k)
        self.minbtl(s)
        self.caveat()
        self.question()

    def card(self):
        c = chapter_card(6, r"The trial counter and the hurdle", r"How many tries does a Sharpe ratio have to beat?",
                         lit=(2014,), part=PART)
        with self.voiceover("Chapter six. The trial counter: the number every backtest in this series has been keeping, "
                            "and the hurdle it implies."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def registry(self):
        card = house_lab(r"Registering a strategy", pit.register, "env = _read()", 6, width=9.6)
        card.to_edge(UP, buff=0.4)
        notes = VGroup(
            label(r"the hash of the code that produced it", font_size=20, color=RULE),
            label(r"its parameters, as run", font_size=20, color=RULE),
            label(r"how many configurations were tried to arrive at it", font_size=20, color=HURDLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(card, DOWN, buff=0.35)
        with self.voiceover(
            "Since Part one, every strategy the House has wanted to believe has been registered before its sealed "
            "years were opened. <bookmark mark='a'/> A registration records three things: a hash of the code that "
            "produced it, so it cannot be quietly edited afterwards; its parameters, as run; and the number of "
            "configurations that were tried to arrive at it. <bookmark mark='b'/> The third is the trial counter. It "
            "is written by the code that did the trying, so it regenerates when the code is rerun, and it can only go "
            "up."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(n_, shift=RIGHT * 0.2) for n_ in notes], lag_ratio=0.5))
            vo.wait_until("b")
            self.play(Indicate(notes[2], color=HURDLE))
        self.wait(0.4)
        self.clear_scene()

    def byparts(self, k):
        parts = {int(p): v for p, v in k["parts"].items()}
        ps = sorted(parts)
        g = axes([-0.6, len(ps) - 0.4], [0, 2.6], x_length=9.0, y_length=4.0, xlabel=r"part",
                 ylabel=r"$\log_{10}$ configurations registered", xticks=[], yticks=[0, 1, 2], font_size=13).to_edge(
            LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        grp = VGroup()
        for i, p in enumerate(ps):
            v = np.log10(parts[p] + 1)
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
            grp.add(VGroup(Rectangle(width=0.5, height=max(y1 - y0, 0.01), stroke_width=0, fill_color=QC.HOUSE,
                                     fill_opacity=0.85).move_to([ax.c2p(i, 0)[0], (y0 + y1) / 2, 0]),
                           MathTex(str(parts[p]), font_size=16).next_to(ax.c2p(i, v), UP, buff=0.05),
                           label(rf"{p}", font_size=13, color=GREY_A).next_to(ax.c2p(i, 0), DOWN, buff=0.1)))
        side = VGroup(MathTex(rf"\text{{before this part}}:\ {k['before']}", font_size=28, color=QC.HOUSE),
                      wrapped_label(r"configurations tried, by the part that registered them: Part 3's published "
                                    r"predictors, Part 6's industries, Part 7's volatility models, Part 24's ten classic "
                                    r"factors, Part 25's shrinkage grid", 3.2, 16, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Here is the count so far, part by part. <bookmark mark='a'/> Part three registered two hundred and "
            "twenty-two configurations, most of them published predictors. Part six, fifty-nine, most of them "
            "industries. Part seven eleven volatility models; Part twenty-four ten classic factors; Part twenty-five "
            "twenty-one points on its shrinkage grid. Three hundred and forty-six in all before this part. "
            "<bookmark mark='b'/> By its end, this part alone will add ten thousand."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in grp], lag_ratio=0.1), FadeIn(side), run_time=2.5)
            vo.wait_until("b")
            self.play(Indicate(side[0], color=QC.HOUSE))
        self.wait(0.4)
        self.clear_scene()

    def hurdle(self, k):
        grid, h = np.log10(np.asarray(k["grid"])), np.asarray(k["hurdle"])
        g = axes([0, 5], [0, 1.6], x_length=7.6, y_length=4.2, xlabel=r"$N$, configurations tried",
                 ylabel=rf"the Sharpe ratio the best of $N$ reaches by luck ({k['T_years']:.0f} years of daily data)",
                 xticks=[0, 1, 2, 3, 4, 5], yticks=[0, 0.5, 1.0, 1.5], log_x=True, font_size=14).to_edge(LEFT, buff=0.5)
        g.shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, grid, h, HURDLE, stroke_width=3)
        nb, na = k["before"], k["before"] + 10_000
        d1 = VGroup(Dot(ax.c2p(np.log10(nb), k["at_before"]), color=QC.HOUSE, radius=0.08),
                    MathTex(rf"{nb}:\ {k['at_before']:.2f}", font_size=22, color=QC.HOUSE).next_to(
                        ax.c2p(np.log10(nb), k["at_before"]), UL, buff=0.1))
        d2 = VGroup(Dot(ax.c2p(np.log10(na), k["at_after"]), color=BAD, radius=0.08),
                    MathTex(rf"{comma(na)}:\ {k['at_after']:.2f}", font_size=22, color=BAD).next_to(
                        ax.c2p(np.log10(na), k["at_after"]), UL, buff=0.1))
        side = wrapped_label(r"if every configuration were independent and none had any edge: the expected best Sharpe "
                             r"ratio, annualised. The hurdle grows like $\sqrt{2 \ln N}$: slowly, and forever", 3.4, 15,
                             GREY_A).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "What the count implies. <bookmark mark='a'/> With ten years of daily data, the best of N configurations "
            "with no edge at all is expected to show this Sharpe ratio. <bookmark mark='b'/> At the House's three "
            "hundred and forty-six, it is about point nine three: any House strategy chosen from all of them should be "
            "compared with that, not with zero. <bookmark mark='c'/> After this part's ten thousand rules, the "
            "hurdle is one point two. It grows like the square root of two log N, slowly and forever. The cure for "
            "a high hurdle is not to stop counting. It is to try fewer things, and to try them on data that has "
            "not been seen."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(line), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(d1))
            vo.wait_until("c")
            self.play(FadeIn(d2))
        self.wait(0.4)
        self.clear_scene()

    def minbtl(self, s):
        rows = [cmath(r"\mathbb{E}\big[\max_N \widehat{SR}_{\text{annual}}\big]", r"\approx", r"\frac{1}{\sqrt{T_{\text{years}}}}"
                      r"\Big[(1 - \gamma)\,\Phi^{-1}\!\big(1 - \tfrac1N\big) + \gamma\,\Phi^{-1}\!\big(1 - \tfrac{1}{Ne}\big)\Big]",
                      font_size=32, colors={r"\mathbb{E}\big[\max_N \widehat{SR}_{\text{annual}}\big]": HURDLE}),
                cmath(r"\text{MinBTL}", r"\approx", r"\frac{\big[(1 - \gamma)\,\Phi^{-1}(1 - \frac1N) + \gamma\,\Phi^{-1}(1 - "
                      r"\frac{1}{Ne})\big]^2}{SR^2}", font_size=34, colors={r"\text{MinBTL}": BAD})]
        whys = [why(r"zero-skill configurations: an annual Sharpe estimate from $T$ years has variance $1/T$, so the "
                    r"hurdle falls with the square root of the backtest's length"),
                why(r"set the hurdle equal to a target Sharpe ratio and solve for $T$: the minimum backtest length, in years "
                    r"(Bailey, Borwein, Lopez de Prado and Zhu 2014)")]
        step = ladder(self, rows, whys, keep=2, top=3.2, x=-0.5, buff=0.35, edge=6.9)
        grid = np.log10(np.asarray(s["grid"]))
        g = axes([0, 4], [0, 20], x_length=6.4, y_length=2.8, xlabel=r"$N$", ylabel=r"years", xticks=[0, 1, 2, 3, 4],
                 yticks=[0, 5, 10, 15, 20], log_x=True, font_size=13).to_edge(DOWN, buff=0.35).shift(LEFT * 2.6)
        ax = g.ax
        ls = VGroup()
        for sr, col in (("1.0", BAD), ("2.0", HURDLE)):
            y = np.asarray(s["btl"][sr])
            k = (grid <= 4) & (y <= 20)
            ls.add(curve(ax, grid[k], y[k], col, stroke_width=3))
        dot = Dot(ax.c2p(np.log10(45), s["btl_45"]), color=BAD, radius=0.08)
        side = VGroup(
            MathTex(rf"N = {s['n_5y_sr1']}\ \text{{in 5 years}}", font_size=26, color=BAD),
            legend([(BAD, r"to rule out a Sharpe ratio of 1"), (HURDLE, r"to rule out 2")], font_size=15),
            wrapped_label(r"five years of data allow about 45 independent tries before a Sharpe ratio of one is what luck "
                          r"alone would show", 4.4, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(g, RIGHT, buff=0.6)
        with self.voiceover(
            "The same formula, read the other way. <bookmark mark='a'/> For zero-skill configurations, an annual "
            "Sharpe ratio estimated from T years has variance one over T, so the hurdle falls with the square root of "
            "the backtest's length. <bookmark mark='b'/> Set the hurdle equal to the Sharpe ratio you hope to "
            "detect, and solve for T: the minimum backtest length. <bookmark mark='c'/> Bailey, Borwein, Lopez de Prado "
            "and Zhu put it bluntly in 2014: with five years of data, no more than about forty-five independent "
            "configurations should be tried before a Sharpe ratio of one is just what luck would show. Most parameter "
            "sweeps try more than that before lunch."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            self.play(FadeIn(g), Create(ls), FadeIn(dot), FadeIn(side), run_time=2.5)
        self.wait(0.5)
        self.clear_scene()

    def caveat(self):
        cards = VGroup(
            desk_question(r"trials are not independent", r"two moving-average rules that differ by one day make almost the "
                          r"same trades: they are nearly one trial, not two. The formula's $N$ is the number of independent "
                          r"tries, smaller than the count", width=12.2, font_size=19),
            desk_question(r"so the count is an upper bound", r"and its effective size is estimated from how correlated "
                          r"the tries were, and from how much their Sharpe ratios varied: chapter 8 does both for ten "
                          r"thousand rules", width=12.2, font_size=19),
            desk_question(r"and a lower bound", r"the count holds only what was registered. The ideas abandoned before "
                          r"any code was written, and the colleague's notebook, are tries the counter never saw",
                          width=12.2, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Two caveats pull in opposite directions. <bookmark mark='a'/> Trials are not independent: two "
            "moving-average rules that differ by one day make almost the same trades, so they are nearly one trial, "
            "not two. <bookmark mark='b'/> In that sense the count overstates N, and the effective number has to be "
            "estimated from how correlated the tries were; chapter eight does it for ten thousand rules. "
            "<bookmark mark='c'/> But the count also understates N, because it holds only what was registered: the "
            "ideas abandoned before any code was written, and the colleague's notebook, are tries the counter never saw."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"a team has tried about 2,000 correlated variations of one idea, and estimates they amount to 100 "
                r"independent tries. Their best has a Sharpe ratio of 1.0 over eight years. Clear the hurdle?".replace(
                    "2,000", "2{,}000"))
        with self.voiceover(
            "Pause and predict. A team has tried about two thousand correlated variations of one idea, which they "
            "estimate amount to a hundred independent tries. Their best has a Sharpe ratio of one over eight years. "
            "Does it clear the hurdle?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
