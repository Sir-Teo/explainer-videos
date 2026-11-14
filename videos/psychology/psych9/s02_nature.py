from __future__ import annotations

import numpy as np

from videos.psychology.psych9.common import *  # noqa: F403


class Nature(VoiceoverScene):
    def construct(self):
        self.card()
        self.galton()
        self.two_worlds()
        self.eugenics()

    def card(self):
        card = chapter_card(1, r"Nature and nurture", r"Why can a family tree not answer the question?",
                            lit={1875: r"Galton's twins"}, part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover(
            "Chapter one. Nature and nurture."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def galton(self):
        g = archive.GALTON_1875.data
        head = heading(rf"{g['hereditary_genius']}: \ eminence runs in families")
        father = VGroup(little_person(1.3, VOLT), label(r"a judge", font_size=30, color=VOLT)).arrange(DOWN, buff=0.12)
        son = VGroup(little_person(1.0, VOLT), label(r"his son", font_size=30, color=VOLT)).arrange(DOWN, buff=0.12)
        father.move_to([-4.6, 1.2, 0])
        son.move_to([-4.6, -2.0, 0])
        a1 = Arrow(father.get_bottom() + LEFT * 0.55, son.get_top() + LEFT * 0.55, buff=0.12, color=GENE, stroke_width=6)
        a2 = Arrow(father.get_bottom() + RIGHT * 0.55, son.get_top() + RIGHT * 0.55, buff=0.12, color=HOME, stroke_width=6)
        l1 = label(r"his genes", font_size=30, color=GENE).next_to(a1, LEFT, buff=0.15)
        l2 = wrapped_label(r"his house, \ his books, \ his school, \ his name", 2.9, 29, HOME).next_to(a2, RIGHT, buff=0.15)
        rows = rows_of([
            (r"Francis Galton lists the relatives of eminent judges, \ statesmen, \ scientists and poets", WHITE),
            (r"their close relatives are far more often eminent than strangers are", WHITE),
            (r"his conclusion: \ ability is inherited", DATA),
            (r"but a family passes on genes and a home together: \ a family tree cannot say which did the work", BAD),
        ], 6.0, 30, 0.3).move_to([3.7, -0.2, 0])
        keep_in_frame(rows)
        src = historical_tag(archive.GALTON_1875.cite)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "The phrase comes from Francis Galton, a cousin of Charles Darwin. In "
            f"{g['hereditary_genius']} he published a book called Hereditary Genius. "
            "<bookmark mark='a'/> He'd gone through the families of eminent English judges, statesmen, "
            "scientists and poets, and found that eminence ran in families. The close relatives of an "
            "eminent man were far more likely to be eminent than strangers were. <bookmark mark='b'/> He "
            "concluded that ability is inherited. <bookmark mark='c'/> You can see the hole in the "
            "argument. The son of a judge gets his father's genes. He also gets his father's house, his "
            "books, his school, his name and his friends. <bookmark mark='d'/> A family passes on both at "
            f"once, so a family tree can't tell you which one did the work. Galton saw the difficulty, "
            f"and in {g['twins']} he tried a way round it. He sent a questionnaire to twins."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(father), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(son), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(GrowArrow(a1), FadeIn(l1), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(GrowArrow(a2), FadeIn(l2))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def two_worlds(self):
        c = load("confound")
        head = heading(r"Two worlds that look the same from inside a family")
        panels = []
        for x0, key, name, col in ((-4.6, "genes", r"a world of genes", GENE), (0.3, "homes", r"a world of homes", HOME)):
            A = axes([-3, 3], [-3, 3], x_length=4.0, y_length=3.2, xticks=[], yticks=[], xlabel=r"parent", ylabel=r"child",
                     center=[x0, 0.5, 0])
            pts = scatter(A.ax, c[f"{key}_parent"], c[f"{key}_child"], col, radius=0.03, opacity=0.6)
            title = label(name, font_size=32, color=col).next_to(A.ax.c2p(0, 3), UP, buff=0.12)
            r = label(rf"$r = {r2(c[f'r_{key}'])}$", font_size=32, color=col).next_to(A.ax.c2p(-3, 3), DR, buff=0.12)
            panels.append(VGroup(A, pts, title, r))

        def rowpair(x0, bio, ado, col):
            t1 = label(rf"birth parents: \ ${r2(abs(bio))}$", font_size=30, color=col)
            t2 = label(rf"adoptive parents: \ ${r2(abs(ado))}$", font_size=30, color=col)
            g = VGroup(t1, t2).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            return g.move_to([x0, -2.75, 0])

        ad_g = rowpair(-4.6, c["genes_biological"], c["genes_adoptive"], GENE)
        ad_h = rowpair(0.3, c["homes_biological"], c["homes_adoptive"], HOME)
        keep_in_frame(ad_g)
        ad_l = label(r"adopted children: \ how alike are they and \dots", font_size=29, color=THRESH).move_to([-2.2, -2.0, 0])
        end = wrapped_label(r"Every design in this part looks for people who share genes but not a home, \ or a home but "
                            r"not genes.", 3.3, 29, P.ACCENT).move_to([5.25, 0.5, 0])
        keep_in_frame(end)
        tag = psyche_tag(r"simulated: two imaginary populations")
        with self.voiceover(
            "Here's the difficulty as a picture. Two imaginary worlds. In the first, a trait is passed on "
            "entirely through genes, and homes make no difference. <bookmark mark='a'/> Measure parents "
            f"and their children. The correlation is {c['r_genes']:.2f}. <bookmark mark='b'/> In the "
            "second world there are no genes for the trait at all. Children resemble their parents only "
            f"because they grow up in their parents' home. The correlation: {c['r_homes']:.2f}. "
            "<bookmark mark='c'/> The two pictures are the same. No amount of data on ordinary families "
            "can tell these worlds apart. <bookmark mark='d'/> So do something to the families. Take "
            "children who were raised from birth by other people. In the world of genes, they still "
            f"resemble the parents who gave them their genes, {c['genes_biological']:.2f}, and not the "
            f"parents who raised them, {abs(c['genes_adoptive']):.2f}. In the world of homes it's the "
            "reverse. <bookmark mark='e'/> That's the logic of every design in this part. Find people who "
            "share genes but not a home, or a home but not genes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(panels[0][0]), FadeIn(panels[0][2]))
            vo.wait_until("a")
            self.play(FadeIn(panels[0][1], lag_ratio=0.002), FadeIn(panels[0][3]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(panels[1][0]), FadeIn(panels[1][2]), FadeIn(panels[1][1], lag_ratio=0.002), FadeIn(panels[1][3]),
                      run_time=1.5)
            vo.wait_until("c")
            self.play(Indicate(panels[0][3], color=WHITE), Indicate(panels[1][3], color=WHITE))
            vo.wait_until("d")
            self.play(FadeIn(ad_l), FadeIn(ad_g), FadeIn(ad_h))
            vo.wait_until("e")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def eugenics(self):
        g = archive.GALTON_1875.data
        head = heading(r"Where Galton's programme went")
        line = Line([-6.2, 1.6, 0], [6.2, 1.6, 0], color=GREY_B, stroke_width=3)
        marks = VGroup()
        for x, year, what in ((-5.0, g["hereditary_genius"], r"Hereditary Genius"), (-1.2, g["twins"], r"the twins"),
                              (2.6, g["eugenics_coined"], r"he coins ``eugenics''")):
            marks.add(VGroup(Dot([x, 1.6, 0], radius=0.09, color=DATA),
                             label(str(year), font_size=30, color=DATA).move_to([x, 2.05, 0]),
                             label(what, font_size=28, color=WHITE).move_to([x, 1.15, 0])))
        rows = rows_of([
            (r"eugenics: \ improving a population by controlling who has children", WHITE),
            (r"within fifty years it was law in many countries: \ forced sterilization, \ immigration quotas, \ and worse", BAD),
            (r"the science it claimed was mostly wrong; \ chapter 6 lists the mistakes; \ the history is Part 32", GREY_A),
            (r"A careful answer to ``how much is inherited?'' is the best protection against the careless ones.", P.ACCENT),
        ], 12.4, 31, 0.3).move_to([0, -1.5, 0])
        src = historical_tag(archive.GALTON_1875.cite)
        with self.voiceover(
            "One more thing has to be said about Galton before we borrow his question. He didn't stop at "
            f"measuring. <bookmark mark='a'/> In {g['eugenics_coined']} he coined a word, eugenics, for "
            "the project of improving a population by controlling who has children. "
            "<bookmark mark='b'/> Within fifty years that idea was law in many countries: forced "
            "sterilization, immigration quotas, and worse. <bookmark mark='c'/> The science it claimed was "
            "mostly wrong, and chapter six will show exactly which mistakes it made about the number we're "
            "about to compute. The history itself is told in Part 32. <bookmark mark='d'/> For now, keep "
            "one thing in mind. The question of how much is inherited has been used to hurt people, and a "
            "careful answer to it is the best protection against the careless ones."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), Create(line), FadeIn(marks[0]), FadeIn(marks[1]))
            vo.wait_until("a")
            self.play(FadeIn(marks[2]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()
