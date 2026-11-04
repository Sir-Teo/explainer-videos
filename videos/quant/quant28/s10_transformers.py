from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant28.common import HURDLE, MODEL_A, MODEL_B, MODEL_C, PART, WORD, comma, fit_right, load


class Transformers(VoiceoverScene):
    def construct(self):
        m = load("lm")
        self.card()
        self.attention()
        self.finbert()
        self.pocket(m)
        self.replay(m)
        self.question()

    def card(self):
        c = chapter_card(9, r"Transformers and FinBERT", r"What does a model gain by reading the whole sentence at once?",
                         part=PART)
        with self.voiceover("Chapter nine. An embedding gives each word one vector, whatever sentence it is in. Will "
                            "not hesitate to tighten and will not tighten mean opposite things with nearly the same words. "
                            "What does a model gain by reading the whole sentence at once?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def attention(self):
        words = [r"the", r"Committee", r"will", r"not", r"hesitate", r"to", r"tighten"]
        chips = VGroup(*[label(rf"\texttt{{{w}}}", font_size=26, color=WORD) for w in words]).arrange(RIGHT, buff=0.35)
        chips.shift(UP * 0.4)
        tgt = 6
        weights = [0.02, 0.06, 0.12, 0.34, 0.30, 0.04, 0.12]
        arcs = VGroup(*[ArcBetweenPoints(chips[k].get_top() + UP * 0.05, chips[tgt].get_top() + UP * 0.05, angle=-PI / 2.2,
                                         color=HURDLE, stroke_width=1 + 14 * w, stroke_opacity=0.35 + w)
                        for k, w in enumerate(weights) if k != tgt])
        rows = [cmath(r"\mathrm{Attn}(Q, K, V)", r"=", r"\operatorname{softmax}\Big(\frac{QK^\top}{\sqrt{d}}\Big) V", font_size=32,
                      colors={r"\mathrm{Attn}(Q, K, V)": HURDLE})]
        eq = rows[0].to_edge(DOWN, buff=1.2)
        note_ = wrapped_label(r"each word's vector is rebuilt as a weighted average of the others: \emph{tighten} next "
                              r"to \emph{not hesitate} is a different vector from \emph{tighten} next to \emph{not}. "
                              r"Weights here are illustrative", 10.6, 18, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The answer of the last decade is attention, which the AI series builds from scratch. "
            "<bookmark mark='a'/> To represent the word tighten, the model looks back at every other word in the "
            "sentence and decides how much each one matters: here, not and hesitate matter a lot. "
            "<bookmark mark='b'/> The new vector for tighten is a weighted average of the others, so the same word "
            "gets a different meaning in every sentence. Stack dozens of these layers and train on enough text, and "
            "you have a transformer: BERT, GPT and every model since."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c_) for c_ in chips], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(a_) for a_ in arcs], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(eq), FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def finbert(self):
        card = firm_card(r"Huang, Wang and Yang (2023)", r"`FinBERT: a large language model for extracting information "
                         r"from financial text': BERT pretrained on 4.9 billion tokens of 10-Ks and 10-Qs, earnings call "
                         r"transcripts and analyst reports, then fine-tuned on 10{,}000 analyst-report sentences labelled "
                         r"by hand",
                         numbers=((r">", r"beats the Loughran--McDonald dictionary and other machine-learning methods "
                                         r"on sentiment"),
                                  (r"\checkmark", r"largest gains on sentences the others call neutral, and with little "
                                                  r"training data"),
                                  (r"18\%", r"other methods understate the information in earnings calls by at least this "
                                            r"much")),
                         source=r"\textit{Contemporary Accounting Research} 40 (2023)", kind=r"Paper file", width=10.6,
                         font_size=21).move_to(ORIGIN)
        with self.voiceover(
            "Finance's own transformer came from accounting. <bookmark mark='a'/> Allen Huang, Hui Wang and Yi Yang "
            "pretrained BERT on four point nine billion tokens of filings, earnings calls and analyst reports, then "
            "fine-tuned it on ten thousand analyst sentences labelled by hand. <bookmark mark='b'/> It beat the "
            "dictionary and the older machine-learning methods, most of all on sentences the others called neutral, "
            "and it needed little labelled data to do it. Measured with it, earnings calls carry at least eighteen "
            "percent more information than the older methods could see."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def pocket(self, m):
        cfg = m["cfg"]
        sl = m["slices"]
        n_par = sl["A"]["params"]["total"]
        rows = [cmath(r"\text{tokens}", r":", rf"\text{{byte-pair encoding, {cfg['vocab']:,} pieces, learned from the "
                      r"training text only}}".replace(",", "{,}"), font_size=28),
                cmath(r"\text{model}", r":", rf"{cfg['layers']}\ \text{{layers}},\ d = {cfg['d']},\ {cfg['heads']}\ "
                      rf"\text{{heads}},\ \text{{context}}\ {cfg['seq']},\ {n_par / 1e6:.1f}\text{{m parameters}}", font_size=28),
                cmath(r"\text{trained}", r":", rf"{m['tokens'] / 1e6:.0f}\text{{m tokens, next-token prediction, on a laptop "
                      r"CPU}}", font_size=28)]
        whys = [why(r"Part 1 of the AI series: pieces of words, merged by frequency. A point-in-time tokenizer cannot "
                    r"know words that did not exist yet"),
                why(r"a modern decoder: RMSNorm, rotary positions, SwiGLU (the House's \texttt{explainer.lm.pocket})"),
                why(r"about a hundred-thousandth of BloombergGPT; enough to learn the committee's prose")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "We cannot train FinBERT here, but we can train its little cousin, the way the AI series does. "
            "<bookmark mark='a'/> Pieces of words learned by byte-pair encoding, from the training text only, so a "
            "tokenizer trained on 2007 text has never seen the word pandemic. <bookmark mark='b'/> A modern decoder "
            f"with {cfg['layers']} layers and {n_par / 1e6:.1f} million parameters. <bookmark mark='c'/> Trained to "
            f"predict the next token, on {m['tokens'] / 1e6:.0f} million tokens of FOMC minutes, on an ordinary CPU. "
            "Three copies of it, trained on three different slices of history, are the next chapter's experiment."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def replay(self, m):
        a = m["slices"]["A"]
        cur = np.asarray(a["curve"], float)
        steps, loss = cur[:, 0], cur[:, 1]
        ev = np.asarray(a["evals"], float)
        samples = load("lookahead")["A"]["samples"]

        ck = [int(steps[0]), int(steps[len(steps) // 3]), int(steps[2 * len(steps) // 3]), int(steps[-1])]
        txt = samples[0][:150]
        for ch, rep in (("\\", ""), ("_", r"\_"), ("%", r"\%"), ("$", r"\$"), ("&", r"\&"), ("#", r"\#"), ("{", ""), ("}", "")):
            txt = txt.replace(ch, rep)

        def frame(k):
            e = float(np.interp(ck[k], ev[:, 0], ev[:, 2]))
            g = VGroup(label(r"model A: minutes 1996--2007", font_size=20, color=MODEL_A),
                       MathTex(rf"\text{{loss on 2008--2012 minutes}} = {e:.2f}", font_size=24, color=GREY_A))
            if k == len(ck) - 1:
                g.add(label(r"its continuation of: \emph{In light of the deterioration in financial conditions, the "
                            r"Committee}", font_size=14, color=GREY_B),
                      wrapped_label(r"\texttt{" + txt + r"}", 5.4, 14, GREY_A))
            return g.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        rp = TrainingReplay(steps, loss, frame, checkpoints=ck, ylabel=r"training loss (nats per token)",
                            color=MODEL_A)
        with self.voiceover(
            "Here is the first copy learning. <bookmark mark='a'/> The loss starts near the log of the vocabulary, "
            f"about {np.log(m['cfg']['vocab']):.1f} nats per token, a uniform guess, and falls as it learns spelling, "
            f"then grammar, then the committee's habits, to about {loss[-20:].mean():.1f}. On the left, its loss on the "
            "minutes of 2008 to 2012, which it never sees, falls with it. <bookmark mark='b'/> And at the end, what it "
            "writes when asked to continue a sentence about deteriorating financial conditions. It has never read a "
            "word from after 2007."
        ) as vo:
            self.play(FadeIn(rp))
            vo.wait_until("a")
            rp.play(self, run_time=6)
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"the loss of a model that guesses uniformly over 2{,}048 tokens is $\log 2048$. What is it in "
                       r"nats, and in bits?")
        with self.voiceover(
            "Pause and predict. A model that guesses uniformly over two thousand and forty-eight tokens has a loss of "
            "the log of two thousand and forty-eight. What is that in nats, and in bits?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
