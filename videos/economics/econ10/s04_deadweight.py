from __future__ import annotations

from videos.economics.econ10.common import *  # noqa: F403


class Deadweight(VoiceoverScene):
    def construct(self):
        card(self, 3, r"What monopoly costs: \ Harberger's triangles \ and Posner's rectangles", r"How much does "
             r"market power cost an economy?", "Chapter three. What monopoly costs: Harberger's triangles and Posner's "
             "rectangles.", lit={1954: r"Harberger's triangles"}, scale=("market", "nation"))
        self.triangle()
        self.harberger()
        self.posner()

    def triangle(self):
        m = load("monopoly")
        ax = plane([0, 100], [0, 10], center=LEFT * 2.9 + DOWN * 0.3, x_length=6.4, y_length=5.0,
                   xticks=[0, 25, 50, 75, 100], yticks=[0, 5, 10], xlabel=r"crossings a day", ylabel=r"\$ a crossing",
                   font_size=17)
        dem = path(ax, m["qs"], m["p_of_q"], color=DEM, width=3.5, smooth=False)
        q, p = m["q"], m["p"]
        cs = region(ax, [(0, p), (q, p), (0, 10)], CS, 0.35)
        prof = region(ax, [(0, 0), (q, 0), (q, p), (0, p)], PROFIT, 0.3)
        dwl = region(ax, [(q, 0), (100, 0), (q, p)], DWL, 0.45)
        side = VGroup(
            label(rf"at a fare of \${p:.0f}: \ Bo's takings \${m['profit']:.0f} a day", font_size=23, color=PROFIT),
            label(rf"the passengers' surplus: \ \${m['cs']:.0f}", font_size=23, color=CS),
            label(rf"the deadweight loss: \ \${m['dwl']:.0f}, \\ crossings worth more than they cost, \ not made",
                  font_size=23, color=DWL),
            label(rf"at a fare equal to cost, \ every \${m['cs_competitive']:.0f} would go to passengers", font_size=22,
                  color=GREY_A),
            label(r"the takings are a transfer; \ only the triangle is a loss", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.45)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Now the cost. <bookmark mark='a'/> At Bo's fare of five dollars, his takings are two hundred and fifty "
            "dollars a day. <bookmark mark='b'/> The passengers who cross get a surplus of a hundred and twenty-"
            "five: what crossing is worth to them, above the fare. <bookmark mark='c'/> And this triangle is the "
            "deadweight loss: crossings worth more than they cost, which are not made, another hundred and twenty-"
            "five dollars. <bookmark mark='d'/> At a fare equal to cost, all five hundred dollars of value would go "
            "to the passengers. <bookmark mark='e'/> The takings are a transfer from passengers to Bo; whether that "
            "is fair is another question. The loss to the economy as a whole is the triangle."
        ) as vo:
            self.play(FadeIn(ax), Create(dem), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(prof), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(cs), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(dwl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), Indicate(dwl, color=DWL))
        self.clear_scene()

    def harberger(self):
        hc = history_card(1954, r"Arnold Harberger", r"``Monopoly and Resource Allocation'': \ add up the triangles "
                          r"for American manufacturing", color=DWL, width=11.0, font_size=24).to_edge(UP, buff=0.6)
        rows = VGroup(
            label(r"profit rates by industry, \ above the average, \ as markups; \ an elasticity of demand of 1",
                  font_size=24),
            label(r"the triangles came to less than a tenth of one percent of national income", font_size=26,
                  color=DWL),
            label(r"``Harberger's triangles'': \ the standard view for twenty years \\ was that monopoly costs little",
                  font_size=25, color=GREY_A),
            label(r"the triangle is small: \ half of a small markup times a small loss of output", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.4).next_to(hc, DOWN, buff=0.6)
        tag = published_tag(r"Harberger, American Economic Review 44(2) (1954); the figure as reported by later surveys",
                            corner=DR, font_size=13)
        with self.voiceover(
            "How big are such triangles in a real economy? <bookmark mark='a'/> In 1954 Arnold Harberger added them "
            "up for American manufacturing. He took the profit rates of industries above the average as their "
            "markups, and assumed an elasticity of demand of one. <bookmark mark='b'/> The total came to less than "
            "a tenth of one percent of national income. <bookmark mark='c'/> For two decades that was the standard "
            "view: monopoly, whatever else is wrong with it, costs the economy very little. <bookmark mark='d'/> "
            "The reason is arithmetic: the triangle is half the markup times the output lost, and both are small "
            "numbers, so their product is tiny."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.2))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def posner(self):
        m = load("monopoly")
        hc = history_card(1975, r"Richard Posner", r"``The Social Costs of Monopoly and Regulation'': \ the profit "
                          r"is a prize, \ and the competition to win it uses up resources", color=PROFIT, width=11.0,
                          font_size=24).to_edge(UP, buff=0.6)
        rows = VGroup(
            label(r"licences, \ lobbying, \ lawyers, \ advertising to deter rivals: \ rent-seeking", font_size=25),
            label(r"if firms compete for the monopoly until the prize is spent, \\ the whole profit rectangle is "
                  r"wasted, \ not just the triangle", font_size=24, color=PROFIT),
            label(rf"for Bo's ferry: \ the loss could be \${m['dwl']:.0f} \ or \${m['dwl'] + m['profit']:.0f} a "
                  r"day, \ depending on how he got it", font_size=24, color=DWL),
            label(r"Tullock (1967) had seen it first; \ so the cost of monopoly depends on how it arises", font_size=23,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.4).next_to(hc, DOWN, buff=0.6)
        tag = published_tag(r"Posner, Journal of Political Economy 83(4) (1975); Tullock, Western Economic Journal "
                            r"5(3) (1967)", corner=DR, font_size=13)
        with self.voiceover(
            "Then Richard Posner, in 1975, pointed at the rectangle. <bookmark mark='a'/> A monopoly's profit is a "
            "prize, and firms spend real resources to win prizes: on licences, lobbying, lawyers, and advertising "
            "meant to keep rivals out. Economists call it rent-seeking. <bookmark mark='b'/> If firms compete for "
            "the prize until they've spent what it's worth, the whole profit rectangle is wasted, not just the "
            "triangle. <bookmark mark='c'/> For Bo's ferry, the loss to the Island could be a hundred and twenty-five "
            "dollars a day, or three hundred and seventy-five, depending on how he came by his monopoly. "
            "<bookmark mark='d'/> Gordon Tullock had made the same point in 1967. The cost of market power depends "
            "on how it is won, which is why competition policy cares about that too."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.2))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
