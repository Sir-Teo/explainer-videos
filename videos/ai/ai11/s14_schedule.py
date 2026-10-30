from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.charopt import WARMUP, lr_factor
from videos.ai.ai11.common import PART, SCHED_COLORS, bits_axes, growing, lag, load, step_counter, takeaway_card

CON, COS, WSD, SMALL = SCHED_COLORS["constant"], SCHED_COLORS["cosine"], SCHED_COLORS["wsd"], SCHED_COLORS["small"]
NAMES = {"constant": r"constant", "cosine": r"cosine", "wsd": r"warmup--stable--decay", "small": r"constant, \ $\eta/5$"}
SAYK = {"constant": "constant", "cosine": "cosine", "wsd": "warmup–stable–decay", "small": "small constant"}


class Schedule(VoiceoverScene):
    def construct(self):
        self.card()
        self.shapes()
        self.river()
        self.decompose()
        self.charmodel()
        self.takeaway()

    def card(self):
        c = chapter_card(13, r"Schedules and the river valley", r"How should the step size change over a run?", part=PART)
        with self.voiceover("Chapter thirteen. Schedules, and the river valley."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def shapes(self):
        S = 4000
        ax = CornerAxes(x_range=[0, S, 1000], y_range=[0, 1.1, 0.5], x_length=7.0, y_length=3.0, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-2.6, 0.6, 0])
        ks = np.arange(1, S + 1, 10)
        shp = {k: curve(ax, ks, [lr_factor(int(x), S, k) for x in ks], SCHED_COLORS[k], 3.5) for k in ("constant", "cosine", "wsd")}
        yl = label(r"learning rate \ (fraction of the peak)", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        xl = label(r"step", font_size=20, color=GREY_A).next_to(ax, DOWN, buff=0.12)
        lg = VGroup(*[label(NAMES[k], font_size=22, color=SCHED_COLORS[k]) for k in ("constant", "cosine", "wsd")])
        lg.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.6, 1.6, 0])
        ramp = SurroundingRectangle(Line(ax.c2p(0, 0), ax.c2p(WARMUP * 4, 1.05)), color=WHITE, buff=0.06, corner_radius=0.05,
                                    stroke_width=1.5)
        warm = definition_card(r"warmup", r"the first steps, \ tiny and growing: \ the weights are random, \ Adam's "
                               r"running sizes are not yet known, \ and the early landscape is sharp", width=5.6,
                               font_size=20, color=WHITE).move_to([3.6, -1.9, 0])
        cites = cite(r"I.~Loshchilov \& F.~Hutter, SGDR (2016); \ X.~Zhai et al.\ (2022); \ S.~Hu et al., MiniCPM (2024); "
                     r"\ D.~Kalra \& M.~Barkeshli (2024)", corner=DL)
        with self.voiceover(
            "Chapter three's lesson was that a constant step ends in a cloud, and only a shrinking step settles. So "
            "real runs change the learning rate as they go. <bookmark mark='a'/> Almost all begin with a warmup: a "
            "few hundred tiny, growing steps, while the weights are random, Adam's running sizes are still unknown, "
            "and, as Chapter five showed, the landscape is sharp. <bookmark mark='b'/> For years the standard was a "
            "cosine, from Ilya Loshchilov and Frank Hutter in 2016: glide smoothly from the peak to zero. "
            "<bookmark mark='c'/> The newer standard holds the rate flat for most of the run and decays it only at "
            "the end: warmup, stable, decay, popularized by the MiniCPM team in 2024."
        ) as vo:
            self.play(Create(ax), FadeIn(yl), FadeIn(xl), Create(shp["constant"]), FadeIn(lg[0]), FadeIn(cites))
            vo.wait_until("a")
            self.play(Create(ramp), FadeIn(warm, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Create(shp["cosine"]), FadeIn(lg[1]))
            vo.wait_until("c")
            self.play(Create(shp["wsd"]), FadeIn(lg[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def river(self):
        r = load("river")
        xs = np.asarray(r["grid_x"])
        fl = np.asarray(r["floor_y"])
        ax = Axes(x_range=[-1, 13, 2], y_range=[-2.2, 2.2, 1], x_length=12.0, y_length=4.4, tips=False,
                  axis_config={"stroke_width": 0}).move_to(DOWN * 0.6)
        A = float(r["A"])

        def L(x, y):
            return 0.5 * math.log1p(math.exp(-(x - 6.0))) + 0.5 * A * (y - 0.8 * math.sin(0.5 * x)) ** 2

        cont = contour_lines(ax, L, (-1, 13), (-2.2, 2.2), [0.05, 0.2, 0.5, 1.0, 2.0, 3.5], n=(160, 70), stroke_width=1.5)
        riv = VMobject(color="#7FD3FF", stroke_width=5).set_points_smoothly([ax.c2p(x, y) for x, y in zip(xs, fl)])
        rl = label(r"the river: \ a slow descent along the valley floor", font_size=22, color="#7FD3FF").next_to(ax.c2p(9, 1.6), UP, buff=0.0)
        hl = label(r"the hills: \ steep, \ across it", font_size=22, color=GREY_A).next_to(ax.c2p(1.5, -1.9), DOWN, buff=0.0)
        pc = VMobject(color=CON, stroke_width=2).set_points_as_corners([ax.c2p(*p) for p in np.asarray(r["path_constant"])])
        pw = VMobject(color=WSD, stroke_width=2.5).set_points_as_corners([ax.c2p(*p) for p in np.asarray(r["path_wsd"])])
        ps = VMobject(color=SMALL, stroke_width=2.5).set_points_as_corners([ax.c2p(*p) for p in np.asarray(r["path_small"])])
        lg = VGroup(label(rf"constant, \ $\eta = {float(r['eta0']):g}$", font_size=22, color=CON),
                    label(r"constant, \ $\eta/5$", font_size=22, color=SMALL),
                    label(r"warmup--stable--decay", font_size=22, color=WSD)).arrange(RIGHT, buff=0.7).to_edge(UP, buff=0.35)
        tag = note(rf"a toy: \ $L = R(x) + \tfrac{{{A:g}}}{{2}}\,(y - c(x))^2$, \ every gradient noisy; \ one run of "
                   rf"${int(r['T'])}$ steps each; \ computed").to_corner(DR, buff=0.2)
        cite_ = cite(r"K.~Wen, Z.~Li, J.~Wang, D.~Hall, P.~Liang \& T.~Ma, \textit{A River Valley Loss Landscape "
                     r"Perspective} (2024)", corner=DL)
        with self.voiceover(
            "Why does holding the rate high, then dropping it, work so well? In 2024 Kaiyue Wen and colleagues at "
            "Stanford offered a picture: a river valley. <bookmark mark='a'/> The loss has a valley floor, a river, "
            "that descends slowly, and steep hills on either side. <bookmark mark='b'/> With a large constant step, "
            "the noise throws the walker up the hills, but it travels fast down the river. <bookmark mark='c'/> With "
            "a small step it stays near the floor, but crawls. <bookmark mark='d'/> Warmup, stable, decay gets both: "
            "it travels down the river at the high rate, then drops onto the floor at the end."
        ) as vo:
            self.play(Create(cont), FadeIn(tag), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Create(riv), FadeIn(rl), FadeIn(hl))
            vo.wait_until("b")
            self.play(Create(pc), FadeIn(lg[0]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(ps), FadeIn(lg[1]), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(pw), FadeIn(lg[2]), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    def decompose(self):
        r = load("river")
        T = int(r["T"])
        kinds = list(r["kinds"])
        tot = {k: np.asarray(r[f"river_{k}"]) + np.asarray(r[f"hill_{k}"]) for k in kinds}
        hi = float(max(v[20:].max() for v in tot.values())) * 1.05
        g1 = bits_axes([0, T], [0, hi], x_length=5.6, y_length=3.6, center=[-3.4, -0.4, 0], xlabel=r"step",
                       ylabel=r"the toy's loss \ (mean of $20$ runs)", y_step=round(hi / 4, 2), yfmt=lambda v: f"{v:.2f}",
                       x_step=100, font_size=20)
        lines = {k: curve(g1.ax, np.arange(1, T + 1), tot[k], SCHED_COLORS[k], 3) for k in kinds}
        # the split at the end: river and hill, per schedule
        fin = {k: (float(np.asarray(r[f"river_{k}"])[-1]), float(np.asarray(r[f"hill_{k}"])[-1])) for k in kinds}
        mx = max(a + b for a, b in fin.values())
        bars = VGroup()
        for i, k in enumerate(kinds):
            a, b = fin[k]
            y = 1.2 - 0.75 * i
            ra = Rectangle(width=3.6 * a / mx, height=0.38, stroke_width=0, fill_color="#7FD3FF", fill_opacity=0.9)
            rb = Rectangle(width=max(0.01, 3.6 * b / mx), height=0.38, stroke_width=0, fill_color=GREY_B, fill_opacity=0.9)
            ra.move_to([2.4 + ra.width / 2, y, 0])
            rb.next_to(ra, RIGHT, buff=0)
            nm = label(NAMES[k], font_size=20, color=SCHED_COLORS[k]).next_to(ra, UP, buff=0.06).align_to(ra, LEFT)
            bars.add(VGroup(ra, rb, nm))
        bl = VGroup(label(r"river (left), \ hill (right): \ the final loss", font_size=20, color=GREY_A))
        bl.next_to(bars, UP, buff=0.25).align_to(bars, LEFT)
        hp = float(r["hill_pred"])
        hc = float(np.asarray(r["hill_constant"])[-100:].mean())
        best = min(kinds, key=lambda k: sum(fin[k]))
        pred = label(rf"constant: \ hill loss ${hc:.3f}$; \ predicted $\frac{{\eta\sigma^2}}{{4}} \big/ (1 - \frac{{\eta A}}{{2}}) = {hp:.3f}$",
                     font_size=20, color=GREY_A).next_to(bars, DOWN, buff=0.35).align_to(bars, LEFT)
        keep_in_frame(pred)
        said1 = (f"warmup–stable–decay has the lowest total loss: it has come as far down the river as the constant "
            "rate, and its hill part has collapsed. "
            if best == "wsd" else
            f"the lowest total belongs to the {SAYK[best]} schedule. ")
        with self.voiceover(
            "Split the loss into its two parts. <bookmark mark='a'/> At a constant rate, the hill part settles at a "
            f"level set by the step: {hc:.3f}, against {hp:.3f} predicted from Chapter four's stationary cloud. "
            "<bookmark mark='b'/> The river part is where the real progress is, and only a large step makes it fast. "
            "<bookmark mark='c'/> At the end, "
            + said1
            + "The decay doesn't find a better place; it removes the noise that hid how good the place already was."
        ) as vo:
            self.play(FadeIn(g1), *[Create(l_) for l_ in lines.values()], run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(bl), FadeIn(bars[0]), FadeIn(pred))
            vo.wait_until("b")
            self.play(FadeIn(bars[3]))
            vo.wait_until("c")
            self.play(FadeIn(bars[1]), FadeIn(bars[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def charmodel(self):
        s = load("schedule")
        Ls = list(s["lengths"])
        seeds = list(s["seeds"])
        const = np.asarray(s[f"const_{seeds[0]}"])
        allv = [const[const[:, 0] >= 500, 1]] + [np.asarray(s[f"cos_{S}_{seeds[0]}"])[5:, 1] for S in Ls]
        lo = float(min(v.min() for v in allv)) - 0.03
        hi = float(max(v.max() for v in allv)) + 0.03
        g = bits_axes([0, max(Ls)], [lo, hi], x_length=7.4, y_length=4.4, center=[-2.4, -0.4, 0], x_step=1000,
                      y_step=round((hi - lo) / 4, 2), yfmt=lambda v: f"{v:.2f}")
        ax = g.ax
        t = ValueTracker(0)
        cl = np.clip(const[:, 1], lo, hi)
        live = [growing(ax, const[:, 0], cl, t, CON, 2.5)]
        for S in Ls:
            c = np.asarray(s[f"cos_{S}_{seeds[0]}"])
            live.append(growing(ax, c[:, 0], np.clip(c[:, 1], lo, hi), t, COS, 2.5))
        brs = VGroup()
        for S in Ls:
            b = np.asarray(s[f"wsdcurve_{S}_{seeds[0]}"])
            k0 = int(0.8 * S)
            start = (k0, float(np.interp(k0, const[:, 0], const[:, 1])))
            pts = [start] + [tuple(p) for p in b]
            brs.add(VMobject(color=WSD, stroke_width=3.5).set_points_as_corners([ax.c2p(x, min(max(y, lo), hi)) for x, y in pts]))
        cnt = step_counter(t, ax.get_corner(UR), DL)
        mean = lambda key: float(np.mean([s[f"{key}_{sd}"] for sd in seeds]))  # noqa: E731
        rows = VGroup(label(r"held-out bits at the end, \ mean of $2$ seeds", font_size=20, color=GREY_A))
        for S in Ls:
            cf, wf = mean(f"cosfinal_{S}"), mean(f"wsdfinal_{S}")
            rows.add(label(rf"${S:,}$ steps: \ cosine ${cf:.3f}$, \ WSD ${wf:.3f}$".replace(",", "{,}"), font_size=21,
                           color=WHITE))
        rows.add(label(rf"constant, no decay, at ${max(Ls):,}$: \ ${mean('constfinal'):.3f}$".replace(",", "{,}"),
                       font_size=21, color=CON))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.4, 0.9, 0])
        keep_in_frame(rows)
        lg = VGroup(label(r"one constant run", font_size=20, color=CON), label(r"three cosine runs", font_size=20, color=COS),
                    label(r"its three cool-down branches", font_size=20, color=WSD)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        lg.next_to(rows, DOWN, buff=0.4).align_to(rows, LEFT)
        tag = note(rf"AdamW at the race's best rate, \ $\eta = {float(s['lr']):g}$; \ seed $0$ drawn").to_corner(DL, buff=0.2)
        diffs = [mean(f"wsdfinal_{S}") - mean(f"cosfinal_{S}") for S in Ls]
        spread = max(abs(float(s[f"cosfinal_{S}_{seeds[0]}"]) - float(s[f"cosfinal_{S}_{seeds[1]}"])) for S in Ls)
        if all(abs(d) <= max(spread, 0.005) for d in diffs):
            verdict = ("at every length the cool-down branch matches the cosine run trained for exactly that long, to "
                       "within the difference between seeds.")
        elif all(d < 0 for d in diffs):
            verdict = "at every length the cool-down branch beats the cosine run trained for exactly that long."
        else:
            verdict = ("the cool-down branches and the cosine runs trade places: neither schedule wins at every "
                       "length.")
        drop = mean(f"constfinal") - mean(f"wsdfinal_{max(Ls)}")
        with self.voiceover(
            "Now on our character model, with AdamW. Three cosine runs, one for each length: a thousand, two "
            "thousand and four thousand steps. And a single constant-rate run, with a branch leaving it at four "
            "fifths of each length to cool down. <bookmark mark='a'/> The constant run plateaus. Each branch drops "
            f"sharply as its rate falls: at the end, by {drop:.2f} bits below the constant run. "
            f"<bookmark mark='b'/> The verdict: {verdict} "
            "<bookmark mark='c'/> And one constant run gave all three. That is why scaling-law studies like part "
            "twelve's use it: a whole family of finished models for the price of one run."
        ) as vo:
            self.play(FadeIn(g), FadeIn(lg), FadeIn(tag))
            self.add(*live, cnt)
            self.play(t.animate.set_value(max(Ls)), run_time=6.0, rate_func=linear)
            for m_ in live + [cnt]:
                m_.clear_updaters()
            vo.wait_until("a")
            self.play(*[Create(b) for b in brs], run_time=1.5)
            vo.wait_until("b")
            self.play(lag([FadeIn(r_) for r_ in rows], lag_ratio=0.25), run_time=2)
            vo.wait_until("c")
            self.play(Indicate(brs, color=WHITE, scale_factor=1.02))
        self.wait(0.3)
        self.clear_scene()

    def takeaway(self):
        t = takeaway_card(r"Travel at a high rate, \ settle at the end",
                          r"A high rate moves fast down the river while noise keeps it up the hills; \ decaying removes "
                          r"the noise. \ Warmup--stable--decay does it at any length, \ from one run.",
                          r"Next: \ can we skip the schedule altogether?")
        with self.voiceover(
            "So a high learning rate travels; a falling one settles; and warmup, stable, decay lets you decide when "
            "to settle after the fact. Can we drop the schedule altogether?"
        ):
            self.play(FadeIn(t[0], shift=UP * 0.2))
            self.play(FadeIn(t[1]))
        self.wait(0.3)
        self.clear_scene()
