from __future__ import annotations

from videos.economics.econ46.common import *  # noqa: F403


class Dual(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Dual economies", r"Why are farm workers so much less productive than town workers?",
             "Chapter four. Dual economies.", lit={1954: r"Lewis", 2014: r"Gollin, Lagakos and Waugh"},
             scale=("nation",), horizon=("decades",))
        self.lewis_model()
        self.lewis_path()
        self.gap()
        self.why()

    def lewis_model(self):
        chain = flow_chain([(r"farms with \\ surplus labour", FARM), (r"a modern sector \\ hires at a \\ subsistence "
                                                                      r"wage", TOWN),
                            (r"profits \\ reinvested", E.ACCENT), (r"more jobs, \\ same wage", TOWN),
                            (r"the turning \\ point", GAIN)],
                           notes=[r"one worker fewer: \\ the harvest \\ barely changes",
                                  r"workers come \\ without a raise", r"capital grows", r"until the \\ surplus is gone",
                                  r"wages start \\ to rise"],
                           box_w=2.3, box_h=1.05, buff=0.42, font_size=18, note_size=15)
        chain.move_to(UP * 0.5)
        tag = published_tag(tables.DUAL_46.tag, corner=DR, font_size=11)
        foot = label(r"W. Arthur Lewis, \ 1954: \ \emph{Economic Development with Unlimited Supplies of Labour}",
                     font_size=20, color=GREY_A).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "In 1954 W. Arthur Lewis, who would share a Nobel prize for it, described how a poor economy grows. "
            "<bookmark mark='a'/> Most people work on family farms, where there is more labour than land: take one "
            "worker away and the harvest barely changes. <bookmark mark='b'/> A modern sector, factories and "
            "mines and trade, can hire from the farms at a wage just above subsistence, and workers come without a "
            "raise. <bookmark mark='c'/> Its owners reinvest their profits, <bookmark mark='d'/> which creates more "
            "jobs at the same wage, year after year, as long as the surplus on the farms lasts. <bookmark "
            "mark='e'/> When it runs out, the modern sector must bid workers away from farms that now miss them, "
            "and wages begin to rise. That moment is called the Lewis turning point."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(foot), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]))
            for k, mk in enumerate("bcde"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
        self.clear_scene()

    def lewis_path(self):
        L = load("lewis")
        T = len(L["emp"])
        t = list(range(T))
        a1 = plane([0, T - 1], [0, 100], center=LEFT * 3.4 + DOWN * 0.4, x_length=5.4, y_length=4.2,
                   xticks=[0, 20, 40, 59], yticks=[0, 20, 40, 60, 80, 100], xlabel=r"years",
                   ylabel=r"workers in the modern sector", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=13)
        a2 = plane([0, T - 1], [0, 2.6], center=RIGHT * 3.0 + DOWN * 0.4, x_length=5.4, y_length=4.2,
                   xticks=[0, 20, 40, 59], yticks=[0, 0.5, 1, 1.5, 2, 2.5], xlabel=r"years",
                   ylabel=r"the wage \ (subsistence = 1)", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=13)
        e = path(a1, t, L["emp"], TOWN, 3.2, smooth=False)
        w = path(a2, t, L["wage"], GAIN, 3.2, smooth=False)
        sur = DashedLine(a1.ax.c2p(0, L["surplus"]), a1.ax.c2p(T - 1, L["surplus"]), color=FARM, stroke_width=1.8)
        sl = label(rf"the surplus: \ {L['surplus']:.0f} of {L['labour']:.0f}", font_size=15, color=FARM).next_to(
            a1.ax.c2p(2, L["surplus"]), UP, buff=0.08).align_to(a1.ax.c2p(2, 0), LEFT)
        tp = VGroup(vline(a1, L["turn"], 0, 100, WHITE), vline(a2, L["turn"], 0, 2.6, WHITE))
        tl = label(rf"the turning point, \ year {L['turn']}", font_size=16, color=WHITE).next_to(
            a2.ax.c2p(L["turn"], 2.3), LEFT, buff=0.1)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is Lewis's economy on the Island: a hundred workers, sixty of them surplus on the farms. "
            "<bookmark mark='a'/> Modern employment grows slowly, then fast, as reinvested profits compound. "
            "<bookmark mark='b'/> Through all of it, the wage stays at subsistence. Growth goes to profits, and to "
            f"more jobs, not to higher pay. <bookmark mark='c'/> In year {L['turn']} the surplus is used up. "
            "<bookmark mark='d'/> From then on each worker the factories hire is missed on the farm, the wage "
            "rises, and the gains of growth begin to reach workers. Many economists have asked whether China passed "
            "its own turning point in the 2000s, when factory wages there began to climb fast."
        ) as vo:
            self.play(FadeIn(a1), FadeIn(a2), FadeIn(tag), Create(sur), FadeIn(sl), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(e), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(w), run_time=3.0)
            vo.wait_until("c")
            self.play(Create(tp), FadeIn(tl))
            vo.wait_until("d")
            self.play(Indicate(tl, color=E.ACCENT))
        self.clear_scene()

    def gap(self):
        G = load("agrigap")
        ax = plane([2.9, 5.25], [0, 12], center=LEFT * 1.8 + DOWN * 0.35, x_length=8.2, y_length=4.8,
                   xticks=[3, 4, 5], yticks=[0, 2, 4, 6, 8, 10, 12],
                   xlabel=r"GDP per head, \ 2021 dollars at PPP \ (log scale)",
                   ylabel=r"output per worker: \ outside farms / on farms",
                   xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), yfmt=lambda v: f"{v:.0f}", font_size=13)
        x = np.log10(np.array(G["gdppc"]))
        g = np.array(G["gap"])
        pts = VGroup(*[dot(ax, a, min(b, 12), FARM if b <= 12 else HOLD, 0.045) for a, b in zip(x, g)])
        n_top = int(np.sum(g > 12))
        top = label(rf"{n_top} above 12, \ drawn at the top, \\ among them Equatorial Guinea's \\ oil and Zambia's "
                    r"copper", font_size=13,
                    color=HOLD).next_to(ax.ax.c2p(4.4, 12), DOWN, buff=0.05)
        one = DashedLine(ax.ax.c2p(2.9, 1), ax.ax.c2p(5.25, 1), color=GREY_B, stroke_width=1.6)
        ol = label(r"no gap", font_size=14, color=GREY_B).next_to(ax.ax.c2p(5.25, 1), UP, buff=0.05).shift(LEFT * 0.4)
        names = VGroup()
        for c in ("MWI", "ETH", "BGD", "IND", "CHN", "BRA", "USA"):
            if c in G["pick"]:
                p = G["pick"][c]
                names.add(label(p["name"], font_size=13, color=WHITE).next_to(
                    ax.ax.c2p(np.log10(p["gdppc"]), min(p["gap"], 12)), UR, buff=0.04))
        side = VGroup(
            label(rf"{G['n']} countries, \\ latest year", font_size=18, color=WHITE),
            label(rf"poorest quarter: \\ median gap {G['median_poorest']:.1f}", font_size=18, color=FARM),
            label(rf"richest quarter: \\ median gap {G['median_richest']:.1f}", font_size=18, color=TOWN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        eq = MathTex(r"\text{gap} = \frac{(1-v)/(1-e)}{v/e}", font_size=30, color=THEORY).next_to(side, DOWN,
                                                                                                  buff=0.4)
        el = label(r"$v$: \ farms' share of value added \\ $e$: \ farms' share of workers", font_size=14,
                   color=GREY_A).next_to(eq, DOWN, buff=0.15)
        tag = data_tag(r"World Bank, \ WDI: \ SL.AGR.EMPL.ZS, \ NV.AGR.TOTL.ZS, \ NY.GDP.PCAP.PP.KD", corner=DL,
                       font_size=11)
        with self.voiceover(
            "Lewis's dual economy leaves a trace in national accounts. If farms hold more workers than they need, "
            "output per worker on farms is low compared with output per worker elsewhere. <bookmark mark='a'/> "
            "The ratio is easy to compute: the share of value added outside farms over the share of workers "
            "outside farms, divided by the same ratio on farms. <bookmark mark='b'/> Here it is for "
            f"{G['n']} countries, from the World Bank's latest data. <bookmark mark='c'/> In the poorest quarter of "
            f"countries the median worker outside agriculture produces {G['median_poorest']:.1f} times as much as "
            "one on a farm. <bookmark mark='d'/> In the richest quarter, "
            f"{G['median_richest']:.1f} times. If labour moved freely to where it produces most, the ratio would be "
            "about one. In poor countries it is far from one."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(one), FadeIn(ol), run_time=1.0)
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(el))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.01), FadeIn(names), FadeIn(side[0]),
                      FadeIn(top), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def why(self):
        Tg = tables.DUAL_46.data
        cards = point_cards([
            (r"the raw gap", rf"about {Tg['raw']} in national \\ accounts, \ more \\ in poor countries", FARM),
            (r"measurement", r"hours, \ schooling, \\ living costs, \\ farm output \\ missed by surveys", HOLD),
            (r"what remains", rf"about {Tg['adjusted']} after all \\ adjustments", POOR),
            (r"why?", r"who chooses to move, \\ or barriers to moving: \\ Part 37's cities", TOWN),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"Gollin, \ Lagakos and Waugh, \ 2014", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.DUAL_46.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Douglas Gollin, David Lagakos and Michael Waugh asked how much of this gap is real. <bookmark "
            "mark='a'/> In national accounts it is about three, and larger in developing countries. <bookmark "
            "mark='b'/> Part of it is measurement: farmers work fewer hours, have less schooling, live where things "
            "cost less, and grow food that surveys miss. <bookmark mark='c'/> Correct for all of it, and a gap of "
            "about two remains. <bookmark mark='d'/> Why would workers leave that much on the table? Either the "
            "people who move are different from those who stay, so the gap is about people rather than places; or "
            "something stops them moving, the cost of a city, the loss of village insurance, rights to land that "
            "lapse when you leave. Which one it is decides whether helping people move to towns would raise their "
            "incomes, and Part thirty-seven's cities are part of the answer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Circumscribe(cards.cards[0], color=WHITE, buff=0.05))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
