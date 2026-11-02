from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import GAIN, LOSS, PART, TRADE, load

C_ = {r"\sigma": QC.IDEA, r"\lambda": LOSS, r"n": TRADE}


def row(*parts, fs=36):
    return cmath(*parts, colors=C_, font_size=fs)


class Dealers(VoiceoverScene):
    def construct(self):
        r = load("rfq")
        self.card()
        self.rfq_live(r)
        self.rfq_math(r)
        self.wholesale(r)

    def card(self):
        c = chapter_card(5, r"Dealers, RFQ and wholesalers", r"Why would anyone pay to trade against you?", part=PART)
        with self.voiceover("Chapter five. Dealers, requests for quote, and wholesalers."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def rfq_live(self, r):
        rng = np.random.default_rng(5)
        client = VGroup(Circle(radius=0.45, color=QC.HOUSE, fill_opacity=0.15), label(r"client", font_size=22))
        client.move_to(LEFT * 4.6 + UP * 0.6)
        n = 8
        dealers = VGroup()
        for i in range(n):
            ang = -0.9 + 1.8 * i / (n - 1)
            d = VGroup(Circle(radius=0.28, color=TRADE, fill_opacity=0.12),
                       MathTex(str(i + 1), font_size=22, color=TRADE)).move_to(client.get_center()
                                                                              + 3.2 * np.array([np.cos(ang), np.sin(ang), 0]))
            dealers.add(d)
        lines = VGroup(*[DashedLine(client.get_center(), d.get_center(), buff=0.5, color=GREY_D, stroke_width=1.5)
                         for d in dealers])
        hist = r["hist"]
        edges = np.asarray(r["hist_edges"])
        g = axes([-4, 2], [0, 1.05], x_length=5.2, y_length=3.2, xlabel=r"best quote, in units of $\sigma$ "
                 r"(lower is better for a buyer)", xticks=[-3, -2, -1, 0, 1], font_size=16)
        g.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.6)
        ax = g.ax
        cols = {"1": GREY_B, "3": QC.IDEA, "10": GAIN}
        polys = VGroup()
        for kk, col in cols.items():
            h = np.asarray(hist[kk], float)
            h = h / h.max()
            xs = (edges[:-1] + edges[1:]) / 2
            polys.add(VGroup(band(ax, xs, np.zeros_like(h), h, col, 0.25), curve(ax, xs, h, col, stroke_width=2.5)))
        leg = legend([(GREY_B, r"ask 1 dealer"), (QC.IDEA, r"ask 3"), (GAIN, r"ask 10")], font_size=19)
        leg.next_to(g, UP, buff=0.25).align_to(g, LEFT)
        src = note(r"simulated: each dealer's quote is the mid plus its own cost shock, $\sigma Z_i$; "
                   r"$10^5$ requests", font_size=16).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Most bonds, currencies and swaps don't trade in a central book. They trade with dealers, who quote "
            "from their own inventory, often by request for quote: the client asks several dealers at once and "
            "takes the best answer. <bookmark mark='a'/> Each dealer's price differs a little, because each holds "
            "a different inventory: one is long and keen to sell, another short. Ask one dealer and you get one "
            "draw. Ask three, and the best of three. <bookmark mark='b'/> Repeat it a hundred thousand times. The "
            "distribution of the best quote slides left as more dealers are asked: competition works. But it slides "
            "by less and less with each dealer added."
        ) as vo:
            self.play(FadeIn(client), LaggedStart(*[FadeIn(d) for d in dealers], lag_ratio=0.1), Create(lines))
            vo.wait_until("a")
            for rep in range(3):
                vals = rng.standard_normal(n)
                tags = VGroup(*[MathTex(f"{100 + 0.05 * v:.2f}", font_size=20, color=GREY_A).next_to(d, RIGHT, buff=0.08)
                                for d, v in zip(dealers, vals)])
                best = int(np.argmin(vals))
                self.play(FadeIn(tags), run_time=0.4)
                self.play(Indicate(dealers[best], color=GAIN), tags[best].animate.set_color(GAIN), run_time=0.6)
                self.play(FadeOut(tags), run_time=0.3)
            vo.wait_until("b")
            self.play(FadeIn(g), FadeIn(leg), FadeIn(src))
            for p in polys:
                self.play(FadeIn(p[0]), Create(p[1]), run_time=1.0)
        self.wait(0.4)
        self.clear_scene()

    def rfq_math(self, r):
        rows = [
            row(r"\text{quote}_i", r"=", r"m + c_i, \qquad c_i = \sigma Z_i \ \text{iid}"),
            row(r"\mathbb E\,\text{best}", r"=", r"m - \sigma\,\mathbb E\max_{i \le n} Z_i,\quad "
                r"\mathbb E\max_{i\le n} Z_i = n\!\int z\,\phi(z)\,\Phi(z)^{n-1}dz \approx \sqrt{2\ln n}"),
            row(r"C(n)", r"=", r"m - \sigma\,\mathbb E\max_n Z + \lambda\,(n-1)"),
            row(r"n^*:", r"\ ", r"\sigma\big(\mathbb E\max_{n+1} - \mathbb E\max_{n}\big) < \lambda"),
        ]
        whys = [why(r"each dealer's cost of taking the other side is private: its inventory", font_size=20),
                why(r"order statistics: the density of the maximum of $n$ is $n\phi\Phi^{n-1}$", font_size=20),
                why(r"but every dealer asked learns your intention and can trade ahead: leakage $\lambda$ each",
                    font_size=20),
                why(r"stop asking when the next dealer saves less than it leaks", font_size=20)]
        for r_ in rows:
            r_.scale(0.82)
        step = ladder(self, rows, whys, keep=2, top=3.4, x=-2.4, buff=0.42, edge=6.9)
        n = np.asarray(r["n"], float)
        cost = np.asarray(r["cost"], float)
        g = axes([1, 20], [-1.6, 1.4], x_length=5.0, y_length=2.4, xlabel=r"dealers asked $n$",
                 ylabel=rf"cost, units of $\sigma$ ($\lambda = {r['lam0']:.2f}\sigma$)", xticks=[1, 5, 10, 15, 20],
                 yticks=[-1, 0, 1], font_size=15).to_corner(DL, buff=0.45)
        ax = g.ax
        cu = curve(ax, n, cost, QC.IDEA)
        nst = int(r["nstar0"])
        md = Dot(ax.c2p(nst, cost[nst - 1]), radius=0.08, color=QC.HOUSE)
        g2 = axes([0, 0.5], [0, 20], x_length=4.2, y_length=2.4, xlabel=r"leakage $\lambda/\sigma$",
                  ylabel=r"best number to ask $n^*$", xticks=[0.1, 0.3, 0.5], yticks=[0, 10, 20], font_size=15)
        g2.to_corner(DR, buff=0.45)
        st = VMobject(color=QC.HOUSE, stroke_width=3).set_points_as_corners(
            [g2.ax.c2p(x, y) for x, y in zip(r["lam_grid"], r["nstar"])])
        with self.voiceover(
            "Write it down. Each quote is the mid plus a dealer's private cost, sigma times a standard normal. "
            "<bookmark mark='a'/> The best of n is the mid minus sigma times the expected maximum of n normals, "
            "an order statistic, which grows only like the square root of two log n: slowly. "
            "<bookmark mark='b'/> And every dealer you ask learns that you want to trade, and can trade ahead of "
            "you: call that leakage lambda per dealer. <bookmark mark='c'/> The total cost is a U: savings that "
            f"flatten, against leakage that grows in a straight line. With lambda at {r['lam0']:.2f} sigma the "
            f"best is to ask {nst}; and as leakage rises, the best number falls fast. Real platforms cap requests "
            "at a handful of dealers for exactly this reason."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            self.play(FadeIn(g), Create(cu), FadeIn(g2))
            self.play(FadeIn(md, scale=1.5), Create(st))
        self.wait(0.4)
        self.clear_scene()

    def wholesale(self, r):
        hs = np.asarray(r["hs"], float)
        mk = r["markout"]
        g = axes([0, 300], [-2.4, 0.5], x_length=5.6, y_length=3.4, xlabel=r"seconds after the fill",
                 ylabel=r"dealer's markout, per share", xticks=[0, 60, 120, 300], yticks=[-2, -1, 0], font_size=16)
        g.to_edge(LEFT, buff=0.6).shift(UP * 0.4)
        ax = g.ax
        rl = curve(ax, hs, np.asarray(mk["retail"]), GAIN)
        il = curve(ax, hs, np.asarray(mk["institutional"]), LOSS)
        leg = legend([(GAIN, r"retail flow: 2\% informed"), (LOSS, r"institutional flow: 30\% informed")],
                     font_size=18).next_to(g, DOWN, buff=0.3).align_to(g, LEFT)
        eq = MathTex(r"\text{profit per share} = \tfrac{s}{2} - \text{adverse selection} - \text{price improvement} "
                     r"- \text{PFOF}", font_size=26, color=QC.HOUSE).to_edge(DOWN, buff=0.75)
        facts = VGroup(
            label(r"GameStop, January 2021 (SEC staff report):", font_size=21, color=QC.IDEA),
            label(r"about 80\% of off-exchange trades internalized by wholesalers", font_size=19),
            label(r"88\% of that by three firms: Citadel Securities nearly 50\%, Virtu about 26\%", font_size=19),
            label(r"27 January: Citadel internalized nearly \$4.2 billion of GameStop", font_size=19),
            label(r"Ernst and Spatt (2022): PFOF is small in stocks, large in options", font_size=19),
            label(r"Battalio, Corwin and Jennings (2016): brokers routing for rebates", font_size=19),
            label(r"got worse fills on limit orders", font_size=19),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(RIGHT, buff=0.35).shift(UP * 0.7)
        src = note(r"markouts simulated: informed orders know the price 60 seconds ahead", font_size=16)
        src.to_edge(DOWN, buff=0.2)
        ret0 = float(np.asarray(mk["retail"])[6])
        inst0 = float(np.asarray(mk["institutional"])[6])
        with self.voiceover(
            "Now American retail stock orders. Most never reach an exchange: wholesalers fill them, and pay the "
            "broker for the flow. Why pay to trade against someone? Because of who that someone is. A dealer's "
            "markout is what a fill is worth a minute later. <bookmark mark='a'/> In this simulation, flow with a "
            "few informed traders costs the dealer almost nothing, "
            f"{abs(ret0):.2f} per share a minute later; flow where a third know where the price is going costs "
            f"{abs(inst0):.2f}. Retail orders are mostly uninformed, so filling them earns the spread. "
            "<bookmark mark='b'/> A wholesaler keeps half the spread, less the adverse selection, less the price "
            "improvement it gives the customer, less what it pays the broker. Competition decides how that surplus "
            "is split. <bookmark mark='c'/> In GameStop's January, about eighty percent of off-exchange trading was "
            "internalized, eighty-eight percent of it by three wholesalers, and on the 27th Citadel Securities "
            "alone internalized nearly four point two billion dollars of it. Ernst and Spatt find payment for "
            "order flow small in stocks and large in options; Battalio, Corwin and Jennings found that brokers "
            "routing for rebates got worse fills on their customers' limit orders. Brokers owe their customers "
            "best execution, and these papers are how anyone checks. However a trade is made, in a book, an auction or "
            "with a dealer, it leaves a promise between two parties. Next: who stands behind it."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            self.play(Create(rl), Create(il), run_time=max(2.0, vo.until("a")))
            vo.wait_until("b")
            self.play(Write(eq))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(f) for f in facts], lag_ratio=0.4, run_time=5), FadeIn(src))
        self.wait(0.4)
        self.clear_scene()
