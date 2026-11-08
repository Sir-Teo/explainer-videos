from __future__ import annotations

from videos.philosophy.philosophy21.common import *  # noqa: F403


class Intrinsics(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Temporary intrinsics", r"How can one thing be bent and straight?",
                            lit=(1986, 1987), part=PART)
        with self.voiceover("Chapter eight. Temporary intrinsics."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.problem()
        self.answers()
        self.price()

    def problem(self):
        hc = history_card(1986, r"David Lewis", r"\textit{On the Plurality of Worlds}, \ pp. 202--4", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)

        def figure(x, bent, col):
            g = VGroup(Circle(radius=0.22, color=col).move_to([x, 0.6, 0]))
            if bent:
                g.add(Line([x, 0.38, 0], [x, -0.4, 0], color=col), Line([x, -0.4, 0], [x + 0.6, -0.4, 0], color=col),
                      Line([x + 0.6, -0.4, 0], [x + 0.6, -1.1, 0], color=col),
                      Rectangle(width=1.0, height=0.12, color=GREY_B).move_to([x + 0.4, -0.5, 0]))
            else:
                g.add(Line([x, 0.38, 0], [x, -0.6, 0], color=col), Line([x, -0.6, 0], [x - 0.2, -1.4, 0], color=col),
                      Line([x, -0.6, 0], [x + 0.2, -1.4, 0], color=col))
            return g

        sit = figure(-5.0, True, NOM)
        stand = figure(-2.6, False, NOM)
        sl = label(r"sitting: \ bent", font_size=16, color=GREY_A).next_to(sit, DOWN, buff=0.2)
        stl = label(r"standing: \ straight", font_size=16, color=GREY_A).next_to(stand, DOWN, buff=0.2)
        rows = stack([(r"I am bent when sitting, \ straight when standing", WHITE),
                      (r"bent and straight are \textit{intrinsic}: \ about me alone, \ not my relations", GOAL),
                      (r"but nothing is both bent and straight", BAD),
                      (r"and if I endure, \ one and the same whole thing has both: \ a contradiction?", BAD)],
                     font_size=20, aligned_edge=LEFT, width=6.4).move_to([3.4, -0.3, 0])
        with self.voiceover(
            "David Lewis pressed a problem for endurance. <bookmark mark='a'/>When I sit, my shape is bent; when I "
            "stand, it is straight. <bookmark mark='b'/>Shapes are intrinsic properties: they concern how a thing is "
            "in itself, not how it is related to other things. <bookmark mark='c'/>But nothing can be both bent and "
            "straight. <bookmark mark='d'/>If I endure, the one whole thing that sits is the very thing that stands, "
            "and it has both shapes. How can that be?"
        ) as vo:
            self.play(FadeIn(hc), FadeIn(sit), FadeIn(stand), FadeIn(sl), FadeIn(stl))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def answers(self):
        head = label(r"Four answers", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"relations to times", r"bent-at-$t_1$, \ straight-at-$t_2$: \ but then shape is a relation, \ not "
                                    r"intrinsic", UNIV),
            (r"adverbialism", r"Johnston; \ Haslanger: \ I am bent $t_1$-ly; \ the time modifies the having", ABS),
            (r"presentism", r"only the present exists: \ I am straight, \ and was bent; \ no conflict", NOM),
            (r"perdurance", r"Lewis: \ one temporal part is bent, \ another straight, \ as one part of a road is wet",
             WHOLE),
            (r"the lesson", r"what persistence is depends on what time is \ (Part 24 and 25)", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.6, x_text=-2.4, label_size=21)
        with self.voiceover(
            "There are four main answers. <bookmark mark='a'/>Make shapes relations to times: bent-at-one-time and "
            "straight-at-another. But then shape is not intrinsic after all, which Lewis found unbelievable. "
            "<bookmark mark='b'/>Adverbialists, such as Mark Johnston and Sally Haslanger, let the time modify the "
            "having: I am bent in a sitting-time way. <bookmark mark='c'/>Presentists say only the present exists: I am "
            "straight, and I was bent, and there is no conflict between what is and what was. "
            "<bookmark mark='d'/>Lewis's own answer is perdurance: one temporal part of me is bent, another straight, "
            "just as one part of a road is wet and another dry. <bookmark mark='e'/>So what persistence is depends on "
            "what time is, the subject of Parts 24 and 25."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def price(self):
        d = load("intrinsics")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert d["mcs"] == [["I1"], ["I2"], ["I3"], ["I4"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.9, width=3.6, font_size=19,
                       center=[0, -0.5, 0], title=r"The Price List: \ temporary intrinsics")
        positions = [(("I1",), r"relationalism", r"shapes are relations to times: \ bent-at-$t_1$"),
                     (("I2",), r"Lewis", r"perdurance: \ different temporal parts have the different shapes"),
                     (("I3",), r"presentism", r"only one of them is true now: \ I am straight, \ and was bent"),
                     (("I4",), r"adverbialism", r"I have bent \textit{sitting-ly}: \ there is no having simpliciter")]
        with self.voiceover(
            "The four answers are the exits from one Price List. <bookmark mark='a'/>Shapes are intrinsic. I endure, "
            "wholly present when sitting and when standing. I am bent and I am straight. And nothing has both shapes "
            "simpliciter. <bookmark mark='b'/>The four cannot all hold. <bookmark mark='c'/>Relationalists give up "
            "the first. <bookmark mark='d'/>Lewis gives up the second, endurance. <bookmark mark='e'/>Presentists give "
            "up the third, as a timeless claim: only one shape is mine now. <bookmark mark='f'/>Adverbialists give up "
            "the fourth: there is no having a shape simpliciter, only having it in a temporal way."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cdef", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()
