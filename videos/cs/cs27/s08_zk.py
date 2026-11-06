from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs27.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table, load, mono)

PAL = [DATA, HEAD, YES]


def petersen(center, r1=1.5, r2=0.75):
    pos = []
    for i in range(5):
        a = PI / 2 + 2 * PI * i / 5
        pos.append(center + r1 * np.array([np.cos(a), np.sin(a), 0]))
    for i in range(5):
        a = PI / 2 + 2 * PI * i / 5
        pos.append(center + r2 * np.array([np.cos(a), np.sin(a), 0]))
    return pos


class ZeroKnowledge(VoiceoverScene):
    def construct(self):
        self.card()
        self.cave()
        self.protocol()
        self.measured()
        self.simulator()

    def card(self):
        card = chapter_card(7, r"Zero knowledge", r"Can you prove something without revealing anything else?",
                            lit=(1985, 1986), extra=((1985, r"GMR"), (1986, r"Goldreich--Micali--Wigderson")),
                            part=PART)
        with self.voiceover("Chapter seven. Zero knowledge."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def cave(self):
        head = label(r"Ali Baba's cave", font_size=34).to_edge(UP, buff=0.35)
        ring = Annulus(inner_radius=1.0, outer_radius=1.5, color=GREY_D, fill_opacity=0.6).shift(LEFT * 3.4)
        door = Line(ring.get_center() + UP * 1.0, ring.get_center() + UP * 1.5, color=NO, stroke_width=8)
        entr = Rectangle(width=0.5, height=1.0, color=GREY_D, fill_opacity=0.6).next_to(ring, DOWN, buff=-0.05)
        la = label(r"A", font_size=22, color=DATA).move_to(ring.get_center() + LEFT * 1.25)
        lb = label(r"B", font_size=22, color=HEAD).move_to(ring.get_center() + RIGHT * 1.25)
        lines = VGroup(
            label(r"a ring-shaped cave, \ a magic door at the back", font_size=21, color=WHITE),
            label(r"Peggy enters by path A or B; \ Victor then shouts which path to come back by", font_size=21,
                  color=DATA),
            label(r"if she knows the word, \ she always can; \ if not, \ she is caught half the time", font_size=21,
                  color=NO),
            label(r"20 rounds: \ a bluffer survives with probability $2^{-20}$", font_size=21, color=HEAD),
            label(r"Victor learns \textbf{nothing} about the word: \ he could have filmed the same video with an "
                  r"actor \\ by editing out the failures", font_size=21, color=YES),
            label(r"Quisquater and others, \ ``How to explain zero-knowledge protocols to your children'' \ (1989)",
                  font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ring, RIGHT, buff=0.8)
        fit_right(lines)
        with self.voiceover(
            "Here is the classic story. <bookmark mark='a'/> A cave is shaped like a ring, with a door at the back "
            "that opens only with a secret word. <bookmark mark='b'/> Peggy walks in by one of two paths while Victor "
            "waits outside. Then Victor shouts which path she should come back by. <bookmark mark='c'/> If she "
            "knows the word, she can always comply, opening the door if needed. If not, she is caught half the time. "
            "<bookmark mark='d'/> After twenty rounds, a bluffer survives with probability one in a million. "
            "<bookmark mark='e'/> And Victor learns nothing about the word. He could have produced an identical "
            "video with an actor who doesn't know it, by simply editing out the failed rounds. <bookmark mark='f'/> "
            "That is the definition of zero knowledge: whatever the verifier sees, he could have simulated himself."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ring), FadeIn(door), FadeIn(entr), FadeIn(la), FadeIn(lb))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def protocol(self):
        z = load("zk")
        head = label(r"A zero-knowledge proof of 3-colourability \ (GMW, 1986)", font_size=30).to_edge(UP, buff=0.3)
        pos = petersen(LEFT * 3.8 + DOWN * 0.3)
        edges = z["edges"]
        es = VGroup(*[Line(pos[u], pos[v], stroke_width=2, color=GREY_B) for u, v in edges])
        boxes = VGroup(*[VGroup(Square(side_length=0.32, color=GREY_A, fill_color=GREY_D, fill_opacity=1).move_to(p),
                                mono("?", 14, WHITE).move_to(p)) for p in pos])
        u, v = edges[7]
        opened = VGroup(*[Circle(radius=0.17, color=PAL[c], fill_opacity=1).move_to(pos[w])
                          for w, c in ((u, (z["colouring"][u] + 1) % 3), (v, (z["colouring"][v] + 1) % 3))])
        hl = Line(pos[u], pos[v], stroke_width=6, color=LAM)
        steps = VGroup(
            label(r"1. \ the prover \textbf{permutes} the three colours at random", font_size=20, color=WHITE),
            label(r"2. \ commits to every vertex's colour: \ a hash $H(\text{nonce} \,\|\, \text{colour})$ \\ "
                  r"(binding: \ can't change it; \ hiding: \ reveals nothing)", font_size=20, color=DATA),
            label(r"3. \ the verifier picks one random \textbf{edge}", font_size=20, color=LAM),
            label(r"4. \ the prover opens just those two commitments", font_size=20, color=WHITE),
            label(r"5. \ accept if the two colours differ; \ repeat with fresh colours", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5).shift(UP * 0.4)
        fit_right(steps)
        with self.voiceover(
            "Oded Goldreich, Silvio Micali and Avi Wigderson showed in 1986 that every problem in NP has a "
            "zero-knowledge proof, through three-colouring. Here is the Petersen graph, which the prover knows how to "
            "colour. <bookmark mark='a'/> Each round, the prover first shuffles the three colours at random, <bookmark "
            "mark='b'/> then commits to every vertex's colour, here by publishing a hash of a random nonce and the "
            "colour. It cannot change a colour later, and the hash reveals nothing. <bookmark mark='c'/> The verifier "
            "points at one edge. <bookmark mark='d'/> The prover opens the two commitments at its ends, <bookmark "
            "mark='e'/> and the verifier checks that the colours differ and the hashes match. Then everything starts "
            "again with a fresh shuffle."
        ) as vo:
            self.play(FadeIn(head), Create(es), FadeIn(boxes))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(Create(hl), FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(opened), FadeIn(steps[3]))
            vo.wait_until("e")
            self.play(FadeIn(steps[4]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        z = load("zk")
        head = label(r"A cheater, \ measured", font_size=34).to_edge(UP, buff=0.35)
        rows = [[str(r["k"]), f"{r['empirical']:.4f}", f"{r['theory']:.4f}"] for r in z["survive"]]
        tab = grid_table([r"rounds $k$", r"survived \ (2,000 runs)", r"$(1 - 2/15)^k$"], rows, widths=[2.0, 3.2, 2.6],
                         row_h=0.42, font_size=20, mono_cols=(), colors=[[WHITE, NO, GREY_A]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=1.0)
        notes = VGroup(
            label(rf"a cheating prover with a colouring that has \\ {z['bad_edges']} bad edges out of {z['m']}",
                  font_size=21, color=WHITE),
            label(r"caught whenever the verifier picks a bad edge", font_size=21, color=NO),
            label(r"with one bad edge, \ the worst case: \\ survival $(1 - 1/m)^k$", font_size=21, color=HEAD),
            label(rf"{z['rounds_for_1e9']} rounds make it $< 10^{{-9}}$", font_size=22, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(tab, RIGHT, buff=0.7).align_to(tab, UP)
        fit_right(notes)
        with self.voiceover(
            "Is it sound? <bookmark mark='a'/> We gave a cheating prover a colouring with two bad edges out of "
            "fifteen. <bookmark mark='b'/> It is caught whenever the verifier picks one of them. <bookmark "
            "mark='c'/> In two thousand runs, the fraction still undetected after k rounds follows one minus two "
            "fifteenths to the k: forty-seven percent after five rounds, six percent after twenty. A cheater with a "
            "single bad edge survives longer, one minus one over m to the k. <bookmark mark='d'/> Three hundred and "
            "one rounds push even that below one in a billion."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab), FadeIn(notes[0]))
            for mk, n_ in zip("bcd", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def simulator(self):
        z = load("zk")
        head = label(r"Why the verifier learns nothing", font_size=34).to_edge(UP, buff=0.3)
        pairs = z["dist"]["pairs"]
        names = [f"{a + 1}{b + 1}" for a, b in pairs]
        bars = VGroup()
        for k, (r, sm) in enumerate(zip(z["dist"]["real"], z["dist"]["sim"])):
            b1 = Rectangle(width=0.32, height=r * 12, stroke_width=0, fill_color=DATA, fill_opacity=0.85)
            b2 = Rectangle(width=0.32, height=sm * 12, stroke_width=0, fill_color=HEAD, fill_opacity=0.85)
            b1.move_to([k * 1.0, r * 6, 0])
            b2.move_to([k * 1.0 + 0.36, sm * 6, 0])
            nm = mono(names[k], 16, GREY_A).move_to([k * 1.0 + 0.18, -0.25, 0])
            bars.add(VGroup(b1, b2, nm))
        bars.next_to(head, DOWN, buff=0.7).to_edge(LEFT, buff=1.0)
        leg = VGroup(label(r"real transcripts", font_size=19, color=DATA),
                     label(r"simulated, \ no colouring known", font_size=19, color=HEAD)).arrange(RIGHT, buff=0.5)
        leg.next_to(bars, DOWN, buff=0.4)
        lines = VGroup(
            label(r"what the verifier sees each round: \\ two different colours, \ uniformly random", font_size=21,
                  color=WHITE),
            label(r"a \textbf{simulator} with no colouring \\ can produce exactly that: \\ pick two different colours "
                  r"at random", font_size=21, color=HEAD),
            label(r"6,000 rounds each: \ every pair near $\tfrac16$", font_size=21, color=YES),
            label(r"so the transcript carries no information \\ the verifier couldn't have made itself", font_size=21,
                  color=DATA),
            label(r"Fiat--Shamir: \ replace the verifier's coins by a hash \\ and the proof becomes a signature \ "
                  r"(Part 30)", font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(bars, RIGHT, buff=0.8).align_to(bars, UP)
        fit_right(lines)
        with self.voiceover(
            "And what does the verifier learn? <bookmark mark='a'/> In each round it sees two different colours at "
            "the ends of an edge. Because the colours were freshly shuffled, the pair is uniformly random. <bookmark "
            "mark='b'/> A simulator that knows no colouring at all can produce exactly the same thing: pick two "
            "different colours at random. <bookmark mark='c'/> Over six thousand rounds each, the real and simulated "
            "transcripts show every ordered pair about one sixth of the time. <bookmark mark='d'/> Anything the "
            "verifier could compute from the conversation, it could have computed from the simulation, so it learns "
            "nothing beyond the fact that the graph is colourable. <bookmark mark='e'/> Amos Fiat and Adi Shamir "
            "showed how to replace the verifier's coins with a hash of the conversation, turning such proofs into "
            "signatures; Part 30 uses it, and so do today's blockchains."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars), FadeIn(leg))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
