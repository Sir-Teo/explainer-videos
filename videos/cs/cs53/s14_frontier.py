from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs53.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


def tile(title, body, col, w=4.2, h=3.0):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=col, stroke_width=2, fill_color=BG,
                             fill_opacity=1)
    t = label(title, font_size=22, color=col)
    b = wrapped_label(body, w - 0.4, font_size=18, color=GREY_A)
    VGroup(t, b).arrange(DOWN, buff=0.3).move_to(frame)
    return VGroup(frame, t, b)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.keys()
        self.rsa()
        self.uses()
        self.open()

    def card(self):
        card = chapter_card(13, r"Frontier: \ keys, \ chemistry and the hardware",
                            r"What will quantum computers actually change, \ and when?", lit=(1984, 2024),
                            extra=((1984, r"Bennett and Brassard: \ BB84"),
                                   (2024, r"NIST's post-quantum standards")), part=PART)
        with self.voiceover("Chapter thirteen, the frontier. What will quantum computers actually change, and when?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def keys(self):
        b = load("bb84")
        head = label(r"Quantum mechanics against eavesdroppers", font_size=36).to_edge(UP, buff=0.3)
        n = 16
        import random
        rng = random.Random(4)
        bits = [rng.randint(0, 1) for _ in range(n)]
        ab = [rng.randint(0, 1) for _ in range(n)]
        bb = [rng.randint(0, 1) for _ in range(n)]
        sym = {0: (r"$|0\rangle$", r"$|1\rangle$"), 1: (r"$|{+}\rangle$", r"$|{-}\rangle$")}
        cells = VGroup()
        for i in range(n):
            col = VGroup(label(str(bits[i]), font_size=20, color=WHITE),
                         label(sym[ab[i]][bits[i]], font_size=20, color=DATA),
                         label(r"$Z$" if bb[i] == 0 else r"$X$", font_size=20, color=KERN),
                         label(r"keep" if ab[i] == bb[i] else r"---", font_size=16,
                               color=YES if ab[i] == bb[i] else GREY_D)).arrange(DOWN, buff=0.22)
            cells.add(col)
        cells.arrange(RIGHT, buff=0.28).next_to(head, DOWN, buff=0.6).shift(RIGHT * 0.9)
        names = VGroup(*[label(t, font_size=17, color=GREY_B) for t in (r"Alice's bit", r"sent as", r"Bob measures",
                                                                         r"bases agree?")])
        for nm, k in zip(names, range(4)):
            nm.next_to(cells[0][k], LEFT, buff=0.5)
        names.align_to(names[0], RIGHT)
        res = VGroup(label(rf"no eavesdropper: \ {100 * b['honest']['error_rate']:.0f}\% errors in the "
                           rf"{b['honest']['kept']:,} kept bits", font_size=21, color=YES),
                     label(rf"an eavesdropper measuring and resending: \ {100 * b['eve']['error_rate']:.1f}\% errors "
                           r"\ (theory: 25\%)", font_size=21, color=NO)).arrange(DOWN, buff=0.18)
        res.next_to(cells, DOWN, buff=0.5)
        pqc = wrapped_label(r"the other defence needs no quantum hardware: \ NIST's 2024 post-quantum standards \ "
                            r"(ML-KEM, \ ML-DSA, \ SLH-DSA) \ replace RSA and elliptic curves with problems not known "
                            r"to fall to Shor", 12.4, font_size=19, color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Quantum mechanics also protects secrets. <bookmark mark='a'/> In Bennett and Brassard's protocol of "
            "1984, Alice sends random bits, each encoded in one of two bases chosen at random. Bob measures each in "
            "a random basis, and afterwards they compare bases in public and keep only the positions where they "
            "agreed. <bookmark mark='b'/> With nobody listening, our simulation's kept bits agree perfectly. "
            "<bookmark mark='c'/> An eavesdropper must measure to learn anything, and measuring in the wrong basis "
            "disturbs the state: a quarter of the kept bits come out wrong, and Alice and Bob notice. "
            "<bookmark mark='d'/> The more urgent defence needs no quantum hardware at all. In 2024 the United "
            "States standards body NIST published post-quantum algorithms that replace RSA and elliptic curves with "
            "lattice and hash-based problems not known to fall to Shor's algorithm, and the migration is under way, "
            "because data recorded today could be decrypted later."
        ) as vo:
            self.play(FadeIn(head), FadeIn(names))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c[:3]) for c in cells], lag_ratio=0.05), run_time=2)
            self.play(LaggedStart(*[FadeIn(c[3]) for c in cells], lag_ratio=0.05))
            vo.wait_until("b")
            self.play(FadeIn(res[0]))
            vo.wait_until("c")
            self.play(FadeIn(res[1]))
            vo.wait_until("d")
            self.play(FadeIn(pqc))
        self.wait(0.4)
        self.clear_scene()

    def rsa(self):
        r = load("repetition")
        head = label(r"How far is RSA-2048?", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r"Gidney and Eker\aa{}, \ 2019", r"about 20 million", r"about 8 hours"],
                [r"Gidney, \ 2025", r"under 1 million", r"under a week"]]
        tab = grid_table([r"resource estimate", r"noisy physical qubits", r"time"], rows, widths=[4.6, 3.6, 3.0],
                         row_h=0.55, font_size=19, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5)
        hw = wrapped_label(r"both assume physical error rates of about one in a thousand and surface-code error "
                           r"correction; \ the largest machines today have on the order of a hundred to a thousand "
                           r"physical qubits", 12.0, font_size=19, color=GREY_A).next_to(tab, DOWN, buff=0.35)
        lam = r["lambda"]["0.01"][0]
        qec = wrapped_label(r"Google Quantum AI, \ 2024: \ growing a surface code from distance 3 to 5 to 7 cut the "
                            r"logical error rate by about half at each step: \ below threshold, \ for the first time; "
                            rf"\ our repetition code at $p = 1\%$ divides it by about {lam:.0f} per step, \ but it "
                            r"protects against only one kind of error", 12.0, font_size=19,
                            color=YES).next_to(hw, DOWN, buff=0.35)
        foot = note(r"estimates as published; \ hardware figures approximate", font_size=16).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "How far away is a machine that breaks today's cryptography? <bookmark mark='a'/> Resource estimates "
            "have fallen fast. In 2019 Craig Gidney and Martin Ekerå estimated that factoring a 2048-bit RSA key "
            "would take about twenty million noisy qubits for about eight hours. In 2025 Gidney brought that "
            "under a million qubits, in under a week. <bookmark mark='b'/> Both assume physical error rates of "
            "about one in a thousand, and the surface code of chapter twelve; today's largest machines have "
            "hundreds to about a thousand physical qubits. <bookmark mark='c'/> The decisive step is error "
            "correction that improves as the code grows, and in 2024 Google's team showed it: each step up in "
            "distance roughly halved the logical error rate. Our repetition code does far better on paper, but it "
            "only corrects bit flips, while a real code must also catch phase errors."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])),
                      LaggedStart(*[FadeIn(VGroup(*c)) for c in tab.cells[1:]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(hw))
            vo.wait_until("c")
            self.play(FadeIn(qec))
        self.wait(0.4)
        self.clear_scene()

    def uses(self):
        head = label(r"What quantum computers are expected to be good for", font_size=36).to_edge(UP, buff=0.3)
        tiles = VGroup(
            tile(r"simulating nature", r"Feynman's original problem: \ molecules, \ catalysts and materials whose "
                 r"electrons are too entangled for classical methods", YES),
            tile(r"cryptanalysis", r"Shor's algorithm against RSA and elliptic curves; \ the reason post-quantum "
                 r"migration has already begun", NO),
            tile(r"less certain", r"optimization and machine learning: \ claimed speedups are often matched by "
                 r"classical algorithms once examined \ (Tang, \ 2018)", HEAD),
        ).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.6)
        foot = wrapped_label(r"demonstrations of quantum advantage on sampling tasks \ (2019 onwards) \ have "
                             r"repeatedly been challenged by better classical simulations; \ the contest continues",
                             12.4,
                             font_size=20, color=WHITE).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "What are they likely to be good for? <bookmark mark='a'/> First, Feynman's own problem: simulating "
            "molecules and materials whose electrons are too entangled for classical methods, where a quantum "
            "computer simply is the right kind of machine. <bookmark mark='b'/> Second, cryptanalysis, which is why "
            "the migration to new cryptography has already begun. <bookmark mark='c'/> Elsewhere the case is weaker. "
            "Several proposed quantum speedups for recommendation systems and optimization were matched by new "
            "classical algorithms once examined closely, starting with Ewin Tang's in 2018. <bookmark mark='d'/> "
            "Claims of quantum advantage on sampling tasks, from 2019 on, have repeatedly been challenged by better "
            "classical simulations. The contest continues, which is how it should be."
        ) as vo:
            self.play(FadeIn(head))
            for mk, t in zip("abc", tiles):
                vo.wait_until(mk)
                self.play(FadeIn(t, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def open(self):
        head = label(r"Open", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(
            wrapped_label(r"1. \ \textbf{BQP against NP}: \ no quantum algorithm is known to solve NP-complete "
                          r"problems fast, \ and none is expected.", 12.4, font_size=24, color=WHITE),
            wrapped_label(r"2. \ \textbf{Useful advantage}: \ a practical problem with a proven, \ verifiable "
                          r"exponential speedup.", 12.4, font_size=24, color=YES),
            wrapped_label(r"3. \ \textbf{Is factoring classically hard?} \ Unproved, \ like every lower bound of Part "
                          r"26.", 12.4, font_size=24, color=HEAD),
            wrapped_label(r"4. \ \textbf{Better codes}: \ fewer physical qubits per logical qubit than the surface "
                          r"code.", 12.4, font_size=24, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45)
        star = wrapped_label(r"$\bigstar$ \ this part's research problem: \ the least space-time volume of "
                             r"physical qubits needed to factor a 2048-bit number at a physical error rate of "
                             r"$10^{-3}$, \ and a lower bound to match", 12.4, font_size=23,
                             color=LAM).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Open problems. <bookmark mark='a'/> Whether quantum computers can solve NP-complete problems quickly: "
            "no algorithm is known, and most researchers expect none. <bookmark mark='b'/> A practical problem with "
            "a proven, verifiable exponential speedup. <bookmark mark='c'/> Whether factoring is hard for classical "
            "computers at all, which, like every lower bound in Part 26, nobody can prove. <bookmark mark='d'/> And "
            "codes that need fewer physical qubits per logical one. <bookmark mark='e'/> This part's research problem "
            "asks how small the machine that factors a 2048-bit number can be: the least space-time volume of "
            "physical qubits at an error rate of one in a thousand, with a lower bound to match."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.6)
        self.clear_scene()


_ = (DATA, KERN, LAM, NO, YES)
