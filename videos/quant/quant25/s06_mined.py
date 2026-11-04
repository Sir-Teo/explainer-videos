from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant25.common import BAD, GOOD, HURDLE, NOISE, PART, SDF, TRUE, ask, fit_right, illustration, load


class Mined(VoiceoverScene):
    def construct(self):
        self.card()
        self.experiment()
        self.chance()
        self.result()
        self.risk()
        self.yanzheng()
        self.lesson()

    def card(self):
        c = chapter_card(5, r"Data-mined against peer-reviewed", r"Does a theory make a signal more likely to last?",
                         lit=(2022,), part=PART)
        with self.voiceover("Chapter five. A test of the whole enterprise: do published, theorised predictors do better "
                            "than ones found by brute force?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def experiment(self):
        rows = [cmath(r"x_{ab}", r"=", r"\frac{\text{accounting item}_a}{\text{accounting item}_b}\ \ \text{or}\ \ "
                      r"\Delta\,\frac{a}{b},\quad 29{,}000\ \text{signals}", font_size=36, colors={r"x_{ab}": NOISE}),
                cmath(r"\text{benchmark}_j", r"=", r"\{x : t(x) > 2\ \text{in predictor } j\text{'s own sample}\}",
                      font_size=36, colors={r"\text{benchmark}_j": HURDLE})]
        whys = [why(r"Chen, Lopez-Lira and Zimmermann: form every ratio, and growth of a ratio, from pairs of accounting "
                    r"items: about twenty-nine thousand signals with no theory at all"),
                why(r"for each published predictor, the mined signals that would have passed $t > 2$ in the same years: "
                    r"what a data miner with no ideas would have published instead. Then compare what each does after "
                    r"its sample ends")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Andrew Chen, Alejandro Lopez-Lira and Tom Zimmermann ran the experiment. Take pairs of accounting items "
            "and form every ratio, and every change in a ratio: about twenty-nine thousand signals, with no idea behind "
            "any of them. <bookmark mark='a'/> For each published predictor, find the mined signals that would have "
            "passed a t of two in the same years: what a data miner with no theory would have published instead. "
            "Then compare what each does after its sample ends."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def chance(self):
        rows = [cmath(r"\Pr(|t| > 2 \mid H_0)", r"\approx", r"4.6\%\ \Rightarrow\ 29{,}000 \times 0.046 \approx 1{,}320", font_size=38,
                      colors={r"\Pr(|t| > 2 \mid H_0)": NOISE}),
                cmath(r"\Pr(|t| > 3 \mid H_0)", r"\approx", r"0.27\%\ \Rightarrow\ \approx 78", font_size=38,
                      colors={r"\Pr(|t| > 3 \mid H_0)": HURDLE})]
        whys = [why(r"if none of the 29,000 mined signals had a true premium, and they were independent, about thirteen "
                    r"hundred would still clear $|t| > 2$ in any given sample"),
                why(r"and about eighty would clear three. Mining finds false positives by the hundred: the experiment's "
                    r"question is whether its winners do any worse out of sample than the journals' winners")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "First, what chance alone would give. <bookmark mark='a'/> If none of the twenty-nine thousand signals had "
            "any premium, about four and a half percent would still clear a t of two in any sample: some thirteen "
            "hundred false positives. <bookmark mark='b'/> About eighty would clear three. So the miner's winners "
            "surely include many duds. The interesting question is whether they do any worse, out of sample, than the "
            "journals' winners."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def result(self):
        g = axes([-0.6, 1.6], [0, 0.7], x_length=5.6, y_length=4.2, xlabel=r"", ylabel=r"share of the in-sample return kept",
                 xticks=[], yticks=[0, 0.2, 0.4, 0.6], font_size=13).to_edge(LEFT, buff=1.0).shift(DOWN * 0.2)
        ax = g.ax
        vals = [(r"peer-reviewed", 0.53, SDF), (r"data-mined", 0.51, NOISE)]
        grp = VGroup()
        for i, (nm, v, col) in enumerate(vals):
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
            grp.add(VGroup(Rectangle(width=0.8, height=y1 - y0, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                [ax.c2p(i, 0)[0], (y0 + y1) / 2, 0]), MathTex(f"\\approx {100 * v:.0f}\\%", font_size=24).next_to(
                ax.c2p(i, v), UP, buff=0.08), label(nm, font_size=16, color=GREY_A).next_to(ax.c2p(i, 0), DOWN, buff=0.15)))
        side = VGroup(
            wrapped_label(r"about half of the in-sample predictability survives out of sample in both groups (as reported "
                          r"in their working paper; figures vary slightly by version)", 4.6, 17, GREY_A),
            wrapped_label(r"and the data miner gets there first: investment, issuance and accrual themes appear among "
                          r"the mined signals decades before they were published", 4.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The answer is uncomfortable. <bookmark mark='a'/> About half of the in-sample predictability survives "
            "out of sample, and it is about the same half for the peer-reviewed predictors and for the mined ones. "
            "<bookmark mark='b'/> And the miner gets there first: themes like investment, share issuance and accruals "
            "appear among the mined signals decades before papers explained them. On this evidence, peer review "
            "selects signals about as well as brute force with a hurdle of two."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in grp], lag_ratio=0.4), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
        self.add(illustration(r"Chen, Lopez-Lira and Zimmermann, 'Does peer-reviewed research help predict stock returns?'"))
        self.wait(0.4)
        self.clear_scene()

    def risk(self):
        cards = VGroup(
            desk_question(r"risk stories did not help", r"predictors whose papers offered a risk-based or equilibrium "
                          r"explanation did not hold up better out of sample, and in some comparisons did worse", width=12.0,
                          font_size=20),
            desk_question(r"why that is not a paradox", r"a mispricing that was real decays as it is traded away; a 'risk "
                          r"premium' that was really a mispricing decays too. Labels are cheap; out-of-sample returns are "
                          r"not", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "A second result. <bookmark mark='a'/> Predictors whose papers explained them as compensation for risk did "
            "not hold up better than the others, and in some comparisons did worse. <bookmark mark='b'/> That is not a "
            "paradox. A real mispricing decays as it is traded away, and so does a mispricing that was labelled a risk "
            "premium. The label is cheap; out-of-sample returns are not. Part twenty-three's rule, that every premium "
            "must state its reason, still stands: the reason is how the House knows what to stress, not proof that the "
            "premium will last."
        ) as vo:
            for i, mk in enumerate(("a", "b")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def yanzheng(self):
        rows = [cmath(r"\#\{x : |t(x)| > 3\}", r"\gg", r"\mathbb{E}_{H_0}[\,\#\{x : |t(x)| > 3\}\,]", font_size=40,
                      colors={r"\#\{x : |t(x)| > 3\}": TRUE})]
        whys = [why(r"Yan and Zheng (2017) mined about 18{,}000 fundamental signals and bootstrapped the null: far more "
                    r"cleared high hurdles than chance allows. Many accounting signals carry real information, which is "
                    r"why a data miner and a theorist find the same things")]
        step = ladder(self, rows, whys, keep=1, top=2.4, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "Why does mining work at all? Xuemin Yan and Lingling Zheng mined about eighteen thousand fundamental "
            "signals and bootstrapped what chance alone would produce. Far more signals cleared high hurdles than "
            "chance allows. Accounting data really do carry information about future returns, so a careful data miner "
            "and a careful theorist tend to find the same things. Data mining is not the problem. Data mining without "
            "a count of the tries is. With the count, a mined signal can be judged like any other."
        ) as vo:
            step(0)
        self.wait(0.4)
        self.clear_scene()

    def lesson(self):
        cards = VGroup(
            desk_question(r"for the research desk", r"a mined signal, honestly counted and tested out of sample, is "
                          r"evidence of the same quality as a published one", width=12.0, font_size=20),
            desk_question(r"the trial counter", r"what separates them is the count: the miner knows it tried 29{,}000; "
                          r"a paper rarely says how many it tried", width=12.0, font_size=20),
            desk_question(r"Part 29", r"the House's own alpha miners, genetic, reinforcement-learning and LLM, will run "
                          r"the counter into the millions, and be deflated accordingly", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "For the research desk. <bookmark mark='a'/> A mined signal, honestly counted and tested out of sample, is "
            "evidence of the same quality as a published one. <bookmark mark='b'/> What separates them is the count: "
            "the miner knows it tried twenty-nine thousand, and a paper rarely says how many versions it tried. "
            "<bookmark mark='c'/> Part twenty-nine builds the House's own alpha miners, and they will run the trial "
            "counter into the millions."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"a colleague mined 10,000 ratios and found one with $t = 4.5$ in 1980--2000 and $t = 2.4$ in 2001--2020. "
                r"Is it a discovery? What hurdle should each period face?")
        with self.voiceover("A colleague mined ten thousand ratios and found one with a t-statistic of four and a half in "
                            "1980 to 2000, and two point four in 2001 to 2020. Is it a discovery? What hurdle should each "
                            "period face?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
