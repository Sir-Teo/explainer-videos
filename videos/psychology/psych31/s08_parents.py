from __future__ import annotations

from videos.psychology.psych31.common import *  # noqa: F403


class Parents(VoiceoverScene):
    def construct(self):
        self.card()
        self.confound()
        self.siblings()
        self.nurture()
        self.birth_order()

    def card(self):
        card = chapter_card(7, r"Parents", r"What do parents do to how a child turns out?",
                            lit={1987: r"Plomin \& Daniels", 1998: r"Harris", 2015: r"Rohrer et al."}, part=PART,
                            scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter seven. Parents."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def confound(self):
        head = heading(r"A correlation with two causes")
        par = VGroup(person(1.4, CARE), label(r"parent", font_size=22, color=CARE)).arrange(DOWN, buff=0.15)
        kid = VGroup(person(1.0, CHILD), label(r"child", font_size=22, color=CHILD)).arrange(DOWN, buff=0.15)
        par.move_to([-3.5, 1.2, 0])
        kid.move_to([3.5, 1.2, 0])
        a1 = CurvedArrow(par.get_right() + UP * 0.4, kid.get_left() + UP * 0.4, color=CARE, angle=-0.5)
        a2 = CurvedArrow(par.get_right() + DOWN * 0.4, kid.get_left() + DOWN * 0.4, color=COHORT, angle=0.5)
        l1 = label(r"the home: \ books, \ talk, \ warmth", font_size=22, color=CARE).next_to(a1, UP, buff=0.1)
        l2 = label(r"half their genes", font_size=22, color=COHORT).next_to(a2, DOWN, buff=0.1)
        rows = rows_of([
            (r"parents who read to their children have children who read well: \ but the parents gave them both "
             r"the books and half their genes", WHITE),
            (r"in an ordinary family the two routes are confounded; \ Part 9's twins and adoptees pull them apart",
             COHORT),
            (r"an adopted child shares a home with its siblings, \ not genes: \ their likeness measures the shared "
             r"environment", CARE),
        ], 12.4, 24, 0.38).move_to([0, -1.8, 0])
        with self.voiceover(
            "Parents who read to their children have children who read well. <bookmark mark='a'/> But those parents "
            "gave their children two things: the books, the talk and the warmth of the home, and half their genes. "
            "<bookmark mark='b'/> In an ordinary family the two routes are confounded. Part 9's twins and adoptees "
            "pull them apart. <bookmark mark='c'/> An adopted child shares a home with the other children in it, "
            "but not genes, so how alike adoptive siblings are measures the shared environment, everything about a "
            "family that makes its children similar."
        ) as vo:
            self.play(FadeIn(head), FadeIn(par), FadeIn(kid))
            vo.wait_until("a")
            self.play(Create(a1), FadeIn(l1), Create(a2), FadeIn(l2), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def siblings(self):
        d = load("parents")
        head = heading(r"How alike are siblings, \ as children and as adults?")
        A = axes([-0.6, 6.6], [0, 0.9], x_length=6.6, y_length=4.0, xticks=None, yticks=[0, 0.3, 0.6, 0.9],
                 yfmt=lambda v: f"{v:g}", ylabel=r"correlation", center=[-2.9, -0.2, 0], font_size=16)
        names = (r"identical twins", r"fraternal twins", r"adoptive siblings")
        xs_c, xs_a = [0, 1, 2], [4, 5, 6]
        cols = [COHORT, AGE, CARE]
        bc = bars(A.ax, xs_c, d["child_sim"], cols, width=0.7)
        ba = bars(A.ax, xs_a, d["adult_sim"], cols, width=0.7)
        th = VGroup(*[Line(A.ax.c2p(x - 0.38, y), A.ax.c2p(x + 0.38, y), color=WHITE, stroke_width=3)
                      for x, y in zip(xs_c + xs_a, list(d["child_theory"]) + list(d["adult_theory"]))])
        gl = VGroup(label(r"in childhood", font_size=20, color=CHILD).next_to(A.ax.c2p(1, 0), DOWN, buff=0.25),
                    label(r"in adulthood", font_size=20, color=OLD).next_to(A.ax.c2p(5, 0), DOWN, buff=0.25))
        key = legend([(c, n) for c, n in zip(cols, names)], font_size=16).move_to(A.ax.c2p(3.0, 0.8))
        rows = rows_of([
            (r"the model \ (Part 9): \ identical twins share $h^2 + c^2$, \ fraternal twins $h^2/2 + c^2$, \ "
             r"adoptive siblings $c^2$ alone", WHITE),
            (rf"in childhood, \ $h^2 = {d['child_h2']:g}$ and $c^2 = {d['child_c2']:g}$; \ in adulthood, \ "
             rf"$h^2 = {d['adult_h2']:g}$ and $c^2 = 0$: \ 300 simulated pairs each, \ white lines the theory",
             MODEL),
            (r"Robert Plomin and Denise Daniels, \ 1987: \ adoptive siblings' IQs correlated about 0.3 in "
             r"childhood studies, \ and $-0.03$ in the first study after adolescence", CARE),
            (r"what a family shares matters for children's IQ, \ and fades as they leave home and choose their own "
             r"environments", YOU),
        ], 5.4, 20, 0.34).move_to([3.7, -0.2, 0])
        tag = psyche_tag(r"\texttt{lifespan.sibling\_correlations}; \ Plomin \& Daniels (1987)")
        with self.voiceover(
            "So how alike are siblings? <bookmark mark='a'/> In the model of Part 9, identical twins share all of "
            "the genetic variance and all of the shared environment, fraternal twins half the genetic variance and "
            "all of the shared environment, and adoptive siblings only the shared environment. "
            "<bookmark mark='b'/> Psyche simulates three hundred pairs of each, once with a sizeable shared "
            "environment in childhood, and once with none in adulthood, and heritability higher. "
            "<bookmark mark='c'/> That is the pattern for IQ. Robert Plomin and Denise Daniels reviewed it in 1987: "
            "adoptive siblings' IQs correlated about 0.3 in studies of children, and minus 0.03 in the first study "
            "after adolescence. <bookmark mark='d'/> What a family shares matters for children's IQ, and it fades as "
            "they leave home and choose their own environments."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(gl), FadeIn(key), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(bc), FadeIn(ba), FadeIn(th), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def nurture(self):
        head = heading(r"The nurture assumption")
        rows = rows_of([
            (r"for personality, \ adoptive siblings grow up hardly more alike than strangers; \ Plomin and Daniels "
             r"asked why children in one family are so different", WHITE),
            (r"Judith Rich Harris, \ 1998, \ \emph{The Nurture Assumption}: \ beyond the genes they pass on, \ "
             r"parents shape personality far less than assumed; \ peers shape it more", CARE),
            (r"the replies: \ \emph{shared} environment is not the same as parenting; \ parents treat each child "
             r"differently, \ and that counts as non-shared", COHORT),
            (r"and randomized evidence: \ in Bucharest, \ part of foster care's effect on IQ ran through the "
             r"quality of caregiving and the security of attachment", GOOD),
            (r"what parenting demonstrably does: \ the extremes matter most, \ deprivation above all; \ within the "
             r"ordinary range, \ effects on lasting traits are hard to find", YOU),
        ], 12.4, 24, 0.38).move_to([0, -0.3, 0])
        tag = published_tag(r"Harris (1998); \ Humphreys et al.\ (2022)")
        with self.voiceover(
            "For personality the shared environment is even smaller. <bookmark mark='a'/> Adoptive siblings grow up "
            "hardly more alike than strangers, and Plomin and Daniels asked why children in one family are so "
            "different. <bookmark mark='b'/> In 1998 Judith Rich Harris pushed the point in The Nurture "
            "Assumption: beyond the genes they pass on, parents shape their children's personalities far less than "
            "everyone assumes, and peers shape them more. <bookmark mark='c'/> The replies: the shared environment "
            "isn't the same thing as parenting. Parents treat each child differently, and that counts as non-shared. "
            "<bookmark mark='d'/> And there's randomized evidence: in Bucharest, part of foster care's effect on IQ "
            "ran through the quality of caregiving and the security of attachment. <bookmark mark='e'/> So what "
            "parenting demonstrably does is clearest at the extremes, deprivation above all. Within the ordinary "
            "range of homes, effects on lasting traits are hard to find."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def birth_order(self):
        head = heading(r"Firstborns, \ middle children, \ the baby of the family")
        rows = rows_of([
            (r"Lillian Belmont and Francis Marolla, \ 1973: \ nearly 400{,}000 Dutch 19-year-old men; \ test "
             r"scores fell with each later birth and with family size", WHITE),
            (r"Petter Kristensen and Tor Bjerkedal, \ 2007: \ 241{,}310 Norwegian conscripts; \ second-born "
             r"sons whose elder sibling had died in infancy scored like firstborns: \ the rank in which a child "
             r"is raised, \ not the order of birth", AGE),
            (r"Julia Rohrer, \ Boris Egloff and Stefan Schmukle, \ 2015: \ more than 20{,}000 adults in three "
             r"countries, \ within families: \ a small decline in IQ with birth order, \ and none in the Big Five",
             COHORT),
            (r"Rodica Damian and Brent Roberts, \ 2015: \ 377{,}000 American high-school students: \ an average "
             r"correlation of 0.02 with personality, \ 0.04 with intelligence, \ about one IQ point", CARE),
            (r"the popular theory, \ birth order shapes personality, \ failed; \ the small IQ difference holds, \ "
             r"and the first-born is the brighter in only about six pairs in ten", YOU),
        ], 12.4, 22, 0.32).move_to([0, -0.4, 0])
        tag = published_tag(r"Belmont \& Marolla (1973); \ Kristensen \& Bjerkedal (2007); \ Rohrer et al.\ (2015); "
                            r"\ Damian \& Roberts (2015)")
        with self.voiceover(
            "And then there's birth order, the oldest folk theory of family life. <bookmark mark='a'/> In 1973, "
            "Lillian Belmont and Francis Marolla studied nearly four hundred thousand Dutch nineteen-year-old men: "
            "test scores fell with each later birth and with family size. <bookmark mark='b'/> In 2007 Petter "
            "Kristensen and Tor Bjerkedal studied two hundred and forty-one thousand Norwegian conscripts. Second-born "
            "sons whose elder sibling had died in infancy scored like firstborns. What mattered was the rank in "
            "which a child was raised, not the order of birth. <bookmark mark='c'/> In 2015 Julia Rohrer, Boris "
            "Egloff and Stefan Schmukle compared siblings within families in three national panels, more than twenty "
            "thousand adults: a small decline in IQ with birth order, and none in the Big Five personality traits. "
            "<bookmark mark='d'/> The same year, Rodica Damian and Brent Roberts studied three hundred and "
            "seventy-seven thousand American high-school students: an average correlation of 0.02 with personality "
            "and 0.04 with intelligence, about one IQ point. <bookmark mark='e'/> So the popular theory, that birth "
            "order shapes personality, failed. The small IQ difference holds, and even so the first-born is the "
            "brighter in only about six pairs of siblings in ten."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
