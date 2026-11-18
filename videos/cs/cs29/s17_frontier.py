from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs29.common import (DATA, HEAD, LAM, NO, PART, YES, flow_box)


class Frontier(WatchScene):
    def construct(self):
        self.card()
        self.minicrypt()
        self.quantum()

    def card(self):
        self.chapter(16, r"Frontier: \ proofs, \ quanta and lightweight ciphers", r"What is still unknown about secrets?", lit=(1999, 2020, 2023), extra=((1999, r"H\aa stad et al.: \ PRGs from any OWF"), (2016, r"Simon's algorithm "
                                                                                          r"vs.\ modes"),
                                   (2020, r"Liu--Pass"), (2023, r"Ascon")), part=PART, said="Chapter sixteen. The frontier: proofs, quantum attackers, and lightweight ciphers.")

    def minicrypt(self):
        head = label(r"One assumption under everything", font_size=34).to_edge(UP, buff=0.3)
        owf = flow_box(r"one-way functions", YES, w=3.0, h=0.8, font=22).move_to([0, 0.6, 0])
        outs = [(r"PRGs \\ (H\aa stad et al.\ 1999)", [-4.6, 2.2]), (r"PRFs \\ (GGM 1986)", [-1.6, 2.4]),
                (r"PRPs \\ (Luby--Rackoff)", [1.6, 2.4]), (r"MACs, \ encryption", [4.6, 2.2]),
                (r"commitments \\ (Naor 1991)", [-4.6, -0.6]), (r"signatures \\ (Rompel 1990)", [4.6, -0.6])]
        boxes = VGroup(*[flow_box(t, DATA, w=2.5, h=0.9, font=18).move_to([x, y, 0]) for t, (x, y) in outs])
        arrows = VGroup()
        for b in boxes:
            if b.get_y() > owf.get_y() + 0.5:
                st, en = owf.get_top() + RIGHT * 0.5 * np.sign(b.get_x()), b.get_bottom()
            else:
                st = owf.get_left() if b.get_x() < 0 else owf.get_right()
                en = b.get_right() if b.get_x() < 0 else b.get_left()
            arrows.add(Arrow(st, en, buff=0.08, stroke_width=2.5, color=GREY_B))
        pnp = flow_box(r"P $\ne$ NP", NO, w=2.0, h=0.7, font=22).move_to([0, -1.0, 0])
        pa = Arrow(owf.get_bottom(), pnp.get_top(), buff=0.08, stroke_width=2.5, color=NO)
        lines = VGroup(
            label(r"Impagliazzo's \textbf{Minicrypt}: \ all of symmetric cryptography exists iff one-way functions do",
                  font_size=21, color=WHITE),
            label(r"and one-way functions imply P $\ne$ NP: \ so no proof is coming soon", font_size=21, color=NO),
            label(r"Liu and Pass \ (2020): \ one-way functions exist iff time-bounded Kolmogorov complexity is mildly "
                  r"hard on average", font_size=21, color=HEAD),
            label(r"AES and SHA-256 sit outside the theory: \ conjectured PRP and hash, \ backed by cryptanalysis "
                  r"alone", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.17).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The theory in this part has a remarkable shape. <bookmark mark='a'/> From any one-way function, a "
            "function easy to compute and hard to invert, you can build pseudorandom generators, pseudorandom "
            "functions and permutations, secure encryption and MACs, commitments, even digital signatures. And each "
            "of these gives back a one-way function. Russell Impagliazzo called this world Minicrypt: all of "
            "symmetric cryptography stands or falls with one assumption. <bookmark mark='b'/> But one-way functions "
            "imply that P is not NP, so a proof that they exist would settle Part 26's question, and more. <bookmark "
            "mark='c'/> In 2020 Yanyi Liu and Rafael Pass found an unexpected equivalent: one-way functions exist "
            "exactly when a problem about the compressibility of strings, time-bounded Kolmogorov complexity, is "
            "mildly hard on average. Cryptography and the theory of information turned out to be one question. "
            "<bookmark mark='d'/> Meanwhile the ciphers we actually use are not built from one-way functions at all. "
            "AES is conjectured to be a pseudorandom permutation, and the only evidence is that no one has broken it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(owf))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(b)) for a, b in zip(arrows, boxes)],
                                  lag_ratio=0.3), FadeIn(lines[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(GrowArrow(pa), FadeIn(pnp), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def quantum(self):
        self.ask(r"Grover's search against a 128-bit key. \\ Effective strength:", [r"$128$ bits", r"$64$ bits",
                 r"none"], 1,
                 say="A quantum computer runs Grover's search against a hundred-and-twenty-eight-bit key. How strong is the key then?",
                 reveal="About sixty-four bits: Grover takes a square root. Doubling the key restores the margin.")
        head = label(r"Quantum attackers", font_size=34).to_edge(UP, buff=0.3)
        lines = VGroup(
            label(r"\textbf{Grover} \ (1996): \ search $2^k$ keys in about $2^{k/2}$ quantum steps \ (Part 53)",
                  font_size=22, color=WHITE),
            label(r"but the steps are sequential: \ split the work over $m$ machines and each still needs "
                  r"$2^{k/2}/\sqrt{m}$", font_size=22, color=GREY_A),
            label(r"so AES-128 is still judged adequate, \ and AES-256 is the conservative choice for decades-long "
                  r"secrets", font_size=22, color=YES),
            label(r"\textbf{Simon's algorithm} breaks 3-round Feistel, \ Even--Mansour, \ CBC-MAC and GCM \ "
                  r"(Kuwakado--Morii, \ Kaplan et al.\ 2016)", font_size=22, color=NO),
            label(r"\ldots\ but only if the attacker can query the \textbf{keyed} cipher in superposition", font_size=22,
                  color=HEAD),
            label(r"open: \ which symmetric designs stay secure in that model, \ and what quantum computers really "
                  r"cost", font_size=22, color=LAM),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Public-key cryptography falls to a large quantum computer, as Part 30 explains. Symmetric cryptography "
            "fares better. <bookmark mark='a'/> Lov Grover's algorithm, which Part 53 builds, searches two to the k "
            "keys in about two to the k over two quantum steps: a square root. <bookmark mark='b'/> But those steps "
            "must run one after another. Spreading the search over many machines helps only by the square root of "
            "their number, and each step needs error-corrected quantum hardware. <bookmark mark='c'/> So AES-128 is "
            "still judged adequate by the standards bodies, and AES-256 is the conservative choice for secrets that "
            "must last decades. <bookmark mark='d'/> A stranger threat came from Daniel Simon's algorithm, which "
            "finds hidden periods. From 2010 on, researchers used it to break the three-round Feistel network, the "
            "Even-Mansour cipher, CBC-MAC and GCM's authentication in polynomial time. <bookmark mark='e'/> The "
            "catch: the attacker must be able to run the keyed cipher on a superposition of inputs, which a remote "
            "server never allows. <bookmark mark='f'/> Which designs survive even that, and what a real quantum "
            "attack would cost, are active questions."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()


