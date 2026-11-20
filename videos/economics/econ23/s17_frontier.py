from __future__ import annotations

from videos.economics.econ23.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ the return on everything", r"What have the world's assets paid over a century and "
             r"a half?", "Chapter fifteen. Frontier: the return on everything.",
             lit={2019: r"Jordà et al.", 2013: r"He and Krishnamurthy", 2014: r"Adrian, Etula, Muir"},
             scale=("world",), horizon=("a century",))
        self.everything()
        self.intermediaries()
        self.open()

    def everything(self):
        rows = [(r"housing", 0.07, 0.08, HOUSE), (r"equities", 0.07, 0.07, STOCK), (r"government bonds", 0.025, 0.025,
                                                                                       BILL),
                (r"bills", 0.01, 0.01, SDF)]
        ax = plane([0.4, 4.6], [0, 0.09], center=LEFT * 1.8 + DOWN * 0.5, x_length=7.6, y_length=4.6, xticks=[],
                   yticks=[0, 0.02, 0.04, 0.06, 0.08], ylabel=r"average real return a year, \ 16 countries, \ "
                   r"1870--2015", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=15)
        bars = VGroup()
        for k, (name, lo, hi, col) in enumerate(rows):
            x = k + 1
            b = Rectangle(width=ax.ax.c2p(x + 0.3, 0)[0] - ax.ax.c2p(x - 0.3, 0)[0],
                          height=ax.ax.c2p(0, lo)[1] - ax.ax.c2p(0, 0)[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to(ax.ax.c2p(x, 0), aligned_edge=DOWN)
            nm = label(name, font_size=18, color=col).next_to(ax.ax.c2p(x, 0), DOWN, buff=0.15)
            txt = (rf"about {100 * lo:.0f}--{100 * hi:.0f}\%" if hi != lo else rf"about {100 * lo:g}\%")
            val = label(txt, font_size=17, color=col).next_to(b, UP, buff=0.08)
            bars.add(VGroup(b, nm, val))
        side = VGroup(
            label(r"Òscar Jordà, \ Katharina Knoll, \\ Dmitry Kuvshinov, \ Moritz \\ Schularick, \ Alan Taylor, \ "
                  r"2019", font_size=18, color=E.ACCENT),
            label(r"housing matches equities, \\ with far less volatility", font_size=19, color=HOUSE),
            label(r"risky returns well above \\ growth for most of the \\ period: \ $r > g$", font_size=19,
                  color=WHITE),
            label(r"safe returns low, \ and \\ sometimes below growth", font_size=19, color=BILL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Jordà, Knoll, Kuvshinov, Schularick and Taylor, QJE 134(3) (2019); \ NBER WP 24112",
                            corner=DR, font_size=12)
        with self.voiceover(
            "The frontier has widened the data from America to the world. <bookmark mark='a'/> Òscar Jordà, "
            "Katharina Knoll, Dmitry Kuvshinov, Moritz Schularick and Alan Taylor assembled total returns on "
            "housing, equities, government bonds and bills for sixteen rich countries from 1870 to 2015. "
            "<bookmark mark='b'/> Equities returned about seven percent a year after inflation. Housing returned as "
            "much or a little more, about seven to eight, with far less volatility. Bonds about two and a half, "
            "bills about one. <bookmark mark='c'/> The return on risky wealth was well above the growth rate for "
            "most of the period, the inequality that Part forty takes up. <bookmark mark='d'/> The safe rate was "
            "low, and sometimes below growth: Tirole's condition, and Part thirty-two's question of whether "
            "governments can borrow for free."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(*[GrowFromEdge(b[0], DOWN) for b in bars], *[FadeIn(b[1:]) for b in bars])
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def intermediaries(self):
        rows = VGroup(
            label(r"intermediary asset pricing", font_size=28, color=E.ACCENT),
            label(r"the marginal buyer of many assets is not a household but a bank or a dealer", font_size=23,
                  color=GREY_A),
            label(r"so the discount factor that matters may be the intermediaries': \ their capital and leverage",
                  font_size=23, color=SDF),
            label(r"Zhiguo He and Arvind Krishnamurthy, \ 2013; \ Tobias Adrian, \ Erkko Etula and Tyler Muir, \ 2014",
                  font_size=21, color=GREY_B),
            label(r"when intermediaries are short of capital, \ risk premia jump: \ 2008 \ (Parts 26 and 33)",
                  font_size=23, color=RISK),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"He and Krishnamurthy, AER 103(2) (2013); \ Adrian, Etula and Muir, JF 69(6) (2014)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "A second frontier asks whose marginal utility prices assets. <bookmark mark='a'/> For many markets the "
            "marginal buyer is not a household but a bank or a dealer. <bookmark mark='b'/> Then the discount factor "
            "that matters is theirs, and it moves with their capital and leverage. <bookmark mark='c'/> Zhiguo He "
            "and Arvind Krishnamurthy built the theory; Tobias Adrian, Erkko Etula and Tyler Muir found that dealers' "
            "leverage prices a wide range of portfolios. <bookmark mark='d'/> When intermediaries run short of "
            "capital, risk premia jump, as they did in 2008: Parts twenty-six and thirty-three."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def open(self):
        cards = point_cards([
            (r"which repair?", r"habits, \ long-run risk \\ or disasters, \ or all three?", RISK),
            (r"whose discount factor?", r"households, \ intermediaries, \\ or beliefs?", SDF),
            (r"investment and $q$", r"why investment tracks \\ cash flow more than $q$", FIRM),
            (r"low safe rates", r"$r < g$: \ bubbles, \\ debt and secular stagnation", BILL),
        ], width=12.4, cols=2, font_size=22).move_to(DOWN * 0.2)
        head = label(r"open questions", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Open questions. <bookmark mark='a'/> Which repair of the puzzle is right: habits, long-run risk, "
            "disasters, or some of each? <bookmark mark='b'/> Whose discount factor prices assets: households', "
            "intermediaries', or simply beliefs that are wrong? <bookmark mark='c'/> Why does investment track cash "
            "flow more closely than q, as the theory says it should not? <bookmark mark='d'/> And what low safe "
            "rates mean for bubbles, for public debt, and for the stagnation that Part thirty-one takes up."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
