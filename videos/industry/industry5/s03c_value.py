from __future__ import annotations

from videos.industry.industry5.common import *  # noqa: F403

SHORT = {"Software (Entertainment)": "Software: entertainment", "Software (System & Application)": "Software: systems",
         "Computers/Peripherals": "Computers", "Semiconductor": "Chips", "Healthcare Support Services":
         "Health care support", "Drugs (Pharmaceutical)": "Drugs", "Retail (General)": "Retail: general",
         "Insurance (Prop/Cas.)": "Insurance", "Telecom. Services": "Telecoms",
         "Oil/Gas (Production and Exploration)": "Oil and gas", "Household Products": "Household products"}


class Value(VoiceoverScene):
    def construct(self):
        card(self, 4, "Where the excess profit is", "In dollars, which industries earn the most above their cost?",
             "Chapter four. Where the excess profit is.", lit=("moat", "dollar"))
        E = R["eva"]
        rows = E["rows"]
        pos = [(n, v) for n, v in rows if v > 0]
        top = pos[:11]
        rest = sum(v for _, v in pos[11:])
        cols = ["#B58CFF", "#9D7BEA", "#7EC8F5", "#5DA9E9", "#7BD88F", "#4FC3A1", "#F2A65A", "#E9C46A", "#F6C453",
                "#E8554E", "#C9A26B"]
        items = [(SHORT.get(n, n), v, c, f"${v:.0f}bn") for (n, v), c in zip(top, cols)]
        items.append((f"{len(pos) - len(top)} other industries", rest, "#4A5568", f"${rest:.0f}bn"))
        tm = viz.treemap(items, width=8.0, height=5.0, size=18).move_to([2.15, -0.4, 0])
        eq = MathTex(r"(\text{return} - \text{cost of capital}) \times \text{capital}", font_size=24).move_to(
            [-4.75, 2.2, 0])
        eq_t = tx("profit above what the capital\ncould have earned elsewhere", 18, GREY_B).next_to(eq, DOWN, buff=0.2)
        tot = VGroup(tx("all industries, 2025", 18, GREY_B), tx(f"${E['positive'] / 1000:.2f} trillion", 36, RET, bold=True),
                     tx(f"against ${-E['negative']:.0f}bn of losses below the cost", 17, COST_)).arrange(
            DOWN, buff=0.08).move_to([-4.75, -0.3, 0])
        five = tx(f"five industries: {100 * E['top5_share']:.0f}% of it", 22, GOLD, bold=True).move_to([-4.75, -2.2, 0])
        src = source("Damodaran, Excess Returns (EVA) by industry, US companies, 2025: this film's arithmetic, $bn",
                     size=13)
        names = [SHORT.get(n, n) for n, _ in top[:5]]
        with self.voiceover(
            "A percentage hides how much money is at stake. <bookmark mark='a'/> Multiply each industry's return "
            "above its cost of capital by the capital it uses, and you get its profit above what that capital "
            "could have earned anywhere else. Economists call it economic profit. <bookmark mark='b'/> For "
            f"American companies in 2025 it came to about {E['positive'] / 1000:.1f} trillion dollars, against "
            f"about {-E['negative']:.0f} billion lost by the industries that earned less than their cost. "
            "<bookmark mark='c'/> And it is not spread evenly. Each block is an industry's share. "
            f"<bookmark mark='d'/> Five industries, {names[0].lower()}, {names[1].lower()}, computers, chips and "
            f"health care support, earn {100 * E['top5_share']:.0f} percent of it. The castles with the deepest "
            "moats in the American economy are, overwhelmingly, the ones built from software and silicon. Notice "
            "what they share with Part 4: software costs almost nothing to copy once written, and the leading chip "
            "and computer makers sit furthest down their learning curves. The cost curve and the moat are "
            "often the same thing seen from two sides."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(eq_t))
            vo.wait_until("b")
            self.play(FadeIn(tot, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b, scale=0.9) for b in tm], lag_ratio=0.08), run_time=2.6)
            vo.wait_until("d")
            self.play(FadeIn(five), *[Indicate(tm[i], color=WHITE, scale_factor=1.04) for i in range(5)])
        self.clear_scene()
