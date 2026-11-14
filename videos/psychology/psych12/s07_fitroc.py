from __future__ import annotations

import numpy as np
from scipy import stats

from videos.psychology.psych12.common import *  # noqa: F403
from videos.psychology.psych12.s04_roc import roc_axes


class FitRoc(VoiceoverScene):
    def construct(self):
        self.card()
        self.zspace()
        self.fit()
        self.memory()

    def card(self):
        card = chapter_card(6, r"Fitting an ROC", r"Are the two distributions really the same width?",
                            lit={1992: r"Ratcliff, Sheu and Gronlund"}, part=PART, scale=("mind",), marr=("what",))
        with self.voiceover(
            "Chapter six. Fitting an ROC."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def zspace(self):
        head = heading(r"In $z$ coordinates, \ an ROC is a straight line")
        R = roc_axes([-3.6, -0.2, 0], size=4.4)
        Zx = axes([-2.5, 2.5], [-2.5, 2.5], x_length=4.4, y_length=4.4, xticks=[-2, 0, 2], yticks=[-2, 0, 2],
                  xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"$z$(false-alarm rate)",
                  ylabel=r"$z$(hit rate)", center=[2.0, -0.2, 0])
        fa = np.linspace(0.005, 0.995, 200)
        eq = 1 - stats.norm.cdf(stats.norm.ppf(1 - fa) - 1.5)
        k = stats.norm.ppf(1 - fa)
        uq = 1 - stats.norm.cdf((k - 1.5) / 1.25)
        c1 = curve(R.ax, fa, eq, ROCC, stroke_width=4)
        c2 = curve(R.ax, fa, uq, SIGNALC, stroke_width=4)
        z1 = np.linspace(-2.5, 1.0, 40)
        z2 = np.linspace(-2.5, 1.625, 40)
        l1 = curve(Zx.ax, z1, z1 + 1.5, ROCC, stroke_width=4)
        l2 = curve(Zx.ax, z2, z2 / 1.25 + 1.5 / 1.25, SIGNALC, stroke_width=4)
        lg = legend([(ROCC, r"equal spreads: \ slope 1"), (SIGNALC, r"signal 1.25 times wider: \ slope 0.8")],
                    font_size=22).next_to(Zx, DOWN, buff=0.35)
        rows = rows_of([
            (r"take $z$ of both rates", WHITE),
            (r"slope $= 1/\sigma_s$: \ the noise's spread over the signal's", SIGNALC),
            (r"intercept $= d'/\sigma_s$", MODEL),
        ], 2.6, 25, 0.3).move_to([5.6, 0.4, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ $d' = 1.5$")
        with self.voiceover(
            "Everything so far assumed that the two distributions have the same width. That's a claim about the "
            "data, and an ROC can test it. <bookmark mark='a'/> Take the z score of both rates. In those "
            "coordinates an equal-variance ROC becomes a straight line with slope one. <bookmark mark='b'/> If the "
            "signal distribution is wider than the noise, the line is still straight, but its slope is the noise's "
            "spread divided by the signal's: a quarter wider gives a slope of point eight. "
            "<bookmark mark='c'/> And the intercept is d prime over that spread. So the slope of a z ROC measures "
            "something the yes-no task can't: whether signal evidence varies more than noise."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(R), Create(c1), Create(c2))
            vo.wait_until("a")
            self.play(FadeIn(Zx), Create(l1), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(l2), FadeIn(lg), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def fit(self):
        d = load("fitroc")
        head = heading(r"Fitting by maximum likelihood")
        Zx = axes([-2.3, 1.0], [-1.0, 1.8], x_length=5.0, y_length=4.2, xticks=[-2, -1, 0, 1], yticks=[-1, 0, 1],
                  xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"$z(F)$", ylabel=r"$z(H)$", center=[-3.6, -0.3, 0])
        ax = Zx.ax
        pts = VGroup(*[Dot(ax.c2p(float(a), float(b)), radius=0.08, color=YOU) for a, b in zip(d["zfa"], d["zhit"])])
        ze = np.linspace(max(-2.3, -1.0 - d["d_e"]), min(1.0, 1.8 - d["d_e"]), 40)
        b_u = d["d_u"] * d["slope_u"]
        zu = np.linspace(max(-2.3, (-1.0 - b_u) / d["slope_u"]), min(1.0, (1.8 - b_u) / d["slope_u"]), 40)
        eq = curve(ax, ze, ze + d["d_e"], RIVAL, stroke_width=3)
        uq = curve(ax, zu, zu * d["slope_u"] + b_u, MODEL, stroke_width=4)
        lg = legend([(RIVAL, r"equal spreads"), (MODEL, r"unequal spreads")], font_size=22).move_to(ax.c2p(-1.4, 1.55))
        rows = rows_of([
            (r"a rating study: \ 300 signal and 300 blank trials from an observer whose signal is 1.25 times wider", WHITE),
            (r"maximum likelihood on the counts, \ as in Part 11, \ two ways", MODEL),
            (rf"unequal: \ slope {d['slope_u']:.2f}, \ $d' = {d['d_u']:.2f}$ \ (planted: 0.80 and 1.25)", MODEL),
            (rf"equal spreads fit worse: \ likelihood-ratio $\chi^2 = {d['lr']:.1f}$, \ $p = {d['p']:.3f}$", RIVAL),
            (r"with ROC data you can test the assumption; \ with one pair of rates you cannot", THRESH),
        ], 5.6, 26, 0.26).move_to([3.4, -0.2, 0])
        keep_in_frame(rows)
        tag = simulated_tag(r"simulated: \ the middle of 41 studies by fitted slope")
        with self.voiceover(
            "Now fit one. Here's a rating study from an observer whose signal distribution is a quarter wider "
            "than its noise. Five points in z coordinates. <bookmark mark='a'/> Fit the model by maximum "
            "likelihood, as in Part 11, but now on six-category counts, and fit it two ways: forcing equal "
            "spreads, and letting them differ. <bookmark mark='b'/> The free fit finds a slope of "
            f"{d['slope_u']:.2f} and a d prime of {d['d_u']:.2f}, close to the planted point eight and one point "
            "two five. <bookmark mark='c'/> And the equal-spread model fits significantly worse. "
            "<bookmark mark='d'/> The moral: one pair of rates gives you d prime only if you assume equal spreads. "
            "A rating ROC lets you check."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(Zx), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.2),
                      FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(eq), Create(uq), FadeIn(lg), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def memory(self):
        d = load("fitroc")
        src = archive.RATCLIFF_1992
        head = heading(r"Memory's evidence is lopsided")
        A = axes([-3.5, 5.5], [0, 0.45], x_length=6.8, y_length=3.0, xticks=[-2, 0, 2, 4], yticks=[],
                 xfmt=lambda v: f"{v:g}", xlabel=r"how familiar the word feels", ylabel=r"", center=[-3.0, 0.2, 0])
        ax = A.ax
        g = gauss_pair(ax, 1.25, 1.25)
        ln = label(r"new words", font_size=24, color=NOISEC).move_to(ax.c2p(-2.0, 0.38))
        ls = label(r"studied words", font_size=24, color=SIGNALC).move_to(ax.c2p(3.6, 0.3))
        rows = rows_of([
            (rf"recognition memory: \ zROC slopes near {d['recognition_slope']:.1f}, \ study after study", DATA),
            (r"studied words vary more than new ones: \ some were learned well, \ some barely", SIGNALC),
            (r"or: \ part of memory is all-or-none recollection, \ added to graded familiarity (chapter 8)", RIVAL),
            (r"the slope is a fact; \ its meaning is argued. \ Part 21 returns to it", THRESH),
        ], 5.4, 27, 0.3).move_to([3.7, -0.1, 0])
        keep_in_frame(rows)
        tags = VGroup(published_tag(src.cite), psyche_tag(r"the curves: \ slope 0.8 drawn"))
        with self.voiceover(
            "This isn't a curiosity. In recognition memory, deciding whether a word was on a list, z ROC slopes "
            "come out near point eight, in experiment after experiment. Ratcliff, Sheu and Gronlund made the "
            "point sharply in 1992. <bookmark mark='a'/> The usual reading: the familiarity of studied words "
            "varies more than that of new ones, because some words were learned well and some barely at all. "
            "<bookmark mark='b'/> But there's a rival reading. Perhaps part of recognition is all-or-none, a "
            "sudden recollection of the word on the list, added to graded familiarity. That model bends the curve "
            "too. <bookmark mark='c'/> The slope is a fact. What it means is still argued, and chapter eight shows "
            "how the shape of an ROC is used to argue it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tags), FadeIn(A), Create(g.noise), Create(g.signal), FadeIn(ln), FadeIn(ls),
                      FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
