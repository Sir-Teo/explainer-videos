from __future__ import annotations

from videos.stats.stats57.common import *  # noqa: F403


class Online(VoiceoverScene):
    def construct(self):
        self.card()
        self.aci()
        self.aci_chart()
        self.proof()
        self.aci_worked()
        self.dtaci()
        self.beyond()

    def card(self):
        card = chapter_card(6, r"Online and adversarial", r"Coverage with no probability model at all", lit=(2021,), part=PART)
        with self.voiceover("Chapter six. Online and adversarial coverage: guarantees with no probability model at all."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def aci(self):
        rows = [
            cmath(r"\text{at each time } t", r":", r"\text{predict } C_t \text{ at level } 1 - \alpha_t, \ \text{then see } Y_t", font_size=34),
            cmath(r"\mathrm{err}_t", r"=", r"1\{Y_t \notin C_t\}", font_size=38),
            cmath(r"\alpha_{t+1}", r"=", r"\alpha_t + \gamma\,(\alpha - \mathrm{err}_t): \ \text{miss} \Rightarrow \text{widen; \ cover} \Rightarrow \text{narrow}", font_size=32),
            cmath(r"\text{guarantee}", r":", r"\Big|\frac1T\textstyle\sum_{t \le T}\mathrm{err}_t - \alpha\Big| \le \frac{\max(\alpha_1, 1 - \alpha_1) + \gamma}{\gamma T}", font_size=32),
        ]
        rows[2][-1].set_color(WEIGHTC)
        rows[3][-1].set_color(COVC)
        whys = [why(r"any base method"), why(r"a miss indicator"), why(r"Gibbs \& Cand\`es (2021)"), why(r"for every sequence")]
        with self.voiceover(
            "<bookmark mark='a'/> Part thirty-four showed adaptive conformal inference at work; here is its guarantee. At each "
            "time, predict a set at level one minus alpha t, then see the outcome. <bookmark mark='b'/> Record whether it was "
            "missed. <bookmark mark='c'/> Isaac Gibbs and Candès update the working level by gamma times alpha minus the miss: "
            "after a miss, widen; after a hit, narrow slightly. <bookmark mark='d'/> Then the long-run miss rate is within a "
            "constant over gamma T of alpha, for every sequence of data whatsoever, adversarial included."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def aci_chart(self):
        d = load("aci")
        t = np.asarray(d["t"])
        A = axes([t[0], t[-1]], [0.5, 1.02], x_length=7.4, y_length=4.4, xlabel=r"time \ (noise SD 1, \ then 2.5 from $t = 1{,}000$)",
                 ylabel=r"coverage, \ rolling 100", xticks=[500, 1000, 1500, 2000], yticks=[0.5, 0.75, 0.9, 1.0], center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = [MISSC, WEIGHTC, COVC]
        lines = [polyline(ax, t, np.clip(d[str(g)]["roll"], 0.5, 1.0), c, 3.5) for g, c in zip(d["gammas"], cols)]
        nom = DashedLine(ax.c2p(t[0], 0.9), ax.c2p(t[-1], 0.9), color=GREY_B, stroke_width=2)
        cp = DashedLine(ax.c2p(1000, 0.5), ax.c2p(1000, 1.02), color=GREY_C, stroke_width=2)
        g0, g1, g2 = (d[str(g)] for g in d["gammas"])
        side = fit_rows(VGroup(
            label(r"the drifting series again; \ 300 past scores, \ level $1 - \alpha_t$", font_size=22),
            label(rf"$\gamma = 0$: \ plain split, \ {100 * g0['after']:.0f}\% after the jump", font_size=22, color=MISSC),
            label(rf"$\gamma = 0.005$: \ {100 * g1['after']:.0f}\% after; \ misses {100 * g1['miss']:.1f}\% overall", font_size=22, color=WEIGHTC),
            label(rf"$\gamma = 0.02$: \ {100 * g2['after']:.0f}\% after; \ misses {100 * g2['miss']:.1f}\% overall", font_size=22, color=COVC),
            label(r"larger $\gamma$: \ faster recovery, \ jumpier sets", font_size=22, color=TESTPT),
        ), 4.6, 0.4, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Here it is on chapter five's drifting series, with three hundred past scores and a working "
            f"level one minus alpha t. <bookmark mark='b'/> With gamma zero, this is plain split conformal on a moving window: "
            f"in the three hundred steps after the jump it covers {100 * g0['after']:.0f} percent. <bookmark mark='c'/> With "
            f"gamma one in two hundred, the misses push the level up and coverage recovers to {100 * g1['after']:.0f} percent; "
            f"the overall miss rate is {100 * g1['miss']:.1f} percent. <bookmark mark='d'/> With gamma two in a hundred, "
            f"{100 * g2['after']:.0f} percent after the jump, and {100 * g2['miss']:.1f} percent misses overall. <bookmark "
            f"mark='e'/> Larger gamma recovers faster, and pays with sets that jump around."
        ) as vo:
            self.play(FadeIn(A), FadeIn(nom), FadeIn(cp), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(Create(lines[k]), FadeIn(side[k + 1]), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"\text{sum the update}", r":", r"\alpha_{T+1} - \alpha_1 = \gamma\textstyle\sum_{t \le T}(\alpha - \mathrm{err}_t)", font_size=34),
            cmath(r"\alpha_t \in [-\gamma, 1 + \gamma]", r":", r"\alpha_t < 0: \text{ no miss; \ } \alpha_t > 1: \text{ a miss}", font_size=36),
            cmath(r"\Rightarrow", r"\;", r"\Big|\textstyle\sum_t(\alpha - \mathrm{err}_t)\Big| \le \frac{\max(\alpha_1, 1 - \alpha_1) + \gamma}{\gamma}", font_size=34),
            cmath(r"\text{divide by } T", r":", r"\text{the bound} \qquad \blacksquare", font_size=36),
        ]
        rows[2][-1].set_color(COVC)
        whys = [why(r"it telescopes"), why(r"the level cannot run away"), why(r"bounded"), why(r"no probability used")]
        with self.voiceover(
            "<bookmark mark='a'/> The proof is two lines. Summing the update telescopes: the change in alpha over T steps is "
            "gamma times the total of alpha minus the misses. <bookmark mark='b'/> And alpha t cannot run away: if it drops "
            "below zero the set becomes everything and cannot miss, which pushes it back up; above one the set is empty, misses "
            "for certain, and is pushed back down. <bookmark mark='c'/> So the total deviation is bounded, <bookmark mark='d'/> "
            "and dividing by T gives the guarantee. No probability was used anywhere: it is a statement about every sequence, "
            "in the spirit of Part fifty-four's online learning."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def aci_worked(self):
        rows = [
            cmath(r"\alpha = 0.1, \ \gamma = 0.005", r":", r"\text{bound} = \frac{0.9 + 0.005}{0.005\,T} = \frac{181}{T}", font_size=34),
            cmath(r"T = 1{,}700", r":", r"\pm 10.6 \text{ points: \ uninformative}", font_size=36),
            cmath(r"\text{within one point}", r":", r"T \ge 18{,}100", font_size=36),
            cmath(r"\gamma = 0.02", r":", r"T \ge 4{,}600: \ \text{faster, \ but jumpier}", font_size=36),
        ]
        rows[1][-1].set_color(MISSC)
        rows[2][-1].set_color(COVC)
        whys = [why(r"the worst case"), why(r"the chart's run"), why(r"a long stream"), why(r"chapter 6's trade")]
        with self.voiceover(
            "<bookmark mark='a'/> How long is the long run? With alpha a tenth and gamma one in two hundred, the bound "
            "is nine hundred and five thousandths over gamma T: a hundred and eighty-one over T. <bookmark mark='b'/> "
            "For the seventeen hundred steps of our chart that is plus or minus ten points: a worst case, and "
            "uninformative. <bookmark mark='c'/> To be within one point needs eighteen thousand one hundred steps. "
            "<bookmark mark='d'/> With gamma four times larger it needs a quarter as many, at the price of jumpier "
            "sets. The guarantee is for every sequence, so it is conservative for any particular one."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def dtaci(self):
        rows = [
            cmath(r"\gamma \text{ small}", r":", r"\text{stable sets, \ slow to react}", font_size=36),
            cmath(r"\gamma \text{ large}", r":", r"\text{fast reaction, \ jumpy sets}", font_size=36),
            cmath(r"\text{DtACI}", r":", r"\text{run many } \gamma\text{'s, \ weight them by exponential weights}", font_size=34),
            cmath(r"\text{guarantee}", r":", r"\text{the same long-run bound, \ and adaptive regret}", font_size=34),
        ]
        rows[2][-1].set_color(WEIGHTC)
        whys = [why(r"under-reacts"), why(r"over-reacts"), why(r"Gibbs \& Cand\`es (2024)"), why(r"Part 54's Hedge")]
        with self.voiceover(
            "<bookmark mark='a'/> The step size gamma matters. Small gamma gives stable sets that are slow to react to "
            "a change; <bookmark mark='b'/> large gamma reacts quickly but makes the sets jump around. <bookmark "
            "mark='c'/> Gibbs and Candès's later method runs many values of gamma at once and combines them with "
            "exponential weights, the Hedge algorithm of Part fifty-four. <bookmark mark='d'/> It keeps the same "
            "long-run guarantee and adapts to the best gamma for each stretch of the data."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def beyond(self):
        rows = fit_rows(VGroup(
            label(r"what it does and does not say:", font_size=28, color=GREY_A),
            label(r"long-run frequency of misses $\to \alpha$, \ for any data", font_size=26, color=COVC),
            label(r"nothing about any single time, \ or about a subgroup", font_size=26, color=MISSC),
            label(r"choosing $\gamma$: \ fast adaptation or stable sets; \ later work adapts $\gamma$ itself", font_size=26, color=WEIGHTC),
            label(r"the same online-learning idea will give anytime-valid tests in Part 58", font_size=26, color=TESTPT),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> What it says, and what it does not. <bookmark mark='b'/> The long-run frequency of misses "
            "tends to alpha for any data. <bookmark mark='c'/> It says nothing about any single time, or about any subgroup. "
            "<bookmark mark='d'/> Gamma trades fast adaptation against stable sets, and later work adapts gamma itself. "
            "<bookmark mark='e'/> And the same online-learning idea, of controlling a cumulative error against every sequence, "
            "will give anytime-valid tests in Part fifty-eight."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
