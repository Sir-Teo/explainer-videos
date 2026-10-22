from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import (C_COL, DECODER, ENCODER, MONO, PART, PRIOR, F, arch_diagram, chip, human, load,
                                   node_box, said, take_away)


def pct(x: float) -> str:
    return f"{100 * x:.1f}"


class OurLineage(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup()
        self.replay_gpt()
        self.replay_bert()
        self.cloze()
        self.probe()
        self.writing()

    def card(self):
        card = chapter_card(13, r"Our own lineage: \ GPT against BERT", r"On equal compute, which objective learns "
                            r"more?", lit=(2018,), part=PART)
        with self.voiceover("Chapter thirteen. Our own lineage: GPT against BERT."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def setup(self):
        g, L = load("gpt_m"), load("lineage")
        sh, p = g["shape"], g["params"]
        gpt = VGroup(arch_diagram("decoder", 1.0), label(r"GPT-style: \ predict every next token", font_size=22,
                                                         color=DECODER)).arrange(DOWN, buff=0.25)
        bert = VGroup(arch_diagram("encoder", 1.0), label(r"BERT-style: \ predict the hidden $15\%$", font_size=22,
                                                          color=ENCODER)).arrange(DOWN, buff=0.25)
        pair = VGroup(gpt, bert).arrange(RIGHT, buff=1.2, aligned_edge=UP).move_to([-3.4, 1.3, 0])
        same = VGroup(
            label(rf"same shape: \ ${sh['layers']}$ layers, \ width ${sh['d']}$, \ ${sh['heads']}$ heads, \ "
                  rf"${p['total'] / 1e6:.2f}$M parameters", font_size=22, color=WHITE),
            label(r"same block: \ pre-norm RMSNorm, SwiGLU, RoPE, no biases", font_size=22, color=WHITE),
            label(r"same starting weights, \ same text in the same order", font_size=22, color=WHITE),
            label(rf"same ${g['tokens'] / 1e6:.1f}$ million tokens, \ optimizer, \ schedule", font_size=22, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([-3.2, -1.7, 0])
        flops = cmath(r"C", r"=", r"6 N D", r"=", rf"6 \times {p['compute'] / 1e6:.2f}\text{{M}} \times "
                                                  rf"{g['tokens'] / 1e6:.1f}\text{{M}} \approx " + sci(g["flops"], 1),
                      font_size=30).move_to([3.4, 1.6, 0])
        flops[0].set_color(C_COL)
        fl = label(r"each, \ counting the matrices every token passes through", font_size=18, color=GREY_B)
        fl.next_to(flops, DOWN, buff=0.12)
        d = definition_card(r"fair, \ here", r"equal model, \ equal data, \ equal compute: \ only the attention mask and "
                            r"the objective differ. \ Judged on tasks both can do.", color=C.BITS, width=6.0,
                            font_size=22).move_to([3.4, -1.0, 0])
        tag = note(r"computed: \ trained on this computer, \ on Part 1's thirty novels").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Now our own version of the 2018 question. Two models with exactly the same shape: "
            f"{sh['layers']} layers, a width of {sh['d']}, {sh['heads']} heads, {p['total'] / 1e6:.2f} million "
            "parameters, built from the modern block of chapter ten. <bookmark mark='a'/> They start from identical "
            f"weights and read the same {g['tokens'] / 1e6:.1f} million tokens of the thirty novels, in the same "
            "order, with the same optimizer and learning-rate schedule. <bookmark mark='b'/> Only two things differ. "
            "The GPT-style model's attention looks back only, and it predicts every next token. The BERT-style "
            "model's attention looks both ways, and it predicts the fifteen percent of tokens we hide. "
            "<bookmark mark='c'/> So the compute is identical: six, times the parameters each token passes through, "
            "times the tokens. <bookmark mark='d'/> That is what fair means here: the same model, the same data, the "
            "same compute, with only the objective changed; and then a test on tasks both can do."
        ) as vo:
            self.play(FadeIn(pair), FadeIn(tag))
            self.play(FadeIn(same[0]), FadeIn(same[1]))
            vo.wait_until("a")
            self.play(FadeIn(same[2]), FadeIn(same[3]))
            vo.wait_until("b")
            self.play(Indicate(pair[0][0], color=DECODER), Indicate(pair[1][0], color=ENCODER))
            vo.wait_until("c")
            self.play(Write(flops), FadeIn(fl))
            vo.wait_until("d")
            self.play(FadeIn(d, shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def _curve_panel(self, run, color, ylabel, center):
        cv = np.asarray(run["curve"])
        sn = run["snaps"]
        S = float(run["tokens"])
        ys = [s["val"] for s in sn]
        top = math.ceil(max(max(ys), float(np.percentile(cv[:, 2], 99))) + 0.2)
        bot = math.floor(min(ys) - 0.3)
        g = axes([0, S], [bot, top], x_length=5.4, y_length=3.6, xlabel=r"tokens read", ylabel=ylabel,
                 xticks=[0, S / 2, S], yticks=[bot, top], xfmt=lambda v: rf"{v / 1e6:.0f}\text{{M}}" if v else "0",
                 center=center)
        train = curve(g.ax, cv[:, 1], np.clip(cv[:, 2], bot, top), color, 2)
        train.set_stroke(opacity=0.35)
        pts = VGroup(*[Dot(g.ax.c2p(s["tokens"], s["val"]), radius=0.06, color=color) for s in sn])
        return g, train, pts, top

    def replay_gpt(self):
        r = load("gpt_m")
        sn = r["snaps"]
        g, train, pts, top = self._curve_panel(r, DECODER, r"next-token loss (nats)", [-3.6, -0.4, 0])
        prompt = data_text("The door opened, and", font=MONO, font_size=22, color=GREY_A)
        prompt.move_to([3.3, 2.4, 0])
        held = label(r"held-out text \ (dots); \ training batches \ (faint)", font_size=18, color=GREY_B)
        held.next_to(g, UP, buff=0.15).align_to(g, LEFT)
        k_show = list(range(len(sn)))
        boxes = [said(s["sample"], chars=34, font_size=20, max_lines=4, box_color=DECODER).move_to([3.3, 0.6, 0])
                 for s in sn]
        steps = [label(rf"after ${s['tokens'] / 1e6:.2f}$M tokens: \ held-out loss ${s['val']:.2f}$", font_size=22,
                       color=DECODER).move_to([3.3, -1.4, 0]) for s in sn]
        tag = note(r"computed: \ the same seed for every sample").to_corner(DR, buff=0.2)
        first, last = sn[0], sn[-1]
        uniform = math.log(4096)
        start = (f"Untrained, its loss is {first['val']:.2f} nats per token, about what guessing uniformly among four "
                 "thousand tokens gives, and it writes noise." if abs(first["val"] - uniform) < 0.4 else
                 f"Untrained, its loss is {first['val']:.2f} nats per token, and it writes noise.")
        cv = np.asarray(r["curve"])
        train_end = float(np.mean(cv[-max(5, len(cv) // 20):, 2]))
        gap = last["val"] - train_end
        fit = ("The two stay together: it is learning the language of the novels, not memorizing its batches."
               if gap < 0.1 else
               f"By the end the training loss is {gap:.2f} nats below the held-out loss: it has begun to memorize "
               "what it reads.")
        with self.voiceover(
            "Watch the GPT-style model learn. On the left, its loss on held-out text as training goes on; on the right, "
            "what it writes after the words 'The door opened, and', frozen at each checkpoint, with the same random "
            "seed every time. <bookmark mark='a'/> " + start + " <bookmark mark='b'/> Let it read. Each dot is "
            "the loss on text it never trains on, and the faint line is the loss on the batches it does train on. "
            "The checkpoints are spaced out geometrically: close together early, when it changes fastest. " + fit +
            f" <bookmark mark='c'/> By the end, the loss is {last['val']:.2f} nats, and it writes something "
            "like the novels it read: not sense yet, but their words and rhythm."
        ) as vo:
            self.play(FadeIn(g), FadeIn(held), FadeIn(prompt), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(pts[0], scale=1.5), FadeIn(boxes[0]), FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(Create(train), run_time=1.5)
            cur_b, cur_s = boxes[0], steps[0]
            per = max(0.8, vo.until("c") / max(1, len(k_show) - 1))
            for k in k_show[1:]:
                self.play(FadeIn(pts[k], scale=1.5), ReplacementTransform(cur_b, boxes[k]),
                          ReplacementTransform(cur_s, steps[k]), run_time=0.6 * per)
                cur_b, cur_s = boxes[k], steps[k]
                self.wait(0.4 * per)
            vo.wait_until("c")
            self.play(Indicate(cur_b, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()

    def replay_bert(self):
        r = load("bert_m")
        sn = r["snaps"]
        g, train, pts, top = self._curve_panel(r, ENCODER, r"loss on the hidden tokens (nats)", [-3.6, -0.4, 0])
        sent = "It was a cold ___ in the ___ of winter, and the ___ was falling."
        parts = sent.split("___")

        def filled(words):
            row = VGroup()
            for k, part in enumerate(parts):
                if part.strip():
                    row.add(data_text(part.strip(), font=MONO, font_size=20, color=GREY_A))
                if k < len(words):
                    row.add(chip(words[k], ENCODER, font_size=20))
            return row.arrange(RIGHT, buff=0.12)

        rows = [filled(s["fill"]) for s in sn]
        for rw in rows:
            if rw.width > 6.6:
                rw.width = 6.6
            rw.move_to([3.4, 0.6, 0])
        steps = [label(rf"after ${s['tokens'] / 1e6:.2f}$M tokens: \ loss ${s['val']:.2f}$", font_size=22,
                       color=ENCODER).move_to([3.4, -1.0, 0]) for s in sn]
        q = label(r"a sentence we wrote, \ three words hidden", font_size=20, color=GREY_B).move_to([3.4, 1.6, 0])
        last = sn[-1]
        g_last = load("gpt_m")["snaps"][-1]["val"]
        note_ = label(rf"GPT's next-token loss: \ ${g_last:.2f}$ \\ a different problem: \ not comparable",
                      font_size=22, color=GREY_A).move_to([3.4, -2.4, 0])
        if last["val"] < g_last:
            cmp_ = (f"That number can't be compared with the GPT-style model's {g_last:.2f}: guessing a hidden word with "
                    "the words on both sides visible is a different, easier problem than guessing the next word.")
        else:
            cmp_ = (f"It is higher than the GPT-style model's {g_last:.2f}, but the two can't be compared: guessing a "
                    "hidden word with both sides visible is a different problem from guessing the next word, and the "
                    "masked model learned from only fifteen percent of the tokens.")
        with self.voiceover(
            "The BERT-style model learns to fill blanks. Here is a sentence with three words hidden, and its best "
            "guess for each, at the same checkpoints. <bookmark mark='a'/> Its loss is measured only on the hidden "
            f"words, and it falls to {last['val']:.2f} nats. <bookmark mark='b'/> " + cmp_ + " To compare the two "
            "models fairly, we need tasks both can do."
        ) as vo:
            self.play(FadeIn(g), FadeIn(q), FadeIn(pts[0]), FadeIn(rows[0]), FadeIn(steps[0]))
            self.play(Create(train), run_time=1.2)
            cur_r, cur_s = rows[0], steps[0]
            for k in range(1, len(sn)):
                self.play(FadeIn(pts[k], scale=1.5), ReplacementTransform(cur_r, rows[k]),
                          ReplacementTransform(cur_s, steps[k]), run_time=0.7)
                cur_r, cur_s = rows[k], steps[k]
                self.wait(0.3)
            vo.wait_until("b")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cloze(self):
        L = load("lineage")
        ex = L["cloze_example"]
        k = L["cloze_k"]
        sent = VGroup(data_text(ex["left"].strip(), font=MONO, font_size=20, color=WHITE),
                      data_text("____", font=MONO, font_size=20, color=YELLOW),
                      data_text(ex["right"].strip(), font=MONO, font_size=20, color=WHITE)).arrange(RIGHT, buff=0.12)
        if sent.width > 12.8:
            sent.width = 12.8
        sent.move_to(UP * 2.6)
        opts = VGroup(*[data_text(o, font=MONO, font_size=20, color=C.INTERVAL if i == ex["answer"] else GREY_A)
                        for i, o in enumerate(ex["opts"])]).arrange(RIGHT, buff=0.4).next_to(sent, DOWN, buff=0.35)
        ol = label(rf"${k}$ candidates: \ the real word and ${k - 1}$ of similar frequency", font_size=20,
                   color=GREY_B).next_to(opts, DOWN, buff=0.15)
        how = VGroup(label(r"BERT: \ a mask in the gap; \ pick the candidate it rates most likely", font_size=22,
                           color=ENCODER),
                     label(r"GPT: \ put each candidate in the gap; \ pick the most likely whole sentence",
                           font_size=22, color=DECODER),
                     label(r"GPT, left only: \ pick the most likely next word at the gap", font_size=22,
                           color=PRIOR)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([0, 0.3, 0])
        items = [(r"GPT, \ words before the gap only", L["cloze_gpt_left"], PRIOR),
                 (r"GPT, \ the whole sentence", L["cloze_gpt"], DECODER),
                 (r"BERT", L["cloze_bert"], ENCODER)]
        bars = VGroup()
        for i, (nm, v, col) in enumerate(items):
            n_ = label(nm, font_size=20, color=col).move_to([-1.5, -1.3 - 0.55 * i, 0], aligned_edge=RIGHT)
            b = Rectangle(width=max(6.0 * v, 0.02), height=0.36, stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([-1.3, -1.3 - 0.55 * i, 0], aligned_edge=LEFT)
            t = label(rf"${pct(v)}\%$", font_size=22, color=col).next_to(b, RIGHT, buff=0.12)
            bars.add(VGroup(n_, b, t))
        chance = DashedLine([-1.3 + 6.0 / k, -1.05, 0], [-1.3 + 6.0 / k, -2.6, 0], color=GREY_B, dash_length=0.06)
        cl = label(rf"chance: \ ${100 / k:.1f}\%$", font_size=18, color=GREY_B).next_to(chance, DOWN, buff=0.06)
        tag = note(rf"computed: \ ${L['cloze_n']}$ sentences from paragraphs neither model read").to_corner(DR, buff=0.2)
        b_, g_, gl_ = L["cloze_bert"], L["cloze_gpt"], L["cloze_gpt_left"]
        if b_ > g_ + 0.02:
            verdict = (f"The masked model wins, {pct(b_)} percent against {pct(g_)}: as BERT's authors found, reading "
                       "both sides directly beats inferring them through the likelihood of the whole sentence.")
        elif g_ > b_ + 0.02:
            verdict = (f"Here the GPT-style model wins, {pct(g_)} percent against {pct(b_)}: scoring whole sentences "
                       "lets it use the words after the gap too, and it learned from every token, not fifteen percent.")
        else:
            verdict = (f"They tie, {pct(g_)} and {pct(b_)} percent: once the GPT-style model scores whole sentences, "
                       "it uses the words after the gap as well as the masked model does.")
        with self.voiceover(
            "Task one: fill in a blank. Take a sentence from a paragraph neither model has read, remove one word, and "
            f"offer {k} candidates: the real word and {k - 1} others about as common. <bookmark mark='a'/> The "
            "BERT-style model reads the sentence with a mask in the gap and picks the candidate it rates most likely. "
            "The GPT-style model can't see past the gap, but it can put each candidate in place and compare the "
            "probabilities of the whole sentences, which uses the words after the gap too. For contrast, we also let "
            f"it judge from the words before the gap alone. <bookmark mark='b'/> On {L['cloze_n']} sentences, with "
            f"chance at {100 / k:.1f} percent: from the left only, the GPT-style model gets {pct(gl_)} percent. "
            f"<bookmark mark='c'/> Scoring the whole sentence, {pct(g_)}. <bookmark mark='d'/> " + verdict
        ) as vo:
            self.play(FadeIn(sent), FadeIn(opts), FadeIn(ol), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(h, shift=UP * 0.1) for h in how], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(chance), FadeIn(cl), FadeIn(bars[0][0]), GrowFromEdge(bars[0][1], LEFT), FadeIn(bars[0][2]))
            vo.wait_until("c")
            self.play(FadeIn(bars[1][0]), GrowFromEdge(bars[1][1], LEFT), FadeIn(bars[1][2]))
            vo.wait_until("d")
            self.play(FadeIn(bars[2][0]), GrowFromEdge(bars[2][1], LEFT), FadeIn(bars[2][2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def probe(self):
        L = load("lineage")
        nc = L["probe_classes"]
        pg, pb = L["probe_gpt"], L["probe_bert"]
        steps_ = VGroup(*[node_box(t, c, font_size=20) for t, c in ((r"a held-out sentence", GREY_B),
                                                      (r"frozen model", GREY_B),
                                                      (r"average of the \\ final states", C.EMBED),
                                                      (r"one linear layer \\ ($30$ books)", C.REWARD))])
        steps_.arrange(RIGHT, buff=0.5).move_to(UP * 2.0)
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, color=GREY_B, stroke_width=2.5)
                          for a, b in zip(steps_, steps_[1:])])
        info = label(rf"trained on ${L['probe_n_train']:,}$ sentences, \ tested on ${L['probe_n_test']:,}$ from "
                     r"held-out paragraphs".replace(",", "{,}"), font_size=22, color=GREY_A).next_to(steps_, DOWN, buff=0.35)
        items = [(r"GPT-style", pg, DECODER), (r"BERT-style", pb, ENCODER)]
        W, H = 1.3, 3.0
        mx = max(pg, pb, 1 / nc) * 1.25
        bars = VGroup()
        for i, (nm, v, col) in enumerate(items):
            b = Rectangle(width=W, height=max(H * v / mx, 0.02), stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([-1.2 + 2.4 * i, -2.9, 0], aligned_edge=DOWN)
            t = label(rf"${pct(v)}\%$", font_size=28, color=col).next_to(b, UP, buff=0.1)
            n_ = label(nm, font_size=22, color=col).next_to(b, DOWN, buff=0.12)
            bars.add(VGroup(b, t, n_))
        chance = DashedLine([-2.4, -2.9 + H / mx / nc, 0], [2.4, -2.9 + H / mx / nc, 0], color=GREY_B, dash_length=0.06)
        cl = label(rf"chance: \ ${100 / nc:.1f}\%$", font_size=18, color=GREY_B).next_to(chance, RIGHT, buff=0.1)
        if pb > pg + 0.02:
            verdict = (f"The BERT-style model's features name the book {pct(pb)} percent of the time, against "
                       f"{pct(pg)} for the GPT-style model's: on a GLUE-style test, bidirectional features win again.")
        elif pg > pb + 0.02:
            verdict = (f"Here the GPT-style model's features do better, {pct(pg)} percent against {pct(pb)}: at our "
                       "small scale, learning from every token seems to matter more than seeing both ways.")
        else:
            verdict = (f"The two are about equal, {pct(pg)} and {pct(pb)} percent: on this test, at this scale, the "
                       "objective hardly matters.")
        with self.voiceover(
            "Task two is the kind of test GLUE was made of: classify a sentence. Which of the thirty novels is it "
            "from? <bookmark mark='a'/> Freeze each model, run a sentence through it, average its final states over "
            "the sentence, and train the same simple linear classifier on top, for each model the same way. "
            f"<bookmark mark='b'/> Chance is {100 / nc:.1f} percent. <bookmark mark='c'/> " + verdict
        ) as vo:
            self.play(LaggedStart(*[AnimationGroup(FadeIn(s_), *([GrowArrow(arrows[i - 1])] if i else []))
                                    for i, s_ in enumerate(steps_)], lag_ratio=0.5), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(info))
            vo.wait_until("b")
            self.play(Create(chance), FadeIn(cl))
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1]), FadeIn(b[2])) for b in bars],
                                  lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def writing(self):
        L, S = load("lineage"), load("scoreboard")
        prompt = data_text("The door opened, and", font=MONO, font_size=22, color=GREY_A).move_to([0, 2.9, 0])
        gw = VGroup(label(r"GPT-style, \ sampling the next token", font_size=22, color=DECODER),
                    said(L["gpt_sample"], chars=40, font_size=20, max_lines=3, box_color=DECODER)).arrange(DOWN, buff=0.15)
        bw = VGroup(label(r"BERT-style, \ filling a mask at the end, \ again and again", font_size=22, color=ENCODER),
                    said(L["bert_sample"], chars=40, font_size=20, max_lines=3, box_color=ENCODER)).arrange(DOWN, buff=0.15)
        VGroup(gw, bw).arrange(RIGHT, buff=0.6, aligned_edge=UP).move_to([0, 1.3, 0])
        ours = {r["name"]: r for r in S["ours"]}["gpt_m"]
        rows = [dict(label=r["label"], bits=r["bits"], kind=r["kind"]) for r in S["rows"]]
        if "base" in S:
            rows.append(dict(label=rf"the series' model, \ ${S['base']['params'] / 1e6:.1f}$M", bits=S["base"]["bits"],
                             kind="lm"))
        rows.append(dict(label=rf"our GPT-style model, \ ${ours['params'] / 1e6:.1f}$M", bits=ours["bits"], kind="lm"))
        board = scoreboard(rows, highlight=(len(rows) - 1,), max_bits=6.0, row_h=0.46, font_size=20, bar_width=5.0,
                           label_width=3.8).scale(0.9)
        board.move_to([-1.3, -1.7, 0])
        bl = label(r"bits per character on the scoreboard's passage", font_size=20, color=GREY_B).next_to(board, UP, buff=0.1)
        nob = label(r"our BERT-style model: \\ no row \\ (its guesses don't multiply \\ into a probability of text)",
                    font_size=18, color=ENCODER).next_to(board, RIGHT, buff=0.4)
        tw = take_away(r"a model of $p(\text{text})$ can be sampled, scored and prompted: \ one model does it all",
                       color=DECODER, font_size=24)
        with self.voiceover(
            "And the task only one of them can really do: write. <bookmark mark='a'/> Given the opening, the "
            "GPT-style model samples one token after another. <bookmark mark='b'/> The BERT-style model can be made to "
            "write by putting a mask at the end and filling it, again and again, but it was never trained to guess a "
            "word with nothing after it. <bookmark mark='c'/> And only the causal model gives a probability to a "
            "whole text, by the chain rule of Part 1, so only it joins the scoreboard: on the Maltese Falcon passage, "
            f"{ours['bits']:.2f} bits per character. A masked model's guesses don't multiply into the probability of "
            "a text, so it has no row. <bookmark mark='d'/> That is the deeper reason the decoder won. A model of the "
            "probability of text can be sampled, scored and prompted: one model does everything, and it gets better "
            "with scale."
        ) as vo:
            self.play(FadeIn(prompt))
            vo.wait_until("a")
            self.play(FadeIn(gw, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(bw, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(board), FadeIn(bl))
            self.play(FadeIn(nob))
            vo.wait_until("d")
            self.play(FadeIn(tw))
        self.wait(0.3)
        self.clear_scene()

