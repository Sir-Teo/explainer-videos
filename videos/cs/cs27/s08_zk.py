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
            label('2. commit to every colour with a salted hash; binding/hiding require assumptions', font_size=20, color=DATA),
            label(r"3. \ the verifier picks one random \textbf{edge}", font_size=20, color=LAM),
            label(r"4. \ the prover opens just those two commitments", font_size=20, color=WHITE),
            label(r"5. \ accept if the two colours differ; \ repeat with fresh colours", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5).shift(UP * 0.4)
        fit_right(steps)
        with self.voiceover(
            "Goldreich, Micali and Wigderson obtained zero-knowledge proofs for NP using suitable commitments and reductions. Here is the three-colouring teaching protocol. <bookmark mark='a'/> Every round freshly permutes the three colours. <bookmark mark='b'/> The prover commits to each vertex using a salted hash. Binding and hiding require computational assumptions; a fixed hash and a seeded Python generator do not supply an unconditional security theorem. <bookmark mark='c'/> The honest verifier uniformly selects an edge only after commitments have been sent. <bookmark mark='d'/> The prover opens the endpoint commitments, and the verifier checks both hashes and the two colours. Our full public commitment and opening records are retained. <bookmark mark='e'/> Different colours pass; equal colours fail. Fresh independent rounds amplify soundness under the commitment assumptions. The public graph and the claim of colourability are already known to the verifier."
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
            "The measured cheating experiment fixes an invalid colouring rather than solving a cryptographic attack. <bookmark mark='a'/> The supplied colouring has two bad edges among fifteen. <bookmark mark='b'/> With independent uniform edge challenges and binding commitments, it survives k rounds with probability thirteen fifteenths to the k. The table compares two thousand actual trials with this exact finite model. <bookmark mark='c'/> A colouring with only one bad edge has the weaker survival bound one minus one over the number of edges, raised to k. <bookmark mark='d'/> Three hundred and one rounds put that bound below one in a billion. These probabilities assume correct commitment binding and independent challenges; our seeded experiment demonstrates the mechanics."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab), FadeIn(notes[0]))
            for mk, n_ in zip("bcd", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def simulator(self):
        z = load("zk")
        head = label('Opened-colour marginals; full zero knowledge needs more', font_size=34).to_edge(UP, buff=0.3)
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
        leg = VGroup(label('real opened-colour pairs', font_size=19, color=DATA),
                     label(r"simulated, \ no colouring known", font_size=19, color=HEAD)).arrange(RIGHT, buff=0.5)
        leg.next_to(bars, DOWN, buff=0.4)
        lines = VGroup(
            label(r"what the verifier sees each round: \\ two different colours, \ uniformly random", font_size=21,
                  color=WHITE),
            label('a simulator samples the same ordered-colour-pair marginal without a colouring', font_size=21, color=HEAD),
            label(r"6,000 rounds each: \ every pair near $\tfrac16$", font_size=21, color=YES),
            label('this histogram checks a marginal; full simulation must include commitments and verifier state', font_size=21,
                  color=DATA),
            label('Fiat--Shamir: suitable public-coin protocols, transcript binding and additional security analysis', font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(bars, RIGHT, buff=0.8).align_to(bars, UP)
        fit_right(lines)
        with self.voiceover(
            "The histogram measures one carefully limited part of the verifier’s view. <bookmark mark='a'/> For a valid colouring and a fresh uniform colour permutation, the two opened endpoint colours form a uniform ordered pair of distinct colours. <bookmark mark='b'/> A simulator can sample that pair distribution without knowing the colouring. This equality is exact for the marginal distribution. <bookmark mark='c'/> Six thousand real and simulated pair samples fluctuate around one sixth for each ordered pair. Their empirical similarity alone is not a proof of zero knowledge. <bookmark mark='d'/> A complete zero-knowledge argument must simulate commitments, openings, verifier randomness and the full interaction. It uses the commitment assumptions and, for arbitrary verifiers, the appropriate simulator and rewinding analysis. <bookmark mark='e'/> Fiat–Shamir can remove interaction from suitable public-coin protocols under additional security conditions. It is not a universal transformation from any proof into a secure signature. Our exercise is explicitly a transcript-bound teaching demonstration."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars), FadeIn(leg))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
