from __future__ import annotations

from videos.philosophy.philosophy18.common import *  # noqa: F403


class Kuhn(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Paradigms and revolutions", r"Is science a steady accumulation of truths?",
                            lit=(1962, 1970), part=PART)
        with self.voiceover("Chapter four. Paradigms and revolutions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.cycle()
        self.copernicus()
        self.toy()
        self.gestalt()
        self.values()

    def cycle(self):
        hc = history_card(1962, r"Thomas Kuhn", r"\textit{The Structure of Scientific Revolutions}", width=6.4,
                          color=HIST).to_corner(UL, buff=0.35)
        stages = [(r"normal science", THEORY), (r"anomalies", DATA), (r"crisis", BAD), (r"revolution", REAL),
                  (r"new paradigm", OK)]
        R = 2.0
        c0 = np.array([-2.6, -0.8, 0])
        nodes = VGroup()
        for i, (t, c) in enumerate(stages):
            a = PI / 2 - i * TAU / 5
            p = c0 + R * np.array([np.cos(a), np.sin(a), 0])
            nodes.add(VGroup(RoundedRectangle(width=2.2, height=0.62, corner_radius=0.15, color=c, stroke_width=2.5),
                             label(t, font_size=19, color=c)).move_to(p))
        arrows = VGroup(*[CurvedArrow(nodes[i].get_center() + (nodes[(i + 1) % 5].get_center() - nodes[i].get_center())
                                      * 0.32, nodes[(i + 1) % 5].get_center() - (nodes[(i + 1) % 5].get_center() -
                                                                                 nodes[i].get_center()) * 0.32,
                                      angle=-0.35, color=GREY_B, stroke_width=2.5) for i in range(5)])
        side = stack([(r"a paradigm: \ exemplary solutions, \ shared methods and values", THEORY),
                      (r"normal science solves puzzles; \ failures blame the scientist, \ not the paradigm", GREY_A),
                      (r"anomalies pile up \ (Mercury's perihelion, \ black-body radiation)", DATA),
                      (r"a revolution replaces the paradigm: \ Copernicus, \ Lavoisier, \ Einstein", REAL)],
                     font_size=20, aligned_edge=LEFT, width=5.8).move_to([3.6, -0.6, 0])
        with self.voiceover(
            "In 1962 Thomas Kuhn, a physicist turned historian, argued that science does not grow by steady "
            "accumulation. <bookmark mark='a'/>Most of the time scientists do normal science within a paradigm: a "
            "set of exemplary solutions, methods and values that define which problems matter. "
            "<bookmark mark='b'/>Normal science is puzzle-solving. When an experiment fails, the scientist is "
            "blamed, not the paradigm. <bookmark mark='c'/>But anomalies accumulate: the advance of Mercury's "
            "perihelion, the spectrum of black-body radiation. Eventually they produce a crisis. "
            "<bookmark mark='d'/>A revolution replaces the paradigm, as with Copernicus, Lavoisier and Einstein, "
            "and a new period of normal science begins."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(nodes[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Create(arrows[0]), FadeIn(nodes[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Create(arrows[1]), FadeIn(nodes[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Create(arrows[2]), FadeIn(nodes[3]), Create(arrows[3]), FadeIn(nodes[4]),
                      Create(arrows[4]))
        self.clear_scene()

    def copernicus(self):
        d = load("copernicus")
        head = label(r"The Copernican revolution: \ two geometries, \ one sky", font_size=28, color=CONN).to_edge(
            UP, buff=0.3)
        rm = d["rm"]
        s = 0.62
        cp = np.array([-4.6, 0.9, 0])
        cc = np.array([-1.4, 0.9, 0])
        t = ValueTracker(0.0)

        def ang(per):
            return 2 * np.pi * t.get_value() / per

        # Ptolemy: Earth at the centre; deferent (1.881 yr) carries an epicycle (1 yr)
        earth_p = Dot(cp, color=ANTI, radius=0.09)
        deferent = Circle(radius=rm * s, color=GREY_D, stroke_width=1.5).move_to(cp)
        epi = always_redraw(lambda: Circle(radius=1.0 * s, color=GREY_D, stroke_width=1.5).move_to(
            cp + rm * s * np.array([np.cos(ang(d["Tm"])), np.sin(ang(d["Tm"])), 0])))
        mars_p = always_redraw(lambda: Dot(cp + rm * s * np.array([np.cos(ang(d["Tm"])), np.sin(ang(d["Tm"])), 0])
                                           - s * np.array([np.cos(ang(1.0)), np.sin(ang(1.0)), 0]), color=BAD,
                                           radius=0.08))
        tp = label(r"Ptolemy: \ deferent and epicycle", font_size=17, color=GREY_A).next_to(deferent, DOWN, buff=0.75)
        trail = TracedPath(lambda: mars_p.get_center(), stroke_color=BAD, stroke_width=2, stroke_opacity=0.7)
        # Copernicus: Sun at the centre
        sun = Dot(cc, color=GOAL, radius=0.11)
        orb_e = Circle(radius=1.0 * s, color=GREY_D, stroke_width=1.5).move_to(cc)
        orb_m = Circle(radius=rm * s, color=GREY_D, stroke_width=1.5).move_to(cc)
        earth_c = always_redraw(lambda: Dot(cc + s * np.array([np.cos(ang(1.0)), np.sin(ang(1.0)), 0]), color=ANTI,
                                            radius=0.08))
        mars_c = always_redraw(lambda: Dot(cc + rm * s * np.array([np.cos(ang(d["Tm"])), np.sin(ang(d["Tm"])), 0]),
                                           color=BAD, radius=0.08))
        sight = always_redraw(lambda: Line(earth_c.get_center(), mars_c.get_center(), color=BAD, stroke_width=1.5,
                                           stroke_opacity=0.6))
        tc = label(r"Copernicus: \ two orbits about the Sun", font_size=17, color=GREY_A).next_to(orb_m, DOWN,
                                                                                               buff=0.75)
        ax = Axes(x_range=[0, 4, 1], y_range=[min(d["lon_deg"]) - 20, max(d["lon_deg"]) + 20, 180], x_length=5.4,
                  y_length=2.6, axis_config={"color": GREY_B, "include_ticks": False}).move_to([3.8, 1.0, 0])
        lon = series_plot(ax, d["lon_deg"], BAD, xs=d["t"], width=3)
        al = label(r"Mars's longitude, \ seen from Earth, \ over 4 years", font_size=17, color=GREY_A).next_to(
            ax, UP, buff=0.1)
        rows = stack([(r"identical predictions: \ largest difference " + f"{d['max_diff_deg']:.1f}" +
                       r"$^\circ$; \ " + f"{d['retrograde_episodes']}" + r" retrograde loops in both", OK),
                      (r"Ptolemy must stipulate that every outer planet's epicycle turns in exactly one year", BAD),
                      (r"Copernicus explains it: \ the epicycle \textit{is} the Earth's own orbit", GOAL),
                      (r"yet for decades Copernicus was no more accurate \ (Kuhn, \ \textit{The Copernican Revolution}, "
                       r"\ 1957)", GREY_A)], font_size=19, aligned_edge=LEFT, width=12.6).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Kuhn's first book was about the Copernican revolution, and the Reasoner can show what was, and was not, "
            "at stake. <bookmark mark='a'/>In Ptolemy's system, Mars rides on a small circle, the epicycle, whose "
            "centre rides on a large circle around the Earth. <bookmark mark='b'/>In Copernicus's, the Earth and "
            "Mars both circle the Sun. <bookmark mark='c'/>Track Mars's direction as seen from Earth in each. The "
            "two curves are identical, retrograde loops and all: the geometries are equivalent, and no observation "
            "of direction could tell them apart. <bookmark mark='d'/>But Ptolemy must stipulate that the epicycle of "
            "every outer planet turns in exactly one year. <bookmark mark='e'/>Copernicus explains the coincidence: "
            "the epicycle is the Earth's own orbit, seen from the moving Earth. <bookmark mark='f'/>And yet, as Kuhn "
            "showed, for decades the new system was no more accurate than the old. Its advantages were harmony and "
            "unification, values, not data."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(earth_p), Create(deferent), FadeIn(epi), FadeIn(mars_p), FadeIn(tp))
            self.add(trail)
            vo.wait_until("b")
            self.play(FadeIn(sun), Create(orb_e), Create(orb_m), FadeIn(earth_c), FadeIn(mars_c), FadeIn(sight),
                      FadeIn(tc))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(al))
            self.play(t.animate.set_value(4.0), Create(lon), run_time=6, rate_func=linear)
            self.play(FadeIn(rows[0]))
            for mk, r in zip("def", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def toy(self):
        d = load("kuhn")
        head = label(r"A toy of revolution \ (an analogy, \ not a model of history)", font_size=28,
                     color=CONN).to_edge(UP, buff=0.3)
        yrs = len(d["share_B"])
        ax = Axes(x_range=[0, yrs, 20], y_range=[0, 1, 0.25], x_length=7.0, y_length=3.6,
                  axis_config={"color": GREY_B, "font_size": 18, "include_numbers": True}).move_to([-2.2, -0.2, 0])
        amax = max(d["anomalies"])
        an = series_plot(ax, [a / amax for a in d["anomalies"]], DATA)
        sh = series_plot(ax, d["share_B"], REAL, width=4)
        xl = label(r"years", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.25)
        la = label(r"anomalies \ (scaled; \ " + f"{amax}" + r" by the end)", font_size=18, color=DATA).move_to(
            ax.c2p(yrs * 0.25, 0.6))
        lb = label(r"share working in paradigm B", font_size=18, color=REAL).move_to(ax.c2p(yrs * 0.8, 0.3))
        jx = d["jump_year"]
        jl = DashedLine(ax.c2p(jx, 0), ax.c2p(jx, 1), color=GOAL)
        side = stack([(f"{d['n']}" + r" scientists; \ anomalies arrive at random", WHITE),
                      (r"each has a tolerance for anomalies, \ and a social threshold: \ how many colleagues must "
                       r"switch first \ (Granovetter, \ 1978)", GREY_A),
                      (r"anomalies grow steadily; \ in year " + f"{jx}" + r" alone, \ " + f"{100 * d['jump']:.0f}" +
                       r"\% convert", GOAL),
                      (r"90\% only by year " + f"{d['t90']}" + r": \ holdouts linger \ (`science advances one funeral "
                       r"at a time')", BAD)], font_size=20, aligned_edge=LEFT, width=5.2).move_to([4.4, -0.2, 0])
        with self.voiceover(
            "Here is a toy that captures one feature of Kuhn's picture. It is an analogy, not a model of real "
            "history. <bookmark mark='a'/>Two hundred scientists work in paradigm A, and anomalies arrive at random "
            "over the years. <bookmark mark='b'/>Each scientist will tolerate a certain number of anomalies, and "
            "will switch only when enough colleagues have already switched: Mark Granovetter's threshold model of "
            "collective behaviour. <bookmark mark='c'/>The anomalies grow steadily. But conversion comes as a "
            "cascade: in a single year, more than forty percent of the community switches. "
            "<bookmark mark='d'/>Then holdouts linger for decades, as in Max Planck's remark that science advances "
            "one funeral at a time."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl))
            vo.wait_until("a")
            self.play(Create(an), FadeIn(la), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(sh), FadeIn(lb), run_time=2)
            self.play(Create(jl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def gestalt(self):
        head = label(r"Incommensurability", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        s = 1.3
        f = [np.array(p) * s for p in ([0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0])]
        off = np.array([0.55, 0.45, 0]) * s
        front = Polygon(*f, color=THEORY, stroke_width=3)
        back = Polygon(*[p + off for p in f], color=THEORY, stroke_width=3)
        edges = VGroup(*[Line(p, p + off, color=THEORY, stroke_width=3) for p in f])
        cube = VGroup(front, back, edges).move_to([-4.0, 0.6, 0])
        cl = label(r"Necker's cube: \ the same lines, \ two ways of seeing", font_size=18, color=GREY_A).next_to(
            cube, DOWN, buff=0.3)
        rows = [
            (r"meaning change", r"Newton's `mass' is conserved; \ Einstein's varies with speed: \ is it the same "
                                r"concept?", REAL),
            (r"no neutral language", r"observations are theory-laden \ (Hanson, \ 1958): \ Tycho and Kepler watch "
                                     r"the same dawn", DATA),
            (r"no algorithm", r"paradigm choice is like a gestalt switch, \ or a conversion", BAD),
            (r"the worry", r"is theory choice then irrational, \ `a matter for mob psychology' \ (Lakatos)?", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=5.8, x_label=-1.6, x_text=1.0, label_size=20, text_size=19)
        with self.voiceover(
            "Kuhn's most controversial claim was incommensurability. <bookmark mark='a'/>Look at this cube. The "
            "same lines can be seen with either face in front, and the switch is sudden and complete. "
            "<bookmark mark='b'/>Kuhn argued that rival paradigms differ in the same way. Newton's mass is "
            "conserved; Einstein's varies with speed. Are they even the same concept? <bookmark mark='c'/>There is "
            "no neutral observation language in which to compare them: observation is theory-laden, as Norwood "
            "Russell Hanson put it, imagining Tycho and Kepler watching the same dawn. One sees the sun rise, the "
            "other sees the horizon fall. <bookmark mark='d'/>So paradigm choice has no algorithm. It resembles a "
            "gestalt switch, or a conversion. <bookmark mark='e'/>Imre Lakatos's response was blunt: on this view, "
            "theory choice becomes a matter for mob psychology."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(cube), FadeIn(cl))
            self.play(Indicate(front, color=GOAL), run_time=0.8)
            self.play(Indicate(back, color=GOAL), run_time=0.8)
            for mk, r in zip("bcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def values(self):
        hc = history_card(1977, r"Thomas Kuhn", r"`Objectivity, Value Judgment, and Theory Choice'", width=6.6,
                          color=HIST).to_corner(UL, buff=0.35)
        vals = [r"accuracy", r"consistency", r"scope", r"simplicity", r"fruitfulness"]
        chips = VGroup(*[VGroup(RoundedRectangle(width=2.2, height=0.6, corner_radius=0.15, color=OK, stroke_width=2),
                                label(v, font_size=20, color=OK)) for v in vals]).arrange(RIGHT, buff=0.25)
        for c in chips:
            c[1].move_to(c[0])
        chips.next_to(hc, DOWN, buff=0.6).set_x(0)
        rows = stack([(r"five shared values guide theory choice: \ reasons, \ not an algorithm", WHITE),
                      (r"they conflict: \ Copernicus was simpler, \ not at first more accurate", BAD),
                      (r"and each scientist weighs them differently", GREY_A),
                      (r"Kuhn's mature view: \ rational, \ but not rule-governed", GOAL),
                      (r"a formal echo: \ Okasha \ (2011) \ applies Arrow's theorem to weighing them \ (Part 39)", REAL)],
                     font_size=21).next_to(chips, DOWN, buff=0.5)
        with self.voiceover(
            "Kuhn answered the charge in 1977. <bookmark mark='a'/>Theory choice is guided by five values that "
            "scientists share: accuracy, consistency, scope, simplicity and fruitfulness. These are reasons, but "
            "not an algorithm. <bookmark mark='b'/>They can conflict: Copernicus's system was simpler, but not at "
            "first more accurate than Ptolemy's. <bookmark mark='c'/>And individual scientists weigh them "
            "differently. <bookmark mark='d'/>The result is rational but not rule-governed. "
            "<bookmark mark='e'/>Samir Okasha later showed that combining such criteria into one ranking runs into "
            "Arrow's impossibility theorem, which Part 39 proves."
        ) as vo:
            self.play(FadeIn(hc), LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.15))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
