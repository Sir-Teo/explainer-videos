from __future__ import annotations

from videos.economics.econ41.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.napkin()
        self.where()
        self.question()
        self.title()
        self.objectives()

    def napkin(self):
        N = load("napkin")
        cloth = RoundedRectangle(width=8.4, height=5.6, corner_radius=0.15, stroke_width=0, fill_color=NAPKIN,
                                 fill_opacity=1).move_to(LEFT * 1.6 + DOWN * 0.3)
        fold = DashedLine(cloth.get_top(), cloth.get_bottom(), color="#CFC6B1", stroke_width=1.5)
        o = cloth.get_corner(DL) + RIGHT * 0.9 + UP * 0.8
        W, H = 6.6, 3.9
        xax = Line(o, o + RIGHT * W, color=INK, stroke_width=3)
        yax = Line(o, o + UP * H, color=INK, stroke_width=3)
        t = np.array(N["t"])
        rev = np.array(N["rev"][1])
        pts = [o + RIGHT * W * a + UP * H * 3.2 * b for a, b in zip(t, rev)]
        curve = VMobject(stroke_color=INK, stroke_width=4).set_points_smoothly(pts[::4] + [pts[-1]])
        lx = label(r"\emph{tax rate}", font_size=24, color=INK).next_to(xax, DOWN, buff=0.15)
        ly = label(r"\emph{revenue}", font_size=24, color=INK).rotate(PI / 2).next_to(yax, LEFT, buff=0.15)
        z0 = label(r"0", font_size=22, color=INK).next_to(o, DOWN + LEFT, buff=0.08)
        z1 = label(r"100\%", font_size=22, color=INK).next_to(o + RIGHT * W, DOWN, buff=0.1)
        side = VGroup(
            label(r"1974, \ Washington: \\ Arthur Laffer, \ economist, \\ sketches for Dick Cheney, \\ then a "
                  r"White House aide", font_size=19, color=WHITE),
            label(r"a rate of zero raises nothing; \\ so does a rate of 100\%", font_size=19, color=REVENUE),
            label(r"the journalist Jude Wanniski \\ names it the Laffer curve", font_size=18, color=GREY_A),
            label(r"accounts differ on the date \\ and the guests; \ the napkin \\ in the Smithsonian may \\ be a "
                  r"later copy", font_size=16, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = published_tag(tables.LAFFER_1974.tag, corner=DR, font_size=11)
        with self.voiceover(
            "In 1974, at a restaurant in Washington, the economist Arthur Laffer took a pen to a napkin for Dick "
            "Cheney, then an aide in President Ford's White House. <bookmark mark='a'/> Across the bottom, the tax "
            "rate; up the side, the revenue it raises. <bookmark mark='b'/> At a rate of zero the government "
            "collects nothing. At a rate of one hundred percent it also collects nothing, because no one will earn "
            "income that is all taken away. In between, revenue must rise and then fall. <bookmark mark='c'/> The "
            "journalist Jude Wanniski, who had arranged the meeting, called it the Laffer curve, and it became the "
            "emblem of the tax cuts of the 1980s. <bookmark mark='d'/> The details are disputed: who was there, "
            "and when; the cloth napkin in the Smithsonian may have been drawn years later. The curve itself is not."
        ) as vo:
            self.play(FadeIn(cloth), FadeIn(fold), FadeIn(tag), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(xax), Create(yax), FadeIn(lx), FadeIn(ly), FadeIn(z0), FadeIn(z1))
            vo.wait_until("b")
            self.play(Create(curve), FadeIn(side[1]), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def where(self):
        N = load("napkin")
        ax = plane([0, 1], [0, 0.6], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 0.2, 0.4, 0.6], xlabel=r"tax rate",
                   ylabel=r"revenue, \ per unit of the untaxed base", xfmt=lambda v: f"{100 * v:.0f}\\%",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        cols = (REVENUE, LOSS)
        curves = VGroup(*[path(ax, N["t"], r, c, 3.4) for r, c in zip(N["rev"], cols)])
        peaks = VGroup(*[VGroup(vline(ax, p, 0, pr, c), dot(ax, p, pr, c, 0.08))
                         for p, pr, c in zip(N["peak"], N["peak_rev"], cols)])
        eq = MathTex(r"R(t) = t\,(1 - t)^{e} \quad\Rightarrow\quad t^{*} = \frac{1}{1 + e}", font_size=34).to_edge(
            UP, buff=0.35)
        side = VGroup(
            label(rf"gold: \ the base shrinks \\ slowly, \ $e$ = {N['e'][0]:g}; \\ the top at "
                  rf"{100 * N['peak'][0]:.0f}\%", font_size=19, color=REVENUE),
            label(rf"red: \ it shrinks fast, \\ $e$ = {N['e'][1]:g}; \ the top \\ at {100 * N['peak'][1]:.0f}\%",
                  font_size=19, color=LOSS),
            label(r"the napkin cannot \\ say which", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The curve is correct. The question it cannot answer is where its top is. Suppose the taxed income "
            "shrinks as the rate rises, with an elasticity e of income to the share people keep. "
            f"<bookmark mark='a'/> If income responds weakly, e equal to {N['e'][0]:g}, revenue keeps rising until "
            f"the rate reaches {100 * N['peak'][0]:.0f} percent. <bookmark mark='b'/> If it responds strongly, e "
            f"equal to one, the top comes at {100 * N['peak'][1]:.0f} percent. <bookmark mark='c'/> Everything "
            "depends on a number the napkin does not contain: how much people change what they earn, or report, "
            "when the rate changes. Much of this part is about that number."
        ) as vo:
            self.play(Write(eq), FadeIn(ax), FadeIn(tag), Create(curves[0]), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(peaks[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(curves[1]), FadeIn(peaks[1]), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 38, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"who bears a tax, \ whoever hands over the money?", font_size=26, color=WORKER),
            label(r"why does a tax's cost grow faster than the tax?", font_size=26, color=LOSS),
            label(r"how high should the top rate be, \ and why does the answer need only three numbers?",
                  font_size=26, color=TOP),
            label(r"how do people respond, \ by working, \ relabelling, \ moving and hiding?", font_size=26,
                  color=RATE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "This part asks who really pays a tax, and how high the top rate should be. <bookmark mark='a'/> Who "
            "bears a tax, whoever hands over the money? <bookmark mark='b'/> Why does a tax's cost grow faster than "
            "the tax? <bookmark mark='c'/> How high should the top rate be, and why does the answer need only three "
            "numbers? <bookmark mark='d'/> And how do people respond: by working less, by relabelling income, by "
            "moving, by hiding it?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([1913, 2025], [0, 100], x_length=4.2, y_length=1.4)
        logo = path(mini, F["t"], F["v"], RATE, 2.6, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 41 \ $\cdot$ \ Taxes", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part forty-one: taxes."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act VIII \ $\cdot$ \ Work and the State", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"incidence in general equilibrium; \ the cost of a tax; \ a game",
            r"Ramsey's rule; \ Mirrlees's problem; \ the top rate derived; \ the whole schedule",
            r"measuring the elasticity; \ bunching; \ salience",
            r"capital, \ corporations and havens; \ evasion",
            r"three dials; \ scoring a tax change; \ the frontier",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> Who bears the corporate tax, why a tax's cost grows with its "
            "square, and a game. <bookmark mark='b'/> Then the theory of optimal taxes: Ramsey's rule for goods, "
            "Mirrlees's problem for incomes, the top rate derived, and the shape of the whole schedule. "
            "<bookmark mark='c'/> How the key elasticity is measured, by panels, by bunching at kinks, and why "
            "visibility matters. <bookmark mark='d'/> Capital, corporations, tax havens and evasion. "
            "<bookmark mark='e'/> Three dials, how a tax change is scored, and the frontier."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
