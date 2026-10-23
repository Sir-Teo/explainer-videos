from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai18.common import (EDU, F, GROUP_C, KEPT, PART, REMOVED, hbars, load, spoken_int, stage_row, take_away)

GROUP_TEX = [r"American", r"English society", r"Adventure and mystery", r"Translations and \textit{Ulysses}"]


class Mixture(VoiceoverScene):
    def construct(self):
        self.card()
        self.why_mix()
        self.regmix()
        self.tested()
        self.synthetic()
        self.collapse()

    def card(self):
        card = chapter_card(5, r"Mixtures, \ synthetic data \ and collapse", r"How much of each kind of text? \ "
                            r"And can a model make its own?", part=PART)
        with self.voiceover("Chapter five. Mixtures, synthetic data and collapse."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def why_mix(self):
        D, R = F.DOREMI, F.REGMIX
        pile = VGroup(*[VGroup(Rectangle(width=w, height=0.5, stroke_width=1, stroke_color=BLACK, fill_color=c,
                                         fill_opacity=0.85), label(t, font_size=18, color=BLACK))
                        for w, c, t in ((2.4, "#6EA8FE", r"web $24\%$"), (0.9, "#5CD0B3", r"Wiki $9\%$"),
                                        (0.6, "#FFB86B", r"code"), (6.1, GREY_C, r"the other $19$ sources"))])
        for r_ in pile:
            r_[1].move_to(r_[0])
        pile.arrange(RIGHT, buff=0).move_to(UP * 2.3)
        pl = label(r"The Pile (2020): \ $22$ sources, \ weights set by hand", font_size=22, color=GREY_A)
        pl.next_to(pile, UP, buff=0.15)
        doremi = VGroup(
            label(r"DoReMi \ (Xie et al., 2023)", font_size=32, color=EDU),
            label(rf"a ${D['proxy'] / 1e6:.0f}$M proxy model plays a game against the worst-predicted domains", font_size=25,
                  color=GREY_A),
            label(rf"its weights train an ${D['target'] / 1e9:.0f}$B model: \ $+{D['gain']}$ points few-shot, \ "
                  rf"the same accuracy in $1/{D['speedup']}$ of the steps", font_size=25, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        regmix = VGroup(
            label(r"RegMix \ (Liu et al., 2024)", font_size=32, color=KEPT),
            label(rf"${R['models']}$ models of ${R['params'] / 1e6:.0f}$M parameters, \ each on a random mixture", font_size=25,
                  color=GREY_A),
            label(r"a regression from mixture to loss; \ the best mixture it predicts", font_size=25, color=GREY_A),
            label(rf"trains a ${R['big'] / 1e9:.0f}$B model on ${R['big_tokens'] / 1e9:.0f}$B tokens: \ best of "
                  rf"${R['candidates']}$ mixtures tried", font_size=25, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        both = VGroup(doremi, regmix).arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        if both.width > 13.0:
            both.width = 13.0
        both.move_to(DOWN * 0.75)
        src = cite(r"Gao et al.\ (2020); \ Xie et al., DoReMi (NeurIPS 2023); \ Liu et al., RegMix (ICLR 2025)",
                   font_size=17)
        with self.voiceover(
            "A corpus is a mixture: web pages, encyclopedias, code, books, maths, papers. How much of each? "
            "<bookmark mark='a'/> In 2020 The Pile set its weights by hand: a quarter web, nine percent Wikipedia, and "
            "twenty other sources. <bookmark mark='b'/> In 2023 DoReMi learned them: a small proxy model trains while an "
            "adversary keeps raising the weight of whichever domain it predicts worst relative to a reference model, and "
            "the weights it ends with let an eight-billion-parameter model reach the baseline in 2.6 times fewer steps. "
            "<bookmark mark='c'/> In 2024 RegMix made it a regression: train 512 tiny models on random mixtures, fit the "
            "loss you care about as a function of the mixture, and train the big model on the mixture the fit likes best. "
            "Its pick beat all 64 mixtures they tried at a billion parameters."
        ) as vo:
            self.play(FadeIn(pl), FadeIn(src), LaggedStart(*[FadeIn(r_) for r_ in pile], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(Indicate(pile, scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(doremi, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(regmix, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def regmix(self):
        M = load("mixture")
        proxy = M["proxy"]
        sizes = np.asarray(M["sizes"])
        groups = VGroup()
        for k, (name, nb) in enumerate(zip(GROUP_TEX, M["books"].values())):
            groups.add(VGroup(Square(0.28, stroke_width=0, fill_color=GROUP_C[k], fill_opacity=0.9),
                              label(rf"{name}: \ ${nb}$ books, \ ${sizes[k] / 1e6:.1f}$M tokens", font_size=20,
                                    color=GROUP_C[k])).arrange(RIGHT, buff=0.15))
        groups.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL, buff=0.4)
        tgt = label(r"target: \ chapters 1 and 3 of \textit{The Maltese Falcon} \\ (chapter 2, the scoreboard's, kept "
                    r"for the test)", font_size=20, color=C.BITS).next_to(groups, DOWN, buff=0.3).align_to(groups, LEFT)
        y = np.array([p_["target"] for p_ in proxy])
        w0 = np.array([p_["w"][0] for p_ in proxy])
        lo, hi = math.floor(y.min() * 10) / 10, math.ceil(y.max() * 10) / 10
        g = axes([0, 1], [lo, hi], x_length=5.2, y_length=3.4, xlabel=r"share of American novels in the mixture",
                 ylabel=r"loss on the target (nats per token)", xticks=[0, 0.5, 1], yticks=[lo, hi],
                 center=[3.6, 1.2, 0], font_size=18)
        dots = VGroup(*[Dot(g.ax.c2p(a, b), radius=0.06, color=WHITE) for a, b in zip(w0, y)])
        loo = np.asarray(M["loo"])
        g2 = axes([lo, hi], [lo, hi], x_length=2.6, y_length=2.0, xlabel=r"actual", ylabel=r"predicted, \ left out",
                  xticks=[lo, hi], yticks=[lo, hi], center=[-3.8, -2.0, 0], font_size=16)
        d2 = VGroup(*[Dot(g2.ax.c2p(a, b), radius=0.04, color=KEPT) for a, b in zip(y, loo)])
        diag = DashedLine(g2.ax.c2p(lo, lo), g2.ax.c2p(hi, hi), color=GREY_B, dash_length=0.05)
        corr = label(rf"correlation ${M['loo_corr']:.2f}$", font_size=18, color=KEPT).next_to(g2, RIGHT, buff=0.15)
        nat, best = np.asarray(M["natural"]), np.asarray(M["best"])
        fan = VGroup()
        if all(p_.get("evals") for p_ in proxy):
            evs = [np.asarray(p_["evals"]) for p_ in proxy]
            top = min(8.6, max(e[:, 1].max() for e in evs))
            bot = math.floor(min(e[:, 1].min() for e in evs) * 4) / 4
            gf = axes([0, M["proxy_spec"]["steps"]], [bot, top], x_length=3.6, y_length=1.9, xlabel=r"step",
                      ylabel=r"held-out loss", xticks=[0, M["proxy_spec"]["steps"]], yticks=[bot, round(top, 1)],
                      yfmt=lambda v: f"{v:.1f}", center=[-3.6, -2.05, 0], font_size=15)
            wmax = max(float(p_["w"][0]) for p_ in proxy)
            curves = VGroup(*[curve(gf.ax, e[:, 0], np.minimum(e[:, 1], top),
                                    interpolate_color(ManimColor(GREY_D), ManimColor(GROUP_C[0]), float(p_["w"][0]) / wmax),
                                    1.8) for e, p_ in zip(evs, proxy)])
            fan = VGroup(gf, curves, note(r"each run's training, \\ coloured by \\ its American share", font_size=16)
                         .next_to(gf, RIGHT, buff=0.25).align_to(gf, UP))
        # the thirty novels on a shelf, by group; the target book and its chapters
        shelf = VGroup()
        for k, nb in enumerate(M["books"].values()):
            shelf.add(VGroup(*[Rectangle(width=0.16, height=1.25 + 0.45 * (((7 * i + 3 * k) % 5) / 4), stroke_width=1,
                                         stroke_color=BLACK, fill_color=GROUP_C[k], fill_opacity=0.85)
                               for i in range(nb)]).arrange(RIGHT, buff=0.03, aligned_edge=DOWN))
        shelf.arrange(RIGHT, buff=0.32, aligned_edge=DOWN).move_to([3.4, 1.5, 0])
        snote = note(r"the thirty novels, \ in four groups", font_size=18).next_to(shelf, DOWN, buff=0.15)
        falcon = shelf[0][0]
        chaps = VGroup(*[VGroup(RoundedRectangle(width=1.5, height=0.5, corner_radius=0.08, stroke_width=1.5,
                                                 stroke_color=C.BITS if c_ != 2 else KEPT,
                                                 fill_color=C.BITS if c_ != 2 else KEPT, fill_opacity=0.2),
                                label(rf"ch.~${c_}$: \ " + (r"tune" if c_ != 2 else r"test"), font_size=19,
                                      color=C.BITS if c_ != 2 else KEPT)) for c_ in (1, 2, 3)])
        for c_ in chaps:
            c_[1].move_to(c_[0])
        chaps.arrange(RIGHT, buff=0.2).move_to([3.4, -0.7, 0])
        fl = label(r"\textit{The Maltese Falcon}", font_size=22, color=C.BITS).next_to(chaps, UP, buff=0.2)
        farrow = Arrow(fl.get_top(), falcon.get_bottom(), buff=0.1, color=C.BITS, stroke_width=2.5,
                       max_tip_length_to_length_ratio=0.15)

        def mixbar(w, y_, title):
            row = VGroup()
            x = 0.0
            for k, v in enumerate(w):
                r_ = Rectangle(width=max(4.4 * v, 0.02), height=0.42, stroke_width=1, stroke_color=BLACK,
                               fill_color=GROUP_C[k], fill_opacity=0.9)
                r_.move_to([1.3 + x + 4.4 * v / 2, y_, 0])
                row.add(r_)
                x += 4.4 * v
            t = label(title, font_size=20, color=GREY_A).next_to(row, LEFT, buff=0.15)
            return VGroup(t, row)

        mb = VGroup(mixbar(nat, -1.6, r"natural"), mixbar(best, -2.3, r"RegMix's pick"))
        tag = note(rf"computed: \ ${len(proxy)}$ runs of a ${M['proxy_spec']['d']}$-wide, "
                   rf"${M['proxy_spec']['layers']}$-layer model, \ ${M['proxy_spec']['steps']}$ steps each",
                   font_size=18).to_corner(DR, buff=0.2)
        shares = ", ".join(f"{100 * v:.0f}" for v in best)
        rho = float(np.corrcoef(w0, y)[0, 1])
        if rho < -0.4:
            trend = "the more American text, the lower the loss, though the other three groups matter too"
        elif rho < -0.1:
            trend = "more American text helps a little, but the other groups matter as much"
        else:
            trend = "the share of American text alone doesn't decide it"
        am = best[0] - nat[0]
        if best[0] > 0.75:
            lean = "puts nearly everything on the American novels"
        elif am > 0.05:
            lean = "leans toward the American novels"
        elif am < -0.05:
            lean = "moves away from the American novels"
        else:
            lean = "stays close to the natural mixture"
        with self.voiceover(
            "We ran RegMix on the thirty novels. Split them into four groups: American novels, English novels of "
            "society, adventure and mystery, and the translations with Ulysses. <bookmark mark='a'/> Our target is "
            "the scoreboard's own book, The Maltese Falcon, an American detective novel of 1930; we tune on its "
            "first and third chapters and keep the second, the scoreboard's passage, for the test. "
            f"<bookmark mark='b'/> {len(proxy)} tiny models, each on a random mixture. Here is each one's loss on the "
            "target against its share of American novels: " + trend + ". "
            "<bookmark mark='c'/> A regression on the four weights and their products predicts each run's loss from "
            f"the other runs with a correlation of {M['loo_corr']:.2f}. <bookmark mark='d'/> Asked for the best "
            f"mixture, it {lean}: {shares} percent of the four groups, against the natural proportions of the books."
        ) as vo:
            self.play(FadeIn(groups), FadeIn(tag), LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for gr in shelf for b_ in gr],
                                                                lag_ratio=0.04), FadeIn(snote), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(tgt), falcon.animate.set_stroke(YELLOW, width=3), FadeIn(fl), GrowArrow(farrow))
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.1) for c_ in chaps], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeOut(VGroup(shelf, snote, chaps, fl, farrow)))
            if len(fan):
                self.play(FadeIn(fan[0]), FadeIn(fan[2]), LaggedStart(*[Create(c_) for c_ in fan[1]], lag_ratio=0.03),
                          run_time=2.5)
            self.play(FadeIn(g), LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in dots], lag_ratio=0.05), run_time=2.5)
            vo.wait_until("c")
            if len(fan):
                self.play(FadeOut(fan))
            self.play(FadeIn(g2), Create(diag), LaggedStart(*[FadeIn(d_) for d_ in d2], lag_ratio=0.03), FadeIn(corr))
            vo.wait_until("d")
            self.play(FadeIn(mb[0]), run_time=0.8)
            self.play(FadeIn(mb[1]), run_time=0.8)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tested(self):
        M = load("mixture")
        T = M["tests"]
        names = [("natural", r"natural", GREY_B), ("uniform", r"a quarter each", "#FFB86B"),
                 ("regmix", r"RegMix's pick", KEPT)]
        test = {n: [T[f"test_{n}_{s}"]["test"] for s in (0, 1)] for n, _, _ in names}
        val = {n: [T[f"test_{n}_{s}"]["val"] for s in (0, 1)] for n, _, _ in names}
        allv = [v for n in test for v in test[n]]
        lo, hi = math.floor(min(allv) * 20) / 20 - 0.05, math.ceil(max(allv) * 20) / 20 + 0.05
        allh = [v for n in val for v in val[n]]
        lo2, hi2 = math.floor(min(allh) * 20) / 20 - 0.05, math.ceil(max(allh) * 20) / 20 + 0.05

        def panel(vals, lo_, hi_, title, center):
            g = axes([0, 3], [lo_, hi_], x_length=4.2, y_length=3.4, ylabel=title, yticks=[lo_, hi_],
                     yfmt=lambda v: f"{v:.2f}", center=center, font_size=18)
            marks = VGroup()
            for i, (n, nm, col) in enumerate(names):
                for v in vals[n]:
                    marks.add(Dot(g.ax.c2p(i + 0.5, v), radius=0.08, color=col))
                marks.add(Line(g.ax.c2p(i + 0.3, np.mean(vals[n])), g.ax.c2p(i + 0.7, np.mean(vals[n])), color=col,
                               stroke_width=4))
                marks.add(label(nm, font_size=18, color=col).next_to(g.ax.c2p(i + 0.5, lo_), DOWN, buff=0.15))
            return VGroup(g, marks)

        p1 = panel(test, lo, hi, r"loss on the scoreboard's passage", [-3.4, 0.4, 0])
        p2 = panel(val, lo2, hi2, r"loss on all thirty novels (held out)", [3.4, 0.4, 0])
        spec = M["test_spec"]
        head = label(rf"each mixture, \ a ${spec['d']}$-wide model, \ ${spec['steps']}$ steps, \ two seeds",
                     font_size=22, color=GREY_A).to_edge(UP, buff=0.4)
        r, n_ = np.mean(test["regmix"]), np.mean(test["natural"])
        spread = max(abs(test["regmix"][0] - test["regmix"][1]), abs(test["natural"][0] - test["natural"][1]))
        rv, nv = np.mean(val["regmix"]), np.mean(val["natural"])
        if n_ - r > max(spread, 0.01):
            verdict = (f"On the held-out chapter, RegMix's pick beats the natural mixture, {r:.3f} nats against "
                       f"{n_:.3f}, by more than the gap between seeds.")
        elif r - n_ > max(spread, 0.01):
            verdict = (f"On the held-out chapter, RegMix's pick does worse than the natural mixture, {r:.3f} nats "
                       f"against {n_:.3f}: the regression, fitted on tiny models, didn't carry to a larger one.")
        else:
            verdict = (f"On the held-out chapter, RegMix's pick and the natural mixture are within the noise of two "
                       f"seeds, {r:.3f} and {n_:.3f} nats: at our scale, the mixture of thirty novels matters less "
                       "than luck.")
        spread_v = max(abs(val["regmix"][0] - val["regmix"][1]), abs(val["natural"][0] - val["natural"][1]))
        if rv - nv > max(spread_v, 0.005):
            cost = (f"And on the thirty novels as a whole it pays, {rv:.3f} nats against {nv:.3f}: tuning toward one "
                    "book costs the others.")
        else:
            cost = "And on the thirty novels as a whole it costs nothing we can measure."
        tw = take_away(r"a mixture is chosen for a target: \ say which, \ and test on held-out text", font_size=24)
        trn = VGroup()
        if all(T[f"test_{n}_{s_}"].get("evals") for n, _, _ in names for s_ in (0, 1)):
            evs = {(n, s_): np.asarray(T[f"test_{n}_{s_}"]["evals"]) for n, _, _ in names for s_ in (0, 1)}
            top = min(8.6, max(e[:, 1].max() for e in evs.values()))
            bot = math.floor(min(e[:, 1].min() for e in evs.values()) * 4) / 4
            gt = axes([0, spec["steps"]], [bot, top], x_length=4.2, y_length=3.4, xlabel=r"step",
                      ylabel=r"held-out loss, \ all thirty novels", xticks=[0, spec["steps"]],
                      yticks=[bot, round(top, 1)], yfmt=lambda v: f"{v:.1f}", center=[3.4, 0.4, 0], font_size=18)
            lines = VGroup()
            for (n, s_), e in evs.items():
                col = next(c for n2, _, c in names if n2 == n)
                c_ = curve(gt.ax, e[:, 0], np.minimum(e[:, 1], top), col, 2.5)
                lines.add(DashedVMobject(c_, num_dashes=30) if s_ else c_)
            trn = VGroup(gt, lines, note(r"their training: \ solid seed $0$, \ dashed seed $1$", font_size=16)
                         .next_to(gt, DOWN, buff=0.35))
        with self.voiceover(
            "Now the test: does the pick carry over to a larger model? We trained each mixture again, at the "
            "larger size, with two seeds. <bookmark mark='a'/> " + verdict + " <bookmark mark='b'/> " + cost +
            " <bookmark mark='c'/> That is the general lesson: a mixture is chosen for a target, so say which, and "
            "test on text the choice never saw."
        ) as vo:
            self.play(FadeIn(head), FadeIn(p1[0]), FadeIn(p1[1]))
            if len(trn):
                self.play(FadeIn(trn[0]), FadeIn(trn[2]), LaggedStart(*[Create(l_) for l_ in trn[1]], lag_ratio=0.2),
                          run_time=2.5)
            vo.wait_until("a")
            self.play(Indicate(p1[1], scale_factor=1.02))
            vo.wait_until("b")
            if len(trn):
                self.play(FadeOut(trn))
            self.play(FadeIn(p2[0]), FadeIn(p2[1]))
            vo.wait_until("c")
            self.play(FadeIn(tw, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def synthetic(self):
        K, W = F.KIMIK2, F.WRAP
        wrap = VGroup(
            label(r"WRAP \ (Maini et al., 2024)", font_size=26, color=EDU),
            label(r"an instruction-tuned model rewrites web pages: \ ``like Wikipedia'', \ ``as questions and answers''",
                  font_size=21, color=GREY_A),
            label(rf"real and rewritten text together: \ about ${W['speedup']}\times$ faster pretraining on C4",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.6)
        rows = hbars([(t, v, c) for (t, v), c in zip(K["rephrase"], [GREY_B, "#FFB86B", KEPT])], 32.0, width=4.6,
                     font_size=21, label_width=4.4, fmt=lambda v: rf"${v:.2f}\%$")
        rows.move_to([1.6, -0.9, 0])
        rh = label(r"Kimi K2: \ SimpleQA accuracy after training on the same knowledge text", font_size=22,
                   color=KEPT).next_to(rows, UP, buff=0.3)
        src = cite(r"Maini et al.\ (2024); \ Kimi Team (2025), Table 1; \ Muennighoff et al.\ (2023)", font_size=17)
        rep = label(rf"repeating data: \ up to ${F.REPEAT['epochs']}$ epochs about as good as new data, \ then "
                    r"returns fall", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.85)
        rs = F.REPEAT["rd_star"]
        ep = np.linspace(1, 40, 200)
        worth = 1 + rs * (1 - np.exp(-(ep - 1) / rs))  # in epochs of unique data
        gr = axes([0, 40], [0, 40], x_length=4.6, y_length=3.0, xlabel=r"epochs over the same tokens",
                  ylabel=r"worth, in epochs of new data", xticks=[0, 4, 10, 20, 30, 40], yticks=[0, 10, 20, 30, 40],
                  center=[-0.6, -0.55, 0], font_size=17)
        new_ = DashedLine(gr.ax.c2p(0, 0), gr.ax.c2p(40, 40), color=GREY_B, dash_length=0.06)
        wc = curve(gr.ax, ep, worth, EDU, 3)
        w4 = 1 + rs * (1 - math.exp(-(F.REPEAT["epochs"] - 1) / rs))
        d4 = Dot(gr.ax.c2p(F.REPEAT["epochs"], w4), radius=0.06, color=YELLOW)
        l4 = label(rf"${F.REPEAT['epochs']}$ epochs: \ worth ${w4:.1f}$", font_size=18, color=YELLOW)
        l4.next_to(d4, RIGHT, buff=0.15).shift(UP * 0.2)
        rlg = legend([(GREY_B, r"new data"), (EDU, r"repeated: \ Muennighoff et al.'s fit")], font_size=17)
        rlg.next_to(gr, RIGHT, buff=0.3).align_to(gr, UP)
        rplot = VGroup(gr, new_, wc, d4, l4, rlg)
        with self.voiceover(
            "When good text runs short, there are two ways to stretch it. Repeat it: Muennighoff and colleagues found "
            "in 2023 that up to about four passes over the same data are nearly as good as new data; after that the "
            "returns fall away. <bookmark mark='a'/> Or rewrite it: in 2024 WRAP, from Apple and Carnegie Mellon, had a "
            "model rephrase noisy web pages as encyclopedia entries or questions and answers, and real and rephrased text "
            "together reached the same quality about three times faster. <bookmark mark='b'/> Kimi K2's report measured "
            "it on knowledge. Text repeated ten times taught a model to answer "
            f"{K['rephrase'][0][1]:.2f} percent of a set of factual questions; rephrased once and repeated ten times, "
            f"{K['rephrase'][1][1]:.2f}; rephrased ten different ways and read once each, {K['rephrase'][2][1]:.2f}."
        ) as vo:
            self.play(FadeIn(rep), FadeIn(src), FadeIn(gr), FadeIn(rlg), Create(new_))
            self.play(Create(wc), run_time=2.5)
            self.play(FadeIn(d4, scale=1.5), FadeIn(l4))
            vo.wait_until("a")
            self.play(FadeIn(wrap, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeOut(rplot), FadeOut(rep))
            self.play(FadeIn(rh), LaggedStart(*[AnimationGroup(FadeIn(r_[0]), GrowFromEdge(r_[1], LEFT), FadeIn(r_[2]))
                                                for r_ in rows], lag_ratio=0.5), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def collapse(self):
        Cl = load("collapse")
        rep, acc = np.asarray(Cl["replace"]), np.asarray(Cl["accumulate"])
        gens = Cl["gens"]
        x = np.arange(gens + 1)
        top = float(rep[:, 0, 0].mean())
        g = axes([0, gens], [0, 3500], x_length=5.4, y_length=3.4, xlabel=r"generation",
                 ylabel=r"tokens the model can still produce", xticks=[0, 10, 20, 30], yticks=[0, 1000, 2000, 3000],
                 yfmt=lambda v: f"{int(v):,}".replace(",", "{,}"), center=[-3.3, -0.5, 0], font_size=18)
        g2 = axes([0, gens], [9.6, 10.8], x_length=5.0, y_length=3.4, xlabel=r"generation",
                  ylabel=r"cross-entropy on real text (bits)", xticks=[0, 10, 20, 30], yticks=[9.6, 10.2, 10.8],
                  center=[3.6, -0.5, 0], font_size=18)
        rc = curve(g.ax, x, rep[:, :, 0].mean(0), REMOVED, 3)
        ac = curve(g.ax, x, acc[:, :, 0].mean(0), KEPT, 3)
        rb = band(g.ax, x, rep[:, :, 0].min(0), rep[:, :, 0].max(0), REMOVED)
        rc2 = curve(g2.ax, x, rep[:, :, 1].mean(0), REMOVED, 3)
        ac2 = curve(g2.ax, x, acc[:, :, 1].mean(0), KEPT, 3)
        lg = legend([(REMOVED, r"each generation trained on the last one's samples"),
                     (KEPT, r"each generation trained on everything so far")], font_size=18).to_edge(UP, buff=0.5)
        sch = note(rf"computed: \ a unigram model of the novels' tokens, \ ${Cl['n'] // 1000}$k samples a generation, "
                   rf"\ ${Cl['seeds']}$ seeds", font_size=18).to_corner(DR, buff=0.2)
        start, end = rep[:, 0, 0].mean(), rep[:, -1, 0].mean()
        lost = rep[:, -1, 2].mean()
        ce_r, ce_a = rep[:, :, 1].mean(0), acc[:, :, 1].mean(0)
        if (np.diff(ce_r) > 0).all():
            climb = "Its cross-entropy on real text climbs with every generation."
        elif ce_r[-1] > ce_r[0]:
            climb = "Its cross-entropy on real text climbs over the generations."
        else:
            climb = "Its cross-entropy on real text barely moves."
        kept_all = acc[:, -1, 0].mean() >= acc[:, 0, 0].mean()
        small = (ce_a[-1] - ce_a[0]) < 0.5 * (ce_r[-1] - ce_r[0])
        if kept_all and small:
            cure = "Nothing real is lost, and the damage stays small."
        elif small:
            cure = "The damage stays much smaller."
        else:
            cure = "Here it only slows the damage."
        src = cite(r"Shumailov et al., \textit{Nature} (2024); \ Gerstgrasser et al.\ (2024)", font_size=17)
        chain = stage_row([(r"real text", KEPT), (r"model 1", GREY_A), (r"its samples", REMOVED), (r"model 2", GREY_A),
                           (r"its samples", REMOVED), (r"model 3", GREY_A)], font_size=18)
        if chain.width > 12.4:
            chain.width = 12.4
        chain.move_to(UP * 2.3)
        s_lab = label(f"${start:,.0f}$".replace(",", "{,}"), font_size=18, color=REMOVED).next_to(g.ax.c2p(0, start), RIGHT,
                                                                                                 buff=0.15).shift(UP * 0.2)
        e_lab = label(f"${end:,.0f}$".replace(",", "{,}"), font_size=18, color=REMOVED).next_to(g.ax.c2p(gens, end), UP,
                                                                                               buff=0.15)
        with self.voiceover(
            "But training on a model's output has a known failure. Shumailov and colleagues called it model collapse, in "
            "Nature in 2024: train each generation on the last one's samples, and the tails of the distribution vanish. "
            "We can watch it in the simplest language model there is, the frequencies of the novels' tokens. "
            "<bookmark mark='a'/> Fit it to fifty thousand real tokens, sample fifty thousand from it, fit the next "
            "generation to those, and repeat: a rare token that once fails to be sampled is gone for good. "
            f"<bookmark mark='b'/> Over {gens} generations, the tokens it can produce fall from {start:,.0f} to "
            f"{end:,.0f}, and the lost ones carried {100 * lost:.0f} percent of real text. <bookmark mark='c'/> " + climb +
            " <bookmark mark='d'/> Gerstgrasser and colleagues found the way out the same year: keep the real data, and "
            "add each generation's samples to it instead of replacing it. " + cure + " That is how synthetic data is used "
            "in 2026: alongside real text, never instead of it."
        ) as vo:
            self.play(FadeIn(g), FadeIn(g2), FadeIn(sch), FadeIn(src), FadeIn(lg[0]))
            self.play(LaggedStart(*[FadeIn(b_) for b_ in chain.boxes], *[GrowArrow(a_) for a_ in chain.arrows],
                                  lag_ratio=0.15), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(rb), Create(rc), run_time=6.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(s_lab), FadeIn(e_lab))
            vo.wait_until("c")
            self.play(Create(rc2), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(lg[1]), Create(ac), Create(ac2), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
