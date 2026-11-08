from __future__ import annotations

from videos.philosophy.philosophy26.common import *  # noqa: F403


class GRW(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Spontaneous collapse", r"What if the wavefunction collapses on its own?",
                            lit=(1986,), part=PART)
        with self.voiceover("Chapter twelve. Spontaneous collapse."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.rule()
        self.amplify()
        self.hit()
        self.tests()

    def rule(self):
        d = load("grw")
        hc = history_card(1986, r"Ghirardi, \ Rimini and Weber", r"`Unified Dynamics for Microscopic and Macroscopic "
                          r"Systems'", width=6.8, color=HIST).to_corner(UL, buff=0.3)
        rows = stack([(r"every particle, \ at random times, \ suffers a `hit'", WHITE),
                      (r"the hit multiplies its wavefunction by a narrow Gaussian, \ and renormalizes", WAVE),
                      (r"where the hit lands: \ chosen with Born-rule probability", ABS),
                      (rf"two new constants of nature: \ rate $\lambda \approx 10^{{-16}}$ per second, \ width "
                       rf"$\sigma \approx 10^{{-7}}$ m", ALICE),
                      (rf"for one particle: \ a hit about every {d['one_particle_years']:.0f} hundred million years",
                       GOAL)], font_size=22, aligned_edge=LEFT, width=11.6, buff=0.32).move_to([0, -0.4, 0])
        with self.voiceover(
            "In 1986 GianCarlo Ghirardi, Alberto Rimini and Tullio Weber gave up the linearity of the equation. "
            "<bookmark mark='a'/>Every particle, at random times, suffers a hit. <bookmark mark='b'/>The hit "
            "multiplies its wavefunction by a narrow bell curve centred somewhere, and renormalizes, localizing the "
            "particle. <bookmark mark='c'/>Where the hit lands is chosen with a probability that reproduces the Born "
            "rule. <bookmark mark='d'/>There are two new constants of nature: a rate of about ten to the minus "
            "sixteen per second, and a width of about a ten-thousandth of a millimetre. <bookmark mark='e'/>For a "
            "single particle, hits are absurdly rare: about one every three hundred million years. So atoms and "
            "molecules behave exactly as quantum mechanics says."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def amplify(self):
        d = load("grw")
        head = label(r"Amplification", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        hd = [r"\text{particles in the superposed body}", r"\text{mean time to the first hit}"]

        def fmt(s):
            yrs = s / 3.156e7
            if s >= 3.156e7:
                return rf"{yrs:.0e}".replace("e+0", r"\times 10^{").replace("e+", r"\times 10^{") + r"}\ \text{years}"
            m, e = f"{s:.0e}".split("e")
            return rf"{m} \times 10^{{{int(e)}}}\ \text{{s}}"

        rows = []
        for r in d["rows"]:
            n = r["particles"]
            nt = r"1" if n == 1 else rf"10^{{{int(round(math.log10(n)))}}}"
            rows.append([MathTex(nt, font_size=26), MathTex(fmt(r["mean_wait_s"]), font_size=26, color=ALICE)])
        grid = ValueGrid(hd, rows, col_w=[5.4, 5.0], cell_h=0.55, font_size=22).move_to([0, 0.4, 0])
        foot = label(r"a pointer in a superposition of two places collapses as soon as any one of its particles is "
                     r"hit", font_size=21, color=GOAL).next_to(grid, DOWN, buff=0.6)
        with self.voiceover(
            "The trick is amplification. <bookmark mark='a'/>A measuring device is made of about ten to the "
            "twenty-three particles. If the pointer is in a superposition of two positions, a hit on any one of its "
            "particles localizes that particle, and, because the particles are entangled with one another, the whole "
            "pointer with it. <bookmark mark='b'/>So the waiting time shrinks in proportion to the number of "
            "particles: from three hundred million years for one particle, to about a ten-millionth of a second for "
            "a pointer. Cats are never dead and alive for long."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.5)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def hit(self):
        d = load("grw")
        head = label(r"A hit, \ simulated", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[-2, 2, 0.5], y_range=[0, max(max(d["after"]), max(d["before"])) * 1.1, 2], x_length=9.0,
                  y_length=3.6, axis_config={"color": GREY_B, "font_size": 16}, x_axis_config={
                      "include_numbers": True}, y_axis_config={"include_ticks": False}).move_to([-0.6, -0.6, 0])
        xl = label(r"position (micrometres)", font_size=18, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.4)
        before = series_plot(ax, d["before"], WAVE, xs=d["x_um"], width=3)
        after = series_plot(ax, d["after"], ALICE, xs=d["x_um"], width=3)
        mark_ = DashedLine(ax.c2p(d["hit_um"], 0), ax.c2p(d["hit_um"], max(d["after"])), color=BAD)
        side = stack([(r"blue: \ a particle in two places, \ one micrometre apart", WAVE),
                      (rf"a hit lands at {d['hit_um']:+.2f} $\mu$m, \ chosen with Born weights", BAD),
                      (rf"orange: \ afterwards, \ {100 * max(d['left_weight_after'], 1 - d['left_weight_after']):.4f}\% "
                       r"in one place", ALICE)], font_size=20, aligned_edge=LEFT, width=4.0, buff=0.3).move_to(
            [5.0, 1.4, 0])
        with self.voiceover(
            "Here is one hit, simulated. <bookmark mark='a'/>A particle in a superposition of two places a micrometre "
            "apart. <bookmark mark='b'/>A hit lands, its centre drawn with the probabilities GRW prescribes, near "
            "one of the two packets. <bookmark mark='c'/>Multiply by the Gaussian and renormalize: the other packet "
            "is suppressed by a factor so large that essentially all the probability is in one place. The "
            "superposition has collapsed, by the dynamics alone, with no observer in the story."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl))
            vo.wait_until("a")
            self.play(Create(before), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(mark_), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(after), FadeIn(side[2]))
        self.clear_scene()

    def tests(self):
        head = label(r"A theory you can test", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the difference", r"GRW is not an interpretation: \ it makes different predictions, \ for big enough "
                                r"superpositions", OK),
            (r"heating", r"hits jostle particles: \ a tiny, \ universal heating, \ and stray X-rays", ALICE),
            (r"the bounds", r"matter-wave interferometry with large molecules; \ cold atoms; \ gravitational-wave "
                            r"detectors; \ underground X-ray searches", ABS),
            (r"so far", r"no collapse seen; \ the simplest gravity-related model \ (Diósi--Penrose) \ ruled out by "
                        r"an underground test \ (Donadi et al., \ 2021)", BAD),
            (r"the cost", r"two new constants, \ and energy not quite conserved", BAD),
        ]
        g = rows_table(rows, top=1.7, gap=0.45, width=8.6, x_text=-2.4, label_size=22, text_size=21)
        with self.voiceover(
            "GRW has a virtue the interpretations lack. <bookmark mark='a'/>It is a different theory, with different "
            "predictions, for large enough superpositions. <bookmark mark='b'/>Each hit jostles a particle a little, "
            "so matter should be very slightly heated, and charged particles should emit faint X-rays. "
            "<bookmark mark='c'/>Experiments bound the constants from several sides: interferometry with ever "
            "larger molecules, cold atoms, gravitational-wave detectors, and searches for X-rays deep underground. "
            "<bookmark mark='d'/>So far no collapse has been seen. A 2021 experiment in the Gran Sasso laboratory, by "
            "Sandro Donadi and colleagues, ruled out the simplest gravity-related collapse model, Diósi and Penrose's. "
            "<bookmark mark='e'/>The cost of GRW: two new constants of nature, and energy that is not quite "
            "conserved."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
