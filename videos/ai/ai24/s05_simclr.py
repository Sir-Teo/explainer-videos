from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai24.common import (Scrub, MOCO, NEG, PANEL, PART, POS, SIMCLR, TARGET, arrow, axes, bars_chart, digit,
                                   digit_sheet, ink_rgb, load, node_box, pct, rgb_of, seed_curves, tag, take_away,
                                   to_image)

MAIN = "0.2"


def nn_sheet(pool, pool_y, queries, nn, size=0.5, gap=0.06):
    """Each query (white) and its neighbours, green when they are the same digit, red when not."""
    imgs, cols = [], []
    for qi, row in zip(queries, nn):
        imgs.append(pool[qi])
        cols.append(None)
        for j in row:
            imgs.append(pool[j])
            cols.append(POS if pool_y[j] == pool_y[qi] else NEG)
    return digit_sheet(np.asarray(imgs), len(queries), 1 + nn.shape[1], size=size, gap=gap, colors=cols)


class SimCLR(VoiceoverScene):
    def construct(self):
        self.card()
        self.views()
        self.pipeline()
        self.replay()
        self.head()
        self.moco()

    def card(self):
        card = chapter_card(4, r"Two views of one digit", r"SimCLR and MoCo: \ what is a positive pair?",
                            lit=(1993,), part=PART)
        with self.voiceover("Chapter four. Two views of one digit."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def views(self):
        v = load("views")
        orig, full = np.asarray(v["orig"]), np.asarray(v["full"])
        rows = Group()
        for c in (3, 5, 8):
            o = digit(orig[c], 0.9, frame=True)
            vs = digit_sheet(full[:6, c], 1, 6, size=0.9, gap=0.08, color=SIMCLR)
            rows.add(Group(o, MathTex(r"\to", font_size=34, color=GREY_B), vs).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, buff=0.35).move_to([-1.0, -0.2, 0])
        ops = VGroup(*[label(t, font_size=21, color=GREY_A) for t in
                       (r"crop and zoom", r"tilt and shear", r"contrast", r"blur", r"erase a patch", r"noise")])
        ops.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([5.6, -0.2, 0])
        head = label(r"Views: \ the same digit, \ changed in ways that keep it the same digit", font_size=30)
        head.to_edge(UP, buff=0.4)
        pair = SurroundingRectangle(rows[1][2][1][:1], color=POS, buff=0.06)
        pos_l = label(r"two views of one digit: \ a \textbf{positive pair}", font_size=24, color=POS)
        pos_l.to_edge(DOWN, buff=0.75)
        neg_l = label(r"every other view in the batch: \ a \textbf{negative}", font_size=24, color=NEG)
        neg_l.next_to(pos_l, DOWN, buff=0.15)
        with self.voiceover(
            "Contrastive learning for pictures needs a partner for each picture, and the partner is made, not "
            "found. <bookmark mark='a'/> Take a digit and change it at random: crop and zoom, tilt, change the "
            "contrast, blur it, erase a patch, add noise. <bookmark mark='b'/> Each version is still the same "
            "digit. Two versions of one digit make a positive pair; <bookmark mark='c'/> every version of every "
            "other digit in the batch is a negative. These choices are the only knowledge we give the network: "
            "they say what should not matter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0][0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(o, shift=LEFT * 0.1) for o in ops], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(pos_l))
            vo.wait_until("c")
            self.play(FadeIn(neg_l))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pipeline(self):
        v = load("views")
        full = np.asarray(v["full"])
        a = digit(full[0, 5], 0.9, frame=True).move_to([-5.8, 1.1, 0])
        b = digit(full[1, 5], 0.9, frame=True).move_to([-5.8, -1.1, 0])
        fa = node_box(r"$f$", SIMCLR, font_size=30, height=0.8).move_to([-3.9, 1.1, 0])
        fb = node_box(r"$f$", SIMCLR, font_size=30, height=0.8).move_to([-3.9, -1.1, 0])
        shared = label(r"the same network", font_size=18, color=GREY_B).move_to([-3.9, 0, 0])
        ha = MathTex(r"h", font_size=34, color=SIMCLR).move_to([-2.5, 1.1, 0])
        hb = MathTex(r"h'", font_size=34, color=SIMCLR).move_to([-2.5, -1.1, 0])
        ga = node_box(r"$g$", GREY_B, font_size=28, height=0.7).move_to([-1.2, 1.1, 0])
        gb = node_box(r"$g$", GREY_B, font_size=28, height=0.7).move_to([-1.2, -1.1, 0])
        za = MathTex(r"z", font_size=34, color=POS).move_to([0.1, 1.1, 0])
        zb = MathTex(r"z'", font_size=34, color=POS).move_to([0.1, -1.1, 0])
        arrs = VGroup(arrow(a.get_right(), fa.get_left()), arrow(b.get_right(), fb.get_left()),
                      arrow(fa.get_right(), ha.get_left()), arrow(fb.get_right(), hb.get_left()),
                      arrow(ha.get_right(), ga.get_left()), arrow(hb.get_right(), gb.get_left()),
                      arrow(ga.get_right(), za.get_left()), arrow(gb.get_right(), zb.get_left()))
        keep = label(r"kept: \ $h$, \ the representation", font_size=20, color=SIMCLR).next_to(ha, UP, buff=0.5)
        drop = label(r"thrown away after training: \ the head $g$", font_size=20, color=GREY_B).next_to(gb, DOWN,
                                                                                                    buff=0.4)
        f = MathTex(r"\ell_i", r"=", r"-\log", r"\frac{e^{\cos(z_i, z_{i'})/\tau}}{\sum_{k \ne i} e^{\cos(z_i, z_k)/\tau}}",
                    font_size=38).move_to([3.9, 0.9, 0])
        f[3].set_color(POS)
        n1 = label(r"each of $2 \times 128$ views \\ picks its partner \\ out of the other $255$", font_size=24,
                   color=GREY_A).next_to(f, DOWN, buff=0.4)
        n2 = label(r"InfoNCE, \ with $\cos$ for $f$ \\ and a temperature $\tau$", font_size=22,
                   color=C.BITS).next_to(n1, DOWN, buff=0.3)
        src = cite(r"Chen, Kornblith, Norouzi \& Hinton (2020): \ SimCLR")
        with self.voiceover(
            "In 2020 Ting Chen, Simon Kornblith, Mohammad Norouzi and Geoffrey Hinton put the pieces together in "
            "SimCLR. Two views of a digit go through the same network f, <bookmark mark='a'/> giving two "
            "representations, h. <bookmark mark='b'/> A small head, g, maps each to a vector z on the unit sphere. "
            "<bookmark mark='c'/> The loss is InfoNCE with the cosine as the score: in a batch of a hundred and "
            "twenty-eight digits, each of the two hundred and fifty-six views must pick out its partner from the "
            "other two hundred and fifty-five, at a temperature tau. <bookmark mark='d'/> After training, the head "
            "is thrown away and h is kept."
        ) as vo:
            self.play(FadeIn(a), FadeIn(b), FadeIn(fa), FadeIn(fb), FadeIn(shared), GrowArrow(arrs[0]),
                      GrowArrow(arrs[1]), FadeIn(src))
            vo.wait_until("a")
            self.play(GrowArrow(arrs[2]), GrowArrow(arrs[3]), FadeIn(ha), FadeIn(hb))
            vo.wait_until("b")
            self.play(FadeIn(ga), FadeIn(gb), *[GrowArrow(x) for x in arrs[4:]], FadeIn(za), FadeIn(zb))
            vo.wait_until("c")
            self.play(Write(f), FadeIn(n1))
            self.play(FadeIn(n2))
            vo.wait_until("d")
            self.play(FadeIn(keep), FadeIn(drop), Indicate(ha, color=SIMCLR))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        s = load("simclr")
        pool, pool_y = np.asarray(s["pool"]), np.asarray(s["pool_y"])
        Q = list(s["queries"])
        NN = np.asarray(s["rec_nn"])
        steps = np.asarray(s["rec_steps"])
        n_s = len(steps)
        same = [float(np.mean([pool_y[j] == pool_y[q] for q, row in zip(Q, NN[i]) for j in row])) for i in range(n_s)]
        tr = ValueTracker(0)

        sh = Scrub([nn_sheet(pool, pool_y, Q, NN[i], size=0.52).move_to([-3.0, -0.3, 0]) for i in range(n_s)], tr)
        ql = label(r"query", font_size=20, color=GREY_A).move_to([-3.0 - 4 * 0.58, 1.8, 0])
        nl = label(r"its $8$ nearest test digits, \ by $h$", font_size=20, color=GREY_A).move_to([-2.4, 1.8, 0])
        stl = always_redraw(lambda: label(rf"step ${steps[int(np.clip(round(tr.get_value()), 0, n_s - 1))]}$", font_size=24,
                                          color=GREY_A).move_to([-3.0, 2.4, 0]))
        runs, keys = s["runs"], s["keys"][MAIN]
        ax = axes([0, steps[-1]], [0.7, 1.0], x_length=4.4, y_length=3.0, xlabel=r"training step",
                  ylabel=r"$k$-NN accuracy (quick test)", xticks=[0, steps[-1]], yticks=[0.7, 0.8, 0.9, 1.0],
                  center=[4.0, -0.3, 0])
        cs = seed_curves(ax.ax, runs, keys, "knn", SIMCLR)
        sf = always_redraw(lambda: label(
            rf"same digit: \ ${pct(same[int(np.clip(round(tr.get_value()), 0, n_s - 1))], 0)}\%$ of neighbours",
            font_size=24, color=POS).next_to(ax, DOWN, buff=0.35))
        tg = tag(r"computed: \ SimCLR, $\tau = 0.2$, \ three seeds, \ the first replayed")
        fin = s["summary"][MAIN]
        with self.voiceover(
            "Here is our SimCLR learning. Six test digits, and next to each, the eight test digits whose vectors "
            "are nearest to it, green when they are the same digit, red when they are not. <bookmark mark='a'/> At "
            f"the start the network is random, and only {pct(same[0], 0)} percent of the neighbours match. "
            f"<bookmark mark='b'/> As training goes on, the neighbourhoods fill with the right digits: "
            f"{pct(same[-1], 0)} percent by the end. <bookmark mark='c'/> On the full test, a linear probe on its "
            f"vectors reads the digit correctly {pct(fin['linear'][0])} percent of the time, the mean of three "
            "runs, and the nearest-neighbour vote "
            f"{pct(fin['knn'][0])} percent."
        ) as vo:
            self.play(FadeIn(sh), FadeIn(ql), FadeIn(nl), FadeIn(stl), FadeIn(ax), FadeIn(tg))
            vo.wait_until("a")
            self.play(FadeIn(sf))
            vo.wait_until("b")
            self.play(tr.animate.set_value(n_s - 1), Create(cs), run_time=max(3.0, vo.until("c") - 0.2),
                      rate_func=linear)
            vo.wait_until("c")
            self.play(Indicate(cs[0], color=SIMCLR))
        for m in (sh, stl, sf):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def head(self):
        s = load("simclr")
        runs, keys = s["runs"], s["keys"][MAIN]
        hl = np.mean([runs[k]["final"]["linear"] for k in keys])
        zl = np.mean([runs[k]["extra"]["zlinear"] for k in keys])
        hk = np.mean([runs[k]["final"]["knn"] for k in keys])
        zk = np.mean([runs[k]["extra"]["zknn"] for k in keys])
        lo = min(hl, zl, hk, zk)
        ch = bars_chart([hl, zl, hk, zk], [SIMCLR, GREY_B, SIMCLR, GREY_B],
                        [r"$h$, linear", r"$z$, linear", r"$h$, $k$-NN", r"$z$, $k$-NN"], height=3.2, bar_w=0.9,
                        gap=0.6, vmin=max(0.0, np.floor((lo - 0.03) * 50) / 50), vmax=1.0, digits=1,
                        value_fmt=lambda x: pct(x) + r"\%", font_size=24)
        ch.move_to([-2.6, -0.4, 0])
        ax_note = label(rf"axis from ${pct(max(0.0, np.floor((lo - 0.03) * 50) / 50), 0)}\%$", font_size=18,
                        color=GREY_B).next_to(ch, DOWN, buff=0.15)
        better = hl > zl
        lit = label(r"Chen et al.\ (2020): \ the layer before the head \\ beat the layer after by over $10\%$ \\ on "
                    r"ImageNet", font_size=22, color=GREY_A).move_to([3.8, 1.2, 0])
        why_ = label(r"the head learns to forget \\ whatever the views disagree on: \\ rotation, contrast, \ size",
                     font_size=22, color=GREY_B).next_to(lit, DOWN, buff=0.5)
        res = label(r"ImageNet, \ ResNet-50 $(4\times)$: \ $76.5\%$ linear probe, \\ matching a supervised ResNet-50",
                    font_size=22, color=SIMCLR).next_to(why_, DOWN, buff=0.5)
        verdict = (f"Ours agrees: reading the digits from h gives {pct(hl)} percent, from z only {pct(zl)}."
                   if better else
                   f"On our digits the difference is small: {pct(hl)} percent from h, {pct(zl)} from z.")
        with self.voiceover(
            "Why throw the head away? Because the loss asks z to ignore everything the two views disagree on: the "
            "tilt, the size, the contrast. <bookmark mark='a'/> The head pays that price, and h, one layer below, "
            f"keeps more. <bookmark mark='b'/> {verdict} <bookmark mark='c'/> SimCLR's authors found the same on "
            "ImageNet, by more than ten points, and with a wide network and very large batches, their linear probe "
            "reached 76.5 percent, as good as the same network trained with every label."
        ) as vo:
            self.play(FadeIn(ch.bars[:1]), FadeIn(ch.bars[1:]), FadeIn(ch[0]), FadeIn(ch.names), FadeIn(ax_note))
            vo.wait_until("a")
            self.play(FadeIn(why_))
            vo.wait_until("b")
            self.play(FadeIn(ch.vals), FadeIn(ch.whiskers))
            vo.wait_until("c")
            self.play(FadeIn(lit), FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def moco(self):
        s = load("simclr")
        mo = load("moco")
        q = node_box(r"query encoder", MOCO, font_size=22).move_to([-4.6, 1.2, 0])
        k = node_box(r"momentum encoder", TARGET, font_size=22).move_to([-4.6, -0.6, 0])
        ema = label(r"$\theta_k \leftarrow m\,\theta_k + (1 - m)\,\theta_q$", font_size=24, color=TARGET)
        ema.next_to(k, DOWN, buff=0.25)
        queue = VGroup(*[Rectangle(width=0.22, height=0.5, stroke_width=1, stroke_color=NEG, fill_color=NEG,
                                   fill_opacity=0.15 + 0.6 * i / 14) for i in range(14)]).arrange(RIGHT, buff=0.04)
        queue.move_to([-1.0, -0.6, 0])
        ql = label(r"a queue of past keys: \ the negatives", font_size=20, color=NEG).next_to(queue, DOWN, buff=0.2)
        a1 = arrow(k.get_right(), queue.get_left(), color=TARGET)
        src = cite(r"He, Fan, Wu, Xie \& Girshick (2020): \ MoCo; \ the paper: $65{,}536$ keys, $m = 0.999$")
        runs_s, keys_s = s["runs"], s["keys"][MAIN]
        runs_m, keys_m = mo["runs"], mo["keys"]
        ax = axes([0, runs_s[keys_s[0]]["steps"][-1]], [0.7, 1.0], x_length=4.6, y_length=2.8,
                  xlabel=r"training step", ylabel=r"$k$-NN (quick test)", yticks=[0.7, 0.8, 0.9, 1.0],
                  center=[3.8, 0.6, 0])
        c1 = seed_curves(ax.ax, runs_s, keys_s, "knn", SIMCLR)
        c2 = seed_curves(ax.ax, runs_m, keys_m, "knn", MOCO)
        leg = VGroup(label(r"SimCLR: \ 254 negatives from the batch", font_size=18, color=SIMCLR),
                     label(r"MoCo: \ 4{,}096 from the queue", font_size=18, color=MOCO)).arrange(DOWN,
                                                                                               aligned_edge=LEFT,
                                                                                               buff=0.08)
        leg.next_to(ax, DOWN, buff=0.15)
        sl, ml = s["summary"][MAIN]["linear"], mo["summary"]["linear"]
        sk, mk = s["summary"][MAIN]["knn"], mo["summary"]["knn"]
        crop = s["summary"]["crop"]
        diff = ml[0] - sl[0]
        if diff > 0.002:
            mo_line = (f"On our digits, MoCo's linear probe reaches {pct(ml[0])} percent against SimCLR's "
                       f"{pct(sl[0])}: the queue's extra negatives help a little.")
        elif diff > -0.002:
            mo_line = (f"On our digits, MoCo's linear probe reaches {pct(ml[0])} percent against SimCLR's "
                       f"{pct(sl[0])}: about the same; with only ten kinds of digit, a few hundred negatives are "
                       "already plenty.")
        else:
            mo_line = (f"On our digits, MoCo's linear probe reaches {pct(ml[0])} percent against SimCLR's "
                       f"{pct(sl[0])}: slightly behind; with ten kinds of digit, more negatives buy nothing.")
        crop_line = (f"And the views matter more than either: with crops alone, and no changes of contrast, blur, "
                     f"erasing or noise, SimCLR's probe falls to {pct(crop['linear'][0])} percent."
                     if crop["linear"][0] < sl[0] - 0.003 else
                     f"With crops alone, SimCLR's probe is {pct(crop['linear'][0])} percent: on clean black-and-white "
                     "digits, the other changes add little.")
        tk = take_away(r"the views decide what the network may ignore; \ the negatives keep it from ignoring "
                       r"everything")
        with self.voiceover(
            "SimCLR needs its negatives in the batch, so it needs huge batches: the paper went to eight thousand "
            "images. Months earlier, Kaiming He and his colleagues had found another way, MoCo. <bookmark "
            "mark='a'/> Keep the keys of past batches in a queue and use them as negatives. <bookmark mark='b'/> "
            "To keep old keys comparable with new ones, compute them with a second encoder that is a slowly moving "
            "average of the first. <bookmark mark='c'/> We trained MoCo with a queue of four thousand and "
            f"ninety-six keys. {mo_line} <bookmark mark='d'/> {crop_line}"
        ) as vo:
            self.play(FadeIn(q), FadeIn(k), FadeIn(src))
            vo.wait_until("a")
            self.play(GrowArrow(a1), LaggedStart(*[FadeIn(r) for r in queue], lag_ratio=0.05), FadeIn(ql))
            vo.wait_until("b")
            self.play(FadeIn(ema))
            vo.wait_until("c")
            self.play(FadeIn(ax), Create(c1), Create(c2), FadeIn(leg), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(tk, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
