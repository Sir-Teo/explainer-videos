from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import (DROPC, EXPERT_COLORS, F, HISTC, MODE_COLOR, MODES, PART, ROUTER, load, ms,
                                   take_away)


class Capacity(VoiceoverScene):
    def construct(self):
        self.card()
        self.buffers()
        self.dropped()
        self.sweep()
        self.trained()

    def card(self):
        card = chapter_card(7, r"Capacity and dropped tokens", r"What happens when too many tokens want one expert?",
                            part=PART)
        with self.voiceover("Chapter seven. Capacity, and dropped tokens."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def buffers(self):
        E, cap = 6, 4
        want = [3, 6, 2, 4, 1, 5]  # illustrative: tokens routed to each expert
        bins = VGroup()
        for i, w in enumerate(want):
            col = EXPERT_COLORS[i]
            slots = VGroup(*[Square(0.36, stroke_color=GREY_C, stroke_width=1.2) for _ in range(cap)]).arrange(UP, buff=0.04)
            toks = VGroup()
            for j in range(w):
                sq = Square(0.3, stroke_width=0, fill_color=col if j < cap else DROPC, fill_opacity=0.9)
                if j < cap:
                    sq.move_to(slots[j])
                else:
                    sq.next_to(slots, UP, buff=0.12 + 0.36 * (j - cap))
                toks.add(sq)
            lab = MathTex(rf"E_{i + 1}", font_size=26, color=col).next_to(slots, DOWN, buff=0.12)
            bins.add(VGroup(slots, toks, lab))
        bins.arrange(RIGHT, buff=0.45, aligned_edge=DOWN).move_to([-3.2, -1.0, 0])
        capl = DashedLine(bins.get_left() + LEFT * 0.2 + UP * (bins[0][0].get_top()[1] - bins.get_center()[1]),
                          bins.get_right() + RIGHT * 0.2 + UP * (bins[0][0].get_top()[1] - bins.get_center()[1]),
                          color=GREY_B, stroke_width=1.5)
        capl.set_y(bins[0][0].get_top()[1])
        cl = label(r"capacity $C$", font_size=20, color=GREY_B).next_to(capl, RIGHT, buff=0.1)
        colors = {r"C": GREY_A, r"c": C.BITS}
        rows = VGroup(
            cmath(r"C", r"=", r"\Big\lceil", r"c", r"\cdot \frac{kN}{E} \Big\rceil", colors=colors, font_size=34),
            label(r"$kN/E$: \ an expert's share of the batch, \ if all were equal", font_size=20, color=GREY_A),
            label(r"$c$: \ the capacity factor \ (Switch: \ $1$ to $1.25$ in training)", font_size=20, color=C.BITS),
            label(r"past capacity: \ dropped \ (the token skips the layer, \ through the residual)", font_size=20, color=DROPC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        rows.scale_to_fit_width(min(rows.width, 6.6)).move_to([3.3, 1.0, 0])
        keep_in_frame(rows)
        tag = note(r"illustrative", font_size=18).to_corner(DR, buff=0.25)
        hist = history_card(2020, r"GShard; \ Switch (2021)", r"a fixed buffer per expert, \ so every chip's work has a "
                            r"fixed size", width=4.4, color=HISTC).move_to([3.6, -1.9, 0])
        with self.voiceover(
            "On real hardware, each expert gets a buffer of fixed size, so that every chip knows its work in advance. "
            "<bookmark mark='a'/> The capacity: a factor c times an expert's fair share of the batch, k N over E. "
            "<bookmark mark='b'/> When more tokens than that choose one expert, the extra ones are dropped: they skip "
            "the layer, carried along by the residual connection, as if the layer weren't there. <bookmark mark='c'/> "
            "GShard and Switch trained with factors of one to one and a quarter, and accepted a few dropped tokens. "
            "The more uneven the router, the more it drops."
        ) as vo:
            self.play(*[FadeIn(b_[0]) for b_ in bins], *[FadeIn(b_[2]) for b_ in bins], Create(capl), FadeIn(cl),
                      FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(t_, shift=DOWN * 0.2) for b_ in bins for t_ in b_[1][:cap]], lag_ratio=0.03),
                      run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(rows[:3]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t_, shift=DOWN * 0.2) for b_ in bins for t_ in b_[1][cap:]], lag_ratio=0.2),
                      FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dropped(self):
        colors = {r"f_i": C.BALANCE, r"c": C.BITS}
        rows = [
            cmath(r"n_i", r"=", r"f_i", r"\, kN", colors=colors, font_size=38),
            cmath(r"C", r"=", r"c", r"\, \frac{kN}{E}", colors=colors, font_size=38),
            cmath(r"\text{dropped}", r"=", r"\frac{1}{kN} \sum_i \max\big(0,\ n_i - C\big)", colors=colors, font_size=38),
            cmath(r"\text{dropped}", r"=", r"\sum_i \max\Big(0,\ ", r"f_i", r"- \frac{", r"c", r"}{E}\Big)", colors=colors,
                  font_size=38),
        ]
        whys = [why(r"expert $i$ is asked for $n_i$ slots: \ its share $f_i$ of all $kN$"),
                why(r"its buffer"), why(r"whatever doesn't fit"), why(r"divide through by $kN$")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.6, buff=0.45, edge=6.8)
        pc = pause_card(r"With perfectly even routing, \ what capacity factor drops nothing? \ And with one expert at twice its share?",
                        width=8.6, font_size=24).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "How much is dropped? Expert i is asked for f i times k N slots, its share of all of them. "
            "<bookmark mark='a'/> Its buffer holds c times k N over E. <bookmark mark='b'/> Whatever doesn't fit is "
            "dropped. <bookmark mark='c'/> Divide by the number of slots, and the dropped share is the sum over experts "
            "of how far each one's share exceeds c over E. <bookmark mark='d'/> Pause and predict: with perfectly even "
            "routing, what factor drops nothing? One. And if one expert gets twice its share, a factor of one drops "
            "exactly the extra: one E-th of all the slots."
        ) as vo:
            step(0)
            for i, mk in zip((1, 2, 3), "abc"):
                vo.wait_until(mk)
                step(i)
            vo.wait_until("d")
            self.play(FadeIn(pc, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sweep(self):
        d = load("capacity")
        cfs = [float(c) for c in d["cfs"]]
        fin = [c for c in cfs if c > 0]
        xs = list(range(len(fin)))
        ax1 = Axes(x_range=[-0.3, len(fin) - 0.7, 1], y_range=[0, 0.5, 0.1], x_length=5.6, y_length=3.4, tips=False,
                   axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.4, -0.4, 0])
        drops = {k: np.asarray(d[f"{k}_drops"], float)[:, :len(fin)] for k, _, _ in MODES}
        bits = {k: np.asarray(d[f"{k}_bits"], float) for k, _, _ in MODES}
        top = max(0.1, float(max(v.max() for v in drops.values())) * 1.1)
        ax1 = Axes(x_range=[-0.3, len(fin) - 0.7, 1], y_range=[0, top, top / 4], x_length=5.6, y_length=3.4, tips=False,
                   axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.4, -0.4, 0])
        xt = VGroup(*[MathTex(f"{c:g}", font_size=22, color=GREY_B).next_to(ax1.c2p(i, 0), DOWN, buff=0.1) for i, c in enumerate(fin)])
        yt = VGroup(*[MathTex(rf"{100 * v:.0f}\%", font_size=20, color=GREY_B).next_to(ax1.c2p(-0.3, v), LEFT, buff=0.08)
                      for v in np.linspace(0, top, 5)[::2]])
        xl = label(r"capacity factor $c$", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"token-slots dropped", font_size=20, color=GREY_A).next_to(ax1, UP, buff=0.1).align_to(ax1, LEFT)
        ln1 = VGroup()
        for k, _, col in MODES:
            a = drops[k]
            ln1.add(VGroup(band(ax1, xs, a.min(0), a.max(0), col, 0.18), curve(ax1, xs, a.mean(0), col, 3)))
        # bits lost against no limit
        loss = {k: (bits[k][:, :len(fin)] - bits[k][:, -1:]) for k, _, _ in MODES}
        ltop = max(0.02, float(max(v.max() for v in loss.values())) * 1.1)
        ax2 = Axes(x_range=[-0.3, len(fin) - 0.7, 1], y_range=[0, ltop, ltop / 4], x_length=5.6, y_length=3.4, tips=False,
                   axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.4, -0.4, 0])
        xt2 = VGroup(*[MathTex(f"{c:g}", font_size=22, color=GREY_B).next_to(ax2.c2p(i, 0), DOWN, buff=0.1) for i, c in enumerate(fin)])
        yt2 = VGroup(*[MathTex(f"{v:.2f}", font_size=20, color=GREY_B).next_to(ax2.c2p(-0.3, v), LEFT, buff=0.08)
                       for v in np.linspace(0, ltop, 5)[::2]])
        xl2 = label(r"capacity factor $c$", font_size=20, color=GREY_A).next_to(xt2, DOWN, buff=0.1)
        yl2 = label(r"bits lost, \ against no limit", font_size=20, color=GREY_A).next_to(ax2, UP, buff=0.1).align_to(ax2, LEFT)
        ln2 = VGroup()
        for k, _, col in MODES:
            a = np.clip(loss[k], 0, ltop)
            ln2.add(VGroup(band(ax2, xs, a.min(0), a.max(0), col, 0.18), curve(ax2, xs, a.mean(0), col, 3)))
        key = VGroup(*[label(nm, font_size=20, color=col) for _, nm, col in MODES]).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.3)
        tag = note(r"each trained router (three seeds), \ the limit imposed afterwards; \ batches of $2{,}048$ tokens",
                   font_size=17).to_edge(DOWN, buff=0.2)
        i1 = fin.index(1.0)
        i2 = fin.index(2.0) if 2.0 in fin else len(fin) - 1
        dn, da, db = (float(drops[k][:, i1].mean()) for k in ("none", "aux", "moe"))
        ln_, la_, lb_ = (float(loss[k][:, i1].mean()) for k in ("none", "aux", "moe"))
        remain = ("Even perfect balance on average isn't balance in every batch, so some drops remain. " if db > 0.005
                  else "With the bias, almost nothing is dropped at all. ")
        if max(float(loss[k][:, i2].mean()) for k in loss) < 0.01:
            two = f"At a factor of {fin[i2]:g}, almost nothing is lost by any of them."
        else:
            two = f"Even at a factor of {fin[i2]:g}, the unbalanced router still loses {float(loss['none'][:, i2].mean()):.3f}."
        with self.voiceover(
            "We can measure this on our trained routers: impose a capacity afterwards, and count what's dropped. "
            f"<bookmark mark='a'/> At a factor of one, the unbalanced router drops {100 * dn:.0f} percent of its "
            f"token slots, the router trained with Switch's loss {100 * da:.0f} percent, and the router with the "
            f"loss-free bias {100 * db:.0f} percent. <bookmark mark='r'/>" + remain
            + f"<bookmark mark='b'/> In bits, a factor of one costs the unbalanced model {ln_:.3f} bits a character, "
            f"and the bias model {lb_:.3f}. <bookmark mark='t'/>" + two
        ) as vo:
            self.play(FadeIn(key), Create(ax1), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(tag),
                      Create(ax2), FadeIn(xt2), FadeIn(yt2), FadeIn(xl2), FadeIn(yl2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in ln1], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in ln2], lag_ratio=0.4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def trained(self):
        d = load("capacity")
        cf, nocf = ms(d["cf_train_valid"]), ms(d["nocf_train_valid"])
        tr = np.asarray(d["cf_train_drops"], float)  # seeds, time
        ax = Axes(x_range=[0, tr.shape[1] - 1, 25], y_range=[0, max(0.05, float(tr.max()) * 1.1), 0.05], x_length=6.0,
                  y_length=3.0, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.2, -0.2, 0])
        every = 20
        xs = np.arange(tr.shape[1])
        ln = VGroup(band(ax, xs, tr.min(0), tr.max(0), DROPC, 0.2), curve(ax, xs, tr.mean(0), DROPC, 3))
        yl = label(r"token-slots dropped in training, \ $c = 1$", font_size=20, color=DROPC).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        xl = label(rf"training $\to$ \ ($2{{,}}000$ steps)", font_size=20, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        res = VGroup(
            label(r"held-out bits, \ two seeds:", font_size=22, color=GREY_A),
            label(rf"no limit: \ ${nocf[0]:.3f}$", font_size=24, color=MODE_COLOR["moe"]),
            label(rf"capacity factor $1$: \ ${cf[0]:.3f}$", font_size=24, color=DROPC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.6, 0.8, 0])
        ec = VGroup(history_card(2022, r"Yanqi Zhou et al.\ (Google)", r"expert choice: \ each expert picks its top tokens, "
                                 r"\ balanced by construction \ (but it looks at the whole batch)", width=4.8,
                                 color=HISTC)).move_to([3.6, -1.7, 0])
        early, late = float(tr[:, :5].mean()), float(tr[:, -10:].mean())
        diff = cf[0] - nocf[0]
        v = (f"Trained with a capacity factor of one from the start, the router learns to fit: drops fall from "
             f"{100 * early:.0f} percent early on to {100 * late:.1f} percent at the end. " if early > late + 0.01 else
             f"Trained with a capacity factor of one, it drops about {100 * late:.1f} percent of slots throughout. ")
        w = (f"The cost: {cf[0]:.3f} bits against {nocf[0]:.3f} with no limit. " if diff > 0.002 else
             f"And it costs almost nothing: {cf[0]:.3f} bits against {nocf[0]:.3f} with no limit. ")
        with self.voiceover(
            "What if the limit is there during training? <bookmark mark='a'/> " + v + "<bookmark mark='b'/> " + w
            + "<bookmark mark='c'/> There's another way to avoid drops: let each expert choose its tokens instead, "
            "expert choice, from Yanqi Zhou and colleagues in 2022. It balances perfectly by construction, but an "
            "expert's choice depends on the whole batch, including tokens that come later, a problem chapter eleven "
            "meets again. DeepSeek-V3 drops nothing at all: its balance is good enough, and its kernels flexible "
            "enough, to take whatever arrives."
        ) as vo:
            self.play(Create(ax), FadeIn(yl), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(ln), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in res], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(ec, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
