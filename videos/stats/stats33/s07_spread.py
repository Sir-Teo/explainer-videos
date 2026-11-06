from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats33.common import *  # noqa: F403


class Spread(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_()
        self.hists()
        self.numbers()
        self.why_spread()
        self.widen()
        self.board()
        self.fdx()

    def card(self):
        card = chapter_card(6, r"FDR is an average", r"The false discovery proportion of one study", lit=(2001,), part=PART)
        with self.voiceover("Chapter six. The false discovery rate is an average."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def setup_(self):
        rows = [
            cmath(r"m = 1{,}000", r":", r"900 \text{ nulls}, \ 100 \text{ effects at } z = 2.5", font_size=30),
            cmath(r"\text{independent}", r":", r"\rho = 0", font_size=32),
            cmath(r"\text{equicorrelated}", r":", r"z_i = \sqrt{\rho}\, W + \sqrt{1 - \rho}\, \varepsilon_i, \ \rho = 0.5", font_size=30),
            cmath(r"\text{BH at } q = 0.1", r":", r"\text{2,000 studies each}", font_size=30),
        ]
        rows[2][-1].set_color(BHC)
        whys = [why(r"one-sided $z$-tests"), why(r"the textbook case"), why(r"one shared factor $W$: \ a batch effect"),
                why(r"the FDP of each")]
        with self.voiceover(
            "<bookmark mark='a'/> A simulation: a thousand one-sided tests, nine hundred true nulls and a hundred real "
            "effects of size two and a half. <bookmark mark='b'/> First with independent tests. <bookmark mark='c'/> Then "
            "with every pair of tests correlated one half, through one shared factor, like a batch effect that shifts every "
            "measurement in a study together. <bookmark mark='d'/> BH at ten percent, two thousand studies each way, "
            "recording the false discovery proportion of each study."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def hists(self):
        d = load("fdp")
        f0, f5 = np.asarray(d["0.0"]["fdp"]), np.asarray(d["0.5"]["fdp"])
        edges = np.linspace(0, 0.6, 31)
        w = edges[1] - edges[0]
        A1 = axes([0, 0.6], [0, 13], x_length=5.4, y_length=3.8, xlabel=r"FDP", ylabel=r"independent",
                  xticks=[0, 0.1, 0.2, 0.4, 0.6], yticks=[0, 5, 10], center=[-3.3, 0.6, 0])
        A2 = axes([0, 0.6], [0, 13], x_length=5.4, y_length=3.8, xlabel=r"FDP", ylabel=r"correlated, \ $\rho = 0.5$",
                  xticks=[0, 0.1, 0.2, 0.4, 0.6], yticks=[0, 5, 10], center=[3.3, 0.6, 0])
        h1 = hist_bars(A1.ax, edges, np.minimum(np.histogram(f0, edges)[0] / (len(f0) * w), 13), color=BHC, opacity=0.7)
        h2 = hist_bars(A2.ax, edges, np.minimum(np.histogram(f5, edges)[0] / (len(f5) * w), 13), color=BYC, opacity=0.7)
        q1 = DashedLine(A1.ax.c2p(0.1, 0), A1.ax.c2p(0.1, 12.5), color=SIGC, stroke_width=2)
        q2 = DashedLine(A2.ax.c2p(0.1, 0), A2.ax.c2p(0.1, 12.5), color=SIGC, stroke_width=2)
        foot = fit_rows(VGroup(
            label(rf"independent: \ mean {d['0.0']['fdr']:.3f}, \ tightly around $\pi_0 q = 0.09$", font_size=22, color=BHC),
            label(rf"correlated: \ mean {d['0.5']['fdr']:.3f}, \ but a spike at 0 and a long tail", font_size=22, color=BYC),
        ), 12.0, 0.2, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> With independent tests the false discovery proportions cluster tightly around the "
            "promised average, point oh nine. <bookmark mark='b'/> With correlated tests the average is even lower, point "
            "oh six, comfortably within the promise. But look at the shape: a spike at zero, from studies where the shared "
            "factor pushed everything down and few or no discoveries were made, and a long tail of studies where it pushed "
            "everything up and a third or more of the discoveries were false."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A1), FadeIn(A2), Create(q1), Create(q2))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in h1], lag_ratio=0.03), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in h2], lag_ratio=0.03), FadeIn(foot[1]))
        self.clear_scene()

    def numbers(self):
        d = load("fdp")
        a, b = d["0.0"], d["0.5"]
        hdr = [r"\textbf{2,000 studies}", r"\textbf{independent}", r"\textbf{$\rho = 0.5$}"]
        body = [[r"mean FDP \ (the FDR)", f"{a['fdr']:.3f}", f"{b['fdr']:.3f}"],
                [r"P(FDP $> 0.2$)", f"{100 * a['p_gt']:.1f}\\%", f"{100 * b['p_gt']:.1f}\\%"],
                [r"P(no discoveries)", f"{100 * a['p_zero']:.1f}\\%", f"{100 * b['p_zero']:.1f}\\%"],
                [r"discoveries: \ mean $\pm$ SD", rf"{a['R_mean']:.0f} $\pm$ {a['R_sd']:.0f}", rf"{b['R_mean']:.0f} $\pm$ {b['R_sd']:.0f}"]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=1.0, row_buff=0.32, colors=[GREY_A, None, FALSEC, None, None])
        for r in tb[1:]:
            r[1].set_color(BHC)
            r[2].set_color(BYC)
        tb.move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(r"same procedure, \ same average promise", font_size=22),
            label(r"under dependence, \ one study in eleven has more than twice the promised share of false discoveries", font_size=22, color=FALSEC),
        ), 12.0, 0.22, [0, -2.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In numbers. The averages are point oh nine and point oh six. But the chance that a study's "
            "list is more than twenty percent false, twice the promise, is under one percent with independence and nine "
            "percent with correlation. One correlated study in five makes no discoveries at all, and the number of "
            "discoveries has a standard deviation of eighty-seven, against eight. <bookmark mark='b'/> Same procedure, same "
            "average promise, <bookmark mark='c'/> very different guarantees for the one study you actually ran."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb))
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def why_spread(self):
        rows = [
            cmath(r"W \text{ large}", r":", r"\text{every } z \text{ shifted up: \ many nulls cross the line}", font_size=30),
            cmath(r"W \text{ small}", r":", r"\text{every } z \text{ shifted down: \ even real effects missed}", font_size=30),
            cmath(r"E(\text{FDP})", r"=", r"E_W[E(\text{FDP} \mid W)] \le \pi_0 q", font_size=32),
            cmath(r"\text{the average hides}", r":", r"\text{a mixture of very good and very bad studies}", font_size=30),
        ]
        rows[3][-1].set_color(FALSEC)
        whys = [why(r"an unlucky batch"), why(r"a lucky batch"), why(r"the promise is about the average"),
                why(r"Efron (2007): \ correlation and large-scale testing")]
        with self.voiceover(
            "<bookmark mark='a'/> Why? When the shared factor is large, every z-value is pushed up and many nulls cross the "
            "line together. <bookmark mark='b'/> When it is small, everything is pushed down and even the real effects are "
            "missed. <bookmark mark='c'/> The false discovery rate averages over the shared factor, so its promise survives. "
            "<bookmark mark='d'/> But the average hides a mixture of very good and very bad studies, as Efron emphasized in "
            "2007. The empirical null of chapter five is one remedy: it estimates the shift that this study's factor caused."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=33) if r.part == 33][:4]
        b = coverage_board(rows, lit_part=33, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> On the Board, as error rates, with a thousand studies each. No correction, every p below "
            "ten percent: a false discovery rate of fifty percent, broken. <bookmark mark='b'/> BH with independent tests: "
            "kept, at point oh nine. With correlated tests: conservative, point oh six five. <bookmark mark='c'/> BY: very "
            "conservative, one percent. The Board judges averages; the histograms remind us what an average hides."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            vo.wait_until("a")
            self.play(FadeIn(b.body[0]))
            vo.wait_until("b")
            self.play(FadeIn(b.body[1]), FadeIn(b.body[2]))
            vo.wait_until("c")
            self.play(FadeIn(b.body[3]))
        self.wait(1.0)
        self.clear_scene()

    def fdx(self):
        rows = fit_rows(VGroup(
            label(r"to control the FDP of your own study: \ $P(\text{FDP} > \gamma) \le \alpha$", font_size=26, color=BHC),
            label(r"the false discovery exceedance \ (Lehmann \& Romano 2005; \ Genovese \& Wasserman 2006)", font_size=26),
            label(r"or simultaneous bounds on the FDP of every list \ (Goeman \& Solari 2011)", font_size=26, color=GREY_A),
            label(r"stronger promises cost discoveries, \ as always", font_size=26, color=FALSEC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> If you care about your own study rather than the average, control the false discovery "
            "proportion directly: the probability that it exceeds some gamma at most alpha. <bookmark mark='b'/> Erich "
            "Lehmann and Joseph Romano, and Christopher Genovese and Larry Wasserman, built such procedures. "
            "<bookmark mark='c'/> Jelle Goeman and Aldo Solari went further, with confidence bounds on the false discovery "
            "proportion of every possible list at once, so the list can be chosen after looking. <bookmark mark='d'/> "
            "Stronger promises cost discoveries, as always."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def widen(self):
        rows = [
            cmath(r"z_i \mid W", r"\sim", r"N(\sqrt\rho W, 1 - \rho)", font_size=32),
            cmath(r"\text{one study}", r":", r"\text{the nulls' histogram is } N(\sqrt\rho W, 1 - \rho)", font_size=30),
            cmath(r"\text{the theoretical null}", r":", r"N(0, 1): \ \text{wrong in every single study}", font_size=30),
            cmath(r"\text{the empirical null}", r":", r"\text{estimates } (\sqrt\rho W, \sqrt{1 - \rho}) \text{ from the middle}", font_size=28),
        ]
        rows[3][-1].set_color(BHC)
        whys = [why(r"conditional on the batch"), why(r"shifted and narrowed"), why(r"right only on average"), why(r"chapter five's remedy")]
        with self.voiceover(
            "<bookmark mark='a'/> Seen from inside one study, given the shared factor, each null z-value is normal "
            "with mean root rho times W and variance one minus rho. <bookmark mark='b'/> So the histogram of the nulls "
            "in this study is shifted by the batch and narrower than the standard normal. <bookmark mark='c'/> The "
            "theoretical null is therefore wrong in every individual study, and right only on average over studies. "
            "<bookmark mark='d'/> The empirical null of chapter five estimates the shift and the width from the middle "
            "of this study's own histogram, which is why Efron recommends it whenever correlation is suspected."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
