from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai24.common import (Scrub, BEIT_C, HIST, MAE_C, PART, SIMCLR, arrow, axes, bars_chart, digit, digit_sheet,
                                   ink_rgb, load, node_box, pct, seed_curves, tag, take_away, to_image)


class Masked(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.mae()
        self.replay()
        self.ratio()
        self.beit()
        self.verdict()

    def card(self):
        card = chapter_card(11, r"Fill in the blanks: \ MAE and BEiT", r"Does predicting pixels teach what a digit is?",
                            lit=(2018,), part=PART)
        with self.voiceover("Chapter eleven. Fill in the blanks: MAE and BEiT."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def history(self):
        cards = VGroup(
            history_card(2008, r"Vincent, Larochelle, Bengio \& Manzagol", r"denoising autoencoders: \ corrupt the "
                         r"input, \ reconstruct the clean one", color=MAE_C, width=4.2, font_size=20),
            history_card(2018, r"Devlin et al.: \ BERT", r"hide $15\%$ of the words, \ predict them \ (Part 14)",
                         color=HIST, width=4.2, font_size=20),
            history_card(2021, r"Bao et al.: \ BEiT; \ He et al.: \ MAE", r"hide image patches; \ predict their "
                         r"tokens, \ or their pixels", color=BEIT_C, width=4.2, font_size=20),
        ).arrange(RIGHT, buff=0.3).move_to(UP * 1.1)
        why_ = label(r"text is dense: \ hide $15\%$; \ \ images are redundant: \ hide $75\%$", font_size=28,
                     color=GREY_A).move_to(DOWN * 1.6)
        sub = label(r"a neighbouring pixel gives most of a hidden pixel away", font_size=22, color=GREY_B)
        sub.next_to(why_, DOWN, buff=0.25)
        with self.voiceover(
            "The second family hides part of the input and asks for it back. In 2008, denoising autoencoders "
            "corrupted an input and learned to restore it. <bookmark mark='a'/> In 2018 BERT hid fifteen percent of "
            "the words in a sentence and learned language by guessing them, as Part 14 showed. <bookmark mark='b'/> "
            "In 2021 the idea came to vision transformers twice: BEiT, which predicts discrete tokens of the hidden "
            "patches, and MAE, which predicts their pixels. <bookmark mark='c'/> The one big change from text is "
            "how much to hide. Words are dense with meaning; images are redundant, and a neighbouring pixel gives "
            "most of a hidden pixel away. MAE hides three quarters of the image."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.15))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(why_), FadeIn(sub))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mae(self):
        m = load("mae")
        orig = np.asarray(m["orig"])[1].astype(float) / 255.0
        hid = np.asarray(m["rec_masked"])[-1][1]
        rec = np.asarray(m["rec_recon"])[-1][1]
        x = digit(orig, 1.5, frame=True).move_to([-5.6, 0.8, 0])
        xm = digit(hid, 1.5, frame=True).move_to([-3.4, 0.8, 0])
        enc = node_box(r"encoder \\ (visible patches)", MAE_C, font_size=20, height=1.2).move_to([-1.1, 0.8, 0])
        dec = node_box(r"small \\ decoder", GREY_B, font_size=20, height=1.2).move_to([1.0, 0.8, 0])
        out = digit(rec, 1.5, frame=True).move_to([3.2, 0.8, 0])
        arrs = VGroup(arrow(x.get_right(), xm.get_left()), arrow(xm.get_right(), enc.get_left()),
                      arrow(enc.get_right(), dec.get_left()), arrow(dec.get_right(), out.get_left()))
        loss = label(r"loss: \ squared error \\ on the hidden patches only", font_size=22, color=C.LOSS).move_to(
            [5.6, 0.8, 0])
        vit = label(r"MAE's vision transformer drops the hidden patches: \ the encoder works on a quarter of the image, "
                    r"\\ three times faster or more; \ ViT-Huge: \ $87.8\%$ on ImageNet after fine-tuning",
                    font_size=21, color=GREY_A).move_to([0, -1.6, 0])
        ours = label(r"ours: \ the same convolutional network as every other method; \ hidden patches are blanked",
                     font_size=21, color=MAE_C).next_to(vit, DOWN, buff=0.35)
        src = cite(r"He, Chen, Xie, Li, Doll\'ar \& Girshick (2022): \ MAE")
        with self.voiceover(
            "Kaiming He's masked autoencoder is simple. Cut the image into patches, hide three quarters of them at "
            "random, <bookmark mark='a'/> encode what is left, <bookmark mark='b'/> and let a small decoder paint "
            "the whole image, scored only on the patches it could not see. <bookmark mark='c'/> MAE's encoder is a "
            "vision transformer, which can simply skip the hidden patches, so it trains three or more times "
            "faster; fine-tuned, the largest reached 87.8 percent on ImageNet. <bookmark mark='d'/> Ours uses the "
            "same convolutional network as every other method in this part, so the hidden patches are blanked out "
            "instead. Forty-nine patches of four by four pixels, thirty-seven of them hidden."
        ) as vo:
            self.play(FadeIn(x), FadeIn(src))
            self.play(GrowArrow(arrs[0]), FadeIn(xm))
            vo.wait_until("a")
            self.play(GrowArrow(arrs[1]), FadeIn(enc))
            vo.wait_until("b")
            self.play(GrowArrow(arrs[2]), FadeIn(dec), GrowArrow(arrs[3]), FadeIn(out), FadeIn(loss))
            vo.wait_until("c")
            self.play(FadeIn(vit))
            vo.wait_until("d")
            self.play(FadeIn(ours))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        m = load("mae")
        steps = np.asarray(m["rec_steps"])
        HM, RC = np.asarray(m["rec_masked"]), np.asarray(m["rec_recon"])
        orig = np.asarray(m["orig"])
        n = len(steps)
        tr = ValueTracker(0)

        sh = Scrub([digit_sheet(np.concatenate([HM[i], RC[i], orig.astype(np.uint8)]), 3, 6, size=0.95,
                                gap=0.1).move_to([-1.3, -0.2, 0]) for i in range(n)], tr)
        f0 = sh.frames[0]
        rl = VGroup(label(r"what it sees", font_size=20, color=GREY_A), label(r"its reconstruction", font_size=20,
                                                                              color=MAE_C),
                    label(r"the original", font_size=20, color=GREY_A))
        for k, r_ in enumerate(rl):
            r_.next_to([f0.get_left()[0], f0.get_top()[1] - 0.06 - 0.475 - 1.05 * k, 0], LEFT, buff=0.2)
        runs, keys = m["runs"], m["keys"]["0.75"]
        S_ = runs[keys[0]]["steps"][-1]
        lmax = max(max(x for x in runs[k]["loss"] if np.isfinite(x)) for k in keys)
        ax = axes([0, S_], [0, lmax * 1.05], x_length=3.6, y_length=2.6, xlabel=r"training step",
                  ylabel=r"loss on hidden pixels", xticks=[0, S_], center=[4.6, 0.0, 0])
        lc = seed_curves(ax.ax, runs, keys, "loss", MAE_C)
        st = always_redraw(lambda: label(rf"step ${steps[int(np.clip(round(tr.get_value()), 0, n - 1))]}$", font_size=22,
                                         color=GREY_A).next_to(f0, UP, buff=0.25))
        tg = tag(r"computed: \ $75\%$ hidden, \ the same masks at every snapshot; \ three seeds")
        with self.voiceover(
            "Here is ours learning, on six test digits, with the same patches hidden at every snapshot. <bookmark "
            "mark='a'/> At first the decoder paints grey mush. Within a few dozen steps it has learned that most "
            "of the picture is black, <bookmark mark='b'/> then where strokes go, and by the end it fills in "
            "strokes it never saw, continuing the visible ones. <bookmark mark='c'/> To do that it has to know "
            "something about how digits are drawn."
        ) as vo:
            self.play(FadeIn(sh), FadeIn(rl), FadeIn(st), FadeIn(tg), FadeIn(ax))
            vo.wait_until("a")
            self.play(tr.animate.set_value(n * 0.4), Create(lc), run_time=max(2.0, vo.until("b")), rate_func=linear)
            vo.wait_until("b")
            self.play(tr.animate.set_value(n - 1), run_time=max(2.0, vo.until("c")), rate_func=linear)
        sh.clear_updaters()
        st.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ratio(self):
        m = load("mae")
        S = m["summary"]
        rs = ["0.5", "0.75", "0.9"]
        lin = [S[r]["linear"] for r in rs]
        few = [S[r]["few"] if "few" in S[r] else None for r in rs]
        lo = float(np.floor((min(x[1] for x in lin) - 0.02) * 50) / 50)
        ch = bars_chart([x[0] for x in lin], [MAE_C] * 3, [r"$50\%$ hidden", r"$75\%$", r"$90\%$"], height=3.0,
                        bar_w=1.0, gap=0.8, vmin=lo, vmax=1.0, spread=[(x[1], x[2]) for x in lin],
                        value_fmt=lambda v: pct(v), font_size=24).move_to([-2.6, -0.5, 0])
        cl = label(rf"linear probe, \% \ (axis from ${pct(lo, 0)}$)", font_size=22, color=GREY_A).next_to(ch, UP,
                                                                                                       buff=0.3)
        ex = []
        for r in ("0.5", "0.9"):
            k = m["keys"][r][0]
            ex.append(k)
        best = rs[int(np.argmax([x[0] for x in lin]))]
        v = (f"Hiding three quarters gives the best probe, {pct(lin[1][0])} percent; half gives {pct(lin[0][0])}, "
             f"nine tenths {pct(lin[2][0])}." if best == "0.75" else
             f"On our digits the best ratio is {pct(float(best), 0)} percent hidden: probes of {pct(lin[0][0])}, "
             f"{pct(lin[1][0])} and {pct(lin[2][0])} percent for half, three quarters and nine tenths.")
        n1 = label(r"too little hidden: \ copy from the neighbours", font_size=22, color=GREY_A).move_to([3.6, 0.8, 0])
        n2 = label(r"too much hidden: \ guess blindly", font_size=22, color=GREY_A).move_to([3.6, -0.2, 0])
        tg = tag(r"computed: \ $75\%$: three seeds; \ $50\%$ and $90\%$: one each")
        with self.voiceover(
            "How much to hide? Too little, and the network can copy from the neighbours; too much, and it can only "
            "guess. <bookmark mark='a'/> We trained ours at three ratios. <bookmark mark='b'/> " + v
        ) as vo:
            self.play(FadeIn(n1), FadeIn(n2))
            vo.wait_until("a")
            self.play(FadeIn(cl), FadeIn(ch[0]), FadeIn(ch.names), FadeIn(tg))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in ch.bars], lag_ratio=0.2), FadeIn(ch.whiskers),
                      FadeIn(ch.vals))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def beit(self):
        b = load("beit")
        cb = np.asarray(b["codebook"]).reshape(-1, 4, 4)
        use = np.asarray(b["use"])
        order = np.argsort(-use)
        book = digit_sheet(np.clip(cb[order], 0, 1), 8, 8, size=0.32, gap=0.05).move_to([-4.6, -0.3, 0])
        bl = label(r"$64$ codes: \ $k$-means \\ on $4 \times 4$ patches", font_size=20, color=BEIT_C).next_to(book, UP,
                                                                                                       buff=0.2)
        orig = np.asarray(b["orig"])[2].astype(float) / 255.0
        quant = np.asarray(b["quant"])[2]
        codes = np.asarray(b["codes"])[2].reshape(7, 7)
        d1 = digit(orig, 1.7, frame=True).move_to([-1.2, 0.5, 0])
        d2 = digit(quant, 1.7, frame=True).move_to([1.2, 0.5, 0])
        grid = VGroup(*[MathTex(str(int(c)), font_size=16, color=BEIT_C) for c in codes.ravel()])
        grid.arrange_in_grid(7, 7, buff=(0.08, 0.06)).move_to([4.2, 0.5, 0])
        l1 = label(r"a digit", font_size=20, color=GREY_A).next_to(d1, UP, buff=0.15)
        l2 = label(r"as codes", font_size=20, color=BEIT_C).next_to(d2, UP, buff=0.15)
        l3 = label(r"the $49$ tokens", font_size=20, color=BEIT_C).next_to(grid, UP, buff=0.15)
        runs, keys = b["runs"], b["keys"]
        accs = [runs[k]["logs"][-1]["acc"] for k in keys]
        task = label(rf"hide $40\%$ of the patches; \ predict each hidden patch's code out of $64$: \\ right "
                     rf"${pct(np.mean(accs), 0)}\%$ of the time by the end of training", font_size=22,
                     color=GREY_A).to_edge(DOWN, buff=0.7)
        src = cite(r"Bao, Dong, Piao \& Wei (2022): \ BEiT, \ with DALL$\cdot$E's tokenizer of $8{,}192$ codes", corner=UR)
        with self.voiceover(
            "BEiT's targets are tokens instead of pixels. It borrowed the image tokenizer of OpenAI's first DALL·E, "
            "which turns each patch into one of eight thousand discrete codes. <bookmark mark='a'/> Ours is simpler, "
            "a codebook like the ones in Part 23: k-means on four-by-four patches, sixty-four codes. <bookmark "
            "mark='b'/> A digit becomes forty-nine tokens, <bookmark mark='c'/> and the network, shown the digit "
            "with forty percent of its patches hidden, must name each hidden patch's code, as BERT names a hidden "
            f"word. By the end it is right {pct(np.mean(accs), 0)} percent of the time."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(book), FadeIn(bl))
            vo.wait_until("b")
            self.play(FadeIn(d1), FadeIn(l1), FadeIn(d2), FadeIn(l2), FadeIn(grid), FadeIn(l3))
            vo.wait_until("c")
            self.play(FadeIn(task))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def verdict(self):
        m = load("mae")
        b = load("beit")
        s = load("simclr")
        rows = [(r"SimCLR", SIMCLR, s["summary"]["0.2"]), (r"MAE", MAE_C, m["summary"]["0.75"]),
                (r"BEiT-style", BEIT_C, b["summary"])]
        hdr = VGroup(label(r"", font_size=22), label(r"linear probe", font_size=22, color=GREY_A),
                     label(r"$k$-NN", font_size=22, color=GREY_A),
                     label(r"10 labels per digit", font_size=22, color=GREY_A))
        tab = VGroup(hdr)
        for n_, c_, sm in rows:
            tab.add(VGroup(label(n_, font_size=28, color=c_), MathTex(pct(sm["linear"][0]) + r"\%", font_size=32),
                           MathTex(pct(sm["knn"][0]) + r"\%", font_size=32),
                           MathTex(pct(sm["few"][0]) + r"\%", font_size=32)))
        xs = [-4.6, -1.6, 1.0, 3.8]
        for i, r_ in enumerate(tab):
            for j, x_ in enumerate(r_):
                x_.move_to([xs[j], 2.2 - 0.8 * i, 0])
        ml, sl = rows[1][2]["linear"][0], rows[0][2]["linear"][0]
        mk, sk = rows[1][2]["knn"][0], rows[0][2]["knn"][0]
        bl = rows[2][2]["linear"][0]
        un = float(np.mean([r["linear"] for r in load("baselines")["random_cnn"]]))
        if ml < un - 0.005:
            v = (f"Not on our network. Filling in pixels leaves a representation at {pct(ml)} percent on the linear "
                 f"probe, below even the untrained network's {pct(un)}, and far below SimCLR's {pct(sl)}; predicting "
                 f"codes gives {pct(bl)}. To paint strokes, each cell of the small map learned where ink goes near it; "
                 "averaged over the map, that says little about which digit it is.")
        elif ml < sl - 0.005:
            v = (f"Filling in pixels gives a representation {pct(sl - ml)} points behind SimCLR on the linear probe, "
                 f"and {pct(sk - mk)} behind by nearest neighbours. Predicting codes instead of pixels gives "
                 f"{pct(bl)} percent.")
        else:
            v = (f"On our digits, filling in pixels does as well as contrast: MAE {pct(ml)} percent against SimCLR's "
                 f"{pct(sl)}, and the code-predicting model {pct(bl)}.")
        lit = label(r"MAE's paper: \ weak linear probes, \ strong after fine-tuning; \\ a pixel target spends effort "
                    r"on details \ the probe does not need", font_size=22, color=GREY_A).move_to([0, -1.3, 0])
        tk = take_away(r"masked models learn by filling in; \ their features are rich, \ but not laid out flat for a "
                       r"linear probe")
        with self.voiceover(
            f"So, does filling in teach what a digit is? <bookmark mark='a'/> {v} <bookmark mark='b'/> The same "
            "pattern appears at scale: MAE's linear probes trail the contrastive methods, and it shines only once the "
            "whole network is fine-tuned. A pixel target makes the network spend its effort on exact strokes, much "
            "of which a classifier does not need. That suggests a third way: predict, but not pixels."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in tab], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(Indicate(tab[2], color=MAE_C, scale_factor=1.04))
            vo.wait_until("b")
            self.play(FadeIn(lit))
            self.play(FadeIn(tk, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
