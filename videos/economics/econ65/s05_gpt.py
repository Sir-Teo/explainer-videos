from __future__ import annotations

from videos.economics.econ65.common import *  # noqa: F403


def factory(unit_drive: bool, w=5.0, h=3.0):
    """A factory floor seen from above.  Group drive: one engine turns a line shaft and every machine sits along it.
    Unit drive: each machine has its own motor, and the machines follow the work."""
    floor = Rectangle(width=w, height=h, stroke_color=GREY_B, stroke_width=2)
    g = VGroup(floor)
    if not unit_drive:
        eng = Square(side_length=0.6, stroke_color=NAIVE, fill_color=NAIVE, fill_opacity=0.5).move_to(
            floor.get_left() + RIGHT * 0.5)
        shaft = Line(eng.get_right(), floor.get_right() + LEFT * 0.2, color=GREY_A, stroke_width=4)
        ms = VGroup(*[Square(side_length=0.36, stroke_color=MACH, fill_color=MACH, fill_opacity=0.4).move_to(
            [eng.get_right()[0] + 0.5 + 0.55 * k, floor.get_center()[1] + (0.45 if k % 2 else -0.45), 0])
            for k in range(7)])
        belts = VGroup(*[Line(m.get_center(), [m.get_center()[0], floor.get_center()[1], 0], color=GREY_C,
                              stroke_width=1.5) for m in ms])
        g.add(shaft, belts, eng, ms)
    else:
        pts = [floor.get_left() + RIGHT * (0.5 + 0.62 * k) + UP * (0.8 * np.sin(k * 0.9)) for k in range(7)]
        flow = VMobject(stroke_color=GDP, stroke_width=2).set_points_smoothly(pts)
        ms = VGroup(*[Square(side_length=0.36, stroke_color=MACH, fill_color=MACH, fill_opacity=0.4).move_to(p)
                      for p in pts])
        motors = VGroup(*[Dot(m.get_corner(UR), radius=0.06, color=NEWT) for m in ms])
        g.add(flow, ms, motors)
    return g


