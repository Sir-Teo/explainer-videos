from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import HIST, MEAS, TEST, TRAIN, chapter, curve, load, log_axes

FAST, SLOW = C.MODEL_Q, C.TRUE_P


class MoreDescents(VoiceoverScene):
    def construct(self):
        chapter(self, 13, r"Double descent in samples and in epochs", r"Can more data, or more training, hurt?",
                "Chapter thirteen. Double descent in samples, and in epochs.", lit=(2019,))
        self.samples()
        self.epochs()

    # ------------------------------------------------------------------
    def samples(self):
        s = load("samplewise")
        ns, med, lo, hi, rd = (np.asarray(s[k], float) for k in ("ns", "med", "lo", "hi", "ridge"))
        p = int(s["p"])
        ylo, yhi = -1.0, 1.5
        G = log_axes((math.log10(ns[0]), math.log10(ns[-1])), (ylo, yhi), x_length=8.0, y_length=4.4,
                     xticks=[math.log10(v) for v in (20, 50, 100, 200, 448)], xfmt=lambda v: f"{10 ** v:.0f}",
                     yticks=[-1, 0, 1], xlabel=r"$n$: \ training pages", ylabel=r"squared error on new pages",
                     center=(-1.2, -0.6, 0))
        ax = G.ax
        lx = np.log10(ns)
        bd = band(ax, lx, np.clip(np.log10(lo), ylo, yhi), np.clip(np.log10(hi), ylo, yhi), TEST, 0.18)
        cm = curve(ax, lx, np.clip(np.log10(med), ylo, yhi), TEST, 4)
        cr = curve(ax, lx, np.clip(np.log10(rd), ylo, yhi), C.INTERVAL, 3)
        pl = DashedLine(ax.c2p(math.log10(p), ylo), ax.c2p(math.log10(p), yhi), color=WHITE, stroke_width=1.5)
        pll = label(rf"$n = p = {p}$", font_size=22).next_to(pl.get_top(), RIGHT, buff=0.1)
        key = legend([(TEST, r"minimum-norm fit: \ median, \ quartiles of $20$ subsets"),
                      (C.INTERVAL, r"with ridge")], font_size=20).to_corner(UR, buff=0.35)
        head = label(rf"${p}$ random features, \ fixed; \ more and more pages", font_size=28).to_corner(UL, buff=0.35)
        k = int(np.argmax(med))
        j = int(np.argmin(med[:k])) if k > 0 else 0
        worse = bool(s["worse"]) and med[k] > med[j]
        with self.voiceover(
            "If the peak sits where the number of parameters equals the number of examples, then it can be reached "
            f"from the other side too. Fix {p} random features, and give the model more and more pages. "
            "<bookmark mark='a'/> "
            + (f"From {int(ns[j])} pages to {int(ns[k])}, the error on new pages rises, from {med[j]:.2f} to "
               f"{med[k]:.1f}: more data made the model worse, because more pages push it toward the point where it "
               "can only just fit them. <bookmark mark='b'/> Beyond that, more data helps again. "
               if worse else
               "The error doesn't rise here; more data helps throughout. <bookmark mark='b'/> ")
            + "<bookmark mark='c'/> With a little ridge, the curve simply falls. Nakkiran and colleagues found this "
            "sample-wise version in deep networks in 2019: for a fixed model, there's a range where more data hurts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(G), Create(pl), FadeIn(pll))
            vo.wait_until("a")
            self.play(FadeIn(bd), Create(cm), FadeIn(key[0]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(cr), FadeIn(key[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def epochs(self):
        e = load("epochwise")
        ts = np.asarray(e["ts"], float)
        med, lo, hi = np.asarray(e["med"]), np.asarray(e["lo"]), np.asarray(e["hi"])
        fast, slow, tr = np.asarray(e["fast"]), np.asarray(e["slow"]), np.asarray(e["train"])
        noise = float(e["noise"])
        i1, i2 = int(e["i1"]), int(e["i2"])
        G = log_axes((0, math.log10(ts[-1])), (-1, 1), x_length=7.4, y_length=4.4, xticks=[0, 2, 4, 6],
                     yticks=[-1, 0, 1], xlabel=r"gradient descent steps", ylabel=r"error on new data",
                     center=(-2.0, -0.5, 0))
        ax = G.ax
        lt = np.log10(ts)

        def ly(v):
            return np.clip(np.log10(np.maximum(v, 1e-1)), -1, 1)

        bd = band(ax, lt, ly(lo), ly(hi), TEST, 0.15)
        cm = curve(ax, lt, ly(med), TEST, 4.5)
        cf = curve(ax, lt, ly(fast + noise), FAST, 2.5)
        cs = curve(ax, lt, ly(slow + noise), SLOW, 2.5)
        ct = curve(ax, lt, ly(tr), TRAIN, 2.5)
        key = legend([(TEST, r"test error \ (median, quartiles, $20$ draws)"), (TRAIN, r"training error"),
                      (FAST, r"error from the fast directions"), (SLOW, r"error from the slow directions")], font_size=19)
        key.to_corner(UR, buff=0.3)
        d1 = Dot(ax.c2p(lt[i1], ly(med[i1])), radius=0.08, color=TEST)
        d2 = Dot(ax.c2p(lt[i2], ly(med[i2])), radius=0.08, color=TEST)
        setup = label(rf"a linear model: \ ${e['d1']}$ directions of variance $1$, \ ${e['d2']}$ of variance $0.0003$; "
                      rf"\ $n = {e['n']}$ \ (illustrative)", font_size=21, color=GREY_A).to_edge(DOWN, buff=0.25)
        dbl = bool(e["double"])
        hist = history_card(2021, r"R.~Heckel \& F.~F.~Yilmaz", r"epoch-wise double descent as two bias--variance "
                            r"curves on different time scales", width=4.6, font_size=17, color=HIST)
        hist.next_to(key, DOWN, buff=0.25).align_to(key, RIGHT)
        with self.voiceover(
            "Nakkiran and colleagues also saw it in time: train a network longer and longer, and its test error can "
            "fall, rise, and fall again. The simplest model that does this is linear, with inputs on two very "
            "different scales. <bookmark mark='a'/> Gradient descent learns the large-scale directions first. "
            + (f"The test error falls, to its first low at step {int(ts[i1])}, <bookmark mark='b'/> then rises, to "
               f"a peak around step {int(ts[i2]):,}, as those fast directions finish fitting their share of the "
               "noise, and of signal they can't represent. <bookmark mark='c'/> Only then do the slow directions, "
               f"which hold the rest of the signal, get learned, and the error falls again, to {med[-1]:.2f}, far below "
               "the first low. "
               if dbl else
               "<bookmark mark='b'/> Here the error falls without a second rise. <bookmark mark='c'/> ")
            + "<bookmark mark='d'/> Split by direction, it's two bias-variance curves, one fast, one slow, added "
            "together: Heckel and Yilmaz's explanation, from 2021. Training error falls the whole time. When to "
            "stop training is not a question with one answer, which part twelve's grokking takes to an extreme."
        ) as vo:
            self.play(FadeIn(G), FadeIn(setup))
            vo.wait_until("a")
            k1 = i1 + 1
            part = curve(ax, lt[:k1], ly(med[:k1]), TEST, 4.5)
            self.play(Create(part), FadeIn(key[0]), run_time=1.5)
            self.play(FadeIn(d1))
            vo.wait_until("b")
            part2 = curve(ax, lt[i1:i2 + 1], ly(med[i1:i2 + 1]), TEST, 4.5)
            self.play(Create(part2), run_time=1.5)
            self.play(FadeIn(d2))
            vo.wait_until("c")
            part3 = curve(ax, lt[i2:], ly(med[i2:]), TEST, 4.5)
            self.play(Create(part3), FadeIn(bd), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(cf), Create(cs), Create(ct), FadeIn(key[1:]), run_time=2.0)
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
