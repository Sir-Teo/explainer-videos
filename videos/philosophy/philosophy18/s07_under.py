from __future__ import annotations

from videos.philosophy.philosophy18.common import *  # noqa: F403


class Under(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Underdetermination", r"Can the evidence ever settle which theory is true?",
                            lit=(1906, 1951), part=PART)
        with self.voiceover("Chapter six. Underdetermination."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.newton()
        self.duhem()
        self.quine()

    def newton(self):
        d = load("twins")
        head = label(r"Newton's absolute space: \ two worlds, \ one set of observations", font_size=28,
                     color=CONN).to_edge(UP, buff=0.3)
        pr, pm = d["path_rest"], d["path_moving"]
        xmax = max(p[0] for p in pm) + 1
        ax1 = Axes(x_range=[-2, 2, 1], y_range=[-1.5, 1.5, 1], x_length=3.2, y_length=2.4,
                   axis_config={"color": GREY_D, "include_ticks": False}).move_to([-4.6, 1.0, 0])
        ax2 = Axes(x_range=[-2, xmax, 5], y_range=[-1.5, 1.5, 1], x_length=7.0, y_length=2.4,
                   axis_config={"color": GREY_D, "include_ticks": False}).move_to([2.6, 1.0, 0])
        p1 = series_plot(ax1, [p[1] for p in pr], REAL, xs=[p[0] for p in pr])
        p2 = series_plot(ax2, [p[1] for p in pm], ANTI, xs=[p[0] for p in pm])
        l1 = label(r"centre of mass at rest", font_size=18, color=REAL).next_to(ax1, UP, buff=0.1)
        l2 = label(r"the same system moving at $v = " + f"{d['v']:.1f}" + r"$", font_size=18, color=ANTI).next_to(
            ax2, UP, buff=0.1)
        ax3 = Axes(x_range=[0, len(d["sep"]), 10], y_range=[0, max(d["sep"]) * 1.1, 1], x_length=6.0, y_length=1.6,
                   axis_config={"color": GREY_D, "include_ticks": False}).move_to([-1.6, -1.6, 0])
        sep = series_plot(ax3, d["sep"], GOAL, width=4)
        sl = label(r"what anyone inside can measure: \ the separation \ (the same in both worlds)", font_size=18,
                   color=GOAL).next_to(ax3, DOWN, buff=0.15)
        side = stack([(r"Newton: \ absolute space exists", REAL),
                      (r"theory $T_v$: \ the solar system moves at $v$; \ one theory for every $v$", GREY_A),
                      (r"every $T_v$ predicts the same observations: \ Galilean invariance", BAD),
                      (r"empirically equivalent, \ yet incompatible", GOAL)], font_size=19, aligned_edge=LEFT,
                     width=4.6).move_to([4.6, -1.8, 0])
        with self.voiceover(
            "Underdetermination is the thesis that evidence cannot settle which of several rival theories is true. "
            "Newton supplied the cleanest example himself. <bookmark mark='a'/>He believed in absolute space. Here "
            "is a pair of bodies in orbit, their centre of mass at absolute rest. <bookmark mark='b'/>And here is "
            "the same system moving through absolute space at a constant velocity. "
            "<bookmark mark='c'/>The Reasoner integrates both. Everything an observer inside could measure, such "
            "as the distance between the bodies, is the same in both worlds, step for step. "
            "<bookmark mark='d'/>So there is a family of theories, one for each absolute velocity, all making the "
            "same predictions, and incompatible with one another. <bookmark mark='e'/>Bas van Fraassen made this "
            "his central example: empirically equivalent, yet they cannot all be true."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax1), FadeIn(l1), FadeIn(side[0]))
            self.play(Create(p1), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(ax2), FadeIn(l2), FadeIn(side[1]))
            self.play(Create(p2), run_time=2)
            vo.wait_until("c")
            self.play(Create(ax3), Create(sep), FadeIn(sl))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def duhem(self):
        d = load("duhem")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert sorted(map(tuple, d["mcs"])) == [("A1",), ("A2",), ("A3",), ("E",), ("H",)]

        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.9, width=3.4, font_size=19,
                       center=[0, -0.5, 0], title=r"The Duhem problem: \ faster-than-light neutrinos")
        positions = [(("H",), r"some theorists", r"relativity fails for neutrinos: \ dozens of papers in weeks"),
                     (("E",), r"ICARUS \ (2012)", r"the same beam, \ another detector: \ no anomaly"),
                     (("A2",), r"OPERA \ (2012)", r"a loose fibre-optic connector: \ the auxiliary gave way")]
        with self.voiceover(
            "Pierre Duhem saw in 1906 that experiments never test a hypothesis alone. <bookmark mark='a'/>In 2011 "
            "the OPERA experiment timed neutrinos travelling seven hundred and thirty kilometres from CERN to Gran "
            "Sasso, and found them arriving sixty nanoseconds early: faster than light. The prediction followed from "
            "relativity only together with auxiliary assumptions: that the clocks agree, that the timing cable is "
            "sound, that the distance is right. <bookmark mark='b'/>The five claims are inconsistent, and the "
            "Reasoner finds that dropping any one of them restores consistency. Logic alone cannot say which. "
            "<bookmark mark='c'/>Some theorists rejected relativity, at least for neutrinos. "
            "<bookmark mark='d'/>The ICARUS detector measured the same beam and found no anomaly. "
            "<bookmark mark='e'/>And in 2012 OPERA found the culprit: a loose fibre-optic connector in its timing "
            "system. An auxiliary assumption had failed, not relativity."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cde", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()

    def quine(self):
        head = label(r"The web of belief", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rings = VGroup(*[Circle(radius=r, color=c, stroke_width=2.5) for r, c in
                         ((0.7, THEORY), (1.4, REAL), (2.1, DATA))]).move_to([-3.8, -0.6, 0])
        rl = VGroup(label(r"logic", font_size=16, color=THEORY).move_to(rings.get_center()),
                    label(r"theory", font_size=16, color=REAL).move_to(rings.get_center() + UP * 1.05),
                    label(r"observation", font_size=16, color=DATA).move_to(rings.get_center() + UP * 1.75))
        hit = Arrow(rings.get_center() + np.array([2.9, 1.6, 0]), rings.get_center() + np.array([1.55, 0.8, 0]),
                    color=BAD, buff=0, stroke_width=4)
        rows = [
            (r"Quine \ (1951)", r"`our statements about the external world face the tribunal of sense experience "
                                r"not individually but only as a corporate body'", REAL),
            (r"the strong thesis", r"any statement can be held true come what may, \ if we make drastic enough "
                                   r"adjustments elsewhere", BAD),
            (r"the reply", r"Laudan and Leplin \ (1991): \ equivalent rivals are rare, \ and evidence can bear on "
                           r"theories indirectly", OK),
            (r"the new worry", r"Stanford \ (2006): \ unconceived alternatives: \ historically, \ the rival was one "
                               r"no one had thought of", GOAL),
        ]
        g = rows_table(rows, top=1.5, gap=0.5, width=5.4, x_label=-1.0, x_text=1.4, label_size=20, text_size=19)
        with self.voiceover(
            "W. V. Quine generalized Duhem's point. <bookmark mark='a'/>Our statements about the world face the "
            "tribunal of experience not one by one, but as a corporate body: a web whose centre is logic and "
            "mathematics and whose edge touches observation. <bookmark mark='b'/>A recalcitrant experience can be "
            "accommodated by adjusting anything, and any statement can be held true come what may, if we make "
            "drastic enough changes elsewhere. <bookmark mark='c'/>Larry Laudan and Jarrett Leplin replied that "
            "genuinely equivalent rivals are rare, and that evidence can bear on a theory indirectly, through the "
            "larger theories it belongs to. <bookmark mark='d'/>Kyle Stanford gave the worry a historical form: "
            "again and again, the rival that replaced a theory was one that no one had yet conceived."
        ) as vo:
            self.play(FadeIn(head), Create(rings), FadeIn(rl))
            vo.wait_until("a")
            self.play(FadeIn(g[0]))
            vo.wait_until("b")
            self.play(GrowArrow(hit), FadeIn(g[1]), rings[1].animate.set_color(BAD))
            for mk, r in zip("cd", g[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
