from __future__ import annotations

import numpy as np

from explainer.stats.board import Row, coverage_board, load_all
from videos.stats.stats10.common import *  # noqa: F403


class Peeking(VoiceoverScene):
    def construct(self):
        self.card()
        self.paths()
        self.climb()
        self.history()
        self.board()

    def card(self):
        card = chapter_card(10, r"The peeking problem", r"Look after every observation, \ stop when $p < 0.05$", lit=(1945,), part=PART)
        with self.voiceover("Chapter ten. The peeking problem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def paths(self):
        d = load("peeking")
        paths = np.asarray(d["paths"])
        crit = np.asarray(d["crit"])
        n = np.arange(1, 201)
        A = axes([0, 200], [-4, 4], x_length=9.6, y_length=4.4, xlabel=r"observations so far, \ $n$", ylabel=r"the running $t$ statistic",
                 xticks=[10, 50, 100, 150, 200], yticks=[-4, -2, 0, 2, 4], center=[-0.6, 0.2, 0])
        ax = A.ax
        keep = n >= 10
        up = polyline(ax, n[keep], crit[keep], REJ, 2.5)
        dn = polyline(ax, n[keep], -crit[keep], REJ, 2.5)
        cols = [SIM, S.POST, S.PRIOR, ALTC, S.TREAT, GREY_A]
        lines = VGroup()
        stops = VGroup()
        for i in range(len(paths)):
            t = paths[i]
            lines.add(polyline(ax, n[keep], t[keep], cols[i % len(cols)], 2.0))
            hit = np.flatnonzero(keep & (np.abs(paths[i]) > crit))
            if len(hit):
                j = hit[0]
                stops.add(Dot(ax.c2p(n[j], paths[i][j]), radius=0.09, color=OBS))
        rows = fit_rows(VGroup(
            label(r"$H_0$ is true: \ every crossing is a false alarm", font_size=24, color=GREY_A),
            label(r"stop at the first crossing, \ and report $p < 0.05$", font_size=26, color=OBS),
        ), 12.6, 0.25, [0, -2.9, 0])
        tag = simulated_tag(r"simulated: \ standard normal data", corner=UR)
        with self.voiceover(
            "Here's a habit that seems harmless. <bookmark mark='a'/> An experimenter collects data one observation at a "
            "time, and after every new observation, from the tenth on, runs a t-test. The red lines are the five "
            "percent critical values. <bookmark mark='b'/> Each wandering line is the t statistic of one experiment as "
            "the data accumulate, and in every one of them the null is true: the data are pure noise. "
            "<bookmark mark='c'/> But the paths wander, and some of them touch a red line. <bookmark mark='d'/> If the "
            "experimenter stops at the first crossing and reports p less than point zero five, every one of these is a "
            "false alarm. Each individual test had a five percent error rate. The procedure doesn't."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(up), Create(dn))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3), run_time=4.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(stops, scale=1.6), FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def climb(self):
        d = load("peeking")
        curve_ = np.asarray(d["curve"])
        ns = np.arange(d["start"], d["N"] + 1)
        A = axes([10, 500], [0, 0.5], x_length=7.4, y_length=4.4, xlabel=r"the largest $n$ the experimenter will wait for",
                 ylabel=r"chance of ever reaching $p < 0.05$", xticks=[10, 100, 200, 300, 400, 500], yticks=[0, 0.05, 0.2, 0.3, 0.4, 0.5],
                 center=[-2.0, -0.3, 0])
        ax = A.ax
        cv = polyline(ax, ns, curve_, OBS, 3.5)
        nominal = DashedLine(ax.c2p(10, 0.05), ax.c2p(500, 0.05), color=GREY_B, stroke_width=1.5)
        ev = d["ever"]
        dots = VGroup(*[Dot(ax.c2p(int(k), v), radius=0.07, color=REJ) for k, v in ev.items() if int(k) >= 10])
        rows = fit_rows(VGroup(
            MathTex(rf"n \le 20:\ {100 * ev['20']:.0f}\%,\ \ 50:\ {100 * ev['50']:.0f}\%,\ \ 100:\ {100 * ev['100']:.0f}\%,\ \ 500:\ {100 * ev['500']:.0f}\%",
                    font_size=26, color=REJ),
            label(rf"looking only every 10th observation, \ up to 100: \ {100 * d['every10_to100']:.0f}\%", font_size=24),
            label(r"wait long enough and the rate goes to 100\%: \ the law of the iterated logarithm (Part 44)", font_size=24, color=OBS),
            label(r"``sampling to a foregone conclusion''", font_size=24, color=GREY_A),
        ), 5.2, 0.34, [4.3, -0.3, 0])
        tag = simulated_tag(r"simulated: \ 10,000 experiments", corner=UR)
        with self.voiceover(
            "How bad is it? <bookmark mark='a'/> Simulate ten thousand experiments under the null, each peeking after "
            "every observation, and count how often p ever dips below point zero five. <bookmark mark='b'/> Willing to "
            "go to twenty observations, the false-positive rate is thirteen percent. To fifty, twenty-two. To a hundred, "
            "twenty-nine. To five hundred, forty-two percent. <bookmark mark='c'/> Peeking less often helps only a "
            "little: looking every tenth observation, up to a hundred, still gives twenty percent. "
            "<bookmark mark='d'/> And the curve never levels off. By the law of the iterated logarithm, a random walk "
            "eventually crosses any boundary that grows like root n, so a patient enough experimenter is certain to "
            "reach significance under a true null. Statisticians call it sampling to a foregone conclusion."
        ) as vo:
            self.play(FadeIn(A), Create(nominal), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(cv), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(dots), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2:]))
        self.clear_scene()

    def history(self):
        h1 = history_card(1945, r"Abraham Wald, \ US wartime research", r"the sequential probability ratio test: \ look as often as you "
                          r"like, \ with boundaries designed for it", color=ALTC, width=6.0, font_size=22).move_to([-3.3, 1.0, 0])
        h2 = history_card(1969, r"P. Armitage, \ C. McPherson \& B. Rowe, \ \emph{JRSS A}", r"``Repeated significance tests on "
                          r"accumulating data'': \ the false-positive rate of naive peeking, \ computed", color=ALTC, width=6.0,
                          font_size=22).move_to([3.3, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"group-sequential trials: \ Pocock (1977), \ O'Brien \& Fleming (1979): \ a few planned looks, \ stricter boundaries",
                  font_size=24, color=GREY_A),
            label(r"anytime-valid inference: \ $p$-values you may check every second \ (Part 58)", font_size=24, color=OBS),
        ), 12.6, 0.3, [0, -1.9, 0])
        intro = label('Sequential tests need sequential error control', font_size=36)
        with self.voiceover(
            "The problem has solutions, and they're old. <bookmark mark='a'/> During the war, Abraham Wald invented the "
            "sequential probability ratio test, designed from the start to be checked after every observation, with "
            "boundaries that account for it. <bookmark mark='b'/> In 1969 Peter Armitage and his colleagues computed "
            "the damage done by naive repeated testing, in a paper whose lessons medical trials took to heart. "
            "<bookmark mark='c'/> Clinical trials now use group-sequential designs, with a few planned looks at the "
            "data and stricter boundaries at each, from Stuart Pocock and from Peter O'Brien and Thomas Fleming. "
            "<bookmark mark='d'/> And the newest answer, anytime-valid inference, gives p-values and intervals you may "
            "check as often as you like. That's Part 58."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(h1, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(h2, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def board(self):
        rows = load_all(upto=10)
        b = coverage_board(rows, lit_part=10, placeholders=1, font_size=18, row_h=0.42)
        b.scale_to_fit_height(min(b.height, 7.4)).move_to(ORIGIN)
        mine = [i for i, r in enumerate(rows) if r.part == 10]
        with self.voiceover(
            "Time to add Part 10's promises to the Coverage Board. For a test, the board records its size: how often "
            "it rejects a true null, which should be five percent. <bookmark mark='a'/> Student's pooled t on two "
            "samples of ten men's heights: five point oh four percent. Kept. <bookmark mark='b'/> The same test when the "
            "group of ten is nearly three times as spread out as the group of forty: twenty-three point six percent. "
            "Broken. <bookmark mark='c'/> Welch's test in the same setting: five point one five. Kept. "
            "<bookmark mark='d'/> A t-test peeked at after every observation from ten to a hundred: twenty-nine percent. "
            "Badly broken. These World-height tests are approximate individually; the earlier normal-data simulation shows the same failure even when every fixed-sample test is exact. <bookmark mark='e'/> And a permutation test "
            "on samples of eight of the World's skewed incomes: four point eight five percent. Kept, under exchangeability, with the plus-one Monte Carlo p-value correction and no parametric shape assumption. Five rows, two of them broken by habits rather than by mathematics."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend), *[FadeIn(b.body[i]) for i in range(len(b.body)) if i not in mine])
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                if k < len(mine):
                    self.play(FadeIn(b.body[mine[k]], shift=RIGHT * 0.2))
        self.wait(1.0)
        self.clear_scene()
