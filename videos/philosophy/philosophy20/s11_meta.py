from __future__ import annotations

from videos.philosophy.philosophy20.common import *  # noqa: F403


class Meta(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Metaontology", r"Are disputes about what exists substantive?", lit=(1950, 2011),
                            part=PART)
        with self.voiceover("Chapter ten. Metaontology."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.carnap()
        self.putnam()
        self.variance()

    def carnap(self):
        hc = history_card(1950, r"Rudolf Carnap", r"`Empiricism, Semantics, and Ontology'", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        frame = RoundedRectangle(width=5.2, height=2.8, corner_radius=0.2, color=UNIV).move_to([-3.4, -0.8, 0])
        fl = label(r"the number framework", font_size=18, color=UNIV).next_to(frame, UP, buff=0.1)
        inside = label(r"`is there a prime above 100?' \ \ yes", font_size=18, color=OK).move_to(
            frame.get_center() + UP * 0.5)
        inside2 = label(r"`are there numbers?' \ \ trivially yes", font_size=18, color=OK).move_to(
            frame.get_center() + DOWN * 0.4)
        outside = label(r"`but are there \textit{really} numbers?'", font_size=19, color=BAD).move_to([-3.4, -2.8, 0])
        rows = stack([(r"internal questions: \ asked within a linguistic framework, \ answered by its rules and "
                       r"evidence", OK),
                      (r"external questions: \ whether to adopt the framework at all", BAD),
                      (r"not true or false: \ a practical choice of language, \ judged by its usefulness", GOAL),
                      (r"Quine \ (1951): \ no sharp line between framework and theory: \ ontology is continuous with "
                       r"science", GREY_A)], font_size=19, aligned_edge=LEFT, width=6.0).move_to([3.5, -0.6, 0])
        with self.voiceover(
            "Rudolf Carnap thought most of these debates were confused. <bookmark mark='a'/>Questions about "
            "existence asked within a linguistic framework, such as is there a prime above a hundred, are answered by "
            "the rules and evidence of the framework. Within the number framework, are there numbers is trivially "
            "yes. <bookmark mark='b'/>The metaphysician wants to step outside and ask whether there are really "
            "numbers. That external question, Carnap said, is only whether to adopt the framework. "
            "<bookmark mark='c'/>It is not true or false, but a practical choice of language, judged by how useful it "
            "is. <bookmark mark='d'/>Quine replied that there is no sharp line between choosing a framework and "
            "choosing a theory: ontology is part of science, and as serious as any of it."
        ) as vo:
            self.play(FadeIn(hc), Create(frame), FadeIn(fl))
            vo.wait_until("a")
            self.play(FadeIn(inside), FadeIn(inside2), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(outside), FadeIn(rows[1]))
            for mk, r in zip("cd", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def putnam(self):
        d = load("putnam")
        head = label(r"Putnam's cookie cutter \ (1987)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        pos = [np.array([-5.2 + 1.2 * i, 0.9, 0]) for i in range(3)]
        dots = VGroup(*[Dot(p, radius=0.2, color=PARTC) for p in pos])
        names = VGroup(*[label(r"$x_" + f"{i + 1}" + r"$", font_size=20, color=WHITE).next_to(dots[i], DOWN, buff=0.15)
                         for i in range(3)])
        sums = VGroup()
        for k, s in enumerate(d["sums"]):
            g = VGroup(*[Dot(radius=0.09, color=WHOLE if len(s) > 1 else PARTC) for _ in s]).arrange(RIGHT, buff=0.08)
            box = SurroundingRectangle(g, buff=0.08, color=WHOLE if len(s) > 1 else PARTC, corner_radius=0.08,
                                       stroke_width=1.5)
            sums.add(VGroup(g, box).move_to([-6.0 + 0.95 * k, -0.9, 0]))
        c1 = label(r"Carnap: \ " + f"{d['carnap']}" + r" objects", font_size=24, color=PARTC).move_to([-4.0, 2.0, 0])
        c2 = label(r"the Polish logician: \ " + f"{d['polish']}" + r" objects", font_size=24, color=WHOLE).move_to(
            [-3.2, -2.0, 0])
        rows = stack([(r"same world, \ different counts", WHITE),
                       (r"Putnam: \ `object' has no meaning fixed apart from a conceptual scheme", GOAL),
                       (r"internal realism: \ the question `how many objects \textit{really}?' has no answer", BAD)],
                      font_size=20, aligned_edge=LEFT, width=5.8).move_to([3.6, 0.0, 0])
        with self.voiceover(
            "Hilary Putnam gave the debate a famous example. <bookmark mark='a'/>Imagine a world with three "
            "individuals. How many objects are there? Carnap counts three. <bookmark mark='b'/>A Polish logician, a "
            "follower of Leśniewski who accepts every mereological sum, counts seven: the three, the three pairs, and "
            "the whole. <bookmark mark='c'/>The same world, two counts. <bookmark mark='d'/>Putnam concluded that the "
            "word object has no meaning fixed independently of a conceptual scheme. <bookmark mark='e'/>Ask how many "
            "objects there really are, and there is no answer to give."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(dots), FadeIn(names), FadeIn(c1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s) for s in sums], lag_ratio=0.15), FadeIn(c2))
            for mk, r in zip("cde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def variance(self):
        head = label(r"Verbal disputes, \ or joints in nature?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"quantifier variance", r"Hirsch \ (2002, \ 2011): \ `there is' can mean different things; \ the nihilist "
                                     r"and the universalist each speak truly, \ in their own language", UNIV),
            (r"so", r"many ontological disputes are merely verbal", BAD),
            (r"easy ontology", r"Thomasson \ (2015): \ existence questions are answered by trivial inferences from "
                               r"conceptual truths", NOM),
            (r"structure", r"Sider \ (2011): \ some meanings carve nature at its joints; \ ontology asks what exists in "
                           r"the most joint-carving sense of `exists'", GOAL),
            (r"the test", r"is the fundamental quantifier one, \ or many? \ the dispute is now about structure", GREY_A),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "Today's metaontology continues the argument. <bookmark mark='a'/>Eli Hirsch defends quantifier "
            "variance: the phrase there is can be given different meanings, and the nihilist and the universalist "
            "each speak truly in their own language. <bookmark mark='b'/>Their dispute is merely verbal, like an "
            "argument over whether a glass is half full. <bookmark mark='c'/>Amie Thomasson's easy ontology says "
            "existence questions are answered by trivial inferences from conceptual truths. "
            "<bookmark mark='d'/>Ted Sider replies with structure. Some meanings carve nature at its joints better "
            "than others, and ontology asks what exists in the most joint-carving sense of exists. "
            "<bookmark mark='e'/>Whether there is one such meaning, or many equally good ones, is now itself the "
            "question."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
