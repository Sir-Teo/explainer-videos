from __future__ import annotations

from videos.economics.econ32.common import *  # noqa: F403


class Theory(VoiceoverScene):
    def construct(self):
        card(self, 3, r"The multiplier in theory", r"How much output does a dollar of government spending buy?",
             "Chapter three. The multiplier in theory.",
             lit={1931: r"Kahn", 2011: r"Woodford; \ Christiano, \ Eichenbaum and Rebelo"}, scale=("nation",),
             horizon=("a quarter", "years"))
        self.cross()
        self.nk()

    def cross(self):
        rows = VGroup(
            label(r"three answers, \ from three models", font_size=27, color=E.ACCENT),
            label(r"the Keynesian cross \ (Part 27): \ each dollar spent is someone's income, \ spent again",
                  font_size=22, color=SPEND),
            MathTex(r"\frac{\Delta Y}{\Delta G} = \frac{1}{1 - \text{MPC}} = 2.5 \quad (\text{MPC} = 0.6)",
                    font_size=36, color=SPEND),
            label(r"crowding out: \ spending raises interest rates, \ which cut investment", font_size=22, color=RATE),
            label(r"Ricardian households \ (Barro): \ they expect the taxes that will pay for it, \ and spend less",
                  font_size=22, color=TAX),
            label(r"in the model of Part 30, \ it depends on what the central bank does", font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"Kahn, \ \emph{Economic Journal} 41(162) (1931); \ Barro, \ \emph{JPE} 82(6) (1974)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Theory gives three answers. <bookmark mark='a'/> The Keynesian cross of Part 27: a dollar the "
            "government spends is someone's income, part of which is spent again, and again. <bookmark mark='b'/> "
            "With sixty cents of each extra dollar spent, the multiplier is two and a half. <bookmark mark='c'/> But "
            "spending can raise interest rates, which cut private investment: crowding out. "
            "<bookmark mark='d'/> And households who expect the taxes that will pay for the spending may spend "
            "less themselves, as Robert Barro argued. <bookmark mark='e'/> In the New Keynesian model of Part 30, "
            "the answer depends above all on the central bank."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def nk(self):
        N = load("nk")
        rho = np.array(N["rho"])
        ax = plane([0, 0.75], [0, 3.0], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[0, 0.25, 0.5, 0.75], yticks=[0, 0.5, 1, 1.5, 2, 2.5, 3],
                   xlabel=r"how long the spending lasts \ (persistence, \ quarter to quarter)",
                   ylabel=r"the multiplier, \ $\Delta Y / \Delta G$", xfmt=lambda v: f"{v:.2f}",
                   yfmt=lambda v: f"{v:.1f}", font_size=15)
        one = seg(ax, 0, 1, 0.75, 1, GREY_C, 1.5, dashed=True)
        normal = path(ax, rho, N["normal"], SPEND, 3.5)
        zlb = path(ax, rho, np.array(N["zlb"]), INFL, 3.5, yr=(0, 3.0))
        edge = vline(ax, N["edge"], 0, 3.0, HOLD, 2)
        P = N["points"]
        side = VGroup(
            label(r"teal: \ a central bank following \\ Taylor's rule", font_size=18, color=SPEND),
            label(rf"below one: \ {P['0.5']['normal']:.2f} for spending \\ that halves each quarter", font_size=18,
                  color=SPEND),
            label(r"red: \ the rate stuck at zero \\ for as long as the spending", font_size=18, color=INFL),
            label(rf"above one: \ {P['0.5']['zlb']:.2f}, \ and {P['0.7']['zlb']:.1f} \\ if it lasts longer",
                  font_size=18, color=INFL),
            label(r"the more persistent the trap, \\ the bigger the multiplier", font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Woodford, \ \emph{AEJ: Macro} 3(1) (2011); \ Christiano, \ Eichenbaum and Rebelo, \ "
                            r"\emph{JPE} 119(1) (2011); \ the Island", corner=DR, font_size=12)
        with self.voiceover(
            "Here is the multiplier in Part 30's model, for spending that fades at different speeds. "
            "<bookmark mark='a'/> With a central bank that follows Taylor's rule, extra spending raises inflation "
            "and the bank raises its rate, crowding out private demand. <bookmark mark='b'/> The multiplier is "
            f"below one: {P['0.5']['normal']:.2f} for spending that halves each quarter, and smaller the longer it "
            "lasts. <bookmark mark='c'/> Now put the economy at the zero bound, with the rate stuck at zero for as "
            "long as the spending lasts. <bookmark mark='d'/> Extra spending raises expected inflation, which "
            f"lowers the real interest rate instead of raising it: the multiplier is {P['0.5']['zlb']:.2f}, and "
            f"{P['0.7']['zlb']:.1f} if the trap and the spending are more persistent. <bookmark mark='e'/> Michael "
            "Woodford, and Lawrence Christiano, Martin Eichenbaum and Sergio Rebelo, showed this in 2011. Past the "
            "dashed line, the model has no stable answer at all. Theory says the multiplier is not one number. It "
            "depends on the state of the economy and on the central bank."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(one), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(normal), FadeIn(side[0]), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(zlb), FadeIn(side[2]), run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(edge), FadeIn(side[4]))
        self.clear_scene()
