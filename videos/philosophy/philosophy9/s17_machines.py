from __future__ import annotations

from videos.philosophy.philosophy9.common import *  # noqa: F403


class Machines(VoiceoverScene):
    def construct(self):
        card = chapter_card(16, r"Proofs by machine", r"What does a machine-checked proof show?", lit=(2022,),
                            part=PART)
        with self.voiceover("Chapter sixteen. Proofs by machine."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.fourcolour()
        self.kernel()
        self.lte()
        self.misstated()
        self.ai()

    def fourcolour(self):
        hcs = VGroup(history_card(1976, r"Kenneth Appel \& Wolfgang Haken", r"the four-colour theorem, \ by computer",
                                  width=5.4, color=HIST),
                     history_card(1979, r"Thomas Tymoczko", r"`The four-color problem and its philosophical "
                                  r"significance'", width=5.6, color=HIST)).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.4)
        rows = VGroup(
            label(r"every map can be coloured with four colours, \ no two neighbours alike", font_size=24, color=NUM),
            label(r"the proof: \ reduce to nearly two thousand configurations, \ each checked by a program", font_size=24),
            label(r"no human has read the whole proof", font_size=24, color=GOAL),
            label(r"Tymoczko: \ such a proof rests on an experiment with a machine: \ mathematics, \ partly empirical",
                  font_size=24, color=BAD),
            label(r"Gonthier (2005): \ the entire proof, \ checked in the proof assistant Coq", font_size=24,
                  color=OK)).arrange(DOWN, buff=0.32).move_to([0, -0.6, 0])
        with self.voiceover(
            "In 1976 the computer entered the proof itself. <bookmark mark='a'/>Kenneth Appel and Wolfgang Haken "
            "proved that every map can be coloured with four colours so that no two neighbouring countries share "
            "one. <bookmark mark='b'/>Their proof reduced the problem to nearly two thousand configurations, each "
            "checked by a program. <bookmark mark='c'/>No human being has read the whole proof. <bookmark mark='d'/>"
            "Thomas Tymoczko argued in 1979 that such a proof rests on an experiment with a machine, so that "
            "mathematics had become, in part, empirical. <bookmark mark='e'/>In 2005 Georges Gonthier checked the "
            "entire proof in the proof assistant Coq, and the question changed: not whether to trust a program, but "
            "which program to trust."
        ) as vo:
            self.play(FadeIn(hcs))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def kernel(self):
        d = load("kernel")
        head = label(r"The de Bruijn criterion: \ a checker small enough to trust", font_size=30,
                     color=CONN).to_edge(UP, buff=0.35)
        lean = code_block([
            "theorem K (A B : Prop) : A → B → A :=",
            "  fun a _ => a",
            "",
            "theorem swap (A B : Prop) : A ∧ B → B ∧ A :=",
            "  fun h => And.intro h.right h.left",
        ], font_size=18, color=GREY_A)
        box = SurroundingRectangle(lean, buff=0.3, corner_radius=0.12, stroke_color=GREY_C, stroke_width=2,
                                   fill_color="#0F141C", fill_opacity=1)
        prog = VGroup(box, lean).move_to([-2.9, 0.9, 0])
        tag = label(r"Lean: \ a proof is a program, \ and checking is type checking \ (Chapter 7)", font_size=21,
                    color=PROOF).next_to(prog, DOWN, buff=0.2)
        side = VGroup(
            label(r"de Bruijn's Automath (1967)", font_size=22, color=HIST),
            VGroup(label(r"trust only a small \textit{kernel};", font_size=21, color=GREY_A),
                   label(r"everything else must pass it", font_size=21, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"the Reasoner's own kernel:", font_size=21, color=OK),
                   label(rf"\texttt{{type\_of}}, \ {d['lines']} lines", font_size=21, color=OK)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"Lean (de Moura, 2013);", font_size=21, color=GREY_A),
                   label(r"Mathlib (2017): \ a community library", font_size=21, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.4, 0.6, 0])
        foot = label(r"a proof search may be huge and untrusted; \ the certificate it produces is checked by the small "
                     r"kernel", font_size=22, color=GOAL).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Proof assistants rest on an idea of Nicolaas de Bruijn, from his Automath project of 1967. "
            "<bookmark mark='a'/>Here are two theorems in Lean, a proof assistant begun by Leonardo de Moura in 2013. "
            "The proof of K is the program that takes a and ignores the rest; the proof of swap builds a new pair "
            "from the parts of the old. Chapter 7's dictionary, in daily use. <bookmark mark='b'/>De Bruijn's "
            "criterion: trust only a small kernel, a type checker short enough to read and understand. Everything "
            "else, however clever, must produce a proof that the kernel accepts. The Reasoner's own kernel, the "
            "function that checked every program in Chapter 7, is forty lines. <bookmark mark='c'/>Lean's community "
            "library, Mathlib, begun in 2017, now holds a large part of an undergraduate degree and much research "
            "mathematics. <bookmark mark='d'/>So proof search can be enormous and untrusted, as long as the "
            "certificate it produces passes the kernel."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(prog), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def lte(self):
        hcs = VGroup(history_card(r"Dec 2020", r"Peter Scholze", r"`Liquid tensor experiment': \ a challenge to check "
                                  r"a theorem of his and Clausen's", width=5.6, color=HIST),
                     history_card(r"July 2022", r"the Lean community, \ led by Johan Commelin", r"the challenge met, \ "
                                  r"after the key step within six months", width=5.6, color=HIST)).arrange(
            RIGHT, buff=0.4).to_edge(UP, buff=0.4)
        rows = VGroup(
            label(r"Scholze: \ he was not fully sure of the proof himself, \ and few readers could check it", font_size=23),
            label(r"the theorem confirmed, \ and the argument simplified along the way", font_size=23, color=OK),
            label(r"Kepler's conjecture \ (Hales, 1998): \ referees `99\% certain'; \ Flyspeck checked it by 2014",
                  font_size=23, color=GREY_A),
            label(r"Tao and collaborators: \ large proofs, \ split among many people, \ trusted because checked",
                  font_size=23, color=GREY_A)).arrange(DOWN, buff=0.32).move_to([0, -0.7, 0])
        with self.voiceover(
            "The proof assistants have reached research mathematics. <bookmark mark='a'/>In December 2020 Peter "
            "Scholze, one of the leading mathematicians of his generation, challenged the Lean community to check a "
            "theorem he and Dustin Clausen had proved. He was not fully confident in it himself, and very few people "
            "could read it. <bookmark mark='b'/>The key step was formalized within six months, and the whole "
            "challenge was met by July 2022. The theorem was confirmed, and along the way the argument was "
            "simplified. <bookmark mark='c'/>Thomas Hales's proof of the Kepler conjecture about packing spheres left "
            "its referees ninety-nine percent certain; his Flyspeck project checked it formally by 2014. "
            "<bookmark mark='d'/>And Terence Tao has run projects in which large proofs are split among many "
            "contributors, people and programs, trusted because every piece is checked."
        ) as vo:
            self.play(FadeIn(hcs[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(hcs[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def misstated(self):
        d = load("euclid")
        head = label(r"A checker certifies what you wrote", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        bad = MathTex(r"\forall n\; \exists p\; \mathrm{prime}(p)", font_size=38, color=BAD)
        good = MathTex(r"\forall n\; \exists p\; (p > n \wedge \mathrm{prime}(p))", font_size=38, color=OK)
        hd = [label(r"$n$", font_size=22, color=P.CLAIM), label(r"a witness, \ as written", font_size=22, color=BAD),
              label(r"a witness, \ as meant", font_size=22, color=OK)]
        rows = [[MathTex(str(n), font_size=24), MathTex(str(p), font_size=24, color=BAD),
                 MathTex(str(q), font_size=24, color=OK)] for (n, p), (_, q) in zip(d["bad"], d["good"])]
        grid = ValueGrid(hd, rows, col_w=[1.2, 2.8, 2.8], cell_h=0.36, font_size=22).move_to([-2.6, -0.9, 0])
        stmts = VGroup(VGroup(label(r"meant: \ there are infinitely many primes", font_size=22, color=GREY_A),
                              good).arrange(DOWN, buff=0.12),
                       VGroup(label(r"written: \ there is a prime", font_size=22, color=GREY_A), bad).arrange(
                           DOWN, buff=0.12)).arrange(DOWN, buff=0.4).move_to([3.6, 0.9, 0])
        moral = VGroup(label(r"the bad statement is true, \ with the witness 2 every time", font_size=22, color=BAD),
                       label(r"trust = \ a small kernel \ + \ reading the statement", font_size=24, color=GOAL),
                       label(r"Pollack (1998): \ `How to believe a machine-checked proof'", font_size=20,
                             color=GREY_B)).arrange(DOWN, buff=0.2).move_to([3.6, -1.9, 0])
        with self.voiceover(
            "But what exactly does a checked proof show? <bookmark mark='a'/>Suppose we want to formalize Euclid's "
            "theorem that there are infinitely many primes: for every n there is a prime bigger than n. "
            "<bookmark mark='b'/>Suppose we slip, and write only: for every n there is a prime. <bookmark mark='c'/>"
            "The checker will happily accept a proof. The Reasoner finds the witness for each n: two, every time. "
            "The intended statement needs a new witness for each n: the next prime. <bookmark mark='d'/>A checker "
            "certifies the statement that was written, not the one that was meant. So trust in a formal proof "
            "rests on two things: a small kernel, and a human who reads the statement. Robert Pollack's paper on "
            "how to believe a machine-checked proof makes exactly this point."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(stmts[0]))
            vo.wait_until("b")
            self.play(FadeIn(stmts[1]))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(len(rows))], lag_ratio=0.15),
                      FadeIn(moral[0]), run_time=4)
            vo.wait_until("d")
            self.play(FadeIn(moral[1]), FadeIn(moral[2]))
        self.clear_scene()

    def ai(self):
        hcs = VGroup(history_card(2024, r"Google DeepMind", r"AlphaProof and AlphaGeometry 2: \ International "
                                  r"Mathematical Olympiad, \ silver-medal standard \ (28 of 42 points)", width=6.2,
                                  color=HIST),
                     history_card(2025, r"several laboratories", r"gold-medal standard \ (35 of 42), \ in natural "
                                  r"language; \ also in Lean", width=6.0, color=HIST)).arrange(RIGHT, buff=0.4).to_edge(
            UP, buff=0.35)
        rows = VGroup(
            label(r"AlphaProof wrote its proofs in Lean: \ certain, \ whoever or whatever found them", font_size=23,
                  color=OK),
            label(r"a proof may be certain \ and still not understood", font_size=24, color=GOAL),
            label(r"Thurston (1994), \ `On proof and progress in mathematics': \ the aim is human understanding",
                  font_size=23, color=GREY_A),
            label(r"the Reasoner's view: \ the kernel settles \textit{that}; \ explanation \ (Chapter 15) \ is "
                  r"still \textit{why}", font_size=23, color=PROOF)).arrange(DOWN, buff=0.32).move_to([0, -0.9, 0])
        with self.voiceover(
            "And now machines find proofs, as well as check them. <bookmark mark='a'/>In 2024 Google DeepMind's "
            "systems AlphaProof and AlphaGeometry 2 solved four of the six problems at the International "
            "Mathematical Olympiad, the standard of a silver medal, and AlphaProof's proofs were written in Lean, so "
            "they are certain, whoever or whatever found them. <bookmark mark='b'/>In 2025 systems from several "
            "laboratories reached the standard of a gold medal, some writing in ordinary mathematical language, "
            "others in Lean. <bookmark mark='c'/>That raises an old question in a new form. A proof can be certain, "
            "and still not understood. <bookmark mark='d'/>William Thurston argued in 1994 that the point of "
            "mathematics is not a stock of certified theorems, but human understanding. <bookmark mark='e'/>The "
            "kernel settles that a theorem is true. Why it is true, the question of Chapter 15, is still ours to "
            "answer."
        ) as vo:
            self.play(FadeIn(hcs[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(hcs[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
