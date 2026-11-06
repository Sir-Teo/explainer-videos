from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs27.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table, load, mono)


def pentagraph(edges, center, r=0.8, color=DATA):
    pos = [center + r * np.array([np.cos(PI / 2 + 2 * PI * i / 5), np.sin(PI / 2 + 2 * PI * i / 5), 0])
           for i in range(5)]
    es = VGroup(*[Line(pos[u], pos[v], stroke_width=2.5, color=color) for u, v in edges])
    ds = VGroup(*[Dot(p, radius=0.08, color=WHITE) for p in pos])
    return VGroup(es, ds)


class Interactive(VoiceoverScene):
    def construct(self):
        self.card()
        self.gni()
        self.classes()

    def card(self):
        card = chapter_card(5, r"Interactive proofs", r"Can a conversation prove more than a document?",
                            lit=(1985,), extra=((1985, r"Goldwasser--Micali--Rackoff; \ Babai"),), part=PART)
        with self.voiceover("Chapter five. Interactive proofs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def gni(self):
        g = load("gni")
        head = label(r"Proving two graphs are \textbf{not} the same", font_size=32).to_edge(UP, buff=0.3)
        G0 = pentagraph(g["G0"], LEFT * 4.6 + UP * 1.0, color=DATA)
        G1 = pentagraph(g["G1"], LEFT * 2.2 + UP * 1.0, color=HEAD)
        l0 = label(r"$G_0$", font_size=22, color=DATA).next_to(G0, DOWN, buff=0.1)
        l1 = label(r"$G_1$", font_size=22, color=HEAD).next_to(G1, DOWN, buff=0.1)
        steps = VGroup(
            label(r"1. \ the verifier secretly picks $b \in \{0, 1\}$ \\ and a random relabelling of $G_b$",
                  font_size=20, color=WHITE),
            label(r"2. \ the prover, \ all-powerful, \ says which graph it came from", font_size=20, color=WHITE),
            label(r"3. \ the verifier accepts if the answer is $b$", font_size=20, color=WHITE),
            label(rf"not isomorphic: \ the prover can always tell: \ {g['honest_rate'] * 100:.0f}\% right", font_size=20,
                  color=YES),
            label(rf"isomorphic \ (a 5-cycle relabelled): \ the prover can only guess: \\ {g['bluff_rate'] * 100:.0f}\% "
                  r"right in 2,000 rounds", font_size=20, color=NO),
            label(r"after $k$ rounds a bluffer survives with probability $2^{-k}$: \ $10^{-6}$ after 20", font_size=20,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(VGroup(G0, G1), RIGHT, buff=0.7).align_to(G0, UP)
        fit_right(steps)
        note = label(r"no short certificate for non-isomorphism is known: \ interaction does what a written proof "
                     r"apparently cannot", font_size=21, color=LAM).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "How do you prove that two graphs are different? For sameness, the matching of vertices is a short "
            "certificate. For difference, none is known. But a conversation works. <bookmark mark='a'/> The verifier "
            "flips a coin, picks one of the two graphs, scrambles its vertex labels, and shows the result to the "
            "prover. <bookmark mark='b'/> The prover, who has unlimited computing power, says which graph it came "
            "from. <bookmark mark='c'/> The verifier accepts if the answer matches the coin. <bookmark mark='d'/> If "
            "the graphs really differ, the prover can always tell, and our honest prover was right every time. "
            "<bookmark mark='e'/> If they are the same, the scrambled graph carries no information about the coin, "
            "and the prover can only guess: forty-nine percent in our two thousand rounds. <bookmark mark='f'/> Twenty "
            "rounds push a bluffer's chances below one in a million. <bookmark mark='g'/> Interaction has proved "
            "something no known written proof can."
        ) as vo:
            self.play(FadeIn(head), FadeIn(G0), FadeIn(G1), FadeIn(l0), FadeIn(l1))
            for mk, st in zip("abcdef", steps):
                vo.wait_until(mk)
                self.play(FadeIn(st, shift=UP * 0.1))
            vo.wait_until("g")
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    def classes(self):
        head = label(r"IP, \ and Arthur and Merlin", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"\textbf{IP}: \ a randomized polynomial-time verifier talks to an all-powerful prover", font_size=22,
                  color=WHITE),
            label(r"\textbf{completeness}: \ true statements are accepted \ (with probability $\ge \tfrac23$)",
                  font_size=22, color=YES),
            label(r"\textbf{soundness}: \ false ones are rejected whatever the prover does \ (probability $\ge "
                  r"\tfrac23$)", font_size=22, color=NO),
            label(r"Goldwasser, \ Micali and Rackoff \ (1985): \ private coins, \ and the idea of \textbf{knowledge}",
                  font_size=22, color=DATA),
            label(r"Babai \ (1985): \ \textbf{Arthur--Merlin} games, \ where the coins are public", font_size=22,
                  color=HEAD),
            label(r"Goldwasser and Sipser \ (1986): \ private and public coins give the same power", font_size=22,
                  color=LAM),
            label(r"NP is IP with no coins and one message. \ How much more does interaction buy? \ Next chapter",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "The general setting is called IP. <bookmark mark='a'/> A verifier that runs in polynomial time and "
            "flips coins exchanges messages with an all-powerful prover. <bookmark mark='b'/> True statements must be "
            "accepted with high probability, <bookmark mark='c'/> and false ones rejected with high probability, "
            "whatever the prover tries. <bookmark mark='d'/> Shafi Goldwasser, Silvio Micali and Charles Rackoff "
            "introduced the idea in 1985, together with the question of how much knowledge a proof conveys. "
            "<bookmark mark='e'/> László Babai independently defined Arthur-Merlin games, in which the verifier's "
            "coins are shown to the prover. <bookmark mark='f'/> Goldwasser and Sipser showed that hiding the coins "
            "makes no difference. <bookmark mark='g'/> NP is the special case with one message and no coins. How "
            "much more does interaction give? The answer is the next chapter."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdefg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
