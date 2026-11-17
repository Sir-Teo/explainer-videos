from __future__ import annotations

from videos.psychology.psych31.common import *  # noqa: F403


class Parents(VoiceoverScene):
    def construct(self):
        self.card()
        self.styles()
        self.confound()
        self.siblings()
        self.nurture()
        self.birth_order()
        self.ecology()

    def card(self):
        card = chapter_card(7, r"Parents", r"What do parents do to how a child turns out?",
                            lit={1987: r"Plomin \& Daniels", 1998: r"Harris", 2015: r"Rohrer et al."}, part=PART,
                            scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter seven. Parents."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def styles(self):
        head = heading(r"Four parenting styles")
        q = quadrant([
            (r"authoritarian", r"firm rules, \ obedience, \ few reasons", LOST),
            (r"authoritative", r"warm, \ firm, \ explains its rules", GOOD),
            (r"neglectful", r"little warmth, \ little supervision", GREY_B),
            (r"indulgent", r"warm, \ asks little", CARE),
        ], xlabel=r"responsiveness: \ warmth", ylabel=r"demandingness: \ control", size=5.0, font_size=21)
        q.move_to([-3.45, -0.2, 0])
        card_ = theory_card(r"Parenting styles", r"Diana Baumrind, \ 1966--1971; \ Maccoby and Martin, \ 1983",
                            r"warm, \ firm parents who explain their rules raise competent children",
                            r"the correlation holds; \ how much of it the style causes is in doubt", "contested",
                            width=6.3, font_size=20, color=CARE)
        card_.move_to([3.45, 1.15, 0])
        checks = verdict_row([
            (r"Lamborn and colleagues, \ 1991: \ about 4{,}100 teenagers; \ authoritative homes best, \ "
             r"neglectful homes worst", "replicated"),
            (r"that the style is the cause: \ children shape their parents \ (Bell, \ 1968) \ and share their "
             r"genes \ (Avinun and Knafo, \ 2014)", "contested"),
        ], width=6.3, font_size=19)
        checks.next_to(card_, DOWN, buff=0.3)
        tag = published_tag(r"Baumrind (1966, \ 1971); \ Maccoby \& Martin (1983); \ Lamborn et al.\ (1991); \ "
                            r"Bell (1968)")
        with self.voiceover(
            "Before the twin studies, the textbook answer was a typology. <bookmark mark='a'/> In the 1960s Diana "
            "Baumrind observed preschool children in California, at home and in nursery school, and sorted their "
            "parents. Authoritarian parents set firm rules and expected obedience, without reasons. Permissive "
            "parents were warm and asked little. Authoritative parents were both warm and firm, and explained their "
            "rules. <bookmark mark='b'/> In 1983 Eleanor Maccoby and John Martin turned the types into two "
            "dimensions, how responsive a parent is and how demanding, and Baumrind's permissive parents split in "
            "two: indulgent ones, warm but undemanding, and neglectful ones, neither warm nor demanding. "
            "<bookmark mark='c'/> The children of authoritative parents did best, and as a correlation that has "
            "held up. In 1991 Susie Lamborn and colleagues surveyed about four thousand one hundred American "
            "teenagers: those from authoritative homes had the best grades and adjustment, and those from "
            "neglectful homes the worst. <bookmark mark='d'/> But a correlation between families has more than one "
            "cause. In 1968 Richard Bell pointed out that children shape their parents too: an easy child invites "
            "warmth and reasons, a defiant one invites force. And parents and children share genes, which twin "
            "studies find even in how parents treat each child. <bookmark mark='e'/> So the style goes with the "
            "outcome. How much of the outcome the style causes is the question for the rest of this chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(q.axes))
            vo.wait_until("a")
            self.play(FadeIn(q.cells[0]), FadeIn(q.cells[1]), FadeIn(q.cells[3]),
                      FadeIn(card_.box), FadeIn(card_.name), FadeIn(card_.claim), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(q.cells[2], scale=0.9), Indicate(q.cells[3].title, color=CARE))
            vo.wait_until("c")
            self.play(FadeIn(checks.rows[0], shift=RIGHT * 0.15), Indicate(q.cells[1].box, color=GOOD,
                                                                            scale_factor=1.04))
            vo.wait_until("d")
            self.play(FadeIn(checks.rows[1], shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(card_.verdict), FadeIn(card_.status))
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

    def ecology(self):
        head = heading(r"Beyond the family")
        rg = rings([(r"microsystem", CARE), (r"mesosystem", CHILD), (r"exosystem", AGE), (r"macrosystem", COHORT)],
                   radius=2.6, font_size=20, centre=person(0.55, CHILD))
        rg.move_to([-3.4, 0.0, 0])
        notes = VGroup(
            label(r"family, \ class, \ friends", font_size=19, color=CARE),
            label(r"the links between them", font_size=19, color=CHILD),
            label(r"a parent's workplace, \ the council", font_size=19, color=AGE),
            label(r"culture, \ laws, \ the economy", font_size=19, color=COHORT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        notes.move_to([2.35, 1.35, 0], aligned_edge=LEFT)
        dots = VGroup(*[Dot(radius=0.06, color=c).next_to(n, LEFT, buff=0.18)
                        for n, c in zip(notes, (CARE, CHILD, AGE, COHORT))])
        chrono = Arrow([-6.4, -3.4, 0], [-0.4, -3.4, 0], buff=0, color=PERIOD, stroke_width=4,
                       max_tip_length_to_length_ratio=0.04)
        chrono_l = label(r"chronosystem: \ the year and the generation \ (chapter one's clocks)", font_size=19,
                         color=PERIOD).next_to(chrono, UP, buff=0.08)
        card_ = theory_card(r"Ecological systems", r"Urie Bronfenbrenner, \ 1979",
                            r"a child develops inside nested settings, \ and the links between them",
                            r"a map of where a cause might sit, \ not a prediction that could fail",
                            "not directly tested", width=5.2, font_size=19, color=COHORT)
        card_.move_to([4.05, -1.55, 0])
        tag = published_tag(r"Bronfenbrenner (1979, \ 1986)", corner=DR)
        with self.voiceover(
            "Parents, siblings and birth order all sit inside the family. An older framework drew what lies "
            "around it. <bookmark mark='a'/> In 1979 Urie Bronfenbrenner described a child's world as nested "
            "systems. The microsystem is the settings the child is in: the family, the classroom, the friends. "
            "<bookmark mark='b'/> The mesosystem is the links between them, such as whether home and school pull "
            "the same way. <bookmark mark='c'/> The exosystem holds settings the child never enters that still "
            "reach it, like a parent's workplace or the local council. The macrosystem is the culture, the laws "
            "and the economy around all of these. <bookmark mark='d'/> Later he added the chronosystem, time: the "
            "year and the generation a child grows up in, which are chapter one's period and cohort clocks. "
            "<bookmark mark='e'/> It is a framework rather than a theory with a prediction that could fail, and its "
            "use is as a map of where a cause might sit. It was also meant for action: Bronfenbrenner helped plan "
            "Head Start, the kind of programme the next chapter tests."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rg.centre))
            vo.wait_until("a")
            self.play(FadeIn(rg.rings[0]), FadeIn(dots[0]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(rg.rings[1]), FadeIn(dots[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(rg.rings[2]), FadeIn(dots[2]), FadeIn(notes[2]))
            self.play(FadeIn(rg.rings[3]), FadeIn(dots[3]), FadeIn(notes[3]))
            vo.wait_until("d")
            self.play(GrowArrow(chrono), FadeIn(chrono_l))
            vo.wait_until("e")
            self.play(FadeIn(card_, shift=UP * 0.15))
        self.clear_scene()
