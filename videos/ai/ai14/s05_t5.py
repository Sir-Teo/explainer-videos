from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import (DECODER, ENCDEC, ENCODER, HUMAN, MONO, PART, PRIOR, F, said, take_away)


class TextToText(VoiceoverScene):
    def construct(self):
        self.card()
        self.text_to_text()
        self.spans()
        self.table()
        self.twist()

    def card(self):
        card = chapter_card(4, r"Everything is text to text", r"Which architecture and objective actually work best?",
                            lit=(2019,), part=PART)
        with self.voiceover("Chapter four. Everything is text to text."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def text_to_text(self):
        T = F.T5
        ex = [("translate English to German: That is good.", "Das ist gut."),
              ("cola sentence: The course is jumping well.", "not acceptable"),
              ("stsb sentence1: The rhino grazed on the grass. sentence2: A rhino is grazing in a field.", "3.8"),
              ("summarize: state authorities dispatched emergency crews tuesday to survey the damage after an "
               "onslaught of severe weather in mississippi...", "six people hospitalized after a storm in attala county.")]
        t5 = VGroup(RoundedRectangle(width=1.4, height=4.6, corner_radius=0.2, stroke_color=ENCDEC, stroke_width=3,
                                     fill_color=ENCDEC, fill_opacity=0.12), label(r"T5", font_size=40, color=ENCDEC))
        t5[1].move_to(t5[0])
        t5.move_to([0.2, -0.2, 0])
        ins = VGroup(*[said(a, chars=36, font_size=17, max_lines=3, box_color=GREY_B) for a, _ in ex])
        ins.arrange(DOWN, buff=0.25, aligned_edge=RIGHT).next_to(t5, LEFT, buff=0.6)
        outs = VGroup(*[said(b, chars=26, font_size=17, max_lines=2, box_color=ENCDEC) for _, b in ex])
        for o, i in zip(outs, ins):
            o.next_to(t5, RIGHT, buff=0.6).set_y(i.get_y())
        arr_in = VGroup(*[Arrow(i.get_right(), [t5.get_left()[0], i.get_y(), 0], buff=0.08, stroke_width=2,
                                color=GREY_B) for i in ins])
        arr_out = VGroup(*[Arrow([t5.get_right()[0], o.get_y(), 0], o.get_left(), buff=0.08, stroke_width=2,
                                 color=ENCDEC) for o in outs])
        hc = label(r"Raffel, Shazeer, Roberts, Lee, Narang, Matena, Zhou, Li \& Liu \ (Google, October 2019)",
                   font_size=22, color=GREY_A).to_edge(UP, buff=0.3)
        c4 = label(rf"trained on C4: \ a cleaned web crawl of about ${T['c4_gb']}$ GB", font_size=24, color=C.DATA)
        c4.to_corner(DL, buff=0.3)
        tag = note(r"examples from Raffel et al.\ (2019), Figure 1").to_corner(DR, buff=0.2)
        ask = label(r"so many objectives and architectures: \\ which actually work best?", font_size=34,
                    color=WHITE).move_to([0.2, 0.0, 0])
        with self.voiceover(
            "In October 2019, Colin Raffel and colleagues at Google asked a plain question. With so many objectives "
            "and architectures on offer, which actually work best? To compare them fairly, they first made every task "
            "the same shape. <bookmark mark='a'/> Text in, text out. Translation: the words 'translate English to "
            "German', then the sentence, and the model writes the German. <bookmark mark='b'/> Grammar: the model "
            "writes 'acceptable' or 'not acceptable'. Even a similarity score is written out as text: three point "
            "eight. <bookmark mark='c'/> And summaries. One model, one loss, one way of decoding, for every task. They "
            "called it T5, the Text-to-Text Transfer Transformer, and trained it on C4, a cleaned crawl of the web of "
            "about 750 gigabytes."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(ask), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeOut(ask), FadeIn(t5))
            self.play(FadeIn(ins[0]), GrowArrow(arr_in[0]))
            self.play(GrowArrow(arr_out[0]), FadeIn(outs[0]))
            vo.wait_until("b")
            for k in (1, 2):
                self.play(FadeIn(ins[k]), GrowArrow(arr_in[k]), GrowArrow(arr_out[k]), FadeIn(outs[k]))
            vo.wait_until("c")
            self.play(FadeIn(ins[3]), GrowArrow(arr_in[3]), GrowArrow(arr_out[3]), FadeIn(outs[3]))
            self.play(FadeIn(c4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spans(self):
        T = F.T5
        orig = "Thank you for inviting me to your party last week ."
        toks = orig.split()
        drop = {2, 3, 8}  # "for inviting", "last"
        row = VGroup(*[said(t, chars=20, font_size=20, max_lines=1) for t in toks]).arrange(RIGHT, buff=0.08)
        row.move_to(UP * 1.6)
        for i in drop:
            row[i][0].set_stroke(ENCDEC, width=3)
        inp = ["Thank", "you", "<X>", "me", "to", "your", "party", "<Y>", "week", "."]
        tgt = ["<X>", "for", "inviting", "<Y>", "last", "<Z>"]
        sent = {"<X>": ENCDEC, "<Y>": ENCDEC, "<Z>": ENCDEC}
        r_in = VGroup(*[said(t, chars=20, font_size=20, max_lines=1, box_color=sent.get(t, GREY_B)) for t in inp])
        r_in.arrange(RIGHT, buff=0.08).move_to(UP * 0.0)
        r_tg = VGroup(*[said(t, chars=20, font_size=20, max_lines=1, box_color=sent.get(t, ENCDEC)) for t in tgt])
        r_tg.arrange(RIGHT, buff=0.08).move_to(DOWN * 1.6)
        li = label(r"input", font_size=22, color=GREY_A).next_to(r_in, LEFT, buff=0.3)
        lt = label(r"target", font_size=22, color=ENCDEC).next_to(r_tg, LEFT, buff=0.3)
        lo = label(r"original", font_size=22, color=GREY_A).next_to(row, LEFT, buff=0.3)
        rule = label(rf"corrupt ${int(T['corrupt'] * 100)}\%$ of the tokens, \ in spans of about ${T['span']}$; \ "
                     r"each span becomes one sentinel", font_size=24, color=WHITE).to_edge(DOWN, buff=0.6)
        tag = note(r"example from Raffel et al.\ (2019), Figure 2").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Their pretraining objective, the one that won their comparison, is a cousin of BERT's masking, called "
            "span corruption. <bookmark mark='a'/> Pick fifteen percent of the tokens, in spans averaging three "
            "tokens. <bookmark mark='b'/> Replace each span with one sentinel token in the input. <bookmark mark='c'/> "
            "The target is just the missing spans, each after its sentinel. The encoder reads the damaged text both "
            "ways; the decoder writes what was taken out."
        ) as vo:
            self.play(FadeIn(row), FadeIn(lo), FadeIn(tag))
            vo.wait_until("a")
            self.play(*[Indicate(row[i], color=ENCDEC) for i in drop], FadeIn(rule))
            vo.wait_until("b")
            self.play(FadeIn(r_in, shift=DOWN * 0.1), FadeIn(li))
            vo.wait_until("c")
            self.play(FadeIn(r_tg, shift=DOWN * 0.1), FadeIn(lt))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        T = F.T5
        head = [r"architecture", r"objective", r"GLUE", r"SQuAD", r"SuperGLUE"]
        xs = [-4.4, -1.4, 1.2, 3.1, 5.2]
        y0 = 2.0
        hrow = VGroup(*[label(h, font_size=24, color=GREY_A).move_to([x, y0, 0]) for h, x in zip(head, xs)])
        cols = {"encoder-decoder": ENCDEC, "prefix LM": ENCODER, "decoder-only LM": DECODER}
        rows = VGroup()
        vals = np.array([[r[2], r[3], r[4]] for r in T["table"]])
        for k, (arch, obj, *v) in enumerate(T["table"]):
            y = y0 - 0.72 * (k + 1)
            cells = VGroup(label(arch, font_size=24, color=cols[arch]).move_to([xs[0], y, 0]),
                           label(r"denoising" if obj == "denoising" else r"next token (LM)", font_size=22,
                                 color=WHITE).move_to([xs[1], y, 0]))
            for j, x in enumerate(xs[2:]):
                col = vals[:, j]
                t = (v[j] - col.min()) / (col.max() - col.min())
                bg = RoundedRectangle(width=1.3, height=0.52, corner_radius=0.06, stroke_width=0,
                                      fill_color=interpolate_color(ManimColor("#3A2230"), ManimColor(ENCDEC), t),
                                      fill_opacity=0.55).move_to([x, y, 0])
                cells.add(VGroup(bg, MathTex(f"{v[j]:.1f}", font_size=28).move_to(bg)))
            rows.add(cells)
        best = SurroundingRectangle(rows[0], color=ENCDEC, buff=0.08, stroke_width=3)
        worst = SurroundingRectangle(rows[5], color=DECODER, buff=0.08, stroke_width=3)
        gap = T["table"][0][2] - T["table"][5][2]
        cite_ = cite(r"Raffel et al.\ (2019), Table 2: \ models of equal cost, \ fine-tuned, \ dev sets")
        with self.voiceover(
            "Then came the comparison, with every model given the same budget of compute. <bookmark mark='a'/> Here "
            "are the architectures and objectives, each pretrained, then fine-tuned and scored on three benchmarks: "
            "GLUE, question answering, and SuperGLUE. <bookmark mark='b'/> The encoder–decoder trained by denoising "
            f"came first, with {T['table'][0][2]:.1f} on GLUE. <bookmark mark='c'/> The decoder-only language model, "
            f"trained to predict the next token, the GPT recipe, came last: {T['table'][5][2]:.1f}, about "
            f"{round(gap)} points behind. On tasks fine-tuned for understanding, seeing both ways won again."
        ) as vo:
            self.play(FadeIn(hrow), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in rows], lag_ratio=0.2), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(best))
            vo.wait_until("c")
            self.play(Create(worst))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def twist(self):
        W, S = F.WANG2022, F.SUPERGLUE
        top = label(rf"T5-11B on SuperGLUE: \ ${S['t5']}$, \ people ${S['human']}$", font_size=30, color=ENCDEC)
        top.to_edge(UP, buff=0.5)
        q = label(r"so why did the decoder-only design take over?", font_size=32, color=DECODER).next_to(top, DOWN,
                                                                                                         buff=0.4)
        hc = history_card(2022, r"Wang, Roberts, Hesslow, Le Scao, Chung, Beltagy, Launay \& Raffel (BigScience)",
                          rf"models of ${W['params'] / 1e9:.0f}$ billion parameters, ${W['tokens'] / 1e9:.0f}$ billion "
                          r"tokens, every architecture and objective", width=9.0, color=PRIOR)
        hc.next_to(q, DOWN, buff=0.35)
        left = VGroup(label(r"fine-tuned on many prompted tasks", font_size=26, color=GREY_A),
                      label(r"best: \ sees both ways, \\ masked objective", font_size=32, color=ENCODER)).arrange(DOWN, buff=0.2)
        right = VGroup(label(r"no fine-tuning: \ just prompted", font_size=26, color=GREY_A),
                       label(r"best: \ causal decoder, \\ next token", font_size=32, color=DECODER)).arrange(DOWN, buff=0.2)
        VGroup(left, right).arrange(RIGHT, buff=1.6).next_to(hc, DOWN, buff=0.6)
        for side_, col in ((left, ENCODER), (right, DECODER)):
            side_.add_to_back(SurroundingRectangle(side_, color=col, buff=0.25, corner_radius=0.12, stroke_width=2))
        tw = take_away(r"the field was about to stop fine-tuning, \ and start asking", color=DECODER, font_size=28)
        with self.voiceover(
            "The largest T5, eleven billion parameters, came within a point of the human score on SuperGLUE. And yet "
            "the decoder-only design is the one that took over. Why? <bookmark mark='a'/> A 2022 study by Thomas Wang "
            "and colleagues, in the BigScience collaboration, gives the clearest answer. They trained five-billion-"
            "parameter models on 170 billion tokens with each architecture and objective. <bookmark mark='b'/> Judged "
            "after fine-tuning on many tasks, the models that see both ways, with masked objectives, were best, just as "
            "T5 found. <bookmark mark='c'/> But judged with no fine-tuning at all, simply prompting the pretrained "
            "model, the causal decoder trained on the next token was best. <bookmark mark='d'/> And the field was about "
            "to stop fine-tuning a separate model for every task, and start asking one model, in words. That shift "
            "began with GPT-2."
        ) as vo:
            self.play(FadeIn(top), FadeIn(q))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(left, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(right, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(tw))
        self.wait(0.3)
        self.clear_scene()
