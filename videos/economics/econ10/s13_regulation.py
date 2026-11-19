from __future__ import annotations

from videos.economics.econ10.common import *  # noqa: F403

CAPC = "#F28C6F"
LABC = "#7EC8F5"


class Regulation(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Regulating a monopoly", r"If a regulator caps the profit, what does the firm do?",
             "Chapter eleven. Regulating a monopoly.", lit={1962: r"Averch and Johnson"}, scale=("firm", "nation"),
             horizon=("a decade",))
        self.rate_of_return()
        self.caps()

    def rate_of_return(self):
        a = load("aj")
        f, r = a["free"], a["regulated"]
        rows = VGroup(
            label(r"rate-of-return regulation: \ the waterworks may earn at most a fair return on its capital",
                  font_size=24),
            label(rf"the allowed return, \ {a['s']:.1f}, \ is above what capital costs, \ {a['r']:.1f}", font_size=24,
                  color=GREY_A),
            label(r"so every extra unit of capital raises the profit the firm may keep", font_size=24, color=HOLD),
        ).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.6)
        bars = VGroup()
        for k, (name, ratio, col) in enumerate(((r"least-cost mix", a["efficient_ratio"], GREY_B),
                                                (r"unregulated monopoly", f["ratio"], CS),
                                                (r"rate-of-return regulated", r["ratio"], CAPC))):
            bars.add(VGroup(label(name, font_size=22, color=col),
                            Rectangle(width=4.0 * ratio, height=0.4, stroke_width=0, fill_color=col, fill_opacity=0.85),
                            label(rf"{ratio:.2f}", font_size=22, color=col)))
        for g in bars:
            g[0].set_width(min(g[0].width, 3.6))
            g[1].next_to(g[0], RIGHT, buff=0.3)
            g[2].next_to(g[1], RIGHT, buff=0.15)
        bars.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(rows, DOWN, buff=0.55)
        x0 = max(g[0].get_right()[0] for g in bars) + 0.3
        for g in bars:
            g[1].align_to(np.array([x0, 0.0, 0.0]), LEFT)
            g[2].next_to(g[1], RIGHT, buff=0.15)
        bars.set_x(0)
        cap = label(r"capital per worker", font_size=20, color=GREY_A).next_to(bars, UP, buff=0.15).align_to(
            bars[0][1], LEFT)
        foot = label(rf"Averch and Johnson (1962): \ too much capital, \ {100 * (r['ratio'] / a['efficient_ratio'] - 1):.0f}"
                     r"\% more per worker than the least-cost mix: \ ``gold plating''", font_size=23,
                     color=E.ACCENT).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Averch and Johnson, American Economic Review 52(5) (1962)", corner=DR, font_size=14)
        with self.voiceover(
            "For most of the twentieth century, American utilities were regulated by capping their profit. "
            "<bookmark mark='a'/> The waterworks may earn no more than a fair return on the capital it has "
            "invested. <bookmark mark='b'/> If the allowed return is above what capital actually costs, "
            "<bookmark mark='c'/> then every extra pipe raises the profit the firm is allowed to keep. "
            "<bookmark mark='d'/> Agora's waterworks, left alone, would use three quarters of a unit of capital per "
            "worker, the least-cost mix. Under the regulation it uses one point oh seven: forty-three percent more. "
            "<bookmark mark='e'/> Harvey Averch and Leland Johnson pointed this out in 1962. It came to be called "
            "gold plating."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(cap), LaggedStart(*[FadeIn(g, shift=RIGHT * 0.1) for g in bars], lag_ratio=0.5),
                      run_time=2.5)
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def caps(self):
        head = label(r"price caps", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"cap the price instead: \ it may rise each year by inflation minus $X$", font_size=26),
            label(r"proposed by Stephen Littlechild in 1983, \ for British Telecom, \ privatized in 1984", font_size=23,
                  color=GREY_A),
            label(r"now the firm keeps whatever it saves: \ a reason to cut costs, \ not to gold-plate", font_size=25,
                  color=CS),
            label(r"but when the cap is reset, \ low costs are rewarded with a lower cap: \ the ratchet", font_size=25,
                  color=HOLD),
            label(r"every regulator trades incentives against rents: \ Part 14 has the theory", font_size=25,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "The alternative is to cap the price, not the profit. <bookmark mark='a'/> Each year the price may rise "
            "by inflation minus some figure, X, the expected gain in efficiency. <bookmark mark='b'/> Stephen "
            "Littlechild proposed it in 1983 for British Telecom, which was privatized the next year, and it spread "
            "to water, gas and electricity. <bookmark mark='c'/> Under a price cap the firm keeps whatever it saves, so it "
            "has every reason to cut costs, and none to gold-plate. <bookmark mark='d'/> The catch comes when the "
            "cap is reset: a firm that cut its costs a lot finds itself with a tighter cap, which weakens the "
            "incentive. <bookmark mark='e'/> Every regulator trades the firm's incentive to be efficient against "
            "the profit it is allowed to keep. Part fourteen has the theory."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2), FadeIn(rows[0], shift=UP * 0.1))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
