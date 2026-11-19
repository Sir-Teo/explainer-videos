from __future__ import annotations

from videos.economics.econ18.common import *  # noqa: F403

RATE_COLOR = {"0.014": WELF, "0.03": MONEY, "0.045": CYCLE}


class CBA(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Cost-benefit analysis as applied social choice", r"When a government adds up gains and losses "
             r"in money, \ which social welfare function is it using?",
             "Chapter ten. Cost-benefit analysis as applied social choice.",
             lit={1844: r"Dupuit", 1928: r"Ramsey", 2006: r"Stern"}, scale=("community", "nation", "world"),
             horizon=("a decade", "a century"))
        self.jetty()
        self.ought()
        self.discount()

    def jetty(self):
        c = load("cba")
        (wa, ya, ga), (wf, yf, gf) = c["who"]
        people = VGroup(
            VGroup(islander(wa, 0.8, name=True), label(rf"income {ya:.0f}", font_size=19, color=GREY_A),
                   label(rf"gains {ga:.0f} baskets' worth", font_size=21, color=WELF)).arrange(DOWN, buff=0.1),
            VGroup(islander(wf, 0.8, name=True), label(rf"income {yf:.0f}", font_size=19, color=GREY_A),
                   label(rf"loses {-gf:.0f}", font_size=21, color=CYCLE)).arrange(DOWN, buff=0.1),
        ).arrange(RIGHT, buff=2.4).move_to(UP * 1.7)
        head = label(r"a new jetty: \ what each would pay for it, \ or must be paid to accept it", font_size=25,
                     color=E.ACCENT).to_edge(UP, buff=0.3)
        n = c["net"]
        rows = VGroup(
            label(rf"unweighted: \ ${ga:.0f} - {-gf:.0f} = {n['0.0']['net']:+.0f}$: \ build it \ (Kaldor and Hicks, "
                  rf"in money)", font_size=22, color=MONEY),
            label(r"but a basket means more to someone with five than to someone with eighty", font_size=22,
                  color=GREY_A),
            label(rf"weights (mean income $/$ own income)$^\varepsilon$, \ $\varepsilon = \tfrac12$: \ "
                  rf"${n['0.5']['weights'][0]:.2f} \times {ga:.0f} - {n['0.5']['weights'][1]:.2f} \times {-gf:.0f} = "
                  rf"{n['0.5']['net']:.1f}$", font_size=21, color=WELF),
            label(rf"$\varepsilon = 1$: \ ${n['1.0']['weights'][0]:.2f} \times {ga:.0f} - {n['1.0']['weights'][1]:.1f}"
                  rf" \times {-gf:.0f} = {n['1.0']['net']:.1f}$: \ don't build it", font_size=21, color=RAWLS),
            label(r"the case for no weights: \ redistribute with taxes, \ judge projects by efficiency \ (Kaplow and "
                  r"Shavell)", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.28).next_to(people, DOWN, buff=0.45)
        tag = published_tag(r"Kaplow and Shavell, J.\ Legal Stud.\ 23(2) (1994)", corner=DR, font_size=13)
        with self.voiceover(
            "Cost-benefit analysis is social choice done with money. The island considers a new jetty. "
            "<bookmark mark='a'/> Ana, the richest, would pay up to thirty baskets for it; Friday, the poorest, "
            "would lose ten baskets' worth of fishing ground. <bookmark mark='b'/> The usual analysis adds the money: "
            "thirty minus ten is twenty, so build it. That is Kaldor and Hicks's test, in money. "
            "<bookmark mark='c'/> But willingness to pay depends on what you have. A basket means more to someone "
            "with five than to someone with eighty. <bookmark mark='d'/> Weight each person's money by Atkinson's "
            "rule: mean income over their own, raised to epsilon. At epsilon a half, the jetty's net value turns "
            f"negative, {say_num(n['0.5']['net'], 1)}. <bookmark mark='e'/> At epsilon one, it is "
            f"{say_num(n['1.0']['net'], 0)}: don't build it. <bookmark mark='f'/> The case for leaving the weights "
            "out, made by Louis Kaplow and Steven Shavell, is that taxes redistribute more cheaply than distorted "
            "projects do, so projects should be judged on efficiency alone. Its force depends on whether the taxes "
            "really follow."
        ) as vo:
            self.play(FadeIn(head), FadeIn(people[0]), FadeIn(people[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            for mk, r in zip("cdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def ought(self):
        io = is_ought_card(
            r"the jetty adds 30 baskets' worth for Ana and costs Friday 10; \ unweighted, \ it gains 20",
            r"whether the island should build it",
            r"how much a basket to Friday counts against a basket to Ana \ ($\varepsilon$), \ and whether Friday "
            r"will in fact be compensated",
            width=12.0, font_size=24).move_to(UP * 0.1)
        with self.voiceover(
            "This is where the measuring stops and a judgment begins. <bookmark mark='a'/> Economics can measure "
            "the jetty: thirty baskets' worth for Ana, ten lost by Friday, twenty gained in all. "
            "<bookmark mark='b'/> Whether to build it needs a judgment about how much a basket to Friday counts "
            "against a basket to Ana, which is epsilon, and about whether Friday will in fact be compensated. "
            "<bookmark mark='c'/> An analysis that uses no weights has still made a choice: epsilon zero."
        ) as vo:
            self.play(FadeIn(io.card), FadeIn(io.is_row))
            vo.wait_until("b")
            self.play(FadeIn(io.judgment), FadeIn(io[1][1]))
            vo.wait_until("c")
            self.play(FadeIn(io.ought), FadeIn(io[1][3]))
        self.clear_scene()

    def discount(self):
        d = load("discount")
        yrs = np.array(d["years_axis"], float)
        ax = plane([0, 100], [0, 1], center=LEFT * 2.6 + DOWN * 0.45, x_length=6.6, y_length=4.4,
                   xticks=[0, 25, 50, 75, 100], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"years from now", ylabel=r"value today of 1 dollar then", font_size=18)
        curves = VGroup(*[path(ax, yrs, d["curves"][k], color=RATE_COLOR[k], width=4) for k in RATE_COLOR])
        ram = MathTex(r"r = \delta + \eta\, g", font_size=44, color=WHITE).to_edge(UP, buff=0.35)
        parts = label(r"$\delta$: \ impatience \quad $\eta$: \ how fast utility flattens \quad $g$: \ growth",
                      font_size=21, color=GREY_A).next_to(ram, DOWN, buff=0.15)
        rows = VGroup(label(rf"one million dollars, \ {d['years']} years away, \ is worth today:", font_size=21))
        names = {"0.014": r"Stern's 1.4\%", "0.03": r"3\%", "0.045": r"4.5\%"}
        for k in RATE_COLOR:
            rows.add(label(rf"at {names[k]}: \ " + dollars(d["pv"][k], 0), font_size=22, color=RATE_COLOR[k]))
        rows.add(label(r"a factor of twenty, \ from the rate alone", font_size=21, color=E.ACCENT))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(ax, RIGHT, buff=0.5).shift(UP * 0.2)
        foot = label(r"$\delta$ and $\eta$ are ethical choices; \ part forty-eight puts them to work on the climate",
                     font_size=21, color=GREY_A).to_edge(DOWN, buff=0.25)
        tag = published_tag(r"Ramsey, EJ 38(152) (1928); \ Stern, \emph{The Economics of Climate Change} (2007)",
                            corner=DR, font_size=12).shift(UP * 0.45)
        pv = d["pv"]
        with self.voiceover(
            "The same judgment reaches across time. Gains in a century must be set against costs today, and the "
            "tool is the discount rate. <bookmark mark='a'/> Frank Ramsey's formula from 1928 splits it into two "
            "parts: delta, pure impatience, and eta times g, where g is growth and eta is the epsilon of this part, "
            "now saying how much less an extra dollar means to a richer future. "
            "<bookmark mark='b'/> Nicholas Stern's review of climate change in 2006 set delta near zero, at nought "
            "point one percent, eta at one and growth at one point three percent: a rate of one point four "
            "percent. <bookmark mark='c'/> At that rate, a million dollars a hundred years away is worth about "
            f"{pv['0.014'] / 1000:.0f} thousand today. At three percent, about {pv['0.03'] / 1000:.0f} thousand. At "
            f"four and a half percent, near the market returns that William Nordhaus argued for, about "
            f"{pv['0.045'] / 1000:.0f} thousand. <bookmark mark='d'/> A factor of twenty, from the rate alone. "
            "<bookmark mark='e'/> Delta and eta are ethical choices, not facts waiting to be measured. Part "
            "forty-eight puts them to work on the climate."
        ) as vo:
            self.play(FadeIn(ram), FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(parts))
            vo.wait_until("b")
            self.play(Create(curves[0]), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            self.play(Create(curves[1]), FadeIn(rows[2]))
            self.play(Create(curves[2]), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
