from __future__ import annotations

from videos.philosophy.philosophy20.common import *  # noqa: F403


class Universals(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Universals and nominalism", r"What do red things have in common?", lit=(1953, 1978),
                            part=PART)
        with self.voiceover("Chapter three. Universals and nominalism."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.views()
        self.medieval()
        self.armstrong()
        self.bradley()

    def views(self):
        head = label(r"One over many: \ three red things", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        cols = []
        titles = [(r"realism", UNIV), (r"trope theory", ABS), (r"nominalism", NOM)]
        for k, (t, col) in enumerate(titles):
            cx = -4.4 + 4.4 * k
            objs = VGroup(*[Circle(radius=0.32, color=BAD, fill_opacity=0.65).move_to([cx - 1.1 + 1.1 * i, -1.6, 0])
                            for i in range(3)])
            tl = label(t, font_size=22, color=col).move_to([cx, 1.9, 0])
            extra = VGroup()
            if k == 0:
                u = VGroup(RoundedRectangle(width=1.6, height=0.6, corner_radius=0.12, color=UNIV),
                           label(r"Redness", font_size=18, color=UNIV)).move_to([cx, 0.7, 0])
                u[1].move_to(u[0])
                extra.add(u, *[Line(u.get_bottom(), o.get_top(), color=UNIV, stroke_width=2) for o in objs])
                cap = label(r"one universal, \ wholly in each", font_size=16, color=GREY_A)
            elif k == 1:
                tr = VGroup(*[Dot(o.get_center() + UP * 0.85, radius=0.1, color=ABS) for o in objs])
                extra.add(tr, *[Line(tr[i].get_center(), objs[i].get_top(), color=ABS, stroke_width=2)
                                for i in range(3)],
                          *[DashedLine(tr[i].get_center(), tr[i + 1].get_center(), color=GREY_B, stroke_width=1.5)
                            for i in range(2)])
                cap = label(r"three red tropes, \ resembling", font_size=16, color=GREY_A)
            else:
                br = Brace(objs, UP, color=NOM)
                extra.add(br)
                cap = label(r"just three red things", font_size=16, color=GREY_A)
            cap.next_to(objs, DOWN, buff=0.3)
            cols.append(VGroup(tl, objs, extra, cap))
        rows = stack([(r"Plato: \ the Form is apart from its instances; \ \ Aristotle: \ the universal is \textit{in} "
                       r"them", UNIV),
                      (r"D. C. Williams \ (1953): \ tropes, \ `abstract particulars', \ are the alphabet of being",
                       ABS),
                      (r"nominalism: \ only particulars; \ `red' is true of many things, \ and that is all", NOM)],
                     font_size=19, width=12.4).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Three red things: a tomato, a postbox, a ruby. They differ in almost every way, yet they agree in "
            "colour. What is that agreement? <bookmark mark='a'/>The realist says there is one thing, redness, a "
            "universal, wholly present in each, so that one entity is in three places at once. For Plato the Form "
            "exists apart from its instances; for Aristotle the universal exists only in them. "
            "<bookmark mark='b'/>The trope theorist says each red thing has its own particular redness, this red "
            "and that red, and the three tropes exactly resemble one another. Donald Williams called tropes the "
            "alphabet of being. <bookmark mark='c'/>The nominalist says there are only the three red things. The "
            "word red is true of each, and there is nothing further to explain."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(VGroup(c[0], c[1])) for c in cols])
            for mk, k in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(FadeIn(cols[k][2]), FadeIn(cols[k][3]), FadeIn(rows[k]))
        self.clear_scene()

    def medieval(self):
        head = label(r"The medieval problem", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Porphyry \ (c. 270)", r"three questions he declined to answer: \ do genera and species exist, \ or only "
                                     r"in thought? \ are they bodies? \ separate from things?", HIST),
            (r"Boethius", r"universals exist in things, \ and are understood apart from them", UNIV),
            (r"Abelard", r"a universal is a word with a common \textit{status}: \ being a man, \ which is no thing",
             NOM),
            (r"Ockham \ (c. 1323)", r"universals are concepts, \ signs in the mind; \ `plurality is not to be posited "
                                    r"without necessity'", GOAL),
            (r"the razor", r"his rule of economy, \ named for him centuries later, \ Quine's starting point", OK),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.6, x_text=-2.4, label_size=21)
        with self.voiceover(
            "The problem shaped a thousand years of philosophy. <bookmark mark='a'/>Around 270, Porphyry raised three "
            "questions about genera and species, and declined to answer them: do they exist, or only in thought; are "
            "they bodies; are they separate from things? <bookmark mark='b'/>Boethius answered that universals exist "
            "in things but are understood apart from them. <bookmark mark='c'/>Peter Abelard held that a universal is "
            "a word, applied to many things because they share a status, such as being a man, which is not itself a "
            "thing. <bookmark mark='d'/>William of Ockham made universals concepts in the mind, natural signs of "
            "many things, and insisted that plurality must not be posited without necessity. "
            "<bookmark mark='e'/>That rule of economy became known as Ockham's razor, and it is where Quine began."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def armstrong(self):
        hc = history_card(1978, r"D. M. Armstrong", r"\textit{Universals and Scientific Realism}", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = stack([(r"sparse universals: \ not one for every predicate, \ but for every genuine similarity", UNIV),
                      (r"which universals there are is for science to discover: \ mass, \ charge, \ spin", PARTC),
                      (r"no uninstantiated universals: \ `immanent realism', \ after Aristotle", GREY_A),
                      (r"states of affairs: \ \textit{a}'s being \textit{F}, \ the world's building blocks \ (1997)",
                       WHOLE),
                      (r"laws as relations of necessitation between universals \ (Part 18; \ Part 24)", GOAL),
                      (r"Lewis \ (1983): \ `natural properties' do the same work, \ with sets of possibilia", NOM)],
                     font_size=20, aligned_edge=LEFT, width=9.4).move_to([0.6, -0.5, 0])
        with self.voiceover(
            "In the twentieth century, David Armstrong revived realism with a scientific temper. "
            "<bookmark mark='a'/>There is not a universal for every predicate, he argued; there are sparse universals, "
            "one for each genuine similarity among things. <bookmark mark='b'/>Which universals exist is for science "
            "to discover: mass, charge, spin, not being a grue emerald. <bookmark mark='c'/>And there are no "
            "uninstantiated universals: realism in things, after Aristotle. <bookmark mark='d'/>The world is a world "
            "of states of affairs, a particular's having a universal. <bookmark mark='e'/>Laws of nature are "
            "relations of necessitation between universals, a view we met in Part 18 and will test in Part 24. "
            "<bookmark mark='f'/>David Lewis, no realist about universals, agreed that some properties are natural "
            "and others gerrymandered, and found the distinction indispensable."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def bradley(self):
        head = label(r"Bradley's regress \ (1893)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        nodes = [(r"$a$", NOM), (r"$F$", UNIV), (r"$I_1$", ABS), (r"$I_2$", ABS), (r"$I_3$", ABS)]
        dots = VGroup()
        for k, (t, c) in enumerate(nodes):
            p = np.array([-5.6 + 1.5 * k, 0.9, 0])
            dots.add(VGroup(Circle(radius=0.36, color=c, fill_opacity=0.25), label(t, font_size=22, color=c)).move_to(p))
        links = VGroup(*[ArcBetweenPoints(dots[0].get_top(), dots[k].get_top(), angle=-0.6 - 0.15 * k, color=GREY_B,
                                          stroke_width=2) for k in range(2, 5)])
        dl = label(r"$\cdots$", font_size=30, color=GREY_A).next_to(dots, RIGHT, buff=0.3)
        rows = stack([(r"for $a$ to be $F$, \ $a$ and $F$ must be related: \ by instantiation, \ $I_1$", WHITE),
                      (r"but then $a$, \ $F$ and $I_1$ must be related, \ by $I_2$; \ and so on, \ forever", BAD),
                      (r"vicious? \ if each link needs another to hold it together, \ nothing ever is $F$", GOAL),
                      (r"Armstrong: \ states of affairs are unities, \ not lists of constituents", UNIV),
                      (r"Strawson: \ a `non-relational tie'; \ the nominalist: \ no tie is needed at all", NOM)],
                     font_size=20, aligned_edge=LEFT, width=11.6).move_to([0, -1.6, 0])
        with self.voiceover(
            "Realists face a regress, first pressed by F. H. Bradley. <bookmark mark='a'/>For a to be F, a and the "
            "universal F must somehow be related: call the relation instantiation. <bookmark mark='b'/>But "
            "instantiation is itself a universal, so a, F and the instantiation relation must be related, by a second "
            "instantiation, and so on without end. <bookmark mark='c'/>Is the regress vicious? If each link needs "
            "another link to hold it together, then nothing is ever F. <bookmark mark='d'/>Armstrong answered that a "
            "state of affairs is a unity, not a list of constituents waiting to be glued. <bookmark mark='e'/>Peter "
            "Strawson spoke of a non-relational tie. The nominalist says no tie is needed, because there was no "
            "universal to tie to."
        ) as vo:
            self.play(FadeIn(head), FadeIn(dots[:2]))
            vo.wait_until("a")
            self.play(FadeIn(dots[2]), Create(links[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(dots[3:]), Create(links[1:]), FadeIn(dl), FadeIn(rows[1]))
            for mk, r in zip("cde", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
