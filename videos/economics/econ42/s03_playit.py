from __future__ import annotations

from videos.economics.econ42.common import *  # noqa: F403


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Play it: \ set the unemployment benefit", r"How generous should the Island be?",
             "Chapter two. Play it: set the unemployment benefit.", lit={1978: r"Baily"},
             scale=("person", "nation"), horizon=("a year",))
        self.ask()
        self.reveal()
        self.curve()

    def ask(self):
        B = load("baily")
        facts = VGroup()
        for big, small, col in ((r"lose your job", r"search: \ the harder you look, \\ the likelier a job; \\ "
                                                    r"looking is costly", UNEMP),
                                (r"if the search fails", r"a benefit $b$, \\ a share of the wage", SMOOTH),
                                (r"if it succeeds", r"the wage, \\ less the tax that \\ pays for the benefits", WORK),
                                (r"besides", rf"savings and a partner's \\ income: \ {B['A']:g} times \\ the wage; "
                                             rf"\\ risk aversion {B['gamma']:g}", GREY_A)):
            box = RoundedRectangle(width=3.0, height=2.3, corner_radius=0.12, stroke_color=col, stroke_width=2.2,
                                   fill_color="#141821", fill_opacity=1)
            t1 = label(big, font_size=22, color=col).move_to(box.get_top() + DOWN * 0.42)
            t2 = label(small, font_size=16, color=GREY_A).next_to(t1, DOWN, buff=0.22)
            facts.add(VGroup(box, t1, t2))
        facts.arrange(RIGHT, buff=0.3).move_to(UP * 0.7)
        opts = VGroup(*[label(o, font_size=26, color=WHITE) for o in
                        [rf"{k}: \ {100 * v:.0f}\% of the wage" for k, v in zip("ABCD", B["options"])]]).arrange(
            RIGHT, buff=0.6).next_to(facts, DOWN, buff=0.55)
        head = label(r"Your turn: \ which benefit makes the Island's workers best off?", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.35)
        ring = countdown().scale(0.6).next_to(opts, DOWN, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        for f in facts:
            f.set_opacity(0.3)
        with self.voiceover(
            "Your turn. On the Island, workers who lose their jobs look for new ones. <bookmark mark='a'/> The "
            "harder they search, the likelier they are to find work, but searching is costly. "
            "<bookmark mark='b'/> If the search fails, they receive a benefit, a share of the wage. "
            "<bookmark mark='c'/> If it succeeds, they earn the wage, less a tax that pays for everyone's benefits. "
            "<bookmark mark='d'/> They also have savings and a partner's income to fall back on, and they dislike "
            "risk about as much as the typical estimate. <bookmark mark='e'/> Which benefit makes them best off, "
            "counting both the comfort it gives and the search it discourages: a tenth of the wage, a third, a half, "
            "or three quarters? Pause, and choose."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(facts, lag_ratio=0.2), run_time=1.5)
            for mk, f in zip("abcd", facts):
                vo.wait_until(mk)
                self.play(f.animate.set_opacity(1.0), Indicate(f[1], scale_factor=1.1))
            vo.wait_until("e")
            self.play(FadeIn(opts), FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.play(FadeOut(ring))
        self.keep = (head, facts, opts, tag)

    def reveal(self):
        B = load("baily")
        head, facts, opts, tag = self.keep
        hl = SurroundingRectangle(opts[1], color=GAIN, buff=0.12)
        at = B["at"]
        eq = label(rf"the best benefit: \ {100 * B['bstar']:.0f}\% of the wage; \ then {100 * at['e']:.0f}\% find "
                   rf"work, \ the tax is {100 * at['tau']:.1f}\%, \ consumption falls {100 * at['drop']:.0f}\% on "
                   r"losing the job", font_size=21, color=E.ACCENT).next_to(opts, DOWN, buff=0.4)
        with self.voiceover(
            "The answer is B, about a third. <bookmark mark='a'/> At that benefit, "
            f"{say_pct(at['e'], 0)} of those who lose their jobs find work within the period, the tax that pays "
            f"for the benefits is {say_pct(at['tau'], 1)} of the wage, and consumption falls by "
            f"{say_pct(at['drop'], 0)} on losing the job. Less generous, and the unemployed bear too much of the "
            "risk. More generous, and too many stop looking, so that the tax to pay for it all rises faster than "
            "the comfort it buys."
        ) as vo:
            self.play(Create(hl))
            vo.wait_until("a")
            self.play(FadeIn(eq, shift=UP * 0.1))
        self.clear_scene()

    def curve(self):
        B = load("baily")
        b = np.array(B["b"])
        w = np.array(B["welfare"])
        wn = (w - w.min()) / (w.max() - w.min())
        ax = plane([0, 0.6], [0, 1.05], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], yticks=[0, 0.5, 1.0],
                   xlabel=r"benefit, \ share of the wage", ylabel=r"workers' expected welfare \ (rescaled)",
                   xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{v:.1f}", font_size=14)
        ln = path(ax, b, wn, GAIN, 3.4)
        k = int(np.argmin(np.abs(b - B["bstar"])))
        top = VGroup(vline(ax, B["bstar"], 0, 1.05, GAIN), dot(ax, b[k], wn[k], GAIN, 0.09))
        e = path(ax, b, np.array(B["e"]), UNEMP, 2.4)
        dr = path(ax, b, 4 * np.array(B["drop"]), SMOOTH, 2.4)
        side = VGroup(
            label(r"green: \ welfare, \ counting \\ the comfort and the \\ cost of searching", font_size=18,
                  color=GAIN),
            label(r"blue: \ the chance of \\ finding work falls", font_size=18, color=UNEMP),
            label(r"pale: \ the fall in \\ consumption on losing \\ the job shrinks \ (x4)", font_size=18,
                  color=GREY_A),
            label(rf"the top: \ {100 * B['bstar']:.0f}\%", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        dr.set_stroke(color=GREY_A)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is the whole trade. <bookmark mark='a'/> Expected welfare, counting the comfort of benefits and "
            "the cost of searching, rises with the benefit at first, then falls. <bookmark mark='b'/> Behind it, "
            "two forces. As benefits rise, the chance of finding work within the period falls, because the "
            "unemployed search less. <bookmark mark='c'/> And the fall in consumption on losing a job shrinks, "
            f"which is what insurance is for. <bookmark mark='d'/> The top is at {say_pct(B['bstar'], 0)} of the "
            "wage. The next chapter finds the same answer from a formula that needs only two numbers, both of which "
            "can be measured."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(e), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(dr), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(top), FadeIn(side[3]))
        self.clear_scene()
