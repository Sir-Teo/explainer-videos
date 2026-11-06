from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import ALT, BAD, FC, GOOD, PART, RET, VOL, load, real_data, predict


def _pad(curves):
    n = max(len(c) for c in curves)
    return np.array([list(c) + [c[-1]] * (n - len(c)) for c in curves], float)


class Training(VoiceoverScene):
    def construct(self):
        t = load("training")
        self.card()
        self.archs(t)
        self.replay(t, "LSTM", ALT)
        self.overfit(t)
        self.seeds(t)
        self.harnet(t)

    def card(self):
        c = chapter_card(13, r"Training the networks", r"What can a network learn from 675 days?", lit=(2019,), part=PART)
        with self.voiceover("Chapter thirteen. Training the networks."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def archs(self, t):
        rows = [
            cmath(r"c_t", r"=", r"f_t\odot c_{t-1} + i_t\odot\tilde c_t,\quad h_t = o_t\odot\tanh c_t", font_size=34),
            cmath(r"\operatorname{Attn}(Q,K,V)", r"=", r"\operatorname{softmax}\big(QK^\top/\sqrt{d}\big)V", font_size=34),
            cmath(r"\ln RV \sim N(m, s^2)", r"\Rightarrow", r"\mathbb{E}[RV] = e^{m + s^2/2}", font_size=34),
            cmath(r"\text{HARNet at } \theta_0", r"=", r"\text{log-HAR}: \text{filters } 1,\ \tfrac15\mathbf{1}_5,\ \tfrac1{22}\mathbf{1}_{22}",
                  font_size=34),
        ]
        whys = [why(r"an LSTM's memory cell: a learned, data-dependent exponential average (compare GARCH, unrolled)"),
                why(r"a transformer reads all 22 days at once, weighting them by learned attention: a learned HAR"),
                why(r"the networks forecast log RV; mapping back needs the log-normal correction, or forecasts are too low"),
                why(r"Reisenhofer, Bayer and Hautsch (2022): start the network exactly at HAR, then let it learn")]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-1.8, buff=0.45, edge=6.9)
        par = MathTex(rf"\text{{parameters: LSTM }} {t['LSTM']['n_params']:,},\ \text{{transformer }} {t['Transformer']['n_params']:,},"
                      rf"\ \text{{HARNet }} {t['HARNet']['n_params']}".replace(",", "{,}"), font_size=28, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Three networks, each reading the last twenty-two days of log realized variance. An LSTM's gated memory cell is a learned, data-dependent exponential average, like GARCH unrolled. "
            "<bookmark mark='a'/> A small transformer looks at all twenty-two days at once and weights them by "
            "attention: a learned version of HAR's averages. <bookmark mark='b'/> All three forecast the logarithm, "
            "so we use a working lognormal back-transform calibrated from validation residuals, not an exact conditional mean without distributional assumptions. <bookmark mark='c'/> And the third, after "
            "Rafael Reisenhofer, Xandro Bayer and Nikolaus Hautsch, is HARNet: its filters and weights start at the training-window log-HAR fit, which differs from the race baseline fitted through December, and optimization then adjusts it using the training loss. <bookmark mark='d'/> "
            "Same data, same early stopping, five seeds each."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeIn(par))
        self.wait(0.3)
        self.clear_scene()

    def _frame_fn(self, t, name, col, keys):
        vt = np.asarray(t["val_t"])
        y = np.asarray(t["val_lrv"])
        all_values = np.concatenate([y] + [np.asarray(v) for v in t[name]["snaps"].values()])
        lo, hi = float(all_values.min()) - 0.3, float(all_values.max()) + 0.3

        def frame(i):
            k = keys[min(i, len(keys) - 1)]
            g = axes([vt[0], vt[-1]], [lo, hi], x_length=5.0, y_length=3.2, xticks=[], yticks=[], font_size=14,
                     ylabel=rf"validation, H2 2019: log RV (dots), {name} (line), epoch {k}")
            p = np.asarray(t[name]["snaps"][k])
            dots = VGroup(*[Dot(g.ax.c2p(a, b), radius=0.025, color=RET) for a, b in zip(vt, y)])
            return VGroup(g, dots, curve(g.ax, vt, p, col, stroke_width=3))
        return frame

    def replay(self, t, name, col):
        V = _pad(t[name]["val"])
        steps = np.arange(V.shape[1])
        keys = ["0", "5", "10", "20", "40", "best"]
        be = t[name]["best_epoch"][0]
        ck = sorted(set([0, 5, 10, 20, min(40, V.shape[1] - 1), V.shape[1] - 1]))
        keys = keys[:len(ck) - 1] + ["best"]
        rp = TrainingReplay(steps, V, self._frame_fn(t, name, col, keys), checkpoints=ck, ylabel=r"validation loss (5 seeds)",
                            xlabel=r"epoch", color=col)
        rp.to_edge(UP, buff=0.6)
        marks = VGroup(*[Dot(rp.ax.c2p(e, float(V[s, min(e, V.shape[1] - 1)])), radius=0.06, color=YELLOW)
                         for s, e in enumerate(t[name]["best_epoch"])])
        cap = label("yellow: each seed's best epoch; stopping after about 30 non-improving epochs", font_size=18, color=GREY_B)
        cap.next_to(rp, DOWN, buff=0.3)
        with self.voiceover(
            f"Watch the {name} learn. On the right, the validation loss for each of the five seeds, the spread as a band. "
            "On the left, the network's forecasts for the second half of 2019 at each checkpoint, against what "
            "happened. <bookmark mark='a'/> At epoch zero this randomly initialized forecast is nearly flat. "
            "Within five epochs it has found the level, within twenty the slow swings. Then validation stops "
            f"improving, and each seed stops on its own schedule: the first seed's best epoch is {be}. This small-data experiment mostly learns level and persistence; it does not bound what larger datasets or models can learn."
        ) as vo:
            self.play(FadeIn(rp))
            vo.wait_until("a")
            rp.play(self, run_time=6)
            self.play(LaggedStart(*[GrowFromCenter(m) for m in marks], lag_ratio=0.2), FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    def seeds(self, t):
        names = [("LSTM", ALT), ("Transformer", BAD), ("HARNet", GOOD)]
        g = axes([0.34, 0.44], [0, 3], x_length=7.0, y_length=3.0, xticks=[0.34, 0.36, 0.38, 0.40, 0.42, 0.44], yticks=[],
                 xfmt=lambda v: f"{v:.2f}", xlabel=r"QLIKE in 2020, each seed scored alone (lower is better)",
                 font_size=16).move_to(DOWN * 0.2 + RIGHT * 1.0)
        ax = g.ax
        rows = VGroup()
        for i, (n_, c_) in enumerate(names):
            y = 2.5 - i
            q = np.asarray(t[n_]["seed_qlike"])
            dots = VGroup(*[Dot(ax.c2p(v, y), radius=0.09, color=c_) for v in q])
            rng_ = Line(ax.c2p(q.min(), y), ax.c2p(q.max(), y), color=c_, stroke_width=3)
            rows.add(VGroup(label(n_, font_size=22, color=c_).next_to(ax.c2p(0.34, y), LEFT, buff=0.3), rng_, dots))
        pc = predict(r"Five seeds, same data, same architecture. Will they agree on 2020?", width=6.4, font_size=22)
        pc.to_edge(UP, buff=0.5)
        sp = {n_: (min(t[n_]["seed_qlike"]), max(t[n_]["seed_qlike"])) for n_, _ in names}
        wide = (sp["Transformer"][1] - sp["Transformer"][0]) / (sp["LSTM"][1] - sp["LSTM"][0])
        with self.voiceover(
            f"""Pause and predict: five seeds, the same data and architecture. Will their 2020 scores agree? <bookmark mark='a'/> The LSTM ranges from {sp['LSTM'][0]:.3f} to {sp['LSTM'][1]:.3f}; the transformer's spread is {wide:.1f} times as wide. Picking a winning seed would add selection freedom. This registered protocol fixes five seeds and averages them, rather than counting a selected seed as a new discovery. <bookmark mark='b'/> HARNet's seeds are much closer, starting from the log-HAR structure."""
        ) as vo:
            self.play(FadeIn(pc))
            vo.wait_until("a")
            self.play(FadeIn(g), LaggedStart(*[FadeIn(r) for r in rows[:2]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.wait(0.3)
        self.clear_scene()

    def harnet(self, t):
        V = _pad(t["HARNet"]["val"])
        steps = np.arange(V.shape[1])
        ck = [0, 5, 10, 20, V.shape[1] - 1]
        rp = TrainingReplay(steps, V, self._frame_fn(t, "HARNet", GOOD, ["0", "5", "10", "20", "best"]), checkpoints=ck,
                            ylabel=r"validation loss (5 seeds)", xlabel=r"epoch", color=GOOD)
        rp.to_edge(UP, buff=0.6)
        f = np.asarray(t["HARNet"]["filters"])
        hd = np.asarray(t["HARNet"]["head"])
        side = VGroup(
            label(r"after training (seed 0): the day filter's weight on yesterday", font_size=19, color=GREY_A),
            MathTex(rf"{f[0, -1]:.2f}\ \ (\text{{started at }} 1)", font_size=28, color=GOOD),
            label(r"head weights on the day, week and month features", font_size=19, color=GREY_A),
            MathTex(rf"{hd[0]:.2f},\ {hd[1]:.2f},\ {hd[2]:.2f}", font_size=28, color=GOOD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.4)
        v0, vb = float(V[0, 0]), float(V[0].min())
        with self.voiceover(
            "HARNet's replay looks different. Its first frame is already log-HAR's forecast, and its validation loss "
            f"starts at {v0:.3f}, where the others needed twenty epochs to arrive. <bookmark mark='a'/> Training "
            f"lowers it only to {vb:.3f}, with its best epoch early; training then continues until the patience rule stops it. The final left panel shows retained best weights, while the right curve shows the full stopping path. The learned filters stay close to "
            "where they started: yesterday still dominates, as Reisenhofer and his coauthors found on stock indices. "
            "The network is a microscope on HAR: it confirms the structure rather than replacing it."
        ) as vo:
            self.play(FadeIn(rp))
            rp.play(self, run_time=4)
            vo.wait_until("a")
            self.play(FadeIn(side))
        self.wait(0.3)
        self.clear_scene()

    def overfit(self, t):
        tr, va = np.asarray(t["LSTM"]["train"][2], float), np.asarray(t["LSTM"]["val"][2], float)
        be = int(t["LSTM"]["best_epoch"][2])
        ep = np.arange(len(tr))
        hi = float(max(tr.max(), va.max())) * 1.05
        g = axes([0, len(tr)], [0, hi], x_length=8.0, y_length=4.0, xticks=[0, be, len(tr) - 1], yticks=[0, round(hi / 2, 2)],
                 xlabel=r"epoch", ylabel=r"LSTM, seed 2: mean squared error on standardized log RV", font_size=16)
        g.move_to(DOWN * 0.3)
        lt = curve(g.ax, ep, tr, GREY_B, stroke_width=3)
        lv = curve(g.ax, ep, va, ALT, stroke_width=3)
        stop = DashedLine(g.ax.c2p(be, 0), g.ax.c2p(be, hi), color=YELLOW, stroke_width=3)
        leg = legend([(GREY_B, r"training loss"), (ALT, r"validation loss (H2 2019)"), (YELLOW, r"best epoch, kept")],
                     font_size=19).to_corner(UR, buff=0.5)
        gap = float(va[-1] - va[be])
        with self.voiceover(
            f"""Why stop early? Training loss keeps falling, which can eventually overfit. <bookmark mark='a'/> This seed's validation loss bottoms at epoch {be}, then rises by {gap:.3f}; that is evidence for stopping here, not proof of memorizing particular noise. <bookmark mark='b'/> Keep the best validation weights and stop after about thirty non-improving epochs. Networks train through June 2019 and validate on the second half. Classical baselines fit through December. 2020 is excluded from gradients and early stopping, but later reused for comparisons and added models. The separate 2021-onward envelope remains sealed."""
        ) as vo:
            self.play(FadeIn(g), Create(lt), FadeIn(leg[0]), run_time=2)
            vo.wait_until("a")
            self.play(Create(lv), FadeIn(leg[1]), run_time=2)
            vo.wait_until("b")
            self.play(Create(stop), FadeIn(leg[2]))
        self.wait(0.3)
        self.clear_scene()
