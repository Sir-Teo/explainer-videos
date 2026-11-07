from __future__ import annotations

import numpy as np

from videos.stats.stats13.common import *  # noqa: F403


class Principles(VoiceoverScene):
    def construct(self):
        self.card()
        self.systematic()
        self.randomized()
        self.replication()
        self.local_control()
        self.peirce()
        self.three()

    def card(self):
        card = chapter_card(1, r"Three principles", r"Replication, \ randomization, \ local control", lit=(1884, 1935), part=PART)
        with self.voiceover("Chapter one. Three principles."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def systematic(self):
        d = load("field")
        y = np.asarray(d["sys_y"])
        west = np.zeros((12, 12), int)
        west[:, 6:] = 1
        fp = field_from(np.asarray(d["fertility"]), cell=0.36, center=[-3.2, -0.2, 0], lo=43, hi=57)
        tags = fp.tags(west, names="AB", colors=[S.CTRL, S.TREAT], font_size=16)
        arrow = Arrow(fp.get_left() + DOWN * 2.6, fp.get_right() + DOWN * 2.6, buff=0, color=GREY_B, stroke_width=3)
        al = label(r"richer soil to the east", font_size=20, color=GREY_B).next_to(arrow, DOWN, buff=0.08)
        rows = fit_rows(VGroup(
            label(r"two varieties: \ B truly yields 2 bushels more than A, \ on every plot", font_size=24),
            label(r"the tidy layout: \ A on the west half, \ B on the east", font_size=24),
            MathTex(rf"\bar y_B - \bar y_A = {d['sys_est']:.1f}", font_size=34, color=RES),
            label(r"swap the halves: \ " + rf"${d['sys_flip']:.1f}$" + r", \ and A ``wins''", font_size=24, color=RES),
            label(r"it measures variety + soil, \ inseparably", font_size=26, color=OBS),
            label(r"confounding: \ no amount of replication fixes it", font_size=22, color=GREY_A),
        ), 5.4, 0.32, [3.7, 0.0, 0])
        tag = simulated_tag(r"the field-trial simulator", corner=DR)
        with self.voiceover(
            "Take our field, now painted by its hidden fertility, which no farmer can see. <bookmark mark='a'/> We want to "
            "compare two varieties of wheat, A and B. In truth, B yields two bushels per acre more than A, on every plot. "
            "<bookmark mark='b'/> The natural layout is tidy: A on the west half, B on the east, easy to sow and easy to "
            "harvest. <bookmark mark='c'/> The experiment reports that B beats A by seven point eight bushels. Nearly four "
            "times the truth. <bookmark mark='d'/> Swap the halves, and A wins by four point three. <bookmark mark='e'/> The "
            "comparison measures the variety plus the soil it happened to be sown on, and nothing in the data can pull the two "
            "apart. <bookmark mark='f'/> That's confounding, and it's not noise: a bigger field, laid out the same way, would "
            "give the same wrong answer more precisely."
        ) as vo:
            self.play(FadeIn(fp, lag_ratio=0.01), GrowArrow(arrow), FadeIn(al), FadeIn(tag), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(tags, lag_ratio=0.005), FadeIn(rows[1]), run_time=1.5)
            for k, m_ in enumerate("cdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2], shift=RIGHT * 0.2))
        self.clear_scene()

    def randomized(self):
        d = load("field")
        lay = np.asarray(d["layouts"][0])
        fp = field_from(np.asarray(d["fertility"]), cell=0.3, center=[-4.4, 0.9, 0], lo=43, hi=57)
        tags = fp.tags(lay, names="AB", colors=[S.CTRL, S.TREAT], font_size=13)
        ests = np.asarray(d["rand_ests"])
        A = axes([-2, 9], [0, 110], x_length=6.4, y_length=3.6, xlabel=r"estimated advantage of B", ylabel=r"layouts",
                 xticks=[0, 2, 4, 6, 8], yticks=[0, 50, 100], center=[2.6, 0.9, 0])
        ax = A.ax
        edges = np.arange(-2, 9.01, 0.25)
        h, _ = np.histogram(ests, edges)
        bars = hist_bars(ax, edges, h, color=SIM, opacity=0.8)
        tline = DashedLine(ax.c2p(2, 0), ax.c2p(2, 105), color=EXACT, stroke_width=3)
        sline = DashedLine(ax.c2p(d["sys_est"], 0), ax.c2p(d["sys_est"], 105), color=RES, stroke_width=3)
        tl = label(r"truth 2", font_size=20, color=EXACT).next_to(tline, UP, buff=0.08)
        sl = label(r"tidy layout", font_size=20, color=RES).next_to(sline, UP, buff=0.08)
        rows = fit_rows(VGroup(
            label(r"randomize: \ any 72 plots get B, \ chosen by lot", font_size=24),
            MathTex(rf"\text{{4,000 layouts (400 shown): \ mean }} {d['rand_mean']:.2f},\quad \text{{SD }} {d['rand_sd']:.2f}", font_size=28),
            label(r"the randomization distribution describes layout error", font_size=24, color=OBS),
            label(r"unbiased over the randomization, \ whatever the soil is like", font_size=22, color=GREY_A),
        ), 12.4, 0.24, [0, -2.85, 0])
        with self.voiceover(
            "Fisher's remedy. <bookmark mark='a'/> Let chance decide: choose the seventy-two plots that get variety B by "
            "lot, with dice, cards or a random number table, so that every plot has the same chance of either variety. "
            "Here is one such layout: untidy, and harder to sow. <bookmark mark='b'/> Now repeat the whole experiment on "
            "four thousand different random layouts. The estimates scatter, but around the truth: their average is one "
            "point nine nine, with a standard deviation of point seven one. The tidy layout's seven point eight is far out "
            "in the tail. <bookmark mark='c'/> Any one random layout still has an error, but the error is now chance, and "
            "chance has a distribution we can compute. That's the point. <bookmark mark='d'/> Over the randomization, the "
            "estimate is unbiased whatever the soil is like, even though no one has measured the soil."
        ) as vo:
            self.play(FadeIn(fp, lag_ratio=0.01))
            vo.wait_until("a")
            self.play(FadeIn(tags, lag_ratio=0.005), FadeIn(rows[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(A), Create(tline), FadeIn(tl))
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.03), FadeIn(rows[1]), run_time=2.5)
            self.play(Create(sline), FadeIn(sl))
            for k, m_ in enumerate("cd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def replication(self):
        d = load("field")
        rep = {int(k): v for k, v in d["replication"].items()}
        sig = d["effective_sigma"]
        A = axes([0, 75], [0, 7], x_length=7.0, y_length=4.4, xlabel=r"plots of each variety, \ $n$", ylabel=r"SD of the estimate",
                 xticks=[1, 8, 16, 36, 72], yticks=[0, 2, 4, 6], center=[-2.4, -0.2, 0])
        ax = A.ax
        ns = np.linspace(1, 74, 300)
        cv = curve(ax, ns, sig * np.sqrt(2 / ns), FIT, 3)
        pts = VGroup(*[Dot(ax.c2p(n, s_), radius=0.08, color=SIM) for n, s_ in sorted(rep.items())])
        rows = fit_rows(VGroup(
            label(r"replication: \ more plots per variety", font_size=24),
            MathTex(r"\mathrm{SD}(\bar y_B - \bar y_A) = \sigma\sqrt{2/n}", font_size=32, color=FIT),
            MathTex(rf"\sigma \approx {sig:.1f}\ \text{{bushels: one plot's own variation}}", font_size=26),
            MathTex(rf"n = 1:\ {rep[1]:.1f};\quad n = 72:\ {rep[72]:.2f}", font_size=28, color=SIM),
            label(r"replication does two jobs: \ it shrinks the error, \ and it measures it", font_size=24, color=OBS),
            label(r"with one plot each, \ there is no way to tell variety from plot", font_size=22, color=GREY_A),
        ), 5.0, 0.32, [4.3, 0.0, 0])
        with self.voiceover(
            "The first principle, replication; the plot noise is independent in this simulator. <bookmark mark='a'/> With one plot of each variety, the comparison is hopeless. "
            "<bookmark mark='b'/> With n plots of each, chosen at random, the standard deviation of the difference falls "
            "like sigma times the square root of two over n, Part 8's law. <bookmark mark='c'/> Here sigma combines finite-field fertility variation and independent plot noise: the effective variation of "
            "one plot, is about four point three bushels. <bookmark mark='d'/> The simulated dots follow the curve: six "
            "bushels of uncertainty with one plot each, point seven with seventy-two. <bookmark mark='e'/> And replication "
            "does a second job, which Fisher thought just as important: <bookmark mark='f'/> by comparing plots that got the "
            "same treatment, it measures the error, so the experiment carries its own yardstick."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cv), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(p_, scale=1.5) for p_ in pts], lag_ratio=0.2), FadeIn(rows[3]))
            for k, m_ in enumerate("ef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 4]))
        self.clear_scene()

    def local_control(self):
        d = load("field")
        g = np.random.Generator(np.random.PCG64(7))
        a = np.zeros((12, 12), int)
        coin = g.random((12, 6)) < 0.5
        a[:, 0::2] = coin
        a[:, 1::2] = ~coin
        fp = field_from(np.asarray(d["fertility"]), cell=0.34, center=[-3.4, -0.2, 0], lo=43, hi=57)
        frames = VGroup(*[fp.outline(r, r, 2 * j, 2 * j + 1, color=BLOCK, stroke_width=1.6) for r in range(12) for j in range(6)])
        tags = fp.tags(a, names="AB", colors=[S.CTRL, S.TREAT], font_size=15)
        rows = fit_rows(VGroup(
            label(r"local control: \ compare like with like", font_size=24),
            label(r"pair neighbouring plots, \ and toss a coin within each pair", font_size=24, color=BLOCK),
            label(r"neighbours share their soil, \ so the difference within a pair cancels it", font_size=24),
            MathTex(rf"\text{{SD: random}}\ {d['rand_sd']:.2f}\ \to\ \text{{paired}}\ {d['pair_sd']:.2f}", font_size=30, color=OBS),
            label(r"the same 144 plots, \ twice the precision: \ like quadrupling the field", font_size=24, color=OBS),
            label(r"randomization is still there: \ within each pair, \ by coin", font_size=22, color=GREY_A),
        ), 5.4, 0.32, [3.7, 0.0, 0])
        with self.voiceover(
            "The third principle, local control. <bookmark mark='a'/> Randomization makes the comparison fair, but the soil's "
            "variation is still in the error. You can remove much of it by comparing like with like. <bookmark mark='b'/> "
            "Pair each plot with its neighbour to the east, and within every pair toss a coin for which gets variety B. "
            "<bookmark mark='c'/> Neighbours share their soil, so within a pair the soil nearly cancels, and what's left is "
            "the variety, plus a little noise. <bookmark mark='d'/> The standard deviation of the estimate falls from point "
            "seven one to point three six. <bookmark mark='e'/> The same field, the same hundred and forty-four plots, twice "
            "the precision: as good as quadrupling the size of the experiment. <bookmark mark='f'/> And randomization hasn't "
            "gone away: it now works within each pair. Restrict the randomization to match the field, and analyse the way you "
            "randomized."
        ) as vo:
            self.play(FadeIn(fp, lag_ratio=0.01))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(frames, lag_ratio=0.01), FadeIn(rows[1]), run_time=2.0)
            self.play(FadeIn(tags, lag_ratio=0.005), run_time=1.5)
            for k, m_ in enumerate("cdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2], shift=RIGHT * 0.2))
        self.clear_scene()

    def peirce(self):
        hc = history_card(1884, r"Charles Sanders Peirce \ and \ Joseph Jastrow, \ Johns Hopkins",
                          r"``On small differences of sensation'': \ can a person feel a tiny change in a weight pressing on a finger? \ "
                          r"Whether each change was up or down was decided by drawing cards from a shuffled pack, \ and the "
                          r"subject could not see it", color=S.PRIOR, width=10.4, font_size=24).move_to([0, 1.1, 0])
        rows = fit_rows(VGroup(
            label(r"one of the earliest documented experiments randomized by a deliberate chance device", font_size=24),
            label(r"blinding and randomization together: \ the subject's guesses could not follow a pattern", font_size=24, color=S.PRIOR),
            label(r"Fisher (1926, \ 1935) \ made randomization the basis of the analysis itself", font_size=24, color=OBS),
        ), 12.4, 0.32, [0, -1.9, 0])
        intro = label('Random assignment predates Fisher', font_size=36)
        with self.voiceover(
            "Fisher wasn't the first to randomize. <bookmark mark='a'/> In 1884 the philosopher Charles Sanders Peirce and his "
            "student Joseph Jastrow tested whether a person could feel a tiny change in a weight pressing on a finger. To keep the "
            "subject from anticipating, they decided whether each change was up or down by drawing cards from a shuffled "
            "pack. <bookmark mark='b'/> It's an early documented experiment randomized on purpose, by a "
            "chance device, and it was blinded too. <bookmark mark='c'/> What Fisher added, forty years later, was the "
            "realization that the randomization is not just a safeguard. It is the probability model on which the analysis "
            "rests. That's the next chapter."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bc"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
            self.play(FadeIn(rows[2], shift=RIGHT * 0.2))
        self.clear_scene()

    def three(self):
        rows = [
            cmath(r"\text{replication}", r":", r"\mathrm{SD} = \sigma\sqrt{2/n}\ \text{, and an estimate of } \sigma", font_size=32),
            cmath(r"\text{randomization}", r":", r"\mathbb E_{\text{layout}}[\bar y_B - \bar y_A] = \tau", font_size=32),
            cmath(r"\text{local control}", r":", r"\sigma^2 \to \sigma^2_{\text{within block}}", font_size=32),
            cmath(r"\text{analyse as randomized}", r":", r"\text{the layout's chance is the model}", font_size=32),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"precision, \ and a yardstick for it"), why(r"assignment independent of potential outcomes"),
                why(r"blocks: \ remove what you know varies"), why(r"``block what you can, \ randomize what you cannot''")]
        intro = label('Replication, randomization and local control', font_size=36)
        with self.voiceover(
            "So, three principles. <bookmark mark='a'/> Replicate, to shrink the error and to measure it. "
            "<bookmark mark='b'/> Randomize, so that the expected estimate over all layouts is the true effect, tau, "
            "whatever confounders lurk, seen or unseen. <bookmark mark='c'/> Control locally, grouping similar units into "
            "blocks, so the error is only the variation within blocks. <bookmark mark='d'/> And analyse the experiment the way "
            "it was randomized. The modern summary, from George Box and his co-authors: block what you can, randomize what "
            "you cannot."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.65, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()
