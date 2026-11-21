from __future__ import annotations

from videos.economics.econ54.common import *  # noqa: F403


class Structural(VoiceoverScene):
    def construct(self):
        card(self, 1, r"What ``structural'' means", r"Which numbers stay put when the policy changes?",
             "Chapter one. What structural means.", lit={1953: r"Marschak", 1976: r"Lucas"},
             scale=("person", "nation"), horizon=("a decade",))
        self.two_kinds()
        self.history()

    def two_kinds(self):
        hc = history_card(1953, r"Jacob Marschak", r"``Economic measurements for policy and prediction'': \ to "
                          r"predict a policy never tried, \ measure what it will not change", color=MODEL,
                          width=10.0, font_size=24).move_to(UP * 0.4)
        red = flow_chain(steps=[(r"a history", DATA), (r"a pattern in it", GRID),
                                (r"a forecast, while the world stays as it was", GRID)],
                         box_w=3.2, box_h=1.0, font_size=19, buff=0.5)
        st = flow_chain(steps=[(r"choices", DATA), (r"preferences and constraints", MODEL),
                               (r"a forecast for any policy that leaves them alone", GAIN)],
                        box_w=3.2, box_h=1.0, font_size=19, buff=0.5)
        heads = VGroup(label(r"reduced form", font_size=24, color=GRID), label(r"structural", font_size=24,
                                                                                color=MODEL))
        VGroup(VGroup(heads[0], red).arrange(DOWN, buff=0.25),
                       VGroup(heads[1], st).arrange(DOWN, buff=0.25)).arrange(DOWN, buff=0.7).move_to(UP * 0.3)
        foot = label(r"Lucas (1976): \ a pattern fitted under one policy can break under another \ (Part 28)",
                     font_size=20, color=E.ACCENT).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Economists use the word structural a great deal. Jacob Marschak gave it its meaning in 1953: to "
            "predict the effect of a policy that has never been tried, you must measure the things the policy "
            "will not change. <bookmark mark='a'/> A reduced-form forecast takes a history, finds a pattern in it, "
            "and extends the pattern. That is fine while the world stays as it was. <bookmark mark='b'/> A "
            "structural forecast goes from choices to what produced them, preferences and constraints, and then "
            "asks how the same people, with the same preferences, would choose under the new policy. <bookmark "
            "mark='c'/> Robert Lucas's critique, from Part twenty-eight, is the warning: a pattern fitted under one "
            "policy can break under another, because the pattern was itself a response to the old policy."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeOut(hc))
            self.play(FadeIn(heads[0]), *[FadeIn(b) for b in red.boxes], *[Create(a) for a in red.arrows])
            vo.wait_until("b")
            self.play(FadeIn(heads[1]), *[FadeIn(b) for b in st.boxes], *[Create(a) for a in st.arrows])
            vo.wait_until("c")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()

    def history(self):
        H = load("history")
        ax = plane([-1.5, 9.0], [-0.4, 0.6], center=LEFT * 1.8 + DOWN * 0.35, x_length=7.8, y_length=4.9,
                   xticks=[-1, 0, 2, 4, 6, 8], yticks=[-0.4, -0.2, 0, 0.2, 0.4, 0.6],
                   xlabel=r"change in the cost of a car trip, \ dollars", ylabel=r"share of commuters who drive",
                   xfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0",
                   yfmt=lambda v: f"{100 * v:.0f}\\%".replace("-", "{-}"), font_size=14)
        zero = DashedLine(ax.ax.c2p(-1.5, 0), ax.ax.c2p(9, 0), color=GREY_D, stroke_width=1.2)
        pts = VGroup(*[dot(ax, x, y, DATA, 0.07) for x, y in zip(H["shifts"], H["obs"])])
        a, b = H["line"]
        line_in = seg(ax, -1.0, a - b, 1.5, a + 1.5 * b, GRID, 2.6)
        xe = min(9.0, (-0.4 - a) / b)
        line_out = seg(ax, 1.5, a + 1.5 * b, xe, a + xe * b, GRID, 2.6, dashed=True)
        g = np.array(H["grid"])
        truth = path(ax, g, H["truth_curve"], TRUTHC, 2.2)
        logit = path(ax, g, H["logit_curve"], EST, 3.0)
        ch = H["charge"]
        cl = vline(ax, ch, -0.4, 0.6, ERR, 1.6)
        side = VGroup(
            label(r"blue: \ twelve years of fuel prices, \\ and the share who drove", font_size=18, color=DATA),
            label(r"grey: \ a straight line through them", font_size=18, color=GRID),
            label(rf"an \${ch:.0f} charge per trip: \\ the line says "
                  rf"{100 * H['charge_line']:.0f}\%".replace("-", "{-}"), font_size=19, color=ERR),
            label(rf"gold: \ the logit from Chapter 2: \ {100 * H['charge_logit']:.1f}\% \\ white: \ the truth: \ "
                  rf"{100 * H['charge_truth']:.1f}\%", font_size=19, color=EST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(r"simulated: \ the Island's 3,000 commuters", corner=DR, font_size=13)
        with self.voiceover(
            "Here is the difference on the Island, where we know the truth. <bookmark mark='a'/> For twelve years "
            "the price of fuel moved the cost of a car trip up and down by a dollar or so, and each year a share "
            "of the Island's three thousand commuters drove. <bookmark mark='b'/> A straight line fits that "
            "history well: each extra dollar, about ten points fewer drivers. <bookmark mark='c'/> Now the town "
            f"proposes a congestion charge of {ch:.0f} dollars a trip, far outside anything in the history. The "
            f"line says {say_pct(H['charge_line'], 0)} of commuters would drive: fewer than none. <bookmark "
            "mark='d'/> The logit we will estimate in the next chapter models each commuter's choice, so the "
            "share can never fall below zero; as the charge rises, fewer and fewer drivers are left to lose. It "
            f"says {say_pct(H['charge_logit'], 1)}. The truth is {say_pct(H['charge_truth'], 1)}. <bookmark "
            "mark='e'/> The line was not wrong about the past. It was never a model of why people drive, so it "
            "had nothing to say about a world it had not seen."
        ) as vo:
            self.play(FadeIn(ax), Create(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_, scale=0.5) for p_ in pts], lag_ratio=0.1), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(line_in), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cl))
            self.play(Create(line_out), FadeIn(side[2]), run_time=1.6)
            vo.wait_until("d")
            self.play(Create(logit), Create(truth), FadeIn(side[3]), run_time=2.0)
            vo.wait_until("e")
            self.play(Indicate(line_out, color=ERR, scale_factor=1.0))
        self.clear_scene()
