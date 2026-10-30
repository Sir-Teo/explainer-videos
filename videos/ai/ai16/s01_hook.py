from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import HISTC, INDEXC, MONO, PART, ROUTER, billions, load


class Hook(VoiceoverScene):
    def construct(self):
        self.experts()
        self.era()
        self.plan()

    # ------------------------------------------------------------------
    def experts(self):
        c = load("configs")
        ds = next(r for r in c["rows"] if r["key"] == "dsv3")
        k3 = next(r for r in c["rows"] if r["key"] == "kimik3")
        n, k = int(ds["experts"]), int(ds["k"])
        cells = VGroup(*[Square(0.27, stroke_width=0.8, stroke_color=GREY_D, fill_color=GREY_D, fill_opacity=0.25)
                         for _ in range(n)]).arrange_in_grid(rows=8, cols=32, buff=0.07).move_to(DOWN * 0.3)
        shared = Square(0.5, stroke_color=C.SHARED_EXPERT, stroke_width=2, fill_color=C.SHARED_EXPERT, fill_opacity=0.5)
        shared.next_to(cells, LEFT, buff=0.35)
        sl = label(r"shared", font_size=18, color=C.SHARED_EXPERT).next_to(shared, DOWN, buff=0.08)
        words = ["Spade", "looked", "at", "the", "girl", "for", "a", "long", "moment", "and", "then", "smiled"]
        g = np.random.default_rng(3)
        head = VGroup(label(rf"DeepSeek-V3 \ (December 2024): \ ${billions(ds['total'])}$ parameters, \ "
                            rf"${n}$ experts in each expert layer", font_size=30),
                      label(rf"each token uses ${k}$ of them, \ and one shared: \ ${billions(ds['active'])}$ "
                            rf"\ (${100 * ds['frac']:.1f}\%$)", font_size=28, color=C.BITS)).arrange(DOWN, buff=0.15)
        head.to_edge(UP, buff=0.35)
        tag = note(r"which experts light up: \ illustrative").to_corner(DR, buff=0.25)
        k3l = label(rf"Kimi K3 \ (July 2026): \ ${billions(k3['total'])}$, \ ${k3['k']}$ of ${k3['experts']}$ experts "
                    rf"and ${k3['shared']}$ shared: \ ${100 * k3['frac']:.1f}\%$ per token", font_size=24,
                    color=GREY_A).to_edge(DOWN, buff=0.45)
        tok = Text("", font=MONO, font_size=30)
        with self.voiceover(
            "DeepSeek-V3 has six hundred and seventy-one billion parameters. <bookmark mark='a'/> But for each "
            f"token it reads, it uses only {ds['active'] / 1e9:.0f} billion of them. Each of its expert layers "
            f"holds {n} small networks, called experts, and a router sends each token to just {k} of them, plus one "
            "that everyone shares. <bookmark mark='b'/> Watch: every word lights up a different few. "
            "<bookmark mark='c'/> And the models keep getting sparser. Kimi K3, released in July 2026, has "
            f"{k3['experts']} experts in a layer and uses {k3['k']} of them, plus {k3['shared']} shared: "
            f"{100 * k3['frac']:.1f} percent of its weights for each token."
        ) as vo:
            self.play(FadeIn(head[0]), LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.003), FadeIn(shared),
                      FadeIn(sl), FadeIn(tag), run_time=2.0)

            def route(w, rt=1.0):
                nonlocal tok
                pick = g.choice(n, k, replace=False)
                t = data_text(w, font=MONO, font_size=34, color=C.BITS).next_to(cells, DOWN, buff=0.35)
                self.play(FadeOut(tok), FadeIn(t), *[cells[i].animate.set_fill(C.BITS, opacity=0.9) for i in pick],
                          shared.animate.set_fill(opacity=0.9), run_time=0.45 * rt)
                self.play(*[cells[i].animate.set_fill(GREY_D, opacity=0.25) for i in pick],
                          shared.animate.set_fill(opacity=0.5), run_time=0.35 * rt)
                tok = t

            for w in words[:3]:
                route(w, 1.6)
            vo.wait_until("a")
            self.play(FadeIn(head[1]))
            for w in words[3:6]:
                route(w, 1.3)
            vo.wait_until("b")
            for w in words[6:]:
                route(w)
            vo.wait_until("c")
            self.play(FadeOut(tok), FadeIn(k3l, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def era(self):
        """How we got here: three threads of sparsity, 1990 to 2026 (dates of the papers and releases)."""
        lanes = [
            (r"experts", ROUTER, [
                (1991, r"Jacobs, Jordan, \\ Nowlan \& Hinton"), (2017, r"Shazeer: \\ sparse, $137$B"),
                (2020.5, r"GShard"), (2021.1, r"Switch: \\ $1.6$T"), (2023.95, r"Mixtral"),
                (2024.95, r"DeepSeek-V3"), (2026.5, r"Kimi K3")]),
            (r"attention", INDEXC, [
                (2019.3, r"Sparse \\ Transformer"), (2020.3, r"Longformer, \\ BigBird"), (2023.7, r"sliding \\ window"),
                (2025.1, r"NSA, \ MoBA"), (2025.75, r"DSA"), (2026.3, r"DeepSeek-V4")]),
            (r"weights", C.TRUE_P, [
                (1990, r"Optimal Brain \\ Damage"), (2015.5, r"pruning \\ AlexNet"), (2018.2, r"lottery \\ tickets"),
                (2020.4, r"$2{:}4$ on \\ the A100"), (2023.1, r"SparseGPT, \\ Wanda")]),
        ]
        x0, x1, T0, TB, T1 = -4.6, 6.4, 1988, 2015, 2027.3
        xb = x0 + 2.6  # 1988-2015 squeezed into the first 2.6 units, the busy decade gets the rest

        def X(t):
            if t <= TB:
                return x0 + (xb - x0) * (t - T0) / (TB - T0)
            return xb + (x1 - xb) * (t - TB) / (T1 - TB)

        head = label(r"How we got here: \ three kinds of sparsity", font_size=34).to_edge(UP, buff=0.3)
        rows = VGroup()
        ys = [1.45, -0.5, -2.45]
        for (name, col, evs), y in zip(lanes, ys):
            ln = Line([x0, y, 0], [x1, y, 0], color=GREY_D, stroke_width=2)
            nm = label(name, font_size=26, color=col).next_to([x0, y, 0], LEFT, buff=0.35)
            ev = VGroup()
            for j, (t, txt) in enumerate(evs):
                d = Dot([X(t), y, 0], radius=0.07, color=col)
                lab = label(txt, font_size=16, color=col)
                lab.next_to(d, UP if j % 2 == 0 else DOWN, buff=0.12 if (j // 2) % 2 == 0 else 0.62)
                lab.set_x(min(max(lab.get_x(), -4.2 + lab.width / 2), 6.9 - lab.width / 2))
                ev.add(VGroup(d, lab))
            rows.add(VGroup(ln, nm, ev))
        years = VGroup(*[Text(str(t), font_size=16, color=GREY_B).move_to([X(t), -3.8, 0]) for t in (1990, 2000, 2015, 2020, 2025)])
        ticks = VGroup(*[DashedLine([X(t), 2.4, 0], [X(t), -3.6, 0], dash_length=0.05, stroke_width=1, color=GREY_D)
                         for t in (1990, 2000, 2015, 2020, 2025)])
        with self.voiceover(
            "How did we get here? Three threads, which this part follows. <bookmark mark='a'/> The first is experts. "
            "In 1991 Robert Jacobs, Michael Jordan, Steven Nowlan and Geoffrey Hinton proposed a gate that picks "
            "which of several networks should answer. <bookmark mark='b'/> In 2017 Noam Shazeer and colleagues, "
            "with Hinton again, made it sparse: thousands of experts, only a few run per token, a hundred and "
            "thirty-seven billion parameters. <bookmark mark='c'/> Google scaled it with GShard and the Switch "
            "Transformer, to a trillion and a half parameters; Mixtral made it open in 2023, and DeepSeek-V3 made it "
            "the frontier's standard. <bookmark mark='d'/> The second thread is attention that reads only some of "
            "the past: fixed patterns from 2019, sliding windows, and in 2025 patterns the model learns to choose. "
            "<bookmark mark='e'/> The third is the oldest: removing weights. Yann LeCun's optimal brain damage in "
            "1990, the lottery tickets of 2018, and the two-in-four pattern NVIDIA built into its chips in 2020."
        ) as vo:
            self.play(FadeIn(head), FadeIn(years), FadeIn(ticks), *[FadeIn(VGroup(r[0], r[1])) for r in rows])
            vo.wait_until("a")
            self.play(FadeIn(rows[0][2][0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[0][2][1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(e) for e in rows[0][2][2:]], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(e) for e in rows[1][2]], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(e) for e in rows[2][2]], lag_ratio=0.4), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Sparsity", font_size=50).to_edge(UP, buff=0.5)
        smap = series_map(current=PART, done=PART - 1).scale(0.8).move_to(DOWN * 0.6)
        obj = objectives_card([
            r"the mixture of experts: \ the 1991 idea, \ top-$k$ gates and the router's gradient, \ ours trained",
            r"keeping experts busy: \ collapse, \ Switch's loss derived, \ DeepSeek's loss-free bias, \ fine-grained "
            r"and shared experts",
            r"capacity and dropped tokens; \ experts across chips; \ counting parameters; \ upcycling",
            r"what experts learn; \ mixture-of-depths",
            r"sparse attention: \ windows, \ NSA's and MoBA's blocks, \ DeepSeek's indexer, \ trained on a recall task",
            r"sparse weights: \ lottery tickets, \ $2{:}4$ sparsity; \ sparse activations; \ the frontier",
        ], font_size=24)
        with self.voiceover(
            "This is Part 16 of AI, Built: using only some of a model at a time. <bookmark mark='a'/> In this part: "
            "the mixture of experts, from its 1991 origin to the router's gradient, trained here on our own "
            "characters; how to keep every expert busy, with Switch's loss derived and DeepSeek's loss-free bias; "
            "capacity, chips and counting; what experts learn, and mixture-of-depths; attention that reads only "
            "some of the past, trained on a recall task; and sparse weights and activations, from lottery tickets "
            "to the two-in-four pattern. Every experiment runs on this computer."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
