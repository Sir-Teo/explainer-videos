from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import deep as D
from videos.quant.quant17.common import BAD, GEN_COL, GOOD, NET, PART, REF, ask, house_lab, illustration, load

ORDER = ["i.i.d. normal", "i.i.d. bootstrap", "GJR-GARCH", "signature LSTM", "diffusion"]


class Generator(VoiceoverScene):
    def construct(self):
        g = load("generator")
        r = load("ddpm_reverse")
        self.card()
        self.why_generate()
        self.derive()
        self.reverse(r)
        self.contenders(g, r)
        self.lineup(g)
        self.scores(g)

    def card(self):
        c = chapter_card(16, r"Market generators", r"Can a network invent markets that look real?", lit=(2020,), part=PART)
        with self.voiceover("Chapter sixteen. Market generators."):
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

    def derive(self):
        rows = [cmath(r"x_t", r"=", r"\sqrt{\bar\alpha_t}\,x_0 + \sqrt{1 - \bar\alpha_t}\,\varepsilon,\quad "
                      r"\bar\alpha_t = \textstyle\prod_{s \le t}(1 - \beta_s)", font_size=36, colors={r"x_t": GREY_B}),
                cmath(r"\min_\theta", r"\ ", r"\mathbb{E}\,\lVert \varepsilon - \varepsilon_\theta(x_t, t)\rVert^2", font_size=38,
                      colors={r"\min_\theta": GOOD}),
                cmath(r"x_{t-1}", r"=", r"\frac{1}{\sqrt{\alpha_t}}\Big(x_t - \frac{\beta_t}{\sqrt{1 - \bar\alpha_t}}\,"
                      r"\varepsilon_\theta(x_t, t)\Big) + \sqrt{\beta_t}\,z", font_size=36, colors={r"x_{t-1}": GEN_COL["diffusion"]}),
                cmath(r"d(X, Y)", r"=", r"\big\lVert\, \mathbb{E}\,S(X) - \mathbb{E}\,S(Y) \,\big\rVert", font_size=38,
                      colors={r"d(X, Y)": NET})]
        whys = [why(r"the forward process: add a little Gaussian noise 200 times; composing Gaussian steps gives any $x_t$ "
                    r"in one draw, a blend of the real window and pure noise"),
                why(r"Ho, Jain and Abbeel (2020): train a network to recognise the noise that was added (the AI series, "
                    r"Part 21, builds it)"),
                why(r"then run backwards from pure noise, removing the predicted noise one step at a time: a new window"),
                why(r"to judge any generator: the expected signature (Part 5) of the windows, as a path of time, level and "
                    r"running variance, determines their law under a normalization (Chevyrev and Oberhauser 2022), so "
                    r"the distance between expected signatures compares two generators. The lead-lag transform's "
                    r"second level is the quadratic variation: volatility clustering shows")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.4, buff=0.62, edge=6.9)
        with self.voiceover(
            "How does a diffusion model invent a month of bitcoin? Forward: add a little Gaussian noise to a real "
            "window, two hundred times, until nothing is left; any stage is one blend of window and noise. "
            "<bookmark mark='a'/> Train a network to "
            "look at a noisy window and the stage, and recognise the noise that was added. <bookmark mark='b'/> Then "
            "run it backwards: start from pure noise and remove the predicted noise one step at a time. What remains "
            "is a window no one has seen. <bookmark mark='c'/> And to judge it, the signature from Part five. Read "
            "each window as a path of time, cumulative return and running variance; the average signature of a set "
            "of windows determines their law, so the distance between two averages compares two generators."
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

    def reverse(self, r):
        s0 = r["seeds"]["0"]
        sn = s0["snaps"]
        fw = s0["forward"]
        ts = [int(t) for t in r["ts"]]
        lim = 14.0
        gl = axes([0, 32], [-lim, lim], x_length=5.6, y_length=4.2, xlabel=r"day", ylabel=r"cumulative return (sd units)",
                  xticks=[0, 16, 32], yticks=[-10, 0, 10], font_size=13)
        gr = axes([0, 32], [-lim, lim], x_length=5.6, y_length=4.2, xlabel=r"day", ylabel="", xticks=[0, 16, 32],
                  yticks=[], font_size=13)
        VGroup(gl, gr).arrange(RIGHT, buff=0.8).shift(DOWN * 0.3)
        x = np.arange(33)

        def fan(t):
            W = np.asarray(sn[str(t)])
            return VGroup(*[curve(gl.ax, x, np.clip(np.r_[0, np.cumsum(w)], -lim, lim), GEN_COL["diffusion"],
                                  stroke_width=1.4).set_stroke(opacity=0.7) for w in W])

        def one(t):
            w = np.asarray(fw[str(t)])
            return curve(gr.ax, x, np.clip(np.r_[0, np.cumsum(w)], -lim, lim), REF, stroke_width=3)
        tl = label(r"reverse: 24 windows from noise", font_size=20, color=GEN_COL["diffusion"]).next_to(gl, UP, buff=0.15)
        tr_ = label(r"forward: one real window, drowned", font_size=20, color=REF).next_to(gr, UP, buff=0.15)
        cur, cur2 = fan(ts[0]), one(ts[-1])
        stage = label(rf"step {ts[0]}", font_size=24, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Here it is, live. On the left, twenty-four windows of pure noise, wandering like random walks with "
            "wild steps. On the right, one real window of bitcoin, held out from training. <bookmark mark='a'/> Run the "
            "two processes against each other: the real window drowns in noise as the forward process runs, while on "
            "the left the reverse process strips noise away, two hundred steps down to zero. The fans settle into "
            "paths with the scale and the jumps of real returns: invented months of bitcoin."
        ) as vo:
            self.play(FadeIn(gl), FadeIn(gr), FadeIn(tl), FadeIn(tr_), FadeIn(cur), Create(cur2), FadeIn(stage))
            vo.wait_until("a")
            per = max(vo.remaining(0.5), 6) / (len(ts) - 1)
            for i, t in enumerate(ts[1:], 1):
                st = label(rf"step {t}", font_size=24, color=GREY_A).move_to(stage)
                self.play(Transform(cur, fan(t)), Transform(cur2, one(ts[len(ts) - 1 - i])), Transform(stage, st),
                          run_time=per)
        self.wait(0.4)
        self.clear_scene()

    def contenders(self, g, r):
        cs = VGroup(
            firm_card(r"GJR-GARCH", r"the econometric baseline of Part 7: volatility that reacts to the last shock, "
                      r"more to falls than to rises", width=3.1, font_size=15),
            firm_card(r"Quant GANs", r"Wiese, Knobloch, Korn and Kretschmer (2020): temporal convolutions trained "
                      r"adversarially; volatility clustering and leverage", source=r"\textit{Quantitative Finance}",
                      width=3.1, font_size=15),
            firm_card(r"Signature generators", r"Buehler, Horvath, Lyons, Perez Arribas and Wood (2020), for small data; "
                      r"Ni, Szpruch et al.\ (2020, 2021): Sig-Wasserstein GANs; Kidger et al.\ (2021): neural SDEs as GANs",
                      width=3.1, font_size=15),
            firm_card(r"Diffusion", r"Ho, Jain and Abbeel (2020): the image generators' method, here on return windows",
                      width=3.1, font_size=15),
        ).arrange(RIGHT, buff=0.15).to_edge(UP, buff=0.35)
        for c_ in cs:
            c_[0].set_stroke(GREY_C)
        sig = np.asarray(g["curves"]["sig"])
        dd = np.array([r["seeds"][s]["curve"] for s in ("0", "1", "2")])
        g1 = axes([0, len(sig) - 1], [float(np.log10(sig.min())) - 0.1, float(np.log10(sig.max())) + 0.1], x_length=5.4,
                  y_length=2.8, xlabel=r"training step (signature network)", ylabel=r"$\log_{10}$ signature loss",
                  xticks=[0, len(sig) - 1], xfmt=lambda v: f"{10 * v:,.0f}".replace(",", "{,}"), yticks=[], font_size=12)
        g2 = axes([0, dd.shape[1] - 1], [float(dd.min()) * 0.95, float(np.percentile(dd, 99))], x_length=5.4,
                  y_length=2.8, xlabel=r"training step (diffusion)", ylabel=r"noise-prediction loss",
                  xticks=[0, dd.shape[1] - 1], xfmt=lambda v: f"{20 * v:,.0f}".replace(",", "{,}"), yticks=[], font_size=12)
        VGroup(g1, g2).arrange(RIGHT, buff=0.9).to_edge(DOWN, buff=0.45)
        l1 = curve(g1.ax, np.arange(len(sig)), np.log10(sig), GEN_COL["signature LSTM"], stroke_width=2.5)
        l2 = seed_band(g2.ax, np.arange(dd.shape[1]), np.clip(dd, None, float(np.percentile(dd, 99))), GEN_COL["diffusion"])
        ks = [r["seeds"][s]["kurtosis"] for s in ("0", "1", "2")]
        with self.voiceover(
            "Four contenders. GJR-GARCH, the econometric baseline from Part seven. Quant GANs, temporal convolution "
            "networks trained adversarially to reproduce clustering and leverage. Signature-based generators, trained "
            "by matching expected signatures, which Buehler's team built for exactly this use, with little data; and the "
            "diffusion model. <bookmark mark='a'/> Two of them trained here, replayed: the signature network's loss "
            "over its fifteen hundred steps, and the diffusion model's over four thousand, three seeds. The three "
            f"diffusion seeds produce windows with excess kurtosis between {min(ks):.1f} and {max(ks):.1f}, against "
            f"{r['real_kurtosis_train']:.1f} in the training years: the tails are the hard part."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cs], lag_ratio=0.4, run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(g1), FadeIn(g2), Create(l1), Create(l2), run_time=3)
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
                (r"dist.\ to training", "sig_train", "{:.2f}"), (r"dist.\ to held-out", "sig_dist", "{:.2f}")]
        names = ["real (train)", "real (held out)"] + ORDER
        disp = {"real (held out)": r"real, 2024--2025 (held out)", "real (train)": r"real, 2017--2023 (training)",
                "i.i.d. normal": r"independent normal draws", "i.i.d. bootstrap": r"independent resampling",
                "GJR-GARCH": r"GJR-GARCH (Part 7)", "signature LSTM": r"signature-trained network",
                "diffusion": r"diffusion model"}
        tab = VGroup(VGroup(label(r"", font_size=17), *[label(c[0], font_size=16, color=GREY_A) for c in cols]))
        for nm in names:
            s_ = sc[nm]
            tab.add(VGroup(label(disp[nm], font_size=18, color=GEN_COL.get(nm, WHITE)),
                           *[MathTex(f.format(s_[k]).replace("-0.00", "0.00").replace("+0.00", "0.00"), font_size=23,
                                     color=GEN_COL.get(nm, WHITE)) for _, k, f in cols]))
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
            "Part one's stylized facts, measured in each set of windows, with the signature distance to each real "
            "period. "
            f"<bookmark mark='a'/> First, the two real periods. The training years have excess kurtosis of "
            f"{tr['kurtosis']:.0f}; the held-out years, calmer, {te['kurtosis']:.1f}. They are far apart: the future "
            "did not look like the past. <bookmark mark='b'/> Now the generators. Independent draws have no clustering "
            f"at all, and yet, by the signature distance, the {b_tr} sit closest to the training years, a hair ahead "
            "of the signature-trained network. At this depth the distance is a weak judge, and the facts catch what it "
            "misses: only the signature-trained network has fat tails, clustering and leverage near those of the "
            f"training years. The {b_te} is closest to the held-out years for a dull reason: its tails are thin, and "
            "those years were calm. No single score is enough."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[3:]], lag_ratio=0.3, run_time=3), FadeIn(foot))
        self.wait(0.6)
        self.clear_scene()
