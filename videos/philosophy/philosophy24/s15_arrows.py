from __future__ import annotations

from videos.philosophy.philosophy24.common import *  # noqa: F403


class Arrows(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"Many arrows, \ one?", r"Are all of time's arrows the arrow of entropy?",
                            lit=(1909, 1956), part=PART)
        with self.voiceover("Chapter fourteen. Many arrows, or one?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.pond()
        self.catalogue()
        self.traces()
        self.verdicts()

    def pond(self):
        hc = history_card(1956, r"Karl Popper", r"`The Arrow of Time', \ \textit{Nature}", width=5.0,
                          color=HIST).to_corner(UL, buff=0.3)
        c = np.array([-3.0, -0.6, 0])
        rim = Circle(radius=2.6, color=GREY_D, stroke_width=2).move_to(c)
        stone = Dot(c, radius=0.1, color=WHITE)
        t = ValueTracker(0.0)

        def waves(sign):
            def make():
                g = VGroup()
                for k in range(4):
                    ph = (t.get_value() - 0.55 * k)
                    if ph <= 0 or ph >= 1:
                        continue
                    r = 2.5 * min(ph, 1.0) if sign > 0 else 2.5 * (1 - min(ph, 1.0))
                    if r <= 0.02:
                        continue
                    g.add(Circle(radius=r, color=LAW if sign > 0 else BAD, stroke_width=3,
                                 stroke_opacity=0.9 * (1 - 0.15 * k)).move_to(c))
                return g
            return make

        out = always_redraw(waves(+1))
        side = stack([(r"drop a stone: \ circular waves spread outward", LAW),
                      (r"the wave equation equally allows waves converging on the centre", BAD),
                      (r"but they would need coordinated disturbances all around the rim", ABS),
                      (r"Ritz and Einstein argued in 1909: \ is the radiative arrow a law, \ or statistics?", HIST)],
                     font_size=20, aligned_edge=LEFT, width=5.0).move_to([3.9, -0.5, 0])
        with self.voiceover(
            "Entropy is not the only arrow. <bookmark mark='a'/>Drop a stone in a pond, and circular waves spread "
            "outward from it. <bookmark mark='b'/>The wave equation is time-symmetric: it equally allows waves that "
            "converge from the edge of the pond onto a point, and lift a stone out of the water. We never see them. "
            "<bookmark mark='c'/>Karl Popper pointed out in 1956 that converging waves would need disturbances all "
            "around the rim, perfectly coordinated. <bookmark mark='d'/>In 1909 Walther Ritz and Albert Einstein "
            "argued over this radiative arrow. Ritz thought it was a fundamental law, and the source of the "
            "thermodynamic arrow. Einstein thought it was a matter of probability, like the second law."
        ) as vo:
            self.play(FadeIn(hc), Create(rim), FadeIn(stone))
            vo.wait_until("a")
            self.add(out)
            self.play(t.animate.set_value(2.8), FadeIn(side[0]), run_time=3, rate_func=linear)
            out.clear_updaters()
            self.remove(out)
            vo.wait_until("b")
            t.set_value(0.0)
            inn = always_redraw(waves(-1))
            self.add(inn)
            self.play(t.animate.set_value(2.8), FadeIn(side[1]), run_time=3, rate_func=linear)
            inn.clear_updaters()
            self.remove(inn)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Indicate(rim, color=BAD))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def catalogue(self):
        head = label(r"The arrows of time", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"thermodynamic", r"entropy rises", ENT),
            (r"radiative", r"waves spread out from sources, \ never converge on sinks", LAW),
            (r"causal", r"causes come before their effects; \ Reichenbach's common causes lie in the past \ (Part "
                        r"17)", CHANCE),
            (r"counterfactual", r"the future depends on what we do now; \ the past does not", ABS),
            (r"epistemic", r"we have records of the past, \ none of the future", DATA),
            (r"psychological", r"we remember the past and anticipate the future", TIME),
            (r"cosmological", r"the universe expands", GREY_A),
        ]
        g = rows_table(rows, top=1.9, gap=0.36, width=8.6, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "List the arrows. <bookmark mark='a'/>Thermodynamic: entropy rises. <bookmark mark='b'/>Radiative: "
            "waves spread out from their sources. <bookmark mark='c'/>Causal: causes come before their effects; "
            "and, as Part 17 found with Reichenbach, correlated events trace back to common causes in their past, "
            "not to common effects in their future. <bookmark mark='d'/>Counterfactual: what happens tomorrow "
            "depends on what we do today, but yesterday does not. <bookmark mark='e'/>Epistemic: we have records "
            "of the past, and none of the future. <bookmark mark='f'/>Psychological: we remember the past, and "
            "only anticipate the future. <bookmark mark='g'/>And cosmological: the universe expands. Are these "
            "seven arrows, or one arrow seen seven ways?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdefg", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def traces(self):
        head = label(r"The asymmetry of traces", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        tl = Arrow([-6.2, -2.6, 0], [6.2, -2.6, 0], color=TIME, buff=0, stroke_width=3)
        tlab = label(r"time", font_size=18, color=TIME).next_to(tl, DOWN, buff=0.1).shift(RIGHT * 5.4)
        ev = Dot([-3.6, 0.0, 0], radius=0.16, color=BAD)
        evl = label(r"a window breaks", font_size=19, color=BAD).next_to(ev, DOWN, buff=0.2)
        rng = np.random.default_rng(1979)
        traces = VGroup()
        for _ in range(16):
            end = np.array([rng.uniform(0.0, 2.6), rng.uniform(-1.9, 1.9), 0])
            traces.add(Line(ev.get_center(), end, color=BAD, stroke_width=1.5, stroke_opacity=0.7))
        tdots = VGroup(*[Dot(l.get_end(), radius=0.05, color=BAD) for l in traces])
        now = DashedLine([1.6, -2.4, 0], [1.6, 2.0, 0], color=GOAL)
        nl = label(r"now", font_size=18, color=GOAL).next_to(now, UP, buff=0.05)
        names = label(r"shards, \ sound waves, \ memories, \ photographs", font_size=17, color=GREY_A).move_to(
            [0.6, 2.4, 0])
        fut = Dot([4.6, 0.6, 0], radius=0.16, color=LAW)
        futl = label(r"a future event: \ hardly any traces now", font_size=18, color=LAW).next_to(fut, DOWN,
                                                                                               buff=0.2)
        side = stack([(r"Lewis \ (1979): \ the past is overdetermined by its many traces", ABS),
                      (r"so the past is fixed by the present many times over; \ the future is not", OK),
                      (r"Albert: \ records are reliable only given the Past Hypothesis", TIME)], font_size=20,
                     aligned_edge=LEFT, width=4.4).move_to([4.6, -1.5, 0])
        with self.voiceover(
            "Why does the future depend on us and the past not? David Lewis, in 1979, located the answer in an "
            "asymmetry of traces. <bookmark mark='a'/>A window breaks. <bookmark mark='b'/>Afterwards the world "
            "fills with traces of the event: shards of glass, sound waves spreading, memories, a photograph. Each "
            "one alone is enough to tell that the window broke. <bookmark mark='c'/>The past is overdetermined by "
            "the present, many times over, so no small change now could have made it different. "
            "<bookmark mark='d'/>A future event leaves almost no traces in the present, so small changes now make "
            "a difference to it. <bookmark mark='e'/>And Albert argues that the asymmetry of traces is itself "
            "statistical: traces are reliable records only given the Past Hypothesis, just as the ice cube was."
        ) as vo:
            self.play(FadeIn(head), GrowArrow(tl), FadeIn(tlab))
            vo.wait_until("a")
            self.play(FadeIn(ev, scale=0.5), FadeIn(evl))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l) for l in traces], lag_ratio=0.08), FadeIn(tdots), FadeIn(names),
                      run_time=2.5)
            vo.wait_until("c")
            self.play(Create(now), FadeIn(nl), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(fut), FadeIn(futl))
            vo.wait_until("e")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def verdicts(self):
        head = label(r"One arrow, \ or a direction in time itself?", font_size=30, color=CONN).to_edge(UP,
                                                                                                    buff=0.35)
        rows = [
            (r"reduction", r"Albert and Loewer: \ every arrow comes from the Past Hypothesis, \ the statistical "
                           r"postulate and the dynamics", OK),
            (r"time's own direction", r"Maudlin: \ time passes, \ and its direction is fundamental; \ the laws "
                                      r"produce the future from the past", TIME),
            (r"the view from nowhen", r"Price \ (1996): \ the arrow is in us and our boundary conditions, \ not in "
                                      r"time; \ look at physics without it", ABS),
            (r"next", r"Part 25: \ relativity, \ the block universe, \ and whether time passes at all", GOAL),
        ]
        g = rows_table(rows, top=1.7, gap=0.5, width=8.4, x_text=-2.4, label_size=22, text_size=21)
        with self.voiceover(
            "There are three verdicts. <bookmark mark='a'/>The reductionists, Albert and Loewer: every arrow, "
            "causal, counterfactual, epistemic and psychological, comes from the Past Hypothesis together with the "
            "statistical postulate and time-symmetric dynamics. One arrow, the thermodynamic, explains the rest. "
            "<bookmark mark='b'/>Tim Maudlin dissents: time passes, its direction is a fundamental fact, and the "
            "laws are what produce each moment from the one before. <bookmark mark='c'/>Huw Price takes the "
            "opposite line: the arrow is in us, and in the boundary conditions, not in time itself, and physics "
            "should be done from a view from nowhen. <bookmark mark='d'/>Whether time passes at all is the question "
            "of Part 25, where relativity takes away the universal now."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
