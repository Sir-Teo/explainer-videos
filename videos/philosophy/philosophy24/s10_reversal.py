from __future__ import annotations

from videos.philosophy.philosophy24.common import *  # noqa: F403


class Reversal(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Loschmidt and Zermelo", r"Can time-symmetric laws prove a one-way law?",
                            lit=(1872, 1896), part=PART)
        with self.voiceover("Chapter nine. Loschmidt and Zermelo."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.htheorem()
        self.loschmidt()
        self.stoss()
        self.zermelo()

    def htheorem(self):
        d = load("htheorem")
        hc = history_card(1872, r"Ludwig Boltzmann", r"`Further Studies on the Thermal Equilibrium of Gas "
                          r"Molecules'", width=6.6, color=HIST).to_corner(UL, buff=0.3)
        f = MathTex(r"H(t) = \int f(v, t)\, \log f(v, t)\, dv, \qquad \frac{dH}{dt} \le 0", font_size=32,
                    color=ENT).move_to([3.4, 1.9, 0])
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 1.0, 0.2], x_length=5.6, y_length=3.2,
                  axis_config={"color": GREY_B, "font_size": 16}, y_axis_config={"include_numbers": True}
                  ).move_to([-3.4, -0.9, 0])
        xnums = VGroup(*[MathTex(str(k - 3), font_size=16, color=GREY_A).next_to(ax.c2p(k, 0), DOWN, buff=0.12)
                         for k in range(7)])
        xl = label(r"velocity $v_x$", font_size=17, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.3)
        cs = [c + 3 for c in d["centers"]]
        w = cs[1] - cs[0]

        def bars(h, c):
            return VGroup(*[Rectangle(width=ax.c2p(w, 0)[0] - ax.c2p(0, 0)[0], height=max(
                ax.c2p(0, y)[1] - ax.c2p(0, 0)[1], 1e-3), stroke_width=0, fill_color=c, fill_opacity=0.75).move_to(
                [ax.c2p(x, 0)[0], (ax.c2p(0, y)[1] + ax.c2p(0, 0)[1]) / 2, 0]) for x, y in zip(cs, h)])

        b0 = bars(d["hists"][0], CHANCE)
        bN = bars(d["hists"][-1], ENT)
        s2 = d["sigma2"]
        maxw = ax.plot(lambda x: np.exp(-(x - 3) ** 2 / (2 * s2)) / np.sqrt(2 * np.pi * s2), x_range=[0, 6],
                       color=GOAL, stroke_width=3)
        ax2 = Axes(x_range=[0, len(d["H"]) - 1, 2], y_range=[0, 2.4, 0.5], x_length=4.6, y_length=2.8,
                   axis_config={"color": GREY_B, "font_size": 16}, x_axis_config={"include_numbers": True}
                   ).move_to([3.6, -1.0, 0])
        hnums = VGroup(*[MathTex(f"{h:.1f}", font_size=16, color=GREY_A).next_to(ax2.c2p(0, h + 5.4), LEFT, buff=0.1)
                         for h in (-5.0, -4.5, -4.0, -3.5, -3.0)])
        xl2 = label(r"collision rounds", font_size=17, color=GREY_A).next_to(ax2.x_axis, DOWN, buff=0.3)
        yl2 = label(r"$H$", font_size=20, color=ENT).next_to(ax2.y_axis, UP, buff=0.1)
        hcurve = series_plot(ax2, [h + 5.4 for h in d["H"]], ENT, width=3)
        hdots = VGroup(*[Dot(ax2.c2p(i, h + 5.4), radius=0.05, color=ENT) for i, h in enumerate(d["H"])])
        with self.voiceover(
            "In 1872 Boltzmann thought he had proved the second law from mechanics. <bookmark mark='a'/>Describe "
            "the gas by f, the distribution of molecular velocities, and define H as the integral of f log f. "
            "Boltzmann's equation for a dilute gas implies that H can only fall, until the velocities reach "
            "Maxwell's distribution. Minus H is the entropy. <bookmark mark='b'/>The Reasoner builds a toy version. "
            "Six thousand molecules, all moving at the same speed in random directions: this spiky distribution of "
            "one velocity component. <bookmark mark='c'/>Let them collide in random pairs, each collision keeping "
            "momentum and energy. <bookmark mark='d'/>H falls round after round, and the velocities settle into "
            "Maxwell's bell curve, drawn in gold. It looks like a proof that entropy must rise."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xnums), FadeIn(xl), FadeIn(b0))
            vo.wait_until("c")
            self.play(Create(ax2), FadeIn(hnums), FadeIn(xl2), FadeIn(yl2), FadeIn(hdots[0]))
            vo.wait_until("d")
            self.play(Transform(b0, bN), Create(hcurve), LaggedStart(*[FadeIn(x) for x in hdots[1:]],
                                                                     lag_ratio=0.15), run_time=3)
            self.play(Create(maxw))
        self.clear_scene()

    def loschmidt(self):
        d = load("freegas")
        hc = history_card(1876, r"Josef Loschmidt", r"the reversibility objection", width=5.4,
                          color=HIST).to_corner(UL, buff=0.3)
        f = MathTex(r"(q, p) \;\mapsto\; (q, -p)", font_size=40, color=TIME).move_to([3.6, 1.9, 0])
        ax = Axes(x_range=[0, 16, 4], y_range=[0, 4, 1], x_length=7.0, y_length=3.4,
                  axis_config={"color": GREY_B, "font_size": 16, "include_numbers": True}).move_to([-2.6, -1.0, 0])
        xl = label(r"time", font_size=17, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.3)
        yl = label(r"coarse-grained entropy (bits)", font_size=17, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1
                                                                                         ).align_to(ax, LEFT)
        t, e = d["t"], d["entropy"]
        half = len(t) // 2 + 1
        up = series_plot(ax, e[:half], ENT, xs=t[:half], width=3.5)
        down = series_plot(ax, e[half - 1:], TIME, xs=t[half - 1:], width=3.5)
        rev = DashedLine(ax.c2p(d["t_rev"], 0), ax.c2p(d["t_rev"], 4), color=GOAL)
        revl = label(r"every velocity reversed", font_size=17, color=GOAL).next_to(ax.c2p(d["t_rev"], 4), UP,
                                                                                  buff=0.1)
        side = stack([(r"Newton's laws are time-reversal invariant", LAW),
                      (r"for every history in which entropy rises, \ there is one in which it falls", BAD),
                      (r"so no theorem from the laws alone can say that it always rises", GOAL)], font_size=20,
                     aligned_edge=LEFT, width=4.6).move_to([4.5, -0.6, 0])
        with self.voiceover(
            "In 1876 Josef Loschmidt, Boltzmann's friend and colleague in Vienna, raised the objection that bears "
            "his name. <bookmark mark='a'/>The laws of mechanics are invariant under time reversal: take any state, "
            "keep the positions, flip every velocity, and the laws run the history backwards. "
            "<bookmark mark='b'/>Here is the film from the start of this part, with its entropy measured by "
            "dividing the box into sixteen cells. As the gas spreads, the entropy climbs toward four bits. "
            "<bookmark mark='c'/>Now reverse every velocity. The same laws carry the gas back into its corner, "
            "and the entropy falls to zero. <bookmark mark='d'/>For every history in which entropy rises, there is "
            "one in which it falls. So no theorem that uses only the laws of motion can prove that entropy always "
            "rises. Something else went into the H-theorem."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(Create(up), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(rev), FadeIn(revl))
            self.play(Create(down), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.clear_scene()

    def stoss(self):
        head = label(r"The hidden assumption", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        a = np.array([-3.4, 0.6, 0])
        b = np.array([-1.0, 0.6, 0])
        m1 = Dot(a, radius=0.2, color=LAW)
        m2 = Dot(b, radius=0.2, color=CHANCE)
        in1 = Arrow(a + LEFT * 1.6 + UP * 0.9, a, buff=0.25, color=LAW)
        in2 = Arrow(b + RIGHT * 1.6 + UP * 0.9, b, buff=0.25, color=CHANCE)
        out1 = Arrow(a, a + LEFT * 1.6 + DOWN * 0.9, buff=0.25, color=LAW, stroke_opacity=0.6)
        out2 = Arrow(b, b + RIGHT * 1.6 + DOWN * 0.9, buff=0.25, color=CHANCE, stroke_opacity=0.6)
        bef = label(r"before: \ uncorrelated", font_size=19, color=OK).move_to([-2.2, 2.1, 0])
        aft = label(r"after: \ correlated", font_size=19, color=BAD).move_to([-2.2, -0.9, 0])
        rows = stack([(r"the \textit{Stosszahlansatz}: \ molecules about to collide have independent velocities", ABS),
                      (r"assumed for every collision \textit{before} it happens, \ never after", TIME),
                      (r"run time backwards and the assumption fails: \ the asymmetry was put in by hand", BAD),
                      (r"the question becomes: \ why is the assumption true toward the future?", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=6.0, buff=0.3).move_to([3.4, -0.2, 0])
        with self.voiceover(
            "The something else is an assumption Boltzmann called the Stosszahlansatz, the hypothesis about the "
            "number of collisions. <bookmark mark='a'/>Molecules about to collide are assumed to have independent "
            "velocities: nothing about one tells you anything about the other. <bookmark mark='b'/>After they "
            "collide, their velocities are correlated, because they just met. <bookmark mark='c'/>The H-theorem "
            "assumes independence before every collision, never after. Run time backwards and the assumption fails, "
            "since every collision's after becomes a before. The asymmetry of the result was put in by an "
            "asymmetric assumption. <bookmark mark='d'/>So the real question is why the assumption holds toward the "
            "future and not toward the past."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(m1), FadeIn(m2), GrowArrow(in1), GrowArrow(in2), FadeIn(bef), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowArrow(out1), GrowArrow(out2), FadeIn(aft), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def zermelo(self):
        d = load("recur")
        hc = history_card(1896, r"Ernst Zermelo", r"after Poincaré's recurrence theorem \ (1890)", width=6.0,
                          color=HIST).to_corner(UL, buff=0.3)
        rows_txt = stack([(r"Poincaré: \ a bounded mechanical system returns arbitrarily close to its starting state, "
                           r"\ again and again", ABS),
                          (r"Zermelo: \ so entropy cannot rise forever; \ it must fall again", BAD),
                          (r"Boltzmann: \ yes, \ but the wait is beyond imagining", ENT)], font_size=21,
                         aligned_edge=LEFT, width=11.6, buff=0.28).move_to([0, 1.0, 0])
        hd = [r"\text{rotors}", rf"\text{{returns in }} {int(d['t_total']):,} \text{{ time units}}".replace(",", r"\,"),
              r"\text{mean wait}"]
        rows = [[MathTex(str(r["rotors"]), font_size=24), MathTex(f"{r['returns']:,}".replace(",", r"\,"),
                                                                  font_size=24),
                 MathTex(f"{r['mean_gap']:.1f}", font_size=24, color=ENT)] for r in d["rows"]]
        grid = ValueGrid(hd, rows, col_w=[1.6, 5.0, 2.4], cell_h=0.48, font_size=20).move_to([-1.9, -1.9, 0])
        gaps = [r["mean_gap"] for r in d["rows"]]
        assert gaps[0] == 0.7 and 3 <= gaps[1] < 3.5 and 19 < gaps[2] < 21 and 135 < gaps[3] < 150
        side = stack([(r"each new rotor multiplies the wait; \ a gas has $10^{23}$", GOAL)], font_size=20,
                     width=3.6).move_to([5.0, -1.9, 0])
        with self.voiceover(
            "The second objection came in 1896 from Ernst Zermelo, using a theorem Henri Poincaré proved in 1890. "
            "<bookmark mark='a'/>Poincaré's recurrence theorem: a bounded mechanical system returns arbitrarily "
            "close to its starting state, and does so again and again. <bookmark mark='b'/>So, said Zermelo, "
            "entropy cannot rise forever: the gas will one day gather itself back into its corner. "
            "<bookmark mark='c'/>Boltzmann agreed, and pointed to the time it takes. <bookmark mark='d'/>The "
            "Reasoner shows why, with rotors turning at incommensurable rates, all starting from zero, and counts "
            "how often every rotor is back within a twentieth of a turn of the start. One rotor returns every "
            "seven-tenths of a time unit; two, every three; three, every twenty; four, every hundred and forty. "
            "<bookmark mark='e'/>Each new degree of freedom multiplies the wait. A gas has ten to the twenty-three "
            "of them."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abc", rows_txt):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.5)
            vo.wait_until("e")
            self.play(FadeIn(side))
        self.clear_scene()
