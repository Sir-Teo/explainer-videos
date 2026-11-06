from __future__ import annotations

from videos.philosophy.philosophy31.common import *  # noqa: F403


class Higher(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Higher-order theories", r"Is a state conscious when we are aware of being in it?",
                            lit=(1986,), part=PART)
        with self.voiceover("Chapter nine. Higher-order theories."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.hot()
        self.blindsight()
        self.monitor()
        self.roc()

    def hot(self):
        hc = history_card(1986, r"David Rosenthal", r"`Two Concepts of Consciousness'", width=5.6,
                          color=HIST).to_corner(UL, buff=0.3)
        first = VGroup(RoundedRectangle(width=3.6, height=1.0, corner_radius=0.2, color=SIG, fill_opacity=0.1),
                       label(r"seeing red \ (first order)", font_size=20, color=SIG)).move_to([-2.2, -1.2, 0])
        second = VGroup(RoundedRectangle(width=3.6, height=1.0, corner_radius=0.2, color=SELF, fill_opacity=0.1),
                        label(r"`I am seeing red' \ (higher order)", font_size=20, color=SELF)).move_to([-2.2, 1.0, 0])
        arr = Arrow(second.get_bottom(), first.get_top(), buff=0.1, color=SELF)
        rows = stack([(r"a mental state is conscious when one is aware of being in it", SELF),
                      (r"by a suitable thought about it \ (Rosenthal) \ or perception of it \ (Armstrong, \ Lycan)",
                       GREY_A),
                      (r"explains unconscious perception: \ the first-order state without the second", OK),
                      (r"Block: \ what if the higher-order state is empty, \ about a red that is not there?", BAD)],
                     font_size=19, aligned_edge=LEFT, width=6.6, buff=0.3).move_to([3.4, -0.1, 0])
        with self.voiceover(
            "Higher-order theories start from a different thought. <bookmark mark='a'/>A mental state is conscious, "
            "David Rosenthal argued, when one is aware of being in it. Seeing red becomes a conscious seeing when it "
            "is accompanied by a suitable higher-order thought: I am seeing red. <bookmark mark='b'/>For Rosenthal "
            "the awareness is a thought; for David Armstrong and William Lycan, a kind of inner perception. "
            "<bookmark mark='c'/>The theory explains unconscious perception neatly: the first-order state is "
            "present, and the higher-order state is not. <bookmark mark='d'/>Ned Block pressed the other case. "
            "What if there is a higher-order state with no first-order state for it to be about? Is there then "
            "something it is like to see a red that is not there?"
        ) as vo:
            self.play(FadeIn(hc), FadeIn(first))
            vo.wait_until("a")
            self.play(FadeIn(second), GrowArrow(arr), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeOut(second), FadeOut(arr))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(second), first.animate.set_opacity(0.2))
        self.clear_scene()

    def blindsight(self):
        head = label(r"Blindsight", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"the patient", r"damage to primary visual cortex: \ a region of the visual field reported blind",
                 GREY_A),
                (r"forced choice", r"asked to guess, \ he points to objects there and names their orientation, \ far "
                                   r"above chance \ (Weiskrantz, \ 1986)", OK),
                (r"no confidence", r"he insists he is only guessing", BAD),
                (r"the lesson", r"performance without awareness, \ or without the monitoring of performance: \ Lau "
                                r"and Rosenthal \ (2011)", SELF)]
        g = rows_table(rows, top=1.6, gap=0.5)
        with self.voiceover(
            "The evidence comes from a strange condition. <bookmark mark='a'/>After damage to the primary visual "
            "cortex, a patient reports a region of the visual field as blind. <bookmark mark='b'/>Yet asked to "
            "guess, Lawrence Weiskrantz found, the patient points to objects there, and names the orientation of "
            "lines, far above chance. <bookmark mark='c'/>And he insists he is only guessing. "
            "<bookmark mark='d'/>For Hakwan Lau and Rosenthal, this is first-order processing without higher-order "
            "monitoring: the information is used, but the system does not represent it as reliable perception. "
            "Lau's later theory calls the monitor perceptual reality monitoring."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def monitor(self):
        d = load("meta")
        head = label(r"Performance and confidence, \ simulated", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows = {r["observer"]: r for r in d["rows"]}
        assert d["d"] == 1.5 and d["trials"] == 20000
        assert [rows[k]["correct"] for k in rows] == [0.7705] * 3
        assert [rows[k]["auroc2"] for k in rows] == [0.7047, 0.6026, 0.4979]
        # two Gaussians and the decision criterion
        ax = Axes(x_range=[-4, 4, 1], y_range=[0, 0.45, 0.2], x_length=6.0, y_length=1.9, tips=False,
                  axis_config={"color": GREY_B}).move_to([-3.3, 1.55, 0])
        g0 = ax.plot(lambda x: np.exp(-(x + 0.75) ** 2 / 2) / np.sqrt(2 * np.pi), color=GREY_B)
        g1 = ax.plot(lambda x: np.exp(-(x - 0.75) ** 2 / 2) / np.sqrt(2 * np.pi), color=SIG)
        crit = DashedLine(ax.c2p(0, 0), ax.c2p(0, 0.44), color=WHITE)
        gl = label(r"absent \quad present: \ $d' = 1.5$", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.12)
        pipe = stack([(r"signal $\to$ \ `present' or `absent' \ (first order)", SIG),
                      (r"signal $+$ the monitor's noise $\to$ \ confidence \ (higher order)", SELF)], font_size=19,
                     aligned_edge=LEFT, buff=0.25).move_to([3.4, 1.6, 0])
        hd = [r"\text{observer}", r"\text{monitor's noise}", r"\text{correct}", r"\text{confidence tracks it}"]
        cells = [[label(k, font_size=19, color=SELF if k != "blindsight" else BAD),
                  label(f"{r['meta_noise']:g}", font_size=19, color=GREY_A),
                  label(f"{100 * r['correct']:.1f}\\%", font_size=19, color=OK),
                  label(f"{r['auroc2']:.3f}", font_size=19, color=OK if r["auroc2"] > 0.55 else BAD)]
                 for k, r in rows.items()]
        grid = ValueGrid(hd, cells, col_w=[3.4, 2.6, 2.0, 3.4], cell_h=0.52, font_size=19).move_to([0, -1.65, 0])
        foot = label(r"type-2 area under the ROC: \ 0.5 means confidence says nothing about being right",
                     font_size=17, color=GREY_A).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "The Reasoner simulates the dissociation in signal detection theory. <bookmark mark='a'/>A stimulus is "
            "present or absent; the observer's internal signal is noisy, with a sensitivity, d prime, of one and a "
            "half. It says present when the signal is above zero. <bookmark mark='b'/>A second-order monitor reads "
            "the same signal, with noise of its own, and turns it into confidence. <bookmark mark='c'/>Twenty "
            "thousand trials. A normal observer is right seventy seven percent of the time, and its confidence "
            "tracks its accuracy: the area under the type-two curve is 0.70. With a noisier monitor, 0.60. And "
            "when the monitor's noise swamps it, the observer is still right exactly as often, seventy seven "
            "percent, but its confidence says nothing about whether it is right: 0.498, chance. "
            "<bookmark mark='d'/>That is blindsight in miniature: the first-order state does its work, and the "
            "higher-order representation of it is missing. On a higher-order theory, what is missing is the "
            "experience."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax), Create(g0), Create(g1), Create(crit), FadeIn(gl), FadeIn(pipe[0]))
            vo.wait_until("b")
            self.play(FadeIn(pipe[1]))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(3):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.6)
            self.play(FadeIn(foot))
            vo.wait_until("d")
            self.play(Indicate(VGroup(*grid.cell[2]), color=BAD, scale_factor=1.04))
        self.clear_scene()

    def roc(self):
        d = load("meta")
        head = label(r"Confidence against correctness", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows = d["rows"]
        assert [r["auroc2"] for r in rows] == [0.7047, 0.6026, 0.4979]
        ax = Axes(x_range=[0, 1, 0.5], y_range=[0, 1, 0.5], x_length=4.8, y_length=4.8, tips=False,
                  axis_config={"color": GREY_B, "include_numbers": True, "font_size": 18,
                               "decimal_number_config": {"num_decimal_places": 1}}).move_to([-2.6, -0.4, 0])
        xl = label(r"confident when wrong", font_size=17, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.45)
        yl = label(r"confident when right", font_size=17, color=GREY_A).rotate(PI / 2).next_to(ax.y_axis, LEFT,
                                                                                             buff=0.45)
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=GREY_C)
        cols = [SELF, FUNC, BAD]
        curves = VGroup(*[VMobject(color=c, stroke_width=3).set_points_as_corners(
            [ax.c2p(a, b) for a, b in r["roc"]]) for r, c in zip(rows, cols)])
        keys = stack([(rf"{r['observer']}: \ area {r['auroc2']:.3f}", c) for r, c in zip(rows, cols)],
                     font_size=20, aligned_edge=LEFT, buff=0.3).move_to([3.4, 0.8, 0])
        foot = stack([(r"each point: \ one confidence threshold, \ over 20\,000 trials", GREY_A),
                      (r"the diagonal is a monitor that knows nothing about its own success", BAD)], font_size=19,
                     aligned_edge=LEFT, width=5.4, buff=0.25).move_to([3.4, -1.6, 0])
        with self.voiceover(
            "The same result as a picture. <bookmark mark='a'/>For each confidence threshold, plot how often the "
            "observer is confident when it is wrong, across, against how often it is confident when it is right, "
            "up. <bookmark mark='b'/>A good monitor bows far above the diagonal: when it is confident, it is "
            "usually right. <bookmark mark='c'/>A noisier monitor bows less. <bookmark mark='d'/>And the blindsight "
            "observer lies on the diagonal itself: its confidence carries no information about its own success, "
            "though its first-order answers are just as good. The area under each curve is the number in the "
            "table. Metacognitive measures like this are now used in experiments on consciousness, precisely "
            "because they separate how well a system performs from how well it knows that it does."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(diag), FadeIn(foot[0]))
            for mk, k in zip("bcd", range(3)):
                vo.wait_until(mk)
                self.play(Create(curves[k]), FadeIn(keys[k]), run_time=1.5)
            self.play(FadeIn(foot[1]))
        self.clear_scene()
