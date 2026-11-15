from __future__ import annotations

from videos.psychology.psych24.common import *  # noqa: F403


class Causes(VoiceoverScene):
    def construct(self):
        self.card()
        self.power()
        self.intervene()

    def card(self):
        card = chapter_card(10, r"Reasoning about causes", r"How do you tell a cause from a coincidence?",
                            lit={1997: r"Cheng", 2005: r"Waldmann \& Hagmayer"},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter ten. Reasoning about causes."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def power(self):
        d = load("causes")
        head = heading(r"Derivation: \ from $\Delta P$ to causal power")
        eqs = VGroup(
            MathTex(r"\Delta P = P(e \mid c) - P(e \mid \neg c)", font_size=34, color=LOGIC),
            MathTex(r"P(e \mid c) = P(e \mid \neg c) + q\,\bigl(1 - P(e \mid \neg c)\bigr)", font_size=32,
                    color=GREY_A),
            MathTex(r"q = \frac{\Delta P}{1 - P(e \mid \neg c)}", font_size=36, color=MODEL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-3.5, 1.2, 0])
        A = axes([0, 0.9], [0, 0.6], x_length=4.6, y_length=2.3, xticks=[0, 0.3, 0.6, 0.9], yticks=[0, 0.25, 0.5],
                 xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.2f}", xlabel=r"$P(e \mid \neg c)$, \ the background",
                 center=[-3.3, -2.0, 0], font_size=15)
        dp = curve(A.ax, d["base"], d["delta_p"], LOGIC, 3)
        pw = curve(A.ax, d["base"], d["power"], MODEL, 3)
        key = legend([(LOGIC, r"$\Delta P$"), (MODEL, r"causal power $q$")], font_size=16).move_to(A.ax.c2p(0.2, 0.12))
        assert np.allclose(d["power"], d["q"])
        rows = rows_of([
            (r"Part 16's contingency: \ how much more often the effect follows the cause than not, \ $\Delta P$", WHITE),
            (r"Cheng, \ 1997: \ but a cause can only act where the effect would not have happened anyway", LOGIC),
            (r"assume the cause produces the effect with probability $q$, \ independently of the background: \ "
             r"solving for $q$ gives \emph{causal power}", MODEL),
            (rf"a cause of the same strength, \ $q = {d['q']:.1f}$, \ on ever busier backgrounds: \ $\Delta P$ "
             rf"shrinks toward zero; \ power stays put", MODEL),
            (r"people's judgements follow power more than $\Delta P$ in many experiments, \ though not all", GREY_A),
        ], 5.6, 23, 0.34).move_to([3.6, 0.0, 0])
        tag = psyche_tag(r"\texttt{reason.delta\_p}, \ \texttt{causal\_power}; \ Cheng (1997)")
        with self.voiceover(
            "Part 16 measured how strongly a cue predicts an outcome by contingency: how much more often the effect "
            "follows the cause than follows its absence. <bookmark mark='a'/> That's delta P. "
            "<bookmark mark='b'/> In 1997 Patricia Cheng pointed out a problem. A cause can only show its effect "
            "where the effect wouldn't have happened anyway. If a headache is already likely, a medicine that causes "
            "headaches has fewer chances to show it. <bookmark mark='c'/> So assume the cause produces the effect with "
            "some probability q, independently of everything else. The probability of the effect given the cause is "
            "then the background rate plus q times what's left. Solve for q, and you get causal power: delta P "
            "divided by one minus the background. <bookmark mark='d'/> Take a cause of the same strength, a half, on "
            "busier and busier backgrounds. Delta P shrinks toward zero. Power stays at a half. "
            "<bookmark mark='e'/> In many experiments people's judgements follow power more closely than delta P, "
            "though not in all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Write(eqs[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Write(eqs[1]), Write(eqs[2]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(A), Create(dp), Create(pw), FadeIn(key), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def intervene(self):
        head = heading(r"Seeing, \ and doing")
        nodes = {"weather": (-4.6, 1.4), "barometer": (-2.4, 0.2), "storm": (-4.6, -1.0)}
        dots = {k: VGroup(Circle(radius=0.55, color=SEARCH, fill_opacity=0.15),
                          label(k, font_size=20)).move_to([x, y, 0]) for k, (x, y) in nodes.items()}
        a1 = Arrow(dots["weather"].get_center(), dots["barometer"].get_center(), buff=0.6, color=GREY_B)
        a2 = Arrow(dots["weather"].get_center(), dots["storm"].get_center(), buff=0.6, color=GREY_B)
        hand = label(r"you move the needle", font_size=20, color=LOST).next_to(dots["barometer"], DOWN, buff=0.2)
        cut = Cross(a1, stroke_color=LOST, stroke_width=4).scale(0.4)
        rows = rows_of([
            (r"a falling barometer predicts a storm: \ \emph{seeing} it fall raises the chance of rain", WHITE),
            (r"pushing the needle down does not: \ an intervention cuts the arrow into what you set", LOST),
            (r"Waldmann \& Hagmayer, \ 2005: \ people given a causal model predict different things after seeing "
             r"and after doing, \ as the model says", MODEL),
            (r"the mathematics of interventions on causal graphs is \emph{Statistics, Built} Part 36", GREY_A),
        ], 6.2, 24, 0.36).move_to([3.3, 0.0, 0])
        tag = published_tag(r"Waldmann \& Hagmayer (2005); \ Pearl (2000)")
        with self.voiceover(
            "Causal knowledge does something that correlation can't. <bookmark mark='a'/> A falling barometer "
            "predicts a storm. Seeing the needle fall should make you expect rain. <bookmark mark='b'/> But if you "
            "push the needle down with your finger, the storm is no more likely. Intervening on something cuts it "
            "off from its usual causes. <bookmark mark='c'/> Michael Waldmann and York Hagmayer gave people causal "
            "models of this kind and found that their predictions after seeing a variable change differed from their "
            "predictions after setting it, much as the models require. <bookmark mark='d'/> The mathematics of "
            "interventions on causal graphs is Part 36 of Statistics, Built."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), *[FadeIn(v) for v in dots.values()], GrowArrow(a1), GrowArrow(a2))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(hand), Create(cut), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
