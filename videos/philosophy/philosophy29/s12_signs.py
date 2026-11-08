from __future__ import annotations

from videos.philosophy.philosophy29.common import *  # noqa: F403


class Signs(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Structure and difference", r"Is meaning a matter of differences?",
                            lit=(1916, 1967), part=PART)
        with self.voiceover("Chapter eleven. Structure and difference."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.saussure()
        self.rotation()
        self.derrida()
        self.dictionary()
        self.critics()

    def saussure(self):
        hc = history_card(1916, r"Ferdinand de Saussure", r"\textit{Course in General Linguistics}", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        oval = Ellipse(width=3.2, height=2.4, color=SIGN).move_to([-3.6, -0.2, 0])
        bar = Line(oval.get_left(), oval.get_right(), color=SIGN)
        sd = label(r"concept: \ tree", font_size=20, color=OBJ).move_to(oval.get_center() + UP * 0.5)
        sr = label(r"sound-image: \ /arbor/", font_size=20, color=ACT).move_to(oval.get_center() + DOWN * 0.5)
        tags = VGroup(label(r"signified", font_size=16, color=OBJ).next_to(oval, LEFT, buff=0.1).shift(UP * 0.5),
                      label(r"signifier", font_size=16, color=ACT).next_to(oval, LEFT, buff=0.1).shift(DOWN * 0.5))
        rows = stack([(r"the bond is arbitrary: \ \textit{arbor}, \ \textit{Baum}, \ \textit{tree}", WHITE),
                      (r"\textit{langue}, \ the system, \ against \textit{parole}, \ the speaking", ACT),
                      (r"`in language there are only differences, \ without positive terms'", SIGN),
                      (r"like a chess piece: \ a knight is whatever plays the knight's role", GOAL)], font_size=20,
                     aligned_edge=LEFT, width=6.4, buff=0.3).move_to([3.2, -0.3, 0])
        with self.voiceover(
            "Structuralism began with lectures on linguistics that Ferdinand de Saussure gave in Geneva, published "
            "by his students in 1916. <bookmark mark='a'/>A sign unites a concept, the signified, with a sound-image, "
            "the signifier. <bookmark mark='b'/>The bond between them is arbitrary: arbor, Baum and tree all do the "
            "job. <bookmark mark='c'/>Linguistics should study langue, the system a community shares, not parole, the "
            "individual acts of speaking. <bookmark mark='d'/>And in that system, Saussure said, there are only "
            "differences, without positive terms. A sign's value is fixed by its contrasts with the others. "
            "<bookmark mark='e'/>His analogy was chess: a knight can be made of wood or ivory, or replaced by a "
            "button; it is a knight because of its role among the other pieces."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Create(oval), Create(bar), FadeIn(sd), FadeIn(sr), FadeIn(tags))
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def rotation(self):
        d = load("procrustes")
        head = label(r"Saussure in geometry", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["k"] == 6 and d["words"] == 58 and d["same_nn"] and abs(d["coord_corr"]) < 0.5
        assert d["cos_change"] < 1e-14 and d["resid"] < 1e-14 and d["map_error"] < 1e-14 and len(d["anchors"]) == 8
        assert any({"big", "england", "france", "germany", "italy"} <= set(g) for g in d["shared"])
        kb, ka = d["sample"]["king"]["before"], d["sample"]["king"]["after"]
        assert len(kb) == len(ka) == 3 and np.isfinite([kb, ka]).all()
        eq = MathTex(r"F = E\,Q, \qquad Q^{\top} Q = I", font_size=32, color=TIME).move_to([-3.4, 2.0, 0])
        before = MathTex(r"\text{king}: \ (" + ", ".join(f"{x:.3f}" for x in kb) + r", \dots)", font_size=24,
                         color=ACT)
        after = MathTex(r"\text{king}: \ (" + ", ".join(f"{x:.3f}" for x in ka) + r", \dots)", font_size=24,
                        color=OBJ)
        col = VGroup(VGroup(label(r"Part 28's vectors", font_size=18, color=GREY_A), before).arrange(DOWN, buff=0.1),
                     VGroup(label(r"after a random rotation", font_size=18, color=GREY_A), after).arrange(DOWN,
                                                                                                    buff=0.1)
                     ).arrange(DOWN, buff=0.3).move_to([-3.4, 0.4, 0])
        rows = stack([(rf"$\mathrm{{corr}}(E,F) = {d['coord_corr']:.2f}$", OBJ),
                      (r"every cosine stays: \ largest change $10^{-15}$; \ every nearest neighbour the same", OK),
                      (r"Procrustes: \ $W = UV^{\top}$ from 8 anchor words recovers $Q$ \ (error $10^{-15}$)", TIME),
                      (rf"{len(d['shared'])} groups share one point each: \ England, \ France, \ Germany, \ Italy, \ `big' keep the same "
                       r"company", BAD)], font_size=19, aligned_edge=LEFT, width=6.2, buff=0.28).move_to([3.4, 0.3, 0])
        foot = label(r"a difference that makes no difference to relations makes no difference to value", font_size=21,
                     color=GOAL).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Part 28 built word vectors from a small corpus. They make Saussure's claim exact. "
            "<bookmark mark='a'/>Rotate the whole space by a random rotation Q. <bookmark mark='b'/>The words' "
            "coordinates change, king's included. The coordinate correlation is shown on screen. "
            "<bookmark mark='c'/>But every cosine between words "
            "stays the same, to fifteen decimal places, and so does every word's nearest neighbour. If meaning is "
            "the network of similarities, the rotation changed nothing. <bookmark mark='d'/>And the rotation can be "
            "recovered from the structure. Given just eight anchor words in both spaces, orthogonal Procrustes finds "
            "the rotation, the matrix U V transpose from a singular value decomposition, to within ten to the minus "
            "fifteen, and carries every word to its image. Aligning embeddings learned in two languages works on "
            "this principle. <bookmark mark='e'/>There is a twist. In this corpus England, France, Germany, Italy "
            "and the word big keep exactly the same company, and they sit at exactly the same point; other groups "
            "do too. No structure can tell them apart. <bookmark mark='f'/>That is Saussure again: a difference that "
            "makes no difference to the relations makes no difference to value."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(FadeIn(col[0]))
            self.play(TransformFromCopy(col[0], col[1]), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def derrida(self):
        hc = history_card(1967, r"Jacques Derrida", r"\textit{Of Grammatology}", width=5.0, color=HIST).to_corner(
            UL, buff=0.3)
        rows = [
            (r"\textit{diff\'erance}", r"a coinage \ (1968): \ meaning both \textit{differs} \ (Saussure) \ and is "
                                       r"\textit{deferred}, \ never fully present in any sign", SIGN),
            (r"oppositions", r"speech over writing, \ presence over absence, \ literal over metaphorical: \ each "
                             r"hierarchy can be shown to depend on what it subordinates", ACT),
            (r"deconstruction", r"reading a text against its own oppositions, \ not destroying it", WORLD),
            (r"`no outside-text'", r"\textit{il n'y a pas de hors-texte}: \ later glossed by Derrida as `there is "
                                   r"nothing outside context' \ (1988)", BODY),
        ]
        g = rows_table(rows, top=0.9, gap=0.45)
        with self.voiceover(
            "Jacques Derrida took Saussure's differences further. <bookmark mark='a'/>He coined a word, différance, "
            "spelled with an a and pronounced like the ordinary French word for difference. It means both to differ, "
            "Saussure's point, and to defer: the meaning of a sign is never fully present in it, but always put off "
            "along a chain of other signs. <bookmark mark='b'/>Western philosophy, he argued, is organised by "
            "oppositions in which one term is privileged: speech over writing, presence over absence, the literal "
            "over the metaphorical. Each hierarchy can be shown to depend on the term it subordinates. "
            "<bookmark mark='c'/>Deconstruction is the practice of reading a text against its own oppositions, which "
            "is not the same as destroying it. <bookmark mark='d'/>His most quoted sentence, there is no outside-text, "
            "is often read as saying that nothing exists but language. Derrida later glossed it as: there is nothing "
            "outside context."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def dictionary(self):
        d = load("dictionary")
        head = label(r"A closed dictionary \ (an analogy)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["words"] == 18 and d["edges"] == 28 and d["grounding_size"] == 3 and d["n_minimum_sets"] == 27
        assert d["grounding"] == ["being", "good", "meaning"]
        dic = d["dictionary"]
        pos = {"thing": (-1.0, 0.9), "being": (0.3, 1.6), "existing": (0.6, 0.2),
               "good": (3.6, 1.6), "valuable": (5.0, 1.0), "worthy": (3.8, 0.2),
               "sign": (-4.6, -1.6), "meaning": (-3.2, -2.3), "word": (-3.0, -0.9),
               "object": (-2.6, 1.6), "seen": (-4.4, 1.3), "eye": (-5.4, 0.2), "body": (-3.6, 0.2),
               "living": (-1.8, -0.4), "right": (2.2, 0.8), "true": (1.8, -0.8), "real": (0.2, -1.2),
               "fact": (2.0, -2.2)}
        core = {"thing", "being", "existing", "good", "valuable", "worthy", "sign", "meaning", "word"}
        nodes = {}
        for w, (x, y) in pos.items():
            t = label(rf"`{w}'", font_size=17, color=SIGN if w in core else GREY_A)  # words mentioned, not used
            bx = RoundedRectangle(width=t.width + 0.25, height=0.38, corner_radius=0.1,
                                  color=SIGN if w in core else GREY_C, stroke_width=1.5)
            nodes[w] = VGroup(bx, t).move_to([x, y - 0.2, 0])
        arrows = VGroup()
        for w, defs in dic.items():
            for v in defs:
                arrows.add(Arrow(nodes[w].get_center(), nodes[v].get_center(), buff=0.25, color=GREY_D,
                                 stroke_width=1.5, max_tip_length_to_length_ratio=0.08))
        ground = VGroup(*[SurroundingRectangle(nodes[w], color=OK, buff=0.06, stroke_width=3) for w in d["grounding"]])
        side = stack([(r"18 words, \ 28 definition links: \ every chain of definitions ends in a circle", WHITE),
                      (r"to break every circle, \ 3 words must get their meaning from outside: \ 27 ways to choose "
                       r"them", OK),
                      (r"Harnad's grounding problem \ (Part 28), \ and a picture of deferral", GOAL)], font_size=18,
                     aligned_edge=LEFT, width=12.0, buff=0.16).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "There is an old observation behind différance, which the Reasoner can make precise as an analogy. "
            "<bookmark mark='a'/>Here is a small dictionary of eighteen words, each defined by one or two others. "
            "Thing is defined by being, being by existing, existing by thing again; good by valuable, valuable by "
            "worthy, worthy by good. <bookmark mark='b'/>Follow any definition, then a word in that definition, and "
            "so on, and you never leave the dictionary: every chain ends in a circle. The meaning of a word is always "
            "deferred to other words. <bookmark mark='c'/>To break every circle, some words must get their meaning "
            "from outside the dictionary altogether, by pointing, perceiving or doing. The smallest number here is "
            "three, one from each circle, and there are twenty-seven ways to choose them. "
            "<bookmark mark='d'/>This is Stevan Harnad's grounding problem from Part 28, in miniature. Derrida "
            "would not have accepted the escape route; that is the disagreement in a nutshell."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(n) for n in nodes.values()], lag_ratio=0.05),
                      LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.03), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(Create(ground), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def critics(self):
        head = label(r"The critics", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Searle \ (1977)", r"`Reiterating the Differences': \ Derrida misread Austin's speech acts \ (Part 28)",
             BAD),
            (r"Cambridge \ (1992)", r"an honorary degree contested in a letter from senior philosophers abroad, \ "
                                    r"and passed by a vote", HIST),
            (r"the charge, \ the defence", r"obscurity used as a shield; \ or serious, \ exact readings, \ with a "
                                         r"lasting influence on literary theory, \ law and architecture", OK),
        ]
        g = rows_table(rows, top=1.4, gap=0.55)
        with self.voiceover(
            "Derrida's work divided philosophers like almost no other. <bookmark mark='a'/>John Searle, in 1977, "
            "replied to Derrida's reading of Austin, from Part 28, that he had simply misunderstood it, and the "
            "exchange grew bitter. <bookmark mark='b'/>In 1992, when Cambridge proposed Derrida for an honorary "
            "degree, senior philosophers from several countries wrote to The Times in protest; the degree was approved by a "
            "vote of the university. <bookmark mark='c'/>The charge was that obscurity was being used as a shield; "
            "the defence, that his readings are serious and exact, and his influence on "
            "literary theory, law and architecture is beyond dispute."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
