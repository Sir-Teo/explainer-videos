from __future__ import annotations

from videos.philosophy.philosophy10.common import *  # noqa: F403

JUDGMENTS = [("quantity", ["universal", "particular", "singular"]),
             ("quality", ["affirmative", "negative", "infinite"]),
             ("relation", ["categorical", "hypothetical", "disjunctive"]),
             ("modality", ["problematic", "assertoric", "apodictic"])]
CATEGORIES = [("quantity", ["unity", "plurality", "totality"]),
              ("quality", ["reality", "negation", "limitation"]),
              ("relation", ["substance and accident", "cause and effect", "community"]),
              ("modality", ["possibility", "existence", "necessity"])]


class Categories(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"The categories", r"What must hold of anything we can experience?", lit=(1781,),
                            part=PART)
        with self.voiceover("Chapter eleven. The categories."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.tables()
        self.deduction()
        self.analogy()

    def tables(self):
        head = label(r"From the forms of judgment \ to the categories", font_size=30, color=CONN).to_edge(UP, buff=0.3)

        def table(spec, color, title):
            cells = VGroup()
            for g, items in spec:
                cells.add(VGroup(label(g, font_size=22, color=color),
                                 *[label(t, font_size=19, color=WHITE) for t in items]).arrange(DOWN, buff=0.1))
            cells.arrange_in_grid(rows=2, cols=2, buff=(0.6, 0.35))
            return VGroup(label(title, font_size=24, color=color), cells).arrange(DOWN, buff=0.25)
        tj = table(JUDGMENTS, REASON, r"twelve forms of judgment \ (logic)")
        tc = table(CATEGORIES, KANT, r"twelve categories \ (concepts of an object)")
        both = VGroup(tj, tc).arrange(RIGHT, buff=1.4)
        both.scale(min(1.4, 12.6 / both.width, 5.4 / both.height)).move_to([0, -0.1, 0])
        arr = Arrow(tj.get_right(), tc.get_left(), buff=0.2, color=GREY_B)
        eg = label(r"`if $p$, then $q$' \ (hypothetical) \ $\longrightarrow$ \ cause and effect", font_size=22,
                   color=GOAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The second part of the answer concerns thought. <bookmark mark='a'/>Logic, Kant believed, had been "
            "complete since Aristotle, and it sorts every judgment along four headings: quantity, quality, relation "
            "and modality, three forms under each. <bookmark mark='b'/>To each form of judgment corresponds a pure "
            "concept of an object in general, a category. Twelve forms, twelve categories. <bookmark mark='c'/>For "
            "example, the hypothetical judgment, if p then q, corresponds to the category of cause and effect. The "
            "categorical judgment, S is P, corresponds to substance and its properties."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tj))
            vo.wait_until("b")
            self.play(GrowArrow(arr), FadeIn(tc))
            vo.wait_until("c")
            self.play(FadeIn(eg), Indicate(tj[1][2], color=GOAL), Indicate(tc[1][2], color=GOAL))
        self.clear_scene()

    def deduction(self):
        q = quote_card(r"The I think must be able to accompany all my representations.", r"Immanuel Kant",
                       r"\textit{Critique of Pure Reason}, \ B131", width=8.4, font_size=30).move_to([0, 2.2, 0])
        steps = VGroup(
            label(r"1. \ experience is a unity: \ all my representations belong to one self", font_size=24),
            label(r"2. \ unity requires combining them by rules", font_size=24),
            label(r"3. \ the rules of combination are the categories", font_size=24, color=KANT),
            label(r"4. \ so the categories hold of every object of possible experience", font_size=24, color=GOAL),
            label(r"so `every event has a cause' \ is not learned from experience: \ it is a condition of having any",
                  font_size=23, color=OK)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -1.2, 0])
        with self.voiceover(
            "Why should the categories apply to the world? This is the transcendental deduction, the hardest part of "
            "the Critique, and here is the structure of its argument. <bookmark mark='a'/>The I think must be able to "
            "accompany all my representations. <bookmark mark='b'/>My experiences are all mine: they form one "
            "experience, of one self. <bookmark mark='c'/>That unity is not given; it requires that the mind combine "
            "its representations by rules. <bookmark mark='d'/>The rules of combination are the categories. "
            "<bookmark mark='e'/>So the categories hold of every object of possible experience. <bookmark mark='f'/>And "
            "so Hume's problem dissolves: every event has a cause is not something we learn from experience, and "
            "could never learn. It is a condition of having experience at all."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            for mk, s_ in zip("bcdef", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s_, shift=RIGHT * 0.1))
        self.clear_scene()

    def analogy(self):
        head = label(r"The second analogy: \ the house and the ship", font_size=30, color=CONN).to_edge(UP, buff=0.4)
        house = VGroup(Polygon([-0.8, 0, 0], [0.8, 0, 0], [0.8, 1.0, 0], [0, 1.6, 0], [-0.8, 1.0, 0],
                               color=SENSE, stroke_width=3)).move_to([-3.6, 0.8, 0])
        hp = VGroup(*[label(t, font_size=20, color=GREY_A) for t in (r"roof, \ then base", r"base, \ then roof")]
                    ).arrange(DOWN, buff=0.15).next_to(house, DOWN, buff=0.35)
        river = Line([1.2, 0.5, 0], [6.2, 0.5, 0], color=REASON, stroke_width=3)
        ship = Triangle(color=WHITE, fill_opacity=0.5).scale(0.25).move_to([2.0, 0.85, 0])
        sp = VGroup(label(r"upstream, \ then downstream", font_size=20, color=GREY_A),
                    label(r"never the other way", font_size=20, color=BAD)).arrange(DOWN, buff=0.15).next_to(
            river, DOWN, buff=0.45)
        rows = VGroup(
            label(r"my perceptions of the house could have come in either order: \ no event", font_size=22),
            label(r"of the ship, \ the order is fixed: \ an event, \ something happened", font_size=22, color=GOAL),
            label(r"what fixes it? \ a rule: \ the later state follows the earlier by necessity", font_size=22,
                  color=KANT),
            label(r"so to experience an event at all \ is to apply the concept of cause", font_size=24,
                  color=OK)).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Kant made the argument concrete with a famous pair of examples, in the second analogy of experience. "
            "<bookmark mark='a'/>Look at a house. My eyes may run from the roof to the base, or from the base to the "
            "roof. The order of my perceptions could have been either. Nothing happened. <bookmark mark='b'/>Now "
            "watch a ship drift downstream. I see it first upstream, then downstream, and I could not have seen it "
            "the other way round. Here something happened: an event. <bookmark mark='c'/>What makes the order "
            "irreversible is not in the perceptions themselves. It is a rule: the later state follows the earlier "
            "necessarily. <bookmark mark='d'/>So to experience an event at all, as opposed to a mere sequence of "
            "perceptions, is already to apply the concept of cause. That is Kant's answer to Hume's billiard balls."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(house), FadeIn(hp), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(river), FadeIn(ship))
            self.play(ship.animate.move_to([5.4, 0.85, 0]), run_time=2.5, rate_func=linear)
            self.play(FadeIn(sp), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
