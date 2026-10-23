from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import (A, DIFFC, GATEC, MONO, PANEL, PART, POS, SINK_COLORS, SINK_NAMES, SINKC, V,
                                   curve, framed, heat_image, load, seed_lines)

VARIANTS = ("softmax", "sink", "gate", "diff")
SPOKEN_SINK = {"softmax": "the plain softmax", "sink": "the sink logit", "gate": "the gated head",
               "diff": "differential attention"}


def show_char(c):
    return {" ": "\u2423", "\n": "\u21b5"}.get(c, c)


class Sinks(VoiceoverScene):
    def construct(self):
        self.card()
        self.ours()
        self.why()
        self.task()
        self.ways()

    def card(self):
        card = chapter_card(12, r"Attention sinks, and three ways out", r"Where does a head look when it has nothing "
                            r"to look for?", part=PART)
        with self.voiceover("Chapter twelve. Attention sinks, and three ways out."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def ours(self):
        t = load("tf")
        sink = np.asarray(t["sink"])  # layer, head: mean weight on position 0 (queries 64-255)
        uni = float(t["sink_uniform"])
        L, H = sink.shape
        sp, sps = np.asarray(t["space_att"]), float(t["space_share"])
        ratio = float(sink.max() / uni)
        strong = ratio > 5
        bw = 0.34
        sy = 2.2 / max(uni * 2, float(sink.max()))
        x0, y0 = -6.2, -1.9
        bars = VGroup()
        for l_ in range(L):
            for h in range(H):
                v = float(sink[l_, h])
                bars.add(Rectangle(width=bw * 0.8, height=max(sy * v, 0.01), stroke_width=0,
                                   fill_color=POS if v > 5 * uni else A, fill_opacity=0.85)
                         .move_to([x0 + (l_ * (H + 1) + h) * bw, y0 + sy * v / 2, 0]))
        right = x0 + (L * (H + 1)) * bw
        base = Line([x0 - 0.2, y0, 0], [right, y0, 0], color=GREY_C, stroke_width=2)
        ul = DashedLine([x0 - 0.2, y0 + sy * uni, 0], [right, y0 + sy * uni, 0], color=GREY_B, stroke_width=1.5)
        ulab = label(r"an even share", font_size=18, color=GREY_B).next_to(ul, UP, buff=0.05).align_to(base, RIGHT)
        lyr = VGroup(*[label(rf"layer {l_ + 1}", font_size=18, color=GREY_B)
                       .move_to([x0 + (l_ * (H + 1) + (H - 1) / 2) * bw, y0 - 0.3, 0]) for l_ in range(L)])
        bl = label(r"our transformer: \ each head's attention on the first character", font_size=22, color=GREY_A)
        bl.next_to(VGroup(base, bars), UP, buff=0.35).align_to(base, LEFT)
        bl.set_y(y0 + 2.75)
        # space and line breaks: the natural landing spots in text
        hi_sp = float(sp.max())
        spl = label(rf"the most space-loving head: \ ${hi_sp:.0%}$ of its attention on spaces and line breaks, \\ "
                    rf"which are ${sps:.0%}$ of the text".replace("%", r"\%"), font_size=20, color=GREY_A)
        spl.move_to([0, -3.2, 0])
        # a large model's sink, drawn
        n = 40
        g = np.random.default_rng(3)
        sk = np.tril(np.exp(-np.abs(np.subtract.outer(np.arange(n), np.arange(n))) / 2.0) * 0.3 + g.random((n, n)) * 0.05)
        sk[:, 0] += 2.0
        sk = np.tril(sk) / np.tril(sk).sum(1, keepdims=True)
        simg = framed(heat_image(sk, 3.2, 3.2, color=A, mask_upper=True)).move_to([3.9, 0.1, 0])
        sl = label(r"a sink head in a large model \ (schematic)", font_size=20, color=GREY_A).next_to(simg, UP, buff=0.12)
        scol = Rectangle(width=3.2 / n * 1.6, height=3.2, stroke_color=POS, stroke_width=2.5).move_to(simg.get_left(),
                                                                                                    aligned_edge=LEFT)
        cite_ = cite(r"G.~Xiao et al., \textit{Efficient Streaming Language Models with Attention Sinks} (2023)",
                     corner=UR)
        # StreamingLLM's recipe: keep the first four tokens and a window of the latest
        cap0 = label(r"in large models, \ many heads put most of their weight \\ on the first token, \ whatever it is",
                     font_size=22, color=GREY_A).move_to([-3.6, 2.75, 0])
        boxes = VGroup()
        for i in range(17):
            if i == 4:
                boxes.add(MathTex(r"\cdots", font_size=30, color=GREY_B))
                continue
            kept = i < 4
            boxes.add(Square(0.3, stroke_color=POS if kept else A, stroke_width=2,
                             fill_color=POS if kept else A, fill_opacity=0.55 if kept else 0.25))
        boxes.arrange(RIGHT, buff=0.08).move_to([-3.6, 1.85, 0])
        bk = VGroup(Brace(boxes[:4], DOWN, buff=0.05, color=POS), Brace(boxes[5:], DOWN, buff=0.05, color=A))
        bkl = VGroup(label(r"the first $4$", font_size=18, color=POS).next_to(bk[0], DOWN, buff=0.05),
                     label(r"a window of the latest", font_size=18, color=A).next_to(bk[1], DOWN, buff=0.05))
        stream = VGroup(boxes, bk, bkl)
        if strong:
            mine = (f"Some heads of our model put a large share of it, up to {sink.max():.0%}, on the very first "
                    f"character, whatever that character is: about {ratio:.0f} times an even share. ")
        else:
            mine = (f"In our small model, nothing like it: no head gives the first character more than "
                    f"{ratio:.1f} times an even share. Its heads park attention elsewhere, on spaces and line breaks: "
                    f"one head spends {hi_sp:.0%} of its attention on them, though they are {sps:.0%} of the text. ")
        with self.voiceover(
            "In 2023 Guangxuan Xiao and colleagues found something strange: in large models, many heads put most of "
            "their weight on the very first token, whatever it is. <bookmark mark='a'/> They called these attention "
            "sinks, and showed that keeping the first four tokens lets a model read on for millions of tokens with a "
            "short window. <bookmark mark='b'/> " + mine
        ) as vo:
            self.play(FadeIn(simg), FadeIn(sl), FadeIn(cite_), FadeIn(cap0))
            vo.wait_until("a")
            self.play(Create(scol), FadeIn(stream, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(bl), Create(base), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.03),
                      Create(ul), FadeIn(ulab), FadeIn(lyr), run_time=2.0)
            if not strong:
                self.play(FadeIn(spl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        rows = [
            cmath(r"\textstyle\sum_j p_{ij}", r"=", r"1", font_size=36, colors={r"\textstyle\sum_j p_{ij}": A}),
            cmath(r"\operatorname{out}_i", r"=", r"\textstyle\sum_j p_{ij}\, v_j \approx 0", font_size=36,
                  colors={r"\operatorname{out}_i": V}),
            cmath(r"p_{i,\text{sink}} \approx 1,", r"\quad", r"v_{\text{sink}} \approx 0", font_size=36),
        ]
        whys = [why(r"a softmax must hand out all its weight"), why(r"a head with nothing to add \\ should add nothing"),
                why(r"so: \ park the weight on a token \\ whose value is small")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-2.2, buff=0.65, edge=6.9)
        cards = VGroup(
            label(r"value-state drains: \ the sink's value shrinks", font_size=22, color=GREY_A),
            label(r"massive activations: \ the sink's residual vector grows huge", font_size=22, color=GREY_A),
            label(r"Guo et al.\ (2024): \ an \textit{active--dormant} head", font_size=22, color=POS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, -2.3, 0])
        with self.voiceover(
            "Why would a head stare at a meaningless token? Because of the softmax. <bookmark mark='a'/> Its weights "
            "must add up to one: a head cannot decline to attend. <bookmark mark='b'/> But many heads have work to "
            "do only some of the time: after a particular kind of token, say. The rest of the time, the right "
            "output is nothing. <bookmark mark='c'/> The only way to output nothing is to put the weight on a token "
            "whose value is close to zero. A token that is always there, at the start, is the natural parking spot. "
            "<bookmark mark='d'/> Tianyu Guo, Song Mei and colleagues traced the whole syndrome to such active-dormant "
            "heads in 2024: the sink's value shrinks, and its vector in the residual stream grows enormous."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(Indicate(rows[0][2], color=A))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.1) for c_ in cards], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def task(self):
        s = load("sinks")
        chars = [str(c) for c in s["chars"]]
        trig = [int(i) for i in s["trig"]]
        x = [int(v) for v in np.asarray(s["example"])]
        c = dict(s["cfg"])
        V_ = len(chars)

        def ch(i):
            return "<s>" if i == V_ else chars[i]

        n = 20
        cells = VGroup()
        for j in range(n):
            t_ = ch(x[j])
            is_t = x[j] in trig
            box = Square(0.5, stroke_width=1.5, stroke_color=SINKC if j == 0 else (POS if is_t else GREY_D),
                         fill_color=PANEL, fill_opacity=1)
            txt = (label(r"$\langle s\rangle$", font_size=18, color=SINKC) if j == 0 else
                   data_text(show_char(t_), font=MONO, font_size=22, color=POS if is_t else WHITE))
            cells.add(VGroup(box, txt.move_to(box)))
        cells.arrange(RIGHT, buff=0.06).move_to([0, 2.3, 0])
        arrows = VGroup()
        for j in range(1, n - 1):
            if x[j] in trig and j >= 2:
                arrows.add(CurvedArrow(cells[j - 1].get_bottom() + DOWN * 0.05, cells[j + 1].get_bottom() + DOWN * 0.05,
                                       angle=PI / 2.2, color=POS, stroke_width=2.5, tip_length=0.12))
        tnames = ["a space" if chars[i] == " " else rf"``{chars[i]}''" for i in trig]
        tl = label(rf"after a trigger ({', '.join(tnames[:-1])} or {tnames[-1]}), \ copy the character before it; \ "
                   r"otherwise, the novels' next-character statistics", font_size=20, color=GREY_A)
        spoken = ["a space" if chars[i] == " " else f"an {chars[i]}" if chars[i] in "aeiou" else f"a {chars[i]}"
                  for i in trig]
        trig_txt = ", ".join(spoken[:-1]) + " or " + spoken[-1]
        tl.next_to(cells, DOWN, buff=0.75)
        M = np.asarray(s["softmax_map"])
        img = framed(heat_image(M, 3.0, 3.0, color=A, mask_upper=True)).move_to([-3.6, -1.35, 0])
        il = label(r"the plain head, \ first seed: \ $24$ positions of one sequence", font_size=18, color=GREY_A)
        il.next_to(img, DOWN, buff=0.12)
        col = Rectangle(width=3.0 / M.shape[0] * 1.3, height=3.0, stroke_color=SINKC, stroke_width=2.5)
        col.move_to(img.get_left(), aligned_edge=LEFT)
        bd, ba = np.asarray(s["softmax_bos_dormant"]), np.asarray(s["softmax_bos_active"])
        pa = np.asarray(s["softmax_prev_active"])
        vb, vr = np.asarray(s["softmax_v_bos"]), np.asarray(s["softmax_v_rest"])
        facts = VGroup(
            label(rf"nothing to copy: \ ${bd.mean():.0%}$ of the weight on $\langle s\rangle$".replace("%", r"\%"),
                  font_size=22, color=SINKC),
            label(rf"after a trigger: \ ${pa.mean():.0%}$ on the character before".replace("%", r"\%"), font_size=22,
                  color=POS),
            label(rf"$\langle s\rangle$'s value: \ ${vb.mean() / vr.mean():.2f}\times$ the size of the others'",
                  font_size=22, color=GREY_A),
            note(rf"means over ${len(bd)}$ seeds; \ ranges ${bd.min():.0%}$--${bd.max():.0%}$, "
                 rf"${pa.min():.0%}$--${pa.max():.0%}$".replace("%", r"\%")),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([2.9, -1.35, 0])
        keep_in_frame(facts)
        sink_formed = bd.mean() > 0.4
        drain = vb.mean() < 0.8 * vr.mean()
        v1 = (f"When there is nothing to copy, it puts {bd.mean():.0%} of its weight on the start marker, which carries "
              "no information about the next character: a sink, formed in a model of one layer. " if sink_formed else
              f"When there is nothing to copy, it puts only {bd.mean():.0%} of its weight on the start marker: in a "
              "run this short the sink is still forming. ")
        v2 = (f"And the marker's value has shrunk to {vb.mean() / vr.mean():.2f} times the size of the others': the "
              "drain." if drain else f"Its value is {vb.mean() / vr.mean():.2f} times the size of the others': no "
              "drain yet.")
        with self.voiceover(
            "We can grow a sink on purpose. Guo's team built a task where one head is needed only some of the time. "
            f"<bookmark mark='a'/> We made it from the novels' {V_} commonest characters: each character follows "
            f"the novels' statistics for what comes next, except after a trigger, {trig_txt}, where the "
            "next character copies the one before the trigger. Every sequence starts with a marker. "
            f"<bookmark mark='b'/> A one-layer transformer learns it in {int(c['steps']):,} steps, three times over. "
            f"After a trigger its head looks one back, {pa.mean():.0%} of the time. <bookmark mark='c'/> " + v1
            + "<bookmark mark='d'/> " + v2
        ) as vo:
            # the trained head's map waits under a veil from the first word, and is uncovered once it has been trained
            veil = Rectangle(width=max(img.width, il.width) + 0.2, height=img.height + il.height + 0.4, stroke_width=0,
                             fill_color=config.background_color, fill_opacity=0.72).move_to(Group(img, il))
            veil.set_z_index(5)
            self.add(veil)
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.03), FadeIn(img), FadeIn(il))
            vo.wait_until("a")
            self.play(FadeIn(tl), LaggedStart(*[Create(a_) for a_ in arrows], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeOut(veil), FadeIn(facts[1]))
            vo.wait_until("c")
            self.play(Create(col), FadeIn(facts[0]))
            vo.wait_until("d")
            self.play(FadeIn(facts[2:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ways(self):
        s = load("sinks")
        bos = {v: np.asarray(s[f"{v}_bos_dormant"]) for v in VARIANTS}
        cp = {v: np.asarray(s[f"{v}_loss_copy"]) for v in VARIANTS}
        bg = {v: np.asarray(s[f"{v}_loss_bigram"]) for v in VARIANTS}
        null = np.asarray(s["sink_null_dormant"])
        g_d, g_a = np.asarray(s["gate_gate_dormant"]), np.asarray(s["gate_gate_active"])
        lam = np.asarray(s["diff_lam"])
        p1 = np.asarray(s["diff_p1_bos_dormant"])
        eqs = VGroup(
            cmath(r"p_j", r"=", r"\frac{e^{s_j}}{e^{\,b} + \sum_k e^{s_k}}", font_size=28, colors={r"e^{\,b}": SINKC}),
            cmath(r"o", r"=", r"\operatorname{Attn}(x) \odot \sigma(x W_g)", font_size=28),
            cmath(r"A", r"=", r"\operatorname{softmax}(Q_1 K_1^\top) - \lambda\, \operatorname{softmax}(Q_2 K_2^\top)",
                  font_size=26),
        )
        names = VGroup(label(r"a sink logit \ (gpt-oss, 2025)", font_size=22, color=SINKC),
                       label(r"an output gate \ (Qiu et al.\ 2025; \ Qwen3-Next)", font_size=22, color=GATEC),
                       label(r"differential attention \ (Ye et al.\ 2024)", font_size=22, color=DIFFC))
        blocks = VGroup(*[VGroup(n_, e_).arrange(DOWN, aligned_edge=LEFT, buff=0.12) for n_, e_ in zip(names, eqs)])
        blocks.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([-3.6, 1.0, 0])
        # each design's training, three seeds each: the weight on <s> when there is nothing to copy, every 100 steps
        hist = {v: np.asarray(s[f"{v}_hist"], float) for v in VARIANTS}  # seed, checkpoint, (step, bigram, copy, <s>)
        hx = hist["softmax"][0, :, 0]
        ytop = max(0.6, float(np.ceil(max(hist[v][:, :, 3].max() for v in VARIANTS) * 5) / 5))
        ch = axes([0, float(hx[-1]), 500], [0, ytop, 0.2], x_length=4.4, y_length=2.1, xlabel=r"training steps",
                  xticks=[0, 500, 1000, int(hx[-1])], xfmt=lambda v: f"{int(v):,}".replace(",", "{,}"),
                  yticks=[0, round(ytop / 2, 1), ytop], yfmt=lambda v: f"{v:.1f}", font_size=18, center=[3.85, 0.75, 0])
        lines = {v: seed_lines(ch.ax, hx, np.clip(hist[v][:, :, 3], 0, ytop), SINK_COLORS[v], 3) for v in VARIANTS}
        ct = label(r"weight on $\langle s\rangle$ \ when there is nothing to copy, \\ during training \ (three seeds each)",
                   font_size=20, color=GREY_A)
        ct.next_to(ch, UP, buff=0.2)
        loss = VGroup(label(r"at the end: \ weight on $\langle s\rangle$; \ bits on the copies, \ and on the rest",
                            font_size=20, color=GREY_A),
                      *[label(rf"{SINK_NAMES[v]}: \ ${bos[v].mean():.2f}$; \ ${cp[v].mean():.3f}$, \ ${bg[v].mean():.3f}$",
                              font_size=18, color=SINK_COLORS[v]) for v in VARIANTS],
                      note(rf"the task's own probabilities, \ on the rest: \ ${float(load('sinkref')['true_bits']):.3f}$",
                           font_size=18))
        loss.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.0, -2.55, 0])
        keep_in_frame(loss)
        facts = label(r"Qiu et al.: \ attention on the first token, \ $46.7\%$ $\to$ $4.8\%$ with the gate; \\ "
                      r"Qwen3-Next and Kimi K3 gate their attention", font_size=20, color=GREY_A).move_to([-3.6, -2.6, 0])
        base_sink = bos["softmax"].mean()

        r_s, r_g, r_d = (float(bos[v].mean()) for v in ("sink", "gate", "diff"))
        nl, gd_, ga_, lm_ = float(null.mean()), float(g_d.mean()), float(g_a.mean()), float(lam.mean())
        v_sink = (f"The sink logit gives the head a place to send its weight that is not a token at all: its weight on "
                  f"the marker falls to {r_s:.0%}, and {nl:.0%} goes nowhere." if r_s < 0.7 * base_sink else
                  f"The sink logit gives the head a place to send its weight that is not a token at all, but its weight "
                  f"on the marker stays at {r_s:.0%}, and only {nl:.0%} goes nowhere.")
        if ga_ > gd_ + 0.05:
            v_gate = (f"The gate lets the head simply switch itself off: it is {gd_:.2f} open when there is nothing to "
                      f"copy and {ga_:.2f} after a trigger, and its weight on the marker is {r_g:.0%}.")
        else:
            v_gate = (f"The gate could let the head switch itself off, but it ends about as open with nothing to copy, "
                      f"{gd_:.2f}, as after a trigger, {ga_:.2f}, and its weight on the marker is {r_g:.0%}.")
        sm_ = float(np.asarray(s["diff_sum_dormant"]).mean())
        v_diff = (f"Differential attention subtracts a second softmax, so its weights need not add up to one: with "
                  f"nothing to copy they add up to {sm_:.2f}, with lambda at {lm_:.2f}, and its weight on the marker is "
                  f"{r_d:.0%}.")
        worst_cp = max(VARIANTS, key=lambda v: cp[v].mean())
        same = max(cp[v].mean() for v in VARIANTS) - min(cp[v].mean() for v in VARIANTS) < 0.05
        worst_name = SPOKEN_SINK[worst_cp]
        v_loss = ("All four learn the task about equally well, so the sinks were never needed for the task "
                  "itself; they were the softmax's way of doing nothing." if same else
                  f"They do not learn the copies equally well: {worst_name} is worst, at "
                  f"{cp[worst_cp].mean():.3f} bits on the copies.")
        with self.voiceover(
            "Three recent designs give a head a better way to do nothing; we trained each on the same task, three "
            "seeds each. <bookmark mark='a'/> gpt-oss adds a learned number to the softmax's denominator, the score "
            "of an invisible key. <bookmark mark='b'/> Gated attention multiplies each head's output by a sigmoid of "
            "the input. <bookmark mark='c'/> Differential attention subtracts two softmax maps. <bookmark mark='d'/> "
            "Here is each design's weight on the marker as it trains. " + v_sink
            + " <bookmark mark='e'/> " + v_gate + " <bookmark mark='f'/> " + v_diff + " <bookmark mark='g'/> " + v_loss
            + " In large models, the gate cut the attention on the first token from 46.7 to 4.8 percent; Qwen3-Next "
            "and Kimi K3 now gate their attention."
        ) as vo:
            self.play(FadeIn(blocks[0]), FadeIn(ct), FadeIn(ch), FadeIn(lines["softmax"][0]),
                      Create(lines["softmax"][1]), FadeIn(loss[0]), FadeIn(loss[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(blocks[1]))
            vo.wait_until("c")
            self.play(FadeIn(blocks[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines["sink"][0]), Create(lines["sink"][1]), FadeIn(loss[2]), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(lines["gate"][0]), Create(lines["gate"][1]), FadeIn(loss[3]), run_time=1.5)
            vo.wait_until("f")
            self.play(FadeIn(lines["diff"][0]), Create(lines["diff"][1]), FadeIn(loss[4]), run_time=1.5)
            vo.wait_until("g")
            self.play(FadeIn(loss[5]), FadeIn(facts))
        self.wait(0.3)
        self.clear_scene()
