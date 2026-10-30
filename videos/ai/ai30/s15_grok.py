from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai30.common import CTRL, FEAT, PART, heat_image, load, signed_image

TRN, TST = C.TRUE_P, C.SURPRISE
RES, EXC, WN = C.BITS, C.MLP, GREY_B


def first(steps, cond):
    i = np.flatnonzero(cond)
    return int(steps[i[0]]) if len(i) else -1


class Grok(VoiceoverScene):
    def construct(self):
        self.card()
        self.curves()
        self.algorithm()
        self.spectrum()
        self.neurons()
        self.progress()

    def card(self):
        card = chapter_card(14, r"Grokking, mechanistically", r"What happens inside before a network suddenly generalizes?",
                            part=PART)
        with self.voiceover("Chapter fourteen. Grokking, mechanistically."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def logaxes(self, d, center, ylabel, x_len=7.0, y_len=3.6, keys=("train_loss", "test_loss"), every=2):
        st = np.asarray(d["step"], float)
        ys = np.log10(np.clip(np.concatenate([d[k] for k in keys]), 1e-8, None))
        lo, hi = np.floor(ys.min()), np.ceil(ys.max())
        g = axes([0, st[-1]], [lo, hi], x_length=x_len, y_length=y_len, xlabel=r"training steps (full batch)",
                 ylabel=ylabel, xticks=[0, st[-1]], yticks=list(np.arange(lo, hi + 1, every)),
                 yfmt=lambda v: rf"10^{{{int(v)}}}", center=center)
        g.lo, g.hi = float(lo), float(hi)  # CornerAxes re-bases ax.y_range at 0, so keep the true range here
        return g, st

    def curves(self):
        d = load("grok")
        g, st = self.logaxes(d, [-2.4, -0.5, 0], r"loss (log scale)", x_len=6.6)
        lt = lambda k: np.log10(np.clip(np.asarray(d[k], float), 1e-8, None))  # noqa: E731
        ct, cv = curve(g.ax, st, lt("train_loss"), TRN, 3), curve(g.ax, st, lt("test_loss"), TST, 3)
        lg = legend([(TRN, rf"the ${int(d['n_train']):,}$ pairs it trains on".replace(",", "{,}")),
                     (TST, rf"the ${int(d['n_test']):,}$ it never sees".replace(",", "{,}"))], font_size=18)
        lg.move_to([4.3, 1.4, 0])
        P = int(d["P"])
        task = label(rf"$(a + b) \bmod {P}$: \ one layer, \ four heads, \ $512$ ReLU units; \ ${100 * float(d['frac']):.0f}\%$ "
                     rf"of the table; \ weight decay ${float(d['wd']):g}$", font_size=22, color=GREY_A).to_edge(UP, buff=0.3)
        tm, tg = int(d["t_memorized"]), int(d["t_grokked"])
        vm = DashedLine(g.ax.c2p(max(tm, 0), g.lo), g.ax.c2p(max(tm, 0), g.hi), color=TRN, dash_length=0.06)
        vg = DashedLine(g.ax.c2p(max(tg, 0), g.lo), g.ax.c2p(max(tg, 0), g.hi), color=TST, dash_length=0.06)
        hc = history_card(2023, r"N.~Nanda, L.~Chan, T.~Lieberum, J.~Smith \& J.~Steinhardt",
                          r"progress measures for grokking via mechanistic interpretability", width=4.4, color=FEAT,
                          font_size=17).move_to([4.3, -1.5, 0])
        grok_said = (f"Then, around step {tg:,}, the held-out loss collapses too: it grokked, "
                     f"{tg / max(tm, 1):.0f} times later than it memorized." if tg > 0 else
                     "In our run the held-out loss never fully collapses.")
        with self.voiceover(
            "Part 12 met grokking: a small network memorizes modular addition, then, long after, suddenly gets it. "
            "Here we ask what happens inside, following Neel Nanda and colleagues' 2023 dissection. "
            f"<bookmark mark='a'/> Their setup, a little smaller: addition modulo {P}, a one-layer transformer, "
            f"trained on {100 * float(d['frac']):.0f} percent of the table with strong weight decay. "
            f"<bookmark mark='b'/> By step {tm:,} it has memorized the pairs it sees, while on the rest it is worse "
            f"than guessing. <bookmark mark='c'/> {grok_said}"
        ) as vo:
            self.play(FadeIn(task), FadeIn(g), FadeIn(lg), FadeIn(hc))
            self.play(Create(ct), Create(cv), run_time=4)
            vo.wait_until("a")
            self.play(Indicate(task, color=FEAT, scale_factor=1.03))
            vo.wait_until("b")
            self.play(Create(vm))
            vo.wait_until("c")
            self.play(Create(vg))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def algorithm(self):
        d = load("grok")
        P = int(d["P"])
        key = [int(k) for k in d["key_final"]]
        rows = [
            cmath(r"a", r"\;\mapsto\;", r"\cos(w_k a),\ \sin(w_k a), \quad w_k = 2\pi k / " + str(P), font_size=32),
            cmath(r"\cos\big(w_k(a + b)\big)", r"=", r"\cos(w_k a)\cos(w_k b) - \sin(w_k a)\sin(w_k b)", font_size=32),
            cmath(r"\cos\big(w_k(a + b - c)\big)", r"=", r"\cos\big(w_k(a+b)\big)\cos(w_k c) + \sin\big(w_k(a+b)\big)\sin(w_k c)",
                  font_size=30),
            cmath(r"\text{logit}(c)", r"\approx", r"\sum_{k} \cos\big(w_k(a + b - c)\big) \quad \text{largest at } c = a + b",
                  font_size=32),
        ]
        whys = [why(r"embed: \ each number as an angle, \ a few frequencies"),
                why(r"attention and the ReLUs build products"),
                why(r"the unembedding reads the angle of $c$"),
                why(r"several frequencies agree only at the answer")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.6, buff=0.45, edge=6.9)
        kl = label(rf"our run's key frequencies: \ $k = {', '.join(map(str, key))}$", font_size=24, color=FEAT).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Nanda and colleagues found the algorithm by reading the weights, and it is trigonometry. "
            "<bookmark mark='a'/> Each number a is embedded as an angle: the cosine and sine of a few frequencies. "
            "<bookmark mark='b'/> Adding two numbers is adding two angles, and the cosine of a sum is a difference of "
            "products, which attention and the ReLU units can compute. <bookmark mark='c'/> The unembedding then "
            "compares that angle with each candidate answer c. <bookmark mark='d'/> Summed over several frequencies, "
            "the waves all peak at c equals a plus b, and nowhere else. <bookmark mark='e'/> Our run settled on "
            f"{len(key)} key frequencies."
        ) as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            self.play(FadeIn(kl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spectrum(self):
        d = load("grok")
        sp = np.asarray(d["spectrum"])  # (checkpoints, frequencies)
        st = np.asarray(d["step"], float)
        pl = np.asarray(d["planes"])
        pst = [int(s) for s in d["plane_steps"]]
        nk = sp.shape[1]
        key = [int(k) for k in d["key_final"]]
        g = axes([0, nk + 1], [0, 1], x_length=6.6, y_length=3.2, xlabel=r"frequency $k$",
                 ylabel=r"share of the embedding", xticks=[1, nk], yticks=[0, 0.5, 1], center=[-3.0, -0.6, 0])
        t = ValueTracker(0)

        def bars_at():
            i = int(np.clip(np.searchsorted(st, t.get_value(), side="right") - 1, 0, len(st) - 1))
            v = sp[i] / max(sp[i].max(), 1e-9)
            return VGroup(*[Rectangle(width=6.6 / (nk + 1) * 0.8, height=max(x * 3.2, 0.01), stroke_width=0,
                                      fill_color=FEAT if (k + 1) in key else CTRL, fill_opacity=0.9)
                            .move_to(g.ax.c2p(k + 1, 0), aligned_edge=DOWN) for k, x in enumerate(v)])

        bs = always_redraw(bars_at)
        cnt = always_redraw(lambda: label(rf"step ${int(t.get_value()):,}$".replace(",", "{,}"), font_size=24, color=WHITE)
                            .next_to(g, UP, buff=0.15))
        yl = label(r"tallest scaled to $1$", font_size=16, color=GREY_B).next_to(g, DOWN, buff=0.55)

        def circle_at(j):
            xy = pl[j]
            xy = xy / max(np.abs(xy).max(), 1e-9) * 1.6
            dots = VGroup(*[Dot([3.8 + x, -0.4 + y, 0], radius=0.045, color=interpolate_color(ManimColor(C.TRUE_P), ManimColor(C.SURPRISE), a / len(xy)))
                            for a, (x, y) in enumerate(xy)])
            return dots

        cj = [circle_at(j) for j in range(len(pst))]
        cl = label(rf"each number in the plane of frequency ${key[0]}$ \\ (colour: \ $0$ to ${int(d['P']) - 1}$)", font_size=18,
                   color=GREY_A).move_to([3.8, 2.1, 0])
        sl = label(rf"step ${pst[0]:,}$".replace(",", "{,}"), font_size=20, color=WHITE).move_to([3.8, -2.4, 0])
        top_share = float(np.sort(sp[-1])[::-1][:len(key)].sum() / sp[-1].sum())
        with self.voiceover(
            "Watch the embedding during training, through its Fourier spectrum: how much of it lies along each "
            "frequency. <bookmark mark='a'/> At first the energy is spread everywhere. <bookmark mark='b'/> As "
            "training goes, a few frequencies take over. By the end the key frequencies hold "
            f"{100 * top_share:.0f} percent of the embedding. <bookmark mark='c'/> In the plane of the strongest one, "
            "the numbers, scattered at the start, end up arranged around a circle: angles."
        ) as vo:
            self.play(FadeIn(g), FadeIn(yl))
            self.add(bs, cnt)
            vo.wait_until("a")
            self.play(t.animate.set_value(st[len(st) // 6]), run_time=2, rate_func=linear)
            vo.wait_until("b")
            self.play(t.animate.set_value(st[-1]), run_time=4, rate_func=linear)
            vo.wait_until("c")
            cur = cj[0]
            self.play(FadeIn(cl), FadeIn(cur), FadeIn(sl))
            for j in range(1, len(cj)):
                self.play(Transform(cur, cj[j]), Transform(sl, label(rf"step ${pst[j]:,}$".replace(",", "{,}"), font_size=20,
                                                                      color=WHITE).move_to(sl)), run_time=0.35)
        for m_ in (bs, cnt):
            m_.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def neurons(self):
        d = load("grok")
        nf, ns = np.asarray(d["neuron_freq"]), np.asarray(d["neuron_share"])
        key = [int(k) for k in d["key_final"]]
        clean = ns > 0.5
        counts = [int(((nf == k) & clean).sum()) for k in key]
        other = int(clean.sum()) - sum(counts)
        A = np.asarray(d["neuron_act"])
        img = heat_image(A, 3.6, 3.6, color=FEAT, gamma=0.7).move_to([3.4, -0.5, 0])
        il = label(rf"neuron {int(d['neuron'])}: \ its activation for every $(a, b)$", font_size=20, color=FEAT).next_to(img, UP, buff=0.15)
        ax_ = label(r"$a \rightarrow$ \quad $b \downarrow$ \quad waves in $a$ and in $b$", font_size=18, color=GREY_B).next_to(img, DOWN, buff=0.12)
        bars_ = VGroup()
        top = max(counts + [other, 1])
        for i, (k, c) in enumerate(zip(key + ["other"], counts + [other])):
            r = Rectangle(width=0.6, height=max(c / top * 3.0, 0.01), stroke_width=0, fill_color=FEAT if k != "other" else CTRL,
                          fill_opacity=0.9).move_to([-5.4 + 0.95 * i, -2.2, 0], aligned_edge=DOWN)
            bars_.add(VGroup(r, MathTex(str(c), font_size=22).next_to(r, UP, buff=0.06),
                             label(rf"$k = {k}$" if k != "other" else r"other", font_size=16, color=GREY_A).next_to(r, DOWN, buff=0.1)))
        bl = label(rf"the ${int(clean.sum())}$ neurons with more than half their activation \\ at one frequency, \ by "
                   r"frequency", font_size=20, color=GREY_A).move_to([-3.4, 1.6, 0])
        with self.voiceover(
            "The MLP's neurons tell the same story. <bookmark mark='a'/> Decompose each neuron's activation, over "
            f"every pair a and b, into waves: {int(clean.sum())} of the 512 have more than half of it at a single "
            f"frequency, and {sum(counts)} of those at a key frequency. <bookmark mark='b'/> Here is one, over the whole "
            "table: waves in a and in b at its frequency, whose products hold the waves of a plus b. The neuron is a "
            "piece of the cosine of a sum."
        ) as vo:
            self.play(FadeIn(bl))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1:])) for b in bars_], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(img), FadeIn(il), FadeIn(ax_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def progress(self):
        d = load("grok")
        g, st = self.logaxes(d, [-2.0, -0.5, 0], r"loss (log scale)", x_len=7.0, y_len=3.8,
                             keys=("test_loss", "restricted_loss", "excluded_loss"), every=1)
        lt = lambda k: np.log10(np.clip(np.asarray(d[k], float), 1e-8, None))  # noqa: E731
        ylo, yhi = g.lo, g.hi
        cl = lambda y: np.clip(y, ylo, yhi)  # noqa: E731
        cv = curve(g.ax, st, cl(lt("test_loss")), TST, 3)
        cr = curve(g.ax, st, cl(lt("restricted_loss")), RES, 3)
        ce = curve(g.ax, st, cl(lt("excluded_loss")), EXC, 3)
        wn = np.asarray(d["weight_norm"], float)
        iw = int(np.argmax(wn))
        lg = legend([(TST, r"test loss"), (RES, r"restricted loss: \ only the key waves kept"),
                     (EXC, r"excluded loss: \ the key waves removed \ (train)")], font_size=17).to_corner(UR, buff=0.3)
        cw = label(rf"size of the weights: \\ ${wn[0]:.0f}$ at the start, \ ${wn[iw]:.0f}$ at step ${int(st[iw]):,}$, \\ "
                   rf"${wn[-1]:.0f}$ at the end".replace(",", "{,}"), font_size=20, color=WN).move_to([5.0, 0.2, 0])
        rt = first(st, lt("restricted_loss") < 0)
        tt = first(st, lt("test_loss") < 0)
        et = first(st, lt("excluded_loss") > 0)
        ok = rt > 0 and tt > 0 and rt < tt
        verdict = (f"The restricted loss, which keeps only the key waves, drops below one nat by step {rt:,}, long "
                   f"before the test loss does, at step {tt:,}: the circuit was being built while the network still "
                   "looked like a memorizer." if ok else
                   f"Here the restricted loss and the test loss fall together, around steps {rt:,} and {tt:,}.")
        with self.voiceover(
            "Nanda and colleagues' real point was a timeline, measured with progress measures that look inside. "
            "Pause and predict: does the circuit appear when the test loss falls, or before? <bookmark mark='a'/> "
            + verdict + " <bookmark mark='b'/> The excluded loss removes exactly those waves "
            "from the logits and scores the training pairs: it climbs as the network comes to rely on them. "
            f"<bookmark mark='c'/> And after a first rise the weights shrink, weight decay pruning the memorized lookup "
            "table. "
            "Three phases: memorization, a circuit forming underneath, and a clean-up that removes the memory. The "
            f"sudden jump is only the last of them. At the end, the key waves account for {100 * float(d['fit_r2']):.0f} "
            "percent of the logits' variance."
        ) as vo:
            self.play(FadeIn(g), Create(cv), FadeIn(lg[0]))
            pz = pause_card(r"The circuit: \ when the test loss falls, \ or before?", width=4.0, font_size=22)
            pz.move_to([4.9, -1.2, 0])
            self.play(FadeIn(pz))
            vo.wait_until("a")
            self.play(FadeOut(pz), Create(cr), FadeIn(lg[1]), run_time=2)
            vo.wait_until("b")
            self.play(Create(ce), FadeIn(lg[2]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(cw))
        self.wait(0.3)
        self.clear_scene()
