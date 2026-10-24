from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai27.common import (ASSIST, BASE, GOLD, MONO, PART, PENALTY, POLICY, REWARD, USER, bubble, load,
                                   node_box, said)
from videos.ai.ai27.compute import EVAL_N


class SFT(VoiceoverScene):
    def construct(self):
        self.card()
        self.template()
        self.tasks()
        self.before_after()
        self.curve()
        self.history()

    def card(self):
        card = chapter_card(2, r"Supervised fine-tuning", r"How do you teach a predictor the shape of a conversation?",
                            lit=(2022,), part=PART)
        with self.voiceover("Chapter two. Supervised fine-tuning."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def template(self):
        toks = [("<|user|>", USER, True), ("Who", USER, False), (" wrote", USER, False), (" Dracula", USER, False),
                ("?", USER, False), ("<|assistant|>", ASSIST, True), ("Bram", ASSIST, False), (" Stoker", ASSIST, False),
                (".", ASSIST, False), ("<|end|>", ASSIST, True)]
        chips = VGroup()
        for t, c, sp in toks:
            tx = data_text(t, font=MONO, font_size=22, color=c if sp else WHITE)
            box = RoundedRectangle(width=tx.width + 0.2, height=0.5, corner_radius=0.08, stroke_color=c,
                                   stroke_width=2 if sp else 1, fill_color=c, fill_opacity=0.12 if sp else 0.04)
            chips.add(VGroup(box, tx.move_to(box)))
        chips.arrange(RIGHT, buff=0.08).move_to(UP * 2.0)
        if chips.width > 13.2:
            chips.width = 13.2
        trained = VGroup(*[SurroundingRectangle(chips[i], color=REWARD, buff=0.05, stroke_width=3) for i in (6, 7, 8, 9)])
        tl = label(r"trained on: \ the answer's tokens only", font_size=24, color=REWARD).next_to(chips, DOWN, buff=0.4)
        rows = [
            cmath(r"\mathcal L_{\mathrm{SFT}}(\theta)", r"=", r"-\sum_{t\, \in\, \text{answer}} \log p_\theta(y_t \mid x,\ "
                  r"y_{<t})", font_size=36),
            cmath(r"\mathcal L_{\mathrm{SFT}}(\theta)", r"=", r"-\log p_\theta(y \mid x)", font_size=36),
        ]
        rows[0][0].set_color(ASSIST)
        whys = [why(r"the pretraining loss, \ masked to the answer"), why(r"the chain rule, \ Part 1")]
        step = ladder(self, rows, whys, keep=2, top=0.4, x=-1.4, buff=0.5, edge=6.9)
        reads = label(r"what the model reads", font_size=24, color=GREY_A).next_to(chips, UP, buff=0.3)
        seen = VGroup(bubble(r"Who wrote Dracula?", "user", font_size=26).move_to([-2.6, 0.2, 0]),
                      bubble(r"Bram Stoker.", "assistant", font_size=26).move_to([2.6, -0.9, 0]))
        sees = label(r"what a person sees", font_size=24, color=GREY_A).next_to(seen, DOWN, buff=0.45)
        with self.voiceover(
            "The first step is to teach the model the shape of a conversation. Every exchange is written in a fixed "
            "template, with special tokens that never appear in ordinary text: one that says a person is speaking, "
            "one that says the assistant's turn begins, and one that ends it. <bookmark mark='a'/> The model is "
            "trained on such conversations with the same next-token loss as in pretraining, with one change: only the "
            "answer's tokens count. The question is context, not something to imitate. <bookmark mark='b'/> By the "
            "chain rule of Part 1, the masked loss is just the log-probability of the whole answer given the "
            "question. Supervised fine-tuning is maximum likelihood on the answers people want."
        ) as vo:
            self.play(FadeIn(seen[0]), FadeIn(seen[1]), FadeIn(sees))
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.1) for c_ in chips], lag_ratio=0.08), FadeIn(reads),
                      run_time=2.0)
            for i in (0, 5, 9):
                self.play(Indicate(chips[i], scale_factor=1.15), run_time=0.8)
            vo.wait_until("a")
            self.play(FadeOut(seen), FadeOut(sees))
            self.play(Create(trained), FadeIn(tl))
            step(0)
            vo.wait_until("b")
            step(1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tasks(self):
        d = load("data")
        s0, t0 = d["which_train"][0]
        top, line = d["line_train"][0]
        a = VGroup(label(r"Which book?", font_size=30, color=ASSIST),
                   said(f'Which book is this from? "{s0}"', "user", chars=38, font_size=18),
                   said(t0, chars=38, font_size=18),
                   label(rf"${len(d['which_train']):,}$ examples, \ $30$ titles; \ ${len(d['which_test'])}$ held-out "
                         r"sentences for testing".replace(",", "{,}"), font_size=20, color=GREY_A))
        a.arrange(DOWN, buff=0.25).move_to([-3.4, 0.2, 0])
        a[2].align_to(a[1], RIGHT)
        b = VGroup(label(r"A line about\dots", font_size=30, color=ASSIST),
                   said(f"Write a line about the {top}.", "user", chars=38, font_size=18),
                   said(line, chars=38, font_size=18),
                   label(rf"${len(d['line_train']):,}$ examples, \ $30$ topics".replace(",", "{,}"), font_size=20,
                         color=GREY_A))
        b.arrange(DOWN, buff=0.25).move_to([3.4, 0.2, 0])
        b[2].align_to(b[1], RIGHT)
        tag = note(r"both made from the thirty novels; \ test sentences come from paragraphs the model never read")
        tag.to_edge(DOWN, buff=0.3)
        tot = int(load("lora")["total_params"])
        model = node_box(rf"our model: \ ${tot / 1e6:.1f}$ million parameters, \ trained on thirty novels", BASE,
                         font_size=24).move_to([0, 3.05, 0])
        with self.voiceover(
            "Our model is the one this series trained on thirty novels: six point eight million parameters, a "
            "modern transformer in miniature. <bookmark mark='h'/> We fine-tune it on two kinds of conversation, "
            "both made from the novels themselves. <bookmark mark='a'/> In the first, the user quotes a sentence and asks which book "
            "it comes from; the answer is the title. It's checkable: right or wrong, and we test on sentences from "
            "paragraphs held out of all its training. <bookmark mark='b'/> In the second, the user asks for a line "
            "about something, the sea, a window, and the answer is a sentence from the novels about it."
        ) as vo:
            self.play(FadeIn(model, scale=1.1))
            vo.wait_until("h")
            arrows = VGroup(*[Arrow(model.get_bottom(), h_.get_top(), buff=0.12, color=GREY_B, stroke_width=2.5,
                                    max_tip_length_to_length_ratio=0.12) for h_ in (a[0], b[0])])
            self.play(LaggedStart(*[GrowArrow(r_) for r_ in arrows], lag_ratio=0.3), FadeIn(a[0]), FadeIn(b[0]),
                      FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(a[1:], shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(b[1:], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def before_after(self):
        d = load("sft")
        s, title, base_ans = d["base_answers"][0]
        sft_ans = next((a for s2, t2, a in d["sft_answers"] if s2 == s), d["sft_answers"][0][2])
        q = said(f'Which book is this from? "{s}"', "user", chars=60, font_size=18).move_to([0, 2.5, 0])
        bl = label(r"the base model", font_size=26, color=BASE).move_to([-3.4, 1.1, 0])
        ba = said(base_ans, chars=34, font_size=18, max_lines=5).next_to(bl, DOWN, buff=0.2)
        sl = label(r"after fine-tuning", font_size=26, color=ASSIST).move_to([3.4, 1.1, 0])
        sa = said(sft_ans, chars=34, font_size=18).next_to(sl, DOWN, buff=0.2)
        truth = label(rf"the answer: \ \textit{{{title}}}", font_size=22, color=GOLD).next_to(sa, DOWN, buff=0.3)
        stats = VGroup(
            label(rf"base model: \ ${100 * d['base_which']:.0f}\%$ right", font_size=26, color=BASE),
            label(rf"fine-tuned: \ ${100 * d['sft_which']:.0f}\%$ right", font_size=26, color=ASSIST),
            label(rf"chance: \ ${100 * d['chance']:.1f}\%$", font_size=22, color=GREY_B),
        ).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.6)
        tag = note(rf"computed: \ ${len(load('data')['which_test'])}$ held-out sentences").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Here is a held-out sentence, put to the model before fine-tuning. <bookmark mark='a'/> The base model "
            "has never seen the special tokens in a meaningful place, so it does what it always does: it continues "
            "a novel. <bookmark mark='b'/> After fine-tuning, it answers with a title. <bookmark mark='c'/> On all "
            f"the held-out sentences, the base model is right {100 * d['base_which']:.0f} percent of the time; the "
            f"fine-tuned model {100 * d['sft_which']:.0f} percent, against one in thirty by guessing. It had read "
            "these books; fine-tuning taught it to say which one it was reminded of."
        ) as vo:
            self.play(FadeIn(q), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(bl), FadeIn(ba))
            vo.wait_until("b")
            self.play(FadeIn(sl), FadeIn(sa), FadeIn(truth))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(m) for m in stats], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curve(self):
        d = load("sft")
        ev = np.asarray(d["evals"])
        S = int(ev[-1, 0])
        g = axes([0, S], [0, 1], x_length=6.0, y_length=3.4, xlabel=r"fine-tuning steps",
                 ylabel=r"held-out sentences placed right", xticks=[0, S // 2, S], yticks=[0, 0.5, 1],
                 yfmt=lambda v: rf"{int(100 * v)}\%", center=[-3.2, -0.2, 0])
        pts = [(0.0, float(d["base_which"]))] + [(float(a), float(b)) for a, b in ev]
        line = VMobject().set_points_as_corners([g.ax.c2p(a, b) for a, b in pts]).set_stroke(ASSIST, 4)
        dots = VGroup(*[Dot(g.ax.c2p(a, b), radius=0.06, color=ASSIST) for a, b in pts])
        fg = VGroup(
            label(r"next-token loss on held-out novel text", font_size=24, color=GREY_A),
            label(rf"before: \ ${d['base_heldout']:.3f}$ nats", font_size=26, color=BASE),
            label(rf"after: \ ${d['sft_heldout']:.3f}$ nats", font_size=26, color=PENALTY if d['sft_heldout'] >
                  d['base_heldout'] else ASSIST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.6, 0.6, 0])
        worse = d["sft_heldout"] - d["base_heldout"]
        fl = label(r"forgetting: \ the price of specializing" if worse > 0.002 else
                   r"little forgotten: \ a short, gentle run", font_size=24,
                   color=PENALTY if worse > 0.002 else ASSIST).next_to(fg, DOWN, buff=0.4)
        fl.align_to(fg, LEFT)
        tag = note(rf"computed: \ checked every $100$ steps on an even sample of ${EVAL_N}$ of the "
                   rf"${len(load('data')['which_test'])}$ test sentences").to_corner(DR, buff=0.2)
        with self.voiceover(
            f"Accuracy climbs over the {S} steps of fine-tuning. <bookmark mark='a'/> But something is lost. On "
            f"ordinary novel text, which it was trained to predict, its loss rises from {d['base_heldout']:.3f} to "
            f"{d['sft_heldout']:.3f} nats per token. <bookmark mark='b'/> Fine-tuning moves every weight to serve the "
            "new task, and some of the old skill goes with it. Keeping that loss small is the job of the next "
            "chapter's method, and, in RLHF, of the leash." if worse > 0.002 else
            f"Accuracy climbs over the {S} steps of fine-tuning. <bookmark mark='a'/> Fine-tuning often costs some "
            f"of the old skill, but here the loss on ordinary novel text barely moves, from {d['base_heldout']:.3f} "
            f"to {d['sft_heldout']:.3f} nats per token. <bookmark mark='b'/> A gentle learning rate and a short run "
            "keep the model near where it started; pushing harder would trade away more. Keeping that cost small is "
            "the job of the next chapter's method, and, in RLHF, of the leash."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            self.play(Create(line), LaggedStart(*[FadeIn(p) for p in dots], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(fg, shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(fl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        cards = VGroup(
            history_card(2021, r"FLAN \ (Wei et al., Google)", r"instruction tuning on $60$ tasks phrased as "
                         r"instructions: \ better at tasks it never saw", width=6.2, color=ASSIST),
            history_card(2023, r"Alpaca \ (Stanford)", r"$52$k instructions and answers written by a stronger model: "
                         r"\ a chat model for a few hundred dollars", width=6.2, color=ASSIST),
            history_card(2023, r"LIMA \ (Zhou et al., Meta)", r"$1{,}000$ carefully chosen examples were enough: \ "
                         r"alignment is mostly style; \ the knowledge comes from pretraining", width=6.2, color=GOLD),
            history_card(2024, r"synthetic data", r"most fine-tuning examples are now written or filtered by models, "
                         r"\ checked by people", width=6.2, color=ASSIST),
        ).arrange_in_grid(rows=2, cols=2, buff=0.35).move_to(UP * 0.1)
        cite_ = cite(r"Wei et al.\ (2021); \ Taori et al.\ (2023); \ Zhou et al., \textit{LIMA} (2023)")
        with self.voiceover(
            "Instruction tuning has a short, fast history. <bookmark mark='a'/> In 2021 Google's FLAN fine-tuned a "
            "model on sixty tasks rewritten as instructions, and it got better at tasks it had never seen. "
            "<bookmark mark='b'/> In 2023 Stanford's Alpaca fine-tuned an open model on fifty-two thousand "
            "examples written by a stronger model, for a few hundred dollars. <bookmark mark='c'/> Meta's LIMA "
            "showed that a thousand carefully chosen examples could go a long way, and proposed that alignment is "
            "largely about style: the knowledge is already there from pretraining. <bookmark mark='d'/> Today most "
            "fine-tuning data is written or filtered by models, and checked by people."
        ) as vo:
            self.play(FadeIn(cite_))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()
