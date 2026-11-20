from __future__ import annotations

from videos.economics.econ38.common import *  # noqa: F403


class Monopsony(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Monopsony", r"What if employers set wages?",
             "Chapter seven. Monopsony.", lit={1933: r"Joan Robinson", 2003: r"Manning, \ \emph{Monopsony in Motion}"},
             scale=("firm", "market"), horizon=("a year",))
        self.diagram()
        self.floor_curve()

    def diagram(self):
        P = load("monopsony")
        L = np.array(P["L"])
        ax = plane([20, 320], [3, 9], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[50, 100, 150, 200, 250, 300], yticks=[3, 4, 5, 6, 7, 8, 9], xlabel=r"workers at the firm",
                   ylabel=r"hourly wage, \ \$", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        sup = path(ax, L, P["w_sup"], SUPPLY, 3.4, yr=(3, 9))
        mcl = path(ax, L, P["mcl"], MCL, 3.4, yr=(3, 9))
        mrp = path(ax, L, P["mrpl"], DEMAND, 3.4, yr=(3, 9))
        ec = dot(ax, P["L_c"], P["w_c"], WHITE, 0.08)
        em = dot(ax, P["L_m"], P["w_m"], E.ACCENT, 0.09)
        drop = DashedLine(ax.ax.c2p(P["L_m"], P["mrpl_m"]), ax.ax.c2p(P["L_m"], P["w_m"]), color=E.ACCENT,
                          stroke_width=2.5)
        side = VGroup(
            label(r"teal: \ workers willing \\ to come at each wage", font_size=17, color=SUPPLY),
            label(r"violet: \ the cost of one more, \\ who raises everyone's pay", font_size=17, color=MCL),
            label(r"red: \ what one more \\ worker adds", font_size=17, color=DEMAND),
            label(rf"the firm pays \${P['w_m']:.2f}, \ hires {P['L_m']:.0f}; \\ competition: \ \${P['w_c']:.2f}, "
                  rf"\ {P['L_c']:.0f}", font_size=17, color=E.ACCENT),
            label(rf"markdown: \ {100 * P['markdown']:.0f}\% below \\ what the worker adds", font_size=17,
                  color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "In 1933 Joan Robinson gave a name to the opposite case: monopsony, a market with one buyer. If one firm "
            "employs most of a town, it faces the town's whole supply curve. <bookmark mark='a'/> To hire one more "
            "worker it must raise the wage, <bookmark mark='b'/> and pay the higher wage to everyone it already "
            "employs, so the cost of one more worker rises faster than the wage. <bookmark mark='c'/> The firm hires "
            "where that cost equals what the worker adds. <bookmark mark='d'/> So it hires fewer people, at a lower "
            f"wage, than a competitive market would: {P['L_m']:.0f} workers at {P['w_m']:.2f} dollars instead of "
            f"{P['L_c']:.0f} at {P['w_c']:.2f}. <bookmark mark='e'/> With a supply elasticity of {P['eta']:.0f}, wages "
            f"are marked down {100 * P['markdown']:.0f} percent below what the marginal worker adds. Alan Manning "
            "argued in 2003 that firms need not be alone in town to have this power: if finding another job takes "
            "time, every employer faces an upward-sloping supply."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(sup), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(mcl), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(mrp), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(em, scale=1.5), Create(drop), FadeIn(ec), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def floor_curve(self):
        P = load("monopsony")
        m, e = np.array(P["m"]), np.array(P["emp"])
        ax = plane([4.6, 7.4], [80, 230], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[5, 5.5, 6, 6.5, 7], yticks=[100, 150, 200], xlabel=r"the minimum wage, \ \$",
                   ylabel=r"workers the firm hires", xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        ln = path(ax, m, e, E.ACCENT, 3.6, smooth=False, yr=(80, 230))
        vm, vc = vline(ax, P["w_m"], 80, 230, MCL), vline(ax, P["w_c"], 80, 230, WHITE)
        side = VGroup(
            label(rf"up to \${P['w_m']:.2f}: \ no effect", font_size=18, color=GREY_A),
            label(rf"\${P['w_m']:.2f} to \${P['w_c']:.2f}: \\ a higher minimum \\ means more jobs", font_size=18,
                  color=WAGE),
            label(rf"above \${P['w_c']:.2f}: \\ the textbook's losses", font_size=18, color=LOSS),
            label(r"how much power firms have: \\ about 800 estimates, \\ by method and country", font_size=17,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = published_tag(tables.SS_2021.tag + r"; \ the Island", corner=DR, font_size=12)
        with self.voiceover(
            "Now impose a minimum wage on the monopsonist. <bookmark mark='a'/> Below its own wage, nothing happens. "
            "<bookmark mark='b'/> Between its wage and the competitive one, the minimum removes the reason to hold "
            "back: the firm no longer raises everyone's pay by hiring one more, so it hires everyone willing to work "
            "at the minimum, and employment rises. <bookmark mark='c'/> Only above the competitive wage does the "
            "textbook's loss appear. <bookmark mark='d'/> So the effect of a minimum wage depends on how much power "
            "employers have, which is measured by how elastic the supply of workers to a single firm is. Anna "
            "Sokolova and Todd Sorensen collected about eight hundred estimates and found the answer varies by "
            "method, country and occupation; it is the next chapter's question."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(ln), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(vm), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(vc), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
