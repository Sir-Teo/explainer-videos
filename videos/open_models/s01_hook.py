from __future__ import annotations

import datetime as dt

import numpy as np

from explainer import *  # noqa: F403
from videos.open_models.common import (
    KEYS, MAKERS, MCOLOR, NAMES, Plot, data, label, layer_strip, model, note,
)

OPEN_COLOR = "#57A8FB"  # Artificial Analysis draws open-weights models in this blue
CLOSED_COLOR = GREY_B


def year_frac(d: str) -> float:
    t = dt.date.fromisoformat(d)
    return t.year + (t.timetuple().tm_yday - 1) / 365.25


class Hook(VoiceoverScene):
    def construct(self):
        self.lb = data()["leaderboard"]
        self.race()
        self.cards()
        self.machines()
        self.roadmap()

    # ------------------------------------------------------------------
    def race(self):
        prog = self.lb["progress"]
        top = {r["name"]: r for r in self.lb["open"][:3]}
        assert list(top) == ["MiMo-V2.6-Pro", "GLM-5.3 (Max)", "Kimi K3 (Max)"]
        assert [round(r["score"]) for r in top.values()] == [46, 45, 44]
        closed_best = max((r for r in prog if not r["open"]), key=lambda r: r["score"])
        assert closed_best["name"].startswith("Claude Opus 5.5") and round(closed_best["score"]) == 58
        assert self.lb["version"] == "v4.3.2" and len(self.lb["evaluations"]) == 10

        pl = Plot((2022.8, 2026.95), (0, 62), width=8.8, height=5.0, x_ticks=[2023, 2024, 2025, 2026],
                  x_fmt=lambda v: f"{int(v)}", y_ticks=[0, 20, 40, 60]).move_to(DOWN * 0.45 + LEFT * 1.75)
        yl = label(r"Artificial Analysis Intelligence Index (v4.3.2)", font_size=26, color=GREY_A)
        yl.next_to(pl, UP, buff=0.2).align_to(pl, LEFT)
        dots_c = VGroup(*[Dot(pl.c2p(year_frac(r["release"]), r["score"]), radius=0.06, color=CLOSED_COLOR)
                          for r in prog if not r["open"]])
        dots_o = VGroup(*[Dot(pl.c2p(year_frac(r["release"]), r["score"]), radius=0.06, color=OPEN_COLOR)
                          for r in prog if r["open"]])

        def frontier(is_open, color):
            pts, best = [], 0.0
            for r in prog:
                if r["open"] != is_open:
                    continue
                x = year_frac(r["release"])
                if r["score"] > best:
                    if pts:
                        pts.append(pl.c2p(x, best))
                    best = r["score"]
                    pts.append(pl.c2p(x, best))
            pts.append(pl.c2p(2026.85, best))
            return VMobject().set_points_as_corners(pts).set_stroke(color, 3, opacity=0.8)

        fr_c, fr_o = frontier(False, CLOSED_COLOR), frontier(True, OPEN_COLOR)
        leg = VGroup(
            VGroup(Dot(color=CLOSED_COLOR), label(r"proprietary", font_size=26, color=CLOSED_COLOR)).arrange(RIGHT, buff=0.12),
            VGroup(Dot(color=OPEN_COLOR), label(r"open weights", font_size=26, color=OPEN_COLOR)).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(pl.c2p(2023.0, 52), aligned_edge=UL)
        evals = note(r"10 evaluations: agentic knowledge work, terminal coding, scientific code, research-level physics,"
                     r" long-context reasoning, \dots", font_size=22).to_edge(DOWN, buff=0.2)

        with self.voiceover(
            "Every few months, a new AI model arrives that anyone can download, not far behind the best ones that you can't. "
            "<bookmark mark='a'/> Here's that race, as tracked by Artificial Analysis. Their Intelligence Index "
            "combines ten evaluations, from agentic office work to coding in a terminal to research-level physics. "
            "<bookmark mark='p'/> Grey dots are proprietary models; <bookmark mark='o'/> blue dots are open-weights models, "
            "whose parameters anyone can download. <bookmark mark='f'/> The best open model has followed the best closed one "
            "at a distance of a few months."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(pl), FadeIn(yl), FadeIn(evals), run_time=1.5)
            vo.wait_until("p")
            self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in dots_c], lag_ratio=0.05), FadeIn(leg[0]), run_time=1.5)
            vo.wait_until("o")
            self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in dots_o], lag_ratio=0.05), FadeIn(leg[1]), run_time=1.5)
            vo.wait_until("f")
            self.play(Create(fr_c), Create(fr_o), run_time=2.5)

        tops = list(top.values())
        keys = ["mimo", "glm", "kimi"]
        pts = [pl.c2p(year_frac(r["release"]), r["score"]) for r in tops]
        rings = VGroup(*[Circle(radius=0.15, color=MCOLOR[k], stroke_width=4).move_to(p) for k, p in zip(keys, pts)])
        x_lab = pl.c2p(2026.95, 0)[0] + 0.55
        c_pt = pl.c2p(year_frac(closed_best["release"]), closed_best["score"])
        c_ring = Circle(radius=0.15, color=WHITE, stroke_width=3).move_to(c_pt)
        c_name = label(r"Claude Opus 5.5 \quad 58", font_size=28, color=GREY_A)
        c_name.move_to([x_lab, c_pt[1] + 0.25, 0], aligned_edge=LEFT)
        c_sub = note(r"best proprietary", font_size=22).next_to(c_name, DOWN, buff=0.08, aligned_edge=LEFT)
        c_lead = Line(c_ring.get_right(), c_name.get_left() + LEFT * 0.08, color=GREY_B, stroke_width=1.5)
        names, leads = VGroup(), VGroup()
        for i, (k, r, ring) in enumerate(zip(keys, tops, rings)):
            y = pl.c2p(2026, 46)[1] + 0.15 - 0.62 * i
            t = label(rf"{NAMES[k]} \quad {r['score']:.0f}", font_size=28, color=MCOLOR[k]).move_to([x_lab, y, 0],
                                                                                                  aligned_edge=LEFT)
            names.add(t)
            leads.add(Line(ring.get_right(), t.get_left() + LEFT * 0.08, color=MCOLOR[k], stroke_width=1.5))
        o_sub = note(r"top three open-weights models", font_size=22).next_to(names, DOWN, buff=0.12, aligned_edge=LEFT)
        date = label(r"as of October 8, 2026", font_size=26, color=GREY_A).to_corner(UR, buff=0.35)
        with self.voiceover(
            "<bookmark mark='d'/> As of October 2026, the top proprietary model scores about 58. <bookmark mark='t'/> And "
            "the top three open-weights models are these: <bookmark mark='m'/> MiMo-V2.6-Pro, from Xiaomi, at 46; "
            "<bookmark mark='g'/> GLM-5.3, from Z.ai, at 45; <bookmark mark='k'/> and Kimi K3, from Moonshot AI, at 44."
        ) as vo:
            vo.wait_until("d")
            self.play(FadeIn(date), Create(c_ring), Create(c_lead), FadeIn(c_name), FadeIn(c_sub))
            vo.wait_until("t")
            self.play(FadeIn(o_sub))
            for i, m in enumerate("mgk"):
                vo.wait_until(m)
                self.play(Create(rings[i]), Create(leads[i]), FadeIn(names[i], shift=LEFT * 0.1), run_time=0.8)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cards(self):
        tot = {k: model(k)["params"]["total"] for k in KEYS}
        act = {k: model(k)["active"] for k in KEYS}
        assert [round(tot[k] / 1e9) for k in KEYS] == [1024, 753, 2780]
        assert [round(act[k] / 1e9) for k in KEYS] == [42, 41, 105]
        releases = {r["name"]: r["release"] for r in self.lb["open"]}
        rel = {"mimo": releases["MiMo-V2.6-Pro"], "glm": releases["GLM-5.3 (Max)"], "kimi": releases["Kimi K3 (Max)"]}
        side_max = 3.0
        cols = VGroup()
        xs = [-4.7, -0.3, 4.3]
        outers, inners, tl, al = VGroup(), VGroup(), VGroup(), VGroup()
        for k, x in zip(KEYS, xs):
            name = label(NAMES[k], font_size=38, color=MCOLOR[k])
            sub = label(rf"{MAKERS[k]}, released {dt.date.fromisoformat(rel[k]).strftime('%B %-d')}", font_size=24,
                        color=GREY_A)
            head = VGroup(name, sub).arrange(DOWN, buff=0.12).move_to([x, 2.85, 0])
            s_out = side_max * np.sqrt(tot[k] / tot["kimi"])
            s_in = side_max * np.sqrt(act[k] / tot["kimi"])
            outer = Square(s_out, stroke_color=MCOLOR[k], stroke_width=2, fill_color=MCOLOR[k], fill_opacity=0.15)
            outer.move_to([x, -0.35, 0], aligned_edge=DOWN).shift(DOWN * 1.2)
            inner = Square(s_in, stroke_width=0, fill_color=MCOLOR[k], fill_opacity=0.95).move_to(outer.get_corner(DL),
                                                                                                    aligned_edge=DL)
            t1 = label(rf"{tot[k] / 1e12:.2f} trillion parameters", font_size=26).next_to(outer, UP, buff=0.15)
            t2 = label(rf"{act[k] / 1e9:.0f} billion active per token", font_size=24, color=MCOLOR[k])
            t2.next_to(outer, DOWN, buff=0.15)
            cols.add(head)
            outers.add(outer)
            inners.add(inner)
            tl.add(t1)
            al.add(t2)
        area = note(r"area $\propto$ number of parameters, counted from the published weight files").to_edge(DOWN, buff=0.2)
        ctx = label(r"context window: 1 million tokens (all three)", font_size=30, color=YELLOW).to_edge(DOWN, buff=0.65)

        with self.voiceover(
            "These three are the subject of this video. <bookmark mark='s'/> They're enormous. Counting every parameter "
            "in the weight files each lab published: MiMo has about a trillion, GLM about three quarters of a trillion, "
            "and Kimi K3 2.8 trillion, by far the largest of the three. <bookmark mark='a'/> Yet each one uses only "
            "a small slice of itself for any one token: about 42 billion parameters, 41 billion, and 105 billion. "
            "<bookmark mark='c'/> And each one can read a million tokens of context at once: several thick novels, or a "
            "whole software project."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in cols], lag_ratio=0.2))
            vo.wait_until("s")
            self.play(*[DrawBorderThenFill(o) for o in outers], *[FadeIn(t) for t in tl], FadeIn(area), run_time=1.5)
            vo.wait_until("a")
            self.play(*[GrowFromPoint(i, i.get_corner(DL)) for i in inners], *[FadeIn(t) for t in al], run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(ctx, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def machines(self):
        m, g, k = model("mimo")["config"], model("glm")["config"], model("kimi")["config"]
        cell, gap, hgt = 0.115, 0.024, 0.55
        s_m = layer_strip(m["layer_types"], {"swa": C.LOCAL, "global": C.GLOBAL}, cell=cell, gap=gap, height=hgt)
        g_types = ["idx" if t == "full" else "shared" for t in g["indexer_types"]]
        s_g = layer_strip(g_types, {"idx": C.INDEXER, "shared": C.INDEXER}, cell=cell, gap=gap, height=hgt,
                          outline_types=("shared",))
        s_k = layer_strip(k["layer_types"], {"kda": C.MEMORY, "mla": C.GLOBAL}, cell=cell, gap=gap, height=hgt)
        rows = VGroup()
        descs = [
            (r"60 layers see only the last 128 tokens; 10 see everything", C.LOCAL),
            (r"every layer: compressed memory, reads only the top 2{,}048 tokens", C.INDEXER),
            (r"69 layers keep a fixed-size memory; 24 see everything", C.MEMORY),
        ]
        for key, strip, (desc, col) in zip(KEYS, (s_m, s_g, s_k), descs):
            nm = label(NAMES[key], font_size=34, color=MCOLOR[key])
            d = label(desc, font_size=28, color=col)
            hdr = VGroup(nm, label(rf"{len(strip)} layers", font_size=28, color=GREY_A)).arrange(RIGHT, buff=0.3)
            row = VGroup(hdr, strip, d).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(DOWN * 0.2)
        top = label(r"Same blueprint as GPT-2 (2019): a stack of transformer layers", font_size=32).to_edge(UP, buff=0.35)
        src = note(r"layer layouts read from each model's config.json").to_edge(DOWN, buff=0.2)

        with self.voiceover(
            "Under the hood, all three are still transformers: the same basic blueprint as GPT-2, back in 2019, a tall "
            "stack of layers. <bookmark mark='d'/> But getting to this scale forced each team to make different bets, and "
            "they ended up as three quite different machines. <bookmark mark='m'/> MiMo makes most of its layers look only "
            "at the last 128 tokens. <bookmark mark='g'/> GLM squeezes each token's memory into a compressed code, and then "
            "reads only the two thousand or so most relevant tokens. <bookmark mark='k'/> And Kimi K3 replaces three "
            "quarters of its attention layers with a memory of fixed size, which rewrites itself as it reads."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("d")
            self.play(FadeIn(src))
            for i, mk in enumerate("mgk"):
                vo.wait_until(mk)
                row = rows[i]
                self.play(FadeIn(row[0]), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in row[1]], lag_ratio=0.01),
                          run_time=1.4)
                self.play(FadeIn(row[2]), run_time=0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def roadmap(self):
        parts = VGroup(
            label(r"\textbf{1.} What they share: the mixture of experts", font_size=34),
            label(r"\textbf{2.} The million-token problem, and three different answers", font_size=34),
            label(r"\textbf{3.} Kimi K3's new ideas for depth and width", font_size=34),
            label(r"\textbf{4.} All three, side by side", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(UP * 0.4)
        promise = label(r"Every number that describes a model is read from the files its lab published.", font_size=28,
                        color=YELLOW).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "In this video we'll open up all three. <bookmark mark='a'/> First, the trick they share: the mixture of "
            "experts. <bookmark mark='b'/> Then the central problem of long context, and the three different ways they "
            "solve it. <bookmark mark='c'/> Then Kimi K3's new ideas for the depth and width of a network. "
            "<bookmark mark='d'/> And finally, all three side by side. <bookmark mark='e'/> Everything on screen that "
            "describes one of these models, from its layer layout to its parameter counts to a few of its learned weights, "
            "is read straight from the files its lab published."
        ) as vo:
            for i, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(parts[i], shift=RIGHT * 0.2), run_time=0.8)
            vo.wait_until("e")
            self.play(FadeIn(promise, shift=UP * 0.2))
        self.wait(0.4)
        self.play(FadeOut(parts), FadeOut(promise))
        card = VGroup(
            label(r"Inside the Open Frontier", font_size=72),
            label(r"the architectures of MiMo-V2.6-Pro, GLM-5.3 and Kimi K3", font_size=36, color=GREY_A),
        ).arrange(DOWN, buff=0.4)
        self.play(FadeIn(card, scale=1.05), run_time=1.2)
        self.wait(2.5)
        self.play(FadeOut(card))
