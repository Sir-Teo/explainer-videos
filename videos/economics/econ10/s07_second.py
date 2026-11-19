from __future__ import annotations

from videos.economics.econ10.common import *  # noqa: F403

DECK = "#9FB8F2"
CABIN = "#F6C453"


class SecondDegree(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Second-degree discrimination: \ menus that sort", r"If the seller can't tell buyers apart, how "
             r"can she charge them differently?", "Chapter six. Second-degree discrimination: menus that sort.",
             lit={1978: r"Mussa and Rosen"})
        self.problem()
        self.menu()
        self.damaged()

    def problem(self):
        s = load("screen")
        rows = VGroup(
            label(r"two kinds of passenger, \ who look the same", font_size=27),
            label(rf"most ({100 * (1 - s['share_hi']):.0f}\%) value comfort $q$ at $1 \times q$; \ "
                  rf"some ({100 * s['share_hi']:.0f}\%) at $2 \times q$", font_size=25),
            label(r"comfort costs Bo $q^2/2$ to provide", font_size=25, color=GREY_A),
            label(r"if Bo could tell them apart: \ deck with comfort 1 for \$1, \ cabin with comfort 2 for \$4",
                  font_size=24, color=GREY_A),
            label(r"but then the comfort-lovers buy the deck: \ $2 \times 1 - 1 = 1$, \ better than $2 \times 2 - 4 = 0$",
                  font_size=24, color=HOLD),
        ).arrange(DOWN, buff=0.38).to_edge(UP, buff=0.8)
        with self.voiceover(
            "Often the seller can't see who is who. <bookmark mark='a'/> Suppose Bo's passengers come in two kinds "
            "that look alike. <bookmark mark='b'/> Seven in ten care a little about comfort, and value it at one "
            "dollar a unit; three in ten care twice as much. <bookmark mark='c'/> Comfort costs Bo the square of the "
            "amount, halved. <bookmark mark='d'/> If he could tell them apart, he would give each kind the comfort "
            "that's worth its cost to them, and charge them its whole value: a deck seat with one unit for a "
            "dollar, and a cabin with two units for four dollars. <bookmark mark='e'/> But he can't. And at those "
            "prices the comfort-lovers would buy the deck seat: it gives them a dollar of surplus, the cabin none."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def menu(self):
        s = load("screen")
        ax = plane([0, 2.4], [0, 5], center=LEFT * 3.2 + DOWN * 0.3, x_length=5.6, y_length=5.0,
                   xticks=[0, 0.5, 1, 1.5, 2], yticks=[0, 1, 2, 3, 4, 5], xlabel=r"comfort $q$", ylabel=r"\$",
                   font_size=17)
        a = ax.ax
        qs = np.linspace(0, 2.4, 100)
        lo = path(ax, qs, 1.0 * qs, color=DECK, width=3)
        hi = path(ax, qs, 2.0 * qs, color=CABIN, width=3)
        cost = path(ax, qs, qs ** 2 / 2, color=GREY_B, width=2.5)
        full = VGroup(Dot(a.c2p(1, 1), radius=0.07, color=GREY_B), Dot(a.c2p(2, 4), radius=0.07, color=GREY_B))

        def key(mob, text, col):
            return VGroup(mob, label(text, font_size=16, color=col)).arrange(RIGHT, buff=0.12)

        names = VGroup(
            key(Line(ORIGIN, RIGHT * 0.4, color=CABIN, stroke_width=3), r"$2q$: \ what a comfort-lover pays", CABIN),
            key(Line(ORIGIN, RIGHT * 0.4, color=DECK, stroke_width=3), r"$q$: \ what the others pay", DECK),
            key(Line(ORIGIN, RIGHT * 0.4, color=GREY_B, stroke_width=2.5), r"$q^2/2$: \ what comfort costs", GREY_B),
            key(Dot(radius=0.07, color=GREY_B), r"the menu if types were seen", GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        names.move_to(a.c2p(0.1, 4.95), aligned_edge=UL)
        rl = label(r"rent", font_size=16, color=HOLD).next_to(a.c2p(s["qH"], (s["pH"] + 4.0) / 2), RIGHT, buff=0.1)
        dL = Dot(a.c2p(s["qL"], s["pL"]), radius=0.1, color=DECK)
        dH = Dot(a.c2p(s["qH"], s["pH"]), radius=0.1, color=CABIN)
        rent = Line(a.c2p(s["qH"], s["pH"]), a.c2p(s["qH"], 4.0), color=HOLD, stroke_width=5)
        side = VGroup(
            label(r"value lines: \ $1 \times q$ \ and \ $2 \times q$; \ cost $q^2/2$", font_size=21, color=GREY_A),
            label(rf"the menu: \ deck, \ comfort {s['qL']:.2f}, \ \${s['pL']:.2f}", font_size=23, color=DECK),
            label(rf"cabin, \ comfort {s['qH']:.0f}, \ \${s['pH']:.2f}", font_size=23, color=CABIN),
            label(r"no distortion at the top: \ the cabin is as good as it should be", font_size=21),
            label(r"the deck is made worse on purpose: \\ so the cabin's buyers aren't tempted", font_size=21,
                  color=HOLD),
            label(rf"their information rent: \ \${s['rent']:.2f}; \ Bo's profit \${s['profit']:.2f} a passenger, \\ "
                  rf"against \${s['profit_full_info']:.2f} if he could see types", font_size=21, color=PROFIT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "So Bo designs a menu that makes passengers sort themselves. <bookmark mark='a'/> These lines are what "
            "each kind would pay for each level of comfort, and the curve is what it costs. <bookmark mark='b'/> "
            "The best menu offers a deck seat with comfort of only nought point five seven, for fifty-seven cents, "
            "<bookmark mark='c'/> and a cabin with comfort two, for three dollars forty-three. "
            "<bookmark mark='d'/> The cabin is exactly as comfortable as it would be if Bo could see types: there's "
            "no distortion at the top. <bookmark mark='e'/> But the deck is made worse than it should be, so that "
            "the comfort-lovers aren't tempted down to it. <bookmark mark='f'/> They still keep fifty-seven cents "
            "of surplus, their information rent, which is the price of not being seen. Bo earns seventy-one cents a "
            "passenger, against ninety-five if he could tell them apart. Michael Mussa and Sherwin Rosen worked out "
            "the general case in 1978."
        ) as vo:
            self.play(FadeIn(ax), Create(lo), Create(hi), Create(cost), FadeIn(full), FadeIn(names), FadeIn(tag),
                      FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(dL, scale=0.5), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(dH, scale=0.5), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(Create(rent), FadeIn(rl), FadeIn(side[5]))
        self.clear_scene()

    def damaged(self):
        hc = history_card(1996, r"Raymond Deneckere and Preston McAfee", r"``Damaged Goods'': \ firms that spend money "
                          r"to make a cheaper version of a product worse", color=HOLD, width=11.0,
                          font_size=24).to_edge(UP, buff=0.6)
        rows = VGroup(
            label(r"a printer sold cheaper, \ slowed down by an extra part; \ a chip sold with a feature switched "
                  r"off", font_size=24),
            label(r"Dupuit's carriages: \ a roof left off third class \ to keep second-class passengers", font_size=24,
                  color=GREY_A),
            label(r"damaging the cheap version can even help everyone: \\ it can bring buyers in who would otherwise "
                  r"get nothing", font_size=24, color=CS),
            label(r"screening returns in Parts 13 and 14, \ where the hidden thing is quality or effort", font_size=23,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.4).next_to(hc, DOWN, buff=0.6)
        tag = published_tag(r"Deneckere and McAfee, Journal of Economics and Management Strategy 5(2) (1996)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "That deliberate damage is real, and common. <bookmark mark='a'/> Raymond Deneckere and Preston McAfee "
            "collected cases in 1996: firms that sold a cheaper version of a printer that was the dear one slowed "
            "down by an extra part, or a chip with a working feature switched off. <bookmark mark='b'/> It's "
            "Dupuit's third-class carriage again. <bookmark mark='c'/> And it isn't simply bad for buyers: offering a "
            "damaged version can bring in customers who would otherwise buy nothing at all. "
            "<bookmark mark='d'/> Screening, designing a menu so that people reveal what you can't see, comes back "
            "in Parts thirteen and fourteen."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.2))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
