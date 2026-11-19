from __future__ import annotations

from videos.economics.econ12.common import *  # noqa: F403

AC = "#F2A65A"


class Contest(VoiceoverScene):
    def construct(self):
        card(self, 13, r"Contestable markets, \ limit pricing \ and predation", r"Can the threat of a rival discipline "
             r"a monopoly, \ and can a monopoly price a rival out?", "Chapter thirteen. Contestable markets, limit "
             "pricing and predation.", lit={1958: r"McGee on Standard Oil", 1982: r"contestable markets"},
             scale=("firm", "market"), horizon=("a year", "a decade"))
        self.contestable()
        self.limit()
        self.predation()

    def contestable(self):
        c = load("contest")
        qs = np.array(c["qs"])
        ax = plane([0, 100], [0, 100], center=LEFT * 3.1 + DOWN * 0.3, x_length=5.6, y_length=5.0,
                   xticks=[0, 45, 77, 100], yticks=[0, 10, 23, 55, 100], xlabel=r"crossings a season",
                   ylabel=r"fare, \ \$", font_size=16, xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        dem = path(ax, qs, c["demand"], color=WHITE, width=3, smooth=False)
        acc = path(ax, qs, c["ac"], color=AC, width=3.5, yr=(0, 100))
        acl = label(r"average cost", font_size=16, color=AC).next_to(a.c2p(16, 72), RIGHT, buff=0.05)
        mono = Dot(a.c2p(c["Qm"], c["Pm"]), radius=0.09, color=CARTEL)
        ml = label(rf"monopoly: \ \${c['Pm']:.0f}", font_size=16, color=CARTEL).next_to(mono, UR, buff=0.05)
        cont = Dot(a.c2p(c["Q"], c["P"]), radius=0.1, color=COMPETE)
        cl = label(rf"contestable: \ \${c['P']:.2f}", font_size=16, color=COMPETE).next_to(cont, UR, buff=0.05)
        side = VGroup(
            label(r"William Baumol, \ John Panzar \ and Robert Willig (1982): \\ what if a rival could enter and "
                  r"leave at no cost?", font_size=21),
            label(rf"a ferry with a fixed cost of \${c['F']:.0f} a season: \\ room for only one", font_size=21,
                  color=GREY_A),
            label(r"if the ferry ever earns a profit, \ a rival \\ arrives, \ undercuts, \ and leaves before \\ it can "
                  r"respond: \ hit and run", font_size=21, color=ENTRANT),
            label(rf"so even a monopoly charges average cost: \\ \${c['P']:.2f}, \ not \${c['Pm']:.0f}", font_size=22,
                  color=COMPETE),
            label(r"airlines were the hope: \ planes can fly any route; \\ but fares turned out to depend on who "
                  r"\emph{does} fly it", font_size=21, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Baumol, Panzar and Willig, \emph{Contestable Markets} (1982); \ the numbers: \ Agora",
                            corner=DR, font_size=13)
        with self.voiceover(
            "Can the mere threat of a rival discipline a monopoly? <bookmark mark='a'/> In 1982 William Baumol, John "
            "Panzar and Robert Willig asked what would happen if a rival could enter a market, and leave it, at no "
            "cost at all. <bookmark mark='b'/> Take a ferry with a fixed cost of a thousand dollars a season, so that "
            "there is room for only one. <bookmark mark='c'/> If the ferry ever earns a profit, a rival can arrive, "
            "undercut it, take the passengers, and leave before the incumbent responds: hit and run. "
            "<bookmark mark='d'/> So even a monopoly must charge its average cost, about twenty-three dollars, not "
            "the monopoly's fifty-five. A market can be contestable with one seller. <bookmark mark='e'/> Airlines "
            "were the hope, since planes can be flown to any route. But studies of fares after America deregulated "
            "its airlines found that fares depend on how many airlines actually fly a route, not just on how many "
            "could. Sunk costs, gates and loyalty schemes make entry far from free."
        ) as vo:
            self.play(FadeIn(ax), Create(dem), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(acc), FadeIn(acl), FadeIn(side[1]), FadeIn(mono), FadeIn(ml))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(cont, scale=1.5), FadeIn(cl), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def limit(self):
        rows = VGroup(
            label(r"limit pricing: \ a low price today, \ to keep a rival from entering tomorrow", font_size=25),
            label(r"but a rational entrant cares about the price after it enters, \ not before", font_size=24,
                  color=GREY_A),
            label(r"Paul Milgrom and John Roberts (1982): \ a low price can signal low costs, \ which entrants fear",
                  font_size=24, color=LEADER),
            label(r"yet in their model, \ when signals work, \ entry happens no less often \ than if costs were known",
                  font_size=24, color=EQ),
            label(r"the incumbent's low price \ mostly benefits buyers", font_size=25, color=E.ACCENT),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        tag = published_tag(r"Bain (1949); \ Milgrom and Roberts, Econometrica 50(2) (1982)", corner=DR, font_size=13)
        with self.voiceover(
            "A second old idea is limit pricing. <bookmark mark='a'/> An incumbent sets a low price today to keep a "
            "rival from entering tomorrow. <bookmark mark='b'/> The trouble is that a rational entrant cares about "
            "the price it will face after it enters, not the price before. <bookmark mark='c'/> In 1982 Paul "
            "Milgrom and John Roberts rescued the idea with private information: if entrants don't know the "
            "incumbent's costs, a low price can signal that they are low, and that a fight would be hard. "
            "<bookmark mark='d'/> Yet in their model, when the signal works, entry happens no less often than it "
            "would if costs were known. <bookmark mark='e'/> The incumbent's low price mostly benefits its buyers."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def predation(self):
        hc = history_card(1958, r"John McGee, \ ``Predatory Price Cutting: \ The Standard Oil (N.J.) Case''",
                          r"in the trial record, \ he found little evidence that Standard Oil \\ priced below cost to "
                          r"ruin rivals: \ it bought them", color=CARTEL, width=11.6, font_size=24).to_edge(UP, buff=0.45)
        rows = VGroup(
            label(r"his argument: \ predation costs the predator more than its prey, \ and buying a rival is "
                  r"cheaper", font_size=23),
            label(r"game theory's reply (Kreps and Wilson; \ Milgrom and Roberts, \ 1982): \ fighting one entrant "
                  r"builds a reputation \\ that deters the next ones", font_size=23, color=LEADER),
            label(r"Brooke Group (1993): \ an American plaintiff must show prices below cost, \\ and a dangerous "
                  r"chance that the predator will recoup its losses", font_size=23, color=GREY_A),
            label(r"since then, \ few predation cases have succeeded in American courts", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.32).next_to(hc, DOWN, buff=0.45)
        tag = published_tag(r"McGee, J.\ Law and Economics 1 (1958); \ Kreps and Wilson, JET 27 (1982); \ 509 U.S. "
                            r"209 (1993)", corner=DR, font_size=12)
        with self.voiceover(
            "The third is predation: pricing below cost to drive a rival out, then raising prices once it is gone. "
            "The classic accusation was against John D. Rockefeller's Standard Oil. In 1958 John McGee went through "
            "the record of the government's case against it, and found little evidence that Standard Oil had "
            "priced below cost to ruin its rivals. It had bought them. <bookmark mark='a'/> His argument was that "
            "predation costs the predator more than its prey, since the predator sells more at the low price, and "
            "that buying a rival is cheaper. <bookmark mark='b'/> Game theory replied in 1982, in papers by David "
            "Kreps and Robert Wilson and by Milgrom and Roberts: an incumbent facing many possible entrants, who are "
            "unsure what kind of firm it is, can fight the first to build a reputation that deters the rest. "
            "<bookmark mark='c'/> American law settled in between. In the Brooke Group case of 1993 the Supreme "
            "Court held that a plaintiff must show prices below cost, and a dangerous probability that the predator "
            "would recoup its losses later. <bookmark mark='d'/> Since then, few predation cases have succeeded in "
            "American courts."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
