from __future__ import annotations

import numpy as np

from videos.stats.stats1.common import *  # noqa: F403


class SameStats(VoiceoverScene):
    def construct(self):
        self.card()
        self.anscombe()
        self.morph()
        self.algorithm()

    def card(self):
        card = chapter_card(11, r"Same statistics, different pictures", r"What do the numbers leave out?",
                            lit={1973: r"Anscombe's quartet", 2017: r"Matejka--Fitzmaurice: same stats, different graphs"},
                            part=PART)
        with self.voiceover("Chapter eleven. Same statistics, different pictures."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def anscombe(self):
        d = load("anscombe")["sets"]
        panels = VGroup()
        for k in ("1", "2", "3", "4"):
            s_ = d[k]
            P = axes([2, 20], [2, 14], x_length=3.4, y_length=2.3, xticks=[5, 10, 15, 20], yticks=[4, 8, 12],
                     font_size=16)
            ax = P.ax
            pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.055, color=S.MUSEUM) for a, b in zip(s_["x"], s_["y"])])
            line = Line(ax.c2p(3, s_["a"] + 3 * s_["b"]), ax.c2p(19, s_["a"] + 19 * s_["b"]), color=S.EST,
                        stroke_width=2.5)
            t = label(rf"{'I' * int(k) if k != '4' else 'IV'}", font_size=24, color=GREY_A).next_to(P, UP, buff=0.05)
            panels.add(VGroup(P, line, pts, t))
        panels.arrange_in_grid(2, 2, buff=(0.5, 0.55)).move_to([-3.0, -0.2, 0])
        s1 = d["1"]
        rows = [(r"mean of $x$", f"{s1['mx']:.1f}"), (r"mean of $y$", f"{s1['my']:.2f}"),
                (r"variance of $x$", f"{s1['vx']:.1f}"), (r"variance of $y$", f"{s1['vy']:.2f}"),
                (r"correlation", f"{s1['r']:.3f}"), (r"line", rf"y = {s1['a']:.2f} + {s1['b']:.3f}\,x")]
        tab = VGroup(*[VGroup(label(a, font_size=26, color=GREY_A), MathTex(b, font_size=30)) for a, b in rows])
        for r in tab:
            r[1].next_to(r[0], RIGHT, buff=0.4)
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.3, 0.3, 0])
        same = label(r"nearly equal in all four", font_size=26, color=S.ACCENT).next_to(tab, DOWN,
                                                                                                    buff=0.4)
        src = historical_tag(r"Anscombe (1973), \emph{The American Statistician}")
        descr = [r"a line, with noise", r"a curve", r"a line, and one outlier", r"no relation, and one lever"]
        dl = VGroup(*[label(t, font_size=20, color=S.ACCENT).next_to(p[0], DOWN, buff=0.08) for t, p in
                      zip(descr, panels)])
        with self.voiceover(
            "Everything so far has been a summary: a centre, a spread, a correlation. Here's what summaries can "
            "hide. <bookmark mark='a'/> In 1973 Francis Anscombe published four small datasets, eleven points each. "
            "<bookmark mark='b'/> All four have nearly the same means, variances, correlation, and best-fitting "
            "line. The published observations are rounded, so the summaries differ slightly in their last digits. "
            "As far as these summaries suggest, they're almost the same data. <bookmark mark='c'/> Now look. "
            "The first is what you'd imagine: a line with "
            "noise. The second is a smooth curve, with no noise at all. The third is a perfect line, except for one "
            "point that drags the fit. And in the fourth, x doesn't vary at all, except for a single point that "
            "creates the entire correlation by itself. <bookmark mark='d'/> Anscombe's moral was blunt: make both "
            "calculations and graphs. Both sorts of output should be studied; each will contribute to "
            "understanding."
        ) as vo:
            self.play(FadeIn(src), LaggedStart(*[FadeIn(p[0]) for p in panels], lag_ratio=0.2))
            vo.wait_until("a")
            self.play(*[Indicate(p[0], color=S.MUSEUM, scale_factor=1.02) for p in panels])
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in tab], lag_ratio=0.25), run_time=3.0)
            self.play(*[Create(p[1]) for p in panels], FadeIn(same))
            vo.wait_until("c")
            for p, t in zip(panels, dl):
                self.play(LaggedStart(*[GrowFromCenter(q) for q in p[2]], lag_ratio=0.05), FadeIn(p[3]), FadeIn(t),
                          run_time=1.4)
            vo.wait_until("d")
            self.play(Indicate(dl, color=S.ACCENT, scale_factor=1.05))
        self.clear_scene()

    def morph(self):
        m = load("morph")
        frames = np.concatenate([np.asarray(m["frames1"]), np.asarray(m["frames2"])[1:]])
        n1 = len(m["frames1"]) - 1
        x0, x1, y0, y1 = m["bounds"]
        x0, x1, y0, y1 = x0 - 4, x1 + 4, y0 - 4, y1 + 4
        box = Rectangle(width=7.4, height=5.8, stroke_color=GREY_D, stroke_width=1.5).move_to([-2.9, -0.5, 0])
        X0 = box.get_corner(DL)
        sc = np.array([7.4 / (x1 - x0), 5.8 / (y1 - y0), 0])
        t = ValueTracker(0.0)

        # each frame shows one snapshot of the search as it is (no interpolation), so the statistics on screen
        # are those of a real dataset at every frame
        def pos(i):
            p = frames[int(round(t.get_value())), i]
            return X0 + np.array([p[0] - x0, p[1] - y0, 0]) * sc

        dots = VGroup(*[Dot(radius=0.05, color=S.DATA) for _ in range(frames.shape[1])])
        for i, d_ in enumerate(dots):
            d_.add_updater(lambda mob, i=i: mob.move_to(pos(i)))
            d_.update()

        def current():
            return frames[int(round(t.get_value()))]

        names = [r"mean $x$", r"mean $y$", r"SD $x$", r"SD $y$", r"corr"]
        vals = VGroup()
        rows = VGroup()
        for k, nm in enumerate(names):
            dn = DecimalNumber(0, num_decimal_places=2, font_size=40, color=S.ACCENT)
            rows.add(VGroup(label(nm, font_size=30, color=GREY_A), dn).arrange(RIGHT, buff=0.4))
            vals.add(dn)
        rows.arrange(DOWN, aligned_edge=RIGHT, buff=0.32).move_to([4.6, 0.2, 0])

        def upd_stats(_):
            P = current()
            st = [P[:, 0].mean(), P[:, 1].mean(), P[:, 0].std(ddof=1), P[:, 1].std(ddof=1),
                  np.corrcoef(P[:, 0], P[:, 1])[0, 1]]
            for dn, v in zip(vals, st):
                dn.set_value(float(np.round(v, 2)))

        rows.add_updater(upd_stats)
        rows.update()
        head = label(r"live, \ from the points on screen", font_size=24, color=GREY_B).next_to(rows, UP, buff=0.35)
        tag = simulated_tag(r"simulated: 142 World adults, \ (age, log income) rescaled")
        with self.voiceover(
            "Anscombe built his four by hand. In 2017 Justin Matejka and George Fitzmaurice showed you can make as "
            "many as you like, by computer, from any data. <bookmark mark='a'/> Here are a hundred and forty-two "
            "adults from the World: age across, the logarithm of income up, rescaled to a box. On the right, their "
            "five summary statistics, computed live from the points on the screen. <bookmark mark='b'/> Watch the "
            "points, and then watch the numbers. <bookmark mark='c'/> The cloud is becoming a word, and not one of "
            f"the five statistics moves in the second decimal place. <bookmark mark='d'/> And from the word to a "
            "ring. Same means, same spreads, same correlation. Three completely different datasets that these "
            "five summaries call identical. Other summaries, such as quantiles, can distinguish them."
        ) as vo:
            self.play(Create(box), FadeIn(dots, lag_ratio=0.01), FadeIn(rows), FadeIn(head), FadeIn(tag))
            vo.wait_until("b")
            self.play(t.animate.set_value(n1), run_time=10.0, rate_func=smooth)
            vo.wait_until("d")
            self.play(t.animate.set_value(len(frames) - 1), run_time=8.0, rate_func=smooth)
        for d_ in dots:
            d_.clear_updaters()
        rows.clear_updaters()
        self.keep = (box, dots, rows, head, tag)

    def algorithm(self):
        m = load("morph")
        box, dots, rows, head, tag = self.keep
        steps = VGroup(
            label(r"repeat a few hundred thousand times:", font_size=26, color=GREY_A),
            label(r"1.\ \ move one random point a little", font_size=26),
            label(r"2.\ \ keep the move only if the five statistics", font_size=26),
            label(r"\qquad are unchanged to two decimals, \ and", font_size=26),
            label(r"3.\ \ the point is now closer to the target shape \\ \qquad (or, early on, at random: annealing)",
                  font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        if steps.width > 5.9:
            steps.width = 5.9
        steps.move_to([3.85, -2.05, 0])
        moral = label(r"a summary is a projection: \ many datasets, \ one shadow", font_size=30, color=S.ACCENT)
        moral.move_to([-2.9, 3.35, 0])
        with self.voiceover(
            "How is it done? <bookmark mark='a'/> With a simple search. Move one point a tiny random step. Keep the "
            "move only if all five statistics are unchanged to two decimals, and the point has moved closer to the "
            "target shape. Early on, also accept some moves that don't help, at random, so the search doesn't get "
            "stuck; that's simulated annealing. <bookmark mark='b'/> Run it a few hundred thousand times and the "
            f"points settle onto the letters, on average within {m['dist1']:.2f} units of them, and then onto the "
            f"ring, within {m['dist2']:.2f}. <bookmark mark='c'/> The lesson is geometric. A summary statistic maps "
            "a whole dataset to a few numbers, like a shadow cast by a three-dimensional object. Infinitely many "
            "different datasets cast the same shadow. So look at the data, not only at its shadow."
        ) as vo:
            self.play(rows.animate.shift(UP * 0.9), head.animate.shift(UP * 0.9))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_, shift=UP * 0.1) for s_ in steps], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(moral, shift=DOWN * 0.2))
        self.clear_scene()
