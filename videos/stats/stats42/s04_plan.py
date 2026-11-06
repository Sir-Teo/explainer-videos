from __future__ import annotations

import numpy as np

from videos.stats.stats42.common import *  # noqa: F403


class TrialPlan(VoiceoverScene):
    def construct(self):
        self.card()
        self.protocol()
        self.ancova()
        self.check()
        self.run()
        self.result()
        self.board()
        self.reporting()

    def card(self):
        card = chapter_card(3, r"Case 1: \ the analysis plan", r"Decide the analysis before the data", part=PART)
        with self.voiceover("Chapter three. The analysis plan, written before any data exist."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def protocol(self):
        head = label(r"The protocol", font_size=36, color=CASE1).to_edge(UP, buff=0.5)
        rows = fit_rows(VGroup(
            label(r"1. \ \ draw 42 of the 200 towns at random: \ the trial speaks for the island", font_size=25),
            label(r"2. \ \ randomize 21 to the programme, \ 21 to control, \ by computer, \ after consent", font_size=25),
            label(r"3. \ \ after a year, \ measure 50 adults drawn at random from each town's register", font_size=25),
            label(r"4. \ \ primary analysis: \ town means on arm and the pilot's town mean, \ $t$ on 39 df", font_size=25, color=CASE1),
            label(r"5. \ \ secondary: \ a mixed model on adults; \ the person-weighted effect", font_size=25, color=GREY_A),
            label(r"6. \ \ registered before randomization; \ the ICC reported, \ whatever the result", font_size=25, color=GREY_A),
        ), 12.4, 0.42, [0, -0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The protocol has six lines. <bookmark mark='b'/> First, draw the forty-two towns at random "
            "from the two hundred, so that the trial's answer is the island's. <bookmark mark='c'/> Second, randomize twenty-one "
            "of them to the programme and twenty-one to control, by computer, after the towns have agreed to take part, so "
            "that no town can choose its arm. <bookmark mark='d'/> Third, after a year, measure fifty adults drawn at random from "
            "each town's register, by examiners who do not know the town's arm. <bookmark mark='e'/> Fourth, the primary "
            "analysis: regress the town means on arm and on the pilot's town mean, with a t on thirty-nine degrees of freedom. "
            "<bookmark mark='f'/> Fifth, secondary analyses: a mixed model on the adults, and the person-weighted effect. "
            "<bookmark mark='g'/> And sixth, register all of this before randomization, and report the intraclass "
            "correlation whatever the result, so the next planner has a better number than ours."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head))
            for k, m_ in enumerate("bcdefg"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def ancova(self):
        rows = [
            cmath(r"\bar y_j", r"=", r"\alpha + \tau z_j + \beta (\bar x_j - \bar x) + \varepsilon_j", font_size=36),
            cmath(r"\bar x_j", r":", r"\text{the town's pilot mean: \ it carries } b_j \text{, the town's own deviation}", font_size=30),
            cmath(r"\text{reliability}", r"=", r"\frac{\hat\sigma_b^2}{\hat\sigma_b^2 + \hat\sigma_w^2 / 30} \approx \frac{9.4}{9.4 + 8.8} = 0.52", font_size=32),
            cmath(r"\text{Var}(\hat\tau)", r"\downarrow", r"\text{randomization keeps } \hat\tau \text{ unbiased; } \ \bar x_j \text{ only removes noise}", font_size=30),
        ]
        rows[0][-1].set_color(CASE1)
        whys = [why(r"cluster-level ANCOVA"), why(r"a baseline covariate"), why(r"how much of $b_j$ it sees"),
                why(r"Part 35's covariate adjustment")]
        with self.voiceover(
            "<bookmark mark='a'/> Why adjust for the pilot? The primary model regresses each town's mean on its arm and on its "
            "own pilot mean, centred. <bookmark mark='b'/> The pilot mean carries the town's lasting deviation, the b j that "
            "made the design effect so expensive. <bookmark mark='c'/> How much of it? The pilot's town mean is a noisy reading of b j "
            "with reliability about a half, by the pilot's own estimates: the between-town variance over itself plus the "
            "within variance over thirty. <bookmark mark='d'/> Randomization keeps the adjusted estimate unbiased whatever the covariate, as in "
            "Part thirty-five; the covariate only removes noise. Because it is named in the protocol, there is no fishing."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def check(self):
        p = load("plan")
        names = [r"individual $z$", r"cluster $t$", r"cluster ANCOVA"]
        keys = ["naive", "t", "ancova"]
        cols = [NAIVEC, CASE1, GOODC]
        A = axes([0, 7], [0, 1], x_length=7.4, y_length=4.4, ylabel=r"share of 4,000 simulated trials significant",
                 yticks=[0, 0.05, 0.5, 0.8, 1], xticks=[], center=[-2.5, 0.0, 0])
        ax = A.ax
        size = bars_at(ax, [0.6, 2.9, 5.2], [p["size"][k] for k in keys], 0.8, GREY_B, opacity=0.85)
        power = bars_at(ax, [1.5, 3.8, 6.1], [p["power"][k] for k in keys], 0.8, S.ACCENT, opacity=0.85)
        for i, c in enumerate(cols):
            size[i].set_fill(c, opacity=0.45)
            power[i].set_fill(c, opacity=0.95)
        tags = VGroup(*[label(n, font_size=20, color=c).next_to(ax.c2p(1.05 + 2.3 * i, 0), DOWN, buff=0.2) for i, (n, c) in enumerate(zip(names, cols))])
        vals = VGroup()
        for i, k in enumerate(keys):
            vals.add(label(f"{100 * p['size'][k]:.1f}\\%", font_size=18, color=GREY_A).next_to(size[i], UP, buff=0.06))
            vals.add(label(f"{100 * p['power'][k]:.1f}\\%", font_size=18, color=GREY_A).next_to(power[i], UP, buff=0.06))
        line05 = DashedLine(ax.c2p(0, 0.05), ax.c2p(7, 0.05), color=GREY_B, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"faint: \ no effect \ (the type I error)", font_size=24, color=GREY_A),
            label(r"solid: \ the 4 mm Hg effect \ (power)", font_size=24, color=GREY_A),
            label(rf"individual analysis: \ {100 * p['size']['naive']:.0f}\% false alarms", font_size=24, color=NAIVEC),
            label(rf"ANCOVA: \ power {100 * p['power']['t']:.0f}\% $\to$ {100 * p['power']['ancova']:.0f}\%", font_size=24, color=GOODC),
            label(rf"SD of $\hat\tau$: \ {p['sd']['t']:.2f} $\to$ {p['sd']['ancova']:.2f}", font_size=24, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A plan should be tested before it is used, and the World lets us test it: four thousand "
            f"trials drawn from the towns' law, each analysed three ways. Faint bars are trials with no effect at all; "
            f"<bookmark mark='b'/> solid bars, trials with the four millimetre effect. <bookmark mark='c'/> Analysing adults "
            f"as if independent declares a significant effect in {100 * p['size']['naive']:.0f} percent of trials where "
            f"there is none: six times the promised five. Both cluster-level analyses hold their five percent. <bookmark "
            f"mark='d'/> And the adjustment pays: power rises from {100 * p['power']['t']:.0f} percent to "
            f"{100 * p['power']['ancova']:.0f}, <bookmark mark='e'/> because the standard deviation of the estimate falls "
            f"from {say(p['sd']['t'], 2)} to {say(p['sd']['ancova'], 2)}. With the pilot in the model, about twenty-eight "
            f"towns would have done. We keep forty-two: the pilot's ICC was uncertain, and so is its covariate's strength."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tags), FadeIn(line05), FadeIn(trial_tag()))
            vo.wait_until("a")
            self.play(FadeIn(size), FadeIn(side[0]), *[FadeIn(vals[2 * i]) for i in range(3)])
            vo.wait_until("b")
            self.play(FadeIn(power), FadeIn(side[1]), *[FadeIn(vals[2 * i + 1]) for i in range(3)])
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def run(self):
        p = load("plan")
        xy = np.asarray(p["all_xy"])
        pick = np.asarray(p["towns"])
        z = np.asarray(p["z"], bool)
        s, c0 = 0.62, np.array([-3.0, -0.2, 0])
        P = lambda q: c0 + s * np.array([q[0], q[1], 0])  # noqa: E731
        allt = VGroup(*[Dot(P(q), radius=0.05, color=GREY_C) for q in xy])
        chosen = VGroup(*[Dot(P(xy[j]), radius=0.09, color=WHITE) for j in pick])
        armed = [chosen[i].animate.set_color(PROGC if z[i] else CTRLC) for i in range(len(pick))]
        side = fit_rows(VGroup(
            label(r"the island's 200 towns", font_size=24, color=GREY_A),
            label(r"42 drawn at random", font_size=24),
            label(r"21 randomized to the programme", font_size=24, color=PROGC),
            label(r"21 to control", font_size=24, color=CTRLC),
            label(r"a year later: \ 50 adults per town", font_size=24, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Now the ministry runs the trial, in the World. Here are its two hundred towns. <bookmark "
            "mark='b'/> Forty-two are drawn at random. <bookmark mark='c'/> A computer assigns twenty-one to the programme "
            "<bookmark mark='d'/> and twenty-one to control. <bookmark mark='e'/> A year later, fifty adults in each town have "
            "their pressure measured."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(allt), FadeIn(side[0]), FadeIn(trial_tag()))
            vo.wait_until("b")
            self.play(FadeIn(chosen), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(*armed[:0], *[chosen[i].animate.set_color(PROGC) for i in range(len(pick)) if z[i]], FadeIn(side[2]))
            vo.wait_until("d")
            self.play(*[chosen[i].animate.set_color(CTRLC) for i in range(len(pick)) if not z[i]], FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def result(self):
        p = load("plan")
        x, y, z = np.asarray(p["base"]), np.asarray(p["ybar"]), np.asarray(p["z"], bool)
        X = np.column_stack([np.ones(len(y)), z, x - x.mean()])
        b, *_ = np.linalg.lstsq(X, y, rcond=None)
        A = axes([110, 132], [110, 136], x_length=7.4, y_length=4.4, xlabel=r"the town's pilot mean, \ mm Hg",
                 ylabel=r"the town's mean a year later", xticks=[110, 115, 120, 125, 130], yticks=[110, 120, 130], center=[-2.5, 0.2, 0])
        ax = A.ax
        dots_p = VGroup(*[Dot(ax.c2p(a, c), radius=0.08, color=PROGC) for a, c in zip(x[z], y[z])])
        dots_c = VGroup(*[Dot(ax.c2p(a, c), radius=0.08, color=CTRLC) for a, c in zip(x[~z], y[~z])])
        xm = x.mean()
        lc = Line(ax.c2p(111, b[0] + b[2] * (111 - xm)), ax.c2p(131, b[0] + b[2] * (131 - xm)), color=CTRLC, stroke_width=3)
        lp = Line(ax.c2p(111, b[0] + b[1] + b[2] * (111 - xm)), ax.c2p(131, b[0] + b[1] + b[2] * (131 - xm)), color=PROGC, stroke_width=3)
        r = p["result"]
        side = fit_rows(VGroup(
            label(rf"ANCOVA: \ ${r['ancova'][0]:.2f}$ \ [{r['ancova'][2]:.2f}, \ {r['ancova'][3]:.2f}]", font_size=24, color=GOODC),
            label(rf"cluster $t$: \ ${r['t'][0]:.2f}$ \ [{r['t'][2]:.2f}, \ {r['t'][3]:.2f}]", font_size=24, color=CASE1),
            label(rf"individual: \ ${r['naive'][0]:.2f}$ \ [{r['naive'][2]:.2f}, \ {r['naive'][3]:.2f}]", font_size=24, color=NAIVEC),
            label(r"95\% intervals, \ mm Hg", font_size=20, color=GREY_B),
            label(r"the World's truth: \ $-4.00$", font_size=24, color=EXACT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Here is the result. Each dot is a town: its pilot mean across, its mean a year later up. "
            f"Programme towns in green, controls in blue. <bookmark mark='b'/> The pre-specified analysis fits two parallel "
            f"lines; the gap between them is the effect, {say(r['ancova'][0], 2)} millimetres, with a ninety-five percent "
            f"interval from {say(r['ancova'][2], 2)} to {say(r['ancova'][3], 2)}. <bookmark mark='c'/> The unadjusted "
            f"cluster t finds {say(r['t'][0], 2)}, with an interval that crosses zero: the same data, less precisely used. "
            f"<bookmark mark='d'/> The individual-level analysis reports the same estimate as the cluster t with an interval "
            f"less than half as wide, a precision the design never had. <bookmark mark='e'/> The World's true effect is minus four. "
            f"This trial, like most, landed a little short of the truth; only the honest analyses say how short it might be."
        ) as vo:
            self.play(FadeIn(A), FadeIn(trial_tag()))
            vo.wait_until("a")
            self.play(FadeIn(dots_c), FadeIn(dots_p))
            vo.wait_until("b")
            self.play(Create(lc), Create(lp), FadeIn(side[0]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def board(self):
        rows = board_rows("cluster")
        show_board(self, rows,
                   "<bookmark mark='a'/> The Coverage Board, over four thousand trials drawn from the towns' law. The "
                   "individual-level interval, nominally ninety percent, covers the true effect sixty-one percent of the time: "
                   "broken. <bookmark mark='b'/> The cluster-level t and the cluster-level ANCOVA both cover ninety percent: "
                   "kept. Cornfield's self-deception, measured.",
                   [("a", [0]), ("b", [1, 2])])

    def reporting(self):
        rows = fit_rows(VGroup(
            label(r"report it by CONSORT's extension for cluster trials:", font_size=26, color=GREY_A),
            label(r"towns and adults at each stage; \ the ICC; \ the analysis that accounts for clustering", font_size=24),
            label(r"and say what was \emph{not} learned: \ one year, \ one island, \ pressure rather than strokes", font_size=24, color=S.ACCENT),
            label(r"a real trial of this kind: \ the salt substitute trial, \ 600 villages \ (2021)", font_size=24, color=CASE2),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The report follows the CONSORT statement's extension for cluster trials, <bookmark "
            "mark='b'/> which asks for the flow of towns and adults through every stage, the intraclass correlation, and an "
            "analysis that accounts for clustering. <bookmark mark='c'/> It should also say what the trial did not learn: one "
            "year, one island, and blood pressure rather than the strokes the ministry actually cares about. <bookmark "
            "mark='d'/> Trials like this are real. The largest, published in 2021, randomized six hundred Chinese villages, "
            "and its subject is the second case."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
