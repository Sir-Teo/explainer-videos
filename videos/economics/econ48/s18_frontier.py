from __future__ import annotations

from videos.economics.econ48.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 16, r"Frontier: \ tipping points, \ adaptation, \ the transition",
             r"What is still being worked out?",
             "Chapter sixteen. Frontier: how large the damage is, who can adapt, and the economics of the transition.",
             lit={2015: r"McGlade and Ekins", 2024: r"Bilal and K\"anzig"}, scale=("world",),
             horizon=("a decade", "a century"))
        self.global_shocks()
        self.transition()
        self.adaptation()

    def global_shocks(self):
        F = tables.FRONTIER48.data
        U = tables.SCC_US.data
        S = load("scc")
        # left: world output lost after a year 1 degree warmer, local-temperature estimates against global
        axL = plane([0, 2], [0, 14], center=LEFT * 3.7 + DOWN * 0.1, x_length=4.0, y_length=3.9, xticks=[],
                    yticks=[0, 4, 8, 12], ylabel=r"world GDP lost, \ \%", yfmt=lambda v: f"{v:.0f}", font_size=13)
        hd_l = label(r"a year 1\textdegree C warmer", font_size=19, color=WHITE).next_to(axL, UP, buff=0.35)
        local, glob = F["global_gdp"] / F["times"], F["global_gdp"]

        def _bar(ax, x, h, col):
            p0, p1 = ax.ax.c2p(x - 0.32, 0), ax.ax.c2p(x + 0.32, h)
            return Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                             fill_opacity=0.85).move_to((p0 + p1) / 2)

        b_loc, b_glob = _bar(axL, 0.55, local, COOL), _bar(axL, 1.45, glob, HEAT)
        l_loc = label(r"local \\ temperature, \\ earlier work", font_size=13, color=COOL).next_to(
            axL.ax.c2p(0.55, 0), DOWN, buff=0.12)
        l_glob = label(r"global \\ temperature, \\ Bilal and K\"anzig", font_size=13, color=HEAT).next_to(
            axL.ax.c2p(1.45, 0), DOWN, buff=0.12)
        n_loc = label(r"about a sixth \\ as large", font_size=13, color=COOL).next_to(b_loc, UP, buff=0.08)
        n_glob = label(rf"about {glob}\%, \\ {F['lag']} years on", font_size=13, color=HEAT).next_to(b_glob, UP,
                                                                                                    buff=0.08)
        # right: social costs of carbon
        axR = plane([0, 1450], [0, 3.6], center=RIGHT * 2.6 + DOWN * 0.1, x_length=5.6, y_length=3.4,
                    xticks=[0, 400, 800, 1200], yticks=[], xlabel=r"\$ a tonne of CO$_2$",
                    xfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), font_size=13)
        hd_r = label(r"the social cost of carbon", font_size=19, color=WHITE).next_to(axR, UP, buff=0.35)
        rows = ((r"this part's model", S["ramsey"], S["ramsey"], OPT), (r"US EPA, \ 2023", U["epa"], U["epa"], POLICY),
                (r"Bilal and K\"anzig", F["scc_lo"], F["scc_hi"], HEAT))
        sccs = VGroup()
        for i, (nm, lo, hi, col) in enumerate(rows):
            yv = 3.0 - 1.0 * i
            p0, p1 = axR.ax.c2p(0, yv - 0.28), axR.ax.c2p(lo, yv + 0.28)
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            g = VGroup(r)
            if hi > lo:
                q0, q1 = axR.ax.c2p(lo, yv - 0.28), axR.ax.c2p(hi, yv + 0.28)
                g.add(Rectangle(width=q1[0] - q0[0], height=q1[1] - q0[1], stroke_color=col, stroke_width=1.5,
                                fill_color=col, fill_opacity=0.3).move_to((q0 + q1) / 2))
                txt = rf"\${lo:,}--{hi:,}".replace(",", "{,}")
            else:
                txt = rf"\${lo:.0f}"
            g.add(label(nm, font_size=13, color=col).next_to(axR.ax.c2p(0, yv), LEFT, buff=0.1))
            g.add(label(txt, font_size=13, color=WHITE).next_to(g[1] if hi > lo else r, RIGHT, buff=0.1))
            sccs.add(g)
        doubt = label(r"the doubt: \ can the world's temperature be separated from everything else that moves the "
                      r"world economy?", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.3)
        head = label(r"how large is the damage?", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(tables.FRONTIER48.tag + r"; \ EPA (2023)", corner=DR, font_size=11)
        with self.voiceover(
            "The first open question is the size of the damage. <bookmark mark='a'/> Chapter twelve measured what a "
            "country's own unusually hot year does: about a point of growth in hot, poor places. <bookmark "
            "mark='b'/> In 2024 Adrien Bilal and Diego Känzig measured something different: what happens when the "
            "whole world has a warm year. They found world GDP about twelve percent lower some six years after a "
            "global rise of one degree, <bookmark mark='c'/> about six times earlier estimates, because extreme "
            "weather strikes many places at once and trade carries the losses. <bookmark mark='d'/> Their social "
            "cost of carbon runs from about eight hundred to over thirteen hundred dollars a tonne in different "
            "versions of the paper, against "
            f"{S['ramsey']:.0f} in this part's model and {U['epa']} in the American government's 2023 estimate. "
            "<bookmark mark='e'/> Others question whether global temperature can be separated from everything "
            "else that moves the world economy. If they are right, every number in this part's dials is too low."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(axL), FadeIn(hd_l), run_time=1.0)
            vo.wait_until("a")
            self.play(GrowFromEdge(b_loc, DOWN), FadeIn(l_loc), run_time=1.2)
            vo.wait_until("b")
            self.play(GrowFromEdge(b_glob, DOWN), FadeIn(l_glob), run_time=2.5)
            self.play(FadeIn(n_glob))
            vo.wait_until("c")
            self.play(FadeIn(n_loc), Indicate(b_loc, color=WHITE, scale_factor=1.05))
            vo.wait_until("d")
            self.play(FadeIn(axR), FadeIn(hd_r), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(g_[1:]) for g_ in sccs], lag_ratio=0.0),
                      LaggedStart(*[GrowFromEdge(g_[0], LEFT) for g_ in sccs], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("e")
            self.play(FadeIn(doubt, shift=UP * 0.1))
        self.clear_scene()

    def transition(self):
        D = load("dice")
        O = D["opt"]
        y = np.array(O["year"])
        ax = plane([2025, 2150], [0, 3.6], center=LEFT * 2.2 + DOWN * 0.35, x_length=7.2, y_length=4.4,
                   xticks=[2050, 2075, 2100, 2125, 2150], yticks=[0, 1, 2, 3], xfmt=lambda v: f"{v:.0f}",
                   ylabel=r"percent of world output", yfmt=lambda v: f"{v:.0f}\\%", font_size=14)
        k = y <= 2150
        ab = path(ax, y[k], 100 * np.array(O["abate"])[k], POLICY, 3.2, smooth=False)
        dm = path(ax, y[k], 100 * np.array(O["damage"])[k], OPT, 3.2, smooth=False)
        db = path(ax, y[k], 100 * np.array(D["base"]["damage"])[k], BASE, 3.2, smooth=False)
        i30, i50 = list(y).index(2030), list(y).index(2050)
        side = VGroup(
            label(rf"purple: \ the optimal \\ path's cost of cutting: \\ {100 * O['abate'][i30]:.2f}\% of output \\ in "
                  rf"2030, \ {100 * O['abate'][i50]:.2f}\% in 2050", font_size=17, color=POLICY),
            label(r"green and red: \\ damages with and \\ without the cuts", font_size=17, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        F = tables.FRONTIER48.data
        res = VGroup()
        for i, (nm, sh, col) in enumerate(((r"coal", F["coal"], GREY_B), (r"gas", F["gas"], COOL),
                                           (r"oil", F["oil"], OIL))):
            yv = 1.3 - 1.15 * i
            full = Rectangle(width=7.0, height=0.62, stroke_color=col, stroke_width=1.5, fill_color=col,
                             fill_opacity=0.3).move_to(np.array([0.6, yv, 0]))
            off = Rectangle(width=7.0 * sh / 100, height=0.62, stroke_width=0, fill_color=LOSS,
                            fill_opacity=0.85).align_to(full, RIGHT).align_to(full, DOWN)
            res.add(VGroup(full, off, label(nm, font_size=22, color=col).next_to(full, LEFT, buff=0.2),
                           label((r"more than " if nm == "coal" else r"about ") + rf"{sh}\% \\ stays unburned",
                                 font_size=16, color=LOSS).next_to(full, RIGHT, buff=0.2)))
        res_h = label(r"for 2\textdegree C at least cost: \ the world's reserves, \ 2010 to 2050", font_size=24,
                      color=E.ACCENT).to_edge(UP, buff=0.7)
        res_t = published_tag(r"McGlade and Ekins, \ Nature (2015)", corner=DR, font_size=11)
        asks = VGroup(*[label(t_, font_size=18, color=c_) for t_, c_ in (
            (r"who bears the losses?", LOSS), (r"how fast can capital move?", CLEAN),
            (r"what happens to interest rates and inflation?", POLICY))]).arrange(RIGHT, buff=0.6).to_edge(DOWN,
                                                                                                    buff=0.6)
        with self.voiceover(
            "The second is the transition itself. <bookmark mark='a'/> In the model, cutting emissions on the "
            f"optimal path costs about {100 * O['abate'][i30]:.2f} percent of world output in 2030 and "
            f"{100 * O['abate'][i50]:.2f} percent in 2050: small beside the economy, <bookmark mark='b'/> and "
            "smaller than the damage it avoids later. <bookmark mark='c'/> But averages hide who pays. Christophe "
            "McGlade and Paul Ekins estimated in 2015 that to hold warming to two degrees at least cost, <bookmark "
            "mark='c1'/> more than eighty percent of the world's coal reserves, <bookmark mark='c2'/> half its gas "
            "<bookmark mark='c3'/> and a third of its oil would have to stay in the ground: <bookmark mark='d'/> "
            "assets on the books of firms and the budgets of governments that would be worth far less. <bookmark "
            "mark='e'/> Who bears those losses, <bookmark mark='e2'/> how fast capital can move to clean energy, "
            "<bookmark mark='e3'/> and what that does to interest rates and inflation, is the macroeconomics of the "
            "transition, and it is being written now."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(ab), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(db), Create(dm), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeOut(VGroup(ax, ab, dm, db, side, tag)), run_time=0.8)
            self.play(FadeIn(res_h), FadeIn(res_t), *[FadeIn(r_[0]) for r_ in res], *[FadeIn(r_[2]) for r_ in res],
                      run_time=1.0)
            for mk, r_ in zip(("c1", "c2", "c3"), res):
                vo.wait_until(mk)
                self.play(GrowFromEdge(r_[1], RIGHT), FadeIn(r_[3]), run_time=1.0)
            vo.wait_until("d")
            self.play(Indicate(VGroup(*[r_[1] for r_ in res]), color=WHITE, scale_factor=1.03))
            for mk, a_ in zip(("e", "e2", "e3"), asks):
                vo.wait_until(mk)
                self.play(FadeIn(a_, shift=UP * 0.1))
        self.clear_scene()

    def adaptation(self):
        H = tables.HEALTH_48.data
        cards = point_cards([
            (r"adaptation works", rf"air conditioning cut \\ the toll of US \\ heat by about {H['ac']}\%", COOL),
            (r"but costs money", r"the hottest countries \\ are among the \\ poorest: \ the ones \\ least able to "
                                 r"adapt", HEAT),
            (r"and is a choice", r"where people live, \\ what farmers grow, \\ what cities build: \\ each priced, "
                                 r"\ or not", POLICY),
            (r"the question", r"how much of the \\ damage is left \\ once people adapt, \\ and who pays \\ for it",
             E.ACCENT),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"who can adapt?", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.HEALTH_48.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The third is adaptation. <bookmark mark='a'/> It works: chapter twelve's air conditioners cut the "
            f"toll of American heat by about {H['ac']} percent. <bookmark mark='b'/> But it costs money, and the "
            "hottest countries, where chapter twelve's curve falls fastest, are among the poorest, the least able "
            "to pay. <bookmark mark='c'/> And it is a set of choices: where people live, what farmers plant, what "
            "cities build, whether flood risk is priced into insurance and property. <bookmark mark='d'/> How much "
            "damage remains once people adapt, and who pays for the adapting, is the question on which the size "
            "of climate damage, and the fairness of climate policy, now turn."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
