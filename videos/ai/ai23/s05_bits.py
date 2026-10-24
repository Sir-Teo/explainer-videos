from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai23.common import LM_COLORS, LM_NAMES, MONO, PART, TEXT_C, load, spread_rows

LM_SAY = {"bytes256": "raw bytes", "bpe1024": "BPE with 1,024 pieces", "bpe4096": "BPE with 4,096 pieces",
          "unigram1024": "the unigram model with 1,024 pieces", "unigram4096": "the unigram model with 4,096 pieces"}


def lm_stats():
    d = load("lms")
    names = [str(n) for n in d["configs"]]
    bpc = {n: np.asarray(d[f"bpc_{n}"], float) for n in names}
    return d, names, bpc


class Bits(VoiceoverScene):
    def construct(self):
        self.card()
        self.units()
        self.race()
        self.replay()
        self.why()

    def card(self):
        card = chapter_card(4, r"What a token is worth", r"How do you compare models that read different tokens?",
                            lit=(1951,), part=PART)
        with self.voiceover("Chapter four. What a token is worth."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def units(self):
        d, names, bpc = lm_stats()
        n = "bpe4096"
        cpt = float(d[f"cpt_{n}"])
        b = float(bpc[n][0])
        bpt = b * cpt
        colors = {r"\text{bits}": C.BITS, r"\text{characters}": TEXT_C, r"\text{tokens}": GREY_A}
        rows = [cmath(r"\text{bits per character}", r"=", r"\frac{\text{total bits}}{\text{total characters}}",
                      font_size=34),
                cmath(r"\text{bits per character}", r"=", r"\frac{\text{total bits} / \text{tokens}}{\text{total characters} / \text{tokens}}",
                      font_size=34),
                cmath(r"\text{bits per character}", r"=", r"\frac{\text{bits per token}}{\text{characters per token}}",
                      font_size=34),
                MathTex(rf"{b:.3f} = \frac{{{bpt:.3f}}}{{{cpt:.3f}}}", font_size=40, color=C.BITS)]
        whys = [why(r"the same surprise, \\ counted per character", font_size=22),
                why(r"divide top and bottom \\ by the number of tokens", font_size=22),
                why(r"the conversion", font_size=22),
                why(r"our $4{,}096$-piece BPE model, \\ on the passage (seed $0$)", font_size=22)]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.6, align_index=None, buff=0.5, edge=6.9)
        with self.voiceover(
            "A tokenizer changes what a model has to guess. A model that predicts bigger tokens has more to guess each "
            "time, so its bits per token can't be compared with a byte model's. <bookmark mark='a'/> The fair "
            "currency is Part 1's bits per character: the text's total surprise, divided by its length. "
            "<bookmark mark='b'/> Divide the top and the bottom by the number of tokens, <bookmark mark='c'/> and bits "
            "per character is bits per token divided by characters per token. <bookmark mark='d'/> Our 4,096-piece "
            f"BPE model pays {bpt:.2f} bits for a token of the scoreboard's passage, and a token covers {cpt:.2f} "
            f"characters: {b:.2f} bits per character."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3, transform=False)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def race(self):
        d, names, bpc = lm_stats()
        cfg = d["cfg"]
        budget = float(d["budget_bytes256"])
        hdr = VGroup(*[label(t, font_size=22, color=GREY_B) for t in (
            r"tokenizer", r"vocabulary", r"FLOPs a token", r"steps", r"characters read")])
        table = VGroup()
        xs = [-4.4, -1.6, 0.6, 2.6, 4.7]
        for j, h in enumerate(hdr):
            h.move_to([xs[j], 1.5, 0])
        table.add(hdr)
        for i, n in enumerate(names):
            V = int(n.replace("bytes", "").replace("bpe", "").replace("unigram", ""))
            fpt = budget / (int(d[f"steps_{n}"]) * int(d[f"tps_{n}"]))
            chars = int(d[f"steps_{n}"]) * int(d[f"tps_{n}"]) * float(d[f"cpt_{n}"])
            vals = [label(LM_NAMES[n], font_size=22, color=LM_COLORS[n]),
                    MathTex(f"{V:,}".replace(",", "{,}"), font_size=26),
                    MathTex(rf"{fpt / 1e6:.2f}\,\text{{M}}", font_size=26),
                    MathTex(f"{int(d[f'steps_{n}']):,}".replace(",", "{,}"), font_size=26),
                    MathTex(rf"{chars / 1e6:.2f}\,\text{{M}}", font_size=26)]
            row = VGroup()
            for j, v in enumerate(vals):
                v.move_to([xs[j], 0.9 - 0.55 * i, 0])
                row.add(v)
            table.add(row)
        line = Line([-6.3, 1.2, 0], [6.3, 1.2, 0], color=GREY_D, stroke_width=1.5)
        head = label(rf"the same transformer \ (${cfg['layers']}$ layers, \ width ${cfg['d']}$, \ "
                     rf"${cfg['seq']}$ tokens of context) \ and the same budget: \ ${budget / 1e12:.1f} \times 10^{{12}}$ "
                     r"FLOPs, \ three seeds", font_size=24, color=GREY_A).to_edge(UP, buff=0.6)
        if head.width > 13:
            head.width = 13
        cb, cbytes = (int(d["steps_bpe4096"]) * int(d["tps_bpe4096"]) * float(d["cpt_bpe4096"]),
                      int(d["steps_bytes256"]) * int(d["tps_bytes256"]) * float(d["cpt_bytes256"]))
        with self.voiceover(
            "Now a fair race. Five tokenizers: raw bytes, and BPE and the unigram model with 1,024 and with 4,096 "
            "pieces. <bookmark mark='a'/> Each gets the same small transformer and the same budget of arithmetic, "
            "three seeds each. <bookmark mark='b'/> A bigger vocabulary makes every token dearer, because the output "
            "layer grows with it, so those models take fewer steps. But each of their tokens carries more text: in "
            f"its budget the 4,096-piece BPE model reads {cb / 1e6:.1f} million characters, the byte model "
            f"{cbytes / 1e6:.1f} million."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hdr), Create(line), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in table[1:]],
                                                             lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(*[Indicate(table[1 + i][4], color=LM_COLORS[n]) for i, n in enumerate(names)], run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        d, names, bpc = lm_stats()
        budget = float(d["budget_bytes256"])
        allc = [np.asarray(d[f"curve_{n}_s{s}"]) for n in names for s in d["seeds"]]
        ymax = min(5.0, max(float(c[1:, 1].max()) for c in allc))
        ymin = min(float(c[:, 1].min()) for c in allc)
        ax = axes([0, budget / 1e12, 1], [math.floor(ymin * 2) / 2 - 0.25, math.ceil(ymax * 2) / 2, 0.5], x_length=6.0,
                  y_length=4.4, xlabel=r"FLOPs spent, \ $10^{12}$", ylabel=r"bits per character, \ held-out text",
                  xticks=list(range(0, int(budget / 1e12) + 1, max(1, int(budget / 1e12) // 4))),
                  yticks=[v for v in np.arange(math.ceil(ymin * 2) / 2, math.ceil(ymax * 2) / 2 + 0.01, 0.5)],
                  center=[-3.3, -0.2, 0])
        lines = VGroup()
        for n in names:
            for s in d["seeds"]:
                c = np.asarray(d[f"curve_{n}_s{s}"])
                c = c[c[:, 1] <= ymax + 0.6]
                lines.add(curve(ax.ax, c[:, 0] / 1e12, np.clip(c[:, 1], None, ymax + 0.4), LM_COLORS[n], 2.5))
        rows = [(LM_NAMES[n], LM_COLORS[n], bpc[n]) for n in names]
        lo = min(v.min() for v in bpc.values())
        hi = max(v.max() for v in bpc.values())
        bars = spread_rows(rows, x_max=hi * 1.08, width=3.0, row_h=0.62, font_size=20, label_w=2.4)
        bars.move_to([3.6, -0.3, 0])
        bl = label(r"the scoreboard's passage: \ bits per character \\ (bar: mean; \ dots: three seeds)",
                   font_size=20, color=GREY_A).next_to(bars, UP, buff=0.3)
        m = {n: float(bpc[n].mean()) for n in names}
        best = min(names, key=lambda n: m[n])
        worst = max(names, key=lambda n: m[n])
        spread = max(float(v.max() - v.min()) for v in bpc.values())
        pairs = []
        for V in (1024, 4096):
            a, b_ = bpc[f"bpe{V}"], bpc[f"unigram{V}"]
            if a.max() < b_.min():
                pairs.append(f"BPE beats the unigram model at {V:,} pieces")
            elif b_.max() < a.min():
                pairs.append(f"the unigram model beats BPE at {V:,} pieces")
            else:
                pairs.append(f"BPE and the unigram model overlap at {V:,} pieces")
        verdict = f"{pairs[0]}, and {pairs[1]}."
        with self.voiceover(
            "Here they learn, all fifteen runs, measured in bits per character on held-out text as the budget is "
            f"spent. <bookmark mark='a'/> On the scoreboard's passage, {LM_SAY[best]} does best, at {m[best]:.2f} "
            f"bits per character, and {LM_SAY[worst]} does worst, at {m[worst]:.2f}; the seeds never differ by more "
            f"than {spread:.2f}. <bookmark mark='b'/> {verdict}"
        ) as vo:
            self.play(FadeIn(ax))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.05), run_time=4.0)
            vo.wait_until("a")
            self.play(FadeIn(bl), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in bars.rows], lag_ratio=0.2),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(*[Indicate(bars.rows[names.index(f"{k}{V}")], color=WHITE, scale_factor=1.04)
                        for k in ("bpe", "unigram") for V in (1024, 4096)], run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        d, names, bpc = lm_stats()
        samples = []
        for n in ("bytes256", "bpe4096"):
            s = (str(d[f"prompt_{n}"]) + str(d[f"sample_{n}"])).replace("\n", " ")[:120]
            samples.append((n, s))
        sg = VGroup()
        for n, s in samples:
            t = data_text(s, font=MONO, font_size=18, color=WHITE)
            if t.width > 12.4:
                words, lines, cur = s.split(" "), [], ""
                for w in words:
                    if len(cur) + len(w) + 1 > 62:
                        lines.append(cur)
                        cur = w
                    else:
                        cur = (cur + " " + w).strip()
                lines.append(cur)
                t = VGroup(*[data_text(l_, font=MONO, font_size=18, color=WHITE) for l_ in lines[:2]]).arrange(
                    DOWN, aligned_edge=LEFT, buff=0.12)
            sg.add(VGroup(label(LM_NAMES[n] + r" \ writes:", font_size=22, color=LM_COLORS[n]), t)
                   .arrange(DOWN, aligned_edge=LEFT, buff=0.12))
        sg.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 1.6)
        pts = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"bigger tokens: \ more text for each FLOP, \ and more text in the window", TEXT_C),
            (r"bigger vocabularies: \ a bigger output layer, \ and rarer tokens, \ each seen less", C.SURPRISE),
            (r"at scale the output layer is a small part of the cost: \ $10^5$ tokens and more", GREY_A))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Why does the tokenizer matter at all? <bookmark mark='a'/> With bigger tokens, every FLOP buys more text, "
            "and the same window of 128 tokens holds more of the passage. <bookmark mark='b'/> But a bigger "
            "vocabulary means a bigger output layer, and rarer tokens, each seen fewer times in training. "
            "<bookmark mark='c'/> In a model with billions of parameters the output layer is a small part of the "
            "cost, which is why real vocabularies have a hundred thousand tokens or more. <bookmark mark='d'/> Here "
            "is what two of ours write after the passage's opening words, at a temperature of 0.8. The tokenizer is "
            "a hidden choice behind every score, and bits per character keeps the comparison honest."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(s_, shift=UP * 0.1) for s_ in sg], lag_ratio=0.4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
