from __future__ import annotations

from videos.industry.industry15.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.funnel()
        self.answers()

    def funnel(self):
        H, G, F = R["hook"], R["geography"], R["fab"]
        levels = [(f"{H['customers']:.0f} customers, {H['products']:,.0f} products", "TSMC, 2025", GOOD),
                  (f"{G['n_fabs']} TSMC fabs, ${F['capex25']:.0f}bn spent on them in 2025", "the factories", DIE),
                  (f"{len(G['leading'])} fabs making its 2- and 3-nanometre chips, all in Taiwan", "the frontier", PRICE),
                  ("1 maker of EUV machines", "ASML, the Netherlands", LIGHT)]
        W0, W1, h, top = 12.0, 3.0, 1.05, 2.4
        bands, labs = VGroup(), VGroup()
        n = len(levels)
        for i, (big, small, col) in enumerate(levels):
            wa = W0 - (W0 - W1) * i / n
            wb = W0 - (W0 - W1) * (i + 1) / n
            ya, yb = top - h * i, top - h * (i + 1)
            band = Polygon([-wa / 2, ya, 0], [wa / 2, ya, 0], [wb / 2, yb + 0.06, 0], [-wb / 2, yb + 0.06, 0], stroke_width=0,
                           fill_color=col, fill_opacity=0.28)
            lab = VGroup(tx(big, 19 if i < 3 else 17, WHITE, bold=True), tx(small, 13, col)).arrange(DOWN, buff=0.04).move_to(band)
            if lab.width > wb - 0.3:
                lab.scale_to_fit_width(wb - 0.3)
            bands.add(band)
            labs.add(lab)
        chip = draw.chip(0.55, PRICE).move_to([0, top - h * n - 0.45, 0])
        head = tx(ASK, 22, WHITE, bold=True).to_edge(UP, buff=0.25)
        src = source("TSMC, Form 20-F 2025 and Form 6-K of 15 October 2026; ASML, Form 20-F 2025", size=13)
        with self.voiceover(
            "So: why do the most advanced chips come from so few factories? <bookmark mark='a'/> Demand is wide: TSMC "
            f"alone made {H['products']:,.0f} products for {H['customers']:.0f} customers in 2025. <bookmark mark='b'/> "
            "But Moore's doubling had a price. Each step down in size needs a dearer factory, and only a company with "
            f"enough customers can fill one: TSMC spent about ${F['capex25']:.0f} billion on its fabs in that one year. "
            f"<bookmark mark='c'/> At the frontier, the {len(G['leading'])} fabs that make its two- and three-nanometre "
            "chips are all in Taiwan. <bookmark mark='d'/> And the machines that print the finest layers come from one "
            "company in the Netherlands. The funnel narrows at every step, because every step costs more than the last, "
            "and each one needs the volume of the whole world to pay for it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), *[FadeIn(b.copy().set_opacity(0.08)) for b in bands])
            for mk, b, l_ in zip("abcd", bands, labs):
                vo.wait_until(mk)
                self.play(FadeIn(b), FadeIn(l_, shift=DOWN * 0.1), run_time=0.9)
            self.play(FadeIn(chip, shift=DOWN * 0.3))
        self.clear_scene()

    def answers(self):
        qs = [("What is sold?", "a die cut from a wafer: logic, memory, analog; designed by one company, made by another"),
              ("How is it made?", "hundreds of steps of printing, etching and filling, in fabs that cost tens of billions"),
              ("Where does the dollar go?", "to the designer with the best chip, the foundry that can make it, and the toolmakers"),
              ("Why does it stay there?", "scale: the frontier needs the volume of the whole world, and few can buy in"),
              ("What moves it?", "the memory cycle, the next node, AI's appetite, and the rules on who may buy")]
        rows = VGroup()
        for i, (q, a) in enumerate(qs):
            rows.add(VGroup(tx(q, 20, PRICE, bold=True), tx(a, 16, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([-5.6, 2.3 - 1.05 * i, 0], aligned_edge=LEFT))
        with self.voiceover(
            "Semiconductors, in five answers. <bookmark mark='a'/> What is sold is a die cut from a wafer, more and more "
            "often designed by one company and made by another. <bookmark mark='b'/> It is made in hundreds of steps, in "
            "factories that cost tens of billions. <bookmark mark='c'/> The dollar goes to the designer with the best chip, "
            "to the foundry that can make it, and to the makers of the tools. <bookmark mark='d'/> It stays there because "
            "the frontier needs the volume of the whole world, and few can afford to buy in. <bookmark mark='e'/> And "
            "what moves it is the memory cycle, the next node, the appetite of AI, and the rules on who may buy. Next "
            "time: electronics, the industry that puts these chips into the things we buy, and why the company that "
            "builds the device keeps the least of it."
        ) as vo:
            head = tx("Semiconductors, in five answers", 24, WHITE, bold=True).to_edge(UP, buff=0.3)
            self.play(FadeIn(head), *[FadeIn(r_[0].copy().set_opacity(0.25)) for r_ in rows])
            for m_, r_ in zip("abcde", rows):
                vo.wait_until(m_)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
