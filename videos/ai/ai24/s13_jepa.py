from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai24.common import (JEPA, MAE_C, PART, SIMCLR, SUP, TARGET, arrow, axes, curve, digit, load,
                                   node_box, pct, seed_curves, take_away)


class JEPAScene(VoiceoverScene):
    def construct(self):
        self.card()
        self.three()
        self.energy()
        self.ijepa()
        self.results()
        self.video()

    def card(self):
        card = chapter_card(12, r"Predict the meaning, \ not the pixels", r"JEPA: \ I-JEPA, \ V-JEPA 2", lit=(),
                            part=PART)
        with self.voiceover("Chapter twelve. Predict the meaning, not the pixels."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def three(self):
        def col(title, color, rows, x):
            t = label(title, font_size=24, color=color)
            body = VGroup(*[node_box(r_, c_, font_size=20) for r_, c_ in rows]).arrange(DOWN, buff=0.45)
            g = VGroup(t, body).arrange(DOWN, buff=0.35).move_to([x, 0.3, 0])
            ar = VGroup(*[arrow(a.get_bottom(), b.get_top(), stroke_width=2) for a, b in zip(body, body[1:])])
            return VGroup(g, ar)

        c1 = col(r"joint embedding", SIMCLR, [(r"two views $x, y$", GREY_A), (r"encode both", SIMCLR),
                                             (r"make them agree", SIMCLR)], -4.4)
        c2 = col(r"generative (masked)", MAE_C, [(r"visible part $x$", GREY_A), (r"encode, \ decode", MAE_C),
                                                (r"predict the pixels of $y$", MAE_C)], 0.0)
        c3 = col(r"joint-embedding predictive", JEPA, [(r"visible part $x$", GREY_A), (r"encode, \ predict", JEPA),
                                                      (r"predict the encoding of $y$", JEPA)], 4.4)
        notes = VGroup(label(r"needs views, \ and a guard \\ against collapse", font_size=19, color=GREY_B),
                       label(r"must model every detail", font_size=19, color=GREY_B),
                       label(r"may ignore what \\ cannot be predicted", font_size=19, color=GREY_B))
        for n_, c_ in zip(notes, (c1, c2, c3)):
            n_.next_to(c_, DOWN, buff=0.3)
        src = cite(r"LeCun (2022): \ ``A path towards autonomous machine intelligence''")
        with self.voiceover(
            "In 2022 Yann LeCun laid out the third way, in a long essay on how machines might learn models of the "
            "world. <bookmark mark='a'/> Joint-embedding methods, like everything since chapter four, make two "
            "views agree; they need hand-made views, and a guard against collapse. <bookmark mark='b'/> Generative "
            "methods, like MAE, predict the hidden part's pixels, every detail, the predictable and the "
            "unpredictable alike. <bookmark mark='c'/> A joint-embedding predictive architecture, a JEPA, predicts "
            "the hidden part's encoding instead: the network decides what about the hidden part is worth "
            "predicting, and can drop the rest."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(c1), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(c2), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(c3), FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def energy(self):
        ys = np.linspace(-3, 3, 200)

        def panel(f, center, title, col):
            ax = axes([-3, 3], [0, 2.2], x_length=4.0, y_length=2.4, xlabel=r"candidate $y$", ylabel=r"energy",
                      center=center)
            c = curve(ax.ax, ys, [f(y) for y in ys], col, 3)
            t = label(title, font_size=22, color=col).next_to(ax, UP, buff=0.15)
            return VGroup(ax, c, t), ax

        flat, ax1 = panel(lambda y: 0.15, [-4.6, 0.2, 0], r"collapsed: \ low everywhere", "#FF5C5C")
        shaped, ax2 = panel(lambda y: 1.9 - 1.7 * np.exp(-2 * (y - 0.6) ** 2), [0.0, 0.2, 0],
                            r"contrastive: \ push up the others", SIMCLR)
        reg, ax3 = panel(lambda y: 1.9 - 1.7 * np.exp(-2 * (y - 0.6) ** 2), [4.6, 0.2, 0],
                         r"regularized: \ ration the low energy", JEPA)
        pos = Dot(ax2.ax.c2p(0.6, 0.2), radius=0.08, color=C.INTERVAL)
        down = Arrow(ax2.ax.c2p(0.6, 1.2), ax2.ax.c2p(0.6, 0.35), buff=0, color=C.INTERVAL, stroke_width=3)
        ups = VGroup(*[Arrow(ax2.ax.c2p(x, 1.0), ax2.ax.c2p(x, 1.8), buff=0, color="#EF6A5B", stroke_width=3)
                       for x in (-2.0, -0.9, 2.2)])
        band = Rectangle(width=ax3.ax.c2p(1.4, 0)[0] - ax3.ax.c2p(-0.2, 0)[0], height=0.25, stroke_width=0,
                         fill_color=JEPA, fill_opacity=0.25).move_to(ax3.ax.c2p(0.6, 0.35))
        e = MathTex(r"E(x, y)", r"=", r"\big\| \mathrm{pred}(s_x) - s_y \big\|^2", font_size=36).to_edge(UP, buff=0.5)
        e[2].set_color(JEPA)
        fams = VGroup(label(r"negatives: \ word2vec, \ SimCLR, \ MoCo", font_size=20, color=SIMCLR).next_to(shaped, DOWN,
                                                                                                         buff=0.6),
                      label(r"variance, \ decorrelation, \ predictors: \\ Barlow, \ VICReg, \ BYOL, \ DINO, \ JEPA",
                            font_size=20, color=JEPA).next_to(reg, DOWN, buff=0.45))
        src = cite(r"LeCun, Chopra, Hadsell, Ranzato \& Huang (2006); \ LeCun (2022); \ energies: \ Part 20")
        with self.voiceover(
            "LeCun frames all of this with energies, the language of Part 20. A JEPA's energy is its prediction "
            "error: low when y fits x, high when it does not. <bookmark mark='a'/> Collapse is an energy that is low "
            "everywhere: every y fits every x. <bookmark mark='b'/> There are two ways to give it shape. "
            "Contrastive methods push the energy down on real pairs and up on chosen negatives, as word2vec and "
            "SimCLR do. <bookmark mark='c'/> Regularized methods instead limit how much of the space can have low "
            "energy at all: VICReg's variance floor, Barlow's decorrelation, the predictors and moving averages of "
            "BYOL, DINO and JEPA. LeCun argues the second kind scales better, because in high dimensions there are "
            "too many places to push."
        ) as vo:
            self.play(Write(e), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(flat))
            vo.wait_until("b")
            self.play(FadeIn(shaped), FadeIn(pos), GrowArrow(down), *[GrowArrow(u) for u in ups], FadeIn(fams[0]))
            vo.wait_until("c")
            self.play(FadeIn(reg), FadeIn(band), FadeIn(fams[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ijepa(self):
        j = load("jepa")
        v = load("views")
        T = np.asarray(j["ex_targets"]).astype(bool)
        G = int(j["grid"])
        img = np.asarray(v["orig"])[4].astype(float) / 255.0
        S = 2.8

        def board(mask, center):
            d = digit(img, S, frame=True).move_to(center)
            cells = VGroup()
            s = S / G
            for r in range(G):
                for c in range(G):
                    sq = Square(s, stroke_color=GREY_D, stroke_width=1)
                    sq.move_to(d.get_corner(UL) + np.array([s * (c + 0.5), -s * (r + 0.5), 0]))
                    if mask[r, c]:
                        sq.set_fill(JEPA, opacity=0.55).set_stroke(JEPA, 2)
                    cells.add(sq)
            return Group(d, cells)

        b1 = board(T[0], [-4.6, 0.6, 0])
        ctx = node_box(r"context encoder \\ (sees the rest)", JEPA, font_size=20, height=1.1).move_to([-1.2, 1.4, 0])
        tgt = node_box(r"target encoder \\ (sees everything; \\ moving average)", TARGET, font_size=20,
                       height=1.3).move_to([-1.2, -0.6, 0])
        pr = node_box(r"predictor", JEPA, font_size=22).move_to([1.6, 1.4, 0])
        ls = node_box(r"$\| \hat s_y - s_y \|^2$ \\ on the hidden blocks", C.LOSS, font_size=20, height=1.1).move_to(
            [4.6, 0.4, 0])
        arrs = VGroup(arrow(b1.get_right() + UP * 0.6, ctx.get_left()), arrow(b1.get_right() + DOWN * 0.6,
                                                                             tgt.get_left(), color=TARGET),
                      arrow(ctx.get_right(), pr.get_left()), arrow(pr.get_right(), ls.get_left() + UP * 0.2),
                      arrow(tgt.get_right(), ls.get_left() + DOWN * 0.2, color=TARGET))
        facts = label(r"I-JEPA: \ one context block, \ four target blocks of $15$--$20\%$; \ ViT-Huge/14 \\ trained "
                      r"on ImageNet in under $72$ hours on $16$ A100 GPUs", font_size=21, color=GREY_A).to_edge(DOWN,
                                                                                                          buff=0.5)
        ours = label(r"ours: \ the same network; \ its final $4 \times 4$ map; \ two hidden blocks of $2 \times 2$ cells",
                     font_size=21, color=JEPA).next_to(facts, UP, buff=0.25)
        src = cite(r"Assran et al.\ (2023): \ I-JEPA", corner=UR)
        with self.voiceover(
            "I-JEPA, from Mahmoud Assran and colleagues in 2023, is the image version. Hide some blocks of the "
            "image. <bookmark mark='a'/> A context encoder sees the rest. <bookmark mark='b'/> A target encoder, a "
            "slowly moving average of the context encoder as in BYOL, sees the whole image, and its output at the "
            "hidden blocks is the target. <bookmark mark='c'/> A predictor, told where the hidden blocks are, must "
            "produce that target from the context. No pixels are predicted, and no views are needed beyond a crop. "
            "<bookmark mark='d'/> Ours runs on the same network as everything else: the targets are cells of its "
            "final four-by-four map, two blocks of two by two."
        ) as vo:
            self.play(FadeIn(b1), FadeIn(src))
            vo.wait_until("a")
            self.play(GrowArrow(arrs[0]), FadeIn(ctx))
            vo.wait_until("b")
            self.play(GrowArrow(arrs[1]), FadeIn(tgt))
            vo.wait_until("c")
            self.play(GrowArrow(arrs[2]), FadeIn(pr), GrowArrow(arrs[3]), GrowArrow(arrs[4]), FadeIn(ls))
            self.play(FadeIn(facts))
            vo.wait_until("d")
            self.play(FadeIn(ours))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        j = load("jepa")
        m = load("mae")
        s = load("simclr")
        b = load("baselines")
        runs_j, kj = j["runs"], j["keys"]["ijepa"]
        runs_m, km = m["runs"], m["keys"]["0.75"]
        runs_s, ks = s["runs"], s["keys"]["0.2"]
        S_ = runs_j[kj[0]]["steps"][-1]
        lo = min(min(runs_j[k]["knn"]) for k in kj)
        lo = min(lo, min(min(runs_m[k]["knn"]) for k in km))
        lo = float(np.floor(lo * 10) / 10)
        ax = axes([0, S_], [lo, 1.0], x_length=5.4, y_length=3.6, xlabel=r"training step",
                  ylabel=r"$k$-NN accuracy (quick test)", xticks=[0, S_], yticks=[lo, 1.0], center=[-2.6, -0.3, 0])
        cj = seed_curves(ax.ax, runs_j, kj, "knn", JEPA)
        cm = seed_curves(ax.ax, runs_m, km, "knn", MAE_C)
        cs = seed_curves(ax.ax, runs_s, ks, "knn", SIMCLR)
        leg = VGroup(label(r"I-JEPA", font_size=20, color=JEPA), label(r"MAE", font_size=20, color=MAE_C),
                     label(r"SimCLR", font_size=20, color=SIMCLR)).arrange(RIGHT, buff=0.5).next_to(ax, UP, buff=0.2)
        J, M_, Sm = j["summary"]["ijepa"], m["summary"]["0.75"], s["summary"]["0.2"]
        un = float(np.mean([r["linear"] for r in b["random_cnn"]]))
        tab = VGroup()
        for n_, c_, sm in ((r"I-JEPA", JEPA, J), (r"MAE", MAE_C, M_), (r"SimCLR", SIMCLR, Sm)):
            tab.add(VGroup(label(n_, font_size=24, color=c_), MathTex(pct(sm["linear"][0]) + r"\%", font_size=28),
                           MathTex(pct(sm["few"][0]) + r"\%", font_size=28)).arrange(RIGHT, buff=0.4))
        hdr = label(r"linear \quad 10 labels", font_size=20, color=GREY_A)
        tab.arrange(DOWN, aligned_edge=RIGHT, buff=0.3)
        hdr.next_to(tab, UP, buff=0.25).align_to(tab, RIGHT)
        VGroup(hdr, tab).move_to([4.2, -0.2, 0])
        jl, ml = J["linear"][0], M_["linear"][0]
        if jl > ml + 0.003:
            v = (f"Predicting the meaning beats predicting the pixels: I-JEPA's linear probe reaches {pct(jl)} percent, "
                 f"MAE's {pct(ml)}" + (f", and it comes within {pct(Sm['linear'][0] - jl)} points of SimCLR, with "
                                       "no hand-made views." if jl < Sm["linear"][0] else ", ahead even of SimCLR."))
        elif jl < ml - 0.003:
            v = (f"On our digits, predicting the encoding does not beat predicting the pixels: I-JEPA reaches "
                 f"{pct(jl)} percent on the linear probe, MAE {pct(ml)}. A four-by-four map is a coarse target, and "
                 "our budget is short.")
        else:
            v = f"On our digits the two are level: I-JEPA {pct(jl)} percent, MAE {pct(ml)}."
        tg = tag(r"computed: \ three seeds each, \ the same network and budget")
        lit = cite(r"Assran et al.\ (2023), \ ViT-H/14: \ I-JEPA $79.3\%$, \ MAE $77.2\%$", corner=DL)
        with self.voiceover(
            "We trained I-JEPA, MAE and SimCLR on the same network, for the same number of steps. <bookmark "
            f"mark='a'/> {v} <bookmark mark='b'/> In the paper, with the largest vision transformers, I-JEPA's "
            "linear probe beat MAE's, 79.3 percent to 77.2, using more than ten times less computation."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(leg), FadeIn(tg))
            self.play(Create(cs), Create(cm), Create(cj), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(hdr), LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(Indicate(tab[0], color=JEPA, scale_factor=1.05), FadeIn(lit))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def video(self):
        events = VGroup(
            history_card(2024, r"V-JEPA", r"the same idea on video: \ predict hidden space--time blocks", color=JEPA,
                         width=4.3, font_size=19),
            history_card(2025, r"V-JEPA 2", r"over a million hours of video; \ Something-Something v2 $77.3\%$; \ then "
                         r"$62$ hours of robot video teach it actions (V-JEPA 2-AC): \ zero-shot pick-and-place by "
                         r"planning toward an image of the goal", color=JEPA, width=4.3, font_size=19),
            history_card(2026, r"V-JEPA 2.1", r"dense features for images and video; \ $+20$ points of grasping "
                         r"success over V-JEPA 2-AC", color=JEPA, width=4.3, font_size=19),
        ).arrange(RIGHT, buff=0.25, aligned_edge=UP).move_to(UP * 0.7)
        le = label(r"LeJEPA (Balestriero \& LeCun, 2025): \ a JEPA with no stop-gradient and no teacher, \\ its "
                   r"collapse prevented by pushing the vectors toward an isotropic Gaussian", font_size=21,
                   color=GREY_A).next_to(events, DOWN, buff=0.5)
        src = cite(r"Bardes et al.\ (2024); \ Assran et al.\ (2025); \ Mur-Labadia et al.\ (2026)")
        tk = take_away(r"predict in representation space: \ the network chooses what is worth predicting \ "
                       r"(world models: Part 29)")
        with self.voiceover(
            "On video, the idea becomes a model of the world. V-JEPA predicts hidden blocks of space and time. "
            "<bookmark mark='a'/> V-JEPA 2, in June 2025, was trained on over a million hours of video. Then, with "
            "less than sixty-two hours of unlabelled robot video, it learned how a robot arm's actions change what "
            "it sees, and it could pick and place objects in labs it had never seen, by searching for actions whose "
            "predicted outcome looks like a picture of the goal. <bookmark mark='b'/> Its 2026 successor learns "
            "detailed features for every patch, and grasps more reliably. <bookmark mark='c'/> And LeJEPA dropped "
            "the stop-gradient and the teacher altogether. World models return in Part 29."
        ) as vo:
            self.play(FadeIn(events[0], shift=UP * 0.15), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(events[1], shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(events[2], shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(le))
            self.play(FadeIn(tk, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
