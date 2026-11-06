from __future__ import annotations

from videos.philosophy.philosophy30.common import *  # noqa: F403


class Eliminate(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Eliminating the mind", r"What if there are no beliefs at all?", lit=(1981,),
                            part=PART)
        with self.voiceover("Chapter ten. Eliminating the mind."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.theory()
        self.replies()
        self.patterns()
        self.barcodes()

    def theory(self):
        hc = history_card(1981, r"Paul Churchland", r"`Eliminative Materialism and the Propositional Attitudes'",
                          width=7.6, color=HIST).to_corner(UL, buff=0.3)
        olds = [(r"phlogiston", r"oxygen"), (r"caloric fluid", r"molecular motion"), (r"vital spirit", r"biochemistry"),
                (r"beliefs and desires?", r"neuroscience")]
        rows = VGroup()
        for i, (a, b) in enumerate(olds):
            y = 1.0 - 0.7 * i
            col = MIND if i == 3 else GREY_A
            rows.add(VGroup(label(a, font_size=22, color=col).move_to([-2.6, y, 0]),
                            MathTex(r"\longrightarrow", font_size=30, color=col).move_to([0, y, 0]),
                            label(b, font_size=22, color=PHYS if i == 3 else GREY_A).move_to([2.8, y, 0])))
        foot = stack([(r"folk psychology is a theory: \ stagnant for two millennia, \ silent on sleep, \ learning and "
                       r"mental illness", BAD),
                      (r"if neuroscience does not vindicate it, \ its entities go the way of phlogiston", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=12.0, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Paul and Patricia Churchland proposed something more radical than any reduction. "
            "<bookmark mark='a'/>Science has often found that the things a theory talked about do not exist. "
            "Phlogiston gave way to oxygen, caloric fluid to molecular motion, vital spirit to biochemistry. Nobody "
            "reduced phlogiston to oxygen; phlogiston was eliminated. <bookmark mark='b'/>Paul Churchland argued in "
            "1981 that beliefs and desires may go the same way. <bookmark mark='c'/>Folk psychology, our everyday "
            "practice of explaining behaviour by beliefs and desires, is a theory, and not a good one: it has hardly "
            "changed in two thousand years, and it says nothing about sleep, learning or mental illness. "
            "<bookmark mark='d'/>If neuroscience does not vindicate it, its entities should be eliminated."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:3]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def replies(self):
        head = label(r"Replies", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"self-refutation", r"the eliminativist \textit{believes} there are no beliefs, \ and wants us to agree \ "
                                 r"(Baker, \ 1987)", BAD),
            (r"the reply", r"that begs the question: \ the theory would be stated in better terms, \ once we have them",
             MIND),
            (r"success", r"folk psychology predicts behaviour astonishingly well: \ who will be at the station at "
                         r"noon tomorrow", OK),
            (r"Fodor", r"the theory is vindicated: \ beliefs are sentences in the language of thought \ (chapter 12)",
             SYM),
        ]
        g = rows_table(rows, top=1.6, gap=0.55)
        with self.voiceover(
            "There were sharp replies. <bookmark mark='a'/>Lynne Rudder Baker argued that eliminativism refutes "
            "itself: the eliminativist believes there are no beliefs, and argues in order that we come to believe it "
            "too. <bookmark mark='b'/>The Churchlands answered that this begs the question: it assumes the old theory "
            "in order to criticize the new, which would be stated in better terms once we have them. "
            "<bookmark mark='c'/>A stronger reply is folk psychology's success. Knowing only that a friend wants to "
            "meet you and believes you will be at the station at noon, you can predict where she will be tomorrow, "
            "something no neuroscience can yet do. <bookmark mark='d'/>And Jerry Fodor held that the theory would be "
            "vindicated: beliefs are real, as sentences in a language of thought."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def patterns(self):
        head = label(r"Real patterns \ (Dennett)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"three stances", r"physical, \ design, \ intentional: \ predict by physics, \ by function, \ or by "
                               r"beliefs and desires", FUNC),
            (r"\textit{The Intentional Stance} \ (1987)", r"a system has beliefs if the intentional stance predicts it "
                                                          r"well", MIND),
            (r"`Real Patterns' \ (1991)", r"like gliders in Life: \ real because they let us compress and predict, \ "
                                          r"though nothing but cells exists", SYM),
            (r"the middle way", r"neither eliminated nor reduced: \ beliefs are real patterns in behaviour", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55)
        with self.voiceover(
            "Daniel Dennett took a middle way. <bookmark mark='a'/>We can predict a system from three stances: the "
            "physical stance, from its physics; the design stance, from what it is for; and the intentional stance, "
            "by treating it as a rational agent with beliefs and desires. <bookmark mark='b'/>A system has beliefs, he "
            "argued, if the intentional stance predicts it well. <bookmark mark='c'/>In a paper of 1991, Real "
            "Patterns, his example was the Game of Life from the last chapter. Gliders are real, though nothing "
            "exists but cells: talking about gliders lets us compress the history of the grid and predict it. "
            "<bookmark mark='d'/>Beliefs, likewise, are real patterns in behaviour: neither eliminated nor reduced."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def barcodes(self):
        d = load("patterns")
        F = d["frames"]
        head = label(r"Real patterns, \ measured", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert [f["noise"] for f in F] == [0.0, 0.01, 0.05, 0.1, 0.25, 0.5] and F[0]["bitmap_bits"] == 900
        assert [f["ratio_two_part"] for f in F] == [0.033, 0.072, 0.306, 0.479, 0.849, 1.025]
        assert [f["ratio_lzma"] for f in F][-1] == 1.003
        on, off = np.array([242, 193, 78, 255], dtype=np.uint8), np.array([34, 38, 46, 255], dtype=np.uint8)
        frames, bars, vals, nl = Group(), VGroup(), VGroup(), VGroup()
        top, step = 2.35, 0.84
        x0, scale = 0.9, 4.2
        for k, f in enumerate(F):
            arr = np.array(f["frame"], dtype=np.uint8)
            rgba = np.where(arr[..., None] == 1, on, off).astype(np.uint8)
            rgba = np.kron(rgba, np.ones((12, 12, 1), dtype=np.uint8))
            img = ImageMobject(rgba)
            img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
            img.width = 5.4
            y = top - step * k
            img.move_to([-2.9, y, 0])
            frames.add(img)
            nl.add(label(f"{round(100 * f['noise'])}\\%", font_size=19, color=GREY_A).move_to([-6.1, y, 0]))
            w = max(scale * f["ratio_two_part"], 0.02)
            bars.add(Rectangle(width=w, height=0.34, fill_color=OK if f["ratio_two_part"] < 1 else BAD,
                               fill_opacity=0.8, stroke_width=0).move_to([x0 + w / 2, y, 0]))
            vals.add(label(f"{f['ratio_two_part']:.3f}", font_size=18, color=GREY_A).next_to(bars[-1], RIGHT,
                                                                                               buff=0.12))
        one = DashedLine([x0 + scale, top + 0.45, 0], [x0 + scale, top - step * 5 - 0.4, 0], color=GREY_B)
        ol = label(r"the bit map", font_size=16, color=GREY_B).next_to(one, DOWN, buff=0.08)
        bl = label(r"pattern $+$ exceptions, \ as a share of the bit map", font_size=16, color=GREY_A).move_to(
            [x0 + 2.0, top + 0.5, 0])
        fl = label(r"noise", font_size=16, color=GREY_A).move_to([-6.1, top + 0.5, 0])
        foot = label(r"a compressor agrees: \ at 50\% noise it saves nothing either \ (1.003)", font_size=19,
                     color=GOAL).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Dennett's argument can be measured. <bookmark mark='a'/>His paper's figure was a set of frames of dots, "
            "each a bar code, ten black dots and ten white, repeated, with some of the dots flipped at random. The "
            "Reasoner draws six such frames of nine hundred dots, with noise from none to one half. "
            "<bookmark mark='b'/>Is the bar code really there? Dennett's test: a pattern is real if describing the "
            "frame by the pattern, plus a list of its exceptions, is shorter than giving every dot. "
            "<bookmark mark='c'/>With no noise, the pattern and its phase take three percent of the bit map. At one "
            "percent noise, seven percent. At five, thirty one percent. At ten percent noise, forty eight; at a "
            "quarter, eighty five. The pattern is there at every one of these levels, ever more faintly. "
            "<bookmark mark='d'/>At one half, describing the frame by the bar code costs more than the bit map: "
            "there is no pattern to find. An off-the-shelf compressor, run on long stretches of each, agrees. "
            "<bookmark mark='e'/>And the pattern pays off in prediction too: betting on the bar code wins ninety "
            "percent of the time at ten percent noise. That, for Dennett, is all it takes for beliefs to be real: "
            "a pattern in behaviour that predicts better than the alternatives, though the noise never goes away."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(fl), LaggedStart(*[FadeIn(x) for x in frames], lag_ratio=0.25),
                      LaggedStart(*[FadeIn(x) for x in nl], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(Create(one), FadeIn(ol), FadeIn(bl))
            vo.wait_until("c")
            for k in range(5):
                self.play(GrowFromEdge(bars[k], LEFT), FadeIn(vals[k]), run_time=0.7)
            vo.wait_until("d")
            self.play(GrowFromEdge(bars[5], LEFT), FadeIn(vals[5]))
            self.play(FadeIn(foot))
            vo.wait_until("e")
            self.play(Indicate(frames[3], color=OK, scale_factor=1.03))
        self.clear_scene()
