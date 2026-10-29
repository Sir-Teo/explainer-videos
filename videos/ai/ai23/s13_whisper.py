from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai23.common import MONO, PART, SND_C, TEXT_C, load, node_box, spectro, spread_rows, token_chips


class Whisper(VoiceoverScene):
    def construct(self):
        self.card()
        self.roads()
        self.design()
        self.measured()
        self.today()

    def card(self):
        card = chapter_card(12, r"Listening at scale", r"What does a recognizer learn from 680{,}000 hours?", part=PART)
        with self.voiceover("Chapter twelve. Listening at scale."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def roads(self):
        left = VGroup(label(r"self-supervised", font_size=30, color=C.CONTEXT),
                      label(r"wav2vec 2.0 \ (Facebook, 2020)", font_size=24, color=GREY_A),
                      label(r"hide stretches of the speech's latent frames; \\ pick the true one, \ quantized, \ "
                            r"from distractors \\ (Part 24's contrastive loss)", font_size=20, color=GREY_A),
                      label(r"with $53{,}000$ unlabelled hours, \\ $10$ minutes of transcripts: \ $4.8\%$ / $8.2\%$ "
                            r"word errors \\ (LibriSpeech clean / other)", font_size=20, color=C.CONTEXT))
        left.arrange(DOWN, aligned_edge=LEFT, buff=0.26).scale(1.2).move_to([-3.4, 0.2, 0])
        right = VGroup(label(r"weakly supervised", font_size=30, color=SND_C),
                       label(r"Whisper \ (OpenAI, 2022)", font_size=24, color=GREY_A),
                       label(r"$680{,}000$ hours of audio with transcripts \\ found on the web, \ imperfect ones "
                             r"included", font_size=20, color=GREY_A),
                       label(r"one model: \ transcribe, \ translate, \\ name the language, \ time the words; \\ "
                             r"nearly a hundred languages", font_size=20, color=SND_C))
        right.arrange(DOWN, aligned_edge=LEFT, buff=0.26).scale(1.2).move_to([3.4, 0.2, 0])
        div = Line([0, 2.6, 0], [0, -2.4, 0], color=GREY_D)
        cite_ = cite(r"A.~Baevski et al.\ (2020); \ A.~Radford et al., \textit{Robust Speech Recognition via Large-Scale "
                     r"Weak Supervision} (2022)", corner=DR)
        with self.voiceover(
            "After Deep Speech, two roads led to the recognizers we use today. <bookmark mark='a'/> One was "
            "self-supervision. Facebook's wav2vec 2.0, in 2020, hid stretches of speech from its own transformer and learned "
            "to pick the true hidden frame out of distractors, Part 24's contrastive loss applied to sound. "
            "Pretrained on 53,000 hours with no transcripts, then fine-tuned on just ten minutes with them, it got "
            "4.8 and 8.2 percent of the words wrong on the two halves of a standard benchmark. <bookmark mark='b'/> "
            "The other road was weak supervision. In December 2022 OpenAI's Whisper trained on 680,000 hours of "
            "audio paired with transcripts found on the web, imperfect ones and all, one model that transcribes, "
            "translates, names the language and times the words, in nearly a hundred languages."
        ) as vo:
            self.play(Create(div), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in left], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in right], lag_ratio=0.4), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def design(self):
        w = load("whisper")
        M = np.asarray(w["example_mel"])
        mel = spectro(M, 5.2, 1.7, lo=M.min(), hi=M.max()).move_to([-3.5, 1.9, 0])
        ml = label(rf"the input: \ $80$ log-mel bands, \ ${float(w['example_seconds']):.1f}$ s of a held-out voice \\ "
                   r"(padded to $30$ s)", font_size=20, color=SND_C).next_to(mel, UP, buff=0.1)
        enc = node_box(rf"encoder: \ ${int(w['enc_layers'])}$ layers", SND_C, font_size=22).move_to([-3.5, -0.2, 0])
        dec = node_box(rf"decoder: \ ${int(w['dec_layers'])}$ layers, \\ writes tokens", TEXT_C, font_size=22).move_to([1.4, -0.2, 0])
        a1 = Arrow(mel.get_bottom(), enc.get_top(), buff=0.1, color=GREY_B)
        a2 = Arrow(enc.get_right(), dec.get_left(), buff=0.1, color=GREY_B)
        a2l = label(r"cross-attention", font_size=18, color=GREY_B).next_to(a2, UP, buff=0.05)
        toks = [str(t) for t in w["example_tokens"]]
        toks = [t.replace("Ġ", " ") for t in toks]
        chips = token_chips(toks, font_size=18, height=0.38, buff=0.04)
        if chips.width > 13.0:
            chips.width = 13.0
        chips.move_to([0, -2.1, 0])
        cl = label(r"what it writes, \ token by token \ (GPT-2's byte-level BPE, \ plus task tokens)", font_size=20,
                   color=TEXT_C).next_to(chips, UP, buff=0.12)
        par = label(rf"Whisper base.en: \ ${int(w['params']) / 1e6:.0f}$ million parameters, \ width "
                    rf"${int(w['d_model'])}$", font_size=22, color=GREY_A).move_to([4.0, 1.9, 0])
        with self.voiceover(
            "Whisper is a plain encoder-decoder transformer, the shape of Part 14's translation model. "
            "<bookmark mark='a'/> Its input is chapter eight's picture: 80 log-mel bands every ten milliseconds, "
            "always thirty seconds long, padded with silence. <bookmark mark='b'/> The encoder reads it; the decoder "
            "writes the transcript one token at a time, with GPT-2's byte-level BPE, attending back to the sound. "
            "<bookmark mark='c'/> Special tokens at the start say what to do: here, start of transcript, no "
            "timestamps. A recognizer has become a language model that listens. <bookmark mark='d'/> We ran the "
            f"smallest English model, base.en, {int(w['params']) / 1e6:.0f} million parameters, from the Hugging Face cache."
        ) as vo:
            self.play(FadeIn(mel), FadeIn(ml), FadeIn(par))
            vo.wait_until("b")
            self.play(GrowArrow(a1), FadeIn(enc), GrowArrow(a2), FadeIn(a2l), FadeIn(dec))
            vo.wait_until("c")
            self.play(FadeIn(cl), LaggedStart(*[FadeIn(c_, shift=UP * 0.1) for c_ in chips], lag_ratio=0.08), run_time=2.0)
            vo.wait_until("d")
            self.play(Indicate(par, color=WHITE))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        w = load("whisper")
        c = load("ctc")
        errs = [(str(r), str(h)) for r, h in w["errors"]][:3]
        rows = spread_rows([(r"Whisper: \ sentences", SND_C, [100 * float(w["wer"])]),
                            (r"Whisper: \ digit strings", SND_C, [100 * float(w["digit_wer"])]),
                            (r"our CTC model: \ digit strings", C.MODEL_Q, 100 * np.asarray(c["wer"], float))],
                           x_max=max(10.0, 100 * max(float(w["wer"]), float(w["digit_wer"]), float(np.max(c["wer"]))) * 1.2),
                           width=3.6, font_size=20, label_w=3.4, fmt="{:.1f}")
        rows.move_to([-1.2, 1.6, 0])
        rl = label(r"word error rate on the two held-out Kokoro voices, \ $\%$", font_size=20, color=GREY_A).next_to(rows, UP, buff=0.2)
        eg = VGroup(label(r"where Whisper went wrong:" if errs else r"no errors on these sentences", font_size=20, color=GREY_A))
        for r, h in errs:
            eg.add(VGroup(data_text("said:  " + r[:64], font="DejaVu Sans", font_size=16, color=GREY_A),
                          data_text("heard: " + h[:64], font="DejaVu Sans", font_size=16, color=C.SURPRISE))
                   .arrange(DOWN, aligned_edge=LEFT, buff=0.06))
        eg.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([0, -1.8, 0])
        if eg.width > 13:
            eg.width = 13
        ws, wd, cw = float(w["wer"]), float(w["digit_wer"]), float(np.mean(c["wer"]))
        cmp_ = ("our tiny specialist does better on its own task" if cw < wd - 0.005 else
                "Whisper does better even on our model's own task" if wd < cw - 0.005 else
                "the two come out about the same on digits")
        with self.voiceover(
            f"How does it do on our voices? <bookmark mark='a'/> On {int(w['n_sents'])} sentences from the two "
            f"held-out Kokoro voices, it gets {100 * ws:.1f} percent of the words wrong. <bookmark mark='b'/> On the "
            f"{int(w['n_strings'])} digit strings, {100 * wd:.1f} percent, counting its numerals as words, against "
            f"{100 * cw:.1f} for our CTC recognizer, trained on nothing but digits: {cmp_}. "
            "<bookmark mark='c'/> Its mistakes are telling: a rare name or an odd word replaced by a likelier one. The "
            "decoder is a language model, and it guesses."
        ) as vo:
            self.play(FadeIn(rl), FadeIn(rows.rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows.rows[1]), FadeIn(rows.rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(eg))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def today(self):
        items = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"2023: \ Whisper large-v3, \ $1.55$ billion parameters", SND_C),
            (r"2024: \ large-v3-turbo: \ $4$ decoder layers instead of $32$", SND_C),
            (r"2026: \ Qwen3-ASR (Alibaba): \ $52$ languages and dialects, \ built on Qwen3-Omni", SND_C))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35).scale(1.15).move_to(UP * 1.3)
        loop = VGroup(node_box(r"the narrator \\ speaks a sentence", C.MODEL_Q, font_size=22),
                      node_box(r"Qwen3-ASR \\ transcribes it", SND_C, font_size=22),
                      node_box(r"too different? \\ take it again", C.SURPRISE, font_size=22),
                      node_box(r"a forced aligner \\ times every word", C.INTERVAL, font_size=22)).arrange(RIGHT, buff=0.6)
        loop.move_to(DOWN * 1.4)
        if loop.width > 13:
            loop.width = 13
        arr = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=2.5) for a, b in zip(loop, loop[1:])])
        ll = label(r"how this series is narrated \ (tools/tts\_server.py)", font_size=20, color=GREY_A).next_to(loop, UP, buff=0.2)
        cite_ = cite(r"Qwen Team, \textit{Qwen3-ASR Technical Report} (2026)", corner=DR)
        with self.voiceover(
            "Recognizers kept growing and getting faster: Whisper large-v3 in 2023, and a turbo version that cut "
            "its decoder from 32 layers to 4. <bookmark mark='a'/> In January 2026 Alibaba's Qwen3-ASR, built on an "
            "omni model, covered 52 languages and dialects. <bookmark mark='b'/> It also works on this series. Every "
            "sentence the narrator speaks is transcribed by Qwen3-ASR and spoken again if the transcript doesn't "
            "match the script, and a forced aligner times each word, which is how the animations know when to move."
        ) as vo:
            self.play(FadeIn(items[0]), FadeIn(items[1]))
            vo.wait_until("a")
            self.play(FadeIn(items[2]), FadeIn(cite_))
            vo.wait_until("b")
            self.play(FadeIn(ll), LaggedStart(*[FadeIn(b_) for b_ in loop], lag_ratio=0.4),
                      LaggedStart(*[GrowArrow(a_) for a_ in arr], lag_ratio=0.4), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()
