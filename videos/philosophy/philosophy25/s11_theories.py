from __future__ import annotations

from videos.philosophy.philosophy25.common import *  # noqa: F403


class Theories(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"What exists: \ now, \ or always?", r"Does relativity refute presentism?",
                            lit=(1966, 1967), part=PART)
        with self.voiceover("Chapter ten. What exists: now, or always?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.pictures()
        self.passage()
        self.rp()
        self.replies()

    def picture(self, cx, kind):
        w, h = 2.6, 3.2
        y0 = -0.5
        frame = Rectangle(width=w, height=h, color=GREY_D, stroke_width=1.5).move_to([cx, y0, 0])
        now_y = y0 + 0.1
        g = VGroup(frame)
        if kind in ("block", "spotlight"):
            g.add(Rectangle(width=w, height=h, stroke_width=0, fill_color=SPACE, fill_opacity=0.25).move_to(
                [cx, y0, 0]))
        if kind == "growing":
            g.add(Rectangle(width=w, height=now_y - (y0 - h / 2), stroke_width=0, fill_color=SPACE,
                            fill_opacity=0.25).move_to([cx, (now_y + y0 - h / 2) / 2, 0]))
        if kind in ("presentism", "growing", "spotlight"):
            g.add(Line([cx - w / 2, now_y, 0], [cx + w / 2, now_y, 0], color=LIGHT, stroke_width=5))
        if kind == "spotlight":
            g.add(Rectangle(width=w, height=0.35, stroke_width=0, fill_color=LIGHT, fill_opacity=0.35).move_to(
                [cx, now_y, 0]))
        return g

    def pictures(self):
        head = label(r"Four pictures of time", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        kinds = [("presentism", r"presentism", r"only the present exists"),
                 ("growing", r"the growing block", r"past and present exist; \ the future does not, \ yet"),
                 ("spotlight", r"the moving spotlight", r"everything exists; \ the present is lit, \ and moves"),
                 ("block", r"eternalism", r"everything exists; \ `now' is like `here'")]
        ps, caps = VGroup(), VGroup()
        for (k, n, cap), cx in zip(kinds, (-5.1, -1.7, 1.7, 5.1)):
            p = self.picture(cx, k)
            ps.add(p)
            caps.add(VGroup(label(n, font_size=20, color=SPACE), wrapped_label(cap, 3.0, 16, GREY_A)).arrange(
                DOWN, buff=0.08).next_to(p, DOWN, buff=0.2))
        tl = label(r"time runs up; \ blue: \ what exists; \ gold: \ the present", font_size=18,
                   color=GREY_A).next_to(head, DOWN, buff=0.2)
        with self.voiceover(
            "McTaggart's debate became a debate about what exists. Draw time running up the page; shade what is "
            "real. <bookmark mark='a'/>Presentism: only the present exists. Dinosaurs did exist, but there are none. "
            "<bookmark mark='b'/>The growing block: the past and the present exist, the future does not yet, and "
            "reality grows as time passes. <bookmark mark='c'/>The moving spotlight: every time exists, but one is "
            "objectively present, lit up, and the light moves. <bookmark mark='d'/>Eternalism, the block universe: "
            "every time exists equally, and now picks out a time the way here picks out a place. The first three "
            "are A-theories; the last is the B-theory's natural home."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tl))
            for mk, i in zip("abcd", range(4)):
                vo.wait_until(mk)
                self.play(FadeIn(ps[i]), FadeIn(caps[i]))
        self.clear_scene()

    def passage(self):
        head = label(r"How fast does time pass?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        f = MathTex(r"\frac{\text{one second}}{\text{per second}} \;=\; 1 \;?", font_size=44,
                    color=LIGHT).move_to([0, 1.6, 0])
        rows = [
            (r"the objection", r"if time passes, \ at what rate? \ a rate is change per unit time: \ one second per "
                               r"second is no rate at all \ (Smart, \ 1949; \ Price)", BAD),
            (r"Maudlin's reply", r"exchange rates can be one dollar per dollar; \ passage is basic, \ and needs no "
                                 r"second time", OK),
            (r"the experience", r"we seem to feel time flowing; \ perhaps that feeling is like the phi phenomenon, \ "
                                r"an illusion of motion \ (L. A. Paul)", ABS),
            (r"the stakes", r"for the block, \ passage is in us; \ for the A-theorist, \ it is the most basic fact "
                            r"there is", GOAL),
        ]
        g = rows_table(rows, top=0.6, gap=0.45, width=8.8, x_text=-2.6, label_size=22, text_size=20)
        with self.voiceover(
            "Before relativity enters, a classic puzzle for the A-theories. <bookmark mark='a'/>If time really passes, "
            "how fast does it pass? A rate is change per unit of time, so the answer seems to be one second per "
            "second, which J. J. C. Smart and Huw Price argue is no rate at all. <bookmark mark='b'/>Tim Maudlin "
            "replies that there is nothing wrong with a rate of one: the exchange rate of a dollar for a dollar is "
            "perfectly good, and passage is a basic fact that needs no second time to measure it. "
            "<bookmark mark='c'/>Then there is experience. We seem to feel time flowing. L. A. Paul has suggested "
            "that the feeling is like the phi phenomenon, in which two flashes in quick succession look like one "
            "moving light: an illusion of motion that the brain constructs. <bookmark mark='d'/>For the block "
            "theorist, passage is in us. For the A-theorist, it is the most basic fact there is."
        ) as vo:
            self.play(FadeIn(head), Write(f))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def rp(self):
        d = load("rp")
        head = label(r"Rietdijk and Putnam", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        o = np.array([-2.8, -0.9, 0])
        s = 1.6
        P = lambda t, x: o + s * np.array([x, t, 0])  # noqa: E731
        axes = VGroup(Arrow(P(0, -2.0), P(0, 2.4), buff=0, color=GREY_B, stroke_width=2),
                      Arrow(P(-1.2, 0), P(2.4, 0), buff=0, color=GREY_B, stroke_width=2))
        cone = VGroup(DashedLine(P(-1.2, -1.2), P(2.1, 2.1), color=LIGHT), DashedLine(P(-1.2, 1.2), P(2.1, -2.1),
                                                                                       color=LIGHT))
        me = Dot(P(0, 0), radius=0.1, color=MATTER)
        mel = label(r"me, \ here-now", font_size=18, color=MATTER).next_to(me, DOWN + LEFT, buff=0.1)
        t_e, x_e = d["event"]
        E = Dot(P(t_e, x_e), radius=0.1, color=CURVE)
        El = label(r"$E$: \ outside my light cone", font_size=18, color=CURVE).next_to(E, RIGHT, buff=0.15)
        my_now = Line(P(0, -2.0), P(0, 2.4), color=TIME, stroke_width=3)
        v = d["v"]
        their_now = Line(P(-2.0 * v, -2.0), P(2.4 * v, 2.4), color=LIGHT, stroke_width=3)
        their_l = label(rf"the `now' of an observer passing me at $v = {v:.1f}\,c$", font_size=18,
                        color=LIGHT).next_to(P(2.4 * v, 2.4), UP, buff=0.1)
        rows = stack([(r"1. \ what is present for me is real for me", WHITE),
                      (r"2. \ what is real for anyone real for me is real for me \ (transitivity)", ABS),
                      (rf"3. \ for an observer here-now at ${v:.1f}\,c$, \ $E$ is present: \ the Reasoner's boost "
                       rf"gives $t' = 0$", LIGHT),
                      (r"4. \ so $E$ is real; \ repeat, \ and every event is real: \ eternalism", BAD)],
                     font_size=20, aligned_edge=LEFT, width=6.0, buff=0.3).move_to([3.6, -0.5, 0])
        assert d["spacelike"] and abs(d["t_prime"]) < 1e-9
        with self.voiceover(
            "In 1966 C. W. Rietdijk, and in 1967 Hilary Putnam, argued that relativity refutes presentism. "
            "<bookmark mark='a'/>Take me, here and now, and an event E, outside my light cone: a little in my future "
            "by my clocks, but too far away for any signal to connect us. <bookmark mark='b'/>Suppose, first, that "
            "what is present for me is real. <bookmark mark='c'/>Second, that whatever is real for someone who is "
            "real for me is real for me. <bookmark mark='d'/>Now an observer passes me at six tenths of the speed of "
            "light. Their slice of simultaneity tilts, and the Reasoner's Lorentz boost puts E exactly in their "
            "present. That observer is here-now with me, so is real for me; E is present for them; so E is real. "
            "<bookmark mark='e'/>Repeat with other observers and other events, and every event in spacetime turns out "
            "to be real. Presentism collapses into the block."
        ) as vo:
            self.play(FadeIn(head), GrowArrow(axes[0]), GrowArrow(axes[1]), Create(cone))
            vo.wait_until("a")
            self.play(FadeIn(me), FadeIn(mel), FadeIn(E), FadeIn(El))
            vo.wait_until("b")
            self.play(Create(my_now), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(Create(their_now), FadeIn(their_l), FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def replies(self):
        head = label(r"The presentist's replies", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"deny transitivity", r"Stein \ (1968): \ only the here-now is present; \ `real for me' is not transitive",
             SPACE),
            (r"a hidden frame", r"one frame's simultaneity is the true one, \ undetectable: \ a neo-Lorentzian "
                                r"relativity", LIGHT),
            (r"cosmic time", r"in our expanding universe, \ the frame at rest relative to the cosmic background", TIME),
            (r"the cost", r"each adds structure relativity's laws do not use: \ chapter 6's principle counts "
                          r"against it", BAD),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.6, x_text=-2.4, label_size=22, text_size=21)
        with self.voiceover(
            "Presentists have replies. <bookmark mark='a'/>Howard Stein argued in 1968 that in relativity only the "
            "here-now is present, and that being real for me is not transitive; but that leaves almost nothing real. "
            "<bookmark mark='b'/>Others posit a hidden preferred frame, whose simultaneity is the true one though no "
            "experiment can detect it: a neo-Lorentzian version of relativity. <bookmark mark='c'/>Or they point to "
            "cosmic time: in our expanding universe, the frame at rest relative to the cosmic microwave background "
            "is natural. <bookmark mark='d'/>The cost of each is the same: it adds structure that relativity's laws "
            "do not use, exactly what chapter six's principle counts against. That is a main reason why many "
            "philosophers of physics are eternalists."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
