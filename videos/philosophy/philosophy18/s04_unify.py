from __future__ import annotations

from videos.philosophy.philosophy18.common import *  # noqa: F403


class Unify(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Unification and mechanism", r"Does explaining mean seeing many things as one?",
                            lit=(1981, 1984), part=PART)
        with self.voiceover("Chapter three. Unification and mechanism."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.moon()
        self.kitcher()
        self.mechanism()
        self.pseudo()

    def moon(self):
        d = load("explain")["moon"]
        head = label(r"Newton's moon test: \ one law, \ apple and Moon", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        earth = Circle(radius=0.55, color=ANTI, fill_opacity=0.35).move_to([-4.2, -0.6, 0])
        el = label(r"Earth", font_size=18, color=ANTI).move_to(earth)
        orbit = Circle(radius=2.6, color=GREY_D, stroke_width=1.5).move_to(earth)
        moon = Dot(earth.get_center() + 2.6 * np.array([np.cos(0.6), np.sin(0.6), 0]), radius=0.16, color=GREY_A)
        ml = label(r"Moon \ ($60\,R_\oplus$)", font_size=18, color=GREY_A).next_to(moon, RIGHT, buff=0.12)
        apple = Dot(earth.get_center() + UP * 0.75, radius=0.08, color=BAD)
        eqs = VGroup(
            MathTex(r"g = " + f"{d['g']:.2f}" + r"\ \mathrm{m/s^2}", font_size=30, color=BAD),
            MathTex(r"\text{inverse square: } \frac{g}{" + f"{d['ratio']:.1f}" + r"^2} = " +
                    f"{d['predicted'] * 1000:.2f}" + r"\times 10^{-3}\ \mathrm{m/s^2}", font_size=30, color=THEORY),
            MathTex(r"\text{Moon's orbit: } \frac{4\pi^2 r}{T^2} = " + f"{d['a_moon'] * 1000:.2f}" +
                    r"\times 10^{-3}\ \mathrm{m/s^2}", font_size=30, color=GREY_A),
            label(r"agreement within " + f"{abs(d['agreement'] - 1) * 100:.0f}" + r"\%: \ the fall of an apple "
                  r"and the orbit of the Moon are one phenomenon", font_size=20, color=OK),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([3.3, -0.4, 0])
        if eqs.width > 6.6:
            eqs.width = 6.6
            eqs.move_to([3.3, -0.4, 0])
        with self.voiceover(
            "The deepest explanations unify. <bookmark mark='a'/>Newton asked whether the force that pulls an apple "
            "to the ground also holds the Moon in its orbit. Near the Earth's surface things fall with an "
            "acceleration of nine point eight one metres per second squared. <bookmark mark='b'/>The Moon is sixty "
            "Earth radii away. If gravity weakens as the inverse square, the Moon should fall toward us with that "
            "acceleration divided by sixty squared: about two point seven thousandths. <bookmark mark='c'/>From "
            "the Moon's distance and its period of twenty-seven days, its actual acceleration toward the Earth is "
            "almost exactly that. <bookmark mark='d'/>Two phenomena that looked unrelated, falling and orbiting, "
            "became one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(earth), FadeIn(el), Create(orbit), FadeIn(moon), FadeIn(ml))
            vo.wait_until("a")
            self.play(FadeIn(apple))
            self.play(apple.animate.move_to(earth.get_top()), FadeIn(eqs[0]), run_time=1)
            vo.wait_until("b")
            self.play(Write(eqs[1]))
            vo.wait_until("c")
            end = earth.get_center() + 2.6 * np.array([np.cos(1.4), np.sin(1.4), 0])
            self.play(Rotate(moon, angle=0.8, about_point=earth.get_center()),
                      ml.animate.next_to(end, RIGHT, buff=0.12), Write(eqs[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(eqs[3]))
        self.clear_scene()

    def kitcher(self):
        hc = history_card(1981, r"Philip Kitcher", r"`Explanatory Unification'", width=5.4,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = [
            (r"Friedman \ (1974)", r"science explains by reducing the number of independent phenomena we must accept "
                                   r"as brute", THEORY),
            (r"Kitcher \ (1981, \ 1989)", r"an explanation instantiates an argument pattern from the store that "
                                          r"derives the most from the fewest patterns", REAL),
            (r"Darwin", r"one pattern \ (variation, \ inheritance, \ selection) \ explains biogeography, \ "
                        r"homology, \ vestigial organs", OK),
            (r"the objection", r"the flagpole again: \ deriving heights from shadows is just as unifying", BAD),
            (r"a successor", r"Strevens's \textit{kairetic} account \ (2008): \ from a unifying derivation, \ keep "
                             r"only what makes a difference", GOAL),
        ]
        g = rows_table(rows, top=1.4, gap=0.45, width=8.4, x_text=-2.4)
        with self.voiceover(
            "Michael Friedman and Philip Kitcher made unification a theory of explanation. "
            "<bookmark mark='a'/>Friedman: science explains by reducing the number of independent phenomena we must "
            "accept as brute facts. <bookmark mark='b'/>Kitcher: an explanation is an instance of an argument "
            "pattern, and the best set of patterns derives the most conclusions from the fewest patterns. "
            "<bookmark mark='c'/>Darwin's single pattern, variation, inheritance and selection, explains "
            "biogeography, homology and vestigial organs at once. <bookmark mark='d'/>The flagpole returns as an "
            "objection: a pattern that derives heights from shadows unifies just as well. "
            "<bookmark mark='e'/>Michael Strevens's kairetic account answers by keeping, from a unifying derivation, "
            "only the factors that make a difference to the outcome."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def mechanism(self):
        head = label(r"Mechanisms: \ how the parts produce the phenomenon", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        names = [r"depolarization", r"Ca$^{2+}$ influx", r"vesicles fuse", r"transmitter crosses", r"receptor opens"]
        boxes = VGroup()
        for i, n in enumerate(names):
            b = RoundedRectangle(width=2.3, height=0.8, corner_radius=0.12, color=THEORY, stroke_width=2.5)
            t = label(n, font_size=17, color=WHITE)
            if t.width > 2.1:
                t.width = 2.1
            boxes.add(VGroup(b, t.move_to(b)))
        boxes.arrange(RIGHT, buff=0.35).move_to([0, 1.1, 0])
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.05, color=GREY_B,
                                stroke_width=3, max_tip_length_to_length_ratio=0.3) for i in range(4)])
        cap = label(r"chemical transmission at a synapse: \ entities and activities, \ organized", font_size=19,
                    color=GREY_A).next_to(boxes, DOWN, buff=0.3)
        rows = stack([
            (r"Machamer, \ Darden and Craver \ (2000): \ `entities and activities organized such that they are "
             r"productive of regular changes'", REAL),
            (r"Salmon \ (1984): \ causal processes transmit marks; \ explanation traces them", THEORY),
            (r"most of biology explains this way, \ with few laws in Hempel's sense", OK),
            (r"how much detail? \ Craver's mutual manipulability: \ a part is relevant if wiggling it changes the "
             r"whole", GOAL),
        ], font_size=20, aligned_edge=LEFT, width=12.4).next_to(cap, DOWN, buff=0.45)
        with self.voiceover(
            "Biologists rarely cite laws. They describe mechanisms. <bookmark mark='a'/>Here is chemical "
            "transmission at a synapse: a voltage change opens calcium channels, calcium triggers vesicles to fuse "
            "with the membrane, transmitter crosses the gap, and receptors on the far side open. "
            "<bookmark mark='b'/>Peter Machamer, Lindley Darden and Carl Craver defined a mechanism as entities and "
            "activities organized so as to produce regular changes. <bookmark mark='c'/>Wesley Salmon's causal-"
            "mechanical account had already said that explanation traces the causal processes that lead to an "
            "event. <bookmark mark='d'/>Most explanation in biology and neuroscience has this form. "
            "<bookmark mark='e'/>Which parts belong in the explanation? Craver's answer is Woodward's: a part is "
            "relevant if intervening on it changes the whole, and intervening on the whole changes it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.3),
                      LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), FadeIn(cap), run_time=2.5)
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def pseudo(self):
        head = label(r"Causal processes and pseudo-processes \ (Salmon, \ 1984)", font_size=28, color=CONN).to_edge(
            UP, buff=0.3)
        lamp = Dot([-5.4, -0.4, 0], color=GOAL, radius=0.14)
        wall_ = Arc(radius=5.0, start_angle=-0.55, angle=1.1, arc_center=lamp.get_center(), color=GREY_B,
                    stroke_width=4)
        th = ValueTracker(-0.45)
        beam = always_redraw(lambda: Line(lamp.get_center(), lamp.get_center() + 5.0 * np.array(
            [np.cos(th.get_value()), np.sin(th.get_value()), 0]), color=GOAL, stroke_width=2, stroke_opacity=0.6))
        spot = always_redraw(lambda: Dot(lamp.get_center() + 5.0 * np.array([np.cos(th.get_value()),
                                                                             np.sin(th.get_value()), 0]),
                                         color=GOAL, radius=0.12))
        wl = label(r"a distant wall", font_size=17, color=GREY_A).next_to(wall_, UP, buff=0.1)
        rows = stack([(r"a beam is a causal process: \ put a red filter in it, \ and the light stays red beyond",
                       OK),
                      (r"the spot is a pseudo-process: \ paint one spot red, \ and the next spot is white again", BAD),
                      (r"swing the lamp, \ and on a far enough wall the spot outruns light: \ relativity forbids "
                       r"only signals", THEORY),
                      (r"explanation traces processes that can transmit a mark", GOAL)], font_size=19,
                     aligned_edge=LEFT, width=6.0).move_to([3.4, -0.6, 0])
        with self.voiceover(
            "Wesley Salmon needed a way to say which processes are causal. <bookmark mark='a'/>A lamp sweeps its "
            "beam across a distant wall. The light travelling from lamp to wall is a causal process: put a red "
            "filter in the beam, and the light stays red all the way to the wall. <bookmark mark='b'/>The spot "
            "moving across the wall is a pseudo-process. Paint the wall red at one point, and the spot turns red "
            "there, but not at the next point: the mark is not carried along. <bookmark mark='c'/>On a far enough "
            "wall, the spot can move faster than light, and relativity is not violated, because nothing is "
            "transmitted from one spot to the next. <bookmark mark='d'/>Salmon's criterion: causal processes are "
            "those that can transmit a mark, and explanation traces them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lamp), Create(wall_), FadeIn(wl), FadeIn(beam), FadeIn(spot))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(th.animate.set_value(0.45), FadeIn(rows[1]), run_time=2)
            vo.wait_until("c")
            self.play(th.animate.set_value(-0.45), FadeIn(rows[2]), run_time=1)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
