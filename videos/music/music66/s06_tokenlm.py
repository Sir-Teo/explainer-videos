from __future__ import annotations

import numpy as np

from videos.music.music66.common import *  # noqa: F403


class TokenLM(SoundScene):
    def construct(self):
        chapter(self, 5, r"Language models over sound", r"What does a language model write when its words are sound?")
        self.lineage()
        self.delay()
        self.picture_()
        self.training()
        self.heard()
        self.copying()

    # ------------------------------------------------------------------
    def lineage(self):
        items = [
            (r"AudioLM \ (Borsos et al., \ 2022): \ coarse `semantic' tokens first, \ then the codec's fine tokens, \ each by a transformer", WHITE),
            (r"MusicLM \ (Agostinelli et al., \ 2023): \ the same, \ conditioned on text through a joint music-text embedding", WHITE),
            (r"MusicGen \ (Copet et al., \ 2023): \ one transformer over EnCodec's four streams, \ delayed against each other", WHITE),
            (r"trained on tens of thousands of hours: \ the model is the easy part; \ the data is not", TUNE),
        ]
        rows_scene(self, r"tokens in, \ tokens out", items,
                   "With a codec, sound becomes text, and the language models of AI, Built apply. <bookmark mark='b'/> AudioLM, "
                   "from Zalán Borsos and colleagues in 2022, writes coarse tokens that capture content first, then the codec's "
                   "fine tokens, each by a transformer. <bookmark mark='c'/> MusicLM, in 2023, does the same conditioned on text, "
                   "through an embedding shared by music and words. <bookmark mark='d'/> MusicGen, from Jade Copet and colleagues "
                   "that year, uses one transformer over EnCodec's four streams of tokens, each delayed against the last. "
                   "<bookmark mark='e'/> They were trained on tens of thousands of hours of music. The model is the easy part; "
                   "the data is not.", marks="bcde")

    # ------------------------------------------------------------------
    def training(self):
        d = load("tokenlm")
        cv_ = np.array(d["curve"])
        ax = frame_axes(width=7.5, height=3.0, xlo=0, xhi=cv_[:, 0].max(), ylo=0, yhi=cv_[:, 1].max() * 1.05, center=DOWN * 0.5 + LEFT * 1.0)
        cv = curve(cv_[:, 0], cv_[:, 1], ax.to, color=TUNE, width=3)
        stop = DashedLine(ax.to(d["steps"], 0), ax.to(d["steps"], cv_[:, 1].max()), color=EAR, stroke_width=2)
        xl = label(r"training steps", font_size=14, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yl = label(r"loss on tunes set aside \ (nats per token)", font_size=14, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        side = VGroup(label(rf"{d['params']:,} weights", font_size=16, color=WHITE),
                      label(rf"{d['train_tokens']:,} tokens: \ about {d['train_tokens'] / 62.5 / 60:.0f} minutes of piano", font_size=16, color=WHITE),
                      label(rf"kept as it was at step {d['steps']} \ (red)", font_size=16, color=EAR)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(RIGHT, buff=0.4)
        head = label(r"a transformer over codec tokens", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Monochord's version: the pocket transformer of AI, Built, four layers, on the one-token codec's tokens of Part "
            f"65's chorale tunes played on the piano, about {say(round(d['train_tokens'] / 62.5 / 60))} minutes. "
            "<bookmark mark='a'/> Its loss on tunes set aside falls and then turns, as Part 65's did, <bookmark mark='b'/> so it "
            f"is kept as it was at step {say(d['steps'])}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xl), FadeIn(yl), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(Create(cv), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(stop), FadeIn(side[2]))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("tokenlm")
        c = clip("tokenlm.two")
        boxes = choice_boxes([r"the tune, \ through the codec", r"its first 4 s, \ then the model's next 6"], width=4.4, height=0.9, buff=0.8, size=18).move_to(UP * 0.6)
        note = label(r"both decoded by the same one-token codec, \ so the difference is the model's", font_size=17, color=GREY_A).next_to(boxes, DOWN, buff=0.6)
        head = label(r"continued, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear a chorale tune the model never learnt from, through the codec, then its first four seconds continued by the model for six more. Both pass through the same codec, so the difference is the model's."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"true, \ then continued", kind="synthesized", detail=r"Part 38's piano; \ codec tokens", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["true"], st["generated"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["generated"], c.duration, buff=0.08)
        with self.voiceover(
            "After the prompt, listen for what survives. The piano's sound must, since every token is a frame of piano; "
            "whether a tune survives, a line anyone would write down, is for your ear to judge. With forty minutes of data "
            "and under a million weights, texture comes first and structure last; the large models learnt structure from "
            "thousands of hours."
        ):
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def copying(self):
        d = load("tokenlm")
        items = [
            (rf"the longest run of the model's tokens found in its training tokens: \ {d['longest_copy_frames']} frames, \ {d['longest_copy_seconds']:.2f} s", WHITE),
            (r"exact runs are a lower bound: \ a copied melody played a little differently gives different tokens", WHITE),
            (r"large music models have been shown to reproduce training audio closely in some cases; \ checking needs the training data", WHITE),
            (r"so the copying test of Part 65 matters more here, \ and is harder: \ near matches, \ not exact ones", TUNE),
        ]
        rows_scene(self, r"does it copy?", items,
                   "Does it copy? <bookmark mark='b'/> The longest run of its tokens that also occurs in its training tokens is "
                   f"{say(d['longest_copy_frames'])} frames, about {say(d['longest_copy_seconds'], 1)} seconds of piano, copied token for "
                   "token. <bookmark mark='c'/> "
                   "Exact runs are only a lower bound: a copied melody played a little differently gives different tokens. "
                   "<bookmark mark='d'/> Large music models have been shown to reproduce training audio closely in some cases, and "
                   "checking needs the training data. <bookmark mark='e'/> So Part 65's copying test matters more for sound, and "
                   "is harder: it needs near matches, not exact ones.", marks="bcde")

    # ------------------------------------------------------------------
    def picture_(self):
        d = load("tokpic")
        S = np.array(d["spectrum"])
        Q = np.array(d["codebook"])
        a = heat_image(S[::-1], S.max() - 9, S.max(), width=10.0, height=1.8).move_to(UP * 1.2)
        b = heat_image(Q[::-1], S.max() - 9, S.max(), width=10.0, height=1.8).move_to(DOWN * 1.0)
        la = label(r"the tune's log spectrum \ (up to 4 kHz)", font_size=15, color=GREY_A).next_to(a, UP, buff=0.1).align_to(a, LEFT)
        lb = label(r"each frame replaced by its nearest codebook entry", font_size=15, color=GREY_A).next_to(b, UP, buff=0.1).align_to(b, LEFT)
        toks = label(r"tokens: \ " + r"\ ".join(str(t) for t in d["tokens"][:22]) + r" \dots", font_size=15, color=TUNE).to_edge(DOWN, buff=0.35)
        head = label(rf"{bwv(d['tune'])} on the piano, \ as tokens", font_size=24, color=GREY_A).to_edge(UP, buff=0.2)
        with self.voiceover(
            "Here is what the language model reads. <bookmark mark='a'/> A piano tune's spectrum, <bookmark mark='b'/> and "
            "the same with every frame replaced by its nearest entry in the first codebook: blockier, but the notes are all "
            f"there. <bookmark mark='c'/> And the tokens themselves, one number a frame. In {say(d['frames'])} frames this tune "
            f"used {say(d['distinct'])} of the 256 entries."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(la))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(lb))
            vo.wait_until("c")
            self.play(FadeIn(toks))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def delay(self):
        cols = [TUNE, BLUE, EAR, GREY_B]
        g = VGroup()
        for s in range(4):
            row = VGroup()
            for t in range(10):
                box = Square(side_length=0.62, stroke_color=cols[s], stroke_width=2, fill_color=cols[s], fill_opacity=0.25)
                box.move_to([-3.6 + 0.75 * (t + s), 1.2 - 0.85 * s, 0])
                row.add(VGroup(box, label(rf"$t_{{{t}}}$", font_size=14, color=WHITE).move_to(box)))
            g.add(VGroup(label(rf"stream {s + 1}", font_size=16, color=cols[s]).move_to([-5.6, 1.2 - 0.85 * s, 0]), row))
        step = Rectangle(width=0.7, height=3.4, stroke_color=WHITE, stroke_width=2).move_to([-3.6 + 0.75 * 5, 1.2 - 0.85 * 1.5, 0])
        note = label(r"each column is one step of the transformer: \ it writes stream 1 for frame 5, \ stream 2 for frame 4, \ and so on", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.5)
        head = label(r"MusicGen's delay pattern", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How does one transformer write four streams of tokens at once? MusicGen's answer is a delay. <bookmark mark='a'/> "
            "Each stream is shifted one frame later than the one above. <bookmark mark='b'/> At each step the model writes one "
            "token of every stream, but for different frames: the coarse stream for the newest frame, the finer ones for frames "
            "just behind it, whose coarser tokens are already written. Four streams cost one step a frame, not four."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in g], lag_ratio=0.3), run_time=1.8)
            vo.wait_until("b")
            self.play(Create(step), FadeIn(note))
        self.wait(0.6)
        self.clear_scene()
