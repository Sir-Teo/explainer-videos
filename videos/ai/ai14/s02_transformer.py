from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import (C_COL, DECODER, ENCDEC, ENCODER, MONO, PART, PRIOR, F, arch_diagram, bars_h,
                                   human, load, take_away)


def tower(title, color, rows, n_label=r"$\times 6$", w=3.0):
    """A stack of sub-layer boxes (bottom to top), a frame around them and the repeat count."""
    boxes = VGroup(*[RoundedRectangle(width=w - 0.4, height=0.5, corner_radius=0.08, stroke_color=c, stroke_width=2,
                                      fill_color=c, fill_opacity=0.16) for _, c in rows]).arrange(UP, buff=0.14)
    for b, (t, c) in zip(boxes, rows):
        tx = label(t, font_size=19, color=c)
        if tx.width > w - 0.6:
            tx.width = w - 0.6
        b.add(tx.move_to(b))
    frame = RoundedRectangle(width=w, height=boxes.height + 0.4, corner_radius=0.14, stroke_color=color,
                             stroke_width=2.4).move_to(boxes)
    n = label(n_label, font_size=26, color=color).next_to(frame, RIGHT, buff=0.12)
    t = label(title, font_size=26, color=color).next_to(frame, UP, buff=0.15)
    return VGroup(frame, boxes, n, t)


