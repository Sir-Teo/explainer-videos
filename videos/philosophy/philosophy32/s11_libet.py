from __future__ import annotations

from videos.philosophy.philosophy32.common import *  # noqa: F403


class Libet(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Libet's clock", r"Does the brain decide before we do?", lit=(1983, 2012),
                            part=PART)
        with self.voiceover("Chapter ten. Libet's clock."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.experiment()
        self.accumulator()
        self.average()
        self.interrupted()
        self.meaning()

    def experiment(self):
        hc = history_card(1983, r"Benjamin Libet et al.", r"\textit{Brain}", width=4.8, color=HIST).to_corner(
            UL, buff=0.3)
        ax = Arrow([-5.6, -1.2, 0], [5.6, -1.2, 0], buff=0, color=GREY_B)
        ticks = [(-4.0, r"$-550$ ms", r"readiness potential begins", LAW),
                 (0.6, r"$-200$ ms", r"`I wanted to move now'", WILL),
                 (4.2, r"$0$", r"the wrist moves", GREY_A)]
        marks = VGroup()
        for x, t, s, c in ticks:
            marks.add(VGroup(Line([x, -1.35, 0], [x, -1.05, 0], color=c), label(t, font_size=18, color=c).move_to(
                [x, -1.7, 0]), wrapped_label(s, 2.6, 18, c).move_to([x, -0.5, 0])))
        clock = VGroup(Circle(radius=0.9, color=GREY_B), Dot(ORIGIN, radius=0.05, color=GREY_B),
                       Line(ORIGIN, UP * 0.8, color=CHANCE)).move_to([3.6, 1.6, 0])
        cl = label(r"a fast clock: \ note where the spot was when you felt the urge", font_size=17,
                   color=GREY_A).next_to(clock, LEFT, buff=0.3)
        foot = label(r"the brain's preparation seems to start a third of a second before the felt decision",
                     font_size=20, color=BAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In 1983 Benjamin Libet and his colleagues brought the question into the laboratory. "
            "<bookmark mark='a'/>Subjects flexed their wrist whenever they felt like it, while watching a spot "
            "circle a fast clock, and reported where the spot was when they first felt the urge to move. "
            "<bookmark mark='b'/>The reported urge came about two hundred milliseconds before the movement. "
            "<bookmark mark='c'/>But a slow negative wave over the motor areas, the readiness potential, had begun "
            "some five hundred and fifty milliseconds before it. <bookmark mark='d'/>The brain, it seemed, starts "
            "preparing a third of a second before we decide. Libet himself left room for a veto: the urge could "
            "still be stopped."
        ) as vo:
            self.play(FadeIn(hc), GrowArrow(ax))
            vo.wait_until("a")
            self.play(FadeIn(clock), FadeIn(cl), Rotate(clock[2], -TAU, about_point=clock[1].get_center()),
                      run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(marks[1]), FadeIn(marks[2]))
            vo.wait_until("c")
            self.play(FadeIn(marks[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def accumulator(self):
        d = load("accumulator")
        head = label(r"A noisy accumulator, \ built", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        pr = d["params"]
        assert (pr["drift"], pr["leak"], pr["noise"], pr["threshold"]) == (0.1, 0.5, 0.1, 0.298)
        assert d["trials"] == 1000 and d["crossed"] == 964 and d["mean_wait"] == 6.329
        eq = MathTex(r"\dot x \;=\; I - k\,x + c\,\xi(t)", font_size=34, color=FUNC).move_to([-3.6, 2.3, 0])
        el = label(r"drift $I = 0.1$, \ leak $k = 0.5$, \ noise $c = 0.1$, \ threshold $0.298$", font_size=17,
                   color=GREY_A).next_to(eq, DOWN, buff=0.15)
        ax = Axes(x_range=[0, 14, 2], y_range=[0, 0.35, 0.1], x_length=7.6, y_length=3.4, tips=False,
                  axis_config={"color": GREY_B, "include_numbers": True, "font_size": 16,
                               "decimal_number_config": {"num_decimal_places": 1}}).move_to([-2.4, -1.2, 0])
        xl = label(r"seconds", font_size=16, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.35)
        thr = DashedLine(ax.c2p(0, pr["threshold"]), ax.c2p(14, pr["threshold"]), color=BAD)
        tl = label(r"threshold: \ the movement", font_size=16, color=BAD).next_to(thr, UP, buff=0.05).align_to(
            thr, RIGHT)
        cols = [FUNC, WILL, SELF, CHANCE, BLAME]
        paths = VGroup()
        for k, ex in enumerate(d["examples"]):
            pts = [ax.c2p(min(0.02 * i, 14), v) for i, v in enumerate(ex) if 0.02 * i <= 14]
            if len(pts) > 1:
                paths.add(VMobject(color=cols[k % 5], stroke_width=2).set_points_as_corners(pts))
        h = d["wait_hist"]
        bx = Axes(x_range=[0, 20, 5], y_range=[0, 300, 100], x_length=3.8, y_length=2.6, tips=False,
                  axis_config={"color": GREY_B, "include_numbers": True, "font_size": 16}).move_to([4.6, -0.6, 0])
        bars = VGroup(*[Rectangle(width=bx.x_axis.unit_size * 2 * 0.9, height=max(bx.y_axis.unit_size * c, 0.001),
                                  fill_color=WILL, fill_opacity=0.8, stroke_width=0).move_to(bx.c2p(2 * k + 1, 0),
                                                                                             aligned_edge=DOWN)
                        for k, c in enumerate(h)])
        bl = label(r"when it crosses, \ of 1000 runs", font_size=16, color=GREY_A).next_to(bx, UP, buff=0.12)
        bxl = label(r"mean 6.3 s; \ 964 cross within 20 s", font_size=17, color=WILL).next_to(bx, DOWN, buff=0.4)
        with self.voiceover(
            "In 2012 Aaron Schurger, Jacobo Sitt and Stanislas Dehaene offered another reading, and the Reasoner "
            "builds their model. <bookmark mark='a'/>Activity x drifts slowly upward, leaks back toward rest, and is "
            "jostled by noise. That is all: no decision anywhere in the equation. When x first crosses a threshold, "
            "the movement happens. <bookmark mark='b'/>Here are five runs. Each wanders, until the noise happens to "
            "carry it over the line. <bookmark mark='c'/>Over a thousand runs, crossings come at all sorts of times, "
            "on average after six point three seconds, like the spontaneous movements in Libet's task."
        ) as vo:
            self.play(FadeIn(head), Write(eq), FadeIn(el))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xl), Create(thr), FadeIn(tl))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.3), run_time=4)
            vo.wait_until("c")
            self.play(Create(bx), FadeIn(bl), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1))
            self.play(FadeIn(bxl))
        self.clear_scene()

    def average(self):
        d = load("accumulator")
        head = label(r"A readiness potential, \ from noise", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["averaged"] == 899 and (d["rp_start"], d["rp_end"], d["half_rise"]) == (0.1179, 0.2999, -0.354)
        ax = Axes(x_range=[-2, 0, 0.5], y_range=[0.1, 0.32, 0.05], x_length=7.6, y_length=4.2, tips=False,
                  axis_config={"color": GREY_B, "include_numbers": True, "font_size": 16,
                               "decimal_number_config": {"num_decimal_places": 2}}).move_to([-2.2, -0.5, 0])
        xl = label(r"seconds before the crossing", font_size=17, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.4)
        curve = VMobject(color=FUNC, stroke_width=4).set_points_as_corners(
            [ax.c2p(t, v) for t, v in zip(d["rp_t"], d["rp"])])
        half = DashedLine(ax.c2p(d["half_rise"], 0.1), ax.c2p(d["half_rise"], 0.32), color=GREY_C)
        hl = label(r"half the rise: \ 0.35 s before", font_size=16, color=GREY_A).next_to(half, UP, buff=0.05)
        side = stack([(r"899 runs, \ lined up at the moment each crossed", GREY_A),
                      (r"averaged backward: \ a slow build-up, \ like the readiness potential", FUNC),
                      (r"made by nothing but the noise that happened to carry $x$ over", WILL)], font_size=19,
                     aligned_edge=LEFT, width=4.2, buff=0.3).move_to([4.5, -0.2, 0])
        with self.voiceover(
            "Now do what Libet did with brain recordings. <bookmark mark='a'/>Take the eight hundred and ninety nine "
            "runs that waited at least two seconds, line them up at the moment each one crossed, and average "
            "backward. <bookmark mark='b'/>A slow, smooth build-up appears, rising from point one two to the "
            "threshold, half of it in the last third of a second: the shape of a readiness potential. "
            "<bookmark mark='c'/>But nothing in the model prepared anything. The build-up is the average of the "
            "noise that happened, on each run, to carry the activity over. Lining runs up at their crossings "
            "selects exactly those stretches."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(curve), run_time=3)
            self.play(Create(half), FadeIn(hl), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def interrupted(self):
        d = load("interruptus")
        head = label(r"A prediction the model got right", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        b = d["bins"]
        assert [x["mean_rt_ms"] for x in b] == [268.3, 186.4, 139.2, 74.9] and d["corr"] == -0.878
        hd = [r"\text{where } x \text{ was at the click}", r"\text{mean response time}"]
        names = [r"lowest quarter", r"second", r"third", r"highest quarter"]
        cells = [[label(n, font_size=19, color=GREY_A), label(f"{x['mean_rt_ms']:.0f} ms", font_size=20,
                                                               color=OK if k == 3 else WILL)]
                 for k, (n, x) in enumerate(zip(names, b))]
        grid = ValueGrid(hd, cells, col_w=[4.6, 3.2], cell_h=0.6, font_size=19).move_to([-2.6, -0.4, 0])
        bars = VGroup()
        for k, x in enumerate(b):
            w = x["mean_rt_ms"] / 100
            bars.add(Rectangle(width=w, height=0.36, fill_color=WILL, fill_opacity=0.8, stroke_width=0).move_to(
                [1.6 + w / 2, grid.cell[k][0].get_center()[1], 0]))
        side = stack([(r"a click at a random moment: \ move at once", GREY_A),
                      (r"in the model: \ a strong extra drift; \ the time to threshold depends on where the noise "
                       r"had carried $x$", FUNC),
                      (r"Schurger et al.: \ the slowest responses came when the brain's signal was furthest from "
                       r"threshold", GOAL)], font_size=19, buff=0.22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The model made a prediction, which the same paper tested. <bookmark mark='a'/>Interrupt subjects with "
            "a click at a random moment, and ask them to move at once. In the model the click adds a strong drift, "
            "and the time to reach threshold depends on where the noise had already carried x. "
            "<bookmark mark='b'/>The Reasoner clicks at random on two thousand three hundred trials. Sorted by "
            "where x was at the click, the mean response falls from two hundred and sixty eight milliseconds in the "
            "lowest quarter to seventy five in the highest. <bookmark mark='c'/>In the experiment, too, the fastest "
            "responses came when the slow brain signal was already furthest along, as the model predicts, and as "
            "the reading of the readiness potential as an early decision does not."
        ) as vo:
            self.play(FadeIn(head), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for k in range(4):
                self.play(*[FadeIn(c) for c in grid.cell[k]], GrowFromEdge(bars[k], LEFT), run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def meaning(self):
        head = label(r"What the experiments show", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"on the accumulator", r"the `decision' is the crossing, \ near the movement, \ not the start of "
                                        r"the potential", FUNC),
                (r"Soon et al. \ (2008)", r"fMRI predicted which of two buttons, \ seconds ahead, \ at about 60\%: \ "
                                          r"a bias, \ not a verdict", CHANCE),
                (r"Maoz et al. \ (2019)", r"for deliberate choices that matter, \ the readiness potential was absent",
                 WILL),
                (r"the philosophy", r"arbitrary flicks are a poor model of choosing; \ and a cause in the brain is not "
                                    r"a cause outside us", GOAL)]
        g = rows_table(rows, top=1.6, gap=0.5)
        with self.voiceover(
            "So what do the experiments show? <bookmark mark='a'/>On the accumulator reading, the decision is the "
            "crossing, close to the movement, not the beginning of the potential, which only looks like preparation "
            "when runs are averaged after the fact. <bookmark mark='b'/>In 2008 Chun Siong Soon and colleagues "
            "predicted, from brain scans, which of two buttons people would press, seconds ahead, but only about "
            "sixty percent of the time: a bias, not a verdict. <bookmark mark='c'/>And in 2019 Uri Maoz and "
            "colleagues found that for deliberate choices that mattered to the subjects, the readiness potential was "
            "absent altogether. <bookmark mark='d'/>Philosophically, an arbitrary flick of the wrist is a poor "
            "model of choosing, and a cause in the brain is not a cause outside us. These experiments matter, but "
            "less than the headlines said."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
