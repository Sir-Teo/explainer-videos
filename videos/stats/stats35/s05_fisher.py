from __future__ import annotations

import numpy as np

from videos.stats.stats35.common import *  # noqa: F403


class Fisher(VoiceoverScene):
    def construct(self):
        self.card()
        self.sharp()
        self.twelve()
        self.dist()
        self.invert()
        self.all2000()
        self.weak()

    def card(self):
        card = chapter_card(4, r"Fisher's sharp null", r"Testing without a model", lit=(1935,), part=PART)
        with self.voiceover("Chapter four. Fisher's sharp null hypothesis."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def sharp(self):
        rows = [
            cmath(r"H_0", r":", r"Y_i(1) = Y_i(0) \ \text{for every } i", font_size=32),
            cmath(r"\text{under } H_0", r":", r"\text{the whole science is known: } Y_i(0) = Y_i(1) = Y_i", font_size=28),
            cmath(r"\text{re-randomize}", r":", r"T(z') \text{ for every possible assignment } z'", font_size=30),
            cmath(r"p", r"=", r"\tfrac{\#\{z': |T(z')| \ge |T_{\rm obs}|\}}{\binom{n}{n_1}}", font_size=32),
        ]
        rows[3][-1].set_color(Y0C)
        whys = [why(r"`sharp': \ every unit"), why(r"no missing data at all"), why(r"Part 13; \ Part 16"),
                why(r"exact, \ for any $n$")]
        with self.voiceover(
            "<bookmark mark='a'/> Fisher's way round the missing half of the science was to test a hypothesis that fills "
            "it in. His null hypothesis is sharp: the treatment does nothing to anyone, so each patient's two potential "
            "outcomes are equal. <bookmark mark='b'/> Under that null the science is completely known: whatever we "
            "observed for a patient is what they would have had either way. <bookmark mark='c'/> So we can compute the "
            "test statistic, say the difference in means, for every assignment the coin might have produced, as in Parts "
            "13 and 16. <bookmark mark='d'/> The p-value is the share of possible assignments giving a statistic at least "
            "as extreme as the one observed. It is exact for any sample size, and needs no model for the outcomes."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def twelve(self):
        d = load("fisher")
        y, z = np.asarray(d["y"]), np.asarray(d["z"], bool)
        rows = [[r"patient", r"arm", r"$Y_i$ (mm Hg)"]] + [[rf"{i + 1}", r"drug" if z[i] else r"control", rf"{y[i]:.0f}"] for i in range(12)]
        tab = table_rows(rows, font_size=22, col_buff=0.6, row_buff=0.12,
                         colors=[GREY_A] + [Y1C if z[i] else Y0C for i in range(12)]).move_to([-3.2, 0, 0])
        if tab.height > 6.6:
            tab.height = 6.6
        side = fit_rows(VGroup(
            label(r"a pilot: \ 12 patients, \ 6 and 6", font_size=22),
            label(rf"drug mean $-$ control mean $= {d['obs']:+.1f}$", font_size=22, color=TAUC),
            label(rf"$\binom{{12}}{{6}} = {d['n_assign']}$ possible assignments", font_size=22, color=Y0C),
        ), 5.2, 0.42, [3.4, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Try it on a pilot study: twelve of the World's patients, six assigned to the drug and six "
            "to control. <bookmark mark='b'/> By the luck of the draw, the drug group's pressures at twelve weeks are "
            "higher, by " + say(d["obs"], 1) + " points. <bookmark mark='c'/> There are nine hundred and twenty-four ways to "
            "choose six of twelve. Under the sharp null, each would have produced its own difference, from the same twelve "
            "numbers."
        ) as vo:
            self.add(trial_tag())
            self.play(FadeIn(tab))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def dist(self):
        d = load("fisher")
        h, e = np.asarray(d["hist"], float), np.asarray(d["edges"], float)
        lo, hi = float(e[0]), float(e[-1])
        A = axes([lo, hi], [0, h.max() / h.sum() * 1.2], x_length=7.4, y_length=4.2, xlabel=r"difference in means under $H_0$",
                 ylabel=r"share", xticks=[round(lo / 5) * 5, 0, round(hi / 5) * 5], yticks=[0, 0.05],
                 center=[-2.0, 0.2, 0])
        ax = A.ax
        cols = [Y0C if abs((a + b) / 2) >= abs(d["obs"]) else GREY_C for a, b in zip(e[:-1], e[1:])]
        bars = VGroup(*[bars_at(ax, [(a + b) / 2], [v / h.sum()], (b - a) * 0.9, c) for a, b, v, c in zip(e[:-1], e[1:], h, cols)])
        obs = DashedLine(ax.c2p(d["obs"], 0), ax.c2p(d["obs"], h.max() / h.sum() * 1.15), color=TAUC, stroke_width=3)
        side = fit_rows(VGroup(
            label(r"all 924 differences, \ under the sharp null", font_size=22),
            label(rf"observed: \ ${d['obs']:+.1f}$", font_size=22, color=TAUC),
            label(rf"$p = {d['p']:.2f}$: \ entirely ordinary", font_size=22, color=Y0C),
            label(r"12 patients cannot see an 8-point effect", font_size=22, color=MISSC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here are all nine hundred and twenty-four. <bookmark mark='b'/> The observed difference "
            "sits in the middle of them. <bookmark mark='c'/> The share at least as far from zero is " + say(d["p"]) + ", so "
            "nothing in this pilot is surprising if the drug does nothing. <bookmark mark='d'/> That is not evidence that "
            "it does nothing. The patients' pressures differ from one another by ten or twenty points, so with twelve of "
            "them, a real effect of eight points is invisible."
        ) as vo:
            self.add(trial_tag())
            self.play(FadeIn(A), FadeIn(bars))
            vo.wait_until("b")
            self.play(Create(obs), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def invert(self):
        d = load("fisher")
        rows = [
            cmath(r"H_0(\tau_0)", r":", r"Y_i(1) = Y_i(0) + \tau_0 \ \text{for every } i", font_size=30),
            cmath(r"\text{impute}", r":", r"Y_i(0) = Y_i - \tau_0 Z_i, \ \ Y_i(1) = Y_i(0) + \tau_0", font_size=30),
            cmath(r"\text{keep}", r":", r"\{\tau_0: p(\tau_0) > 0.1\}", font_size=32),
            cmath(r"\text{pilot}", r":", rf"[{d['ci'][0]:.1f}, \ {d['ci'][1]:.1f}] \ \text{{mm Hg}}", font_size=32),
        ]
        rows[3][-1].set_color(TAUC)
        whys = [why(r"a constant effect $\tau_0$"), why(r"again, \ no missing data"), why(r"a 90\% set by test inversion"),
                why(r"honest, \ and very wide")]
        with self.voiceover(
            "<bookmark mark='a'/> Fisher's test also gives an interval. Any constant-effect hypothesis, that the drug "
            "changes everyone's pressure by exactly tau nought, is also sharp. <bookmark mark='b'/> It too fills in the "
            "science: subtract tau nought from the treated outcomes to get their untreated ones. <bookmark mark='c'/> Test "
            "each tau nought in turn, and keep those not rejected at ten percent. <bookmark mark='d'/> For the pilot, the "
            "interval runs from minus " + say(-d["ci"][0], 0) + " to plus " + say(d["ci"][1], 1) + " points: honest, and "
            "far too wide to be useful."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def all2000(self):
        d = load("fisher")
        rows = fit_rows(VGroup(
            label(r"all 2,000 patients: \ $\binom{2000}{1000} \approx 10^{600}$ assignments", font_size=26),
            label(r"so sample 10,000 of them at random", font_size=26, color=GREY_A),
            label(rf"observed difference: \ ${d['big_obs']:.2f}$", font_size=26, color=TAUC),
            label(rf"the largest of 10,000 null differences: \ {d['big_max']:.2f} \ (SD {d['big_sd']:.2f})", font_size=26, color=Y0C),
            label(r"$p < 1/10{,}000$: \ the drug does something to someone", font_size=26, color=BANDC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> With all two thousand patients there are about ten to the six hundred possible "
            "assignments, <bookmark mark='b'/> so we sample ten thousand of them at random instead. <bookmark mark='c'/> "
            "The observed difference is minus " + say(-d["big_obs"], 1) + " points. <bookmark mark='d'/> The largest of the "
            "ten thousand null differences is only " + say(d["big_max"], 1) + ", and their standard deviation is half a "
            "point. <bookmark mark='e'/> So the p-value is below one in ten thousand: the drug certainly does something to "
            "someone."
        ) as vo:
            self.add(trial_tag())
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def weak(self):
        rows = fit_rows(VGroup(
            label(r"Fisher's null: \ no effect on \emph{anyone}", font_size=26, color=Y0C),
            label(r"Neyman's null: \ no effect \emph{on average}, \ $\bar\tau = 0$", font_size=26, color=TAUC),
            label(r"different questions: \ a drug that helps some and harms others has $\bar\tau = 0$ \ but is not null", font_size=26),
            label(r"the 1935 quarrel; \ today: \ randomization tests that are valid for both (Wu \& Ding 2021)", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Fisher's null says the treatment affects no one. <bookmark mark='b'/> Neyman's says the "
            "effects average to zero. <bookmark mark='c'/> These are different questions: a drug that helps some patients "
            "and harms others equally has a zero average effect, but is far from null in Fisher's sense. <bookmark "
            "mark='d'/> The two men quarrelled about it, bitterly, at the Royal Statistical Society in 1935. Modern work, "
            "such as Jason Wu and Peng Ding's of 2021, shows how to studentize a randomization test so that it is exact for "
            "Fisher's null and asymptotically valid for Neyman's. Neyman's approach comes next."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
