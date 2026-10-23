from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import A, CAPC, K, NORMC, PART, Q, curve, load

PLAIN = C.SURPRISE
MODES = (("plain", r"plain", PLAIN), ("cap", r"soft cap", CAPC), ("norm", r"QK-norm", NORMC))


class Caps(VoiceoverScene):
    def construct(self):
        self.card()
        self.blowup()
        self.norm()
        self.cap()

    def card(self):
        card = chapter_card(13, r"Keeping scores in range", r"What stops attention scores from running away?",
                            part=PART)
        with self.voiceover("Chapter thirteen. Keeping scores in range."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def plot(self, q, key, ylabel, lo, hi, center, ticks, fmt="{:.1f}", modes=("plain",), y_length=3.0):
        cs = np.asarray(q["cs"], float)
        g = axes([1, cs[-1], 1], [lo, hi, (hi - lo) / 4], x_length=5.4, y_length=y_length,
                 xlabel=r"$W_Q$ and $W_K$ grown by a factor $c$", ylabel=ylabel, xticks=list(range(1, int(cs[-1]) + 1)),
                 xfmt=lambda v: f"{int(v)}", yticks=ticks, yfmt=lambda v: fmt.format(v), center=center)
        lines = {m: VGroup(curve(g.ax, cs, np.clip(np.asarray(q[f"{key}_{m}"]), lo, hi), col, 3.5),
                           *[Dot(g.ax.c2p(a, min(max(b, lo), hi)), radius=0.05, color=col)
                             for a, b in zip(cs, q[f"{key}_{m}"])])
                 for m, _, col in MODES}
        return g, lines

    # ------------------------------------------------------------------
    def blowup(self):
        q = load("qkscale")
        cs = np.asarray(q["cs"], float)
        ent, bits, lg = (np.asarray(q[k], float) for k in ("ent_plain", "bits_plain", "logit_plain"))
        pk = np.asarray(q["peak_plain"], float)
        e_hi = float(np.ceil(ent.max() + 0.5))
        g1, l1 = self.plot(q, "ent", r"attention entropy, \ bits", 0, e_hi, [-3.4, -0.3, 0], [0, e_hi / 2, e_hi])
        b_lo, b_hi = float(np.floor(bits.min() * 2) / 2), float(np.ceil(bits.max() * 2) / 2 + 0.5)
        g2, l2 = self.plot(q, "bits", r"bits per character", b_lo, b_hi, [3.4, -0.3, 0], [b_lo, b_hi], fmt="{:.1f}")
        eq = cmath(r"s", r"=", r"\frac{(c\, W_Q x)\cdot(c\, W_K y)}{\sqrt{d}}", r"=", r"c^2 s_0", font_size=34).to_edge(UP, buff=0.5)
        tag = note(r"our transformer, \ $16$ windows of held-out text; \ every head's $W_Q$ and $W_K$ scaled").to_edge(DOWN, buff=0.2)
        hist = label(r"Dehghani et al.\ (2023), ViT-22B: \ attention logits grew without bound, \ and training "
                     r"diverged", font_size=20, color=GREY_A).next_to(eq, DOWN, buff=0.25)
        i2 = int(np.argmin(np.abs(cs - 2.0)))
        with self.voiceover(
            "Chapter three divided by the square root of d to keep scores in range at the start. But training can "
            "grow the weights, and a score is a product of two of them: <bookmark mark='a'/> grow W Q and W K by a "
            "factor c, and every score grows by c squared. <bookmark mark='b'/> Here is what that does to our own "
            f"transformer. At c of 2, the largest score goes from {lg[0]:.0f} to {lg[i2]:.0f}, the attention's "
            f"entropy falls from {ent[0]:.1f} bits to {ent[i2]:.1f}, and the share of rows where one key takes "
            f"over ninety percent of the weight goes from {pk[0]:.0%} to {pk[i2]:.0%}. <bookmark mark='c'/> And the "
            f"model's guesses suffer: from {bits[0]:.2f} bits a character to {bits[i2]:.2f}, and {bits[-1]:.2f} at "
            f"c of {cs[-1]:.0f}. <bookmark mark='d'/> In large runs this happens by itself: in 2023 the team that "
            "trained Google's 22-billion-parameter vision transformer saw attention logits grow without bound until "
            "training diverged."
        ) as vo:
            self.play(FadeIn(eq), FadeIn(g1), FadeIn(g2), FadeIn(tag))
            vo.wait_until("a")
            self.play(Indicate(eq[4], color=PLAIN), Create(l1["plain"][0]), FadeIn(l1["plain"][1:]), run_time=1.5)
            vo.wait_until("b")
            self.play(Indicate(g1, scale_factor=1.02))
            vo.wait_until("c")
            self.play(Create(l2["plain"][0]), FadeIn(l2["plain"][1:]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(hist))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def norm(self):
        q = load("qkscale")
        cs = np.asarray(q["cs"], float)
        rows = [
            cmath(r"\hat q", r"=", r"g_q \odot \frac{q}{\operatorname{rms}(q)}, \quad \hat k = g_k \odot \frac{k}{\operatorname{rms}(k)}",
                  font_size=32, colors={r"\hat q": Q}),
            cmath(r"\Big\|\frac{q}{\operatorname{rms}(q)}\Big\|", r"=", r"\sqrt{d}", font_size=32),
            cmath(r"\frac{|\hat q \cdot \hat k|}{\sqrt d}", r"\le", r"\frac{\|\hat q\|\,\|\hat k\|}{\sqrt d} \le g^2 \sqrt{d}",
                  font_size=32),
        ]
        whys = [why(r"normalize each head's query and key", font_size=20), why(r"$\operatorname{rms}(q) = \|q\|/\sqrt d$", font_size=20),
                why(r"Cauchy--Schwarz; \ $g$ the largest gain", font_size=20)]
        step = ladder(self, rows, whys, keep=3, top=3.15, x=-2.2, buff=0.5, edge=6.9)
        ent = np.asarray(q["ent_norm"], float)
        eh = float(np.ceil(np.asarray(q["ent_plain"]).max() + 0.5))
        g1, l1 = self.plot(q, "ent", r"attention entropy, \ bits", 0, eh, [-3.4, -2.3, 0], [0, eh], fmt="{:.0f}",
                           y_length=2.1)
        users = label(r"QK-norm: \ ViT-22B (2023), \ Qwen3, \ GLM-4.5, \ Gemma 3 \ (2025)", font_size=22,
                      color=NORMC).move_to([3.6, -1.4, 0])
        pt18 = label(r"Part 18 measures the runaway logits \\ in training, with and without it", font_size=20,
                     color=GREY_A).next_to(users, DOWN, buff=0.3)
        b0_, bn_ = float(np.asarray(q["bits_plain"])[0]), float(np.asarray(q["bits_norm"])[0])
        bolt = label(rf"bolted onto our trained model: \ ${bn_:.2f}$ bits \ instead of ${b0_:.2f}$", font_size=20,
                     color=NORMC).next_to(pt18, DOWN, buff=0.3)
        flat = float(np.ptp(ent))
        b0, bn = float(np.asarray(q["bits_plain"])[0]), float(np.asarray(q["bits_norm"])[0])
        if flat < 1e-3:
            moves = ("On our transformer, with its queries and keys normalized to their trained sizes, growing the "
                     "weights now changes nothing at all.")
        else:
            moves = (f"On our transformer, with its queries and keys normalized to their trained sizes, growing the "
                     f"weights now moves the entropy by only {flat:.3f} bits.")
        cost = (f"But bolted onto a model that was trained without it, it costs {bn - b0:.2f} bits a character, "
                f"{bn:.2f} against {b0:.2f}: our model had learned to use the sizes of its queries, so QK-norm has to "
                "be there from the start of training." if bn > b0 + 0.05 else
                "Bolted onto a model trained without it, it costs almost nothing here.")
        with self.voiceover(
            "The fix the vision team used, and many language models since, is QK-norm. <bookmark mark='a'/> Before "
            "the dot product, divide each head's query and key by their root-mean-square size, then multiply by a "
            "learned gain. <bookmark mark='b'/> A vector divided by its root mean square has length exactly the "
            "square root of d, <bookmark mark='c'/> so by Cauchy-Schwarz the score can never exceed the gains "
            "squared times the square root of d, however large W Q and W K become. <bookmark mark='d'/> "
            + moves + " <bookmark mark='e'/> " + cost + " <bookmark mark='f'/> Qwen3, GLM-4.5 and Gemma 3 all normalize their queries and keys; Part 18 shows the "
            "runaway logits in training, with and without it."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(Indicate(rows[0][2], color=NORMC))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(g1), Create(l1["plain"][0]), FadeIn(l1["plain"][1:]))
            self.play(Create(l1["norm"][0]), FadeIn(l1["norm"][1:]), FadeIn(users), FadeIn(pt18))
            if bn_ > b0_ + 0.05:
                self.play(FadeIn(bolt))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cap(self):
        q = load("qkscale")
        cs = np.asarray(q["cs"], float)
        capv = float(q["cap"])
        ent_c, bits_c, bits_p = (np.asarray(q[k], float) for k in ("ent_cap", "bits_cap", "bits_plain"))
        lgc = np.asarray(q["logit_cap"], float)
        g = axes([-3 * capv, 3 * capv, capv], [-1.5 * capv, 1.5 * capv, capv], x_length=4.6, y_length=3.0,
                 xlabel=r"score $s$", ylabel=r"capped score", xticks=[-capv, capv], yticks=[-capv, capv],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", center=[-3.6, 0.6, 0])
        ax = g.ax
        idl = DashedLine(ax.c2p(-1.5 * capv, -1.5 * capv), ax.c2p(1.5 * capv, 1.5 * capv), color=GREY_B, stroke_width=1.5)
        cp = ax.plot(lambda s: capv * np.tanh(s / capv), x_range=[-3 * capv, 3 * capv], color=CAPC, stroke_width=3.5)
        lims = VGroup(*[DashedLine(ax.c2p(-3 * capv, v), ax.c2p(3 * capv, v), color=CAPC, stroke_width=1.2,
                                   stroke_opacity=0.6) for v in (capv, -capv)])
        eq = cmath(r"s", r"\;\leftarrow\;", r"c\,\tanh(s / c)", font_size=36).next_to(g, UP, buff=0.3)
        eh = float(np.ceil(np.asarray(q["ent_plain"]).max() + 0.5))
        g1, l1 = self.plot(q, "ent", r"attention entropy, \ bits", 0, eh, [3.4, 0.6, 0], [0, eh], fmt="{:.0f}")
        facts = VGroup(
            label(r"Gemma 2 (2024): \ $c = 50$ on attention scores, \ $30$ on the output", font_size=20, color=GREY_A),
            label(r"Gemma 3 (2025): \ replaced by QK-norm", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([0, -3.0, 0])
        tag = note(rf"our cap: \ $c = {capv:.0f}$, \ just above the trained model's largest score").next_to(facts, UP, buff=0.2)
        ent_p = np.asarray(q["ent_plain"], float)
        if bits_c[-1] < bits_p[-1] - 0.05:
            bt = f"At c of {cs[-1]:.0f} the bits per character are {bits_c[-1]:.2f} instead of {bits_p[-1]:.2f}. "
        elif bits_c[-1] > bits_p[-1] + 0.05:
            bt = (f"But the guesses get worse, not better: {bits_c[-1]:.2f} bits a character at c of {cs[-1]:.0f}, "
                  f"against {bits_p[-1]:.2f} uncapped. With every large score flattened onto the cap, a head can no "
                  "longer tell its best keys apart: a cap must sit well above the scores a model actually uses. ")
        else:
            bt = f"The bits per character suffer about as much, {bits_c[-1]:.2f}. "
        et = (f"the entropy falls only to {ent_c[-1]:.1f} bits instead of {ent_p[-1]:.1f}" if ent_c[-1] > ent_p[-1] + 0.1
              else f"the entropy falls just as far, to {ent_c[-1]:.1f} bits")
        with self.voiceover(
            "A gentler alternative is a soft cap: replace each score s by c times the hyperbolic tangent of s over "
            "c. <bookmark mark='a'/> Small scores pass almost unchanged; large ones level off at plus or minus c. "
            f"<bookmark mark='b'/> Set c just above our trained model's largest score, {capv:.0f}, and grow the "
            f"weights again: the scores can no longer pass {capv:.0f}, and {et}. <bookmark mark='d'/> " + bt
            + "<bookmark mark='c'/> Gemma 2 capped its attention scores at fifty in 2024; Gemma 3 dropped the cap "
            "for QK-norm, which bounds the scores without bending them."
        ) as vo:
            self.play(FadeIn(g), FadeIn(eq), Create(idl))
            vo.wait_until("a")
            self.play(Create(cp), Create(lims), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(g1), FadeIn(tag), Create(l1["plain"][0]), FadeIn(l1["plain"][1:]))
            self.play(Create(l1["cap"][0]), FadeIn(l1["cap"][1:]))
            vo.wait_until("d")
            self.play(Indicate(l1["cap"][0], color=CAPC))
            vo.wait_until("c")
            self.play(FadeIn(facts))
        self.wait(0.3)
        self.clear_scene()
