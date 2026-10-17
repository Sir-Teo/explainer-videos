from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import MONO, billions, load


class Hook(VoiceoverScene):
    def construct(self):
        self.experts()
        self.plan()

    # ------------------------------------------------------------------
    def experts(self):
        c = load("configs")
        ds = next(r for r in c["rows"] if r["name"] == "DeepSeek-V3")
        n, k = int(ds["experts"]), int(ds["k"])
        cells = VGroup(*[Square(0.27, stroke_width=0.8, stroke_color=GREY_D, fill_color=GREY_D, fill_opacity=0.25)
                         for _ in range(n)]).arrange_in_grid(rows=8, cols=32, buff=0.07).move_to(DOWN * 0.3)
        shared = Square(0.5, stroke_color=C.INTERVAL, stroke_width=2, fill_color=C.INTERVAL, fill_opacity=0.5)
        shared.next_to(cells, LEFT, buff=0.35)
        sl = label(r"shared", font_size=18, color=C.INTERVAL).next_to(shared, DOWN, buff=0.08)
        words = ["Spade", "looked", "at", "the", "girl"]
        g = np.random.default_rng(3)
        head = VGroup(label(rf"DeepSeek-V3: \ ${billions(ds['total'])}$ parameters, \ "
                            rf"${n}$ experts in every layer", font_size=30),
                      label(rf"each token uses ${k}$ of them, \ and one shared: \ ${billions(ds['active'])}$ "
                            rf"\ (${100 * ds['frac']:.1f}\%$)", font_size=28, color=C.BITS)).arrange(DOWN, buff=0.15)
        head.to_edge(UP, buff=0.35)
        tok = Text("", font=MONO, font_size=30)
        with self.voiceover(
            "DeepSeek-V3 has six hundred and seventy-one billion parameters. <bookmark mark='a'/> But for each "
            f"token it reads, it uses only {ds['active'] / 1e9:.0f} billion of them. Every layer "
            f"holds {n} small networks, called experts, and a router sends each token to just {k} of them, plus one "
            "that everyone shares. <bookmark mark='b'/> Watch: every word lights up a different few."
        ) as vo:
            self.play(FadeIn(head[0]), LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.003), FadeIn(shared),
                      FadeIn(sl), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(head[1]))
            vo.wait_until("b")
            for w in words:
                pick = g.choice(n, k, replace=False)
                t = Text(w, font=MONO, font_size=34, color=C.BITS).next_to(cells, DOWN, buff=0.45)
                self.play(FadeOut(tok), FadeIn(t), *[cells[i].animate.set_fill(C.BITS, opacity=0.9) for i in pick],
                          shared.animate.set_fill(opacity=0.9), run_time=0.45)
                self.play(*[cells[i].animate.set_fill(GREY_D, opacity=0.25) for i in pick],
                          shared.animate.set_fill(opacity=0.5), run_time=0.35)
                tok = t
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(r"Part 13: \ Sparsity", font_size=52).to_edge(UP, buff=0.6)
        sub = label(r"routers, \ experts, \ load balancing, \ sparse attention", font_size=30, color=C.BITS)
        sub.next_to(title, DOWN, buff=0.25)
        smap = series_map(current=13, done=12).scale(0.85).move_to(DOWN * 0.9)
        with self.voiceover(
            "This part is about using only some of a model at a time: how a router chooses, how to keep every "
            "expert busy, what the experts learn, <bookmark mark='a'/> and how attention, too, can look at only "
            "what matters."
        ) as vo:
            self.play(FadeIn(title), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(smap))
        self.wait(0.5)
        self.clear_scene()
