from __future__ import annotations

import numpy as np

import json

from explainer.quant import *  # noqa: F403
from explainer.quant.house import deep as D
from explainer.tts import REPO_ROOT
from videos.quant.quant17.common import BAD, GOOD, NET, OPT, PART, REF, ask, house_lab, illustration, load


def _lsm():
    """Part 16's Longstaff-Schwartz on the same five-asset max-call, read from its cache (never recomputed here)."""
    return json.loads((REPO_ROOT / ".cache" / "quant16" / "maxcall.json").read_text())


class Stopping(VoiceoverScene, ThreeDScene):
    def construct(self):
        s = load("stopping")
        r = load("stopping_region")
        self.card()
        self.method()
        self.tunnel(r)
        self.replay(r)
        self.table(s)
        self.lab(s)

    def card(self):
        c = chapter_card(10, r"Deep optimal stopping", r"Can a network learn when to exercise?", lit=(2019,), part=PART)
        with self.voiceover("Chapter ten. Deep optimal stopping."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def method(self):
        rows = [cmath(r"V_n", r"=", r"\max\big(g_n,\ \mathbb{E}[V_{n+1} \mid X_n]\big),\quad V_N = g_N", font_size=38,
                      colors={r"V_n": OPT}),
                cmath(r"\tau_n", r"=", r"n\,F_n + \tau_{n+1}\,(1 - F_n),\qquad F_n = f_n(X_n) \in \{0, 1\}", font_size=38,
                      colors={r"\tau_n": NET}),
                cmath(r"\mathbb{E}\big[g_n F + G_{n+1}(1 - F) \mid X_n\big]", r"=",
                      r"\mathbb{E}[G_{n+1} \mid X_n] + F\,\big(g_n - \mathbb{E}[G_{n+1} \mid X_n]\big)", font_size=34,
                      colors={r"=": WHITE}),
                cmath(r"\mathbb{E}\, g_{\tau_\theta}", r"\le", r"V_0", font_size=40, colors={r"\mathbb{E}\, g_{\tau_\theta}": GOOD})]
        whys = [why(r"the Snell envelope (Parts 8 and 16): at each exercise date, the better of stopping now and the "
                    r"value of waiting"),
                why(r"Becker, Cheridito and Jentzen (2019): any stopping time is built backwards from yes-or-no decisions, "
                    r"one per date, each a function of today's state: so learn the decisions, one network per date"),
                why(r"given today's state the objective is linear in $F$, so it is maximized at $F = 1$ when the payoff beats "
                    r"the value of waiting and $F = 0$ otherwise: bang-bang. Train a sigmoid $F_\theta$ for gradients, "
                    r"then use the hard rule $F_\theta > 1/2$"),
                why(r"any rule is a real strategy, so its average payoff on fresh paths is a lower bound on the price; "
                    r"Part 16's dual gives the upper bound")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.4, buff=0.62, edge=6.9)
        with self.voiceover(
            "Part sixteen priced an American option by regressing the value of waiting. Sebastian Becker, Patrick "
            "Cheridito and Arnulf Jentzen asked a network to learn the decision itself. Start from the Snell "
            "envelope: at each exercise date, the option is worth the better of stopping now and waiting. "
            "<bookmark mark='a'/> Any stopping time can be built backwards from yes-or-no decisions, one per date, "
            "each depending only on today's state: stop now, or follow the later rule. So learn one decision network "
            "per date, starting from expiry and working back. <bookmark mark='b'/> Given today's state, the reward "
            "is linear in the decision: the value of waiting, plus the decision times the gain from stopping. So the "
            "best decision is all or nothing: stop exactly when the payoff beats the value of waiting. Training uses "
            "a soft version, a probability, so gradients flow; the final rule is hard. "
            "<bookmark mark='c'/> And any rule is a real strategy, so its average payoff on fresh paths can only be "
            "a lower bound on the price."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def tunnel(self, r):
        gr = np.asarray(r["grid"])
        regs = {int(k): np.asarray(v) for k, v in r["regions"].items()}
        dates = sorted(regs)
        ax = ThreeDAxes(x_range=[gr[0], gr[-1], 40], y_range=[gr[0], gr[-1], 40], z_range=[0, 9, 1], x_length=5.4,
                        y_length=5.4, z_length=5.0, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        st = 3
        dx = (gr[1] - gr[0]) * st
        layers = VGroup()
        for n in dates:
            R = regs[n]
            cells = VGroup()
            for i in range(0, len(gr), st):
                for j in range(0, len(gr), st):
                    if R[i, j]:
                        x, y = gr[j], gr[i]
                        cells.add(Polygon(ax.c2p(x - dx / 2, y - dx / 2, n), ax.c2p(x + dx / 2, y - dx / 2, n),
                                          ax.c2p(x + dx / 2, y + dx / 2, n), ax.c2p(x - dx / 2, y + dx / 2, n),
                                          stroke_width=0, fill_color=interpolate_color(ManimColor(GOOD), ManimColor(OPT),
                                                                                       (n - 1) / 7), fill_opacity=0.55))
            layers.add(cells)
        diag = Line(ax.c2p(gr[0], gr[0], 0), ax.c2p(gr[-1], gr[-1], 0), stroke_color=GREY_B, stroke_width=2)
        shares = [float(regs[n].mean()) for n in dates]
        hint = VGroup(label(r"asset 1, asset 2 (floor); exercise date (up, 1 to 8)", font_size=19, color=GREY_A),
                      legend([(GOOD, r"exercise now, early dates"), (OPT, r"exercise now, late dates")], font_size=17),
                      label(rf"share of the square where it stops: {100 * shares[0]:.0f}\% at date 1, "
                            rf"{100 * shares[-1]:.0f}\% at date 8", font_size=18, color=GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL, buff=0.3)
        self.set_camera_orientation(phi=62 * DEGREES, theta=-50 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(hint)
        self.remove(hint)
        with self.voiceover(
            "What does the network learn? A call on the better of two assets, nine exercise dates over three years. "
            "Here is every date's decision at once: the floor is the two asset prices, and each layer up is a later "
            "date, coloured where the network says exercise now. <bookmark mark='a'/> Each layer has two lobes: "
            "exercise when one asset is far above the strike and well ahead of the other. Between them runs a valley "
            "along the diagonal, where either asset could still end up the winner and the right to pick the better "
            "one later is worth more than the dividends given up. <bookmark mark='b'/> Fly up the tunnel toward "
            "expiry: the lobes widen and the valley narrows, as waiting is worth less and less. This is the shape "
            "Broadie and Detemple found by theory in 1997, rebuilt from simulations alone."
        ) as vo:
            self.play(Create(ax), Create(diag), FadeIn(hint[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(L_) for L_ in layers], lag_ratio=0.4, run_time=4), FadeIn(hint[1]))
            vo.wait_until("b")
            self.play(FadeIn(hint[2]))
            self.move_camera(phi=40 * DEGREES, theta=-20 * DEGREES, zoom=0.95, run_time=max(vo.remaining(0.3), 2))
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, added_anims=[FadeOut(VGroup(ax, diag, layers)),
                                                                            FadeOut(hint)], run_time=1.2)
        self.clear_scene()

    def replay(self, r):
        cv = r["curves"]
        dates = sorted((int(k) for k in cv), reverse=True)
        steps, vals, ends = [], [], []
        per = r["steps"]
        for i, n in enumerate(dates):
            ys = cv[str(n)]
            for j, y in enumerate(ys):
                steps.append(i * per + j * 50)
                vals.append(y)
            ends.append(i * per + (len(ys) - 1) * 50)
        gr = np.asarray(r["grid"])
        regs = {int(k): np.asarray(v) for k, v in r["regions"].items()}

        def frame(i):
            n = dates[max(i - 1, 0)] if i else dates[0]
            g = axes([gr[0], gr[-1]], [gr[0], gr[-1]], x_length=3.8, y_length=3.8, xlabel=r"asset 1", ylabel=r"asset 2",
                     xticks=[80, 120, 160], yticks=[80, 120, 160], font_size=12)
            R = regs[n]
            st = 2
            d = (gr[1] - gr[0]) * st
            cells = VGroup()
            for a in range(0, len(gr), st):
                for b_ in range(0, len(gr), st):
                    if R[a, b_]:
                        p0, p1 = g.ax.c2p(gr[b_] - d / 2, gr[a] - d / 2), g.ax.c2p(gr[b_] + d / 2, gr[a] + d / 2)
                        cells.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=GOOD,
                                            fill_opacity=0.6).move_to((p0 + p1) / 2))
            return VGroup(g, cells, label(rf"date {n}: trained" if i else rf"date {n}: training", font_size=18,
                                          color=GOOD).next_to(g, DOWN, buff=0.1))
        rp = TrainingReplay(np.array(steps, float), np.array(vals), frame, checkpoints=[0] + ends,
                            ylabel=r"objective (expected payoff)", xlabel=r"training, date 8 back to date 1")
        with self.voiceover(
            "Here is the training, as it ran: backwards from the last exercise date to the first, each date's "
            f"network trained for {per} steps while the later rules are held fixed. On the right, the objective, the "
            "expected payoff of the rule so far; on the left, each date's region as its network finishes. "
            "<bookmark mark='a'/> Each date's objective climbs and flattens, and each step back in time adds the "
            "value of one more chance to exercise early."
        ) as vo:
            self.play(FadeIn(rp))
            vo.wait_until("a")
            rp.play(self, run_time=max(vo.remaining(0.5), 6))
        self.wait(0.4)
        self.clear_scene()

    def table(self, s):
        d2, d5 = s["2"], s["5"]
        lsm = _lsm()["lsm"]["200000"]
        bcj = d5["reference"]
        rows_ = [(r"deep stopping (ours)", d5["lower"], d5["se"], NET, r"500 steps a date, CPU"),
                 (r"Longstaff--Schwartz (Part 16)", lsm["lower"], lsm["se"], QC.DELTA,
                  rf"{lsm['n_basis']} basis functions, 200{{,}}000 fitting paths")]
        lo = min(d5["lower"], lsm["lower"]) - 0.12
        hi = bcj["upper"] + 0.06
        g = axes([lo, hi], [-0.5, 2.5], x_length=9.6, y_length=3.0, xlabel=r"price of the five-asset Bermudan max-call",
                 xticks=[round(v, 2) for v in np.linspace(lo + 0.02, hi - 0.02, 4)], xfmt=lambda v: f"{v:.2f}",
                 yticks=[], font_size=15).move_to(UP * 0.3)
        ax = g.ax
        marks = VGroup()
        for i, (nm, v, se, col, note_) in enumerate(rows_):
            y = 2 - i
            marks.add(VGroup(Line(ax.c2p(v - 2 * se, y), ax.c2p(v + 2 * se, y), stroke_color=col, stroke_width=6),
                             Dot(ax.c2p(v, y), radius=0.08, color=col),
                             label(rf"{nm}: {v:.3f} $\pm$ {2 * se:.3f}", font_size=19, color=col).next_to(
                                 ax.c2p(lo, y), RIGHT, buff=0.1).shift(UP * 0.28)))
        bc = VGroup(Rectangle(width=ax.c2p(bcj["upper"], 0)[0] - ax.c2p(bcj["lower"], 0)[0], height=0.3, stroke_width=0,
                              fill_color=REF, fill_opacity=0.7).move_to(ax.c2p((bcj["lower"] + bcj["upper"]) / 2, 0)),
                    label(rf"Becker, Cheridito and Jentzen: [{bcj['lower']:.3f}, {bcj['upper']:.3f}]", font_size=19,
                          color=REF).next_to(ax.c2p(lo, 0), RIGHT, buff=0.1).shift(UP * 0.3))
        gap = abs(d5["lower"] - lsm["lower"])
        tie = gap < 2 * np.hypot(d5["se"], lsm["se"])
        if tie:
            verdict = "a statistical tie"
        elif d5["lower"] > lsm["lower"]:
            verdict = "the network ahead"
        else:
            verdict = "Longstaff and Schwartz ahead"
        foot = wrapped_label(rf"bars: $\pm 2$ standard errors on independent paths. Two assets: ours "
                             rf"{d2['lower']:.3f}, a binomial tree {d2['reference']['binomial']:.3f}. Their bounds used "
                             r"3{,}000 + $d$ steps of 8{,}192 paths a date on a GPU (their Table 1); ours, 500 steps on a "
                             r"shared CPU. Both of our estimates are lower bounds", 12.2, 19, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now the prices, and a fair comparison. With two assets the network's rule earns "
            f"{d2['lower']:.2f}, against {d2['reference']['binomial']:.2f} from a binomial tree. With five assets, "
            f"{d5['lower']:.3f}, and Part sixteen's Longstaff–Schwartz, on the same option with fifteen basis "
            f"functions and two hundred thousand fitting paths, {lsm['lower']:.3f}. <bookmark mark='a'/> At our "
            f"budget that is {verdict}. <bookmark mark='b'/> Both fall short of Becker, Cheridito and Jentzen's "
            f"published bounds, {bcj['lower']:.3f} to {bcj['upper']:.3f}, which used six times the steps per date, "
            "batches of eight thousand paths and a GPU. A lower bound rises with the training budget. The network's "
            "real advantages are elsewhere: it needs no hand-made basis, and the paper runs it on five hundred assets, "
            "where no regression basis can follow."
        ) as vo:
            self.play(FadeIn(g), FadeIn(marks[0]))
            self.play(FadeIn(marks[1]))
            vo.wait_until("a")
            self.wait(0.3)
            vo.wait_until("b")
            self.play(FadeIn(bc), FadeIn(foot))
        self.wait(0.5)
        self.clear_scene()

    def lab(self, s):
        card = house_lab(r"one exercise date", D.deep_stopping, "for it in range(steps):", 9)
        card.to_edge(UP, buff=0.4).to_edge(LEFT, buff=0.6)
        d2, d5 = s["2"], s["5"]
        outs = [f"d=2: lower bound {d2['lower']:.3f} +/- {2 * d2['se']:.3f}   binomial {d2['reference']['binomial']:.3f}",
                f"d=5: lower bound {d5['lower']:.3f} +/- {2 * d5['se']:.3f}"]
        with self.voiceover(
            "The House's training for one exercise date. Draw a batch of paths. Ask the later, already trained "
            "networks what each path collects if we wait. Turn this date's network into a stopping probability, and "
            "maximize the expected payoff: stop and take the payoff, or wait and take the rest. <bookmark mark='a'/> "
            "Run backwards over the dates, then evaluate the hard rule on a million fresh paths."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, outs)
        q = ask(r"both assets at 130, one date before expiry. Stop or wait?")
        with self.voiceover(
            "A question: both assets at a hundred and thirty, one date before expiry. Stop or wait? Look at the "
            "tunnel's top layer before you answer."
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
