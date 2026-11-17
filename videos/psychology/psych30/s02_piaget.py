from __future__ import annotations

from videos.psychology.psych30.common import *  # noqa: F403


class Piaget(VoiceoverScene):
    def construct(self):
        self.card()
        self.theory()
        self.stages()
        self.conservation()

    def card(self):
        card = chapter_card(1, r"Piaget's infant", r"Does a mind build itself by acting?",
                            lit={1936: r"Piaget", 1937: r"Piaget"}, part=PART, scale=("person",),
                            marr=("what",))
        with self.voiceover("Chapter one. Piaget's infant."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def theory(self):
        head = heading(r"A child builds a mind by acting")
        sch = word_chip(r"scheme: \ grasp", color=OBJ, font_size=24).move_to([-4.0, 1.2, 0])
        assim = word_chip(r"assimilation: \ a new rattle, \ grasped the same way", color=LOOK, font_size=20)
        accom = word_chip(r"accommodation: \ a ball too big to grasp: \ the scheme changes", color=CARE, font_size=20)
        assim.move_to([-3.2, -0.2, 0])
        accom.move_to([-3.2, -1.4, 0])
        rows = rows_of([
            (r"Jean Piaget, \ a biologist by training, \ watched his own three children closely through infancy",
             WHITE),
            (r"knowledge is built from action: \ schemes, \ such as grasping or sucking, \ are applied to new "
             r"things \ (assimilation) \ and changed when they fail \ (accommodation)", OBJ),
            (r"development is a series of reorganizations, \ each stage a new kind of thinking, \ not just more "
             r"knowledge", LOOK),
            (r"his evidence: \ what children did, \ and what they said, \ in tasks he invented", GREY_A),
        ], 5.6, 21, 0.32).move_to([3.4, -0.1, 0])
        tag = historical_tag(r"Piaget (1936, \ 1937)")
        with self.voiceover(
            "Jean Piaget began as a biologist, and he studied children the way a naturalist studies a species, "
            "starting with his own. <bookmark mark='a'/> He watched his three children closely through their "
            "infancy and published his observations in the 1930s. <bookmark mark='b'/> His central idea was that "
            "knowledge is built from action. An infant has schemes, such as grasping or sucking. A new rattle is "
            "grasped the same way, which Piaget called assimilation. A ball too big to grasp forces the scheme to "
            "change, which he called accommodation. <bookmark mark='c'/> Development, for Piaget, is a series of "
            "reorganizations: each stage a new kind of thinking, not just more knowledge. "
            "<bookmark mark='d'/> His evidence was what children did and said in tasks he invented."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(sch))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(assim), FadeIn(accom), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def stages(self):
        head = heading(r"Four stages")
        stages = [(r"sensorimotor", r"birth to about 2", r"acting on the world; \ objects come to exist when out "
                   r"of sight", OBJ),
                  (r"preoperational", r"about 2 to 7", r"symbols and language; \ judgments tied to how things look",
                   LOOK),
                  (r"concrete operational", r"about 7 to 11", r"logical operations on real things: \ conservation, "
                   r"\ classification", NUM),
                  (r"formal operational", r"about 11 on", r"reasoning about the hypothetical and abstract", MIND)]
        blocks = VGroup()
        for i, (name, age, what, col) in enumerate(stages):
            box = RoundedRectangle(corner_radius=0.1, width=2.9, height=2.6, stroke_color=col, stroke_width=2,
                                   fill_color=BLACK, fill_opacity=0.5)
            t = VGroup(label(name, font_size=22, color=col), label(age, font_size=18, color=GREY_B),
                       wrapped_label(what, 2.6, 17, WHITE)).arrange(DOWN, buff=0.18)
            t.move_to(box)
            blocks.add(VGroup(box, t))
        blocks.arrange(RIGHT, buff=0.25).move_to([0, 0.6, 0])
        foot = rows_of([
            (r"the ages are rough, \ and later work found children doing many things earlier than Piaget's tasks "
             r"suggested, \ and adults often failing formal reasoning \ (Part 24)", GREY_A),
            (r"the A-not-B error belongs to the fourth of six sub-stages of the sensorimotor period, \ around "
             r"eight to twelve months", A_COL),
        ], 12.4, 22, 0.3).to_edge(DOWN, buff=0.7)
        tag = historical_tag(r"Piaget (1936, \ 1937)")
        with self.voiceover(
            "Piaget described four stages. <bookmark mark='a'/> The sensorimotor stage, from birth to about two, "
            "is thinking by acting; during it, objects come to exist even when out of sight. "
            "<bookmark mark='b'/> The preoperational stage, from about two to seven, brings symbols and language, "
            "but judgments are tied to how things look. <bookmark mark='c'/> The concrete operational stage, from "
            "about seven to eleven, brings logical operations on real things, such as conservation and "
            "classification. <bookmark mark='d'/> And the formal operational stage, from about eleven, brings "
            "reasoning about the hypothetical and the abstract. <bookmark mark='e'/> The ages are rough. Later "
            "work found children doing many things earlier than Piaget's tasks suggested, and adults often failing "
            "at formal reasoning, as Part 24 showed. The A-not-B error belongs to the sensorimotor period, around "
            "eight to twelve months."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, b in zip("abcd", blocks):
                vo.wait_until(m)
                self.play(FadeIn(b, shift=UP * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def conservation(self):
        head = heading(r"Conservation")
        def glass(w, h, fill, x):
            g = Rectangle(width=w, height=h, color=WHITE, stroke_width=3).move_to([x, -0.5 + h / 2, 0])
            water = Rectangle(width=w - 0.06, height=fill, color=LOOK, fill_color=LOOK, fill_opacity=0.6,
                              stroke_width=0).align_to(g, DOWN).shift(UP * 0.03).set_x(x)
            return VGroup(g, water)
        g1 = glass(1.2, 1.6, 1.0, -5.0)
        g2 = glass(1.2, 1.6, 1.0, -3.3)
        g3 = glass(0.6, 3.0, 2.0, -3.3)
        q = label(r"which has more?", font_size=22, color=YOU).move_to([-4.1, -1.3, 0])
        rows = rows_of([
            (r"two equal glasses of water; \ one is poured into a tall, \ thin glass while the child watches", WHITE),
            (r"a typical five-year-old says the tall glass has more: \ judged by height, \ one dimension at a "
             r"time", LOOK),
            (r"a typical eight-year-old says they are the same, \ because you could pour it back: \ "
             r"reversibility", NUM),
            (r"the task replicates easily; \ what it measures \ (logic, \ language, \ or reading the "
             r"experimenter's question) \ has been argued ever since", GREY_A),
        ], 5.8, 21, 0.32).move_to([3.4, -0.1, 0])
        tag = historical_tag(r"Piaget \& Szeminska (1941)")
        with self.voiceover(
            "The most famous of Piaget's tasks is conservation. <bookmark mark='a'/> A child sees two equal glasses "
            "of water. One is poured into a tall, thin glass while she watches. <bookmark mark='b'/> A typical "
            "five-year-old says the tall glass has more. She judges by height, attending to one dimension at a "
            "time. <bookmark mark='c'/> A typical eight-year-old says they are the same, because you could pour it "
            "back. Piaget called this reversibility. <bookmark mark='d'/> The task replicates easily. What it "
            "measures, logic, language, or how the child reads the experimenter's question, has been argued ever "
            "since. And in infancy the problem is worse: the infant can't answer at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(g1), FadeIn(g2))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Transform(g2, g3))
            vo.wait_until("b")
            self.play(FadeIn(q), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
