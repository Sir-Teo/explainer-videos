from __future__ import annotations

from videos.philosophy.philosophy11.common import *  # noqa: F403


class Plato(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Three answers in the \textit{Theaetetus}", r"What must be added to true belief?",
                            lit=(-380, -369), part=PART)
        with self.voiceover("Chapter one. Three answers in the Theaetetus."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.three()
        self.meno()
        self.jtb()

    def three(self):
        head = label(r"Theaetetus tries three times", font_size=32, color=CONN).to_edge(UP, buff=0.4)

        def col(n, title, lines, color):
            g = VGroup(label(n, font_size=22, color=GREY_B), label(title, font_size=26, color=color))
            for t, c in lines:
                g.add(label(t, font_size=20, color=c))
            for m in g:
                if m.width > 4.1:
                    m.width = 4.1
            return g.arrange(DOWN, buff=0.16)
        a = col(r"151e", r"perception", [(r"Protagoras: \ man is the measure", GREY_A),
                                         (r"but we hear a foreign tongue", WHITE),
                                         (r"without knowing what it says;", WHITE),
                                         (r"and we know what we remember", WHITE),
                                         (r"with our eyes shut", WHITE)], SKEP)
        b = col(r"187b", r"true judgment", [(r"the jury, \ persuaded by an orator", GREY_A),
                                            (r"of what only a witness could know,", WHITE),
                                            (r"judges truly", WHITE),
                                            (r"and does not know", BAD)], BEL)
        c = col(r"201c", r"true judgment with an account", [(r"an account: \ the parts? \ a mark?", GREY_A),
                                                            (r"to give the distinguishing mark", WHITE),
                                                            (r"you must already know", WHITE),
                                                            (r"how the thing differs: \ a circle", BAD)], JUST)
        cols = VGroup(a, b, c).arrange(RIGHT, buff=0.55, aligned_edge=UP).move_to([0, 0.4, 0])
        end = label(r"the dialogue ends without an answer \ (210b)", font_size=26, color=GOAL).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Socrates asks Theaetetus what knowledge is, and gets three answers. <bookmark mark='a'/>First: knowledge "
            "is perception. Socrates links this to Protagoras, who said that man is the measure of all things, and "
            "then attacks it. When we hear a language we do not speak, we perceive the sounds and do not know what "
            "they say. And when we shut our eyes, we still know what we saw a moment ago. <bookmark mark='b'/>Second: "
            "knowledge is true judgment. Socrates answers with a jury. A skilful orator persuades the jurors of what "
            "only an eyewitness could know. If the verdict is true, they judged truly, yet they did not know. "
            "<bookmark mark='c'/>Third: knowledge is true judgment with an account, a logos. But what is an account? "
            "Listing a thing's parts is not enough. Giving the mark that distinguishes it from everything else "
            "requires knowing how it differs, which is knowledge again: the definition goes round in a circle. "
            "<bookmark mark='d'/>The dialogue ends without an answer."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(b, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(end))
        self.clear_scene()

    def meno(self):
        hc = history_card(r"c.\ 385\ BCE", r"Plato", r"\textit{Meno} 97a--98a", width=4.0,
                          color=HIST).to_corner(UL, buff=0.35)
        road = Line([-5.6, 0.6, 0], [1.6, 0.6, 0], color=GREY_B, stroke_width=4)
        town = VGroup(*[Square(side_length=0.35, color=JUST, fill_opacity=0.4) for _ in range(3)]).arrange(
            RIGHT, buff=0.06).next_to(road, RIGHT, buff=0.15)
        town_l = label(r"Larissa", font_size=22, color=JUST).next_to(town, UP, buff=0.12)
        k = person(r"one has walked it", color=KNOW, scale=0.7).move_to([-4.6, 1.5, 0])
        o = person(r"one guesses right", color=BEL, scale=0.7).move_to([-2.3, 1.5, 0])
        note1 = label(r"both arrive: \ a true opinion guides as well as knowledge", font_size=23,
                      color=GREY_A).move_to([-1.9, -0.3, 0])
        statue = VGroup(Rectangle(width=0.5, height=1.1, color=GREY_B, fill_opacity=0.3),
                        Circle(radius=0.22, color=GREY_B, fill_opacity=0.3)).arrange(UP, buff=0.02).move_to(
            [4.6, 0.6, 0])
        rope = Line(statue.get_left() + RIGHT * 0.05, statue.get_left() + LEFT * 0.9 + DOWN * 0.5, color=JUST,
                    stroke_width=3)
        peg = Dot(rope.get_end(), color=JUST)
        st_l = label(r"Daedalus's statues run away \ unless tied down", font_size=21, color=GREY_A).next_to(
            statue, DOWN, buff=0.3)
        tie = VGroup(label(r"true opinions too, \ until tied down `by reasoning out the cause'", font_size=25,
                           color=JUST),
                     label(r"tied down, \ they become knowledge, \ and stay", font_size=25,
                           color=KNOW)).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "In an earlier dialogue, the Meno, Plato had already said what true opinion lacks. "
            "<bookmark mark='a'/>Two travellers want the road to Larissa. One has walked it and knows the way; the "
            "other has never been there but guesses right. Both arrive. As a guide to action, Socrates says, a true "
            "opinion is no worse than knowledge. <bookmark mark='b'/>So why do we value knowledge more? Because true "
            "opinions are like the statues of Daedalus, which were said to be so lifelike that they ran away unless "
            "they were tied down. <bookmark mark='c'/>True opinions do not stay long in the mind, until one ties them "
            "down by reasoning out the cause. Once tied down, they become knowledge, and they stay. The account, the "
            "tether, is what turns a lucky guess into knowledge."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Create(road), FadeIn(town), FadeIn(town_l), FadeIn(k), FadeIn(o))
            self.play(k.animate.move_to([0.9, 1.5, 0]), o.animate.move_to([-1.5, 1.5, 0]), run_time=2)
            self.play(FadeIn(note1))
            vo.wait_until("b")
            self.play(FadeIn(statue), FadeIn(st_l))
            vo.wait_until("c")
            self.play(Create(rope), FadeIn(peg), FadeIn(tie[0]))
            self.play(FadeIn(tie[1]))
        self.clear_scene()

    def jtb(self):
        head = label(r"Justified true belief", font_size=34, color=CONN).to_edge(UP, buff=0.35)
        f = MathTex(r"K_S\,p \;\iff\; p \;\land\; B_S\,p \;\land\; J_S\,p", font_size=44).next_to(head, DOWN,
                                                                                                  buff=0.35)
        tr = Circle(radius=1.55, stroke_color=OK, stroke_width=3, fill_color=OK, fill_opacity=0.08).move_to(
            [-0.95, -1.0, 0])
        be = Circle(radius=1.55, stroke_color=BEL, stroke_width=3, fill_color=BEL, fill_opacity=0.08).move_to(
            [0.95, -1.0, 0])
        ju = Ellipse(width=2.3, height=1.5, stroke_color=JUST, stroke_width=3).move_to([0.75, -1.35, 0])
        tl = label(r"true", font_size=24, color=OK).next_to(tr, LEFT, buff=0.15)
        bl = label(r"believed", font_size=24, color=BEL).next_to(be, RIGHT, buff=0.15)
        jl = label(r"justified", font_size=22, color=JUST).next_to(ju, DOWN, buff=0.08).shift(RIGHT * 0.9)
        kn = Intersection(Intersection(tr, be), ju, color=KNOW, fill_color=KNOW, fill_opacity=0.5,
                          stroke_width=0)
        kl = label(r"knowledge?", font_size=24, color=KNOW).move_to([-3.8, -2.6, 0])
        ka = Arrow(kl.get_right(), kn.get_center() + LEFT * 0.1, buff=0.15, color=KNOW, stroke_width=3)
        who = VGroup(label(r"Ayer (1956): \ `the right to be sure'", font_size=21, color=GREY_A),
                     label(r"Chisholm (1957): \ `adequate evidence'", font_size=21, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.6, -2.6, 0])
        with self.voiceover(
            "From Plato's third answer the twentieth century took a definition. <bookmark mark='a'/>S knows that p "
            "if and only if p is true, S believes p, and S is justified in believing p. <bookmark mark='b'/>Draw the "
            "true propositions, and the ones S believes. True beliefs lie where they overlap, but a lucky guess lies "
            "there too. <bookmark mark='c'/>So add justification: good evidence, good reasons, Plato's tether. "
            "<bookmark mark='d'/>Knowledge, on this analysis, is the region where all three overlap. Versions of it "
            "appear in Alfred Ayer, who in 1956 required the right to be sure, and Roderick Chisholm, who in 1957 "
            "required adequate evidence. It is usually called the traditional analysis, though few philosophers "
            "before them stated it so plainly. In 1963 it was refuted in three pages."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(Create(tr), Create(be), FadeIn(tl), FadeIn(bl))
            vo.wait_until("c")
            self.play(Create(ju), FadeIn(jl))
            vo.wait_until("d")
            self.play(FadeIn(kn), FadeIn(kl), GrowArrow(ka))
            self.play(FadeIn(who))
        self.clear_scene()
