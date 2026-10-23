from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai24.common import (DINO_C, PART, PIX, POS, SIMCLR, SUP, arrow, bars_chart, load, node_box, pct, tag,
                                   take_away, take_away_in)

RAW = "#FF9F45"
CUR = "#5BD17A"


class Scale(VoiceoverScene):
    def construct(self):
        self.card()
        self.dinov2()
        self.pools()
        self.result()
        self.dinov3()
        self.webssl()

    def card(self):
        card = chapter_card(10, r"Scale and curation", r"DINOv2, \ DINOv3, \ and does vision need language?", lit=(2008,),
                            part=PART)
        with self.voiceover("Chapter ten. Scale and curation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def dinov2(self):
        pool = node_box(r"$1.2$ billion web images \\ (uncurated, \ deduplicated)", PIX, font_size=22, height=1.2)
        seeds = node_box(r"curated datasets \\ (ImageNet and others)", SUP, font_size=22, height=1.2)
        ret = node_box(r"embed everything with a \\ self-supervised ViT-H; \\ each seed image retrieves \\ its 4 "
                       r"nearest neighbours", DINO_C, font_size=20, height=1.8)
        out = node_box(r"LVD-142M: \\ $142$ million images", POS, font_size=22, height=1.2)
        VGroup(seeds, pool).arrange(DOWN, buff=0.6).move_to([-4.8, 0.2, 0])
        ret.move_to([-0.8, 0.2, 0])
        out.move_to([3.0, 0.2, 0])
        arrs = VGroup(arrow(pool.get_right(), ret.get_left() + DOWN * 0.3), arrow(seeds.get_right(), ret.get_left() + UP * 0.3),
                      arrow(ret.get_right(), out.get_left()))
        model = label(r"ViT-g: \ $1.1$B parameters; \ DINO + a masked-token loss (iBOT) \\ + spreading (KoLeo) + "
                      r"Sinkhorn centring \\ ImageNet: \ $86.5\%$ linear probe", font_size=22, color=GREY_A)
        model.to_edge(DOWN, buff=0.5)
        src = cite(r"Oquab et al.\ (2023): \ DINOv2", corner=UR)
        with self.voiceover(
            "To scale self-distillation, Meta's DINOv2 team in 2023 found that the data mattered as much as the "
            "model. Raw web images are dominated by a few kinds of picture, duplicated many times. <bookmark "
            "mark='a'/> So they built a dataset by retrieval. Start from curated datasets such as ImageNet; <bookmark "
            "mark='b'/> embed one point two billion deduplicated web images with a self-supervised network; let each "
            "curated image fetch its four nearest neighbours from the pool. <bookmark mark='c'/> The result, a "
            "hundred and forty-two million images, trained a vision transformer of 1.1 billion parameters, "
            "<bookmark mark='d'/> with DINO's loss plus a masked-token term and a term that spreads the vectors: "
            "86.5 percent on ImageNet with a linear probe, never having seen a label."
        ) as vo:
            self.play(FadeIn(pool), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(seeds))
            vo.wait_until("b")
            self.play(GrowArrow(arrs[0]), GrowArrow(arrs[1]), FadeIn(ret))
            vo.wait_until("c")
            self.play(GrowArrow(arrs[2]), FadeIn(out))
            vo.wait_until("d")
            self.play(FadeIn(model))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pools(self):
        c = load("curation")
        pc, cc = np.asarray(c["pool_counts"], float), np.asarray(c["curated_counts"], float)
        names = [str(i) for i in range(10)]
        top = max(pc.max(), cc.max()) * 1.1
        b1 = bars_chart(pc, [RAW] * 10, names, height=2.6, bar_w=0.38, gap=0.18, vmax=top, digits=0, font_size=16)
        b2 = bars_chart(cc, [CUR] * 10, names, height=2.6, bar_w=0.38, gap=0.18, vmax=top, digits=0, font_size=16)
        b1.move_to([-3.5, -0.6, 0])
        b2.move_to([3.5, -0.6, 0])
        t1 = label(rf"the raw pool: \ ${int(pc.sum()):,}$ digits".replace(",", "{,}"), font_size=24, color=RAW).next_to(
            b1, UP, buff=0.35)
        t2 = label(rf"curated by retrieval: \ ${int(cc.sum()):,}$".replace(",", "{,}"), font_size=24,
                   color=CUR).next_to(b2, UP, buff=0.35)
        xl = label(r"digits of each class \ (labels used only to count)", font_size=20, color=GREY_B).to_edge(DOWN,
                                                                                                         buff=0.3)
        head = label(r"Our version: \ an unbalanced pool, \ curated the DINOv2 way", font_size=30).to_edge(UP, buff=0.4)
        rare = [int(i) for i in np.argsort(pc)[:3]]
        common = int(np.argmax(pc))
        ratio_raw = pc.max() / max(pc.min(), 1)
        ratio_cur = cc.max() / max(cc.min(), 1)
        with self.voiceover(
            f"We can try the same recipe on digits. Take {int(pc.sum()):,} training digits, unbalanced the way web "
            f"images are: the commonest digit, {common}, is {pct(pc[common] / pc.sum(), 0)} percent of the pool, the "
            f"rarest only {pct(pc.min() / pc.sum(), 1)} percent. <bookmark mark='a'/> Then curate it: a small "
            "balanced set of a thousand digits, a hundred of each, plays the curated datasets. Each fetches its four "
            "nearest neighbours from the pool, using our SimCLR network as the embedding, and duplicates are "
            f"dropped. <bookmark mark='b'/> The curated pool has {int(cc.sum()):,} digits, and the gap between the "
            f"commonest and the rarest class shrinks from {ratio_raw:.0f} to one to {ratio_cur:.1f} to one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(t1), FadeIn(b1[0]), FadeIn(b1.names), FadeIn(xl))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in b1.bars], lag_ratio=0.08), FadeIn(b1.vals))
            vo.wait_until("a")
            self.play(Indicate(VGroup(*[b1.bars[i] for i in rare]), color=RAW))
            vo.wait_until("b")
            self.play(FadeIn(t2), FadeIn(b2[0]), FadeIn(b2.names),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in b2.bars], lag_ratio=0.08), FadeIn(b2.vals))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def result(self):
        c = load("curation")
        runs, K = c["runs"], c["keys"]
        pc = np.asarray(c["pool_counts"], float)
        per_r = np.mean([runs[k]["extra"]["knn_by_digit"] for k in K["raw"]], 0)
        per_c = np.mean([runs[k]["extra"]["knn_by_digit"] for k in K["curated"]], 0)
        order = np.argsort(-pc)
        lo = float(np.floor((min(per_r.min(), per_c.min()) - 0.02) * 50) / 50)
        bars = VGroup()
        H = 3.2
        for j, cl in enumerate(order):
            x = -5.4 + j * 1.15
            for dx, v, col in ((-0.2, per_r[cl], RAW), (0.2, per_c[cl], CUR)):
                h = max(H * (v - lo) / (1 - lo), 0.01)
                bars.add(Rectangle(width=0.36, height=h, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                    [x + dx, -2.0 + h / 2, 0]))
            bars.add(MathTex(str(int(cl)), font_size=26, color=GREY_A).move_to([x, -2.35, 0]))
        axis = Line([-6.0, -2.0, 0], [6.0, -2.0, 0], color=GREY_C, stroke_width=1.5)
        yl = label(rf"$k$-NN accuracy on each test digit \ (axis from ${pct(lo, 0)}\%$), \ commonest in the raw pool "
                   r"first", font_size=20, color=GREY_A).next_to(axis, UP, buff=3.5)
        leg = VGroup(label(r"trained on the raw pool", font_size=20, color=RAW),
                     label(r"trained on the curated pool", font_size=20, color=CUR)).arrange(RIGHT, buff=0.6)
        leg.next_to(yl, UP, buff=0.15)
        S = c["summary"]
        rare = order[-3:]
        gain_rare = float(np.mean(per_c[rare] - per_r[rare]))
        gain_common = float(np.mean(per_c[order[:3]] - per_r[order[:3]]))
        lr, lc = S["raw"]["linear"][0], S["curated"]["linear"][0]
        fr, fc = S["raw"]["few"][0], S["curated"]["few"][0]
        n_r, n_c = int(pc.sum()), int(np.asarray(c["curated_counts"]).sum())
        rarest = int(order[-1])
        g1 = float(per_c[rarest] - per_r[rarest])
        near = float(max(abs(per_c[o] - per_r[o]) for o in order[:3]))
        if g1 > 0.01:
            v = (f"The biggest change is on the rarest digit, {rarest}, with only {int(pc[rarest])} examples in the raw "
                 f"pool: {pct(per_r[rarest])} percent of its test digits right before curation, {pct(per_c[rarest])} "
                 f"after. On the three commonest, the two networks are within {pct(near)} points. Overall: linear "
                 f"probe {pct(lc)} against {pct(lr)} percent, ten labels per digit {pct(fc)} against {pct(fr)}, from a "
                 f"pool {n_r / n_c:.0f} times smaller.")
        elif gain_rare > 0.005:
            v = (f"On the three rarest digits, the curated pool's network is better by {pct(gain_rare)} points; on "
                 f"the three commonest, the difference is {pct(gain_common)}. Overall: linear probe {pct(lc)} against "
                 f"{pct(lr)} percent, ten labels per digit {pct(fc)} against {pct(fr)}, from a pool "
                 f"{n_r / n_c:.0f} times smaller.")
        else:
            v = (f"On the three rarest digits the curated pool's network is not better: a difference of "
                 f"{pct(gain_rare)} points. Overall: linear probe {pct(lc)} against {pct(lr)} percent, from a pool "
                 f"{n_r / n_c:.0f} times smaller. With only ten kinds of digit, even the rare ones are seen often "
                 "enough.")
        tg = tag(r"computed: \ the same SimCLR, \ same steps, \ two seeds each")
        with self.voiceover(
            "Then train the same SimCLR, for the same number of steps, on each pool, and test on the usual balanced "
            "test set. <bookmark mark='a'/> Here is the accuracy on each digit, the commonest in the raw pool on the "
            f"left. <bookmark mark='b'/> {v}"
        ) as vo:
            self.play(Create(axis), FadeIn(yl), FadeIn(leg), FadeIn(tg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.02), run_time=2.0)
            vo.wait_until("b")
            self.play(*[Indicate(m) for m in bars[-9:]])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dinov3(self):
        facts = VGroup(
            label(r"ViT-7B: \ $6.7$ billion parameters", font_size=24),
            label(r"LVD-1689M: \ $1.7$ billion images, \ chosen from about $17$ billion", font_size=24),
            label(r"curation: \ clustering (5 levels of $k$-means), \ balanced sampling, \ retrieval", font_size=24),
            label(r"ImageNet linear probe: \ $88.4\%$ \ (DINOv2-g $87.3$, \ SigLIP 2-g $89.1$, \ PE-core-G $89.3$)",
                  font_size=24),
            label(r"segmentation (ADE20k) with a linear head: \ $55.9$ mIoU", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-1.6, 0.6, 0])
        g = MathTex(r"\mathcal L_{\rm Gram}", r"=", r"\big\| X_S X_S^\top - X_G X_G^\top \big\|_F^2", font_size=36)
        g.to_edge(DOWN, buff=1.2)
        g[2].set_color(DINO_C)
        gl = label(r"Gram anchoring: \ the student's patch-to-patch similarities \\ held to those of an earlier "
                   r"checkpoint", font_size=22, color=GREY_A).next_to(g, DOWN, buff=0.15)
        src = cite(r"Sim\'eoni et al.\ (2025): \ DINOv3", corner=UR)
        with self.voiceover(
            "In August 2025 came DINOv3: a seven-billion-parameter transformer, trained on one point seven billion "
            "images chosen from about seventeen billion, <bookmark mark='a'/> by clustering them at five levels and "
            "sampling evenly from the clusters, plus retrieval. <bookmark mark='b'/> Its linear probe on ImageNet "
            "reaches 88.4 percent, within a point of the best models trained with captions. <bookmark mark='c'/> "
            "Its new ingredient addresses a problem of long training: the features of individual patches, which "
            "segmentation needs, got worse as the global features improved. Gram anchoring holds the student's "
            "patch-to-patch similarities to those of an earlier checkpoint."
        ) as vo:
            self.play(FadeIn(facts[:2]), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(facts[2]))
            vo.wait_until("b")
            self.play(FadeIn(facts[3]))
            vo.wait_until("c")
            self.play(FadeIn(facts[4]), Write(g), FadeIn(gl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def webssl(self):
        head = label(r"Does vision need language? \ Same 2 billion images, \ two ways to train", font_size=30)
        head.to_edge(UP, buff=0.4)
        ch = bars_chart([53.87, 52.97], [DINO_C, SIMCLR], [r"Web-DINO 7B \\ (images only)",
                                                        r"MetaCLIP 7B \\ (images + captions)"],
                        height=2.8, bar_w=1.4, gap=1.2, vmin=50, vmax=55, digits=2, font_size=26)
        ch.move_to([-3.0, -0.1, 0])
        cap = label(r"average over 16 visual question-answering tasks", font_size=20, color=GREY_A).next_to(ch, DOWN,
                                                                                                        buff=0.5)
        pts = VGroup(
            label(r"self-supervised learning kept improving \\ up to 7 billion parameters, \\ and scaled better "
                  r"than CLIP", font_size=22),
            label(r"keep only the $1.3\%$ of images with text in them: \\ OCR and chart questions $+4.3$ points over "
                  r"CLIP-2B", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([3.4, -0.3, 0])
        src = cite(r"Fan, Tong, Zhu et al.\ (2025): \ Web-SSL")
        tk = take_away(r"at scale, \ curated pictures alone teach a network to see \ about as well as pictures "
                       r"with captions")
        with self.voiceover(
            "Is language necessary? Vision models trained with captions, like CLIP from Part 23, had been ahead on "
            "visual question answering, but they had also been trained on different data. <bookmark mark='a'/> In "
            "2025 David Fan, Saining Xie and colleagues trained both on the same two billion images. At seven "
            "billion parameters, the DINO-style model, which never saw a caption, averaged 53.87 across sixteen "
            "question-answering tasks; the CLIP model, 52.97. <bookmark mark='b'/> The self-supervised models kept "
            "improving with size. <bookmark mark='c'/> And for questions about text and charts, the data mattered "
            "again: keeping only the images that contain text beat a caption-trained model."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(ch), FadeIn(cap))
            vo.wait_until("b")
            self.play(FadeIn(pts[0]))
            vo.wait_until("c")
            self.play(FadeIn(pts[1]))
            self.play(*take_away_in(self, tk))
        self.wait(0.3)
        self.clear_scene()
