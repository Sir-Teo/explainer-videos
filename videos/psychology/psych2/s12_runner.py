from __future__ import annotations

import numpy as np

from videos.psychology.psych2.common import *  # noqa: F403


class Runner(VoiceoverScene):
    def construct(self):
        self.card()
        self.program()
        self.hans_model()
        self.map()

    def card(self):
        card = chapter_card(11, r"A design is a program", r"What does this part add to the things the series builds?",
                            lit=(), part=PART, scale=("group",), marr=("how",))
        with self.voiceover(
            "Chapter eleven. A design is a program."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def program(self):
        d = load("threats")
        e = d["designs"]["randomized"]
        head = heading(r"Three questions, three functions")
        qs = VGroup()
        for q, fn, color in ((r"Who gets what?", r"randomize(n)", P.ACCENT),
                             (r"In what order?", r"williams(k)", "#7EC8F5"),
                             (r"Compared with what?", r"difference(y, groups)", TRUTH)):
            qs.add(VGroup(label(q, font_size=34, color=color), label(rf"\texttt{{{fn}}}", font_size=30, color=WHITE))
                   .arrange(DOWN, buff=0.12))
        qs.arrange(RIGHT, buff=1.1).next_to(head, DOWN, buff=0.45)
        code = code_block([
            r"from explainer.psychology import lab, pool",
            r"L = lab.Lab(pool.Pool())",
            r"L.pre\_post(n=200)\ \ \ \ \ \ \ \ \ \ \ \ \ \# one group, before and after",
            r"L.randomized(n=200)\ \ \ \ \ \ \ \ \ \ \ \# shuffled, with a control group",
            r"L.crossover(n=40)\ \ \ \ \ \ \ \ \ \ \ \ \ \# each person both ways, order balanced",
            r"L.replicate('randomized', 500)\ \# the same study, five hundred times",
        ], font_size=32)
        if code.width > 12.4:
            code.scale_to_fit_width(12.4)
        code.move_to([0, -0.7, 0])
        out = VGroup(label(r"500 studies of a game that does nothing:", font_size=26, color=GREY_A),
                     label(rf"mean ${signed(e['mean'])}$ ms", font_size=34, color=TRUTH),
                     label(rf"spread {e['sd']:.1f} ms", font_size=30, color=WHITE))
        out.arrange(RIGHT, buff=0.5, aligned_edge=DOWN).next_to(code, DOWN, buff=0.4)
        keep_in_frame(out)
        tag = simulated_tag()
        with self.voiceover(
            "In Part 1 the series started building a model subject. Today it gets the other thing a psychology "
            "department has: a laboratory. <bookmark mark='a'/> A design answers three questions, and each is a "
            "small function. Who gets what: a shuffle. In what order: a square. Compared with what: a "
            "difference, with its uncertainty. <bookmark mark='b'/> Put together, a study is a few lines of "
            "code, and the Pool will run it as often as you like. That's how every number in this part was "
            "made. The six unsound designs are each a method you can call, and watch being wrong. "
            "<bookmark mark='c'/> It matters for the rest of the series. Whenever we show an experiment from "
            "now on, we can also show its design running on people whose truth we know, and ask the question "
            "you can never ask of a real study: would this design have found the right answer?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(q, shift=UP * 0.15) for q in qs], lag_ratio=0.5), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(code[0]), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in code.rows], lag_ratio=0.4),
                      run_time=4.0)
            vo.wait_until("c")
            self.play(FadeIn(out, shift=LEFT * 0.15), FadeIn(tag))
        self.clear_scene()

    def hans_model(self):
        d = load("hans")
        rd = d["reader"]
        head = heading(r"Hans, as four numbers")
        rows = d["rows"]
        names = [r"knows", r"does not know", r"seen", r"not seen", r"up to 3.5 m", r"3.5 to 4 m", r"4 to 4.5 m",
                 r"beyond 4.5 m"]
        groups = [(0, r"the number"), (2, r"blinders"), (4, r"distance")]
        w, gap, h = 0.5, 0.38, 2.9
        x = -5.75
        base_y = -0.85
        cols = VGroup()
        for i, (r, nm) in enumerate(zip(rows, names)):
            if i in (2, 4):
                x += 0.45
            data = Rectangle(width=w, height=max(r["share"] * h, 0.03), stroke_width=0, fill_color=P.HUMAN,
                             fill_opacity=0.9)
            data.move_to([x, base_y + data.height / 2, 0])
            model = Rectangle(width=w, height=max(r["model"] * h, 0.03), stroke_width=0, fill_color=P.PSYCHE,
                              fill_opacity=0.9)
            model.move_to([x + w, base_y + model.height / 2, 0])
            t = wrapped_label(nm, 1.3, 20, GREY_A).next_to([x + w / 2, base_y, 0], DOWN, buff=0.12)
            cols.add(VGroup(data, model, t))
            x += 2 * w + gap
        left_x = cols[0][0].get_left()[0] - 0.25
        base = Line([left_x, base_y, 0], [cols[-1][1].get_right()[0] + 0.2, base_y, 0], color=GREY_B, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([left_x, base_y + v * h, 0], [left_x + 0.1, base_y + v * h, 0], color=GREY_B),
                                label(rf"{100 * v:.0f}\%", font_size=18, color=GREY_B)
                                .next_to([left_x, base_y + v * h, 0], LEFT, buff=0.06)) for v in (0.5, 1.0)])
        gl = VGroup()
        for i, name in groups:
            last = i + (1 if i < 4 else 3)
            mid = (cols[i][0].get_left()[0] + cols[last][1].get_right()[0]) / 2
            gl.add(label(name, font_size=26, color=WHITE).move_to([mid, base_y - 0.95, 0]))
        chart = VGroup(cols, base, ticks, gl)
        if chart.get_right()[0] > 6.8:
            chart.shift(LEFT * (chart.get_right()[0] - 6.8))
        # the mechanism, before the fit
        def box(text, sub, color, x_):
            t = VGroup(label(text, font_size=34, color=color), wrapped_label(sub, 4.2, 24, WHITE)).arrange(DOWN, buff=0.15)
            b_ = RoundedRectangle(width=4.9, height=t.height + 0.6, corner_radius=0.15, stroke_color=color,
                                  stroke_width=2.5, fill_color=CARD_FILL, fill_opacity=1)
            return VGroup(b_, t).move_to([x_, 0.3, 0])

        q_box = box(r"the questioner", r"gives the cue at the right count, and only if he knows the answer",
                    P.HUMAN, -3.6)
        r_box = box(r"the reader", r"sees the cue less often from farther away, and sometimes guesses", P.PSYCHE,
                    3.6)
        link = Arrow(q_box.get_right(), r_box.get_left(), buff=0.12, color=KNOWS, stroke_width=5)
        l_lab = label(r"a millimetre", font_size=22, color=KNOWS).next_to(link, UP, buff=0.08)
        mech = VGroup(q_box, r_box, link, l_lab)
        leg = legend([(P.HUMAN, r"Pfungst's counts, 1904"), (P.PSYCHE, r"Psyche: \ the cue reader")], font_size=24)
        leg.arrange(RIGHT, buff=0.8).next_to(head, DOWN, buff=0.3)
        params = VGroup(
            label(rf"half-detection distance: \ {rd['d0']:.1f} m", font_size=24, color=P.PSYCHE),
            label(rf"steepness: \ {rd['sigma']:.2f}", font_size=24, color=P.PSYCHE),
            label(rf"cues missed up close: \ {100 * rd['lapse']:.0f}\%", font_size=24, color=P.PSYCHE),
            label(rf"right by accident: \ {100 * rd['guess']:.0f}\%", font_size=24, color=P.PSYCHE),
        ).arrange_in_grid(2, 2, buff=(0.8, 0.12), cell_alignment=LEFT).to_edge(DOWN, buff=0.7)
        tag = psyche_tag(rf"computed: four parameters, eight conditions; \ largest miss {100 * d['max_abs_miss']:.0f} "
                         r"points")
        src = historical_tag(archive.PFUNGST_1907.cite)
        with self.voiceover(
            "And the horse gets the same treatment as Donders' subject did. Explain it by building it. "
            "<bookmark mark='a'/> The model has a questioner, who gives the cue only if he knows the answer, and "
            "a reader, who sees the cue less often from farther away, misses a few even up close, and is "
            "sometimes right by accident. Four numbers. <bookmark mark='b'/> In white, Pfungst's eight "
            "conditions. In orange, the model. With knowledge and without. Seen and unseen. Near and far. "
            f"<bookmark mark='c'/> It's never out by more than {100 * d['max_abs_miss']:.0f} points, on tests of "
            "a few dozen trials each. <bookmark mark='d'/> Notice what kind of explanation this is. There's no "
            "arithmetic in the model anywhere. The horse's whole performance comes out of a detector with a "
            "threshold, and a human who can't keep still. The commission was asking whether a horse can think. "
            "The answer turned out to be a fact about perception, and the next act of the series is about that."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(q_box, shift=UP * 0.15), GrowArrow(link), FadeIn(l_lab), FadeIn(r_box, shift=UP * 0.15))
            self.play(FadeIn(params, lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeOut(mech))
            self.play(FadeIn(base), FadeIn(ticks), FadeIn(gl), FadeIn(leg[0]),
                      LaggedStart(*[AnimationGroup(GrowFromEdge(c[0], DOWN), FadeIn(c[2])) for c in cols],
                                  lag_ratio=0.15), run_time=3.5)
            self.play(FadeIn(leg[1]), LaggedStart(*[GrowFromEdge(c[1], DOWN) for c in cols], lag_ratio=0.15),
                      FadeIn(tag), run_time=3.0)
            vo.wait_until("d")
            self.play(Indicate(params, color=P.PSYCHE, scale_factor=1.03))
        self.clear_scene()

    def map(self):
        hm = homunculus_map(done=1, height=6.0).move_to([-3.8, 0.0, 0])
        text = VGroup(
            label(r"No new gear today.", font_size=40, color=P.MECH),
            wrapped_label(r"Parts 2, 3 and 4 build the laboratory, the ruler and the rules of evidence that every "
                          r"later gear is tested with.", 6.2, 30, WHITE),
            wrapped_label(r"The Pool can now be assigned, tested twice, and lost to follow-up.", 6.2, 28, P.POOL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.4, 0.2, 0])
        with self.voiceover(
            "So where does that leave the map? <bookmark mark='a'/> One faculty has a gear in it, and that "
            "hasn't changed. No new gear today. <bookmark mark='b'/> This act of the series doesn't build "
            "faculties. It builds the laboratory, the ruler, and the rules of evidence that every later gear "
            "will be tested with. <bookmark mark='c'/> What grew today is the Pool. Its people can now be "
            "assigned to groups, tested twice, and lost to follow-up, like real ones."
        ) as vo:
            self.play(FadeIn(hm))
            vo.wait_until("a")
            self.play(FadeIn(text[0], shift=LEFT * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(text[1], shift=LEFT * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(text[2], shift=LEFT * 0.15))
        self.clear_scene()
