from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry1.common import *  # noqa: F403

BRAND_COL = {"Apple": I.BRAND, "Samsung": "#4FC3A1", "Xiaomi": I.CHANNEL, "vivo": "#8FB4FF", "OPPO": "#7BD88F",
             "Others": "#6B7280"}


class TwoPhones(VoiceoverScene):
    def construct(self):
        card(self, 9, "Three phones, three businesses", "Does every phone maker earn like Apple?",
             "Chapter nine. Three phones, three businesses.", lit=("unit", "moat"))
        self.shares()
        self.perphone()

    def shares(self):
        M = R["market"]
        tm = viz.treemap([(b, u, BRAND_COL[b], f"{100 * u / M['total']:.0f}%  ·  {u:.0f}m") for b, u in M["brands"]],
                         9.0, 5.2, 26).move_to(DOWN * 0.3)
        head = VGroup(TB(f"{M['total'] / 1000:.2f} billion smartphones", 30, I.TEXT),
                      T("shipped worldwide in 2025", 24, I.DIM)).arrange(RIGHT, buff=0.25).to_edge(UP, buff=0.45)
        src = source("IDC Worldwide Quarterly Mobile Phone Tracker, preliminary, 13 January 2026")
        stamp = as_of("2025")
        with self.voiceover(
            "Apple is one phone maker among many. <bookmark mark='a'/> In 2025 the world bought about 1.26 billion "
            "smartphones, by the count of the market tracker IDC. <bookmark mark='b'/> Apple shipped about 248 "
            "million of them, one in five, and Samsung almost as many. <bookmark mark='c'/> Then come three Chinese "
            "brands: Xiaomi, vivo and OPPO. And almost a third of the market is a long list of others, from Honor "
            "and Huawei to Transsion, which sells nearly half of all the smartphones bought in Africa under the "
            "names Tecno, Infinix and itel."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(stamp))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(tm[0], scale=0.9), FadeIn(tm[1], scale=0.9))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b, scale=0.9) for b in tm[2:]], lag_ratio=0.3), run_time=1.8)
        self.clear_scene()

    def perphone(self):
        P = R["perphone"]
        names = (("apple", "Apple", "iPhone", I.BRAND), ("xiaomi", "Xiaomi", "smartphones", I.CHANNEL),
                 ("transsion", "Transsion", "Tecno, Infinix, itel", "#C7D96A"))
        maxrev = P["apple"]["rev"]
        H, base = 4.1, -1.75
        cols = VGroup()
        for (k, n, sub, c), x in zip(names, (-4.3, -0.5, 3.3)):
            d = P[k]
            rev = Rectangle(width=1.3, height=H * d["rev"] / maxrev, fill_color=c, fill_opacity=0.22, stroke_color=c,
                            stroke_width=2)
            rev.move_to(np.array([x, base + rev.height / 2, 0]))
            gp = Rectangle(width=1.3, height=max(H * d["gp"] / maxrev, 0.04), fill_color=I.PROFIT, fill_opacity=0.9,
                           stroke_width=0)
            gp.move_to(np.array([x, base + gp.height / 2, 0]))
            rl = VGroup(TB(money(d["rev"]), 28, c), T("revenue per phone", 16, I.DIM)).arrange(DOWN, buff=0.04
                                                                                              ).next_to(rev, UP, buff=0.12)
            if d["rev"] < 0.5 * maxrev:
                rl.align_to(rev, RIGHT)
            gl = VGroup(TB(money(d["gp"]), 26, I.PROFIT), T("gross profit", 16, I.DIM)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.04).next_to(gp, RIGHT, buff=0.3).align_to(gp, DOWN)
            head = VGroup(TB(n, 26, I.TEXT), T(sub, 16, I.DIM),
                          T(f"{d['units']:.0f} million phones · {pct(d['gm'])} margin", 16, I.DIM)
                          ).arrange(DOWN, buff=0.05).next_to(np.array([x, base, 0]), DOWN, buff=0.22)
            cols.add(VGroup(VGroup(head, VGroup(rev, gp)), rl, gl, VGroup(), VGroup()))
        ratio = VGroup(T("Apple's gross profit per phone is", 24, I.TEXT), TB(f"about {P['ratio']:.0f} times", 30,
                       I.ACCENT), T("Xiaomi's", 24, I.TEXT)).arrange(RIGHT, buff=0.2).to_edge(UP, buff=0.4)
        pools = VGroup(T("Gross profit from phones, 2025:", 22, I.DIM),
                       TB(f"Apple {money_short(P['pool']['apple'], 0)}", 22, I.BRAND),
                       TB(f"Xiaomi {money_short(P['pool']['xiaomi'])}", 22, I.CHANNEL),
                       TB(f"Transsion {money_short(P['pool']['transsion'])}", 22, "#C7D96A")).arrange(RIGHT, buff=0.3
                                                                                                     ).to_edge(UP, buff=0.4)
        src = source("Apple 10-K FY2025 and IDC units; Xiaomi, Transsion 2025 results; FRED yuan rate", corner=DL,
                     size=14)
        tag = estimate_tag("estimate: Apple at its average products margin")
        with self.voiceover(
            "But one phone is not like another. <bookmark mark='a'/> Divide each company's phone sales by the number "
            "of phones it sold. Apple stopped reporting how many iPhones it sells in 2018, so we divide its iPhone "
            "sales for fiscal 2025, 210 billion dollars, by IDC's count: about 859 dollars of revenue per iPhone. "
            "<bookmark mark='b'/> Xiaomi reports both numbers: 186 billion yuan from 165 million phones, about 157 "
            "dollars each. <bookmark mark='c'/> Transsion, about 72 dollars a phone. <bookmark mark='d'/> Now the "
            "margins. Apple does not report the iPhone's margin separately; at the 37 percent it earns across all "
            "its products, an iPhone leaves about 316 dollars of gross profit. Xiaomi's phones kept 10.9 percent: "
            "about 17 dollars each. Transsion, about 14. <bookmark mark='e'/> So each iPhone leaves Apple roughly "
            "eighteen times the gross profit a Xiaomi phone leaves Xiaomi. <bookmark mark='f'/> Add it up over a "
            "year: Apple's iPhones made about 77 billion dollars of gross profit; Xiaomi's phones, under 3 billion. "
            "Apple sells one phone in five. By the tracker Counterpoint's estimates, it collects about half of all "
            "the money the world spends on smartphones, and in 2023 it took 85 percent of the industry's operating "
            "profit. Selling many phones and making money from phones turn out to be different businesses."
        ) as vo:
            self.play(FadeIn(src), FadeIn(tag))
            for i, m in enumerate("abc"):
                vo.wait_until(m)
                c = cols[i]
                self.play(FadeIn(c[0][0]), GrowFromEdge(c[0][1][0], DOWN), FadeIn(c[1]), run_time=1.2)
            vo.wait_until("d")
            self.play(*[AnimationGroup(GrowFromEdge(c[0][1][1], DOWN), FadeIn(c[2])) for c in cols], run_time=1.6)
            vo.wait_until("e")
            self.play(FadeIn(ratio, shift=UP * 0.1))
            vo.wait_until("f")
            self.play(FadeOut(ratio, shift=UP * 0.1), FadeIn(pools, shift=DOWN * 0.1))
        self.clear_scene()
