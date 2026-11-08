from __future__ import annotations

from videos.philosophy.philosophy17.common import *  # noqa: F403


class Hume(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Constant conjunction", r"What do we see when we see a cause?",
                            lit=(1095, 1748), part=PART)
        with self.voiceover("Chapter one. Constant conjunction."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.billiards()
        self.ghazali()
        self.regularity()

    def billiards(self):
        hc = history_card(1748, r"David Hume", r"\textit{Enquiry}, \ \S 7: \ `Of the Idea of Necessary Connexion'",
                          width=7.0, color=HIST).to_corner(UL, buff=0.35)
        table = RoundedRectangle(width=8.0, height=1.6, corner_radius=0.2, stroke_color=GREY_D, fill_color="#0F3A2A",
                                 fill_opacity=0.6).move_to([0, 0.6, 0])
        a = Circle(radius=0.22, color=WHITE, fill_color=WHITE, fill_opacity=1).move_to([-3.4, 0.6, 0])
        b = Circle(radius=0.22, color=CAUSE, fill_color=CAUSE, fill_opacity=1).move_to([0, 0.6, 0])
        seen = stack([(r"we see: \ one motion, \ contact, \ another motion", WHITE),
                      (r"we never see the `power' or `necessary connexion'", BAD)], font_size=22).next_to(
            table, DOWN, buff=0.3)
        q = stack([(r"`an object, followed by another, \ and where all the objects similar to the first are followed by "
                    r"objects similar to the second.", CAUSE),
                   (r"Or in other words where, \ if the first object had not been, \ the second never had existed.'",
                    EFFECT)], font_size=20, width=12.0).to_edge(DOWN, buff=0.35)
        ql = VGroup(label(r"regularity", font_size=18, color=CAUSE).next_to(q[0], UP, buff=0.05).align_to(q[0], LEFT),
                    label(r"counterfactual", font_size=18, color=EFFECT).next_to(q[1], DOWN, buff=0.05).align_to(
                        q[1], LEFT))
        with self.voiceover(
            "Hume's example is a game of billiards. <bookmark mark='a'/>One ball rolls toward another, they touch, and "
            "the second moves off. <bookmark mark='b'/>What do we actually see? One motion, contact, another motion. "
            "We never see the power by which the first ball moves the second. <bookmark mark='c'/>So Hume defined a "
            "cause as an object followed by another, where all objects like the first are followed by objects like "
            "the second: constant conjunction. <bookmark mark='d'/>And then, in the same sentence, he added: or in "
            "other words, where if the first object had not been, the second never had existed. Two definitions, "
            "one of regularity and one of counterfactual dependence, offered as if they were the same. Most of this "
            "part is about why they are not."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(table), FadeIn(a), FadeIn(b))
            vo.wait_until("a")
            self.play(a.animate.move_to([-0.44, 0.6, 0]), run_time=1.2, rate_func=linear)
            self.play(b.animate.move_to([3.4, 0.6, 0]), a.animate.shift(RIGHT * 0.3), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(seen))
            vo.wait_until("c")
            self.play(FadeIn(q[0]), FadeIn(ql[0]))
            vo.wait_until("d")
            self.play(FadeIn(q[1]), FadeIn(ql[1]))
        self.clear_scene()

    def ghazali(self):
        hc = history_card(1095, r"al-Ghazālī", r"\textit{The Incoherence of the Philosophers}, \ Discussion 17",
                          width=7.0, color=HIST).to_corner(UL, buff=0.35)
        rows = [
            (r"the cotton and the fire", r"we observe the burning \textit{with} the contact, \ never \textit{by} it",
             CAUSE),
            (r"occasionalism", r"God creates the burning on each occasion; \ the order is habit, \ not necessity", HIDDEN),
            (r"Averroes \ (1180)", r"deny causes and you deny knowledge: \ `whoever denies causes denies reason'", OK),
            (r"Hume, \ 650 years on", r"the same observation, \ without the theology: \ custom, \ not connexion", GOAL),
        ]
        g = rows_table(rows, top=1.3, gap=0.55, width=8.2, x_text=-2.2)
        with self.voiceover(
            "The argument is older than Hume. <bookmark mark='a'/>Abu Hamid al-Ghazālī, in the eleventh century, "
            "considered cotton touched by fire. We observe that the cotton burns together with the contact, he said, "
            "but never that it burns by it. <bookmark mark='b'/>His conclusion was occasionalism: God creates the "
            "burning on each occasion, and the order we observe is habit, not necessity. "
            "<bookmark mark='c'/>Averroes replied, in The Incoherence of the Incoherence, that whoever denies causes "
            "denies reason itself, since knowledge is knowledge of things through their causes. "
            "<bookmark mark='d'/>Hume made al-Ghazālī's observation six and a half centuries later, without the "
            "theology: what we call necessity is custom."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def regularity(self):
        head = label(r"Regularity is not enough", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        g1 = CausalGraph({"day": [-4.6, 0.8, 0], "night": [-2.2, 0.8, 0], "Earth": [-3.4, 2.2, 0]},
                         [("Earth", "day"), ("Earth", "night")], radius=0.52, font_size=15)
        g2 = CausalGraph({"barometer": [1.4, 0.8, 0], "storm": [4.2, 0.8, 0], "pressure": [2.8, 2.2, 0]},
                         [("pressure", "barometer"), ("pressure", "storm")], radius=0.58, font_size=15)
        l1 = label(r"night always follows day \ (Reid)", font_size=20, color=WHITE).next_to(g1, DOWN, buff=0.3)
        l2 = label(r"the falling barometer precedes the storm", font_size=20, color=WHITE).next_to(g2, DOWN, buff=0.3)
        rows = stack([(r"common causes make regularities without causation", BAD),
                      (r"regularities have no direction: \ which end is the cause?", BAD),
                      (r"Kant: \ cause is a category the mind brings to experience", GREY_A),
                      (r"the twentieth-century answer: \ counterfactuals, \ probabilities, \ interventions", GOAL)],
                     font_size=22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The regularity view faces famous counterexamples. <bookmark mark='a'/>Thomas Reid observed that night "
            "has always followed day, yet day does not cause night; both are produced by the turning Earth. "
            "<bookmark mark='b'/>A falling barometer regularly precedes a storm, but smashing the barometer will not "
            "stop the storm; falling air pressure causes both. <bookmark mark='c'/>Common causes manufacture "
            "regularities without causation. <bookmark mark='d'/>And regularities have no direction: they cannot say "
            "which end is the cause. <bookmark mark='e'/>Kant concluded that causation is a category the mind "
            "brings to experience. <bookmark mark='f'/>The twentieth century tried three replacements: "
            "counterfactuals, probabilities, and interventions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g1), FadeIn(l1))
            vo.wait_until("b")
            self.play(FadeIn(g2), FadeIn(l2))
            for mk, r in zip("cdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
