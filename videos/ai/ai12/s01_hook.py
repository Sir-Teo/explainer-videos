from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import FIT, HIST, PART, era_strip, load, width_ramp


class Hook(VoiceoverScene):
    def construct(self):
        self.law()
        self.era()
        self.plan()

    # ------------------------------------------------------------------
    def law(self):
        s, ch = load("sweep"), load("chinchilla")
        N, D, Lb = np.asarray(s["N"], float), np.asarray(s["D"], float), np.asarray(s["bits"], float)
        widths = [int(w) for w in s["widths"]]
        n_runs = int(np.isfinite(Lb).sum())
        E, slope = float(ch["E"]), float(ch["env_slope"])
        lC = np.log10(6 * N[:, None] * D[None])
        x0, x1 = math.floor(np.nanmin(lC[np.isfinite(Lb)]) * 2) / 2, math.ceil(np.nanmax(lC[np.isfinite(Lb)]) * 2) / 2
        lo = math.floor((np.nanmin(Lb) - 0.1) * 5) / 5
        hi = math.ceil(min(np.nanmax(Lb), np.nanmin(Lb) + 2.6) * 5) / 5
        ax = CornerAxes(x_range=[x0, x1, 1], y_range=[lo, hi, 0.2], x_length=8.0, y_length=4.9, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-2.0, -0.45, 0])
        xt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=22, color=GREY_B).next_to(ax.c2p(k, lo), DOWN, buff=0.1)
                      for k in range(math.ceil(x0), math.floor(x1) + 1)])
        yt = VGroup(*[MathTex(f"{v:.1f}", font_size=22, color=GREY_B).next_to(ax.c2p(x0, v), LEFT, buff=0.1)
                      for v in np.arange(math.ceil(lo * 2) / 2, hi + 1e-9, 0.5)])
        xn = label(r"training compute \ (operations, \ $6ND$)", font_size=24, color=GREY_A).next_to(xt, DOWN, buff=0.15)
        yn = label(r"held-out bits per character", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        clip = lambda v: np.minimum(v, hi)  # noqa: E731
        lt = ValueTracker(x0)

        def fan():
            g = VGroup()
            c = lt.get_value()
            for i in range(len(widths)):
                ok = np.isfinite(Lb[i]) & (lC[i] <= c + 1e-9)
                if ok.sum() >= 1:
                    xs, ys = lC[i][ok], clip(Lb[i][ok])
                    if ok.sum() >= 2:
                        g.add(VMobject(stroke_color=width_ramp(i, len(widths)), stroke_width=2.6).set_points_as_corners(
                            [ax.c2p(a, b) for a, b in zip(xs, ys)]))
                    g.add(*[Dot(ax.c2p(a, b), radius=0.035, color=width_ramp(i, len(widths))) for a, b in zip(xs, ys)])
            return g

        live = always_redraw(fan)
        clock = always_redraw(lambda: MathTex(rf"10^{{{lt.get_value():.1f}}}\ \text{{operations}}", font_size=26,
                                              color=GREY_A).next_to(ax.c2p(x0, hi), DR, buff=0.15).shift(RIGHT * 0.1))
        # the frontier: the lowest loss at each compute, and the power law it follows
        eC, eL = np.log10(np.asarray(ch["env_C"])), np.asarray(ch["env_L"])
        ok = np.isfinite(eL)
        b = np.polyfit(eC[ok], np.log10(eL[ok] - E), 1)
        xs = np.linspace(eC[ok].min(), x1, 120)
        law = curve(ax, xs, clip(E + 10 ** np.polyval(b, xs)), FIT, 4.5, smooth=True)
        floor = DashedLine(ax.c2p(x0, E), ax.c2p(x1, E), color=GREY_B, stroke_width=2) if E > lo else VMobject()
        fl = label(rf"floor \ $E = {E:.2f}$", font_size=22, color=GREY_B).next_to(ax.c2p(x1, E), UL, buff=0.08) if E > lo else VMobject()
        key = VGroup(label(r"width", font_size=22, color=GREY_A),
                     *[label(f"{w:,}".replace(",", "{,}"), font_size=20, color=width_ramp(i, len(widths)))
                       for i, w in enumerate(widths) if i % 2 == 0 or i == len(widths) - 1])
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(ax, RIGHT, buff=0.3).align_to(ax, UP)
        # the inset: what is left above the floor, on log axes, is a straight line
        r = np.log10(eL[ok] - E)
        ry0, ry1 = math.floor(r.min() * 2) / 2, math.ceil(r.max() * 2) / 2
        ix = CornerAxes(x_range=[math.floor(eC[ok].min()), math.ceil(eC[ok].max()), 1], y_range=[ry0, ry1, 0.5],
                        x_length=3.2, y_length=1.7, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([4.75, -2.0, 0])
        idots = VGroup(*[Dot(ix.c2p(a, c), radius=0.04, color=FIT) for a, c in zip(eC[ok], r)])
        iline = Line(ix.c2p(eC[ok].min(), np.polyval(b, eC[ok].min())), ix.c2p(eC[ok].max(), np.polyval(b, eC[ok].max())),
                     color=C.BITS, stroke_width=2.5)
        il = label(r"$L - E$ \ on log axes", font_size=20, color=GREY_A).next_to(ix, UP, buff=0.1)
        isl = label(rf"slope ${slope:.2f}$", font_size=22, color=C.BITS).next_to(ix, DOWN, buff=0.12)
        tag = note(rf"computed: \ ${n_runs}$ training runs of Part 11's character model on this computer").to_corner(DL, buff=0.2)
        with self.voiceover(
            "Make a model bigger, train it longer, and it gets better. That much everyone expected. The surprise was "
            "how predictably. <bookmark mark='a'/> Here are thirteen sizes of part eleven's character model, each "
            f"trained for up to nine lengths: {n_runs} runs on the computer making this video, each drawn at the "
            "number of operations it cost. <bookmark mark='b'/> Every size improves, then flattens: it runs out of "
            "room. But the bottom edge of the whole fan, the best loss each budget can buy, is a smooth curve. "
            f"<bookmark mark='c'/> Take away a floor of {E:.2f} bits, and what's left falls along a straight line on "
            f"log axes: a power law, with slope {slope:.2f}. Curves like this, measured on small models, are how "
            "laboratories decide what to build next."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), FadeIn(key), FadeIn(tag))
            vo.wait_until("a")
            self.add(live, clock)
            self.play(lt.animate.set_value(x1), run_time=7.0, rate_func=linear)
            live.clear_updaters()
            clock.clear_updaters()
            vo.wait_until("b")
            self.play(Create(law), run_time=2.0)
            self.play(Create(floor), FadeIn(fl))
            vo.wait_until("c")
            self.play(Create(ix), FadeIn(il), LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in idots], lag_ratio=0.05))
            self.play(Create(iline), FadeIn(isl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def era(self):
        events = [
            (1994, r"Neal: \\ infinitely wide \\ = a Gaussian process"),
            (2001, r"Banko, Brill: \\ more data beats \\ a better algorithm"),
            (2017, r"Hestness et al.: \\ power laws \\ in four fields"),
            (2018, r"Jacot et al.: \\ the neural \\ tangent kernel"),
            (2020, r"Kaplan et al.: \\ scaling laws; \\ GPT-3"),
            (2022, r"Chinchilla; \\ $\mu$Transfer; \\ grokking"),
            (2023, r"data runs out; \\ emergence, \\ or a mirage?"),
            (2024, r"o1: \\ scaling the \\ thinking"),
            (2025, r"reinforcement \\ learning at \\ pretraining scale"),
            (2026, r"back to much \\ larger base models"),
        ]
        head, axis, tag, skel, marks = era_strip(self, events, font_size=20)
        with self.voiceover(
            "The idea has a history. In 1994, Radford Neal showed that an infinitely wide network is a Gaussian "
            "process. <bookmark mark='a'/> In 2001, Banko and Brill found that more data beat a cleverer algorithm. "
            "<bookmark mark='b'/> In 2017, a team at Baidu found power laws in translation, language, images and "
            "speech. <bookmark mark='c'/> In 2018, the neural tangent kernel. <bookmark mark='d'/> In 2020, "
            "OpenAI's scaling laws, and GPT-3 built on them. <bookmark mark='e'/> In 2022, Chinchilla corrected the "
            "recipe, mu-P let one learning rate serve every size, and grokking puzzled everyone. "
            "<bookmark mark='f'/> In 2023, the limits: data that runs out, and abilities that seem to appear from "
            "nowhere. <bookmark mark='g'/> In 2024, scaling moved to the answer: models that think for longer. "
            "<bookmark mark='h'/> In 2025, reinforcement learning at the scale of pretraining. "
            "<bookmark mark='i'/> And in 2026, laboratories went back to much larger base models."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(tag), FadeIn(skel))
            self.play(FadeIn(marks[0], shift=UP * 0.2))
            for k, mk in enumerate("abcdefghi"):
                vo.wait_until(mk)
                self.play(FadeIn(marks[k + 1], shift=(UP if (k + 1) % 2 == 0 else DOWN) * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ The Mathematics of Scale", font_size=48).to_edge(UP, buff=0.45)
        smap = series_map(current=PART, done=PART - 1).scale(0.8).move_to(DOWN * 0.5)
        obj = objectives_card([
            r"infinitely wide networks: \ Gaussian processes, \ the neural tangent kernel, \ and why a lazy "
            r"network learns no features",
            r"$\mu$P, derived: \ one learning rate for every width and depth; \ and how big a batch",
            r"scaling laws, measured on our own sweep; \ Chinchilla's valley, derived; \ what Kaplan missed",
            r"the trade-offs: \ training for inference, \ repeating data, \ experts, \ fewer bits",
            r"why power laws; \ emergence, or a mirage; \ grokking and its circuit",
            r"the frontier: \ thinking at answer time, \ reinforcement learning, \ and has pretraining stalled?",
        ], font_size=24).move_to(DOWN * 0.35)
        with self.voiceover(
            "This is Part 12 of AI, Built, and the end of its second act. <bookmark mark='a'/> In it: what happens "
            "to a network as it gets infinitely wide; how to set a learning rate once and keep it as the model grows "
            "wider and deeper; the scaling laws, measured on our own models and derived; the trade-offs that bend "
            "them; why they are power laws at all; and what is happening at the frontier."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