class Translation(VoiceoverScene):
    def construct(self):
        self.card()
        self.recurrence()
        self.architecture()
        self.results()
        self.cost()
        self.cuts()

    def card(self):
        card = chapter_card(1, r"Attention is all you need", r"What did the 2017 paper actually build?",
                            lit=(2017,), part=PART)
        with self.voiceover("Chapter one. Attention is all you need."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def recurrence(self):
        words = ["the", "cat", "sat", "on", "the", "mat"]
        xs = np.linspace(-4.5, 4.5, len(words))
        cells = VGroup(*[RoundedRectangle(width=0.9, height=0.7, corner_radius=0.1, stroke_color=PRIOR, stroke_width=2,
                                          fill_color=PRIOR, fill_opacity=0.12).move_to([x, 1.9, 0]) for x in xs])
        ws = VGroup(*[data_text(w, font=MONO, font_size=24, color=WHITE).move_to([x, 0.85, 0]) for w, x in zip(words, xs)])
        ups = VGroup(*[Arrow(w.get_top(), c.get_bottom(), buff=0.08, stroke_width=2, color=GREY_C) for w, c in zip(ws, cells)])
        chain = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.05, stroke_width=3, color=PRIOR) for a, b in
                         zip(cells, cells[1:])])
        rl = label(r"a recurrent network: \ state $h_t = f(h_{t-1},\, x_t)$", font_size=28, color=PRIOR).move_to(UP * 3.1)
        seq = label(r"sequential: \ step $t$ waits for step $t - 1$; \ first word to last: $5$ hops", font_size=24,
                    color=GREY_A).move_to(UP * 0.15)
        dots = VGroup(*[Dot([x, -2.55, 0], radius=0.12, color=ENCDEC) for x in xs])
        dl = VGroup(*[data_text(w, font=MONO, font_size=22, color=WHITE).next_to(d, DOWN, buff=0.15) for w, d in zip(words, dots)])
        arcs = VGroup()
        for i in range(len(xs)):
            for j in range(i + 1, len(xs)):
                arcs.add(ArcBetweenPoints(dots[i].get_top(), dots[j].get_top(), angle=-PI / 3.2, color=ENCDEC,
                                          stroke_width=1.6, stroke_opacity=0.7))
        al = label(r"self-attention: \ all positions at once; \ any two words $1$ hop apart", font_size=24,
                   color=ENCDEC).next_to(dl, DOWN, buff=0.2)
        tag = note(r"schematic").to_corner(DR, buff=0.25)
        with self.voiceover(
            "In 2017 the best translation systems were recurrent networks, the sequence-to-sequence models of Part 10, "
            "with attention added on. They read a sentence one word at a time: the state after each word is computed "
            "from the state after the word before. <bookmark mark='a'/> That chain is the problem. Training can't run "
            "the steps of one sentence in parallel, and the last word reaches the first only through every state in "
            "between. <bookmark mark='b'/> The Transformer dropped the recurrence. Every position attends to every "
            "other position directly, all at once: a whole sentence goes through a layer in one parallel step, and "
            "any two words are a single hop apart."
        ) as vo:
            self.play(FadeIn(rl), FadeIn(ws), FadeIn(cells), FadeIn(ups), FadeIn(tag))
            for a in chain:
                self.play(GrowArrow(a), run_time=0.35)
            vo.wait_until("a")
            self.play(FadeIn(seq), LaggedStart(*[Indicate(c, color=YELLOW, scale_factor=1.08) for c in cells],
                                               lag_ratio=0.35), run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(dots), FadeIn(dl))
            self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.04), FadeIn(al), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def architecture(self):
        enc = tower(r"encoder", ENCODER, [(r"self-attention", ENCODER), (r"feed-forward", C.MLP)])
        dec = tower(r"decoder", DECODER, [(r"masked self-attention", DECODER), (r"cross-attention", ENCDEC),
                                          (r"feed-forward", C.MLP)])
        VGroup(enc, dec).arrange(RIGHT, buff=2.2, aligned_edge=DOWN).scale(1.25).move_to([-0.4, 0.4, 0])
        src = data_text("The cat sat on the mat.", font=MONO, font_size=22, color=WHITE).next_to(enc[0], DOWN, buff=0.7)
        tgt = data_text("Die Katze saß auf der Matte.", font=MONO, font_size=22, color=WHITE)
        tgt.next_to(dec[0], DOWN, buff=0.7)
        a1 = Arrow(src.get_top(), enc[0].get_bottom(), buff=0.1, stroke_width=3, color=GREY_B)
        a2 = Arrow(tgt.get_top(), dec[0].get_bottom(), buff=0.1, stroke_width=3, color=GREY_B)
        cross = CurvedArrow(enc[0].get_right() + UP * 0.3, dec[1][1].get_left(), angle=-0.4, color=ENCDEC,
                            stroke_width=3, tip_length=0.18)
        top_r = dec[0].get_corner(UR) + DOWN * 0.35
        out = label(r"next German \\ token", font_size=22, color=DECODER).next_to(top_r, RIGHT, buff=0.7)
        oa = Arrow(top_r, out.get_left(), buff=0.08, stroke_width=3, color=DECODER)
        extras = VGroup(label(r"residual connections, \ layer normalization", font_size=22, color=GREY_A),
                        label(r"positions: \ sine waves of many frequencies", font_size=22, color=C.POSITION))
        extras.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL, buff=0.35)
        tag = note(r"schematic, \ after Vaswani et al.\ (2017), Figure 1").to_corner(DR, buff=0.25)
        with self.voiceover(
            "Here is the model they built. <bookmark mark='a'/> An encoder reads the English sentence: six identical "
            "layers, each with self-attention, where every word looks at every other word, followed by a small "
            "feed-forward network applied to each position on its own. <bookmark mark='b'/> A decoder writes the "
            "German, one token at a time, with six layers of its own. Its self-attention is masked, so a position sees "
            "only the words already written. <bookmark mark='c'/> And a third sub-layer, cross-attention, lets each "
            "position of the output look at the encoded input. <bookmark mark='d'/> Around every sub-layer, a "
            "residual connection and layer normalization; and to tell the model where each word is, sine waves of "
            "many frequencies, added to the inputs. Part 13 took this machine apart. Here we care about what it "
            "became."
        ) as vo:
            self.play(FadeIn(src), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowArrow(a1), FadeIn(enc))
            vo.wait_until("b")
            self.play(FadeIn(tgt), GrowArrow(a2), FadeIn(dec[0]), FadeIn(dec[1][0]), FadeIn(dec[1][2]), FadeIn(dec[2]),
                      FadeIn(dec[3]))
            self.play(GrowArrow(oa), FadeIn(out))
            vo.wait_until("c")
            self.play(FadeIn(dec[1][1]), Create(cross))
            vo.wait_until("d")
            self.play(FadeIn(extras, shift=DOWN * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        T = F.TRANSFORMER
        p = load("published")

        def card(name, cfg, color):
            rows = VGroup(*[VGroup(label(a, font_size=22, color=GREY_A), MathTex(b, font_size=28))
                            for a, b in ((r"layers per stack", str(cfg["N"])), (r"width $d$", str(cfg["d"])),
                                         (r"feed-forward width", str(cfg["d_ff"])),
                                         (r"attention heads", str(cfg["h"])),
                                         (r"parameters", human(cfg["params"]).replace("M", r"\,\text{M}")),
                                         (r"training steps", f"{cfg['steps']:,}".replace(",", "{,}")))])
            for r in rows:
                r[1].move_to([2.6, 0, 0], aligned_edge=RIGHT)
                r[0].move_to([-0.2, 0, 0], aligned_edge=RIGHT)
            rows.arrange(DOWN, buff=0.18)
            for r in rows:
                r[1].align_to(rows, RIGHT)
            head = label(name, font_size=28, color=color)
            inner = VGroup(head, rows).arrange(DOWN, buff=0.25)
            box = RoundedRectangle(width=inner.width + 0.6, height=inner.height + 0.45, corner_radius=0.14,
                                   stroke_color=color, stroke_width=2, fill_color="#0B0F17", fill_opacity=0.95)
            return VGroup(box, inner.move_to(box))

        cards = VGroup(card(r"Transformer, base", T["base"], ENCDEC), card(r"Transformer, big", T["big"], ENCDEC))
        cards.arrange(RIGHT, buff=0.8).move_to(UP * 0.5)
        data = label(rf"WMT 2014: \ ${T['pairs_en_de'] / 1e6:.1f}$ million English--German sentence pairs; \ "
                     rf"${T['sentences_en_fr'] / 1e6:.0f}$ million English--French", font_size=22, color=GREY_A)
        data.next_to(cards, DOWN, buff=0.45)
        # BLEU (English to German) and training cost
        bl = T["bleu"]
        cols = [PRIOR, PRIOR, PRIOR, ENCDEC, ENCDEC]
        bleu = bars_h([(n, b, c) for (n, b, _, _, _), c in zip(bl, cols)], 30, width=4.2, font_size=20,
                      fmt=lambda v: f"{v:g}")
        bleu.move_to([-2.2, -0.2, 0])
        bt = label(r"BLEU, \ English $\to$ German", font_size=26, color=WHITE).next_to(bleu, UP, buff=0.35)
        cost = bars_h([(n, f_, c) for (n, _, _, f_, _), c in zip(bl, cols)], 3e19, width=3.0, font_size=20,
                      log=True, lo=17.5, fmt=lambda v: sci(v, 1))
        for r in cost:
            r.remove(r[0])  # the names are on the BLEU chart's rows
        bleu.to_edge(LEFT, buff=0.35)
        cost.next_to(bleu, RIGHT, buff=0.55).align_to(bleu, UP)
        ct = label(r"training cost, \ operations \ (log scale)", font_size=26, color=C_COL).next_to(cost, UP, buff=0.35)
        ct.align_to(cost, LEFT)
        base_ratio = bl[0][3] / bl[3][3]
        frac_word = ["", "", "half", "third", "quarter", "fifth", "sixth", "seventh", "eighth"][min(8, round(base_ratio))]
        cite_ = cite(r"Vaswani et al.\ (2017), Tables 2--3")
        with self.voiceover(
            "The paper gave two configurations. <bookmark mark='a'/> The base model: six layers in each stack, a width "
            "of 512, eight attention heads, 65 million parameters, trained for a hundred thousand steps, about twelve "
            "hours. The big model doubles the width and the heads: 213 million parameters, three hundred thousand "
            "steps, three and a half days. Both trained on the standard data of the 2014 Workshop on Machine "
            "Translation: four and a half million English–German sentence pairs, and thirty-six million "
            "English–French. <bookmark mark='b'/> On English to German, the big model scored 28.4 BLEU, a measure of "
            "overlap with human translations, more than two points above the best earlier systems, ensembles included. "
            "<bookmark mark='c'/> And it was cheap. The base model alone beat every earlier system, at a training cost "
            f"about a {frac_word} of Google's own recurrent system."
        ) as vo:
            self.play(FadeIn(cite_), LaggedStart(*[FadeIn(c_, shift=UP * 0.15) for c_ in cards], lag_ratio=0.4))
            vo.wait_until("a")
            self.play(Indicate(cards[0], scale_factor=1.03))
            self.play(FadeIn(data))
            vo.wait_until("b")
            self.play(FadeOut(cards), FadeOut(data), FadeIn(bt), run_time=0.8)
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]))
                                                for r in bleu], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(ct), LaggedStart(*[AnimationGroup(GrowFromEdge(r[0], LEFT), FadeIn(r[1]))
                                                for r in cost], lag_ratio=0.3), run_time=2.5)
            self.play(Indicate(cost[3], color=YELLOW))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cost(self):
        T = F.TRANSFORMER
        p = load("published")
        secs = T["big"]["hours"] * 3600
        rows = [
            cmath(r"C", r"=", r"t \times n_{\mathrm{GPU}} \times r", font_size=40),
            cmath(r"t", r"=", rf"{T['big']['hours'] / 24:.1f}\ \text{{days}} = {secs:,}\ \text{{s}}".replace(",", "{,}"),
                  font_size=40),
            cmath(r"C", r"=", rf"{secs:,}\ \text{{s}} \times {T['gpus']} \times {T['tflops']} \times 10^{{12}}\ "
                              r"\text{FLOP/s}".replace(",", "{,}"), font_size=40),
            cmath(r"C", r"\approx", sci(p["tf_big_flops"], 1) + r"\ \text{FLOP}", font_size=40),
        ]
        for r in (rows[0], rows[2], rows[3]):
            r[0].set_color(C_COL)
        whys = [why(r"time $\times$ GPUs $\times$ throughput: \ the paper's method"),
                why(r"$3.5 \times 86{,}400$ s"),
                why(r"P100: \ $9.5$ TFLOP/s sustained, \ as assumed"),
                why(r"Table 2: \ $2.3 \times 10^{19}$ \ \checkmark")]
        step = ladder(self, rows, whys, keep=4, top=2.5, x=-2.2, buff=0.55, edge=6.9)
        res = label(r"the same count, \ from model size and tokens read: \ chapter 6", font_size=26, color=GREY_A)
        res.to_edge(DOWN, buff=0.4)
        gpus = VGroup(*[VGroup(RoundedRectangle(width=0.9, height=0.55, corner_radius=0.08, stroke_color=C.GPU,
                                                stroke_width=2, fill_color=C.GPU, fill_opacity=0.15),
                               label(r"P100", font_size=16, color=C.GPU)) for _ in range(T["gpus"])])
        for g_ in gpus:
            g_[1].move_to(g_[0])
        gpus.arrange(RIGHT, buff=0.15)
        clock = VGroup(Line(LEFT * 2.2, RIGHT * 2.2, color=C.CLOCK, stroke_width=6),
                       label(r"$3.5$ days of training", font_size=20, color=C.CLOCK))
        clock[1].next_to(clock[0], DOWN, buff=0.1)
        pic = VGroup(gpus, clock).arrange(DOWN, buff=0.35).move_to([0, -2.1, 0])
        with self.voiceover(
            "Where does a number like that come from? The paper's recipe is worth seeing, because the field still "
            "counts compute this way. <bookmark mark='a'/> Training time: three and a half days is 302,400 seconds. "
            "<bookmark mark='b'/> Times the number of GPUs, eight, times what one GPU sustains: the authors assumed "
            "9.5 trillion operations a second for the P100. <bookmark mark='c'/> The product is about 2.3 times ten to "
            "the nineteen operations, the figure in their table. <bookmark mark='d'/> In chapter six we'll count the "
            "same thing a second way, from the model's size and the number of tokens it read."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            self.play(Create(clock[0]), FadeIn(clock[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(g_, shift=UP * 0.1) for g_ in gpus], lag_ratio=0.1))
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeOut(pic), FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cuts(self):
        reasons = VGroup(
            label(r"every position at once: \ training uses parallel hardware fully", font_size=26, color=WHITE),
            label(r"any word reaches any other in one step", font_size=26, color=WHITE),
            label(r"almost all matrix multiplication: \ what GPUs do best \ (Part 17)", font_size=26, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 2.1)
        three = VGroup()
        for kind, who, yr in (("encoder", r"encoder only: \ BERT", 2018), ("decoder", r"decoder only: \ GPT", 2018),
                              ("encdec", r"both: \ T5", 2019)):
            col = {"encoder": ENCODER, "decoder": DECODER, "encdec": ENCDEC}[kind]
            d = arch_diagram(kind, 1.0, label_on=kind != "encdec")
            t = label(who, font_size=24, color=col)
            y = label(str(yr), font_size=20, color=GREY_B)
            three.add(VGroup(d, t, y).arrange(DOWN, buff=0.2))
        three.arrange(RIGHT, buff=1.4, aligned_edge=DOWN).move_to(DOWN * 0.9)
        tw = take_away(r"one architecture, \ three ways to cut it: \ which cut won is this part's thread", font_size=26)
        with self.voiceover(
            "Why did it win? Three reasons, and each matters more as we go. Every position is computed at once, so "
            "training uses parallel hardware fully. Any word reaches any other in a single step, so long-range "
            "dependencies are easy to learn. And the work is almost all matrix multiplication, which is exactly what "
            "graphics cards are built for, the subject of Part 17. <bookmark mark='a'/> The encoder–decoder was built "
            "for translation. Within eighteen months the field had cut it three ways: keep only the encoder, as BERT "
            "did; keep only the decoder, as GPT did; or keep both, as T5 did. <bookmark mark='b'/> Which cut won, and "
            "why, is the thread of this part."
        ) as vo:
            ghost = three.copy().set_opacity(0.15)
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in reasons], lag_ratio=0.5), FadeIn(ghost),
                      run_time=3.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in three], lag_ratio=0.4), FadeOut(ghost), run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(tw))
        self.wait(0.3)
        self.clear_scene()
