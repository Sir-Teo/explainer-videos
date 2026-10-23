from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai21.common import HIST, MDM_C, MONO, PART, legend, load, take_away

KCOL = {"exact": MDM_C, "blurred": C.BITS, "nocontext": C.SURPRISE}
KNAME = {"exact": r"the exact conditionals", "blurred": r"blurred towards uniform", "nocontext": r"no context"}


class Discrete(VoiceoverScene):
    def construct(self):
        self.card()
        self.noise()
        self.derive()
        self.check()
        self.lineage()

    def card(self):
        card = chapter_card(16, r"Diffusion for discrete data", r"What is noise, for words?", part=PART)
        with self.voiceover("Chapter sixteen. Diffusion for discrete data."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def noise(self):
        s = "Spade looked at the girl."
        g = np.random.default_rng(1)
        u = g.random(len(s))
        letters = "abcdefghijklmnopqrstuvwxyz"
        rnd = g.integers(0, 26, len(s))

        def row(t, kind):
            out = []
            for ch, uu, r in zip(s, u, rnd):
                if ch == " " or uu >= t:
                    out.append(ch)
                else:
                    out.append("_" if kind == "mask" else letters[r])
            return "".join(out)

        ts = [0.0, 0.3, 0.6, 1.0]
        cols = VGroup()
        for kind, nm, col in (("uniform", r"uniform: \ swap for a random letter", C.SURPRISE),
                              ("mask", r"absorbing: \ blank it out", MDM_C)):
            rows = VGroup(*[VGroup(MathTex(rf"t = {t:g}", font_size=26, color=GREY_B),
                                   data_text(row(t, kind), font=MONO, font_size=28, color=WHITE)).arrange(RIGHT, buff=0.4)
                            for t in ts]).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            cols.add(VGroup(label(nm, font_size=24, color=col), rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3))
        cols.arrange(RIGHT, buff=0.9).move_to([0, 0.9, 0])
        if cols.width > 13.2:
            cols.width = 13.2
        d = definition_card(r"discrete diffusion (D3PM)", VGroup(
            MathTex(r"q(x_t \mid x_0) = \mathrm{Cat}\big(x_0\, \bar Q_t\big), \qquad \bar Q_t = Q_1 Q_2 \cdots Q_t", font_size=28),
            label(r"each $Q$: \ a matrix of letter-to-letter probabilities", font_size=20, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12), width=7.6).to_edge(DOWN, buff=0.35)
        tag = note(r"illustrative").to_corner(UR, buff=0.3)
        cite_ = cite(r"J.~Austin, D.~Johnson, J.~Ho, D.~Tarlow \& R.~van den Berg, \textit{D3PM} (2021)", corner=UL, font_size=18)
        with self.voiceover(
            "Text is made of symbols, not numbers, so Gaussian noise doesn't fit. In 2021 Jacob Austin and colleagues "
            "at Google generalized diffusion to symbols: <bookmark mark='a'/> each step replaces a symbol at random, "
            "according to a matrix of probabilities, and the matrices multiply into a closed form, just as the "
            "Gaussians did. <bookmark mark='b'/> Two choices matter. Swap a letter for a random one, <bookmark mark='c'/> "
            "or blank it out with a special mask symbol, which then stays blank: absorbing noise. The blanks won. At "
            "the end, everything is blank, and the reverse process fills the blanks in."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(cite_), FadeIn(cols[0][0]), FadeIn(cols[1][0]))
            vo.wait_until("a")
            self.play(FadeIn(d, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in cols[0][1]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in cols[1][1]], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            cmath(r"q(x^i_t \mid x^i_0)", r"=", r"\begin{cases} x^i_0 & 1 - t \\ [\mathrm{M}] & t \end{cases}", font_size=30),
            cmath(r"q(x^i_s \mid x^i_t = [\mathrm{M}],\ x_0)", r"=", r"\begin{cases} [\mathrm{M}] & s/t \\ x^i_0 & (t - s)/t \end{cases}",
                  font_size=30),
            cmath(r"\mathrm{KL}_i", r"=", r"\frac{t - s}{t}\; \big(-\log p_\theta(x^i_0 \mid x_t)\big)", font_size=30),
            cmath(r"\mathcal L", r"=", r"\int_0^1 \frac{1}{t}\; \mathbb E_{x_t}\Big[\sum_{i \text{ blank}} -\log p_\theta(x^i_0 \mid x_t)\Big]\, dt",
                  font_size=30),
            cmath(r"\mathcal L", r"=", r"\sum_{k=1}^{n} \mathbb E_{|M| = k}\Big[\frac{1}{k} \sum_{i \in M} -\log p_\theta(x_i \mid "
                  r"x_{\setminus M})\Big]", font_size=30),
        ]
        whys = [why(r"blank with probability $t$ \ (a linear schedule)"),
                why(r"Bayes: \ blanked before $s$, \ or between $s$ and $t$"),
                why(r"the same chance of staying blank: \ only the reveal differs"),
                why(r"add up the steps: \ $t - s \to dt$"),
                why(r"$k$ blanks: \ $\int_0^1 t^{k-1}(1-t)^{n-k}\, dt = \frac{1}{k \binom{n}{k}}$")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-1.8, buff=0.55, edge=6.85)
        tail = label(r"$=$ \ an autoregressive loss, \ averaged over every order of revealing the letters", font_size=26,
                     color=MDM_C).to_edge(DOWN, buff=0.45)
        cite_ = cite(r"Sahoo et al.\ (MDLM); \ Shi et al.\ (MD4); \ Ou et al.\ (2024)", corner=DR, font_size=18)
        with self.voiceover(
            "With blanks, the bound becomes remarkably simple. Each letter is blank with probability t. "
            "<bookmark mark='a'/> Going back from time t to an earlier time s, a blank either stays blank, with "
            "probability s over t, or reveals its letter. <bookmark mark='b'/> The model's step back can differ only "
            "in which letter it reveals, so each KL term is the reveal probability times the cross-entropy of "
            "guessing the letter. <bookmark mark='c'/> Add up the steps, and the bound is an integral: one over t "
            "times the cross-entropy of guessing every blank from the letters still showing. Three groups derived "
            "this in 2024. <bookmark mark='d'/> One more change of variable, from the time to the number of blanks "
            "k, turns the one over t into one over k: the bound is an average, over every number of blanks, of the "
            "loss per blank. <bookmark mark='e'/> That is an autoregressive model's loss, averaged over every order "
            "in which the letters could be revealed."
        ) as vo:
            self.play(FadeIn(cite_))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
            vo.wait_until("e")
            self.play(FadeIn(tail))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        d = load("discrete")
        Ts = [int(t) for t in d["Ts"]]
        kinds = list(d["kinds"])
        H = float(d["H_bits"])
        L, V = int(d["L"]), int(d["V"])
        top = max(max(float(v) for v in d[f"{k}_disc"]) for k in kinds) * 1.05
        lo = H * 0.95
        g = axes([0, math.log10(Ts[-1])], [lo, top], x_length=6.0, y_length=3.8, xlabel=r"steps $T$ of the chain",
                 ylabel=r"the bound, \ bits per letter", xticks=[], yticks=[round(H, 2), round(top, 2)], center=[-2.6, -0.4, 0])
        g.add(*[MathTex(str(t), font_size=18, color=GREY_B).next_to(g.ax.c2p(math.log10(t), lo), DOWN, buff=0.12)
                for t in Ts[::2]])
        lx = np.log10(Ts)
        lines = VGroup()
        for k in kinds:
            v = np.asarray(d[f"{k}_disc"])
            c = float(d[f"{k}_cont"])
            lines.add(VGroup(curve(g.ax, lx, v, KCOL[k], 3), *[Dot(g.ax.c2p(a, b), radius=0.04, color=KCOL[k]) for a, b in zip(lx, v)],
                             DashedLine(g.ax.c2p(0, c), g.ax.c2p(lx[-1], c), color=KCOL[k], stroke_width=1.5)))
        hl = DashedLine(g.ax.c2p(0, H), g.ax.c2p(lx[-1], H), color=WHITE, stroke_width=2)
        hll = label(rf"the true entropy: \ ${H:.4f}$", font_size=18, color=WHITE).next_to(hl, DOWN, buff=0.06).align_to(hl, RIGHT)
        lang = VGroup(label(rf"a tiny language: \ ${L}$ letters from $\{{a, b, c\}}$, \ ${int(d['n_strings'])}$ strings", font_size=20,
                            color=GREY_A),
                      label(r"a Markov chain that likes $a \to b \to c \to a$", font_size=20, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.7, 2.6, 0])
        rows = [[r"model", r"weighted CE", r"any order", r"left to right"]]
        for k in kinds:
            rows.append([KNAME[k], f"${float(d[f'{k}_cont']):.6f}$", f"${float(d[f'{k}_anyorder']):.6f}$",
                         f"${float(d[f'{k}_l2r']):.6f}$"])
        tab = VGroup(*[VGroup(*[label(c, font_size=17, color=(GREY_A if i == 0 else (KCOL[kinds[i - 1]] if j == 0 else WHITE)))
                                for j, c in enumerate(r)]) for i, r in enumerate(rows)])
        xs = [2.0, 3.85, 5.15, 6.35]
        for i, r in enumerate(tab):
            for j, c in enumerate(r):
                c.move_to([xs[j], 1.4 - 0.42 * i, 0])
                if j == 0:
                    c.align_to([1.2, 0, 0], LEFT)
        lg = legend([(KCOL[k], KNAME[k]) for k in kinds], font_size=18).move_to([3.9, -1.6, 0])
        ex, bl, nc = (float(d[f"{k}_cont"]) for k in kinds)
        gap = max(abs(float(d[f"{k}_cont"]) - float(d[f"{k}_anyorder"])) for k in kinds)
        tight = abs(ex - H) < 1e-6
        d1, dT = float(d["exact_disc"][0]), float(d["exact_disc"][-1])
        dp = min(12, max(1, int(-math.log10(max(gap, 1e-15)))))
        if tight:
            tight_note = ("And with the exact conditionals, the bound equals the true entropy: it is tight. A model that "
                          "learns the conditionals perfectly pays nothing for the bound.")
        else:
            tight_note = "And with the exact conditionals, the bound is close to the true entropy."
        with self.voiceover(
            f"Check it where everything can be enumerated: strings of {L} letters from a, b and c, drawn from a "
            "Markov chain, every probability known. Three models predict the blanks: the exact conditionals, the same "
            "blurred towards uniform, and one that ignores the context. <bookmark mark='a'/> The bound of a chain "
            f"with T steps, computed exactly: with one step, the exact model's bound is {d1:.4f} bits per letter; "
            f"with {Ts[-1]:,} steps, {dT:.4f}, settling onto the integral, the dashed lines. <bookmark mark='b'/> The "
            f"integral, the weighted cross-entropy, and the average over every order of revealing agree to {dp} decimal "
            "places, for every model. <bookmark mark='c'/> " + tight_note
        ) as vo:
            self.play(FadeIn(lang), FadeIn(g), Create(hl), FadeIn(hll), FadeIn(lg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in lines], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(Indicate(lines[0][-1], color=WHITE), Indicate(hl, color=WHITE))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lineage(self):
        cards = VGroup(
            history_card(2014, r"Uria, Murray \& Larochelle", r"one network for every order of an autoregressive model",
                         color=HIST, width=4.3, font_size=17),
            history_card(2022, r"Hoogeboom et al.: \ autoregressive diffusion", r"any order, \ several letters at a time",
                         color=HIST, width=4.3, font_size=17),
            history_card(2024, r"Lou, Meng \& Ermon: \ SEDD", r"ratios of probabilities as the discrete score; \ ICML "
                         r"best paper", color=HIST, width=4.3, font_size=17),
            history_card(2024, r"Sahoo et al.: \ MDLM; \ Shi et al.: \ MD4", r"masked diffusion is a weighted "
                         r"cross-entropy: \ simple, and as good", color=HIST, width=4.3, font_size=17),
            history_card(2024, r"Ou et al.", r"the model need not know the time: \ only which letters are blank",
                         color=HIST, width=4.3, font_size=17),
            history_card(2025, r"Nie et al.: \ LLaDA", r"an $8$-billion-parameter masked diffusion language model",
                         color=HIST, width=4.3, font_size=17),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.22, 0.25)).move_to(UP * 0.4)
        if cards.width > 13.4:
            cards.width = 13.4
        ta = take_away(r"Masked diffusion's bound is an autoregressive loss averaged over all orders; \ its training is "
                       r"fill-in-the-blanks.")
        with self.voiceover(
            "The idea has a lineage. In 2014 Benigno Uria, Iain Murray and Hugo Larochelle trained one network for "
            "every order of an autoregressive model; <bookmark mark='a'/> in 2022 Emiel Hoogeboom and colleagues "
            "connected such any-order models to diffusion. <bookmark mark='b'/> In 2024 Aaron Lou, Chenlin Meng and "
            "Stefano Ermon defined a score for discrete data, ratios of probabilities, and won a best-paper award at "
            "ICML; <bookmark mark='c'/> the same year, two groups, Subham Sahoo's and Jiaxin Shi's, showed separately that "
            "plain masked diffusion, the weighted cross-entropy, does as well, <bookmark mark='d'/> and Jingyang Ou and "
            "colleagues that the model doesn't even need to be told the time. <bookmark mark='e'/> Which is what "
            "made the next step possible: language models trained this way, at scale."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.1))
            for k, mk in enumerate("abcde", 1):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.1), run_time=0.7)
            self.play(FadeIn(ta, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