class GPT(VoiceoverScene):
    def construct(self):
        card(self, 4, r"General-purpose technologies", r"Why does a technology that changes everything take decades "
             r"to show up in productivity?", "Chapter four. General-purpose technologies.",
             lit={1990: "David", 2021: "Brynjolfsson, Rock and Syverson"}, scale=("firm", "nation"),
             horizon=("a decade",))
        self.dynamo()
        self.jcurve()
        self.paradox()

    def dynamo(self):
        a = factory(False).move_to(LEFT * 3.4 + DOWN * 0.2)
        b = factory(True).move_to(RIGHT * 3.4 + DOWN * 0.2)
        la = label(r"group drive: \ the factory built around a shaft", font_size=18, color=GREY_A).next_to(
            a, UP, buff=0.25)
        lb = label(r"unit drive: \ the factory built around the work", font_size=18, color=GREY_A).next_to(
            b, UP, buff=0.25)
        nums = VGroup(label(r"1899: \ electric motors under 5\% of factory drive", font_size=19, color=NAIVE),
                      label(r"1929: \ about 78\%", font_size=19, color=NEWT)).arrange(DOWN, buff=0.15).to_edge(
            DOWN, buff=0.5)
        tag = published_tag(r"David, \ AER 80(2) (1990); \ Devine, \ Journal of Economic History 43(2) (1983)",
                            corner=DL, font_size=12)
        with self.voiceover(
            "Economists call technologies like electricity, the computer and now AI general-purpose technologies: "
            "they can be used almost everywhere, and they keep improving. Paul David asked in 1990 why the electric "
            "dynamo took so long to pay. <bookmark mark='a'/> In 1899, almost two decades after the first power "
            "stations, electric motors supplied under five percent of the mechanical drive in American factories. "
            "<bookmark mark='b'/> The old factory was built around a steam engine and a line shaft: every machine "
            "had to sit along the shaft, often on several floors. Swapping the engine for one big electric motor "
            "saved little. <bookmark mark='c'/> The gain came when each machine got its own small motor, and the "
            "factory could be laid out around the flow of the work, on one floor. That meant new buildings, new "
            "processes and new skills. <bookmark mark='d'/> By 1929, motors supplied about seventy-eight percent of "
            "the drive, and manufacturing productivity surged in the nineteen-twenties."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(nums[0]))
            vo.wait_until("b")
            self.play(FadeIn(a), FadeIn(la))
            vo.wait_until("c")
            self.play(FadeIn(b), FadeIn(lb))
            vo.wait_until("d")
            self.play(FadeIn(nums[1]))
        self.clear_scene()

    def jcurve(self):
        J = load("jcurve")
        t = np.array(J["t"])
        ax = plane([0, 30], [0.9, 1.16], center=LEFT * 1.4 + DOWN * 0.3, x_length=8.6, y_length=4.8,
                   xticks=[0, 5, 10, 15, 20, 25, 30], yticks=[0.92, 0.96, 1.0, 1.04, 1.08, 1.12, 1.16],
                   xlabel=r"years", ylabel=r"productivity, \ relative to the path without the technology",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}", font_size=14)
        base = seg(ax, 0, 1, 30, 1, GREY_C, 2.0, dashed=True)
        build = shade(ax, [(J["start"], J["start"] + J["build"])], 0.9, 1.16, RECESS, 0.45)
        blab = label(r"building intangible capital", font_size=15, color=GREY_A).move_to(
            ax.ax.c2p(J["start"] + J["build"] / 2, 1.15))
        m = path(ax, t, J["measured"], GDP, 3.2)
        tr = path(ax, t, J["true"], NEWT, 3.0)
        key = legend_rows([(GDP, "measured: the investment not counted as output, the capital not as input"),
                           (NEWT, "true: both counted")], font_size=15).next_to(ax.ax, DOWN, buff=0.5).align_to(
            ax.ax, LEFT)
        tag = published_tag(r"Brynjolfsson, \ Rock and Syverson, \ AEJ: Macro 13(1) (2021); \ the Island: \ "
                            r"agora.automation.j\_curve", corner=DL, font_size=12)
        with self.voiceover(
            "Erik Brynjolfsson, Daniel Rock and Chad Syverson turned this into a measurement problem. <bookmark "
            "mark='a'/> A general-purpose technology needs complementary investment: reorganization, training, "
            "software firms write for themselves. Most of it is intangible, and the national accounts miss much of "
            "it. <bookmark mark='b'/> While firms build it, the work they put in shows up as cost, not output, so "
            f"measured productivity falls: here by about {100 * (1 - J['low']):.0f} percent, at the bottom of the J. "
            "<bookmark mark='c'/> Later the intangible capital pays, but because it was never counted as an input, "
            f"its returns look like productivity growth: measured productivity ends {100 * (J['end'] - 1):.0f} "
            f"percent above the old path, the truth {100 * (J['end_true'] - 1):.0f}. <bookmark mark='d'/> They call "
            "it the productivity J-curve: early on, the statistics understate a new technology; later, they "
            "overstate it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(base), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(build), FadeIn(blab))
            vo.wait_until("b")
            self.play(Create(m), FadeIn(key[0]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(tr), FadeIn(key[1]), run_time=2.0)
            vo.wait_until("d")
            self.play(Indicate(m, color=GDP, scale_factor=1.0))
        self.clear_scene()

    def paradox(self):
        N = load("nordhaus")
        P = N["periods"]
        ax = plane([-0.6, len(P) - 0.4], [0, 3.6], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.4, y_length=4.4,
                   xticks=[], yticks=[0, 1, 2, 3], ylabel=r"growth of output per hour, \ \% a year",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        cols = [GREY_B, NAIVE, NEWT, NAIVE, GDP]
        b = bars(ax, range(len(P)), [100 * p["growth"] for p in P], cols, width=0.62)
        names = VGroup(*[label(f"{p['from']}--{p['to']}", font_size=15, color=GREY_A).next_to(
            ax.ax.c2p(k, 0), DOWN, buff=0.15) for k, p in enumerate(P)])
        vals = VGroup(*[label(f"{100 * p['growth']:.1f}", font_size=15, color=c).next_to(bb, UP, buff=0.06)
                        for bb, p, c in zip(b, P, cols)])
        quote = label(r"``You can see the computer age everywhere but in the productivity statistics''",
                      font_size=19, color=E.ACCENT).to_edge(UP, buff=0.45)
        who = label(r"Robert Solow, \ 1987", font_size=16, color=GREY_A).next_to(quote, DOWN, buff=0.12)
        tag = data_tag(rf"BLS via FRED: \ OPHNFB, \ nonfarm business, \ first quarters \ (retrieved "
                       rf"{N['retrieved']})", corner=DL, font_size=12)
        p = {f"{x['from']}": x for x in P}
        with self.voiceover(
            "In 1987 Robert Solow wrote that you can see the computer age everywhere but in the productivity "
            "statistics. <bookmark mark='a'/> He was right at the time. American output per hour grew "
            f"{100 * p['1948']['growth']:.1f} percent a year from 1948 to 1973, then only "
            f"{100 * p['1973']['growth']:.1f} percent until 1995, while computers spread. <bookmark mark='b'/> Then, "
            f"a decade after his remark, it showed up: {100 * p['1995']['growth']:.1f} percent a year from 1995 to "
            "2004, much of it from producing and using computers. <bookmark mark='c'/> And then it faded again, to "
            f"{100 * p['2004']['growth']:.1f} percent until 2019. <bookmark mark='d'/> Since 2019, "
            f"{100 * P[-1]['growth']:.1f} percent. Whether AI is behind any of that recent pickup is too early to "
            "say, and the J-curve warns that the first years of a general-purpose technology are exactly when the "
            "statistics are least reliable."
        ) as vo:
            self.play(FadeIn(quote), FadeIn(who), FadeIn(ax), FadeIn(names), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromEdge(b[0], DOWN), FadeIn(vals[0]), GrowFromEdge(b[1], DOWN), FadeIn(vals[1]))
            for mk, k in zip("bcd", (2, 3, 4)):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b[k], DOWN), FadeIn(vals[k]))
        self.clear_scene()
