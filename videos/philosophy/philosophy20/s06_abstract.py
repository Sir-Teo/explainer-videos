from __future__ import annotations

from videos.philosophy.philosophy20.common import *  # noqa: F403


class Abstract(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Abstract objects", r"Where is the number two?", lit=(1884, 1986), part=PART)
        with self.voiceover("Chapter five. Abstract objects."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.ways()
        self.directions()
        self.views()
        self.classes()

    def ways(self):
        head = label(r"What makes an object abstract? \ \ (Lewis, \ 1986)", font_size=30, color=CONN).to_edge(
            UP, buff=0.35)
        rows = [
            (r"the way of example", r"abstract things are like numbers, \ sets, \ propositions: \ a list, \ not a "
                                    r"criterion", GREY_A),
            (r"the way of negation", r"not in space or time, \ and causally inert: \ but are sets of concrete things "
                                     r"located where their members are?", NOM),
            (r"the way of conflation", r"abstract means universal, \ or set: \ but then which?", UNIV),
            (r"the way of abstraction", r"abstract objects are what we get by abstracting from concrete things: \ "
                                        r"directions from lines, \ shapes from figures", ABS),
            (r"Lewis's verdict", r"no clear line: \ `abstract' is not a well-defined term of art", BAD),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.4, x_text=-2.2, label_size=20)
        with self.voiceover(
            "Numbers, sets and propositions are the usual examples of abstract objects. But what makes an object "
            "abstract? David Lewis surveyed four answers. <bookmark mark='a'/>The way of example just lists cases, "
            "which is not a criterion. <bookmark mark='b'/>The way of negation says abstract things are outside space "
            "and time, and causally inert. But is the set of these three cups located where the cups are? "
            "<bookmark mark='c'/>The way of conflation identifies the abstract with the universal, or with the set, "
            "and these come apart. <bookmark mark='d'/>The way of abstraction says abstract objects are what we reach "
            "by abstracting from concrete ones, as directions from lines. <bookmark mark='e'/>Lewis concluded that "
            "there is no clear line, and that abstract is not a well-defined term."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def directions(self):
        hc = history_card(1884, r"Gottlob Frege", r"\textit{Grundlagen der Arithmetik}, \ \S 64", width=6.0,
                          color=HIST).to_corner(UL, buff=0.3)
        rng = np.random.default_rng(64)
        slopes = [0.4, -1.2, 2.5]
        cols = [PARTC, WHOLE, NOM]
        lines = VGroup()
        groups = {}
        for k in range(7):
            s = slopes[k % 3]
            c = np.array([-5.0 + rng.uniform(0, 3.4), -1.6 + rng.uniform(0, 2.4), 0])
            ang = np.arctan(s)
            v = 0.8 * np.array([np.cos(ang), np.sin(ang), 0])
            ln = Line(c - v, c + v, color=cols[k % 3], stroke_width=4)
            lines.add(ln)
            groups.setdefault(k % 3, []).append(ln)
        n_dir = len(groups)
        f1 = MathTex(r"\mathrm{dir}(a) = \mathrm{dir}(b) \iff a \parallel b", font_size=34, color=ABS).move_to(
            [3.0, 1.6, 0])
        f2 = MathTex(r"\#F = \#G \iff F \approx G", font_size=34, color=UNIV).next_to(f1, DOWN, buff=0.45)
        f2l = label(r"Hume's principle: \ the numbers, \ from one-to-one correspondence", font_size=16,
                    color=GREY_A).next_to(f2, DOWN, buff=0.12)
        f3 = MathTex(r"\{x : Fx\} = \{x : Gx\} \iff \forall x\,(Fx \leftrightarrow Gx)", font_size=30,
                     color=BAD).next_to(f2l, DOWN, buff=0.4)
        f3l = label(r"Basic Law V: \ the same form, \ and it is inconsistent \ (Russell, \ Part 9)", font_size=16,
                    color=BAD).next_to(f3, DOWN, buff=0.12)
        count = label(f"{len(lines)}" + r" lines, \ " + f"{n_dir}" + r" directions: \ classes under parallelism",
                      font_size=19, color=WHITE).move_to([-3.3, -2.8, 0])
        with self.voiceover(
            "Frege showed how abstraction can be made precise. <bookmark mark='a'/>Here are seven lines. Parallelism "
            "sorts them into classes. <bookmark mark='b'/>Frege's principle: the direction of a equals the direction "
            "of b exactly when a is parallel to b. The direction is introduced by an equivalence relation among "
            "concrete lines. <bookmark mark='c'/>The Reasoner counts: seven lines, three directions. "
            "<bookmark mark='d'/>Numbers can be introduced the same way, by Hume's principle: the number of Fs equals "
            "the number of Gs exactly when the Fs and Gs correspond one to one. <bookmark mark='e'/>But the same form "
            "applied to extensions gives Basic Law V, which Russell's paradox showed inconsistent. Abstraction "
            "principles are powerful, and dangerous; which ones are acceptable is still debated."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(ln) for ln in lines], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(Write(f1))
            vo.wait_until("c")
            self.play(FadeIn(count), *[Indicate(VGroup(*g), color=g[0].get_color()) for g in groups.values()])
            vo.wait_until("d")
            self.play(Write(f2), FadeIn(f2l))
            vo.wait_until("e")
            self.play(Write(f3), FadeIn(f3l))
        self.clear_scene()

    def views(self):
        head = label(r"Platonism and its rivals", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Platonism", r"abstract objects exist, \ necessarily and independently of us", UNIV),
            (r"Benacerraf \ (1973)", r"then how can we, \ causally embedded creatures, \ know about them? \ (Part 9)",
             BAD),
            (r"neo-Fregeanism", r"Hale and Wright: \ abstraction principles introduce numbers; \ knowing Hume's "
                                r"principle is knowing arithmetic", ABS),
            (r"thin objects", r"Linnebo \ (2018): \ objects whose existence makes little demand on the world", PARTC),
            (r"fictionalism", r"Field \ (1980): \ `2 + 2 = 4' is true in the story of mathematics, \ as `Holmes is a "
                              r"detective' is in Conan Doyle", NOM),
            (r"easy ontology", r"Thomasson: \ from `there are 2 cups' infer `there is a number': \ existence "
                               r"questions are easy", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.42, width=8.6, x_text=-2.4, label_size=21)
        with self.voiceover(
            "The debate over abstract objects is lively. <bookmark mark='a'/>Platonists hold that they exist, "
            "necessarily and independently of us. <bookmark mark='b'/>Paul Benacerraf asked how we could then know "
            "anything about them, since they cannot affect us. <bookmark mark='c'/>Bob Hale and Crispin Wright reply "
            "that abstraction principles like Hume's introduce the numbers, so knowing such a principle is knowing "
            "arithmetic. <bookmark mark='d'/>Øystein Linnebo calls them thin objects, whose existence asks little of "
            "the world. <bookmark mark='e'/>Hartry Field's fictionalism says that two plus two is four is true only "
            "in the story of mathematics. <bookmark mark='f'/>And Amie Thomasson's easy ontology says that from there "
            "are two cups we may infer there is a number, so existence questions are easy, not deep. That last view "
            "returns in chapter ten."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def classes(self):
        hc = history_card(1991, r"David Lewis", r"\textit{Parts of Classes}", width=5.0, color=HIST).to_corner(
            UL, buff=0.35)
        cats = VGroup(*[Dot([-5.6 + 0.7 * i, -0.2, 0], radius=0.14, color=PARTC) for i in range(3)])
        cl = label(r"three cats", font_size=16, color=PARTC).next_to(cats, DOWN, buff=0.2)
        sing = VGroup(*[VGroup(Circle(radius=0.26, color=ABS), Dot(radius=0.08, color=PARTC)).move_to(
            [-5.6 + 0.7 * i, -1.8, 0]) for i in range(3)])
        sl = label(r"their singletons", font_size=16, color=ABS).next_to(sing, DOWN, buff=0.2)
        big = Ellipse(width=2.6, height=0.9, color=WHOLE).move_to([-4.9, -1.8, 0])
        rows = stack([(r"main thesis: \ a class is the mereological sum of the singletons of its members", WHOLE),
                      (r"so set theory is mereology plus one primitive: \ the singleton function \ $x \mapsto \{x\}$",
                       UNIV),
                      (r"subsets are parts: \ $\{a, b\} \subseteq \{a, b, c\}$ because it is part of it", OK),
                      (r"but what is a singleton? \ an atom with nothing in common with its member: \ `a mystery'",
                       BAD),
                      (r"structuralism \ (Part 9) \ offers relief: \ only the pattern of singletons matters", GREY_A)],
                     font_size=19, aligned_edge=LEFT, width=7.6).move_to([2.6, -0.5, 0])
        with self.voiceover(
            "David Lewis connected the two great formal ontologies, set theory and mereology. "
            "<bookmark mark='a'/>His main thesis: a class is the mereological sum of the singletons of its members. "
            "The class of three cats is the fusion of the three singletons, cat one, cat two and cat three. "
            "<bookmark mark='b'/>Then set theory is mereology plus a single new primitive, the function that takes "
            "each thing to its singleton. <bookmark mark='c'/>And subsets are just parts: a set of two cats is part of "
            "the set of three. <bookmark mark='d'/>But what is a singleton? An atom, with no parts in common with its "
            "member, related to it in a way nothing explains. Lewis confessed it a mystery. <bookmark mark='e'/>The "
            "structuralism of Part 9 offers relief: perhaps only the pattern of the singleton relation matters, not "
            "the nature of its relata."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(cats), FadeIn(cl))
            vo.wait_until("a")
            self.play(TransformFromCopy(cats, VGroup(*[s_[1] for s_ in sing])), FadeIn(VGroup(*[s_[0] for s_ in sing])),
                      FadeIn(sl), Create(big), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
