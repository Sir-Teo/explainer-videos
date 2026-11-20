from __future__ import annotations

from videos.economics.econ31.common import *  # noqa: F403


class Euro(VoiceoverScene):
    def construct(self):
        card(self, 12, r"The euro and the lender of last resort", r"How can a sentence lower a country's "
             r"borrowing costs?", "Chapter twelve. The euro and the lender of last resort.",
             lit={1873: r"Bagehot", 1988: r"Calvo", 2012: r"Draghi"}, scale=("nation", "world"),
             horizon=("a day", "two years"))
        self.game()
        self.backstop()
        self.why()

    def _axes(self):
        return plane([0, 12], [0, 12], center=LEFT * 2.2 + DOWN * 0.3, x_length=5.6, y_length=5.0,
                     xticks=[0, 2, 4, 6, 8, 10, 12], yticks=[0, 2, 4, 6, 8, 10, 12],
                     xlabel=r"the yield investors expect, \ \%", ylabel=r"the yield they then demand, \ \%",
                     xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15)

    def game(self):
        D = load("debt")
        F = D["free"]
        r = np.array(F["r"]) * 100
        R = np.array(F["R"]) * 100
        ax = self._axes()
        diag = seg(ax, 0, 0, 12, 12, GREY_C, 2, dashed=True)
        curve = path(ax, r, R, BOND, 3.5, yr=(0, 12))
        good, bad = F["equilibria"]
        pg = dot(ax, 100 * good, 100 * good, OUTPUT, 0.1)
        pb = dot(ax, 100 * bad, 100 * bad, INFL, 0.1)
        up = D["path_up"]
        stairs = VGroup()
        for a, b in zip(up[:-1], up[1:]):
            if not (np.isfinite(a) and np.isfinite(b)) or 100 * b > 12:
                break
            stairs.add(Line(ax.ax.c2p(100 * a, 100 * a), ax.ax.c2p(100 * a, 100 * b), color=INFL, stroke_width=2.5),
                       Line(ax.ax.c2p(100 * a, 100 * b), ax.ax.c2p(100 * b, 100 * b), color=INFL, stroke_width=2.5))
        side = VGroup(
            label(r"a government owing 120\% of GDP; \\ it defaults if the interest bill \\ exceeds what it can raise",
                  font_size=17, color=GREY_A),
            label(r"purple: \ the yield investors demand, \\ given the yield they expect \\ (higher yields, \ more "
                  r"default)", font_size=17, color=BOND),
            label(rf"green: \ an equilibrium at {100 * good:.1f}\%", font_size=17, color=OUTPUT),
            label(rf"red: \ another at {100 * bad:.1f}\%; \\ beyond it, \ a spiral", font_size=17, color=INFL),
            label(r"same country, \ same debts: \\ which one happens depends \\ on what investors expect",
                  font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Calvo, \ \emph{AER} 78(4) (1988); \ De Grauwe (2011); \ Agora (agora.cb.debt\_game)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Why could a sentence lower Spain's borrowing costs? Because the crisis was partly self-fulfilling. "
            "<bookmark mark='a'/> Take a government that owes a hundred and twenty percent of its income, and will "
            "default if the interest bill grows larger than the taxes it can raise, an amount nobody knows exactly. "
            "<bookmark mark='b'/> Investors who expect a higher yield expect a bigger bill, so a higher chance of "
            "default, so they demand a higher yield still: the purple curve. <bookmark mark='c'/> Where the curve "
            f"meets the diagonal, expectations are fulfilled. At {100 * good:.1f} percent, the bill is small, "
            "default is unlikely, and the low yield is justified. <bookmark mark='d'/> At "
            f"{100 * bad:.0f} percent, the bill is large, default likely, and the high yield justified too. Expect "
            "a little more, and yields spiral up until no one will lend at all. <bookmark mark='e'/> The country's "
            "debts are the same in both. Which equilibrium it gets depends on what investors expect, which was "
            "Guillermo Calvo's point in 1988 and Paul De Grauwe's about the euro area in 2011."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(diag), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(curve), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(GrowFromCenter(pg), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(GrowFromCenter(pb), FadeIn(side[3]))
            self.play(Create(stairs), run_time=2)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def backstop(self):
        D = load("debt")
        F, C = D["free"], D["capped"]
        ax = self._axes()
        diag = seg(ax, 0, 0, 12, 12, GREY_C, 2, dashed=True)
        free = path(ax, np.array(F["r"]) * 100, np.array(F["R"]) * 100, BOND, 2.5, yr=(0, 12))
        capped = path(ax, np.array(C["r"]) * 100, np.array(C["R"]) * 100, CB, 3.5, yr=(0, 12))
        cap = seg(ax, 100 * D["cap"], 0, 100 * D["cap"], 12, CB, 2, dashed=True)
        good = C["equilibria"][0]
        pg = dot(ax, 100 * good, 100 * good, OUTPUT, 0.1)
        pc = D["path_capped"]
        stairs = VGroup()
        for a, b in zip(pc[:-1], pc[1:]):
            if not (np.isfinite(a) and np.isfinite(b)) or abs(a - b) < 2e-4:
                break
            stairs.add(Line(ax.ax.c2p(100 * a, 100 * a), ax.ax.c2p(100 * a, 100 * b), color=CB, stroke_width=2.5),
                       Line(ax.ax.c2p(100 * a, 100 * b), ax.ax.c2p(100 * b, 100 * b), color=CB, stroke_width=2.5))
        side = VGroup(
            label(rf"the backstop: \ the central bank \\ will buy at {100 * D['cap']:.1f}\%, \ without limit",
                  font_size=17, color=CB),
            label(r"the default risk can no longer \\ climb with the yield", font_size=17, color=CB),
            label(rf"one equilibrium left: \ {100 * good:.1f}\%", font_size=17, color=OUTPUT),
            label(r"a panic now runs back down", font_size=17, color=CB),
            label(r"believed, \ the promise is never used: \\ no one sells at the bad price", font_size=18,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now add a lender of last resort. <bookmark mark='a'/> The central bank promises to buy the country's "
            f"bonds, without limit, at {100 * D['cap']:.1f} percent. <bookmark mark='b'/> The bill can no longer "
            "grow with investors' fears, so neither can the chance of default: the curve goes flat. "
            "<bookmark mark='c'/> The bad equilibrium is gone; only the good one is left. <bookmark mark='d'/> "
            "Start from a panic, and yields now run back down. <bookmark mark='e'/> And if investors believe the "
            "promise, nobody sells at the bad price, so the central bank never has to buy. This is Part 26's bank "
            "run again, with a country in place of a bank, and deposit insurance in the form of a sentence. "
            "Walter Bagehot's rule from 1873 was to lend freely, against good collateral, to solvent borrowers; "
            "Draghi's conditions were the modern version of good collateral."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(diag), FadeIn(free), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(cap), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(free.animate.set_stroke(opacity=0.3), Create(capped), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(GrowFromCenter(pg), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(stairs), FadeIn(side[3]), run_time=2)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def why(self):
        S = load("spreads")
        t = np.array(S["t"])
        ax = plane([2007, 2017], [-1, 6], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[2008, 2010, 2012, 2014, 2016], yticks=[0, 2, 4, 6],
                   ylabel=r"10-year yield over Germany's, \ points", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=15)
        zero = seg(ax, 2007, 0, 2017, 0, GREY_C, 1.5)
        es = path(ax, t, S["ES_DE"], COUNTRY["ES"], 3.2, smooth=False)
        it = path(ax, t, S["IT_DE"], COUNTRY["IT"], 3.2, smooth=False)
        gb = path(ax, t, S["GB_DE"], COUNTRY["GB"], 3.2, smooth=False)
        jul = vline(ax, 2012.54, -1, 6, E.ACCENT, 2.5)
        side = VGroup(
            label(r"2011: \ public debt 85\% of GDP in Britain, \\ 69\% in Spain \ (Eurostat)", font_size=17,
                  color=GREY_A),
            label(r"blue: \ Britain's spread over Germany", font_size=17, color=COUNTRY["GB"]),
            label(rf"gold: \ Spain's, \ {S['es_spread_jul12']:.1f} points in July 2012", font_size=17,
                  color=COUNTRY["ES"]),
            label(rf"green: \ Italy's, \ {S['it_spread_jul12']:.1f}", font_size=17, color=COUNTRY["IT"]),
            label(r"Britain's central bank could always \\ print the pounds it owed; \\ Spain's could not print "
                  r"euros", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"OECD bond yields via FRED; \ Eurostat government debt, \ 2011; \ De Grauwe, \ CEPS WD 346 "
                       r"(2011)", corner=DR, font_size=12)
        with self.voiceover(
            "Why were Spain and Italy exposed, and not Britain? <bookmark mark='a'/> In 2011 Britain's public debt "
            "was eighty-five percent of its GDP, Spain's sixty-nine. <bookmark mark='b'/> Yet Britain paid barely "
            "more than Germany to borrow, <bookmark mark='c'/> while Spain paid "
            f"{S['es_spread_jul12']:.1f} points more by July 2012, <bookmark mark='d'/> and Italy "
            f"{S['it_spread_jul12']:.1f}. <bookmark mark='e'/> De Grauwe's explanation: Britain borrows in pounds, "
            "and the Bank of England can always create pounds, so a run on British debt cannot end in a default "
            "forced by a lack of cash. Spain and Italy borrowed in euros that neither could create, so investors "
            "could force them into the bad equilibrium. Draghi's sentence gave the euro area what Britain had: a "
            "central bank that would stand behind its governments' debts, within its mandate."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(jul), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(gb), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(es), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(it), FadeIn(side[3]), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
