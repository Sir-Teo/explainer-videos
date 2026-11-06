from __future__ import annotations

from videos.philosophy.philosophy18.common import *  # noqa: F403


def tick(ok: bool) -> str:
    return r"$\checkmark$" if ok else r"$\times$"


class Vienna(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Meaning and verification", r"Is a statement meaningless if nothing could check it?",
                            lit=(1929, 1949), part=PART)
        with self.voiceover("Chapter one. Meaning and verification."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.circle()
        self.criterion()
        self.church()
        self.boat()
        self.legacy()

    def circle(self):
        hc = history_card(1929, r"The Vienna Circle", r"`The Scientific Conception of the World'", width=6.4,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = [
            (r"members", r"Schlick, \ Carnap, \ Neurath, \ Hahn, \ Feigl, \ G\"odel attended; \ Wittgenstein and "
                         r"Popper on the edge", GREY_A),
            (r"the programme", r"unify the sciences on logic plus experience; \ eliminate metaphysics", THEORY),
            (r"the weapon", r"the verification principle: \ a statement's meaning is its method of verification", REAL),
            (r"the casualties", r"`the Absolute enters into, \ but is itself incapable of, \ evolution and "
                                r"progress' \ (Bradley, \ in Ayer); \ `the nothing itself nothings' \ (Heidegger, \ "
                                r"in Carnap)", BAD),
            (r"Ayer \ (1936)", r"\textit{Language, Truth and Logic}: \ the principle in English, \ for everyone", ANTI),
        ]
        g = rows_table(rows, top=1.3, gap=0.42, width=8.6, x_text=-3.0)
        with self.voiceover(
            "Philosophy of science as a discipline began in a Viennese seminar. <bookmark mark='a'/>Moritz Schlick, "
            "Rudolf Carnap, Otto Neurath, Hans Hahn and Herbert Feigl met weekly; the young Kurt Gödel attended; "
            "Wittgenstein and Popper stood at the edge. <bookmark mark='b'/>Their programme was to unify the "
            "sciences on two foundations, logic and experience, and to eliminate metaphysics. "
            "<bookmark mark='c'/>Their weapon was the verification principle: the meaning of a statement is its "
            "method of verification. <bookmark mark='d'/>A sentence that no observation could ever bear on is not "
            "false, but meaningless. Ayer's example was F. H. Bradley's claim that the Absolute enters into, but is "
            "itself incapable of, evolution and progress; Carnap's target was Heidegger's sentence, the nothing "
            "itself nothings. <bookmark mark='e'/>A. J. Ayer brought the "
            "principle to English readers in 1936."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def criterion(self):
        head = label(r"Making the criterion precise", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"strong verification", r"conclusively verifiable by finite observation: \ kills `all electrons are "
                                     r"charged', \ every universal law", BAD),
            (r"falsifiability", r"conclusively refutable: \ kills `some electron is neutral' \ and every existential "
                                r"claim; \ `all men are mortal' survives, \ `everyone has a mother' does not", BAD),
            (r"weak verification", r"observation must be \textit{relevant}: \ Ayer \ (1946) \ makes it exact, \ via "
                                   r"entailment", GOAL),
            (r"self-reference", r"is the principle itself verifiable? \ If not, \ by its own lights it is "
                                r"meaningless", BAD),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.6, x_text=-2.6)
        with self.voiceover(
            "The trouble was in the details. <bookmark mark='a'/>Demand conclusive verification, and every universal "
            "law dies: no finite set of observations proves that all electrons are charged. "
            "<bookmark mark='b'/>Demand conclusive falsifiability instead, and every existential claim dies, along "
            "with mixed claims like everyone has a mother. <bookmark mark='c'/>So Ayer, in 1946, settled for "
            "relevance: a statement is meaningful if observations bear on it, and he made bearing exact using "
            "logical entailment. <bookmark mark='d'/>And critics asked whether the principle itself is verifiable. "
            "If not, by its own standard it is meaningless; if it is a definition, why accept it?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def church(self):
        d = load("church")
        hc = history_card(1949, r"Alonzo Church", r"review of Ayer, \textit{Journal of Symbolic Logic}", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        ayer = stack([(r"Ayer: \ $S$ is \textit{directly verifiable} if, with some observation sentences, it entails "
                       r"an observation they do not entail alone;", WHITE),
                      (r"\textit{indirectly verifiable} if, with directly verifiable premises, it entails a directly "
                       r"verifiable sentence they do not entail alone", WHITE)], font_size=19, aligned_edge=LEFT,
                     width=12.6).next_to(hc, DOWN, buff=0.3).set_x(0)
        D = MathTex(r"D \;=\; (\lnot O_1 \wedge O_2) \;\vee\; (O_3 \wedge \lnot S)", font_size=34,
                    color=GOAL).next_to(ayer, DOWN, buff=0.35)
        note = label(r"$O_1, O_2, O_3$: \ independent observation sentences; \ \ $S$: \ \textit{any} sentence at all",
                     font_size=19, color=GREY_A).next_to(D, DOWN, buff=0.2)
        texts = [r"$D, O_1 \models O_3$", r"$O_1 \not\models O_3$", r"$S, D \models O_2$", r"$D \not\models O_2$"]
        glosses = [r"so $D$ is directly verifiable", r"", r"so $S$ is indirectly verifiable", r""]
        steps = VGroup()
        for t, gl, st in zip(texts, glosses, d["steps"]):
            steps.add(VGroup(label(t, font_size=22, color=THEORY), label(tick(st["ok"]), font_size=22, color=OK),
                             label(gl, font_size=19, color=GREY_A)).arrange(RIGHT, buff=0.35))
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(note, DOWN, buff=0.3)
        foot = label(r"every sentence passes, \ Bradley's Absolute included \ (the Reasoner checks each entailment by "
                     r"truth table)", font_size=20, color=BAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Alonzo Church needed one paragraph to destroy Ayer's 1946 criterion. <bookmark mark='a'/>Ayer defined a "
            "sentence as directly verifiable if, together with some observation sentences, it entails an "
            "observation they do not entail alone; and indirectly verifiable if, with directly verifiable premises, "
            "it entails a directly verifiable sentence they do not entail alone. <bookmark mark='b'/>Church took "
            "three independent observation sentences and any sentence S whatever, and formed this disjunction, D. "
            "<bookmark mark='c'/>With the first observation, D entails the third, which the first does not entail "
            "alone; so D is directly verifiable. <bookmark mark='d'/>And S together with D entails the second "
            "observation, which D does not entail alone. So S is indirectly verifiable. <bookmark mark='e'/>S was "
            "arbitrary. Every sentence passes, Bradley's Absolute included. The Reasoner checks all four entailments by "
            "truth table."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(ayer))
            vo.wait_until("b")
            self.play(Write(D), FadeIn(note))
            vo.wait_until("c")
            self.play(FadeIn(steps[0]), FadeIn(steps[1]))
            vo.wait_until("d")
            self.play(FadeIn(steps[2]), FadeIn(steps[3]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def boat(self):
        hc = history_card(1932, r"Otto Neurath", r"`Protocol Sentences'", width=5.0, color=HIST).to_corner(UL,
                                                                                                 buff=0.35)
        hull = Polygon([-5.6, -0.6, 0], [-1.4, -0.6, 0], [-2.0, -1.6, 0], [-5.0, -1.6, 0], color=REAL,
                       fill_opacity=0.25, stroke_width=3)
        mast = Line([-3.5, -0.6, 0], [-3.5, 1.4, 0], color=REAL, stroke_width=3)
        sail = Polygon([-3.45, 1.3, 0], [-3.45, -0.4, 0], [-2.2, -0.4, 0], color=GREY_B, fill_opacity=0.2)
        plank = Rectangle(width=0.9, height=0.18, color=GOAL, fill_opacity=0.8).move_to([-4.6, -1.1, 0])
        sea = VGroup(*[Line([-6.6 + 0.9 * i, -1.7, 0], [-6.15 + 0.9 * i, -1.55, 0], color=ANTI) for i in range(8)])
        q = label(r"`We are like sailors who must rebuild their ship on the open sea, \ never able to dismantle it "
                  r"in dry-dock'", font_size=19, color=GOAL).to_edge(DOWN, buff=0.4)
        rows = stack([(r"protocol sentences: \ `Otto's protocol at 3:17: \ Otto saw a table'", THEORY),
                      (r"Schlick: \ observation reports are certain foundations", REAL),
                      (r"Neurath: \ every sentence, \ protocols included, \ can be revised", ANTI),
                      (r"the root of coherentism in science \ (Part 11), \ and of Quine's web", OK)],
                     font_size=19, aligned_edge=LEFT, width=6.2).move_to([3.4, 0.3, 0])
        with self.voiceover(
            "Inside the Circle, a quieter argument mattered more. <bookmark mark='a'/>What are the observation "
            "sentences that verify everything else? Otto Neurath wrote them in a deliberately clumsy form: Otto's "
            "protocol at three seventeen: Otto saw a table. <bookmark mark='b'/>Moritz Schlick held that such "
            "reports are certain, the foundation on which knowledge rests. <bookmark mark='c'/>Neurath denied it. "
            "Every sentence, protocols included, can be revised when it conflicts with the rest. "
            "<bookmark mark='d'/>His image became famous: we are like sailors who must rebuild their ship on the "
            "open sea, plank by plank, never able to take it into dry dock and start from the bottom. It is the root "
            "of coherentism, from Part 11, and of Quine's web."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(sea), FadeIn(hull), Create(mast), FadeIn(sail))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(plank))
            self.play(plank.animate.shift(UP * 0.5 + RIGHT * 0.3), run_time=0.8)
            vo.wait_until("d")
            self.play(plank.animate.shift(DOWN * 0.5 + LEFT * 0.3), FadeIn(q), FadeIn(rows[3]))
        self.clear_scene()

    def legacy(self):
        head = label(r"What survived", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Carnap \ (1936--37)", r"`Testability and Meaning': \ from verification to degrees of confirmation "
                                     r"(Part 15)", THEORY),
            (r"Quine \ (1951)", r"`Two Dogmas': \ sentences meet experience as a corporate body, \ not one by one "
                                r"(Chapter 6)", REAL),
            (r"Hempel \ (1950)", r"every proposed criterion either admits metaphysics or excludes science", BAD),
            (r"the residue", r"theories must answer to observation \textit{somewhere}; \ the question became how", GOAL),
        ]
        g = rows_table(rows, top=1.5, gap=0.55, width=8.6, x_text=-2.6)
        with self.voiceover(
            "Verificationism did not survive as a theory of meaning, but its question did. "
            "<bookmark mark='a'/>Carnap retreated from verification to degrees of confirmation, the programme of "
            "Part 15. <bookmark mark='b'/>Quine argued that sentences do not meet experience one by one, but as a "
            "corporate body, a theme of chapter six. <bookmark mark='c'/>Carl Hempel surveyed the attempts in 1950 "
            "and concluded that every criterion either admits metaphysics or excludes science. "
            "<bookmark mark='d'/>What remained was a demand, not a criterion: theories must answer to observation "
            "somewhere. The rest of this part is about how."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
