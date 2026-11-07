from __future__ import annotations

import numpy as np

from videos.stats.stats37.common import *  # noqa: F403


class Honest(VoiceoverScene):
    def construct(self):
        self.card()
        self.pretests()
        self.example()
        self.idea()
        self.sets()
        self.rm()
        self.lesson()

    def card(self):
        card = chapter_card(10, r"Honest parallel trends", r"What if the trends were not quite parallel?", lit=(2022, 2023), part=PART)
        with self.voiceover("Chapter ten. Honest parallel trends."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def pretests(self):
        rows = fit_rows(VGroup(
            label(r"common practice: \ test the leads; \ if none is significant, \ assume parallel trends", font_size=26),
            label(r"Roth (2022): \ such pre-tests often have little power against trends that matter", font_size=26, color=MISSC),
            label(r"and conditioning on passing them biases what is reported", font_size=26, color=MISSC),
            label(r"better: \ say how far from parallel the trends may be, \ and carry that into the interval", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Common practice treats the leads of an event study as a test: if none is significantly "
            "different from zero, assume parallel trends and move on. <bookmark mark='b'/> Jonathan Roth showed in 2022 "
            "that these pre-tests often have little power against violations large enough to matter. <bookmark mark='c'/> "
            "Worse, reporting only the studies that pass them distorts what gets reported, Part thirty-three's selection "
            "again. <bookmark mark='d'/> The better approach is to say how far from parallel the trends might plausibly be, "
            "and carry that uncertainty into the conclusion."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def example(self):
        d = load("honest")
        e = np.asarray(d["e"], float)
        att, se = np.asarray(d["att"], float), np.asarray(d["se"], float)
        A = axes([-10, 6], [-2.5, 3], x_length=7.6, y_length=4.2, xlabel=r"years since adoption", ylabel=r"event-study estimate",
                 xticks=[-10, -5, 0, 5], yticks=[-2, -1, 0, 1, 2, 3], center=[-1.8, 0.2, 0])
        ax = A.ax
        bnd = band(ax, e, att - 1.645 * se, att + 1.645 * se, Y1C, 0.18)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=Y1C) for a, b in zip(e, att)])
        zero = DashedLine(ax.c2p(-10, 0), ax.c2p(6, 0), color=GREY_C, stroke_width=1.5)
        truth = DashedLine(ax.c2p(0, 1.0), ax.c2p(6, 1.0), color=TRUEC, stroke_width=2.5)
        side = fit_rows(VGroup(
            label(r"150 towns adopt in 2010, \ chosen because they were improving", font_size=22),
            label(rf"their untreated trend: \ +{d['trend']:.1f} a year more than the 150 others", font_size=22, color=MISSC),
            label(rf"the effect: \ +1.0 from adoption on \ (gold)", font_size=22, color=TRUEC),
            label(rf"first-year estimate: \ {d['est0']:.2f}, \ 90\% CI {d['naive_ci'][0]:.2f} to {d['naive_ci'][1]:.2f}", font_size=22, color=Y1C),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A seeded example, with a hundred and fifty towns that adopt a programme in 2010, chosen "
            "because they were already improving, and a hundred and fifty that never adopt. <bookmark mark='b'/> Their "
            "untreated employment rises two tenths of a point a year faster. The leads show it: a steady climb towards "
            "zero. <bookmark mark='c'/> The programme adds exactly one point from adoption on. <bookmark mark='d'/> But the "
            "first-year estimate is " + say(d["est0"], 2) + ", and the lags keep climbing, because the pre-existing trend "
            "is read as effect. The conventional interval excludes the truth."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(zero), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bnd), FadeIn(dots), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(truth), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def idea(self):
        rows = [
            cmath(r"\beta_{e}", r"=", r"\tau_e + \delta_e \quad (\delta: \text{ the violation of parallel trends})", font_size=30),
            cmath(r"\text{leads}", r":", r"\beta_e = \delta_e \text{ for } e < 0 \ \text{(no effect yet)}", font_size=30),
            cmath(r"\text{teaching linear-trend bound }(M)", r":", r"\delta_0 \text{ within } M \text{ of the linear trend in the leads}", font_size=30),
            cmath(r"\Delta^{RM}(\bar M)", r":", r"|\delta_0 - \delta_{-1}| \le \bar M \max_{e<0} |\delta_e - \delta_{e-1}|", font_size=30),
        ]
        rows[2][-1].set_color(BANDC)
        whys = [why(r"every estimate mixes effect and violation"), why(r"the leads measure the violation"),
                why(r"smoothness: \ trends may bend, \ a little"), why(r"relative magnitudes")]
        with self.voiceover(
            "<bookmark mark='a'/> Ashesh Rambachan and Jonathan Roth's framework, published in 2023, writes the "
            "population event-study coefficient as the effect plus the violation of parallel trends. Estimates add "
            "sampling error, correlated across event times. <bookmark mark='b'/> Before adoption there is no effect, "
            "so the leads estimate the violation directly. <bookmark mark='c'/> Then they restrict how the violation "
            "may continue after adoption. Our simplified first-post-period model bounds departure from a fitted "
            "population linear pre-trend by M. It illustrates sensitivity but differs from their full "
            "smoothness-restriction procedure. <bookmark mark='d'/> Under relative magnitudes, the jump after "
            "adoption is at most M-bar times the largest jump seen before it. We account for the full joint "
            "covariance in the linear extrapolation, and use simultaneous pre-jump bounds for the relative-magnitude "
            "interval. These are asymptotic intervals under the stated teaching restrictions."
        ) as vo:
            intro=label('Sensitivity intervals carry uncertainty in pre-trends into conclusions',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def sets(self):
        d = load("honest")
        Ms = [float(m) for m in d["Ms"]]
        A = axes([-0.1, 0.9], [-0.2, 2.2], x_length=7.2, y_length=4.2, xlabel=r"allowed departure $M$ from the linear pre-trend",
                 ylabel=r"first-year effect", xticks=[0, 0.2, 0.4, 0.6, 0.8], yticks=[0, 0.5, 1, 1.5, 2],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-1.8, 0.2, 0])
        ax = A.ax
        bars = VGroup()
        for M in Ms:
            s = d["sd"][str(M) if str(M) in d["sd"] else f"{M}"]
            bars.add(VGroup(Line(ax.c2p(M, s["ci"][0]), ax.c2p(M, s["ci"][1]), color=BANDC, stroke_width=4),
                            Line(ax.c2p(M, s["set"][0]), ax.c2p(M, s["set"][1]), color=TAUC, stroke_width=9)))
        naive = Line(ax.c2p(-0.06, d["naive_ci"][0]), ax.c2p(-0.06, d["naive_ci"][1]), color=Y1C, stroke_width=4)
        truth = DashedLine(ax.c2p(-0.1, 1.0), ax.c2p(0.9, 1.0), color=TRUEC, stroke_width=2)
        zero = DashedLine(ax.c2p(-0.1, 0), ax.c2p(0.9, 0), color=GREY_C, stroke_width=1.5)
        s0 = d["sd"]["0.0"]
        side = fit_rows(VGroup(
            label(r"red, \ far left: \ the conventional interval", font_size=22, color=Y1C),
            label(rf"$M = 0$: \ extrapolate the pre-trend: \ {s0['mid']:.2f} \ ({s0['ci'][0]:.2f} to {s0['ci'][1]:.2f})", font_size=22, color=BANDC),
            label(r"gold: plug-in set; \ green: asymptotic 90\% interval", font_size=22, color=TAUC),
            label(rf"breakdown: \ the effect stays positive until $M$ = {d['breakdown']:.2f}", font_size=22, color=GREY_A),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> For the first year after adoption. On the left, in red, the conventional interval, which "
            "misses the truth. <bookmark mark='b'/> With M equal to zero, the violation is assumed to continue the linear "
            "pre-trend exactly. Subtracting it gives " + say(s0["mid"], 2) + ", with an interval that covers the truth of one. "
            "<bookmark mark='c'/> Allowing the trend to bend by up to M widens the set, in gold, and its interval, in green. "
            "<bookmark mark='d'/> The conclusion that the programme helped survives until M is about " + say(d["breakdown"], 2)
            + ", a departure from this particular linear extrapolation. Its scale and interpretation depend on the "
            "restriction being imposed. That breakdown value is what a reader needs in order to judge."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(zero), Create(truth))
            vo.wait_until("a")
            self.play(Create(naive), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b) for b in bars[1:]], lag_ratio=0.2), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def rm(self):
        d = load("honest")
        rows = [[r"$\bar M$", r"plug-in set", r"90\% Bonferroni interval"]]
        for k in ("0.5", "1.0", "2.0"):
            r = d["rm"][k]
            rows.append([k, rf"{r['set'][0]:.2f} to {r['set'][1]:.2f}", rf"{r['ci'][0]:.2f} to {r['ci'][1]:.2f}"])
        tab = table_rows(rows, font_size=28, col_buff=1.0, row_buff=0.3, colors=[GREY_A, BANDC, TAUC, MISSC]).move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(rf"relative magnitudes: \ the largest year-to-year jump in the leads is {d['rm']['1.0']['max_pre_jump']:.2f}", font_size=24, color=GREY_A),
            label(r"$\bar M = 1$: \ after adoption the trend may jump as much as it ever did before", font_size=24, color=TAUC),
        ), 12.4, 0.3, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Under relative magnitudes, the largest year-to-year change in the leads is "
            + say(d["rm"]["1.0"]["max_pre_jump"], 2) + ". <bookmark mark='b'/> If the violation can jump after adoption by "
            "half that, or by as much, the effect is clearly positive. <bookmark mark='c'/> Even if it can jump by twice the "
            "largest change seen before, the interval stays above zero, from " + say(d["rm"]["2.0"]["ci"][0], 2) + ". The post-treatment restrictions cannot be verified from pre-treatment outcomes alone; the point is to "
            "make the assumption explicit, and to let a reader with a different view recompute the answer."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]), FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"parallel trends is an assumption about counterfactuals: \ the leads inform it, \ not prove it", font_size=26, color=TAUC),
            label(r"report the event study, \ the sensitivity sets, \ and the breakdown value", font_size=26, color=BANDC),
            label(r"the same spirit as Part 36's E-values and robustness values", font_size=26, color=GREY_A),
            label(r"next: \ one treated unit and many possible controls", font_size=26, color=Y0C),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Parallel trends is an assumption about what would have happened. The leads inform it; "
            "they cannot prove it. <bookmark mark='b'/> So report the event study, the sensitivity sets, and the breakdown "
            "value, the departure at which the conclusion changes. <bookmark mark='c'/> It is the same spirit as the "
            "E-values and robustness values of Part thirty-six. <bookmark mark='d'/> Next: what to do when only one unit was "
            "treated, and there are many possible controls."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
