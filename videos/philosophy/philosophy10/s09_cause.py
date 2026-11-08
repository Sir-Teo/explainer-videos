from __future__ import annotations

from videos.philosophy.philosophy10.common import *  # noqa: F403


class Cause(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Custom, \ the great guide", r"What do we see when we see one thing cause another?",
                            lit=(1748,), part=PART)
        with self.voiceover("Chapter eight. Custom, the great guide."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.billiards()
        self.definitions()
        self.induction()
        self.self_()
        self.reid()

    def billiards(self):
        head = label(r"One billiard ball strikes another", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        table = Rectangle(width=8, height=1.4, stroke_color=GREY_C, stroke_width=2, fill_color="#123322",
                          fill_opacity=0.6).move_to([0, 1.0, 0])
        a = Circle(radius=0.25, color=WHITE, fill_color=WHITE, fill_opacity=1).move_to([-3.4, 1.0, 0])
        b = Circle(radius=0.25, color=BAD, fill_color=BAD, fill_opacity=1).move_to([0.2, 1.0, 0])
        seen = VGroup(label(r"what we see: \ contiguity, \ succession, \ and, \ over many cases, \ constant "
                            r"conjunction", font_size=24, color=SENSE),
                      label(r"what we never see: \ the \textit{necessary connection}, \ the power", font_size=24,
                            color=BAD),
                      label(r"its source: \ habit; \ after many repetitions the mind is carried from one to the other",
                            font_size=24, color=GOAL),
                      label(r"necessity is in the mind, \ not in the balls \ (Part 17 returns to this)", font_size=22,
                            color=GREY_A)).arrange(DOWN, buff=0.3).move_to([0, -1.5, 0])
        with self.voiceover(
            "Hume's most famous analysis is of cause and effect. <bookmark mark='a'/>One billiard ball rolls into "
            "another, and the second moves off. <bookmark mark='b'/>What do we actually see? The balls touch; the "
            "first moves before the second; and in case after case, such a collision is followed by such a motion. "
            "<bookmark mark='c'/>What we never see is the necessary connection between them, the power by which the "
            "first makes the second move. Examine the impressions as closely as you like; it is not there. "
            "<bookmark mark='d'/>Where, then, does the idea come from? From habit. After many repetitions, the mind is "
            "carried by custom from the sight of one to the expectation of the other, and we project that feeling of "
            "being carried onto the world. <bookmark mark='e'/>Necessity is in the mind, not in the balls. Part 17, "
            "on causation, picks up the thread."
        ) as vo:
            self.play(FadeIn(head), FadeIn(table), FadeIn(a), FadeIn(b))
            vo.wait_until("a")
            self.play(a.animate.move_to([-0.3, 1.0, 0]), run_time=1.2, rate_func=linear)
            self.play(b.animate.move_to([3.4, 1.0, 0]), a.animate.shift(RIGHT * 0.2), run_time=1.2)
            for mk, r in zip("bcde", seen):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def definitions(self):
        head = label(r"Hume's two definitions of cause", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        rows = VGroup(
            label(r"1. \ an object followed by another, \ where all objects similar to the first \ are followed by "
                  r"objects similar to the second", font_size=22, color=SENSE),
            label(r"the regularity view: \ causation is constant conjunction", font_size=22, color=GREY_A),
            label(r"2. \ `or, in other words, \ where, if the first object had not been, \ the second never had "
                  r"existed'", font_size=22, color=REASON),
            label(r"the counterfactual view: \ David Lewis (1973), \ Part 17", font_size=22, color=GREY_A),
            label(r"Hume thought these were one definition; \ they are not: \ two traditions, \ from one sentence",
                  font_size=24, color=GOAL)).arrange(DOWN, buff=0.28).move_to([0, -0.4, 0])
        for r in rows:
            if r.width > 13.0:
                r.width = 13.0
        with self.voiceover(
            "In the Enquiry, Hume defines a cause in a single sentence that contains two definitions. "
            "<bookmark mark='a'/>First: an object, followed by another, where all the objects similar to the first "
            "are followed by objects similar to the second. <bookmark mark='b'/>That is the regularity view: causation "
            "is nothing but constant conjunction. <bookmark mark='c'/>Then: or in other words, where, if the first "
            "object had not been, the second never had existed. <bookmark mark='d'/>That is a counterfactual, and it "
            "became David Lewis's theory of causation in 1973, which Part 17 builds. <bookmark mark='e'/>Hume thought "
            "he had said the same thing twice. He had not. Two traditions in the philosophy of causation grow from "
            "this one sentence."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def induction(self):
        d = load("induction")
        head = label(r"The problem of induction", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        suns = VGroup(*[VGroup(Circle(radius=0.22, color=GOAL, fill_color=GOAL, fill_opacity=0.8),
                               label(str(i + 1), font_size=18, color=GREY_B)) for i in range(8)])
        for s_ in suns:
            s_[1].next_to(s_[0], DOWN, buff=0.1)
        suns.arrange(RIGHT, buff=0.3).move_to([-3.5, 2.0, 0])
        tomorrow = VGroup(Circle(radius=0.22, color=GREY_B, stroke_width=2).set_fill(opacity=0),
                          label(r"9", font_size=18, color=GREY_B))
        tomorrow[1].next_to(tomorrow[0], DOWN, buff=0.1)
        tomorrow.next_to(suns, RIGHT, buff=0.35)
        qm = label(r"?", font_size=30, color=GOAL).move_to(tomorrow[0])
        hd = [label(r"rule", font_size=22, color=P.CLAIM), label(r"fits days 1--8?", font_size=22, color=P.CLAIM),
              label(r"day 9", font_size=22, color=P.CLAIM)]
        names = {"always": r"always a sunrise", "until day 8": r"sunrise until day 8, \ then none",
                 "until day 10": r"sunrise until day 10, \ then none",
                 "on even days after": r"after day 8, \ every other day"}
        rows = [[label(names[r["rule"]], font_size=21), r["fits"],
                 label(r"sunrise" if r["tomorrow"] else r"no sunrise", font_size=21,
                       color=OK if r["tomorrow"] else BAD)] for r in d["rules"]]
        grid = ValueGrid(hd, rows, col_w=[3.7, 1.9, 1.6], cell_h=0.48, font_size=21).move_to([-3.2, -0.3, 0])
        arg = VGroup(label(r"to infer day 9, \ assume the future resembles the past", font_size=22),
                     label(r"that assumption is no relation of ideas: \ its denial is conceivable", font_size=21,
                           color=GREY_A),
                     label(r"nor a matter of fact we could learn: \ learning it would assume it", font_size=21,
                           color=GREY_A),
                     label(r"so induction has no foundation in reason", font_size=23, color=BAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.22)
        for x in arg:
            if x.width > 5.4:
                x.width = 5.4
        arg.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.05, -0.6, 0])
        assert all(r["fits"] for r in d["rules"])
        with self.voiceover(
            "Habit explains our expectations. It does not justify them. <bookmark mark='a'/>The sun has risen on "
            "every day we have observed. Will it rise tomorrow? <bookmark mark='b'/>The Reasoner writes down four "
            "rules. Always a sunrise; a sunrise until day eight, and then none; a sunrise until day ten; or a "
            "sunrise until day eight and then every other day. Every one fits all eight observations perfectly, and they disagree "
            "about tomorrow. <bookmark mark='c'/>To choose the first, we must assume that the future will resemble "
            "the past. Is that a relation of ideas? No: its denial is perfectly conceivable. Is it a matter of fact, "
            "learned from experience? Only by an argument that already assumes it. <bookmark mark='d'/>So, Hume "
            "concluded, our inferences from experience have no foundation in reason. They rest on custom, which he "
            "called the great guide of human life. Part 15 is devoted to this problem."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in suns], lag_ratio=0.15), FadeIn(tomorrow), FadeIn(qm),
                      run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(len(rows))], lag_ratio=0.5),
                      run_time=5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(x) for x in arg[:3]], lag_ratio=0.6), run_time=4)
            vo.wait_until("d")
            self.play(FadeIn(arg[3]))
        self.clear_scene()

    def self_(self):
        q = quote_card(r"I never can catch myself at any time without a perception, and never can observe any thing but "
                       r"the perception.", r"David Hume", r"\textit{Treatise} I.iv.6", width=9.6,
                       font_size=28).move_to([0, 1.2, 0])
        rows = VGroup(label(r"look inward for the self: \ you find a heat, \ a sound, \ a feeling, \ never a "
                            r"`self'", font_size=24),
                      label(r"the self is a bundle of perceptions, \ in perpetual flux", font_size=26, color=GOAL),
                      label(r"Descartes's first certainty, \ and the bundle that replaced it: \ Part 21", font_size=22,
                            color=GREY_A)).arrange(DOWN, buff=0.3).move_to([0, -1.5, 0])
        with self.voiceover(
            "Hume turned the same test on the self. <bookmark mark='a'/>When I enter most intimately into what I "
            "call myself, he wrote, I always stumble on some particular perception or other, of heat or cold, light "
            "or shade, love or hatred. I never can catch myself at any time without a perception, and never can "
            "observe any thing but the perception. <bookmark mark='b'/>So the self is nothing but a bundle of "
            "perceptions, in perpetual flux. <bookmark mark='c'/>Descartes's first certainty has become a bundle. "
            "Part 21, on personal identity, takes it up."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def reid(self):
        hc = history_card(1764, r"Thomas Reid", r"\textit{An Inquiry into the Human Mind on the Principles of Common "
                          r"Sense}", width=6.0, color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup(
            label(r"Hume's premise: \ we perceive only ideas, \ never things", font_size=24, color=SENSE),
            label(r"Reid: \ that `way of ideas' is the mistake; \ we perceive the things themselves", font_size=24,
                  color=GOAL),
            label(r"some principles are first principles of common sense: \ trust them until shown otherwise",
                  font_size=24),
            label(r"the same faculty that tells us of ideas \ tells us of the world: \ why trust one and not the "
                  r"other?", font_size=22, color=GREY_A),
            label(r"his heirs: \ Moore's `here is one hand' \ (Part 11)", font_size=22, color=OK)).arrange(
            DOWN, buff=0.32).move_to([0, -0.5, 0])
        with self.voiceover(
            "Hume's fellow Scot Thomas Reid answered him in 1764. <bookmark mark='a'/>Hume's skepticism, Reid argued, "
            "followed from a premise shared since Descartes: that what we perceive directly is only ideas in the "
            "mind, never the things themselves. <bookmark mark='b'/>That way of ideas is the mistake. We perceive "
            "things, not pictures of things. <bookmark mark='c'/>And some principles, such as that the things we "
            "perceive exist, are first principles of common sense, to be trusted until shown otherwise. "
            "<bookmark mark='d'/>The same faculty that tells us of our ideas tells us of the world, Reid said; why "
            "trust the one and not the other? <bookmark mark='e'/>His heirs include G. E. Moore, who held up his hand "
            "to refute the skeptic, as Part 11 will show."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
