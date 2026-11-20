from __future__ import annotations

from videos.economics.econ34.common import *  # noqa: F403


class MF(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Mundell-Fleming and the trilemma", r"What can policy do when capital moves freely?",
             "Chapter six. Mundell-Fleming and the trilemma.", lit={1962: r"Fleming", 1963: r"Mundell"},
             scale=("nation", "world"), horizon=("a year",))
        self.model()
        self.table()
        self.triangle()

    def model(self):
        eqs = VGroup(
            label(r"Part 27's IS-LM, \ opened to the world", font_size=26, color=E.ACCENT),
            MathTex(r"\text{IS:}\quad Y = C(Y) + I(r) + G + NX(e)", font_size=36, color=WHITE),
            MathTex(r"\text{LM:}\quad M/P = L(Y, r)", font_size=36, color=WHITE),
            MathTex(r"\text{capital moves freely:}\quad r = r^{*}", font_size=36, color=USD),
            label(r"$e$: \ the price of foreign currency; \ a higher $e$ makes home goods cheaper abroad", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"Mundell, \ \emph{Canadian Journal of Economics and Political Science} 29(4) (1963); "
                            r"\ Fleming, \ \emph{IMF Staff Papers} 9(3) (1962)", corner=DR, font_size=12)
        with self.voiceover(
            "Robert Mundell and Marcus Fleming, in the early 1960s, opened Part twenty-seven's IS-LM model to the "
            "world. <bookmark mark='a'/> Spending now includes net exports, which rise when the currency is cheap. "
            "<bookmark mark='b'/> Money demand is as before. <bookmark mark='c'/> And with capital free to move, a "
            "small country's interest rate cannot differ from the world's: any gap would bring a flood of money in "
            "or out. <bookmark mark='d'/> What adjusts depends on the exchange-rate regime."
        ) as vo:
            self.play(FadeIn(eqs[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", eqs[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def table(self):
        F = load("mf")
        fl, fx = F["floating"], F["fixed"]
        cards = point_cards([
            (r"floating: \ spend more", rf"the rate would rise; \ capital flows in; \\ the currency rises "
                                         rf"({fl['fiscal']['e']:+.1f}); \\ net exports fall: \ output "
                                         rf"{fl['fiscal']['y']:+.1f}", CRISIS),
            (r"floating: \ print more", rf"the rate would fall; \ capital flows out; \\ the currency falls "
                                         rf"({fl['money']['e']:+.1f}); \\ net exports rise: \ output "
                                         rf"{fl['money']['y']:+.1f}", CALM),
            (r"fixed: \ spend more", rf"the bank must supply money \\ to hold the rate: \\ output "
                                      rf"{fx['fiscal']['y']:+.1f}, \ the full multiplier", CALM),
            (r"fixed: \ print more", r"the new money buys foreign assets \\ from the bank's reserves \\ and leaves: \ "
                                      r"output $+0.0$", CRISIS),
        ], width=12.4, cols=2, font_size=21).move_to(DOWN * 0.2)
        head = label(r"a unit of policy, \ in a small open economy \ (the Island's numbers)", font_size=24,
                     color=E.ACCENT).to_edge(UP, buff=0.4)
        tag = island_tag(corner=DR, font_size=13)
        with self.voiceover(
            "Four experiments, each with one unit of policy, on the Island. <bookmark mark='a'/> With a floating "
            "currency, government spending would push up the interest rate; money flows in, the currency rises, net "
            "exports fall, and output ends where it began: fiscal policy is powerless. <bookmark mark='b'/> Monetary "
            "policy is strong: the currency falls and net exports rise. <bookmark mark='c'/> With a fixed rate, the "
            "results flip. Spending works with the full multiplier, because the central bank must supply whatever "
            "money holds the rate. <bookmark mark='d'/> And monetary policy does nothing: new money just buys "
            "foreign currency from the bank's reserves and leaves. A country with a peg has handed its monetary "
            "policy to the country it pegs to, which is exactly the position Britain was in, with Germany."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def triangle(self):
        A, B, C = UP * 2.3, DOWN * 1.6 + LEFT * 3.4, DOWN * 1.6 + RIGHT * 3.4
        tri = Polygon(A, B, C, stroke_color=GREY_B, stroke_width=3)
        corners = VGroup(
            label(r"a fixed exchange rate", font_size=22, color=DEM).next_to(A, UP, buff=0.15),
            label(r"free capital flows", font_size=22, color=USD).next_to(B, DOWN, buff=0.2),
            label(r"its own monetary policy", font_size=22, color=CALM).next_to(C, DOWN, buff=0.2),
        )
        sides = VGroup(
            label(r"the euro area's members; \\ Hong Kong", font_size=18, color=GREY_A).next_to((A + B) / 2, LEFT,
                                                                                            buff=0.3),
            label(r"China, \ Bretton Woods: \\ capital controls", font_size=18, color=GREY_A).next_to((A + C) / 2,
                                                                                                RIGHT, buff=0.3),
            label(r"America, \ Britain since 1992: \ floating", font_size=18, color=GREY_A).next_to((B + C) / 2, DOWN,
                                                                                               buff=0.75),
        )
        head = label(r"the trilemma: \ pick two", font_size=30, color=E.ACCENT).to_corner(UL, buff=0.5)
        uk = label(r"Britain in 1992 \\ tried all three", font_size=20, color=CRISIS).to_corner(UR, buff=0.6)
        with self.voiceover(
            "The model's lesson is a triangle, the trilemma. <bookmark mark='a'/> A country can have a fixed "
            "exchange rate, free movement of capital, and a monetary policy of its own, but only two of the three. "
            "<bookmark mark='b'/> Fix the rate and keep capital free, like the euro's members or Hong Kong, and "
            "interest rates are set abroad. <bookmark mark='c'/> Fix the rate and keep your own policy, like China "
            "or the world of Bretton Woods, and you need capital controls. <bookmark mark='d'/> Keep capital free "
            "and your own policy, like America, and the currency must float. <bookmark mark='e'/> In 1992 Britain "
            "had a peg and free capital, and wanted lower interest rates than Germany's. It could not have all "
            "three, and on Black Wednesday the markets made it choose."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(tri), FadeIn(corners), run_time=1.5)
            for mk, sd in zip("bcd", sides):
                vo.wait_until(mk)
                self.play(FadeIn(sd))
            vo.wait_until("e")
            self.play(FadeIn(uk))
        self.clear_scene()
