from __future__ import annotations

from videos.economics.econ55.common import *  # noqa: F403

LETTERS = ("A", "B", "C")


def panels(P, width=3.5, height=2.6):
    """Three small plots of output (level), inflation and the rate after one shock each."""
    g = VGroup()
    for k, pan in enumerate(P["panels"]):
        h = np.arange(len(pan["y"]))
        ax = plane([0, 12], [-0.6, 1.3], x_length=width, y_length=height, xticks=[0, 4, 8, 12],
                   yticks=[-0.5, 0, 0.5, 1.0], xlabel=r"quarters", ylabel=r"",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.1f}".replace("-", "{-}") if v else "0",
                   font_size=11)
        z = DashedLine(ax.ax.c2p(0, 0), ax.ax.c2p(12, 0), color=GREY_D, stroke_width=1)
        lines = VGroup(path(ax, h, pan["y"], OUT, 2.4), path(ax, h, pan["pi"], INFL, 2.4),
                       path(ax, h, pan["i"], RATE, 2.4))
        name = label(LETTERS[k], font_size=30, color=WHITE).next_to(ax, UP, buff=0.15)
        g.add(VGroup(ax, z, lines, name))
    return g.arrange(RIGHT, buff=0.6)


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Play it: \ which shock was it?", r"Can you tell a shock by what it does?",
             "Chapter two. Play it: which shock was it?", lit={2005: r"Uhlig"}, scale=("nation",),
             horizon=("a year",))
        self.ask()
        self.reveal()

    def ask(self):
        P = load("playit")
        g = panels(P).move_to(UP * 0.6)
        key = VGroup(label(r"blue: \ output", font_size=19, color=OUT), label(r"orange: \ inflation", font_size=19,
                                                                             color=INFL),
                     label(r"pink: \ the policy rate", font_size=19, color=RATE)).arrange(RIGHT, buff=0.7).next_to(
            g, DOWN, buff=0.45)
        q = label(r"Which of A, \ B, \ C is a monetary tightening?", font_size=25, color=E.ACCENT).next_to(
            key, DOWN, buff=0.4)
        ring = countdown().scale(0.5).next_to(q, DOWN, buff=0.3)
        tag = island_tag(r"simulated: \ the Island's three shocks", corner=DR, font_size=13)
        intro = VGroup(
            label(r"supply: \ a change in what the Island can produce", font_size=24, color=SUPPLY),
            label(r"demand: \ a change in what people want to spend", font_size=24, color=DEMAND),
            label(r"monetary: \ a surprise from the central bank", font_size=24, color=MONEY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(UP * 0.3)
        with self.voiceover(
            "Your turn. The Island's economy is hit by three kinds of shock: a change in what it can produce, a "
            "change in what people want to spend, and a surprise from the central bank. <bookmark mark='a'/> Here "
            "is what each one does, unlabelled: output in blue, inflation in orange, the policy rate in pink, over "
            "three years. <bookmark mark='b'/> Which of A, B and C is a monetary tightening? Pause, and choose."
        ) as vo:
            self.play(FadeIn(tag), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in intro], lag_ratio=0.5),
                      run_time=2.5)
            vo.wait_until("a")
            self.play(FadeOut(intro))
            self.play(LaggedStart(*[FadeIn(p_, shift=UP * 0.1) for p_ in g], lag_ratio=0.3), FadeIn(key),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(q), FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.play(FadeOut(ring))
        self.clear_scene()

    def reveal(self):
        P = load("playit")
        g = panels(P).move_to(UP * 1.0)
        names = {"demand": (r"demand", DEMAND), "monetary": (r"monetary", MONEY), "supply": (r"supply", SUPPLY)}
        tags = VGroup()
        for k, (sh, pan) in enumerate(zip(P["order"], g)):
            nm, col = names[sh]
            box = SurroundingRectangle(pan, buff=0.12, color=col, stroke_width=3 if sh == "monetary" else 1.5)
            tags.add(VGroup(box, label(nm, font_size=22, color=col).next_to(box, DOWN, buff=0.15)))
        rows = VGroup(
            label(r"monetary: \ the rate up, \ output and inflation down", font_size=21, color=MONEY),
            label(r"demand: \ all three up \ \qquad supply: \ output up, \ inflation down", font_size=21,
                  color=WHITE),
            label(r"you used signs: \ an assumption about what each shock does, \ not something the data said",
                  font_size=21, color=E.ACCENT),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.45)
        tag = island_tag(r"simulated: \ the Island's three shocks", corner=DR, font_size=13)
        with self.voiceover(
            f"The answer is {LETTERS[P['answer']]}. <bookmark mark='a'/> The rate jumps, and output and inflation "
            "fall: that is what a tightening should do. <bookmark mark='b'/> A is a demand shock, which pushes all "
            "three up together, and C is a supply shock, which raises output and lowers inflation. <bookmark "
            "mark='c'/> But notice how you knew. You did not read it off the data; you brought an expectation about "
            "what a tightening does, its signs, and matched it. That is an identifying assumption, and Harald "
            "Uhlig made it a method: sign restrictions, one of the five we turn to next."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(tags[P["answer"]]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(t) for k, t in enumerate(tags) if k != P["answer"]], FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
