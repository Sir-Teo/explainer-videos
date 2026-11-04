from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import BAD, GOOD, GP_C, HURDLE, PART, RAND_C, RL_C, COMB, comma, load


class Counter(VoiceoverScene):
    def construct(self):
        c = load("counter")
        e = load("envelope")
        self.card()
        self.history(c)
        self.sources(c)
        self.hurdle(c, e)
        self.correlated(c, e)
        self.question()

    def card(self):
        c = chapter_card(8, r"The counter explodes", r"What does a search over thousands of formulas do to the bar a "
                         r"result must clear?", part=PART)
        with self.voiceover("Chapter eight. Since Part twenty-six the series has kept a trial counter: every "
                            "configuration tried on the way to a registered strategy. Machines that search thousands of "
                            "formulas make it run. What does that do to the bar a result must clear?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def history(self, c):
        parts = np.array(c["parts"])
        cnt = np.array(c["count"], float)
        top = float(np.ceil(cnt[-1] / 5000) * 5000)
        g = axes([0.5, parts[-1] + 0.5], [0, top], x_length=9.6, y_length=4.4, xlabel=r"part", ylabel=r"the trial counter",
                 xticks=[1, 10, 20, 26, 29], yticks=[0, top / 2, top], font_size=15,
                 yfmt=lambda v: f"{v:,.0f}".replace(",", "{,}")).move_to(LEFT * 0.4 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.22, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                  fill_color=(HURDLE if p == PART else QC.HOUSE), fill_opacity=0.85).move_to(
            ax.c2p(p, 0), aligned_edge=DOWN) for p, v in zip(parts, cnt)])
        i26 = int(np.flatnonzero(parts == 26)[0])
        t26 = label(rf"Part 26: {comma(cnt[i26] - cnt[i26 - 1])} trading rules", font_size=17, color=QC.HOUSE).next_to(
            bars[i26], UP, buff=0.15).shift(LEFT * 1.4)
        t29 = MathTex(comma(cnt[-1]), font_size=26, color=HURDLE).next_to(bars[-1], UP, buff=0.12)
        with self.voiceover(
            "The counter, part by part. <bookmark mark='a'/> For twenty-five parts it crept up: a few dozen "
            f"configurations at a time, to {comma(cnt[i26 - 1]).replace('{,}', ',')} by Part twenty-five. Part twenty-six "
            "added the ten thousand technical trading rules of its data-snooping study. <bookmark mark='b'/> This part "
            f"adds {comma(cnt[-1] - cnt[-2]).replace('{,}', ',')} more, and the counter stands at "
            f"{comma(cnt[-1]).replace('{,}', ',')}. More than half of every trial in the series so far was made in this "
            "one part."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[:-1]], lag_ratio=0.05), FadeIn(t26))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[-1], DOWN), FadeIn(t29))
        self.wait(0.4)
        self.clear_scene()

    def sources(self, c):
        s = c["by_source"]
        tot = sum(s.values())
        items = [(r"random formulas, Chapter 3", s["random"], RAND_C),
                 (r"distinct trees evaluated by genetic programming, Chapter 4", s["gp"], GP_C),
                 (r"distinct formulas written by the RL generator, Chapter 5", s["rl"], RL_C),
                 (r"combinations of the top alphas, Chapter 7", s["combinations"], COMB)]
        rows = VGroup()
        for t, v, col in items:
            rows.add(VGroup(label(t, font_size=20, color=col), MathTex(comma(v), font_size=28, color=col)))
        for j, r_ in enumerate(rows):
            r_[0].move_to([-1.6, 1.6 - 0.8 * j, 0]).align_to(np.array([-6.0, 0, 0]), LEFT)
            r_[1].move_to([4.8, 1.6 - 0.8 * j, 0])
        line = Line([-6.0, -1.7, 0], [5.6, -1.7, 0], color=GREY_C, stroke_width=1.5)
        total = VGroup(label(r"this part's trials", font_size=22), MathTex(comma(tot), font_size=32, color=HURDLE))
        total[0].move_to([-1.6, -2.2, 0]).align_to(np.array([-6.0, 0, 0]), LEFT)
        total[1].move_to([4.8, -2.2, 0])
        foot = note(r"the agents of Chapter 6 were not run here; on a real desk every loop of theirs would be counted too",
                    font_size=15, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Where they came from. <bookmark mark='a'/> Ten thousand random formulas. The distinct trees that evolution "
            "evaluated across three runs. The distinct formulas the learned generator wrote, though most of its fifteen "
            "hundred attempts were repeats. And the handful of combinations we compared. <bookmark mark='b'/> "
            f"{comma(tot).replace('{,}', ',')} in all. A trial is any configuration whose result could have changed what "
            "we registered, whatever the algorithm called it: a draw, an individual, an episode."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(total), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def hurdle(self, c, e):
        N = sum(c["by_source"].values())
        T = 3.0
        h = math.sqrt(2 * math.log(N)) / math.sqrt(T)
        rows = [cmath(r"\widehat{SR}_i", r"\approx", r"SR_i + \frac{\varepsilon_i}{\sqrt T},\qquad \varepsilon_i \sim N(0, 1)",
                      font_size=32, colors={r"\widehat{SR}_i": HURDLE}),
                cmath(r"\max_{i \le N}\widehat{SR}_i", r"\approx", r"\frac{\sqrt{2\ln N}}{\sqrt T}\quad"
                      r"\text{if every } SR_i = 0", font_size=32, colors={r"\max_{i \le N}\widehat{SR}_i": BAD}),
                cmath(rf"N = {comma(N)},\ T = 3", r"\to", rf"{math.sqrt(2 * math.log(N)):.2f}/\sqrt3 = {h:.2f}", font_size=32),
                cmath(r"\text{the combination}", r":", rf"\widehat{{SR}} = {e['sr_res']:.2f}\ \text{{on 2018--2020}}",
                      font_size=32, colors={r"\text{the combination}": COMB})]
        whys = [why(r"an annualised Sharpe ratio estimated from $T$ years has a standard error of about $1/\sqrt T$"),
                why(r"the best of $N$ independent noise strategies (Part 26's expected maximum)"),
                why(r"this part's trials, and the three research years"),
                why(r"the mined combination's Sharpe ratio on its own research years, before costs")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        verdict = label(r"judged against independent trials, the in-sample result would not clear the bar", font_size=22,
                        color=BAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Part twenty-six's arithmetic. <bookmark mark='a'/> An annual Sharpe ratio measured over T years carries "
            "noise of about one over root T. <bookmark mark='b'/> So if all N strategies were worthless, the best would "
            "still show the square root of two log N over root T. <bookmark mark='c'/> With this part's "
            f"{comma(N).replace('{,}', ',')} trials and three research years, that is {h:.2f}. <bookmark mark='d'/> Our "
            f"mined combination earned {e['sr_res']:.2f} on its research years. Judged this way, it would not clear the "
            "bar: an in-sample number from a search this size proves nothing on its own."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.play(FadeIn(verdict))
        self.wait(0.5)
        self.clear_scene()

    def correlated(self, c, e):
        cards = VGroup(
            desk_question(r"the bar assumes independent trials", r"ten thousand cousins of three ideas are not ten thousand "
                          r"independent tries: the effective count is far smaller, and the bar with it. Estimating that "
                          r"count is hard: L\'opez de Prado and Lewis (2019) cluster the trials first", width=12.4, font_size=19),
            desk_question(r"so the counter is an upper bound on the damage", r"it is the number a sceptic may charge you "
                          r"with; arguing it down needs evidence, such as the correlation of the trials", width=12.4,
                          font_size=19),
            desk_question(r"the clean test is data the search never saw", r"one registered strategy, one sealed envelope: "
                          r"Chapter 13 opens it", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three qualifications. <bookmark mark='a'/> The bar assumes independent trials, and ours are anything but: "
            "ten thousand cousins of three ideas. The effective number of trials is far smaller, and so is the bar, but "
            "estimating it is hard. <bookmark mark='b'/> So the counter is an upper bound on the damage: the number a "
            "sceptic may charge you with, until you show evidence that your trials were correlated. <bookmark mark='c'/> "
            "And the clean test is data the search never saw: one registered strategy, one sealed envelope. Chapter "
            "thirteen opens it."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a lab evaluates a million formulas on two years of data. What annual Sharpe ratio does the best "
                       r"pure-noise formula show?")
        with self.voiceover(
            "Pause and predict. A lab evaluates a million formulas on two years of data. What annual Sharpe ratio does "
            "the best pure-noise formula show?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
