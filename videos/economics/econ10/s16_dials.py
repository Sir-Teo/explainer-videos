from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ10.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 14, r"The Dials: \ how large are markups?", r"How far above marginal cost do real firms price, "
             r"and has the gap grown?", "Chapter fourteen. The Dials: how large are markups?",
             lit={2012: r"De Loecker and Warzynski"}, scale=("firm", "nation"), horizon=("a decade",))
        self.method()
        self.dial()

    def method(self):
        d = load("dlw")
        head = label(r"marginal cost is never in the accounts: \ how do you measure a markup?", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"a firm that minimizes cost buys each flexible input until its price \\ equals marginal cost "
                  r"times what it adds to output", font_size=24),
            MathTex(r"\mu = \frac{p}{MC} = \theta_V \cdot \frac{p\,Q}{P_V\,V}", font_size=46, color=E.ACCENT),
            label(r"$\theta_V$: \ the output elasticity of a flexible input $V$, \ from an estimated production "
                  r"function (Part 8)", font_size=22, color=GREY_A),
            label(r"$p\,Q / P_V V$: \ sales over what the input cost, \ straight from the accounts", font_size=22,
                  color=GREY_A),
            label(rf"Agora's check: \ $\theta = {d['theta']:.1f}$, \ sales over materials {d['ratio']:.1f}, \ so "
                  rf"$\mu = {d['measured']:.2f}$; \ the firm's true markup is {d['true']:.2f}", font_size=23,
                  color=E.AGORA),
            label(r"De Loecker and Warzynski (2012); \ the idea goes back to Hall (1988)", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "This part's dial is the size of markups in real economies. The trouble is that no firm reports its "
            "marginal cost. <bookmark mark='a'/> But a firm that minimizes its costs keeps buying each flexible "
            "input, materials say, until the input's price equals marginal cost times what the input adds to "
            "output. <bookmark mark='b'/> Rearranged, that says the markup is the input's output elasticity times "
            "the ratio of sales to what was spent on the input. <bookmark mark='c'/> The elasticity comes from an "
            "estimated production function, the problem of Part eight. <bookmark mark='d'/> The ratio comes "
            "straight from the accounts. <bookmark mark='e'/> Agora checks it on one firm whose true markup is one "
            "point two five: an elasticity of a half, sales two and a half times the bill for materials, and the "
            "formula gives one point two five exactly. <bookmark mark='f'/> Jan De Loecker and Frederic Warzynski "
            "made this practical in 2012, building on an idea of Robert Hall's."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(rows[1]))
            for mk, r in zip("cdef", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def dial(self):
        dial = dials.DIALS["markups"]
        dl = load("dial")["dleu"]
        head = status_head(dial, r"markups over marginal cost \ (new)")
        frame, rows = dial_rows(dial, 1.0, 1.8, [1.0, 1.2, 1.4, 1.6, 1.8], r"price over marginal cost, \ "
                                r"sales-weighted mean", top=1.9, step=0.9)
        side = VGroup(
            label(rf"average profit rates rose too: \ from {100 * dl['profit_rate'][0]:.0f}\% to "
                  rf"{100 * dl['profit_rate'][1]:.0f}\%", font_size=22, color=GREY_A),
            label(r"the median firm's markup barely moved: \ the rise is at the top", font_size=22, color=GREY_A),
            label(r"Traina (2018): \ count selling, \ general and administrative costs as costs too, \\ and "
                  r"reweight public firms to stand for the whole economy: \ flat, \ or falling", font_size=22,
                  color=HOLD),
            label(r"which costs are flexible? \ which firms are counted? \ the answer turns on both", font_size=23,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"De Loecker, Eeckhout and Unger, QJE 135(2) (2020); Traina, Stigler Center WP 272 "
                            r"(2018)", corner=UR, font_size=12)
        with self.voiceover(
            "Here is what it found. <bookmark mark='a'/> Applying the formula to every American public company from "
            "1955, De Loecker, Jan Eeckhout and Gabriel Unger found the average markup, weighted by sales, at one "
            "point two one in 1980, when it began to rise, and one point six one by 2016. <bookmark mark='b'/> "
            "Average profits rose with it, from one percent to eight. <bookmark mark='c'/> But the median firm's "
            "markup hardly moved: the rise came from the firms at the top, and from sales shifting toward them. "
            "<bookmark mark='d'/> James Traina pointed out that the formula needs the right flexible costs. Count "
            "selling, general and administrative costs, marketing and management, as costs of production, and "
            "reweight public firms to stand for the whole economy, and the aggregate markup is flat or even falling. "
            "<bookmark mark='e'/> So this dial is contested, and the dispute is about measurement: which costs are "
            "flexible, and which firms are counted. Part forty-three returns to it with the demand-side methods."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.6), run_time=2.5)
            for mk, r in zip("bcde", side):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
            self.play(Indicate(head[1], color=WHITE))
        self.clear_scene()
