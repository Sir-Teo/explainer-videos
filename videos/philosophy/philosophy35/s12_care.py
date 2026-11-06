from __future__ import annotations

from videos.philosophy.philosophy35.common import *  # noqa: F403


class Care(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Care", r"Is morality about principles, or about relationships?", lit=(1982, 1984),
                            part=PART)
        with self.voiceover("Chapter eleven. Care."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.heinz()
        self.care()
        self.thought()

    def heinz(self):
        head = label(r"A different voice \ (Gilligan, \ 1982)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"the dilemma", r"Heinz's wife is dying; \ the druggist charges far more than Heinz can pay: \ should "
                                 r"he steal the drug?", GREY_A),
                (r"Kohlberg's stages", r"moral maturity as reasoning from ever more universal principles of justice and "
                                       r"rights", DUTY),
                (r"Amy, \ eleven", r"`they should really just talk it out': \ she looks for a way to keep the "
                                   r"relationships, \ and scored lower", VIRT),
                (r"Gilligan", r"not a lower stage but a different voice: \ an ethics of care and responsibility, \ "
                              r"beside the ethics of justice", GOOD)]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.4)
        with self.voiceover(
            "In 1982 the psychologist Carol Gilligan challenged the leading theory of moral development. "
            "<bookmark mark='a'/>Lawrence Kohlberg had asked children about Heinz, whose wife is dying, and who "
            "cannot afford the drug that might save her: should he steal it? <bookmark mark='b'/>Kohlberg scored "
            "maturity by how far the reasoning rose toward universal principles of justice and rights. "
            "<bookmark mark='c'/>An eleven-year-old girl, Amy, said they should really just talk it out and find "
            "another way, so that no one is hurt and the relationships survive, and she scored lower than a boy who "
            "weighed life against property. <bookmark mark='d'/>Gilligan argued that Amy spoke in a different "
            "voice, not at a lower stage: an ethics of care and responsibility in relationships, beside the ethics "
            "of justice."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def care(self):
        head = label(r"The ethics of care", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"Noddings \ (1984)", r"caring is a relation: \ the one-caring attends to the cared-for, \ who "
                                      r"responds; \ ethics begins there, \ not in principles", GOOD),
                (r"Held \ (2006)", r"dependency is the normal human condition: \ children, \ the sick, \ the old; \ "
                                   r"theories built for independent equals miss most of life", VIRT),
                (r"Kittay; \ Tronto", r"care work, \ mostly unpaid and mostly done by women, \ as a question of "
                                      r"justice", AGG),
                (r"the challenge", r"partiality: \ may I favour those I love? \ impartial theories struggle to say why, "
                                   r"\ care ethics starts there", DUTY),
                (r"the worry", r"care for those near can neglect those far away: \ Part 36's question of whose "
                               r"interests count", HARM)]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.4)
        with self.voiceover(
            "Philosophers developed the idea into a theory. <bookmark mark='a'/>Nel Noddings, in 1984, made caring a "
            "relation: one person attends to another, who responds; ethics begins in that relation, not in "
            "principles. <bookmark mark='b'/>Virginia Held stressed that dependency is the normal human condition, "
            "in childhood, illness and age, so theories built for independent equals miss most of moral life. "
            "<bookmark mark='c'/>Eva Kittay and Joan Tronto turned care work, mostly unpaid and mostly done by "
            "women, into a question of justice. <bookmark mark='d'/>Care ethics starts from what impartial theories "
            "find hardest to explain: why I may favour those I love. <bookmark mark='e'/>Its critics worry that care "
            "for those near can neglect those far away, a question Part 36 takes up."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def thought(self):
        head = label(r"One thought too many \ (Williams, \ 1976)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        water = Rectangle(width=5.6, height=1.6, stroke_width=0, fill_color=DUTY, fill_opacity=0.18).move_to(
            [-3.4, 0.6, 0])
        wife = VGroup(Circle(radius=0.2, color=VIRT, stroke_width=3), label(r"his wife", font_size=15, color=VIRT))
        wife[1].next_to(wife[0], DOWN, buff=0.08)
        stranger = VGroup(Circle(radius=0.2, color=GREY_B, stroke_width=3),
                          label(r"a stranger", font_size=15, color=GREY_B))
        stranger[1].next_to(stranger[0], DOWN, buff=0.08)
        wife.move_to([-4.8, 0.7, 0])
        stranger.move_to([-2.0, 0.7, 0])
        man = VGroup(Circle(radius=0.22, color=GOOD, stroke_width=3), label(r"he can save one", font_size=15,
                                                                             color=GOOD))
        man[1].next_to(man[0], DOWN, buff=0.08)
        man.move_to([-3.4, -1.0, 0])
        long_ = wrapped_label(r"``it was my wife, \ and in situations of this kind it is permissible to save one's "
                              r"wife''", 4.6, 17, GREY_A).move_to([-3.4, -2.3, 0])
        cross = Cross(long_, stroke_color=HARM, stroke_width=3, scale_factor=0.9)
        short = label(r"``it was my wife''", font_size=20, color=VIRT).next_to(long_, DOWN, buff=0.25)
        side = stack([(r"Fried's case: \ the impartialist must justify saving his wife", GREY_A),
                      (r"Williams: \ the justification is one thought too many", VIRT),
                      (r"a good husband does not need a permission from the point of view of the universe", VIRT),
                      (r"Railton \ (1984): \ a sophisticated consequentialist need not think as one", GOOD),
                      (r"Wolf \ (1982): \ a moral saint would lack the loves that make a life worth living", HARM)],
                     font_size=18, aligned_edge=LEFT, width=5.2, buff=0.3).move_to([3.6, -0.3, 0])
        with self.voiceover(
            "Bernard Williams pressed the challenge of partiality in 1976, with a case of Charles Fried's. "
            "<bookmark mark='a'/>A man can save one of two people from drowning, and one of them is his wife. "
            "<bookmark mark='b'/>An impartial theory might permit him to save her, but it owes a justification: it "
            "was my wife, and in situations of this kind it is permissible to save one's wife. "
            "<bookmark mark='c'/>Williams said that is one thought too many. The right motive is simply that it was "
            "his wife; a husband who needs the theory's permission has already lost something. "
            "<bookmark mark='d'/>Peter Railton replied in 1984 that a sophisticated consequentialist need not think "
            "in consequentialist terms: the theory says which motives are good to have, and loving motives are among "
            "them, as Hare's two levels suggested. <bookmark mark='e'/>And Susan Wolf, in Moral Saints of 1982, "
            "argued that a person who aimed at maximal moral goodness would lack the attachments that make a life "
            "worth living: a point for care ethics, and a warning for any theory that asks to be the only thing an "
            "agent cares about."
        ) as vo:
            self.play(FadeIn(head), FadeIn(water))
            vo.wait_until("a")
            self.play(FadeIn(wife), FadeIn(stranger), FadeIn(man), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(long_))
            vo.wait_until("c")
            self.play(Create(cross), FadeIn(short), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
