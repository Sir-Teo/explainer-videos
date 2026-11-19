from __future__ import annotations

from videos.economics.econ4.common import *  # noqa: F403

ALWAYS = "#9AA5B8"
NEVER = "#5C6670"
COMPLIER = "#7BD88F"
DESIGN = "#7BD88F"
STRUCT = "#C9A0FF"


class Structure(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Structure and design", r"What does an estimate tell you about a policy nobody has tried?",
             "Chapter ten. Structure and design.", lit=("government",), scale=("person", "nation"),
             horizon=("a decade",))
        self.late()
        self.debate()
        self.compare()

    def late(self):
        # an illustrative population of 60: who serves, with and without a low lottery number
        kinds = [(r"volunteers", r"serve whatever their number", ALWAYS, 12),
                 (r"never serve", r"exempt, unfit, or refuse, whatever their number", NEVER, 30),
                 (r"compliers", r"serve if and only if their number is called", COMPLIER, 18)]
        groups = VGroup()
        for name, desc, col, n in kinds:
            dots = VGroup(*[Dot(radius=0.11, color=col) for _ in range(n)]).arrange_in_grid(rows=3, buff=0.12)
            t = label(name, font_size=25, color=col)
            dsc = label(desc, font_size=19, color=GREY_A)
            g = VGroup(dots, t, dsc).arrange(DOWN, buff=0.18)
            groups.add(g)
        groups.arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to(UP * 0.7)
        no_def = label(r"and no one who serves \emph{only} if his number is \emph{not} called \ (``no defiers'')",
                       font_size=21, color=GREY_B).next_to(groups, DOWN, buff=0.4)
        box = SurroundingRectangle(groups[2], color=COMPLIER, buff=0.15, corner_radius=0.1)
        res = VGroup(
            label(r"the lottery moves only the compliers, \ so the instrument measures the effect \emph{on them}",
                  font_size=25, color=COMPLIER),
            label(r"the local average treatment effect \ (Imbens and Angrist, 1994)", font_size=26, color=E.ACCENT),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        tag = note(r"illustrative shares", font_size=15, color=GREY_B).to_corner(DR, buff=0.3)
        ask = label(r"What does an instrument estimate?", font_size=34).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Before the debate, a precise question: what exactly does an instrument estimate? "
            "<bookmark mark='a'/> Think of the men in the draft lottery as three kinds. Some volunteered, and "
            "would have served whatever their number. <bookmark mark='b'/> Some would never serve: exempt, unfit, "
            "or unwilling, whatever their number. <bookmark mark='c'/> And some served only because their number "
            "was called. <bookmark mark='d'/> Assume nobody was so contrary that he served only if his number was "
            "not called. <bookmark mark='e'/> Then the lottery changes what happens only to the third group, the "
            "compliers. The other two do the same thing either way, so the comparison by lottery number can only "
            "reflect the compliers' experience. <bookmark mark='f'/> In 1994 Guido Imbens and Joshua Angrist proved "
            "it: an instrument estimates the average effect for the people it moves. They called it the local "
            "average treatment effect. Angrist's fifteen percent is the cost of service for men who served because "
            "they were drafted, not for volunteers."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(ask))
            vo.wait_until("a")
            self.play(FadeIn(groups[0]))
            vo.wait_until("b")
            self.play(FadeIn(groups[1]))
            vo.wait_until("c")
            self.play(FadeIn(groups[2]))
            vo.wait_until("d")
            self.play(FadeIn(no_def))
            vo.wait_until("e")
            self.play(Create(box), groups[0].animate.set_opacity(0.35), groups[1].animate.set_opacity(0.35),
                      FadeIn(res[0]))
            vo.wait_until("f")
            self.play(FadeIn(res[1]))
        self.clear_scene()

    def debate(self):
        cards = VGroup(
            history_card(r"Deaton", r"``Instruments, Randomization, and Learning about Development''",
                         r"the people an instrument moves may not be the people a policy would; an experiment says "
                         r"what happened, not why; without the why, results do not travel", color="#F28C6F",
                         width=4.15, font_size=21),
            history_card(r"Imbens", r"``Better LATE Than Nothing''",
                         r"a credible answer to a narrow question beats an incredible answer to a broad one; and "
                         r"designs can be repeated where the policy will go", color=COMPLIER, width=4.15,
                         font_size=21),
            history_card(r"Heckman", r"``Building Bridges between Structural and Program Evaluation Approaches''",
                         r"use the designs to pin down the parameters of an economic model, then let the model "
                         r"answer the new question", color=STRUCT, width=4.15, font_size=21),
        ).arrange(RIGHT, buff=0.25, aligned_edge=UP).move_to(UP * 0.4)
        head = label(r"\emph{Journal of Economic Literature} 48(2), June 2010", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.4)
        ex = label(r"the PROGRESA trial showed what the grants did in rural Mexico in 1998: \\ would they work the "
                   r"same in a city, at twice the size, or ten years on?", font_size=23, color=E.ACCENT)
        ex.to_edge(DOWN, buff=0.5)
        tag = published_tag(r"Deaton; Imbens; Heckman: JEL 48(2) (2010)", corner=DR, font_size=13)
        with self.voiceover(
            "In 2010 one issue of the Journal of Economic Literature carried the argument. <bookmark mark='a'/> "
            "Angus Deaton warned that the people an instrument moves may not be the people a policy would move, "
            "and that an experiment tells you what happened without telling you why. Without the why, he argued, "
            "results don't travel. <bookmark mark='b'/> Guido Imbens replied that a credible answer to a narrow "
            "question beats an incredible answer to a broad one, and that experiments can be repeated where the "
            "policy is headed. <bookmark mark='c'/> James Heckman asked for a bridge: use the designs to pin down "
            "the parameters of an economic model, and let the model answer the new question. "
            "<bookmark mark='d'/> The stakes are concrete. The PROGRESA trial showed what the grants did in rural "
            "Mexico in 1998. Would they do the same in a city, at twice the size, or ten years later?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c_ in zip("abc", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c_, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(ex))
        self.clear_scene()

    def compare(self):
        rows = [(r"", r"design", r"structure"),
                (r"it gives", r"an effect: \ of this change, \\ on these people", r"parameters: \ tastes, \\ "
                                                                                    r"technology, expectations"),
                (r"it assumes", r"little, \ and says what: \\ the lottery was fair", r"more: \ the shape of the "
                                                                                    r"model, \\ how people decide"),
                (r"a new policy", r"only one like the one tested", r"yes, \ if the model is right"),
                (r"Lucas", r"exposed", r"its answer, \ if the parameters \\ really are deep")]
        table = VGroup()
        for i, (a, b, c) in enumerate(rows):
            fs = 25 if i == 0 else 22
            table.add(VGroup(label(a, font_size=fs, color=GREY_B) if a else VectorizedPoint(),
                             label(b, font_size=fs, color=DESIGN),
                             label(c, font_size=fs, color=STRUCT)))
        for r in table:
            for j, x in enumerate((-5.0, -1.4, 3.2)):
                r[j].move_to([x, 0, 0])
        table.arrange(DOWN, buff=0.3).move_to(UP * 0.9)
        for r in table:
            for j, x in enumerate((-5.0, -1.4, 3.2)):
                r[j].set_x(x)
        rule = Line(LEFT * 6.3, RIGHT * 6.3, color=GREY_C, stroke_width=1.5).next_to(table[0], DOWN, buff=0.15)
        bridge = VGroup(
            label(r"bridges: \ sufficient statistics \ (Chetty, 2009): \ a few well-identified elasticities "
                  r"answer \\ many welfare questions; \ in macro, natural experiments pin down the moments a model "
                  r"must match \ (Nakamura and Steinsson, 2018)", font_size=21, color=E.ACCENT),
            label(r"the Island has both: \ its structure is planted, \ and every design is graded against it",
                  font_size=23, color=E.TRUTH),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"Chetty, Annu.\ Rev.\ Econ.\ 1 (2009); Nakamura and Steinsson, JEP 32(3) (2018)",
                            corner=DR, font_size=13).shift(UP * 0.0)
        with self.voiceover(
            "Here is the trade. <bookmark mark='a'/> A design gives you an effect: of this change, on these people. "
            "A structural model gives you parameters, such as how much people value leisure, or how they form "
            "expectations. <bookmark mark='b'/> The design assumes little, and says exactly what. The model assumes "
            "more: the shape of its equations, how people decide. <bookmark mark='c'/> The design can only speak to "
            "a policy like the one it tested. The model can speak to any policy, if it's right. "
            "<bookmark mark='d'/> And the Lucas critique cuts the design and is the model's whole reason to exist, "
            "provided its parameters really are the deep ones. <bookmark mark='e'/> Most good work today builds "
            "bridges. Raj Chetty showed in 2009 that many welfare questions need only a few well-identified "
            "elasticities, sufficient statistics, rather than a whole model. And in macroeconomics, where "
            "experiments are rare, Emi Nakamura and Jón Steinsson argued in 2018 for using natural experiments to "
            "pin down facts that any model must match. <bookmark mark='f'/> The Island has both. Its structure is "
            "planted, and every design in this series will be graded against it."
        ) as vo:
            self.play(FadeIn(table[0]), Create(rule), FadeIn(tag))
            for mk, r in zip("abcd", table[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(bridge[0]))
            vo.wait_until("f")
            self.play(FadeIn(bridge[1]))
        self.clear_scene()
