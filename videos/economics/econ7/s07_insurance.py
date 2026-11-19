from __future__ import annotations

from videos.economics.econ7.common import *  # noqa: F403

LOAD_COLOR = {"0": SAFE, "0.2": TODAY, "0.5": RISKY}


class Insurance(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Insurance and the risky asset", r"How much risk should a risk-averse person shed, and how much "
             r"should she take on?", "Chapter six. Insurance and the risky asset.", scale=("person", "household",
                                                                                          "market"))
        self.cover()
        self.deductible()
        self.portfolio()

    def cover(self):
        ins = load("insurance")
        ax = plane([0, 1], [0, 1.05], center=LEFT * 2.8 + DOWN * 0.4, x_length=6.8, y_length=4.8,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[], xlabel=r"share of the boat insured",
                   ylabel=r"Ana's expected utility (scaled)", font_size=17, xfmt=lambda v: f"{100 * v:.0f}\\%")
        curves, tops, labs = VGroup(), VGroup(), VGroup()
        allv = np.concatenate([np.array(c["eu"]) for c in ins["covers"].values()])
        lo, hi = allv.min(), allv.max()
        names = {"0": r"fair price", "0.2": r"20\% loading", "0.5": r"50\% loading"}
        for k, c in ins["covers"].items():
            q, eu = np.array(c["q"]), (np.array(c["eu"]) - lo) / (hi - lo)
            col = LOAD_COLOR[k]
            curves.add(path(ax, q, eu, color=col, width=3.2))
            j = int(np.argmax(eu))
            tops.add(Dot(ax.ax.c2p(c["cover"], eu[j]), radius=0.08, color=col))
            labs.add(label(rf"{names[k]}: \ {100 * c['cover']:.0f}\%", font_size=19, color=col).next_to(
                ax.ax.c2p(c["cover"], eu[j]), UP, buff=0.12))
        side = VGroup(
            label(r"Ana: \ \$300, \ \$150 of it her boat", font_size=25),
            label(r"a storm wrecks it in one year in ten", font_size=24, color=RISKY),
            label(rf"fair cover: \ \${ins['fair_premium']:.0f} a year for the whole boat", font_size=24, color=SAFE),
            label(r"at a fair price she insures it all \\ (Mossin, 1968)", font_size=24, color=SAFE),
            label(r"load the price, \ and she keeps \\ part of the risk herself", font_size=24, color=RISKY),
            label(rf"she would pay up to \${ins['max_premium']:.2f} for full cover: \\ the \${ins['max_premium'] - ins['fair_premium']:.2f} "
                  r"above fair is room \\ for an insurer's costs and profit", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Risk aversion creates a market: insurance. <bookmark mark='a'/> Ana has three hundred dollars, a hundred "
            "and fifty of it in her boat, and in one year in ten a storm wrecks it. <bookmark mark='b'/> Cover for "
            "the whole boat at a fair price, one that just pays the expected loss, costs fifteen dollars a year. "
            "<bookmark mark='c'/> Here is her expected utility against the share of the boat she insures. At the fair "
            "price it rises all the way to full cover: a risk-averse person offered fair odds sheds all of the risk. "
            "Jan Mossin proved it in 1968. <bookmark mark='d'/> Real insurance isn't fair; premiums carry a loading "
            "for costs and profit. With a twenty percent loading, Ana covers about four fifths of the boat; with "
            "fifty percent, three fifths. She keeps part of the risk, which is why deductibles exist. "
            "<bookmark mark='e'/> And the most she'd pay for full cover is twenty-seven dollars twenty-seven, twelve "
            "dollars more than fair. That gap is what makes insurance a business."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(Create(curves[0]), FadeIn(tops[0]), FadeIn(labs[0]), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(Create(curves[1]), FadeIn(tops[1]), FadeIn(labs[1]), Create(curves[2]), FadeIn(tops[2]),
                      FadeIn(labs[2]), FadeIn(side[4]))
            vo.wait_until("e")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def deductible(self):
        d = load("insurance")["deductible"]
        head = label(r"a deductible, \ at an American household's scale", font_size=34,
                     color=E.ACCENT).to_edge(UP, buff=0.5)
        setup = VGroup(
            label(r"wealth \$100{,}000; \ a claim in one year in twenty", font_size=27),
            label(rf"a \${d['low']:.0f} deductible or a \${d['high']:.0f} one: \ the lower saves \${d['high'] - d['low']:.0f} "
                  rf"when there is a claim, \\ so on average \${d['saving']:.0f} a year", font_size=27, color=SAFE),
        ).arrange(DOWN, buff=0.25).next_to(head, DOWN, buff=0.4)
        rows = VGroup(label(r"the lower deductible costs, a year, \ extra:", font_size=25, color=GREY_B),
                      label(r"the relative risk aversion it takes to buy it:", font_size=25, color=GREY_B))
        cells = VGroup()
        for i, (x, g) in enumerate(d["rows"]):
            cells.add(VGroup(label(rf"\${x:.0f}", font_size=32), label(rf"{g:.0f}", font_size=34, color=RISKY)))
        grid = VGroup()
        for j, c in enumerate(cells):
            c[0].move_to([-1.0 + 2.8 * j, -0.2, 0])
            c[1].move_to([-1.0 + 2.8 * j, -1.2, 0])
            grid.add(c)
        rows[0].move_to([-4.3, -0.2, 0])
        rows[1].move_to([-4.3, -1.2, 0])
        for r_ in rows:
            r_.width = min(r_.width, 4.4)
        foot = label(r"plausible values run from about 1 to 10; \ yet real homeowners' deductible choices imply "
                     r"\\ risk aversion far beyond them (Sydnor, 2010)", font_size=24, color=GREY_A).to_edge(DOWN,
                                                                                                  buff=0.8)
        tag = illustrative_tag(r"illustrative numbers; \ computed: Agora", corner=DR, font_size=15)
        with self.voiceover(
            "The same arithmetic finds something odd in real insurance. Take an American household with a hundred "
            "thousand dollars, which makes a claim in one year in twenty. <bookmark mark='a'/> It can choose a five "
            "hundred dollar deductible or a thousand dollar one. The lower deductible saves five hundred dollars when "
            "there's a claim, so twenty-five dollars a year on average. <bookmark mark='b'/> If it costs thirty "
            "dollars a year more, buying it takes a relative risk aversion of about twenty-five. At fifty dollars "
            "more, about a hundred; at a hundred dollars more, about two hundred. <bookmark mark='c'/> Nobody thinks "
            "people are that risk averse: estimates run from about one to ten. Yet when Justin Sydnor studied "
            "the customers of a large home insurer, in 2010, the deductibles many of them chose implied risk "
            "aversion far beyond any plausible value. Over small stakes, people behave as if they were far more risk averse than over large ones. Chapter nine "
            "shows why expected utility can't explain that."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(setup[0]))
            vo.wait_until("a")
            self.play(FadeIn(setup[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows))
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in grid], lag_ratio=0.7), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def portfolio(self):
        v = load("insurance")["venture"]
        shares = np.array(v["shares"])
        ax = plane([0, 1.6], [0, 1.05], center=LEFT * 2.8 + DOWN * 0.4, x_length=6.6, y_length=4.8,
                   xticks=[0, 0.5, 1.0, 1.5], yticks=[], xlabel=r"share of wealth in the venture",
                   ylabel=r"expected utility (scaled)", font_size=17, xfmt=lambda v_: f"{100 * v_:.0f}\\%")
        curves, tops = VGroup(), VGroup()
        for g, col in (("2", LATER), ("4", RISKY)):
            e = np.array(v["eu"][g])
            e = (e - e.min()) / (e.max() - e.min())
            curves.add(path(ax, shares, e, color=col, width=3.2))
            b = v[f"best_{g}"]
            j = int(np.argmin(np.abs(shares - b)))
            tops.add(VGroup(Dot(ax.ax.c2p(b, e[j]), radius=0.08, color=col),
                            label(rf"$\gamma = {g}$: \ {100 * b:.0f}\%", font_size=20, color=col).next_to(
                                ax.ax.c2p(b, e[j]), UP, buff=0.12)))
        m = v["merton"]
        side = VGroup(
            label(rf"Dara's venture: \ {100 * (v['outcomes'][0] - 1):.0f}\% or {100 * (v['outcomes'][1] - 1):.0f}\%, "
                  r"\ 50--50", font_size=24, color=RISKY),
            label(rf"mean {100 * v['mu']:.0f}\%, \ s.d.\ {100 * v['sd']:.0f}\%; \ the safe rate {100 * v['safe']:.0f}\%",
                  font_size=23, color=GREY_A),
            MathTex(r"\text{share} \;=\; \frac{\mu - r}{\gamma\,\sigma^2}", font_size=40, color=UTIL),
            label(r"Merton (1969), \ Samuelson (1969)", font_size=21, color=GREY_B),
            label(rf"$\gamma$ = 1, 2, 4, 10: \ {100 * m['1']:.0f}\%, \ {100 * m['2']:.0f}\%, \ {100 * m['4']:.1f}\%, "
                  rf"\ {100 * m['10']:.0f}\%", font_size=24),
            label(r"with constant relative aversion the share \\ doesn't depend on wealth", font_size=22,
                  color=GREY_A),
            label(r"a premium of 6 points needs only modest aversion \\ to hold a lot of the risky asset: \ "
                  r"Part 23's puzzle", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Insurance sheds risk. The opposite choice is taking it on for a reward. <bookmark mark='a'/> Dara's new "
            "venture returns twenty-eight percent in a good year and loses twelve in a bad one, with equal chances: "
            "eight percent on average, against two percent on a safe deposit. <bookmark mark='b'/> How much of her "
            "wealth should an islander put in? Here is expected utility against the share. With a gamma of two, the "
            "best share is about four fifths; with four, about two fifths. <bookmark mark='c'/> Robert Merton and "
            "Paul Samuelson worked out the general answer in 1969: the share in the risky asset is its premium over "
            "the safe rate, divided by gamma times its variance. Here that's six points over gamma times four "
            "hundredths: a hundred and fifty percent at gamma one, seventy-five at two, fifteen at ten. "
            "<bookmark mark='d'/> With constant relative risk aversion the share doesn't depend on how rich you are. "
            "<bookmark mark='e'/> And notice what it implies: a premium of six points, about what American stocks "
            "have paid over bills, should make people with modest risk aversion hold a lot of stocks. Part twenty-three "
            "takes up the puzzle that prices and consumption then pose."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(curves[0]), FadeIn(tops[0]), Create(curves[1]), FadeIn(tops[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]), FadeIn(side[4]))
            vo.wait_until("d")
            self.play(FadeIn(side[5]))
            vo.wait_until("e")
            self.play(FadeIn(side[6]))
        self.clear_scene()
