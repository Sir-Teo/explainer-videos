from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs29.common import (CTRL, DATA, HEAD, NO, PART, YES, flow_box)


class Definitions(VoiceoverScene):
    def construct(self):
        self.card()
        self.bounded()
        self.game()
        self.reductions()

    def card(self):
        card = chapter_card(5, r"What secure means", r"What can we promise if keys are short?", lit=(1883, 1982),
                            extra=((1883, r"Kerckhoffs's principles"), (1982, r"Goldwasser--Micali: \ semantic "
                                                                             r"security")), part=PART)
        with self.voiceover("Chapter five. What secure means."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def bounded(self):
        head = label(r"An attacker with limited computing", font_size=34).to_edge(UP, buff=0.3)
        rows = [(56, r"$2^{56}$: \ every DES key; \ Deep Crack, \ 56 hours \ (1998)", NO),
                (64, r"$2^{64}$: \ done for SHA-1 collisions and RC5 keys", CTRL),
                (94, r"$2^{94}$: \ every Bitcoin miner on Earth, \ for a year of hashing", HEAD),
                (128, r"$2^{128}$: \ every AES-128 key", YES)]
        x0, scale = -6.0, 6.0 / 128
        bars = VGroup()
        for i, (b, t, c) in enumerate(rows):
            y = 1.6 - i * 0.75
            r = Rectangle(width=b * scale, height=0.4, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to(
                [x0 + b * scale / 2, y, 0])
            bars.add(VGroup(r, label(t, font_size=20, color=WHITE).next_to(r, RIGHT, buff=0.2)))
        axl = label(r"work, \ as a power of two \ (bar length $\propto$ exponent)", font_size=17,
                    color=GREY_A).next_to(bars, UP, buff=0.3).align_to(bars, LEFT)
        lines = VGroup(
            label(r"Kerckhoffs \ (1883): \ assume the enemy knows the system; \ only the \textbf{key} is secret",
                  font_size=21, color=WHITE),
            label(r"the attacker runs in \textbf{probabilistic polynomial time} in the key length $n$", font_size=21,
                  color=DATA),
            label(r"success beyond guessing must be \textbf{negligible}: \ smaller than $1/n^c$ for every $c$, \ "
                  r"like $2^{-n}$", font_size=21, color=HEAD),
            label(r"in practice: \ $2^{128}$ work is more than all the world's computers could do before the Sun "
                  r"burns out", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Shannon's theorem is final: with keys shorter than messages, a ciphertext always leaks something to an "
            "attacker with unlimited time. So modern cryptography limits the attacker. <bookmark mark='a'/> First, "
            "a rule from Auguste Kerckhoffs in 1883: assume the enemy knows how your system works. Only the key is "
            "secret, because algorithms leak, get published, get stolen. <bookmark mark='b'/> Second, the attacker "
            "is an efficient algorithm: one that may flip coins, and runs in time polynomial in the key length. "
            "<bookmark mark='c'/> Third, its advantage over blind guessing must be negligible: smaller than one over "
            "any polynomial, like two to the minus n. <bookmark mark='d'/> In concrete numbers: trying every key of "
            "DES took a special machine fifty-six hours in 1998. Every Bitcoin miner together computes about two to "
            "the ninety-four hashes a year. Two to the hundred and twenty-eight is seventeen billion times more. "
            "That is the margin AES is built to."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(axl), LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.4), run_time=3.0)
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def game(self):
        head = label(r"Security as a game: \ IND-CPA", font_size=34).to_edge(UP, buff=0.3)
        L = label(r"challenger \\ (holds $k$, \ flips $b$)", font_size=20, color=HEAD).move_to([-3.6, 2.2, 0])
        R = label(r"adversary $\mathcal{A}$", font_size=20, color=NO).move_to([3.6, 2.2, 0])
        lx, rx = -3.6, 3.6
        vl = DashedLine([lx, 1.75, 0], [lx, -1.4, 0], color=GREY_D)
        vr = DashedLine([rx, 1.75, 0], [rx, -1.4, 0], color=GREY_D)
        msgs = [(1.4, r"any messages $m$", "R"), (1.0, r"$\mathrm{Enc}_k(m)$", "L"),
                (0.35, r"two messages $m_0, m_1$ \ (same length)", "R"), (-0.05, r"$\mathrm{Enc}_k(m_b)$", "L"),
                (-0.6, r"more queries", "R"), (-1.15, r"guess $b'$", "R")]
        arrows = VGroup()
        for y, t, d in msgs:
            a, b = ([rx, y, 0], [lx, y, 0]) if d == "R" else ([lx, y, 0], [rx, y, 0])
            ar = Arrow(a, b, buff=0.05, stroke_width=2.5, color=NO if d == "R" else HEAD,
                       max_tip_length_to_length_ratio=0.04)
            arrows.add(VGroup(ar, label(t, font_size=19, color=WHITE).next_to(ar, UP, buff=0.05)))
        lines = VGroup(
            label(r"secure if every efficient $\mathcal{A}$ has $\bigl|\Pr[b' = b] - \tfrac12\bigr|$ negligible: "
                  r"\ it learns nothing it could use", font_size=21, color=YES),
            label(r"Goldwasser and Micali \ (1982): \ this is equivalent to \textbf{semantic security}: \ no "
                  r"function of $m$ leaks", font_size=21, color=WHITE),
            label(r"consequence: \ encryption must be \textbf{randomised} \ (a fresh IV or nonce): \ else "
                  r"$\mathcal{A}$ asks for $\mathrm{Enc}(m_0)$ and compares", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "What should the attacker be unable to do? Shafi Goldwasser and Silvio Micali answered in 1982 with a "
            "game. <bookmark mark='a'/> A challenger holds a secret key. The adversary may ask for the encryption of "
            "any messages it likes: chosen plaintexts. <bookmark mark='b'/> Then it hands over two messages of its "
            "choice. The challenger secretly flips a coin and returns the encryption of one of them. <bookmark "
            "mark='c'/> The adversary may ask more questions, and finally guesses which one it got. <bookmark "
            "mark='d'/> The scheme is secure if no efficient adversary guesses right noticeably more than half the "
            "time. If you cannot even tell which of two messages you chose was encrypted, you learn nothing useful "
            "about any message: Goldwasser and Micali proved this equivalent to semantic security, and it won them "
            "the Turing Award. <bookmark mark='e'/> One consequence is immediate. If encryption is deterministic, "
            "the adversary simply asks for the encryption of m-zero in advance and compares. Secure encryption must "
            "be randomised, which is exactly what our logo was missing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(L), FadeIn(R), Create(vl), Create(vr))
            vo.wait_until("a")
            self.play(FadeIn(arrows[0]))
            self.play(FadeIn(arrows[1]))
            vo.wait_until("b")
            self.play(FadeIn(arrows[2]))
            self.play(FadeIn(arrows[3]))
            vo.wait_until("c")
            self.play(FadeIn(arrows[4]), FadeIn(arrows[5]))
            vo.wait_until("d")
            self.play(FadeIn(lines[0]), FadeIn(lines[1]))
            vo.wait_until("e")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def reductions(self):
        head = label(r"Proof by reduction", font_size=34).to_edge(UP, buff=0.3)
        outer = RoundedRectangle(width=6.2, height=3.0, corner_radius=0.2, stroke_color=YES, stroke_width=2.5).move_to(
            [-2.6, 0.5, 0])
        ot = label(r"$\mathcal{B}$: \ attacks the \textbf{primitive}", font_size=20, color=YES).next_to(
            outer.get_top(), DOWN, buff=0.2)
        inner = flow_box(r"$\mathcal{A}$: \ breaks the \textbf{scheme}", NO, w=3.6, h=1.2, font=20).move_to(
            outer.get_center() + DOWN * 0.35)
        cin = Arrow(outer.get_left() + LEFT * 1.0 + DOWN * 0.35, inner.get_left(), buff=0.05, color=GREY_B,
                    stroke_width=2.5)
        cout = Arrow(inner.get_right(), outer.get_right() + RIGHT * 0.9 + DOWN * 0.35, buff=0.05, color=GREY_B,
                     stroke_width=2.5)
        notes = VGroup(
            label(r"$\mathcal{B}$ simulates the scheme \\ for $\mathcal{A}$, \ using the \\ primitive it is "
                  r"given", font_size=19, color=WHITE),
            label(r"if $\mathcal{A}$ wins with \\ advantage $\varepsilon$, \ $\mathcal{B}$ wins \\ with "
                  r"advantage $\ge \varepsilon / q$", font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(outer, RIGHT, buff=1.2)
        lines = VGroup(
            label(r"so: \ \textit{if the primitive is secure, \ the scheme is secure} \ (contrapositive)", font_size=21,
                  color=YES),
            label(r"nobody can prove any primitive is secure: \ that would prove P $\ne$ NP \ (Part 26)", font_size=21,
                  color=NO),
            label(r"so cryptography is a tower of reductions on a few assumptions, \ attacked for decades", font_size=21,
                  color=WHITE),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "How do you prove a scheme wins this game? Not directly: nobody knows how. Instead, by reduction, the "
            "method of Part 26. <bookmark mark='a'/> Suppose some adversary A breaks the scheme. Build a new "
            "algorithm B that attacks a simpler primitive, say a pseudorandom generator, by running A inside it, "
            "simulating the scheme for A with the primitive it was handed. <bookmark mark='b'/> If A wins with some "
            "advantage, B wins with nearly as much. <bookmark mark='c'/> So if the primitive is secure, the scheme "
            "is. <bookmark mark='d'/> Why not prove the primitive secure too? Because a proof that any efficient "
            "algorithm fails against it would separate P from NP. <bookmark mark='e'/> So cryptography is a tower: "
            "schemes reduced to primitives, primitives reduced to a few hard problems, and the hard problems attacked "
            "by everyone, for decades. The next two chapters build the primitives."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(outer), FadeIn(ot), FadeIn(inner), GrowArrow(cin), GrowArrow(cout), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
            vo.wait_until("e")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()
