from __future__ import annotations

from videos.philosophy.philosophy26.common import *  # noqa: F403


class Bohm(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Bohmian mechanics", r"What if the particles were there all along?",
                            lit=(1952,), part=PART)
        with self.voiceover("Chapter eleven. Bohmian mechanics."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.theory()
        self.trajectories()
        self.which_slit()
        self.nonlocal_()

    def theory(self):
        hc = history_card(1952, r"David Bohm", r"`A Suggested Interpretation of the Quantum Theory in Terms of "
                          r"\textit{Hidden} Variables'", width=7.0, color=HIST).to_corner(UL, buff=0.3)
        f1 = MathTex(r"i\hbar\,\partial_t \psi = H\psi", font_size=36, color=WAVE).move_to([-3.0, 0.8, 0])
        f2 = MathTex(r"\frac{dX_k}{dt} = \frac{\hbar}{m_k}\,\operatorname{Im}\frac{\nabla_k \psi}{\psi}(X_1, \dots, "
                     r"X_N)", font_size=34, color=PART_C).move_to([2.6, 0.8, 0])
        l1 = label(r"the wave: \ never collapses", font_size=19, color=WAVE).next_to(f1, DOWN, buff=0.25)
        l2 = label(r"the particles: \ guided by the wave", font_size=19, color=PART_C).next_to(f2, DOWN, buff=0.25)
        rows = stack([(r"particles always have positions; \ the wavefunction tells them how to move", WHITE),
                      (r"if positions start distributed as $|\psi|^2$, \ they stay so: \ the Born rule, \ "
                       r"from ignorance of where they are", ABS),
                      (r"de Broglie had the idea in 1927; \ Bohm made it a theory in 1952", HIST)], font_size=21,
                     aligned_edge=LEFT, width=11.0, buff=0.28).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In 1952 David Bohm showed that the thing von Neumann was thought to have proved impossible could be done. "
            "<bookmark mark='a'/>Keep the wavefunction and Schrödinger's equation, with no collapse ever. "
            "<bookmark mark='b'/>Add particles that always have definite positions, and give them an equation of "
            "motion: each particle's velocity is set by the wavefunction, evaluated at the actual positions of all "
            "the particles. <bookmark mark='c'/>The particles are the hidden variables, and the wave guides them. "
            "<bookmark mark='d'/>If the positions start out distributed according to psi squared, the dynamics keeps "
            "them that way, so the Born rule follows from ignorance of exactly where the particles are. "
            "<bookmark mark='e'/>Louis de Broglie had proposed a pilot wave in 1927; Bohm turned it into a full "
            "theory."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(f1), FadeIn(l1))
            vo.wait_until("b")
            self.play(Write(f2), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def trajectories(self):
        d = load("bohm")
        head = label(r"Two slits, \ with trajectories", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        x0, x1 = -5.8, 2.8                 # screen x for t = 0 and t = t_max
        ys = 0.26                          # screen units per unit of transverse position
        yc = -0.5
        ts = d["t"]
        tmax = ts[-1]

        def P(t, x):
            return np.array([x0 + (x1 - x0) * t / tmax, yc + ys * x, 0])

        barrier = VGroup(Line(P(0, -10.5), P(0, -d["slit"] - 0.9), color=GREY_B, stroke_width=6),
                         Line(P(0, -d["slit"] + 0.9), P(0, d["slit"] - 0.9), color=GREY_B, stroke_width=6),
                         Line(P(0, d["slit"] + 0.9), P(0, 10.5), color=GREY_B, stroke_width=6))
        paths = VGroup()
        for tr in d["traj"]:
            pts = [P(t, max(-10.5, min(10.5, x))) for t, x in zip(ts, tr)]
            paths.add(VMobject(stroke_color=PART_C, stroke_width=1.6, stroke_opacity=0.85).set_points_smoothly(pts))
        screen = Line(P(tmax, -10.5), P(tmax, 10.5), color=GREY_B, stroke_width=3)
        xs = d["x"]
        dens = d["density_final"]
        m = max(dens)
        profile = VMobject(stroke_color=WAVE, stroke_width=3).set_points_smoothly(
            [np.array([x1 + 0.15 + 1.6 * v / m, yc + ys * x, 0]) for x, v in zip(xs, dens)])
        pl = label(r"$|\psi|^2$ at the screen", font_size=18, color=WAVE).next_to(profile, UP, buff=0.1)
        side = stack([(r"the Reasoner integrates the guidance equation for 60 particles", PART_C),
                      (r"starting points sampled from $|\psi|^2$ at the slits", WHITE),
                      (r"they never cross, \ and bunch where $|\psi|^2$ is large: \ the fringes", OK)], font_size=19,
                     aligned_edge=LEFT, width=3.0, buff=0.3).move_to([5.6, -1.6, 0])
        assert d["never_cross"]
        with self.voiceover(
            "Here is the theory at work on the most famous experiment of all. <bookmark mark='a'/>A wave passes "
            "through two slits. Just past them, the wavefunction is two packets. <bookmark mark='b'/>The Reasoner "
            "samples sixty starting positions from psi squared at the slits, and integrates the guidance equation "
            "for each particle as the wave spreads and interferes. <bookmark mark='c'/>Each particle goes through "
            "one slit or the other, along a definite path. The paths wiggle as they pass through the interference "
            "pattern, never cross one another, and bunch up where psi squared is large. "
            "<bookmark mark='d'/>At the screen, their distribution reproduces the interference fringes. Each "
            "particle went through one slit; the wave went through both."
        ) as vo:
            self.play(FadeIn(head), Create(barrier), Create(screen))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.03), run_time=5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(profile), FadeIn(pl))
        self.clear_scene()

    def which_slit(self):
        d = load("bohm")
        head = label(r"Which slit?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        x0, x1, ys, yc = -6.0, 0.6, 0.2, -0.6
        ts = d["t"]
        tmax = ts[-1]

        def P(t, x):
            return np.array([x0 + (x1 - x0) * t / tmax, yc + ys * x, 0])

        up = [tr for tr in d["traj"] if tr[0] > 0]
        dn = [tr for tr in d["traj"] if tr[0] < 0]
        up_end = sum(tr[-1] > 0 for tr in up)
        dn_end = sum(tr[-1] < 0 for tr in dn)
        assert len(up) == len(dn) == 30 and up_end == 30 and dn_end == 30
        paths = VGroup()
        for tr, col in [(t_, CLASS) for t_ in up] + [(t_, ALICE) for t_ in dn]:
            pts = [P(t, max(-10.5, min(10.5, x))) for t, x in zip(ts, tr)]
            paths.add(VMobject(stroke_color=col, stroke_width=1.5, stroke_opacity=0.85).set_points_smoothly(pts))
        axis = DashedLine(P(0, 0), P(tmax, 0), color=GREY_B, dash_length=0.12)
        atag = label(r"the axis of symmetry", font_size=17, color=GREY_A).next_to(axis, DOWN, buff=0.08).align_to(
            axis, RIGHT)
        side = stack([(r"teal: \ started in the upper slit; \ orange: \ the lower", WHITE),
                      (rf"{up_end} of {len(up)} upper starters end above the axis; \ {dn_end} of {len(dn)} lower "
                       r"starters below", OK),
                      (r"so a hit on the upper half of the screen came through the upper slit", PART_C),
                      (r"Englert, \ Scully, \ Süssmann and Walther \ (1992): \ with which-path detectors, \ the "
                       r"trajectories look `surreal'", BAD),
                      (r"Dürr, \ Fusseder, \ Goldstein and Zanghì \ (1993): \ the detector records the wave's branch, "
                       r"\ not the particle's path", ABS),
                      (r"Kocsis et al. \ (2011): \ average photon trajectories, \ by weak measurement, \ with the "
                       r"same shape", HIST)], font_size=19, aligned_edge=LEFT, width=5.8, buff=0.24).move_to(
            [3.9, -0.5, 0])
        with self.voiceover(
            "The trajectories answer a question the standard theory refuses: which slit? <bookmark mark='a'/>Colour "
            "each path by the slit it came through. <bookmark mark='b'/>The Reasoner checks: every one of the thirty "
            "particles that started in the upper slit ends on the upper half of the screen, and every lower one on "
            "the lower half. Since paths never cross, and the axis of symmetry is itself a path, no particle crosses "
            "the middle. <bookmark mark='c'/>So a particle that lands high came through the upper slit. "
            "<bookmark mark='d'/>In 1992 Berthold-Georg Englert, Marlan Scully, Georg Süssmann and Herbert Walther "
            "added which-path detectors and called the result surreal: a particle can trigger the upper detector "
            "while travelling along the lower path. <bookmark mark='e'/>Bohmians replied, in 1993, that the detector "
            "records which branch of the wave the particle rides, not where the particle was; nothing measurable is "
            "wrong. <bookmark mark='f'/>And in 2011 Sacha Kocsis and colleagues in Toronto used weak measurements to "
            "reconstruct average photon trajectories through two slits. They have the same shape."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(atag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.02), FadeIn(side[0]), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def nonlocal_(self):
        head = label(r"The price, \ and the reward", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"non-locality", r"each particle's velocity depends on where all the others are, \ instantly, \ "
                              r"however far: \ Bell's theorem says it must", BAD),
            (r"a preferred frame", r"`instantly' needs a simultaneity: \ Bohm sits uneasily with relativity", BAD),
            (r"contextuality", r"spin `values' depend on the whole experimental arrangement \ (chapter 8)", ABS),
            (r"the reward", r"no measurement problem: \ outcomes are where the particles end up", OK),
            (r"Bell's admiration", r"`I saw the impossible done' \ (Bell, \ 1982)", HIST),
        ]
        g = rows_table(rows, top=1.7, gap=0.45, width=8.6, x_text=-2.4, label_size=22, text_size=21)
        with self.voiceover(
            "What does Bohm's theory cost? <bookmark mark='a'/>Non-locality: each particle's velocity depends on the "
            "positions of all the others, instantly, however far away. Bell's theorem says any theory with definite "
            "outcomes in one world must be like this. <bookmark mark='b'/>Instantly needs a notion of simultaneity, "
            "so the theory needs a preferred frame that relativity says is undetectable. <bookmark mark='c'/>And "
            "what looks like a spin value depends on the whole experimental arrangement. <bookmark mark='d'/>What it "
            "buys: no measurement problem at all. The outcome of an experiment is simply where the particles end up. "
            "<bookmark mark='e'/>Bell, who learned of it in 1952, wrote thirty years later: I saw the impossible done."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
