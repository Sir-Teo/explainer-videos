from __future__ import annotations

from videos.philosophy.philosophy21.common import *  # noqa: F403


def worldtube(ax, xs, ts, width, color, opacity=0.35):
    """A spacetime worm: the region swept by an object of given width along a path x(t)."""
    left = [ax.c2p(x - width / 2, t) for x, t in zip(xs, ts)]
    right = [ax.c2p(x + width / 2, t) for x, t in zip(xs, ts)]
    return Polygon(*left, *right[::-1], color=color, fill_opacity=opacity, stroke_width=2)


class Persistence(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Endurance, perdurance, stages", r"How does a thing persist through time?",
                            lit=(1986, 2001), part=PART)
        with self.voiceover("Chapter seven. Endurance, perdurance, stages."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.three()
        self.arguments()
        self.disc()
        self.time()

    def three(self):
        head = label(r"Three pictures of persistence", font_size=30, color=CONN).to_edge(UP, buff=0.25)
        panels = VGroup()
        ts = np.linspace(0, 4, 41)
        xs = 0.5 * np.sin(ts * 0.9)
        titles = [(r"endurance", NOM), (r"perdurance", WHOLE), (r"stage theory", PARTC)]
        for k, (t, col) in enumerate(titles):
            ax = Axes(x_range=[-1.5, 1.5, 1], y_range=[0, 4.2, 1], x_length=3.0, y_length=3.6,
                      axis_config={"color": GREY_D, "include_ticks": False}).move_to([-4.6 + 4.6 * k, -0.4, 0])
            xl = label(r"space", font_size=13, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.05)
            tl = label(r"time", font_size=17, color=GREY_A).next_to(ax.y_axis, UP, buff=0.05)
            ttl = label(t, font_size=21, color=col).next_to(ax, UP, buff=0.35)
            body = VGroup()
            if k == 0:
                for t_ in (0.5, 1.5, 2.5, 3.5):
                    i = int(t_ * 10)
                    body.add(Dot(ax.c2p(xs[i], t_), radius=0.16, color=col))
                body.add(*[DashedLine(ax.c2p(xs[int(a * 10)], a), ax.c2p(xs[int(b * 10)], b), color=col,
                                      stroke_width=1.5) for a, b in ((0.5, 1.5), (1.5, 2.5), (2.5, 3.5))])
                cap = label(r"wholly present at each time", font_size=18, color=GREY_A)
            elif k == 1:
                body.add(worldtube(ax, xs, ts, 0.5, col))
                body.add(*[Line(ax.c2p(xs[int(t_ * 10)] - 0.25, t_), ax.c2p(xs[int(t_ * 10)] + 0.25, t_),
                                color=WHITE, stroke_width=1.5) for t_ in (1.0, 2.0, 3.0)])
                cap = label(r"a 4D worm with temporal parts", font_size=18, color=GREY_A)
            else:
                body.add(worldtube(ax, xs, ts, 0.5, GREY_D, opacity=0.15))
                i = 25
                body.add(Line(ax.c2p(xs[i] - 0.3, 2.5), ax.c2p(xs[i] + 0.3, 2.5), color=col, stroke_width=6))
                body.add(Arrow(ax.c2p(0.9, 2.5), ax.c2p(xs[i] + 0.35, 2.5), buff=0.05, color=col, stroke_width=2,
                               max_tip_length_to_length_ratio=0.25))
                cap = wrapped_label(r"you are this stage; \ the others are your counterparts", 4.0, 18, GREY_A)
            cap.next_to(ax, DOWN, buff=0.3)
            panels.add(VGroup(ax, xl, tl, ttl, body, cap))
        with self.voiceover(
            "How does a thing persist? Draw time vertically and space horizontally. <bookmark mark='a'/>Endurantists "
            "say an object is wholly present at each moment of its existence: the same whole thing, at every time. "
            "<bookmark mark='b'/>Perdurantists say it persists the way a road extends through space, by having parts "
            "at different times. You are a four-dimensional worm, and the you of this moment is a temporal slice of it. "
            "<bookmark mark='c'/>Stage theorists, such as Ted Sider and Katherine Hawley, agree that there are "
            "worms but say that what we name and count are the momentary stages, which persist by having counterparts "
            "at other times."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(VGroup(p[0], p[1], p[2], p[3])) for p in panels])
            for mk, p in zip("abc", panels):
                vo.wait_until(mk)
                self.play(FadeIn(p[4]), FadeIn(p[5]))
        self.clear_scene()

    def arguments(self):
        head = label(r"Arguments for worms", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"relativity", r"there is no absolute present to be wholly present in; \ spacetime is four-dimensional "
                            r"\ (Part 25)", UNIV),
            (r"vagueness", r"Sider \ (2001): \ the argument from vagueness \ (Part 20) \ applied over time gives "
                           r"temporal parts", ABS),
            (r"coincidence", r"the statue and the lump share a stage, \ not a worm: \ no two things in one place",
             WHOLE),
            (r"against", r"change: \ if only stages differ, \ does anything change? \ and Kripke's spinning disc", BAD),
            (r"the stakes", r"fission, \ chapter eleven, \ looks very different with worms", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "Why believe in worms? <bookmark mark='a'/>Relativity: there is no absolute present moment for a thing "
            "to be wholly present in, and spacetime is four-dimensional, as Part 25 will show. "
            "<bookmark mark='b'/>Sider ran Part 20's argument from vagueness over time: if things lose and gain parts "
            "gradually, unrestricted composition over time gives temporal parts. <bookmark mark='c'/>Coincidence: the "
            "statue and the lump can be two worms sharing a stage, so there are never two things in one place at "
            "once. <bookmark mark='d'/>Against worms: if only stages have properties, does anything really change? "
            "And Saul Kripke's spinning disc, perfectly uniform, seems to distinguish a rotating worm from a still one "
            "with exactly the same stages. "
            "<bookmark mark='e'/>The choice will matter for fission."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def disc(self):
        head = label(r"Kripke's spinning disc", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        panels = VGroup()
        for k, (title, spin) in enumerate(((r"still", False), (r"spinning", True))):
            cx = -4.9 + 3.0 * k
            tube = Rectangle(width=2.0, height=3.6, color=WHOLE, fill_opacity=0.2).move_to([cx, -0.4, 0])
            lines = VGroup()
            for j in range(5):
                x0 = cx - 0.8 + 0.4 * j
                if spin:
                    pts = [np.array([cx - 1.0 + ((x0 - (cx - 1.0)) + 0.5 * t) % 2.0, -2.2 + t, 0])
                           for t in np.linspace(0, 3.6, 60)]
                    segs = VGroup()
                    for a, b in zip(pts[:-1], pts[1:]):
                        if b[0] > a[0]:
                            segs.add(Line(a, b, color=PARTC, stroke_width=2))
                    lines.add(segs)
                else:
                    lines.add(Line([x0, -2.2, 0], [x0, 1.4, 0], color=PARTC, stroke_width=2))
            tl = label(title, font_size=20, color=WHOLE).next_to(tube, UP, buff=0.15)
            panels.add(VGroup(tube, lines, tl))
        tlab = label(r"time", font_size=18, color=GREY_A).move_to([-6.55, 1.4, 0])
        rows = stack([(r"a perfectly uniform disc: \ every stage looks the same, \ spinning or not", WHITE),
                      (r"yet spinning and still differ \ (hold a pen to the edge)", GOAL),
                      (r"the lines: \ which part of the disc is where, \ at each time", PARTC),
                      (r"the worm theorist needs those lines to be more than the stages: \ relations between parts "
                       r"across time", BAD)], font_size=21, aligned_edge=LEFT, width=7.2).move_to([3.1, -0.4, 0])
        with self.voiceover(
            "Saul Kripke's spinning disc is a test for worms. <bookmark mark='a'/>Take a perfectly uniform disc. "
            "Every momentary stage of it looks exactly the same, whether it is spinning or still. "
            "<bookmark mark='b'/>Yet surely spinning and being still are different. <bookmark mark='c'/>The "
            "difference lies in which part of the disc is where at each moment: the lines through the worm, straight "
            "for the still disc, winding for the spinning one. <bookmark mark='d'/>So the worm theorist needs more "
            "than a series of stages: facts about which later parts continue which earlier ones, relations that "
            "reach across time. Defenders reply that such facts can be grounded in causal connections between stages."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tlab), *[FadeIn(VGroup(p_[0], p_[2])) for p_ in panels])
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(panels[0][1]), Create(panels[1][1]), FadeIn(rows[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def time(self):
        head = label(r"Persistence needs a theory of time", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"presentism", r"only the present exists: \ endurance is natural, \ and there are no past stages to "
                            r"be parts", NOM),
            (r"growing block", r"past and present exist, \ the future does not \ (Broad, \ 1923)", WHOLE),
            (r"eternalism", r"all times are equally real: \ the natural home of worms", UNIV),
            (r"the pairings", r"not forced: \ an eternalist can be an endurantist, \ though presentist worms are "
                              r"strained", GREY_A),
            (r"onward", r"McTaggart, \ the A- and B-series \ (Part 24); \ relativity of simultaneity \ (Part 25)", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "How a thing persists depends on what time is. <bookmark mark='a'/>Presentists hold that only the present "
            "exists. Endurance is natural for them, since there are no past stages to be parts of anything. "
            "<bookmark mark='b'/>The growing block, from C. D. Broad: the past and present exist, and the future does "
            "not yet. <bookmark mark='c'/>Eternalists hold all times equally real, the natural home of worms. "
            "<bookmark mark='d'/>The pairings are not forced; an eternalist can still be an endurantist. "
            "<bookmark mark='e'/>McTaggart's argument and the two series of times are the subject of Part 24, and "
            "relativity's verdict on simultaneity of Part 25."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
