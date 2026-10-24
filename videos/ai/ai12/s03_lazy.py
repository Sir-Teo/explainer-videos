from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import HIST, LAZY, PART, RICH, SP, band, load, log_axes, predict_card, takeaway_card


class Lazy(VoiceoverScene):
    def construct(self):
        self.card()
        self.lazy()
        self.predict()
        self.race()
        self.units()
        self.takeaway()

    def card(self):
        card = chapter_card(2, r"Lazy", r"Why does an infinitely wide network learn no features?", part=PART)
        with self.voiceover("Chapter two. Lazy."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def lazy(self):
        z = load("lazy")
        W, M = np.asarray(z["widths"], float), np.asarray(z["moved"])
        slope = float(z["slope"])
        lx, ly = np.log10(W), np.log10(M)
        y0, y1 = math.floor(ly.min() * 2) / 2 - 0.25, math.ceil(ly.max() * 2) / 2 + 0.25
        ax, labs = log_axes((1, 3.5), (y0, y1), x_length=6.4, y_length=4.2, center=[-3.0, -0.6, 0],
                            x_ticks=[("10", 1), ("100", 2), ("1{,}000", 3)],
                            y_ticks=[(rf"10^{{{k}}}", k) for k in range(math.ceil(y0), math.floor(y1) + 1)])
        xn = label(r"width of the hidden layers", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.45)
        yn = label(r"how much the hidden features changed in training", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15)
        yn.align_to(ax, LEFT)
        dts = VGroup(*[Dot(ax.c2p(x, y), radius=0.08, color=LAZY) for x, y in zip(lx, ly)])
        b = np.polyfit(lx, ly, 1)
        fit = Line(ax.c2p(1.4, np.polyval(b, 1.4)), ax.c2p(3.4, np.polyval(b, 3.4)), color=WHITE, stroke_width=2.5)
        sl = label(rf"slope ${slope:.2f}$", font_size=28, color=WHITE).next_to(fit.get_center(), UR, buff=0.2)
        tag = note(r"Part 11's character model, \ $800$ steps of plain gradient descent, \ neural-tangent step sizes")
        tag.to_corner(DL, buff=0.25)
        hc = history_card(2019, r"L\'ena\"ic Chizat, Edouard Oyallon \& Francis Bach",
                          r"\textit{On lazy training}: \ scale a model's output up, and it trains like its "
                          r"linearization: "
                          r"a kernel method, \ whatever its architecture", width=5.6, color=HIST).move_to([3.7, 1.5, 0])
        # the lazy picture: the hidden features frozen as they started, only the weights on them re-learned
        ins = VGroup(*[Dot(radius=0.07, color=GREY_B) for _ in range(4)]).arrange(DOWN, buff=0.3)
        hid = VGroup(*[Circle(radius=0.1, color=LAZY, stroke_width=2.5) for _ in range(6)]).arrange(DOWN, buff=0.14)
        hid.next_to(ins, RIGHT, buff=1.2)
        out = Circle(radius=0.13, color=C.BITS, stroke_width=3).next_to(hid, RIGHT, buff=1.2)
        frozen = VGroup(*[DashedLine(a.get_center(), b_.get_left(), color=GREY_D, stroke_width=1.2, dash_length=0.05)
                          for a in ins for b_ in hid])
        learned = VGroup(*[Line(b_.get_right(), out.get_left(), color=C.BITS, stroke_width=2.2) for b_ in hid])
        pic = VGroup(frozen, learned, ins, hid, out,
                     label(r"frozen features", font_size=20, color=GREY_B).next_to(frozen, DOWN, buff=0.1),
                     label(r"re-weighted", font_size=20, color=C.BITS).next_to(learned, DOWN, buff=0.1))
        pic.scale(0.9).move_to([3.7, -1.5, 0])
        with self.voiceover(
            "A wide network trained like its linearization has a catch. Take part eleven's character model, make it "
            "wider and wider, and train it with the step sizes of the neural tangent kernel. Measure how much its "
            "hidden features change: what each hidden unit computes from the input. <bookmark mark='a'/> The wider "
            f"the network, the less they change: slope {slope:.2f}. <bookmark mark='b'/> In 2019, Chizat, Oyallon "
            "and Bach called this lazy training, and showed it is not special to wide networks: scale any model's "
            "output up and it trains like its linearization. <bookmark mark='c'/> A lazy network can only re-weight "
            "the random features it started with. It is a kernel method, like part six's, and the models far bigger "
            "than their data that part eight met are, in this limit, exactly its minimum-norm fits."
        ) as vo:
            self.play(Create(ax), FadeIn(labs), FadeIn(xn), FadeIn(yn), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dts], lag_ratio=0.15), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(fit), FadeIn(sl))
            vo.wait_until("b")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(pic))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def race(self):
        r = load("rich")
        var = float(r["var"])
        nc, mc = np.asarray(r["ntk_curve"]), np.asarray(r["mf_curve"])
        kern = np.asarray(r["kernel"])
        steps = nc[0, :, 0]
        sx = np.log10(np.maximum(steps, 1))
        top = math.ceil(var * 1.15 * 10) / 10
        ax = CornerAxes(x_range=[0, math.ceil(sx.max() * 2) / 2, 1], y_range=[0, top, top / 4], x_length=7.4, y_length=4.2,
                        tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05})
        ax.move_to([-2.2, -0.6, 0])
        xt = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for t, v in (("1", 0), ("10", 1), ("100", 2), ("1{,}000", 3)) if v <= sx.max() + 0.6])
        yt = VGroup(*[MathTex(f"{v:.2f}", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in np.linspace(0, top, 5)])
        xn = label(r"training steps \ (log scale)", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yn = label(r"error on $4{,}000$ new points \ (mean squared)", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12)
        yn.align_to(ax, LEFT)
        guess = DashedLine(ax.c2p(0, var), ax.c2p(sx.max(), var), color=GREY_B, stroke_width=1.8)
        gl = label(r"guessing the average", font_size=18, color=GREY_B).next_to(ax.c2p(sx.max(), var), UL, buff=0.06)
        kl = DashedLine(ax.c2p(0, kern.mean()), ax.c2p(sx.max(), kern.mean()), color=LAZY, stroke_width=2.5)
        kll = label(r"kernel regression", font_size=18, color=LAZY).next_to(ax.c2p(sx.max(), kern.mean()), DL, buff=0.06)

        def runs(cv, col):
            te = cv[:, :, 2]
            return VGroup(band(ax, sx, te.min(0), te.max(0), col, 0.2), curve(ax, sx, te.mean(0), col, 3.5))

        lazy, rich = runs(nc, LAZY), runs(mc, RICH)
        task = VGroup(MathTex(r"y = (w^* \!\cdot x)^2 - 1", font_size=34),
                      label(rf"$x$ in ${int(r['d'])}$ dimensions, \ ${int(r['n'])}$ examples; \\ $w^*$ hidden", font_size=22,
                            color=GREY_A),
                      label(rf"two layers, \ width ${int(r['width']):,}$".replace(",", "{,}"), font_size=22, color=GREY_A))
        task.arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([4.5, 2.2, 0])
        nt, mt = np.asarray(r["ntk_test"]), np.asarray(r["mf_test"])
        lg = VGroup(label(r"lazy: \ neural-tangent scaling", font_size=22, color=LAZY),
                    label(rf"\quad ${nt.mean():.3f}$ \ (seeds ${nt.min():.3f}$--${nt.max():.3f}$)", font_size=20, color=LAZY),
                    label(r"rich: \ mean-field ($\mu$P) scaling", font_size=22, color=RICH),
                    label(rf"\quad ${mt.mean():.3f}$ \ (seeds ${mt.min():.3f}$--${mt.max():.3f}$)", font_size=20, color=RICH))
        lg.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.5, -0.3, 0])
        eqs = VGroup(MathTex(r"\tfrac{1}{\sqrt n}\textstyle\sum_j a_j\,\sigma(w_j\!\cdot x),\ \ \eta", font_size=26, color=LAZY),
                     MathTex(r"\tfrac{1}{n}\textstyle\sum_j a_j\,\sigma(w_j\!\cdot x),\ \ \eta\, n", font_size=26, color=RICH))
        eqs.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(lg, DOWN, buff=0.35)
        tag = note(r"three seeds each; \ bands: \ min to max; \ same data, width, steps; \ each its better of two "
                   r"learning rates").to_corner(DL, buff=0.2)
        ratio = nt.mean() / mt.mean()
        wins = mt.max() < nt.min()
        kgap = kern.mean() / nt.mean() - 1
        said0 = (
            "It ends close to kernel regression with its starting kernel: the lazy limit, computed exactly. "
            if abs(kgap) < 0.15 else
            f"Kernel regression with its starting kernel, the lazy limit computed exactly, ends {100 * abs(kgap):.0f} "
            f"percent {('worse' if kgap > 0 else 'better')}: at this width the network is not yet fully lazy. "
        )
        said1 = (
            f"Its error is {ratio:.1f} times smaller, and every seed beats every lazy seed."
            if wins else f"Its error is {ratio:.1f} times smaller on average, though the seeds overlap."
        )
        with self.voiceover(
            "Does it matter? Here is a task where it does. The answer is the square of how far x points along one "
            f"hidden direction, w-star, minus one, with x in {int(r['d'])} dimensions and {int(r['n'])} examples to "
            "learn from. "
            "<bookmark mark='a'/> Train a wide two-layer network the lazy way, with the neural tangent kernel's "
            "scaling. <bookmark mark='b'/> "
            + said0
            + "<bookmark mark='c'/> Now the same network, the same data and the same "
            "number of steps, scaled the mean-field way: divide the output by n instead of its square root, and "
            "multiply the learning rate by n, so every unit moves by a fixed amount. "
            + said1
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), Create(guess), FadeIn(gl), FadeIn(task),
                      FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(lazy[0]), Create(lazy[1]), FadeIn(lg[:2]), FadeIn(eqs[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(kl), FadeIn(kll))
            vo.wait_until("c")
            self.play(FadeIn(rich[0]), Create(rich[1]), FadeIn(lg[2:]), FadeIn(eqs[1]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def units(self):
        r = load("rich")
        Un, Um = np.asarray(r["ntk_units"]), np.asarray(r["mf_units"])  # snapshots x units x (along w*, off w*)
        steps = np.asarray(r["ntk_curve"])[0, ::5, 0]
        lim = float(np.ceil(np.abs(np.concatenate([Un.reshape(-1, 2), Um.reshape(-1, 2)])).max() * 1.05 * 2) / 2)
        pans, dts = VGroup(), []
        for k, (U, col, ttl) in enumerate(((Un, LAZY, r"lazy"), (Um, RICH, r"rich"))):
            ax = Axes(x_range=[-lim, lim, lim / 2], y_range=[0, lim, lim / 2], x_length=5.4, y_length=3.0, tips=False,
                      axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.4 + 6.8 * k, -0.6, 0])
            xl = label(r"along $w^*$", font_size=20, color=GREY_A).next_to(ax, DOWN, buff=0.12)
            yl = label(r"off $w^*$", font_size=20, color=GREY_A).next_to(ax, LEFT, buff=0.12).rotate(PI / 2)
            t = label(ttl, font_size=30, color=col).next_to(ax, UP, buff=0.2)
            pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.04, color=col).set_opacity(0.85) for a, b in U[0]])
            pans.add(VGroup(ax, xl, yl, t))
            dts.append((ax, pts, U))
        head = label(r"each hidden unit's weights: \ along the hidden direction, \ and off it", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.35)
        clock = VGroup(label(r"step", font_size=24, color=GREY_A), Integer(0, font_size=26, color=C.BITS))
        clock.arrange(RIGHT, buff=0.15).next_to(head, DOWN, buff=0.15)
        mvn, mvm = np.asarray(r["ntk_moved"]).mean(), np.asarray(r["mf_moved"]).mean()
        moral = label(r"learning a feature: \ the units turn toward what matters", font_size=26, color=RICH)
        moral.to_edge(DOWN, buff=0.35)
        tag = note(rf"the first ${Un.shape[1]}$ of ${int(r['width']):,}$ units, \ seed 0".replace(",", "{,}")).to_corner(DR, buff=0.2)
        with self.voiceover(
            "What did the rich network learn that the lazy one could not? Draw each hidden unit as a point: how much "
            "its weights point along the hidden direction, and how much they point elsewhere. "
            "<bookmark mark='a'/> Now replay training. <bookmark mark='b'/> The lazy units hardly move: in all, "
            f"its weights travel {100 * mvn:.0f} percent of their starting length. The rich units swing out along "
            f"w-star, {100 * mvm:.0f} percent: the network has found the one direction that matters. That is a "
            "learned feature, and no kernel method can make one. <bookmark mark='c'/> So the infinite-width limit we "
            "want is the other one, where features keep moving at every width. For two layers it is called mean "
            "field; for any depth, it is mu-P."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(p) for p in pans], *[FadeIn(p) for _, p, _ in dts], FadeIn(clock), FadeIn(tag))
            vo.wait_until("a")
            for t in range(1, len(steps)):
                self.play(*[d.animate.move_to(ax.c2p(a, b)) for ax, pts, U in dts for d, (a, b) in zip(pts, U[t])],
                          clock[1].animate.set_value(int(steps[t])), run_time=0.45, rate_func=smooth)
                if t == 1:
                    vo.wait_until("b")
            vo.wait_until("c")
            self.play(FadeIn(moral))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def predict(self):
        pc = predict_card(r"Two copies of one wide network, \ the same data, \ the same number of steps: \ one "
                          r"scaled the lazy way, \ one the mean-field way. \ Which learns the hidden direction?")
        with self.voiceover(
            "Pause and predict. Two copies of one wide network, the same data and the same number of steps: one "
            "scaled the lazy way, one the mean-field way. Which one learns the hidden direction?"
        ):
            self.play(FadeIn(pc, shift=UP * 0.2))
        self.wait(2.0)
        self.play(FadeOut(pc))

    def takeaway(self):
        tk = takeaway_card(r"Lazy networks learn no features",
                           r"In the lazy limit a network only re-weights the random features it started with. \ To "
                           r"learn features at every width, \ every unit must keep moving.",
                           r"next: \ $\mu$P, \ derived")
        with self.voiceover(
            "The takeaway: in the lazy limit, a network only re-weights the features it started with. To learn "
            "features at any width, every unit must keep moving, and that is what mu-P is built to do. Next, its "
            "derivation."
        ) as vo:
            self.play(FadeIn(tk[0], shift=UP * 0.2))
            self.wait(max(0.0, vo.duration * 0.5 - 1.0))
            self.play(FadeIn(tk[1]))
        self.wait(0.4)
        self.play(FadeOut(tk))
