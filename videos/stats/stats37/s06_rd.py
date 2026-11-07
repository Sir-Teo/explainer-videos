from __future__ import annotations

import numpy as np

from videos.stats.stats37.common import *  # noqa: F403


def lens_axes(center=(-1.6, 0.2, 0), x_length=8.2, y_length=4.4):
    return axes([30, 90], [20, 150], x_length=x_length, y_length=y_length, xlabel=r"exam score", ylabel=r"earnings at 30 (thousands)",
                xticks=[30, 45, 60, 75, 90], yticks=[25, 75, 125], center=list(center))


class RD(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.picture()
        self.identify()
        self.local()
        self.sensitivity()
        self.robust()
        self.study()
        self.board()

    def card(self):
        card = chapter_card(5, r"Regression discontinuity", r"Nature's experiment at a cutoff", lit=(1960, 2012, 2014), part=PART)
        with self.voiceover("Chapter five. Regression discontinuity."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def history(self):
        rows = fit_rows(VGroup(
            label(r"Thistlethwaite \& Campbell (1960): \ certificates of merit for students above a test-score cutoff", font_size=26, color=TAUC),
            label(r"students just above and just below the line are alike in everything but the award", font_size=26),
            label(r"so the jump in outcomes at the line is the award's effect, \ there", font_size=26, color=CUTC),
            label(r"ignored for decades; \ revived in economics around 2000 \ (Hahn, \ Todd \& van der Klaauw 2001)", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1960 the psychologists Donald Thistlethwaite and Donald Campbell studied the National "
            "Merit Scholarship programme, which gave certificates of merit to students who scored above a cutoff. <bookmark "
            "mark='b'/> A student who scored one point above the line is much like one who scored one point below, except "
            "that one got the certificate. <bookmark mark='c'/> So the jump in later outcomes at the line estimates the "
            "certificate's effect, for students at the line. <bookmark mark='d'/> The design was largely ignored for forty "
            "years, then revived by economists around 2000, when Jinyong Hahn, Petra Todd and Wilbert van der Klaauw set out "
            "its assumptions formally."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def picture(self):
        d = load("rd")
        A = lens_axes()
        mids, means = np.asarray(d["mids"], float), np.asarray(d["means"], float)
        k = (mids >= 30) & (mids <= 90)
        L = CutoffLens(A.ax, mids[k], means[k], d["c"])
        side = fit_rows(VGroup(
            label(r"the World: \ a scholarship for an exam score of 60 or more", font_size=22),
            label(r"dots: \ mean earnings at 30, \ by 1-point score bins", font_size=22, color=GREY_A),
            label(rf"scholars vs the rest: \ +{d['naive']:.1f} thousand", font_size=22, color=MISSC),
            label(r"but the better students win: \ compare only near the line", font_size=22, color=CUTC),
        ), 3.6, 0.42, [5.0, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The World has a scholarship of its own: for ten years, every school-leaver who scored at "
            "least sixty on the final exam won a university scholarship. Forty thousand school-leavers, and their earnings "
            "at thirty. <bookmark mark='b'/> Each dot is the mean earnings for one point of the score. Blue below the cutoff, "
            "red above. <bookmark mark='c'/> Scholars earn " + say(d["naive"], 1) + " thousand a year more than everyone else. "
            "<bookmark mark='d'/> But that compares strong students with weak ones. The design compares only those near the "
            "line, and asks how big the step is, right at sixty."
        ) as vo:
            self.add(schol_tag())
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(L), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Indicate(L.line))
        self.clear_scene()

    def identify(self):
        rows = [
            cmath(r"D", r"=", r"\mathbf{1}\{R \ge c\} \quad \text{(sharp)}", font_size=32),
            cmath(r"\text{assume}", r":", r"E[Y(0) \mid R = r],\ E[Y(1) \mid R = r] \text{ continuous at } c", font_size=30),
            cmath(r"\tau_c", r"=", r"\lim_{r \downarrow c} E[Y \mid R = r] - \lim_{r \uparrow c} E[Y \mid R = r]", font_size=30),
            cmath(r"\text{no overlap}", r":", r"\text{an extrapolation to the cutoff from each side}", font_size=30),
        ]
        rows[2][-1].set_color(CUTC)
        whys = [why(r"treatment is decided by the score"), why(r"nothing else jumps at $c$"),
                why(r"Hahn, \ Todd \& van der Klaauw (2001)"), why(r"so the estimate is a boundary problem")]
        with self.voiceover(
            "<bookmark mark='a'/> Formally: treatment is decided by the running variable, the score, crossing the "
            "cutoff c. <bookmark mark='b'/> Assume that the average potential outcomes, with and without the "
            "scholarship, have continuous conditional means at the cutoff, with no other discontinuous intervention. "
            "The World records scores in tenths, so applying continuous-score limit theory here also uses a local "
            "smoothness approximation. <bookmark mark='c'/> Then the effect at the cutoff is the difference between "
            "the two one-sided limits of the regression of the outcome on the score. <bookmark mark='d'/> No one at "
            "the cutoff is both treated and untreated: there is no overlap at all, so each side must be extrapolated "
            "to the line. Estimation is a problem at the boundary of the data."
        ) as vo:
            intro=label('A cutoff identifies a local effect under continuity assumptions',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def local(self):
        d = load("rd")
        A = lens_axes()
        mids, means = np.asarray(d["mids"], float), np.asarray(d["means"], float)
        k = (mids >= 30) & (mids <= 90)
        L = CutoffLens(A.ax, mids[k], means[k], d["c"])
        h = d["h"]
        win = L.window(h)
        fl, fr = L.fit(d["conv"]["left"], h, "left"), L.fit(d["conv"]["right"], h, "right")
        jl, jr = d["conv"]["left"][0], d["conv"]["right"][0]
        J = L.jump(jl, jr, rf"{d['conv']['tau']:.2f}")
        ql, qr = L.fit(d["robust"]["left"], h, "left", color=BANDC), L.fit(d["robust"]["right"], h, "right", color=BANDC)
        side = fit_rows(VGroup(
            label(r"local linear: \ a line on each side, \ triangular weights", font_size=22),
            label(rf"IK-inspired teaching plug-in: \ $h$ = {h:.1f} points", font_size=22, color=CUTC),
            label(rf"jump: \ {d['conv']['tau']:.2f} \ (SE {d['conv']['se']:.2f}); \ truth {d['truth']:.1f}", font_size=22, color=MISSC),
            label(rf"local quadratic: \ {d['robust']['tau']:.2f} \ (SE {d['robust']['se']:.2f})", font_size=22, color=BANDC),
        ), 3.6, 0.42, [5.0, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The standard estimator is local linear regression: on each side of the cutoff, fit "
            "a straight line to the points within a bandwidth h, weighting them by a triangle that peaks at the "
            "cutoff. <bookmark mark='b'/> Our teaching plug-in follows the structure of Imbens and Kalyanaraman's "
            "2012 bandwidth rule. It is not independently validated as their reference implementation or the exact "
            "finite-sample MSE optimum; here it is " + say(h, 1) + " points. <bookmark mark='c'/> The jump between the two lines "
            "at sixty is " + say(d["conv"]["tau"], 2) + " thousand, with a standard error of " + say(d["conv"]["se"], 2)
            + ". The World's truth is three. The earnings curve bends upward, and a straight line across thirty points cannot "
            "follow it to the edge. <bookmark mark='d'/> A local quadratic, with the same window, follows the bend: "
            + say(d["robust"]["tau"], 2) + "."
        ) as vo:
            self.add(schol_tag())
            self.play(FadeIn(A), FadeIn(L), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(win), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(fl), Create(fr))
            self.play(FadeIn(J), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(ql), Create(qr), FadeIn(side[3]))
        self.clear_scene()

    def sensitivity(self):
        d = load("rd")["sens"]
        hs = np.asarray(d["h"], float)
        ll, lq = np.asarray(d["ll_tau"], float), np.asarray(d["lq_tau"], float)
        lls, lqs = np.asarray(d["ll_se"], float), np.asarray(d["lq_se"], float)
        A = axes([3, 35], [1, 5], x_length=7.6, y_length=4.2, xlabel=r"bandwidth $h$ (points)", ylabel=r"estimated jump",
                 xticks=[5, 15, 25, 35], yticks=[1, 2, 3, 4, 5], center=[-1.8, 0.2, 0])
        ax = A.ax
        b1 = band(ax, hs, ll - 1.645 * lls, ll + 1.645 * lls, MISSC, 0.15)
        b2 = band(ax, hs, lq - 1.645 * lqs, lq + 1.645 * lqs, BANDC, 0.15)
        c1, c2 = polyline(ax, hs, ll, MISSC, 3.5), polyline(ax, hs, lq, BANDC, 3.5)
        truth = DashedLine(ax.c2p(3, 3), ax.c2p(35, 3), color=TRUEC, stroke_width=2.5)
        side = fit_rows(VGroup(
            label(r"red: \ local linear, \ with 90\% bands", font_size=22, color=MISSC),
            label(r"green: \ local quadratic", font_size=22, color=BANDC),
            label(r"small $h$: \ less smoothing bias, \ more noise", font_size=22),
            label(r"large $h$: \ precise, \ biased", font_size=22, color=MISSC),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The choice of bandwidth is the choice of a bias-variance trade-off, Part "
            "twenty-nine's smoothing problem at a boundary. Here are the estimates at every bandwidth from three to "
            "thirty-five points, on all forty thousand school-leavers. <bookmark mark='b'/> A narrower window reduces"
            " smoothing bias but increases noise; it is not exactly unbiased. As the window widens it becomes precise"
            " and drifts away from the truth, and its interval drifts with it. <bookmark mark='c'/> The local "
            "quadratic stays near three much longer, at the price of width. <bookmark mark='d'/> A conventional "
            "interval at the mean-squared-error-optimal bandwidth is centred on a biased estimate by design: that "
            "bandwidth balances squared bias against variance, so bias remains material relative to the standard "
            "error under the usual leading-term expansion, even though its absolute size can vanish."
        ) as vo:
            self.add(schol_tag())
            self.play(FadeIn(A), Create(truth))
            vo.wait_until("b")
            self.play(FadeIn(b1), Create(c1), FadeIn(side[0]), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(b2), Create(c2), FadeIn(side[1]))
        self.clear_scene()

    def robust(self):
        rows = [
            cmath(r"\hat\tau_1(h) - \tau", r"\approx", r"B\, h^2 + \text{noise of SD} \propto (nh)^{-1/2}", font_size=30),
            cmath(r"h_{\text{MSE}}", r"\propto", r"n^{-1/5} \ \Rightarrow \ \text{bias} / \text{SD} \text{ stays } \tfrac12", font_size=30),
            cmath(r"\text{bias-corrected}", r":", r"\hat\tau_1 - \hat B h^2, \ \hat B \text{ from a local quadratic}", font_size=30),
            cmath(r"\text{robust SE}", r":", r"\text{include the noise in } \hat B", font_size=30),
        ]
        rows[2][-1].set_color(BANDC)
        whys = [why(r"Part 29"), why(r"the conventional CI undercovers"), why(r"Calonico, \ Cattaneo \& Titiunik (2014)"),
                why(r"with equal bandwidths: \ the local quadratic and its own SE")]
        with self.voiceover(
            "<bookmark mark='a'/> The arithmetic: the local linear estimate's bias grows like the square of the "
            "bandwidth, and its noise shrinks like one over the square root of n times h. <bookmark mark='b'/> The "
            "optimal bandwidth shrinks like n to the minus one fifth, and at it the bias stays half a standard "
            "deviation, however large the sample. Under this nonzero-curvature leading-term model, ignoring the bias "
            "gives asymptotic undercoverage. <bookmark mark='c'/> Sebastian Calonico, Matias Cattaneo and Rocio "
            "Titiunik's fix, in 2014, subtracts an estimate of the bias, using a local quadratic. <bookmark "
            "mark='d'/> And, crucially, widens the standard error to include the noise in that estimate. With the "
            "same bandwidth for both, the robust interval is exactly the local quadratic's estimate with its own "
            "standard error."
        ) as vo:
            intro=label('Bias correction includes uncertainty in the estimated bias',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def study(self):
        d = load("rd")["study"]
        rows = fit_rows(VGroup(
            label(r"one study: \ 2,000 school-leavers drawn from the World", font_size=26),
            label(rf"teaching bandwidth {d['h']:.1f}; \ conventional: \ {d['conv']['tau']:.2f}, \ 90\% CI {d['conv']['ci'][0]:.2f} to {d['conv']['ci'][1]:.2f}", font_size=26, color=MISSC),
            label(rf"robust bias-corrected: \ {d['robust']['tau']:.2f}, \ 90\% CI {d['robust']['ci'][0]:.2f} to {d['robust']['ci'][1]:.2f}", font_size=26, color=BANDC),
            label(r"wider, \ and centred elsewhere: \ the correction is not only a wider interval", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A single study of two thousand school-leavers. <bookmark mark='b'/> The conventional "
            "interval runs from " + say(d["conv"]["ci"][0], 1) + " to " + say(d["conv"]["ci"][1], 1) + ". <bookmark "
            "mark='c'/> The robust bias-corrected interval runs from " + say(d["robust"]["ci"][0], 1) + " to "
            + say(d["robust"]["ci"][1], 1) + ". <bookmark mark='d'/> It is wider, and centred somewhere else: the correction "
            "moves the estimate as well as widening the interval."
        ) as vo:
            self.add(schol_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def board(self):
        rows = board_rows("local linear RD", "robust bias-corrected")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Board, a thousand such studies. The conventional interval at the optimal "
                   "bandwidth covers the truth " + f"{100 * rows[0].achieved:.0f}" + " percent of the time: broken. "
                   "<bookmark mark='b'/> The robust bias-corrected interval covers it " + f"{100 * rows[1].achieved:.0f}"
                   + " percent of the time: kept.",
                   [("a", [0]), ("b", [1])])
