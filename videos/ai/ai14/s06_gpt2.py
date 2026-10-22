from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import (DECODER, ENCDEC, MONO, PART, PRIOR, F, human, said, take_away)


class GPT2(VoiceoverScene):
    def construct(self):
        self.card()
        self.webtext()
        self.prompts()
        self.results()
        self.release()

    def card(self):
        card = chapter_card(5, r"Unsupervised multitask learners",
                            r"Can a language model do tasks it was never trained for?", lit=(2019,), part=PART)
        with self.voiceover("Chapter five. Language models are unsupervised multitask learners."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def webtext(self):
        G = F.GPT2
        hc = history_card(2019, r"GPT-2 \ (Radford, Wu, Child, Luan, Amodei \& Sutskever; OpenAI)",
                          r"a bet: \ a big enough model of varied enough text learns tasks without being told",
                          width=8.6, color=DECODER).to_edge(UP, buff=0.3)
        # the funnel: links -> documents -> gigabytes
        steps = [(rf"${G['links'] / 1e6:.0f}$ million links \\ shared on Reddit, \ $\ge {G['karma']}$ karma", 4.6, PRIOR),
                 (rf"${G['docs'] / 1e6:.0f}$ million documents \\ cleaned, de-duplicated", 3.4, C.DATA),
                 (rf"${G['gb']}$ GB of text: \ WebText", 2.4, C.DATA)]
        fun = VGroup()
        for t, w, c in steps:
            box = RoundedRectangle(width=w, height=0.9, corner_radius=0.12, stroke_color=c, stroke_width=2,
                                   fill_color=c, fill_opacity=0.12)
            tx = label(t, font_size=20, color=c)
            if tx.width > w - 0.2:
                tx.width = w - 0.2
            fun.add(VGroup(box, tx.move_to(box)))
        fun.arrange(DOWN, buff=0.25).move_to([-3.6, -1.1, 0])
        # the four sizes: layers x width
        sizes = G["sizes"]
        bars = VGroup()
        for i, (nm, L, d) in enumerate(sizes):
            r = Rectangle(width=d / 1600 * 3.6, height=L / 48 * 2.6, stroke_color=DECODER, stroke_width=2,
                          fill_color=DECODER, fill_opacity=0.12 + 0.12 * i)
            bars.add(r)
        for r in bars:
            r.move_to([1.2, -2.9, 0], aligned_edge=DL)
        tags = VGroup(*[label(rf"{nm} \ ({L} layers $\times$ {d})", font_size=18, color=DECODER)
                        .next_to(bars[-1], RIGHT, buff=0.15).set_y(r.get_top()[1] - 0.12) for (nm, L, d), r in
                        zip(sizes, bars)])
        sz = label(r"four sizes: \ layers (height) $\times$ width", font_size=22, color=GREY_A).next_to(bars, UP, buff=0.3)
        sz.align_to(bars, LEFT)
        with self.voiceover(
            "February 2019. Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei and Ilya Sutskever, at "
            "OpenAI. Their bet: a big enough language model, trained on varied enough text, would learn tasks without "
            "being told, because the web is full of tasks being done. <bookmark mark='a'/> To get varied text of decent "
            "quality, they took every outbound link from Reddit that had earned at least three karma, about forty-five "
            "million links. After cleaning and removing duplicates: eight million documents, forty gigabytes of text. "
            "<bookmark mark='b'/> The model was GPT-1, scaled up, with layer normalization moved to the input of each "
            "block and a context of 1,024 tokens. Four sizes, the largest forty-eight layers deep and 1,600 wide: one "
            "and a half billion parameters."
        ) as vo:
            self.play(FadeIn(hc, shift=DOWN * 0.15), FadeIn(fun[0], shift=DOWN * 0.15))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f, shift=DOWN * 0.15) for f in fun[1:]], lag_ratio=0.5), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(sz), LaggedStart(*[AnimationGroup(GrowFromEdge(b, DL), FadeIn(t)) for b, t in
                                                zip(bars, tags)], lag_ratio=0.4), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def prompts(self):
        G = F.GPT2
        rows = VGroup(
            VGroup(label(r"summarize", font_size=24, color=DECODER),
                   said("...[a news article]... TL;DR:", chars=40, font_size=19)),
            VGroup(label(r"translate", font_size=24, color=DECODER),
                   said("english sentence = french sentence ... english sentence =", chars=40, font_size=19)),
            VGroup(label(r"answer", font_size=24, color=DECODER),
                   said("...[a passage]... Q: ... A: ... Q: ... A:", chars=40, font_size=19)),
        )
        for r in rows:
            r.arrange(RIGHT, buff=0.4)
            r[0].set_x(-4.6)
            r[1].next_to(r[0], RIGHT, buff=0.45).align_to(rows[0][0], LEFT).shift(RIGHT * 2.0)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(UP * 0.6)
        key = label(r"no fine-tuning: \ the task is written into the text", font_size=28, color=WHITE)
        key.to_edge(DOWN, buff=1.4)
        res = label(rf"reading comprehension: \ ${G['coqa_f1']}$ F1, \ as good as $3$ of $4$ systems trained on "
                    rf"${G['coqa_pairs']:,}$ answers".replace(",", "{,}"), font_size=22, color=GREY_A)
        res.next_to(key, DOWN, buff=0.3)
        tag = note(r"prompt formats from Radford et al.\ (2019), Secs.\ 3.5--3.7").to_corner(DR, buff=0.2)
        idea = label(r"a task is text with a pattern: \ continue the pattern", font_size=32, color=DECODER)
        idea.to_edge(UP, buff=0.5)
        with self.voiceover(
            "The idea is that a task is just text with a pattern, and a good enough predictor will continue the "
            "pattern. <bookmark mark='a'/> To summarize an article, put 'TL;DR:' after it, the way people on the "
            "internet do, and let the model write. <bookmark mark='b'/> To translate, show a few lines of the form "
            "'english sentence equals french sentence', then an English sentence and an equals sign. "
            "<bookmark mark='c'/> To answer questions about a passage, write the passage, the conversation so far, "
            "and 'A:'. <bookmark mark='d'/> Nothing is fine-tuned; the task lives in the prompt. On a reading "
            f"comprehension test, that got {G['coqa_f1']} F1, matching three of four systems trained on more than a "
            "hundred thousand human answers."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(idea))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(key), FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        G = F.GPT2
        params = [117e6, 345e6, 762e6, 1542e6]
        acc = G["lambada_acc"]
        g = axes([8, 9.4], [40, 70], x_length=6.4, y_length=4.0, xlabel=r"parameters \ (log scale)",
                 ylabel=r"LAMBADA accuracy, \ zero-shot", xticks=[8, 9], yticks=[40, 50, 60, 70],
                 xfmt=lambda v: rf"10^{{{int(v)}}}", yfmt=lambda v: rf"{int(v)}\%", center=[-2.6, -0.3, 0])
        ax = g.ax
        sota = DashedLine(ax.c2p(8, G["lambada_sota"]), ax.c2p(9.4, G["lambada_sota"]), color=PRIOR, dash_length=0.08)
        sl = label(rf"previous best: \ ${G['lambada_sota']}\%$", font_size=18, color=PRIOR)
        sl.next_to(sota, DOWN, buff=0.08).align_to(sota, LEFT).shift(RIGHT * 0.1)
        pts = [ax.c2p(math.log10(p), a) for p, a in zip(params, acc)]
        line = VMobject(color=DECODER, stroke_width=4).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.08, color=DECODER) for p in pts])
        vals = VGroup(*[MathTex(rf"{a:.0f}\%", font_size=22, color=DECODER).next_to(d, UL, buff=0.05)
                        for a, d in zip(acc, dots)])
        side = VGroup(
            label(rf"records on ${G['sota_lm']}$ of ${G['lm_sets']}$ language-modelling benchmarks, \\ with no "
                  r"training on any of them", font_size=22, color=WHITE),
            label(rf"Wikipedia, by character: \ ${G['enwik8_bpb']}$ bits per byte", font_size=22, color=C.BITS),
            label(rf"translation: \ ${G['bleu_en_fr']}$ BLEU English $\to$ French, \\ ${G['bleu_fr_en']}$ French $\to$ "
                  r"English: \ poor, \ but rising with size", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.9, 0.3, 0])
        lam = note(r"LAMBADA: \ guess a passage's last word, \ which needs the whole passage").to_edge(UP, buff=0.3)
        cite_ = cite(r"Radford et al.\ (2019), Tables 2--3, Sec.\ 3.7")
        with self.voiceover(
            "With no task-specific training at all, the largest model set records on seven of eight "
            "language-modelling benchmarks. <bookmark mark='a'/> The cleanest picture is LAMBADA, where the last word "
            "of a passage can only be guessed from the whole passage. Accuracy climbs with size: "
            f"{acc[0]:.0f}, {acc[1]:.0f}, {acc[2]:.0f}, {acc[3]:.0f} percent, <bookmark mark='b'/> the last above the "
            f"previous best of {G['lambada_sota']:.0f}, set by models built for this test. <bookmark mark='c'/> On "
            f"Wikipedia, character by character, it reached {G['enwik8_bpb']} bits per byte, a number from the family "
            "of our scoreboard. Its translations were still poor. But almost everything improved steadily with size, "
            "and that trend was the real result."
        ) as vo:
            self.play(FadeIn(g), FadeIn(lam), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Create(line), LaggedStart(*[FadeIn(d, scale=1.5) for d in dots], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(v) for v in vals], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(sota), FadeIn(sl))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(s, shift=LEFT * 0.1) for s in side], lag_ratio=0.5), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def release(self):
        G = F.GPT2
        xs = np.linspace(-4.8, 4.8, len(G["release"]))
        line = Line([xs[0] - 0.6, 0.6, 0], [xs[-1] + 0.6, 0.6, 0], color=GREY_C, stroke_width=2)
        marks = VGroup()
        for (when, size), x in zip(G["release"], xs):
            d = Dot([x, 0.6, 0], radius=0.1, color=DECODER)
            w = label(when, font_size=24, color=GREY_A).next_to(d, UP, buff=0.25)
            s = label(size, font_size=34, color=DECODER).next_to(d, DOWN, buff=0.3)
            marks.add(VGroup(d, w, s))
        head = label(r"a staged release", font_size=34, color=WHITE).to_edge(UP, buff=0.7)
        card = label(r"November 2019: \ the full model, \ with a \emph{model card}: \ intended uses, \ limitations, "
                     r"\ biases", font_size=24, color=GREY_A).move_to(DOWN * 1.4)
        tw = take_away(r"one model trained only to predict text can be pointed at many tasks; \ next: \ make it much "
                       r"bigger", color=DECODER, font_size=26)
        cite_ = cite(r"OpenAI, \textit{Better Language Models and Their Implications} (14 February 2019); \ "
                     r"openai/gpt-2: \ model card (November 2019)")
        why_ = label(r"February 2019: \ the smallest model only, \\ citing concerns about malicious applications",
                     font_size=24, color=GREY_A).move_to(DOWN * 1.4)
        with self.voiceover(
            "OpenAI did not release the largest model at first. Citing the risk of misuse, such as fake news written "
            "at scale, it published the smallest version in February, <bookmark mark='a'/> larger ones in May and "
            "August, and the full one and a half billion parameters in November 2019, <bookmark mark='b'/> with a "
            "model card describing what it was for, where it failed, and the biases of its training text. The debate "
            "it started, about when to release a model's weights, has never stopped; Part 31 returns to it. "
            "<bookmark mark='c'/> The paper's lasting lesson was simpler: one model, trained only to predict text, can "
            "be pointed at many tasks. The obvious next step was to make it much bigger."
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(marks[0]), FadeIn(cite_))
            self.play(FadeIn(why_))
            vo.wait_until("a")
            self.play(FadeIn(marks[1]), FadeIn(marks[2]), lag_ratio=0.5)
            vo.wait_until("b")
            self.play(FadeIn(marks[3]), FadeOut(why_), FadeIn(card))
            vo.wait_until("c")
            self.play(FadeIn(tw))
        self.wait(0.3)
        self.clear_scene()
