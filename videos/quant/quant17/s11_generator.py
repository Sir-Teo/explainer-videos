from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import BAD, GEN_COL, GOOD, NET, PART, REF, illustration, load

ORDER = ["i.i.d. normal", "i.i.d. bootstrap", "GJR-GARCH", "signature LSTM", "diffusion"]


class Generator(VoiceoverScene):
    def construct(self):
        g = load("generator")
        self.card()
        self.why_generate()
        self.lineup(g)
        self.scores(g)

    def card(self):
        c = chapter_card(10, r"Market generators", r"Can a network invent markets that look real?", part=PART)
        with self.voiceover("Chapter ten. Market generators."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def why_generate(self):
        rows = [cmath(r"z", r"\ \mapsto\ ", r"(r_1, \dots, r_{32})", font_size=40, colors={r"(r_1, \dots, r_{32})": NET}),
                cmath(r"\mathbb{E}\big[S(\text{real})\big]", r"\approx", r"\mathbb{E}\big[S(\text{generated})\big]",
                      font_size=36, colors={r"\mathbb{E}\big[S(\text{generated})\big]": NET})]
        whys = [why(r"the deep hedger is only as good as the paths it trains on, and history is one path. A generator turns "
                    r"noise into new 32-day windows of returns; Buehler, Horvath, Lyons, Perez Arribas and Wood (2020) built "
                    r"one for exactly this; J.P. Morgan's team, Risk.net reported, trained its hedgers on such simulated data"),
                why(r"how to compare a set of paths with another? The expected signature (Part 5) of a path's time, level "
                    r"and running variance characterizes its law; matching it trains the generator (Ni et al.\ 2021). A "
                    r"diffusion model, the method behind image generators (AI series, Part 21), is the other contender")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.6, buff=1.0, edge=6.9)
        with self.voiceover(
            "The deep hedger learned from simulated paths. Where do the paths come from? History gives us one path, "
            "and a hedger trained on a model learns the model's mistakes. So the same team built market generators: "
            "networks that turn noise into new stretches of market history, and, as Risk.net reported, trained "
            "hedgers on their output. "
            "<bookmark mark='a'/> Judging a generator means comparing two clouds of paths. One way uses the path "
            "signature from Part five: its average over a set of paths pins down their law, and matching averages "
            "trains a generator. The other contender is a diffusion model, the method behind image generators, from "
            "the AI series."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def lineup(self, g):
        L = g["lineup"]
        panels = [("real", np.asarray(w)) for w in L["real"]] + [("diffusion", np.asarray(w)) for w in L["diffusion"]]
        order = np.random.default_rng(3).permutation(len(panels))
        cells = VGroup()
        for k in order:
            kind, w = panels[k]
            x = np.r_[0, np.cumsum(w)]
            lim = max(0.35, float(np.abs(x).max()) * 1.15)
            ax = Axes(x_range=[0, 32, 8], y_range=[-lim, lim, lim], x_length=2.9, y_length=1.9, tips=False,
                      axis_config={"stroke_color": GREY_D, "stroke_width": 1, "include_ticks": False})
            line = ax.plot_line_graph(np.arange(33), x, add_vertex_dots=False, line_color=GREY_A, stroke_width=2)
            box = SurroundingRectangle(ax, buff=0.08, stroke_color=GREY_D, stroke_width=1)
            cells.add(VGroup(ax, line, box))
            cells[-1].kind = kind
        cells.arrange_in_grid(rows=2, cols=4, buff=(0.35, 0.45)).move_to(UP * 0.1)
        head = label(r"Eight 32-day stretches of bitcoin: four real, four invented", font_size=28).to_edge(UP, buff=0.5)
        tags = VGroup(*[label(r"real" if c.kind == "real" else r"diffusion model", font_size=18,
                              color=REF if c.kind == "real" else GEN_COL["diffusion"]).next_to(c, DOWN, buff=0.08)
                        for c in cells])
        src = illustration(r"real windows from the held-out last 20\% of 2017--2025; cumulative log return")
        with self.voiceover(
            "A lineup. Eight stretches of thirty-two days of bitcoin, as cumulative returns. Four are real, taken from "
            "the last fifth of the data, which no generator saw. Four were invented by a small diffusion model trained "
            "on the earlier years. Which are which? <bookmark mark='a'/> Here is the answer. By eye, they are hard to "
            "tell apart. The eye is a weak test, so the next step is to measure."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.15, run_time=3))
            vo.wait_until("a")
            for c, t in zip(cells, tags):
                c[1].set_color(REF if c.kind == "real" else GEN_COL["diffusion"])
            self.play(FadeIn(tags), *[c[1].animate.set_color(REF if c.kind == "real" else GEN_COL["diffusion"])
                                      for c in cells])
        self.wait(0.6)
        self.clear_scene()

    def scores(self, g):
        sc = g["scores"]
        cols = [(r"excess kurtosis", "kurtosis", "{:.1f}"), (r"vol clustering", "acf_abs_mean", "{:.2f}"),
                (r"leverage", "leverage", "{:+.2f}"), (r"lag-1 autocorr.", "acf1", "{:+.2f}"),
                (r"distance: training years", "sig_train", "{:.2f}"), (r"distance: held-out years", "sig_dist", "{:.2f}")]
        names = ["real (train)", "real (held out)"] + ORDER
        disp = {"real (held out)": r"real, 2024--2025 (held out)", "real (train)": r"real, 2017--2023 (training)",
                "i.i.d. normal": r"independent normal draws", "i.i.d. bootstrap": r"independent resampling",
                "GJR-GARCH": r"GJR-GARCH (Part 7)", "signature LSTM": r"signature-trained network",
                "diffusion": r"diffusion model"}
        tab = VGroup(VGroup(label(r"", font_size=17), *[label(c[0], font_size=16, color=GREY_A) for c in cols]))
        for nm in names:
            s_ = sc[nm]
            tab.add(VGroup(label(disp[nm], font_size=18, color=GEN_COL.get(nm, WHITE)),
                           *[MathTex(f.format(s_[k]), font_size=23, color=GEN_COL.get(nm, WHITE)) for _, k, f in cols]))
        xs = [-4.7, -1.75, -0.15, 1.35, 2.85, 4.45, 6.1]
        for i, row in enumerate(tab):
            for j, cell in enumerate(row):
                cell.move_to([xs[j], 2.5 - 0.55 * i, 0])
        tr, te = sc["real (train)"], sc["real (held out)"]
        best_tr = min(ORDER, key=lambda k: sc[k]["sig_train"])
        best_te = min(ORDER, key=lambda k: sc[k]["sig_dist"])
        spoken = {"i.i.d. normal": "independent normal draws", "i.i.d. bootstrap": "independent resampling",
                  "GJR-GARCH": "GJR-GARCH model of Part seven", "signature LSTM": "signature-trained network",
                  "diffusion": "diffusion model"}
        b_tr, b_te = spoken[best_tr], spoken[best_te]
        sl = sc["signature LSTM"]
        foot = wrapped_label(rf"measured inside 32-day windows (so clustering reads lower than on a long series); distances "
                             r"are signature distances (depth 4), every set clipped at the training data's 0.1\% and 99.9\% "
                             rf"quantiles. By distance alone, {disp[best_tr]} sit closest to the training years, with no "
                             rf"clustering at all; only the signature-trained network gets tails ({sl['kurtosis']:.0f}), "
                             rf"clustering ({sl['acf_abs_mean']:.2f}) and leverage right. No single score is enough",
                             12.6, 18, GREY_A).to_edge(DOWN, buff=0.3)
        src = illustration(r"4{,}000 generated windows each; daily log returns, standardized", corner=UR)
        with self.voiceover(
            "Here are Part one's stylized facts, measured in each set of windows: fat tails, volatility clustering, "
            "the leverage effect, and the absence of autocorrelation, with the signature distance to each real period. "
            f"<bookmark mark='a'/> First, the two real periods. The training years have excess kurtosis of "
            f"{tr['kurtosis']:.0f}; the held-out years, calmer, {te['kurtosis']:.1f}. They are far apart: the future "
            "did not look like the past. <bookmark mark='b'/> Now the generators. Independent draws have no clustering "
            f"at all, and yet, by the signature distance, the {b_tr} sit closest to the training years, a hair ahead "
            "of the signature-trained network. At this depth the distance is a weak judge, and the facts catch what it "
            "misses: only the signature-trained network has fat tails, clustering and leverage near those of the "
            f"training years. The {b_te} is closest to the held-out years for a dull reason: its tails are thin, and "
            "those years were calm. No single score is enough. A desk checks the facts one by one, keeps several "
            "generators, and stresses its hedger on all of them."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[3:]], lag_ratio=0.3, run_time=3), FadeIn(foot))
        self.wait(0.6)
        self.clear_scene()
