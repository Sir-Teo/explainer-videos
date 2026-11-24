from __future__ import annotations

from videos.industry.industry7.common import *  # noqa: F403


def _wrap(s: str, n: int) -> list[str]:
    out, cur = [], ""
    for w in s.split():
        if cur and len(cur) + 1 + len(w) > n:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    return out + [cur]


class Outro(VoiceoverScene):
    def construct(self):
        head = tx("Sizing a market", 40, GOLD, bold=True).to_edge(UP, buff=0.45)
        bottle = draw.bottle(2.6, color=WATER, water=0.2).move_to([-4.6, -0.4, 0])
        level = ValueTracker(0.2)
        bottle.add_updater(lambda b: b[0].stretch_to_fit_height(max(0.01, 2.6 * 0.7 * level.get_value()),
                                                                about_edge=DOWN))
        lines = VGroup(
            tx("First the definition: which level, plants, products, buyers, year.", 22),
            tx("Then two ways to count: top-down from the census,", 22),
            tx("bottom-up from units times a price you must choose.", 22, GREY_A),
            tx("Few firms? Add up their accounts. Many? Count from the top.", 22),
            tx("Compare only on one definition; report a range, and its edges.", 22),
            tx("Split growth in dollars into price and quantity.", 22),
            tx("An addressable market is a dream, not a forecast;", 22),
            tx("an S-curve's ceiling cannot be read from its first years,", 22, GREY_A),
            tx("and a full market is sized by what wears out.", 22, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).move_to([1.8, -0.35, 0])
        groups = [VGroup(lines[0]), VGroup(lines[1], lines[2]), VGroup(lines[3]), VGroup(lines[4]), VGroup(lines[5]),
                  VGroup(lines[6], lines[7], lines[8])]
        with self.voiceover(
            "Sizing a market. <bookmark mark='a'/> Start with the definition: which level of the chain, which "
            "plants, which products, which buyers, which year. <bookmark mark='b'/> Then count it two ways: down from "
            "what the statistical offices count, and up from units times a price you have to choose. "
            "<bookmark mark='c'/> Let the market's structure pick the method: a few big firms, and their own "
            "accounts are the best count there is; thousands of small ones, and only a census will do. "
            "<bookmark mark='d'/> Compare estimates only once they share a definition, and report a range, with "
            "the input that decides its edges. <bookmark mark='e'/> Split every growth rate into price and "
            "quantity. <bookmark mark='f'/> Treat an addressable market as a company's dream, not a forecast; never "
            "trust a ceiling read off the first few years of an S-curve; and remember that once the curve is full, "
            "the market is what wears out. Do that, and the next time someone tells you a market is worth "
            "trillions, you will know the first question to ask: worth trillions of what?"
        ) as vo:
            self.add(bottle)
            self.play(FadeIn(head), FadeIn(bottle))
            for k, m in enumerate("abcdef"):
                vo.wait_until(m)
                self.play(FadeIn(groups[k]), level.animate.set_value(0.2 + 0.13 * (k + 1)), run_time=1.2)
        bottle.clear_updaters()
        self.clear_scene()
        titles = ["Where the Money Goes", "The Economy on One Page", "The Accounts", "The Cost Curve", "The Moat",
                  "The Cycle", "Sizing a Market"]
        icons = [draw.coin_stack(4, r=0.22), draw.skyline(1.4, seed=2), VGroup(*[Rectangle(
            width=0.9, height=0.12, stroke_width=0, fill_color=STONE, fill_opacity=0.8) for _ in range(5)]).arrange(
            DOWN, buff=0.08), VGroup(Line(LEFT * 0.6 + UP * 0.4, ORIGIN + DOWN * 0.3), Line(ORIGIN + DOWN * 0.3, RIGHT * 0.6 +
                                                                                            UP * 0.4)).set_stroke(GOLD, 4),
            draw.castle(1.2, moat=0.25), FunctionGraph(lambda x: 0.35 * np.sin(3 * x), x_range=[-0.8, 0.8],
                                                       color=RETAIL, stroke_width=4),
            draw.bottle(1.0, color=WATER)]
        cards = VGroup()
        for k, (t_, ic) in enumerate(zip(titles, icons)):
            ic.scale_to_fit_height(min(ic.height, 0.9)).scale_to_fit_width(min(ic.width, 1.3))
            box = RoundedRectangle(corner_radius=0.1, width=1.7, height=2.1, stroke_color=GREY_C, stroke_width=1.5,
                                   fill_color="#141A24", fill_opacity=1)
            num = tx(f"Part {k + 1}", 15, GOLD, bold=True)
            nm = VGroup(*[tx(w_, 14, WHITE) for w_ in _wrap(t_, 13)]).arrange(DOWN, buff=0.02)
            inner = VGroup(num, ic, nm).arrange(DOWN, buff=0.18).move_to(box)
            cards.add(VGroup(box, inner))
        cards.arrange(RIGHT, buff=0.15).move_to(UP * 0.3)
        act = tx("Act I: how to read any industry", 26, GREY_B).next_to(cards, UP, buff=0.5)
        nxt = VGroup(tx("Next: Act II, Out of the Ground", 24, GREY_B), tx("Oil and Gas", 56, WHITE, bold=True)).arrange(
            DOWN, buff=0.2).next_to(cards, DOWN, buff=0.55)
        with self.voiceover(
            "That ends the first act of this series. <bookmark mark='a'/> Seven parts on how to read any industry: "
            "where its money goes, its place in the whole economy, its accounts, its cost curve, its moat, its "
            "cycle, and now its size. <bookmark mark='b'/> Every part from here uses these tools on one real "
            "industry. The second act goes out of the ground, starting with the industry the modern economy runs "
            "on: oil and gas."
        ) as vo:
            self.play(FadeIn(act))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.25), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(nxt[0]), FadeIn(nxt[1], scale=1.1), run_time=1.6)
        self.wait(1.0)
        self.clear_scene()
