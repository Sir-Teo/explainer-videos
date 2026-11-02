from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import (DENSEC, EXPERT_COLORS, MOEC, MONO, PART, ROUTER, TOTALC, expert_row, load, ms,
                                   seed_curves, show, take_away)

NAMES = {"dense_active": (r"dense, \ the mixture's arithmetic", DENSEC),
         "moe": (r"mixture: \ $2$ of $8$ experts", MOEC),
         "dense_total": (r"dense, \ the mixture's parameters", TOTALC)}


class Ours(VoiceoverScene):
    def construct(self):
        self.card()
        self.models()
        self.race()
        self.routes()
        self.worth()

    def card(self):
        card = chapter_card(3, r"A mixture, trained", r"Does it beat a dense model at the same cost?", part=PART)
        with self.voiceover("Chapter three. A mixture, trained."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def models(self):
        m = load("moe")
        cols = VGroup()
        specs = [("dense_active", r"one feed-forward layer \\ of width $256$", 1, 1),
                 ("moe", r"$8$ experts of width $128$, \\ $2$ per character", 8, 2),
                 ("dense_total", r"one feed-forward layer \\ of width $1{,}024$", 1, 1)]
        for key, desc, n, k in specs:
            nm, col = NAMES[key]
            c = m[f"{key}_counts"]
            if n == 1:
                w = 0.6 if key == "dense_active" else 2.4
                pic = Rectangle(width=w, height=0.9, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.6)
            else:
                pic = expert_row(n, lit=(2, 5), size=0.26, color=col, buff=0.04)
            box = VGroup(label(nm, font_size=28, color=col), pic.scale(1.4), label(desc, font_size=24, color=GREY_A),
                         label(rf"${c['total']:,}$ parameters".replace(",", "{,}"), font_size=26, color=WHITE),
                         label(rf"${c['active']:,}$ used per character".replace(",", "{,}"), font_size=26, color=C.BITS),
                         label(rf"${m[f'{key}_flops'] / 1e6:.2f}$ MFLOP per character, \ training", font_size=22,
                               color=GREY_B)).arrange(DOWN, buff=0.25)
            cols.add(box)
        cols.arrange(RIGHT, buff=0.6).move_to([0, -0.3, 0])
        if cols.width > 13.0:
            cols.scale_to_fit_width(13.0)
        head = label(r"three character models: \ Part 13's transformer, \ small \ ($d = 64$, \ $2$ blocks, \ $64$ "
                     r"characters of context)", font_size=24).to_edge(UP, buff=0.35)
        tag = note(r"each trained $2{,}000$ steps of $32 \times 64$ characters from the thirty novels; \ three seeds",
                   font_size=18).to_edge(DOWN, buff=0.3)
        ca, cm, ct = (m[f"{k}_counts"] for k in ("dense_active", "moe", "dense_total"))
        with self.voiceover(
            "Now we build one. Part 13's transformer, shrunk to fit a laptop: two blocks, sixty-four numbers wide, "
            "reading sixty-four characters of the thirty novels. <bookmark mark='a'/> In the first model, each "
            "block's feed-forward layer is dense, two hundred and fifty-six wide. <bookmark mark='b'/> In the "
            "mixture it becomes eight experts, each half as wide, and a router picks two for each character: the "
            f"same arithmetic per character, about {cm['active'] / 1e3:.0f} thousand parameters used, but "
            f"{cm['total'] / 1e3:.0f} thousand in all. <bookmark mark='c'/> And the third is a dense model with "
            "all those parameters, one feed-forward layer four times as wide, which does three times the arithmetic. "
            "Each is trained three times, from three seeds, on exactly the same characters."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for i, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(cols[i], shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def race(self):
        m = load("moe")
        keys = ["dense_active", "moe", "dense_total"]
        D = {k: np.asarray(m[f"{k}_curve"], float) for k in keys}
        steps = D["moe"][0, :, 0]
        total = float(steps[-1])
        displayed = {k: D[k][:, 1:].copy() for k in keys}  # initialization omitted; retain every displayed value
        allv = np.concatenate([displayed[k][:, :, 1].ravel() for k in keys])
        lo = math.floor((allv.min() - 0.05) * 4) / 4
        hi = math.ceil((allv.max() + 0.05) * 4) / 4
        tick = 0.5 if hi - lo > 1.5 else 0.25
        ax = Axes(x_range=[0, total, 500], y_range=[lo, hi, tick], x_length=7.6, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.9, -0.3, 0])
        yl = VGroup(*[MathTex(f"{v:.2f}", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in np.arange(lo, hi + 1e-9, tick)])
        ax.y_axis.set_stroke(opacity=1)
        xv = VGroup(*[MathTex(f"{int(v):,}".replace(",", "{,}"), font_size=20, color=GREY_B).next_to(ax.c2p(v, lo), DOWN, buff=0.1)
                      for v in (0, 1000, total)])
        xl = label(r"training steps", font_size=22, color=GREY_A).next_to(xv, DOWN, buff=0.1)
        yn = label(r"held-out bits per character \\ $96$ fixed windows; initialization omitted \\ "
                   r"lines: mean of $3$ seeds; bands: lowest to highest", font_size=18,
                   color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)

        lines = {k: seed_curves(ax, displayed[k], NAMES[k][1]) for k in keys}
        names = VGroup(*[label(NAMES[k][0], font_size=22, color=NAMES[k][1]) for k in keys]).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        names.move_to([4.6, 1.2, 0])
        keep_in_frame(names)
        final_note = label(r"final means: $400$ fixed windows", font_size=18, color=GREY_A)
        final_note.next_to(names, UP, buff=0.2).align_to(names, LEFT)
        keep_in_frame(final_note)
        mv, av, tv = (ms(m[f"{k}_valid"]) for k in ("moe", "dense_active", "dense_total"))
        finals = VGroup(*[label(rf"${ms(m[f'{k}_valid'])[0]:.3f}$", font_size=22, color=NAMES[k][1]) for k in keys])
        finals.arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(names, RIGHT, buff=0.25)
        a_, b_ = D["dense_active"].mean(0), D["moe"].mean(0)
        ahead = [i for i in range(1, len(b_)) if all(b_[j, 1] < a_[j, 1] for j in range(i, len(b_)))]
        when = int(b_[ahead[0], 0]) if ahead else None
        wins = int(m["wins_active"])
        if mv[0] < av[0] and wins == 3 and when is not None:
            v1 = (f"The mixture is ahead of the dense model with the same arithmetic at the saved checkpoint at step {when:,} "
                  f"and every later saved checkpoint, in every seed: {mv[0]:.3f} bits a character at the end, against {av[0]:.3f}. ")
        elif mv[0] < av[0]:
            v1 = (f"On average the mixture ends ahead of the dense model with the same arithmetic, {mv[0]:.3f} bits "
                  f"against {av[0]:.3f}, but only in {wins} of the 3 seeds. ")
        else:
            v1 = (f"The mixture does not beat the dense model with the same arithmetic: {mv[0]:.3f} bits against "
                  f"{av[0]:.3f}. ")
        if tv[0] < mv[0]:
            v2 = (f"The dense model with all the parameters does better still, {tv[0]:.3f}, as it should: it does three "
                  f"times the work. The mixture gets {100 * (av[0] - mv[0]) / max(av[0] - tv[0], 1e-9):.0f} percent of "
                  "the way there, for a third of the arithmetic.")
        else:
            v2 = (f"And the dense model with all the parameters, doing three times the arithmetic, ends at {tv[0]:.3f}: "
                  "no better than the mixture, after the same short training.")
        with self.voiceover(
            "Here are all nine runs. Shown are seven post-initialization checkpoints on ninety-six fixed held-out windows; "
            "each line is the mean of three seeds, and the band runs from the best seed to the worst. "
            "Final scores at right use four hundred windows. <bookmark mark='a'/> " + v1
            + "<bookmark mark='b'/> " + v2
        ) as vo:
            self.play(Create(ax), FadeIn(yl), FadeIn(xv), FadeIn(xl), FadeIn(yn), FadeIn(final_note))
            self.play(FadeIn(lines["dense_active"]), FadeIn(names[0]), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(lines["moe"]), FadeIn(names[1]), FadeIn(finals[:2]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(lines["dense_total"]), FadeIn(names[2]), FadeIn(finals[2]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def routes(self):
        m = load("moe")
        chars = [str(c_) for c_ in m["route_chars"]]
        R = np.asarray(m["routes"], float)  # snaps, layers, chars, E
        steps = [int(s) for s in m["route_steps"]]
        L, E = R.shape[1], R.shape[3]
        cell = 0.255

        def grid(k):
            g = VGroup()
            for li in range(L):
                for i in range(len(chars)):
                    for j in range(E):
                        g.add(Square(cell, stroke_width=0.3, stroke_color=GREY_D, fill_color=EXPERT_COLORS[j],
                                     fill_opacity=0.04 + 0.9 * float(R[k, li, i, j]))
                              .move_to([i * cell, -j * cell - li * (E * cell + 0.75), 0]))
            return g.center().move_to(DOWN * 0.35)

        cur = grid(0)
        n_ = len(chars) * E
        names = VGroup(*[data_text(show(c_), font=MONO, font_size=18, color=C.BITS if c_ in "aeiou" else GREY_A)
                         .next_to(cur[i * E], UP, buff=0.06) for i, c_ in enumerate(chars)])
        layer_l = VGroup(*[label(rf"block {li + 1}", font_size=20, color=GREY_A).next_to(cur[li * n_], LEFT, buff=0.45)
                           for li in range(L)])
        el = VGroup(*[MathTex(rf"E_{j + 1}", font_size=16, color=EXPERT_COLORS[j]).next_to(cur[li * n_ + j], LEFT, buff=0.06)
                      for li in range(L) for j in range(E)])
        t = ValueTracker(0)
        cnt = always_redraw(lambda: label(rf"training step ${int(t.get_value()):,}$".replace(",", "{,}"), font_size=26,
                                          color=WHITE).to_edge(UP, buff=0.3))
        note_ = note(r"first seed; \ columns: the character just read; \ rows: the experts \\ "
                     r"brightness: share of both routing choices \ (at most $50\%$ per expert)",
                     font_size=18).to_edge(DOWN, buff=0.25)
        sharp = [float(R[k].max(-1).mean()) for k in range(len(steps))]
        settle = (f"By the end the corresponding share is {100 * sharp[-1]:.0f} percent. "
                  "The routing patterns rearrange during training; this share is not a confidence probability. ")
        with self.voiceover(
            "Here is the first seed's routing replay: which experts receive each common character, in both blocks. "
            "Each token has two distinct choices, and shares count both slots, so any expert's share is at most fifty percent. "
            "<bookmark mark='a'/> With randomly initialized parameters the choices are already concentrated by character: "
            f"the average largest expert share is {100 * sharp[0]:.0f} percent. "
            f"<bookmark mark='b'/> At the saved checkpoint at step {steps[2]}, it is {100 * sharp[2]:.0f} percent. "
            "<bookmark mark='c'/> " + settle + "<bookmark mark='q'/>What the experts end up doing is chapter ten's question."
        ) as vo:
            self.play(FadeIn(cur), FadeIn(names), FadeIn(layer_l), FadeIn(el), FadeIn(note_))
            self.add(cnt)
            vo.wait_until("a")
            for k, mk in zip(range(1, len(steps)), (None, "b", None, None, "c", None, None)):
                if mk:
                    vo.wait_until(mk)
                self.play(Transform(cur, grid(k)), t.animate.set_value(steps[k]), run_time=1.3)
        self.wait(0.4)
        self.remove(cnt)
        self.clear_scene()

    # ------------------------------------------------------------------
    def worth(self):
        m = load("moe")
        keys = ["dense_active", "moe", "dense_total"]
        sp = load("speed")
        secs = {k: float(sp[k]) * 1e3 for k in keys}  # milliseconds per training step
        fl = {k: float(m[f"{k}_flops"]) for k in keys}
        rows = VGroup()
        for i, k in enumerate(keys):
            nm, col = NAMES[k]
            bw = 1.6 * fl[k] / max(fl.values())
            tw = 1.6 * secs[k] / max(secs.values())
            r = VGroup(label(nm, font_size=22, color=col),
                       Rectangle(width=bw, height=0.3, stroke_width=0, fill_color=col, fill_opacity=0.85),
                       label(rf"${fl[k] / 1e6:.2f}$ MFLOP", font_size=20, color=col),
                       Rectangle(width=tw, height=0.3, stroke_width=0, fill_color=GREY_C, fill_opacity=0.85),
                       label(rf"${secs[k]:.0f}$ ms", font_size=20, color=GREY_A))
            r[0].move_to([-2.4, -i * 0.8, 0], aligned_edge=RIGHT)
            r[1].move_to([-2.1 + bw / 2, -i * 0.8, 0])
            r[2].next_to(r[1], RIGHT, buff=0.12)
            r[3].move_to([2.7 + tw / 2, -i * 0.8, 0])
            r[4].next_to(r[3], RIGHT, buff=0.12)
            rows.add(r)
        rows.scale(1.35)
        rows.scale_to_fit_width(min(rows.width, 12.6)).move_to([0, 0.4, 0])
        h1 = label(r"arithmetic per character", font_size=26, color=GREY_A).next_to(rows, UP, buff=0.5).set_x(rows[0][1].get_x() + 0.8)
        h2 = label(r"time per training step here \ (one CPU core)", font_size=26, color=GREY_A).next_to(rows, UP, buff=0.5).set_x(rows[0][3].get_x() + 0.8)
        keep_in_frame(h1)
        keep_in_frame(h2)
        slow = secs["moe"] / secs["dense_active"]
        howlong = (f"{slow:.1f} times as long as the dense model's. " if slow > 1.15 else
                   "about as long as the dense model's. ")
        ta = take_away(r"sparse arithmetic is not free time: \ the gains need hardware and kernels built for routing",
                       color=ROUTER, font_size=24)
        with self.voiceover(
            "One caution before we celebrate. <bookmark mark='a'/> The mixture does the same arithmetic as the "
            "small dense model, but on this computer a training step takes "
            + howlong + "<bookmark mark='h'/>Sorting tokens by expert, gathering them, and scattering the answers back costs time that the "
            "arithmetic count doesn't see. <bookmark mark='b'/> Big labs win the time back with kernels and hardware "
            "built for routing, and lose some of it to moving tokens between chips, chapter eight's subject."
        ) as vo:
            self.play(FadeIn(h1), FadeIn(h2), *[FadeIn(r_[:3]) for r_ in rows])
            vo.wait_until("a")
            self.play(*[FadeIn(r_[3:]) for r_ in rows])
            vo.wait_until("b")
            self.play(FadeIn(ta))
        self.wait(0.3)
        self.clear_scene()
