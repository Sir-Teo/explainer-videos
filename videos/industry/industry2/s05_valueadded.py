from __future__ import annotations

from videos.industry.industry2.common import *  # noqa: F403


class ValueAdded(VoiceoverScene):
    def construct(self):
        card(self, 5, "The economy by value added", "Which industries make the most of what America produces?",
             "Chapter five. The economy by value added.", lit=("unit",))
        self.map()
        self.changes()

    def map(self):
        secs = R["va"][1:]
        tm = viz.treemap([(short(d["sector"]), d["va"], gcol(d["sector"]), f"{d['pct']:.1f}%") for d in secs],
                         11.6, 5.6, 20).move_to(DOWN * 0.35)
        order = sorted(range(len(secs)), key=lambda i: -secs[i]["va"])
        head = VGroup(TB(f"${R['gdp']:.1f} trillion", 30, I.MONEY), T("of value added in the United States, 2025:", 22,
                      I.TEXT), T("its GDP", 22, I.DIM)).arrange(RIGHT, buff=0.2).to_edge(UP, buff=0.35)
        src = source("BEA, GDP by Industry, published 30 September 2026", corner=DR)
        stamp = as_of("2025", corner=UL)
        idx = {short(d["sector"]): i for i, d in enumerate(secs)}
        def hl(name):
            return Indicate(tm[idx[name]], color=WHITE, scale_factor=1.04)
        with self.voiceover(
            "Here is the American economy in 2025, drawn by value added: 30.9 trillion dollars, split into twenty "
            "sectors, each block sized by what it adds. <bookmark mark='a'/> The biggest block is a surprise: real "
            "estate, at 13.7 percent. Much of it is rent, including a rent the statisticians count homeowners as "
            "paying themselves, so that owning a home and renting one add the same to GDP. <bookmark mark='b'/> Then "
            "government, at 11 percent, and manufacturing, at 9.5. <bookmark mark='c'/> Finance and insurance, "
            "professional services such as law, accounting, engineering and computer design, and health care each "
            "add between 7 and 9 percent. <bookmark mark='d'/> And the industries that first come to mind when we "
            "think of an economy are small: farming adds less than one percent, mining one percent, utilities under "
            "two."
        ) as vo:
            # a pile of coins, one for each industry, poured out and gathered into the map
            pile = VGroup(*[draw.coin(0.16) for _ in order])
            for k, c in enumerate(pile):
                c.move_to([-0.6 + 0.28 * (k % 6), -0.3 + 0.12 * (k // 6), 0])
            self.play(FadeIn(head), FadeIn(src), FadeIn(stamp),
                      LaggedStart(*[FadeIn(c, shift=DOWN * 0.4) for c in pile], lag_ratio=0.04), run_time=1.6)
            self.play(*[ReplacementTransform(pile[k], tm[i]) for k, i in enumerate(order)], run_time=2.4)
            vo.wait_until("a")
            self.play(hl("Real estate"))
            vo.wait_until("b")
            self.play(hl("Government"), hl("Manufacturing"))
            vo.wait_until("c")
            self.play(hl("Finance and insurance"), hl("Professional services"), hl("Health care"))
            vo.wait_until("d")
            self.play(hl("Farms"), hl("Mining"), hl("Utilities"))
        self.clear_scene()

    def changes(self):
        secs = sorted(R["va"][1:], key=lambda d: -(d["pct"] - d["pct97"]))
        pick = secs[:5] + secs[-4:]
        rows = VGroup()
        for d in pick:
            ch = d["pct"] - d["pct97"]
            c = I.PROFIT if ch > 0 else I.COST
            bar = Rectangle(width=max(abs(ch) * 0.75, 0.04), height=0.36, fill_color=c, fill_opacity=0.9, stroke_width=0)
            name = T(short(d["sector"]), 20, I.TEXT)
            val = T(f"{d['pct97']:.1f}% → {d['pct']:.1f}%", 18, c)
            rows.add(VGroup(name, bar, val))
        for i, r in enumerate(rows):
            y = 2.3 - 0.52 * i
            r[0].move_to(np.array([-1.2, y, 0]), aligned_edge=RIGHT)
            ch = pick[i]["pct"] - pick[i]["pct97"]
            r[1].move_to(np.array([-0.9, y, 0]), aligned_edge=LEFT) if ch > 0 else r[1].move_to(
                np.array([-0.9, y, 0]), aligned_edge=LEFT)
            r[2].next_to(r[1], RIGHT, buff=0.2)
        head = T("Change in share of GDP, 1997 to 2025, in percentage points", 22, I.DIM).to_edge(UP, buff=0.4)
        src = source("BEA, GDP by Industry (TVA110)", corner=DR)
        with self.voiceover(
            "And the shares move. <bookmark mark='a'/> Since 1997, professional services, finance, real estate and "
            "health care have all grown as shares of the economy. <bookmark mark='b'/> Manufacturing has shrunk the "
            "most, from 16 percent of GDP to 9.5, and government, retail and other services have shrunk too. We will "
            "come back to why in chapter thirteen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows[:5]], lag_ratio=0.25), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows[5:]], lag_ratio=0.25), run_time=2)
        self.clear_scene()
