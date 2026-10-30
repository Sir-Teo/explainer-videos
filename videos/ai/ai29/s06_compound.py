from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai29.common import AGENT, FAIL, GOOD, PART, REWARD, TOOL, load

P_COLORS = [C.SURPRISE, C.BITS, C.INTERVAL]
MODES = [("head", r"in its head", GREY_B), ("react", r"ReAct, \ with tools", AGENT), ("check", r"ReAct, \ checking its work", REWARD)]


def curve(ax, xs, ys, color, stroke_width=3) -> VMobject:
    return VMobject(color=color, stroke_width=stroke_width).set_points_smoothly([ax.c2p(x, y) for x, y in zip(xs, ys)])


class Compound(VoiceoverScene):
    def construct(self):
        self.card()
        self.compound()
        self.measured()
        self.doubling()

    def card(self):
        card = chapter_card(5, r"Compounding error", r"Why are long tasks so hard?", part=PART)
        with self.voiceover("Chapter five. Compounding error."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def compound(self):
        h = load("horizon")
        ns = np.asarray(h["ns"], float)
        ps = [float(p) for p in h["ps"]]
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 1, 0.25], x_length=8.4, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.4, -0.4, 0])
        xt = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for t, v in (("1", 0), ("10", 1), ("100", 2), ("1{,}000", 3), ("10{,}000", 4))])
        yt = VGroup(*[MathTex(rf"{int(100 * v)}\%", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1) for v in (0, 0.5, 1)])
        xn = label(r"steps in the task \ (log scale)", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yn = label(r"chance of finishing it", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        lines = VGroup(*[curve(ax, np.log10(ns), np.asarray(h[f"succ{p:g}"]), c_, 4) for p, c_ in zip(ps, P_COLORS)])
        keys = VGroup(*[label(rf"each step right ${100 * p:g}\%$ of the time", font_size=24, color=c_) for p, c_ in zip(ps, P_COLORS)])
        keys.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.4, 1.6, 0])
        colors = {r"p": C.BITS, r"n": C.TRUE_P}
        f = cmath(r"P(\text{done})", "=", r"p", r"^{\,", r"n", r"}", colors=colors, font_size=44).move_to([4.4, -0.4, 0])
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(4, 0.5), color=GREY_D, stroke_width=1.5)
        v99 = 0.99 ** 100
        # a task as a chain of steps, schematic: each must go right; one slip and the rest never happen
        n_st = 9
        st_d = VGroup(*[Dot([0.38 * i, 0, 0], radius=0.09, color=GREY_C) for i in range(n_st)])
        st_l = Line(st_d[0].get_center(), st_d[-1].get_center(), color=GREY_D, stroke_width=2)
        st_t = VGroup(label(r"start", font_size=18, color=GREY_B).next_to(st_d[0], DOWN, buff=0.15),
                      label(r"finish", font_size=18, color=GREY_B).next_to(st_d[-1], DOWN, buff=0.15))
        hz = gloss(r"horizon", r"how many steps a task takes, \\ from start to finish", picture=VGroup(st_l, st_d, st_t),
                   corner=DR, width=3.6, color=C.TRUE_P)
        hz_d = hz[1][2][1]
        slip = 6  # schematic: the step that goes wrong
        with self.voiceover(
            "Agents work in long chains of steps: read a page, click, write code, run it, read the error. "
            "<bookmark mark='h'/> How many steps a task takes, from start to finish, is its horizon, and every "
            "step has to go right. <bookmark mark='a'/> If each step succeeds with probability p, a task of n steps "
            "succeeds with p to the n. <bookmark mark='b'/> At ninety percent per step, a ten-step task already "
            f"fails two times in three. At ninety-nine percent, a hundred-step task succeeds only {100 * v99:.0f} "
            "percent of the time. Small errors compound."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), Create(half))
            vo.wait_until("h")
            self.play(FadeIn(hz))
            self.play(LaggedStart(*[d_.animate.set_color(P_COLORS[2]) for d_ in hz_d[:slip]], lag_ratio=0.25), run_time=1.5)
            self.play(hz_d[slip].animate.set_color(C.SURPRISE).scale(1.5), *[d_.animate.set_opacity(0.25) for d_ in hz_d[slip + 1:]],
                      run_time=0.6)
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3), FadeIn(keys), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        a = load("agent")
        ns = np.asarray(a["ns"], float)
        g = axes([0, 60, 10], [0, 1, 0.25], x_length=7.2, y_length=4.4, xlabel=r"steps in the task \ (prices to look up)",
                 ylabel=r"tasks done right", xticks=[0, 20, 40, 60], yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{int(100 * v)}\\%", center=[-2.4, -0.3, 0])
        ax = g.ax
        dots, lines, keys = VGroup(), VGroup(), VGroup()
        for mode, name, col in MODES:
            s_ = np.asarray(a[f"{mode}_succ"])
            dots.add(VGroup(*[Dot(ax.c2p(x, y), radius=0.06, color=col) for x, y in zip(ns, s_)]))
            p = float(a[f"{mode}_p"])
            xx = np.linspace(0, 60, 61)
            lines.add(curve(ax, xx, p ** xx, col, 2).set_stroke(opacity=0.6))
            keys.add(label(rf"{name}: \ ${100 * p:.1f}\%$ a step", font_size=26, color=col))
        keys.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.0, 1.2, 0])
        r = a["rates"]
        tag = note(rf"simulated, \ ${a['tasks']:,}$ tasks per point: \ in its head, \ a slip ${100 * r['head']:.0f}\%$ of "
                   rf"the time; \ a tool call malformed ${100 * r['malformed']:.0f}\%$ (the tool says so), \ silently wrong "
                   rf"${100 * r['silent']:.0f}\%$; \ a check catches a silent slip ${100 * r['catch']:.0f}\%$ of the time"
                   .replace(",", "{,}"), font_size=18).to_edge(DOWN, buff=0.2)
        if tag.width > 13.0:
            tag.width = 13.0
        n60 = {m: float(a[f"{m}_succ"][-1]) for m, _, _ in MODES}
        calls = float(a["check_calls"][-1]) / 60
        th = a["theory"]
        close = all(abs(float(a[f"{m}_p"]) - th[m]) < 0.004 for m, _, _ in MODES)
        fit = ("Each set of points falls on its own curve p to the n, with p what the error rates predict: "
               if close else "The points fall close to curves p to the n, though not always where the error rates "
               "predict, since two slips can cancel and retries use up the budget: ")
        with self.voiceover(
            "Our warehouse agent shows where the reliability comes from. Here is how often it gets the total right, "
            "against the number of prices it has to look up. <bookmark mark='a'/> Working in its head, every slip is "
            f"silent, and by sixty steps it is right only {100 * n60['head']:.0f} percent of the time. "
            "<bookmark mark='b'/> With tools, most errors announce themselves: a malformed call comes back as an "
            "error, and the agent simply tries again. Only the silent slips compound: "
            f"{100 * n60['react']:.0f} percent at sixty steps. <bookmark mark='c'/> Add a check, reading back what "
            "it fetched, and most of the silent slips get caught too: "
            f"{100 * n60['check']:.0f} percent, for {calls:.2f} calls a step. <bookmark mark='d'/> {fit}"
            "an error the loop can see is an error it can fix."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in dots[k]], lag_ratio=0.1), FadeIn(keys[k]),
                          run_time=1.5)
            vo.wait_until("d")
            self.play(*[Create(l_) for l_ in lines], run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def doubling(self):
        h = load("horizon")
        pr, hl = np.asarray(h["p_range"]), np.asarray(h["half_len"])
        err = 1 - pr
        ax = CornerAxes(x_range=[-4, -0.3, 1], y_range=[0, 4, 1], x_length=6.0, y_length=3.8, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([2.6, -0.2, 0])
        xt = VGroup(*[MathTex(t, font_size=20, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for t, v in ((r"0.01\%", -4), (r"0.1\%", -3), (r"1\%", -2), (r"10\%", -1))])
        yt = VGroup(*[MathTex(t, font_size=20, color=GREY_B).next_to(ax.c2p(-4, v), LEFT, buff=0.1)
                      for t, v in (("1", 0), ("10", 1), ("100", 2), ("1{,}000", 3), ("10{,}000", 4))])
        xn = label(r"error rate per step \ (log scale)", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yn = label(r"steps it finishes half the time", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        c = curve(ax, np.log10(err), np.log10(hl), C.BITS, 4)
        rows = [
            cmath(r"p^{\,n_{1/2}}", r"=", r"\tfrac12", font_size=34),
            cmath(r"n_{1/2}", r"=", r"\frac{\ln 2}{-\ln p}", font_size=34),
            cmath(r"-\ln p", r"=", r"(1 - p) + \tfrac{(1-p)^2}{2} + \cdots", font_size=34),
            cmath(r"n_{1/2}", r"\approx", r"\frac{0.69}{1 - p}", font_size=34),
        ]
        whys = [why(r"half the tasks done"), why(r"take logs"), why(r"Taylor series, \ $p$ near $1$"),
                why(r"halve the error, \ double the horizon")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-0.8, buff=0.45, edge=6.9)
        plot = VGroup(ax, xt, yt, xn, yn)
        ex = 0.99
        with self.voiceover(
            "Turn it around: how long a task can an agent finish half the time? <bookmark mark='a'/> Set p to the "
            "n equal to a half, <bookmark mark='b'/> and take logarithms. <bookmark mark='c'/> When p is close to "
            "one, minus log p is almost exactly one minus p, the error rate. <bookmark mark='d'/> So the half-time "
            "horizon is about zero point seven divided by the error rate per step: at ninety-nine percent, "
            f"{math.log(2) / -math.log(ex):.0f} steps. Halve the errors, and the reachable task length doubles. "
            "That is the quantity the next chapter tracks for real models."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.wait(0.2)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            # the derivation steps aside; the curve of the result appears beside its formula
            keep_row = rows[3]
            self.play(*[FadeOut(m) for m in (*rows[:3], *[w for w in whys[:3] if w is not None])],
                      keep_row.animate.scale(1.1).move_to([-4.2, 0.4, 0]),
                      *([whys[3].animate.next_to([-4.2, -0.4, 0], DOWN, buff=0.1).set_x(-4.2)] if whys[3] is not None
                        else []))
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn))
            self.play(Create(c), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()
