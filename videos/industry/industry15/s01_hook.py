from __future__ import annotations

from videos.industry.industry15.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.moore()
        self.chang()
        self.title()

    def moore(self):
        H = R["hook"]
        pa = viz.plot_axes([1958.5, 1975.5], [0, 17], x_length=8.0, y_length=4.6, xticks=[1959, 1962, 1965, 1970, 1975],
                           yticks=[0, 4, 8, 12, 16], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{2 ** int(v):,}",
                           ylabel="components on a chip, at the cheapest cost per component (log scale)", size=13).move_to([-1.7, -0.5, 0])
        pts = H["line"]
        known = [(y, np.log2(c)) for y, c in pts if y <= 1965]
        ahead = [(y, np.log2(c)) for y, c in pts if y >= 1965]
        dots = VGroup(*[Dot(pa.ax.c2p(x, y), radius=0.07, color=LIGHT) for x, y in known])
        line_k = poly(pa, known, LIGHT, 4)
        line_a = DashedVMobject(poly(pa, ahead, PRICE, 4), num_dashes=40)
        end_dot = Dot(pa.ax.c2p(1975, 16), radius=0.1, color=PRICE)
        end = VGroup(end_dot, tx(f"1975: {H['target']:,.0f}", 20, PRICE, bold=True).next_to(end_dot, LEFT, buff=0.15).shift(UP * 0.25))
        head = VGroup(tx("Electronics, 19 April 1965", 24, WHITE, bold=True),
                      tx("Gordon Moore, director of research at Fairchild Semiconductor", 16, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).to_corner(UL, buff=0.4)
        quote = VGroup(tx("'The complexity for minimum component", 16, WHITE), tx("costs has increased at a rate of roughly", 16, WHITE),
                       tx("a factor of two per year.'", 16, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([4.6, 0.6, 0])
        src = source("G. E. Moore, 'Cramming more components onto integrated circuits', Electronics 38 (8), 19 April 1965", size=13)
        with self.voiceover(
            "In April 1965 a trade magazine called Electronics asked Gordon Moore, the head of research at Fairchild "
            "Semiconductor, what would happen to his industry over the next ten years. "
            "<bookmark mark='a'/> He looked at the few chips made so far, each with a handful of components, and noticed "
            "that the number on the most economical chip had been doubling every year. <bookmark mark='b'/> 'The "
            "complexity for minimum component costs,' he wrote, 'has increased at a rate of roughly a factor of two per "
            "year.' <bookmark mark='c'/> Keep doubling for ten years, he said, and by 1975 a single chip would hold "
            f"{H['target']:,.0f} components. It was a forecast about cost as much as about physics: more on one chip, "
            "and each component cheaper."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pa), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.25), run_time=2.0)
            self.play(Create(line_k))
            vo.wait_until("b")
            self.play(FadeIn(quote, shift=LEFT * 0.1))
            vo.wait_until("c")
            self.play(Create(line_a), run_time=3.0)
            self.play(FadeIn(end, scale=1.2))
        self.clear_scene()

    def chang(self):
        H = R["hook"]
        F = R["fab"]
        plant = draw.factory(2.0).move_to([0, -0.2, 0])
        lab = VGroup(tx(f"Hsinchu, Taiwan, {H['founded']:.0f}", 22, WHITE, bold=True),
                     tx("a factory that makes other companies' chips, and designs none of its own", 16, GREY_A)).arrange(
            DOWN, buff=0.06).to_edge(UP, buff=0.4)
        rng = np.random.default_rng(15)
        customers = VGroup()
        for k in range(60):
            ang = TAU * k / 60 + rng.uniform(-0.03, 0.03)
            rad = rng.uniform(2.3, 2.9)
            customers.add(Dot([rad * np.cos(ang) * 1.75, -0.1 + rad * np.sin(ang) * 0.72, 0], radius=0.06, color=GOOD))
        arrows = VGroup(*[Line(c.get_center(), plant.get_center(), stroke_color=GOOD, stroke_width=1, stroke_opacity=0.35) for c in customers])
        stats = VGroup(tx(f"2025: {H['customers']:.0f} customers, {H['products']:,.0f} products", 18, WHITE, bold=True),
                       tx(f"capacity: more than {F['capacity']:.0f} million wafers a year", 16, GREY_A),
                       tx(f"revenue: ${get('tsm.rev.2025.usd'):.0f} billion", 16, GREY_A)).arrange(DOWN, buff=0.06).to_edge(DOWN, buff=0.55)
        src = source("TSMC, Form 6-K of 15 October 2026 ('pioneered the pure-play foundry business model when it was founded in "
                     "1987'); Form 20-F 2025", size=13)
        with self.voiceover(
            "Twenty-two years later, in 1987, a new company opened in Hsinchu, in Taiwan, with an odd plan. "
            "<bookmark mark='a'/> It would make chips, but only other companies' chips. It would design none of its own, "
            "so it would not compete with its customers. <bookmark mark='b'/> Anyone with a design could book its "
            "factories, as you book a printer. <bookmark mark='c'/> That company is Taiwan Semiconductor Manufacturing, "
            f"TSMC. In 2025 it made {H['products']:,.0f} different products for {H['customers']:.0f} customers, and "
            f"took in about ${get('tsm.rev.2025.usd'):.0f} billion."
        ) as vo:
            self.play(FadeIn(lab), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(plant, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromCenter(c) for c in customers], lag_ratio=0.02), run_time=1.5)
            self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.02), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(stats, shift=UP * 0.1))
        self.clear_scene()

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover(
            "Moore's doubling and TSMC's factories are the two halves of this story. One made chips ever cheaper to "
            "compute with; the other made the factories ever dearer to build, until only a few companies could afford "
            "the ones that make the best chips. Industry, Built. Part fifteen: semiconductors. Why do the most advanced chips come from "
            "so few factories?"
        ):
            self.play(FadeIn(card_[0]), FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.0)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
