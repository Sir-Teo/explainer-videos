from __future__ import annotations

from videos.industry.industry14.common import *  # noqa: F403

FATE = [("landfill", LANDFILL, "landfilled"), ("combustion", BURN, "burned"), ("recycling", "#5DA9E9", "recycled"),
        ("composting", RECYCLE, "composted"), ("food", "#B58CFF", "food: other uses")]


class Recycling(VoiceoverScene):
    def construct(self):
        card(self, 8, "Recycling and burning", "Who pays when the bales stop selling?",
             "Chapter eight. Recycling and burning.", lit=("dollar", "change"))
        self.fate()
        self.mrf()
        self.china()

    def fate(self):
        Rc = R["recycling"]
        M = Rc["msw"]
        ys = sorted(M)
        pa = viz.plot_axes([1960, 2018], [0, 300], x_length=8.4, y_length=4.6, xticks=[1960, 1970, 1980, 1990, 2000, 2010, 2018],
                           yticks=[100, 200, 300], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}m",
                           ylabel="US municipal waste, million tons a year", size=13).move_to([-1.4, -0.4, 0])
        layers = [[M[y][k] for y in ys] for k, _, _ in FATE]
        st = stack(pa, ys, layers, [c for _, c, _ in FATE], opacity=0.85)
        g18 = M[2018]["generation"]
        labs = VGroup()
        for (k, col, name), lyr in zip(FATE, st):
            v = M[2018][k]
            labs.add(tx(f"{name}: {100 * v / g18:.0f}%", 15, col, bold=True))
        labs.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([5.2, 0.0, 0])
        e89 = Rc["epa89"]
        note = VGroup(tx("the EPA in 1989:", 14, GREY_A), tx(f"'{e89['landfilled']:.0f} percent of garbage is landfilled'", 14, WHITE),
                      tx(f"recycling: {e89['recycled']:.0f} percent", 14, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        note.move_to(pa.ax.c2p(1971, 250))
        pin = Dot(pa.ax.c2p(1988, M[1988]["generation"]), radius=0.07, color=WHITE)
        head = VGroup(tx(f"2018: {g18:.0f} million tons", 18, WHITE, bold=True), tx(f"{M[2018]['lb']:.1f} lb per person per day", 14, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.04).next_to(labs, UP, buff=0.3).align_to(labs, LEFT)
        src = source("US EPA, Advancing Sustainable Materials Management: Facts and Figures, 1960-2018 (the latest national "
                     "estimates); The Solid Waste Dilemma (1989)", size=13)
        with self.voiceover(
            "What happens to America's rubbish? <bookmark mark='a'/> Here is the EPA's count, from 1960 to 2018, the "
            "last year it has published. In 1960 almost all of it was buried or burned. <bookmark mark='b'/> When the "
            f"EPA sounded its alarm in 1989, it said {e89['landfilled']:.0f} per cent of garbage was landfilled and only "
            f"{e89['recycled']:.0f} per cent recycled. <bookmark mark='c'/> By 2018, of about {g18:.0f} million tons, "
            f"about {100 * M[2018]['recycling'] / g18:.0f} per cent was recycled and {100 * M[2018]['composting'] / g18:.0f} "
            f"composted; about {100 * M[2018]['combustion'] / g18:.0f} per cent was burned to make electricity; and still "
            f"half, {100 * M[2018]['landfill'] / g18:.0f} per cent, went into the ground. Recycling grew enormously, "
            "but it grew alongside landfill, not instead of it."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(lyr) for lyr in st], lag_ratio=0.25), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(pin), FadeIn(note))
            vo.wait_until("c")
            self.play(FadeIn(head), LaggedStart(*[FadeIn(lb, shift=LEFT * 0.1) for lb in labs], lag_ratio=0.2), run_time=2.0)
        self.clear_scene()

    def mrf(self):
        Rc = R["recycling"]
        belt = Rectangle(width=8.0, height=0.25, stroke_width=0, fill_color="#3A4152", fill_opacity=1).move_to([-1.0, 0.0, 0])
        rollers = VGroup(*[Circle(radius=0.12, stroke_width=0, fill_color="#5D6B82", fill_opacity=1).move_to([-4.8 + 0.8 * k, -0.18, 0]) for k in range(11)])
        bin_ = draw.wheelie_bin(1.0, "#3B6FB6", "#2B5390").move_to([-6.2, -0.3, 0])
        items = VGroup()
        cols = ["#B58E5A", "#E8EAED", "#C9D3E0", "#7EC8F5", "#B58E5A", "#9AA3B2", "#E8EAED", "#7EC8F5", "#B58E5A", "#C9D3E0"]
        for k, c in enumerate(cols):
            items.add(Square(0.22, stroke_width=0, fill_color=c, fill_opacity=1).rotate(0.3 * k).move_to([-4.8 + 0.35 * k, 0.25, 0]))
        bales = VGroup(draw.bale(0.7, "#B58E5A"), draw.bale(0.7, "#E8EAED"), draw.bale(0.7, "#C9D3E0"), draw.bale(0.7, "#7EC8F5")).arrange(RIGHT, buff=0.35).move_to([4.6, -1.4, 0])
        bl = VGroup(*[tx(n, 13, GREY_A).next_to(b, DOWN, buff=0.1) for n, b in zip(("cardboard", "paper", "aluminium", "plastic"), bales)])
        sort = tx("sorted by screens, magnets, air jets and people", 15, GREY_A).next_to(belt, UP, buff=0.6)
        r24, r25 = Rc["rsg"]
        price = VGroup(tx("what a ton of Republic's sorted recyclables fetched", 15, GREY_A),
                       tx(f"2024: ${r24:.0f}     2025: ${r25:.0f}", 24, PRICE, bold=True),
                       tx(f"each $10 a ton moves its revenue and profit by about ${Rc['sens']:.0f}m a year", 14, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).move_to([-2.8, -2.0, 0])
        src = source("Republic Services, Form 10-K 2025 (average price of recycled commodities, excluding glass and organics)", size=13)
        with self.voiceover(
            "Recycling is a factory. <bookmark mark='a'/> The blue bin's contents are tipped onto a belt "
            "<bookmark mark='b'/> and sorted, by screens, magnets, jets of air and people, <bookmark mark='c'/> into "
            "bales: cardboard, paper, aluminium, plastic. The bales are sold to mills and smelters, at whatever the "
            "market pays that month. <bookmark mark='d'/> For Republic Services, a ton of its sorted recyclables "
            f"fetched about ${r24:.0f} on average in 2024, and ${r25:.0f} in 2025; every ten dollars a ton moves its "
            f"revenue and profit by about ${Rc['sens']:.0f} million a year. Sorting costs much the same whatever the "
            "bales fetch. So when bale prices fall, someone has to pay the difference: the hauler, or the town that "
            "hired it."
        ) as vo:
            self.play(FadeIn(src), FadeIn(belt), FadeIn(rollers))
            vo.wait_until("a")
            self.play(FadeIn(bin_), LaggedStart(*[FadeIn(i, shift=RIGHT * 0.3) for i in items], lag_ratio=0.08), run_time=1.5)
            vo.wait_until("b")
            self.play(items.animate.shift(RIGHT * 4.0), FadeIn(sort), run_time=2.5, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeOut(items, shift=RIGHT * 1.5), LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in bales], lag_ratio=0.2), FadeIn(bl), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(price, shift=UP * 0.1))
        self.clear_scene()

    def china(self):
        Rc = R["recycling"]
        P = Rc["paper"]
        ks = sorted(P)

        def x_of(k):
            return int(k[:4]) + (int(k[5:7]) - 0.5) / 12
        pa = viz.plot_axes([2010, 2027], [0, 520], x_length=9.6, y_length=4.4, xticks=[2010, 2013, 2016, 2019, 2022, 2025],
                           yticks=[100, 200, 300, 400, 500], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}",
                           ylabel="producer price index, recyclable paper (1982 = 100), monthly", size=13).move_to([-0.6, -0.4, 0])
        ln = poly(pa, [(x_of(k), P[k]) for k in ks], "#B58E5A", 3.5)
        ban = DashedLine(pa.ax.c2p(2018.0, 0), pa.ax.c2p(2018.0, 500), stroke_color=BAD, stroke_width=2, dash_length=0.08)
        ban_l = VGroup(tx("1 January 2018:", 15, BAD, bold=True), tx("China bans imports of mixed", 13, GREY_A),
                       tx("paper and mixed plastics", 13, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.03).next_to(pa.ax.c2p(2018.1, 500), RIGHT, buff=0.1)
        pk_v, pk_k = Rc["paper_peak"]
        lo_v, lo_k = Rc["paper_low"]
        pk = Dot(pa.ax.c2p(x_of(pk_k), pk_v), radius=0.08, color=WHITE)
        lo = Dot(pa.ax.c2p(x_of(lo_k), lo_v), radius=0.08, color=WHITE)
        pk_l = tx(f"{pk_v:.0f}", 15, WHITE, bold=True).next_to(pk, LEFT, buff=0.1)
        lo_l = tx(f"{lo_v:.0f}: {100 * (1 - lo_v / pk_v):.0f}% lower", 15, WHITE, bold=True).next_to(lo, DOWN, buff=0.1)
        src = source("BLS, producer price index for recyclable paper (WPU0912, via FRED); Waste Management, Form 10-K 2018", size=13)
        with self.voiceover(
            "And they do fall. For years, a significant part of the fibre America's haulers recovered was shipped "
            "abroad, particularly to China. <bookmark mark='a'/> Here is the US producer price index for recyclable "
            "paper. <bookmark mark='b'/> In 2017 China announced a ban on imports of mixed waste paper and mixed "
            "plastics from the first of January 2018, as Waste Management told its shareholders. "
            "<bookmark mark='c'/> In the two years that followed, the index fell from about "
            f"{pk_v:.0f} to about {lo_v:.0f}, by {100 * (1 - lo_v / pk_v):.0f} per cent. <bookmark mark='d'/> It has "
            f"swung just as hard since: back to about {P['2021-12']:.0f} at the end of 2021, down to about "
            f"{P['2022-12']:.0f} a year later. When bales fetch less than the sorting costs, recycling costs money "
            "instead of earning it. The business that sorts it is a factory exposed to a world market."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(ln), run_time=4.0, rate_func=linear)
            vo.wait_until("b")
            self.play(Create(ban), FadeIn(ban_l))
            vo.wait_until("c")
            self.play(FadeIn(pk), FadeIn(pk_l), FadeIn(lo), FadeIn(lo_l))
            vo.wait_until("d")
            sw = VGroup(Dot(pa.ax.c2p(x_of("2021-12"), P["2021-12"]), radius=0.07, color=PRICE), Dot(pa.ax.c2p(x_of("2022-12"), P["2022-12"]), radius=0.07, color=PRICE))
            self.play(FadeIn(sw), Indicate(sw, color=PRICE))
        self.clear_scene()
