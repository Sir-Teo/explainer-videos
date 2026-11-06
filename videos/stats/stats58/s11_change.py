from __future__ import annotations

import numpy as np

from videos.stats.stats58.common import *  # noqa: F403


class Change(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter ten. Change detection: when the question is not whether, but when, something changed.",
                       10, r"Change detection", r"Raise the alarm, \ not too often", lit=(1954,))
        self.cusum()
        self.why()
        self.arl()
        self.lorden()
        self.nile_chart()
        self.bocpd()
        self.bocpd_chart()
        self.compare()

    def cusum(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Ewan Page's cumulative sum, from 1954, for a process that may shift from mean mu nought to "
            "mu one at an unknown time. Add up the log likelihood ratios, but never let the total fall below zero. <bookmark "
            "mark='b'/> While nothing has changed, the increments have negative mean and the sum keeps resetting to zero. "
            "<bookmark mark='c'/> After the change they have positive mean, and the sum climbs. <bookmark mark='d'/> Raise "
            "the alarm when it crosses a threshold h: an SPRT restarted every time it would have accepted the null.",
            [(r"W_t", r"=", r"\max\{0, \ W_{t-1} + \log\tfrac{f_1(X_t)}{f_0(X_t)}\}", 38),
             (r"\text{before the change}", r":", r"\text{drift } -\mathrm{KL}(f_0 \,\|\, f_1): \ \text{resets to } 0", 38),
             (r"\text{after}", r":", r"\text{drift } +\mathrm{KL}(f_1 \,\|\, f_0): \ \text{climbs}", 38),
             (r"\text{alarm}", r":", r"W_t \ge h", 40)],
            [r"Page (1954)", r"held at zero", r"evidence accumulates", r"a restarted SPRT"],
            colors=[(0, CHANGEC), (3, FIXEDC)])

    def why(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Why the reset? The likelihood ratio for a change at time k, against no change, is the "
            "product of the increments from k onwards. <bookmark mark='b'/> The best change point is the one that maximizes "
            "it: the maximum over k of the sum from k to t. <bookmark mark='c'/> That maximum obeys exactly the CUSUM "
            "recursion: either the best change is the old one, extended by one step, or it starts afresh now. <bookmark "
            "mark='d'/> So CUSUM is a generalized likelihood-ratio test over the unknown change time, computed in constant "
            "memory.",
            [(r"\text{change at } k", r":", r"\textstyle\sum_{i = k}^t \log\frac{f_1}{f_0}(X_i)", 38),
             (r"\text{best } k", r":", r"\max_{k \le t+1} \textstyle\sum_{i = k}^t \cdots", 38),
             (r"\text{recursion}", r":", r"= \max\{0, \ W_{t-1} + \text{today}\}", 38),
             (r"\text{so}", r":", r"\text{a GLR over the change time, \ constant memory}", 38)],
            [r"Part 22's ratio", r"maximize over $k$", r"extend or restart", r"elegant"],
            colors=[(2, CHANGEC)])

    def arl(self):
        d = load("arl")
        R = d["rows"]
        hdr = [r"threshold $h$", r"ARL$_0$: \ false alarm every", r"ARL$_1$: \ delay after a 1-SD shift"]
        body = [[f"{r['h']:g}", f"{r['arl0']:.0f}", f"{r['arl1']:.1f}"] for r in R]
        tab = table_rows([hdr] + body, font_size=30, col_buff=1.0, row_buff=0.3, colors=[GREY_B] + [WHITE] * len(R)).move_to([0, 0.7, 0])
        foot = fit_rows(VGroup(
            label(r"CUSUM for a shift from $N(0, 1)$ to $N(1, 1)$; \ simulated", font_size=24, color=GREY_A),
            label(r"each step of $h$ multiplies the time between false alarms by about $e$; \ the delay grows only by a step", font_size=24, color=CHANGEC),
        ), 12.4, 0.25, [0, -2.2, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A change detector has two numbers: the average run length to a false alarm when nothing "
            f"changes, and the average delay after a real change. <bookmark mark='b'/> For a one-standard-deviation shift: "
            f"with h of two, a false alarm every {R[0]['arl0']:.0f} observations and a delay of {say(R[0]['arl1'], 1)}; with h of "
            f"five, a false alarm every {R[-1]['arl0']:.0f}, and a delay of {say(R[-1]['arl1'], 1)}. <bookmark mark='c'/> Each "
            f"unit of h multiplies the time between false alarms by roughly e, and adds a step or two of delay: delay grows "
            f"only like the log of the false-alarm time."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[1:]], lag_ratio=0.25), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def lorden(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Gary Lorden's criterion, from 1971: judge a detector by its worst-case delay, over the "
            "change time and over the history before it, given a lower bound gamma on the false-alarm run length. <bookmark "
            "mark='b'/> He showed that CUSUM is asymptotically optimal: as gamma grows, its worst delay is log gamma over the "
            "Kullback–Leibler divergence, and nothing does better. <bookmark mark='c'/> George Moustakides proved in 1986 "
            "that it is exactly optimal for Lorden's criterion. <bookmark mark='d'/> The divergence sets the clock again, as "
            "it did for the SPRT: detection takes log of the false-alarm time over the information per observation.",
            [(r"\text{Lorden}", r":", r"\min \sup_{\nu}\operatorname{ess\,sup} E_\nu[(\tau - \nu)^+ \mid \mathcal F_\nu] \text{ s.t. } E_\infty\tau \ge \gamma", 32),
             (r"\text{CUSUM}", r":", r"\text{delay} \sim \log\gamma / \mathrm{KL}(f_1 \,\|\, f_0)", 38),
             (r"\text{exactly}", r":", r"\text{optimal for every } \gamma", 38),
             (r"\text{reading}", r":", r"\text{delay} = \log(\text{false-alarm time}) / \text{information}", 36)],
            [r"Lorden (1971)", r"asymptotically optimal", r"Moustakides (1986)", r"the divergence as a clock"],
            colors=[(1, CHANGEC), (2, CSC)])

    def nile_chart(self):
        d = load("nile")
        yrs = np.asarray(d["years"])
        flow = np.asarray(d["flow"])
        W = np.asarray(d["W"])
        A = axes([1870, 1971], [400, 1450], x_length=5.6, y_length=3.4, xlabel=r"year", ylabel=r"Nile flow at Aswan \ ($10^8$ m$^3$)",
                 xticks=[1880, 1920, 1960], yticks=[500, 1000], center=[-3.4, 0.6, 0])
        wmax = float(np.ceil(max(d["W"]) / 10) * 10)
        B = axes([1870, 1971], [0, wmax], x_length=5.6, y_length=3.4, xlabel=r"year", ylabel=r"CUSUM $W_t$ \ (shift of $-1$ SD)",
                 xticks=[1880, 1920, 1960], yticks=[0, wmax / 2, wmax], yfmt=lambda v: f"{v:.0f}", center=[3.4, 0.6, 0])
        series = VGroup(polyline(A.ax, yrs, flow, S.DATA, 2.5), *[Dot(A.ax.c2p(a, b), radius=0.035, color=S.DATA) for a, b in zip(yrs, flow)])
        pre = DashedLine(A.ax.c2p(1871, d["pre_mean"]), A.ax.c2p(1898, d["pre_mean"]), color=GREY_B, stroke_width=2)
        post = DashedLine(A.ax.c2p(1899, d["post_mean"]), A.ax.c2p(1970, d["post_mean"]), color=GREY_B, stroke_width=2)
        cus = polyline(B.ax, yrs, W, CHANGEC, 3)
        hline = DashedLine(B.ax.c2p(1870, d["h"]), B.ax.c2p(1971, d["h"]), color=FIXEDC, stroke_width=2)
        alarm = Dot(B.ax.c2p(d["alarm_year"], W[list(yrs).index(d["alarm_year"])]), radius=0.09, color=FIXEDC)
        foot = fit_rows(VGroup(
            label(rf"standardized by 1871--1898: \ mean {d['mu0']:.0f}, \ SD {d['sd']:.0f}; \ CUSUM for a 1-SD drop, \ $h = {d['h']:g}$", font_size=24, color=GREY_A),
            label(rf"alarm in {d['alarm_year']}; \ the mean fell from {d['pre_mean']:.0f} to {d['post_mean']:.0f} around 1899", font_size=24, color=CHANGEC),
        ), 12.4, 0.22, [0, -2.7, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A real change: the Nile's annual flow at Aswan, a hundred years from 1871. <bookmark "
            f"mark='b'/> Around 1899 the mean fell, from about {d['pre_mean']:.0f} to about {d['post_mean']:.0f}, as the climate "
            f"turned drier and the first Aswan dam was begun. <bookmark mark='c'/> A CUSUM, standardized by the first "
            f"twenty-eight years and tuned to a drop of one standard deviation, stays near zero, then climbs. <bookmark "
            f"mark='d'/> It crosses its threshold of four in {d['alarm_year']}, two years after the change, and then keeps "
            f"climbing: the new regime is permanent."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), FadeIn(museum_tag(r"Cobb (1978); \ Durbin \& Koopman")))
            vo.wait_until("a")
            self.play(Create(series), FadeIn(foot[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(pre), Create(post))
            vo.wait_until("c")
            self.play(Create(hline), Create(cus), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(alarm, scale=0.5), FadeIn(foot[1]))
        self.clear_scene()

    def bocpd(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A Bayesian alternative: Ryan Adams and David MacKay's online changepoint detection, from "
            "2007. Track the run length: how long since the last change. <bookmark mark='b'/> Each new observation either "
            "extends the current run, with probability one minus the hazard, or starts a new one. <bookmark mark='c'/> The "
            "posterior over the run length updates by one line of Bayes's rule, using each run's posterior predictive "
            "density. <bookmark mark='d'/> No threshold is needed: the whole posterior is reported, and a change shows as a "
            "shift of mass to short runs.",
            [(r"r_t", r"=", r"\text{time since the last change}", 40),
             (r"r_t", r"\in", r"\{r_{t-1} + 1, \ 0\}: \ \text{prob. } 1 - H, \ H", 38),
             (r"P(r_t \mid x_{1:t})", r"\propto", r"\textstyle\sum_{r_{t-1}} P(r_t \mid r_{t-1})\,p(x_t \mid r_{t-1})\,P(r_{t-1} \mid x_{1:t-1})", 32),
             (r"\text{output}", r":", r"\text{the run-length posterior, \ no threshold}", 38)],
            [r"Adams \& MacKay (2007)", r"a hazard rate", r"one line of Bayes", r"a whole posterior"],
            colors=[(2, POSTC)])

    def bocpd_chart(self):
        d = load("nile")
        yrs = np.asarray(d["years"])
        R = np.asarray(d["R_top"])  # [time, run length]
        T, L = R.shape
        A = axes([1870, 1971], [0, L], x_length=8.0, y_length=4.4, xlabel=r"year", ylabel=r"run length \ (years since the last change)",
                 xticks=[1880, 1900, 1920, 1940, 1960], yticks=[0, 20, 40], center=[-2.0, 0.2, 0])
        ax = A.ax
        cells = VGroup()
        for t in range(0, T, 1):
            for r in range(0, L, 2):
                v = float(R[t, r:r + 2].sum())
                if v < 0.03:
                    continue
                c = Rectangle(width=abs(ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]), height=abs(ax.c2p(0, 2)[1] - ax.c2p(0, 0)[1]),
                              stroke_width=0, fill_color=CHANGEC, fill_opacity=min(1.0, 0.15 + 0.85 * v))
                c.move_to(ax.c2p(yrs[t], r + 1))
                cells.add(c)
        cp = d["final_cp"]
        line = DashedLine(ax.c2p(cp, 0), ax.c2p(cp, L), color=FIXEDC, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"shade: \ posterior probability of each run length", font_size=22),
            label(r"hazard $1/100$; \ each segment's mean has a normal prior", font_size=22, color=GREY_A),
            label(rf"the mass resets around 1899; \ by 1970 the most probable last change is {cp}", font_size=22, color=CHANGEC),
            label(r"the run length then grows by a year a year: \ no further change", font_size=22, color=GREY_A),
        ), 4.4, 0.38, [4.6, 0.3, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The run-length posterior on the Nile. Each column is a year; the shade shows the posterior "
            f"probability of each run length. <bookmark mark='b'/> The hazard is one in a hundred, and each segment's mean has "
            f"a normal prior. <bookmark mark='c'/> Until 1898 the mass climbs the diagonal: one long run. Around 1899 it "
            f"collapses to short runs, and by 1970 the most probable time of the last change is {cp}. <bookmark mark='d'/> "
            f"After that the mass climbs the diagonal again: no further change in seventy years."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"Cobb (1978); \ Durbin \& Koopman")))
            vo.wait_until("a")
            self.play(FadeIn(cells, lag_ratio=0.002), FadeIn(side[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(line), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def compare(self):
        self.list_voiceover(
            "<bookmark mark='a'/> Two philosophies of change. <bookmark mark='b'/> CUSUM: a frequentist alarm, with a "
            "controlled false-alarm rate and optimal delay, for a known pre- and post-change law. <bookmark mark='c'/> Online "
            "Bayesian detection: a posterior over when the change happened, for unknown segment parameters. <bookmark "
            "mark='d'/> Recent work joins them to this part's theme: e-detectors, which run a test martingale from every "
            "possible change time and alarm when any of them is rich, with false-alarm guarantees and no model of what comes "
            "after the change.",
            [(r"two philosophies of change:", GREY_A),
             (r"CUSUM: \ false alarms controlled, \ optimal delay, \ known laws", CHANGEC),
             (r"online Bayes: \ a posterior over the change time, \ unknown parameters", POSTC),
             (r"e-detectors: \ a test martingale from every possible start", WEALTHC)])
