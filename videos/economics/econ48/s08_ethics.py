from __future__ import annotations

from videos.economics.econ48.common import *  # noqa: F403


class Ethics(VoiceoverScene):
    def construct(self):
        card(self, 7, r"The social cost of carbon: \ ethics and evidence", r"Where should a discount rate come from?",
             "Chapter seven. The social cost of carbon: ethics and evidence.",
             lit={1928: r"Ramsey", 2006: r"Stern", 2022: r"Rennert et al."}, scale=("world",),
             horizon=("a century",))
        self.ramsey()
        self.two_worlds()
        self.is_ought()
        self.official()

    def ramsey(self):
        S = load("scc")
        g = 100 * S["first_growth"]
        eq = MathTex(r"r \;=\; \rho \;+\; \eta\, g", font_size=60, color=THEORY).move_to(UP * 1.9)
        parts = VGroup(
            VGroup(MathTex(r"\rho", font_size=44, color=STERN),
                   label(r"pure time preference: \\ how much less a person \\ counts because they \\ live later",
                         font_size=19, color=WHITE)).arrange(DOWN, buff=0.2),
            VGroup(MathTex(r"\eta", font_size=44, color=COOL),
                   label(r"how fast an extra dollar \\ matters less as people \\ grow richer", font_size=19,
                         color=WHITE)).arrange(DOWN, buff=0.2),
            VGroup(MathTex(r"g", font_size=44, color=GAIN),
                   label(rf"growth of consumption \\ per head: \ here \\ about {g:.2f}\% a year", font_size=19,
                         color=WHITE)).arrange(DOWN, buff=0.2),
        ).arrange(RIGHT, buff=1.0).move_to(DOWN * 0.6)
        foot = label(r"future people will be richer, \ so a dollar to them is worth less; \ $\rho$ asks whether they "
                     r"count less for being later", font_size=20, color=E.ACCENT).to_edge(DOWN, buff=0.7)
        tag = published_tag(r"Ramsey, \ Economic Journal (1928)", corner=DR, font_size=11)
        with self.voiceover(
            "Frank Ramsey worked out in 1928 what the discount rate for consumption should be, if a society plans "
            "its saving well. <bookmark mark='a'/> The rate r is the sum of two terms. <bookmark mark='b'/> Rho, "
            "the rate of pure time preference: how much less a person's well-being counts simply because they live "
            "later. <bookmark mark='c'/> Eta, how fast an extra dollar matters less as people grow richer, <bookmark "
            f"mark='d'/> times g, the growth of consumption per head, about {g:.2f} percent a year in the model. "
            "<bookmark mark='e'/> The second term is uncontroversial in kind: if our grandchildren will be richer, "
            "a dollar of damage to them costs them less than a dollar costs us now. The first term is the fight."
        ) as vo:
            self.play(FadeIn(tag), Write(eq), run_time=1.5)
            for mk, p_ in zip("bcd", parts):
                vo.wait_until(mk)
                self.play(FadeIn(p_, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def two_worlds(self):
        D = load("dice")
        S = load("scc")
        O, St = D["opt"], D["stern"]
        T = tables.STERN_2006.data
        ax = plane([2025, 2200], [0, 45], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.6, y_length=4.6,
                   xticks=[2050, 2100, 2150, 2200], yticks=[0, 10, 20, 30, 40], xfmt=lambda v: f"{v:.0f}",
                   ylabel=r"emissions on the optimal path, \ GtCO$_2$ a year", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        y = np.array(O["year"])
        k = y <= 2200
        lo = path(ax, y[k], np.array(O["E"])[k], OPT, 3.2, smooth=False)
        ls = path(ax, y[k], np.array(St["E"])[k], STERN, 3.2, smooth=False)
        side = VGroup(
            label(rf"green: \ $\rho$ = 1.5\%, \ $\eta$ = 1.45 \\ $r \approx$ {100 * S['r_ramsey_n']:.1f}\%: \ "
                  rf"cost of a \\ tonne \${S['ramsey']:.0f}; \ warming \\ peaks at {O['peak_T']:.1f}\textdegree",
                  font_size=18, color=OPT),
            label(rf"purple: \ the Stern Review's \\ $\rho$ = {T['rho']}\%, \ $\eta$ = 1 \\ $r \approx$ "
                  rf"{100 * S['r_ramsey_s']:.1f}\%: \ cost of a \\ tonne \${S['stern']:.0f}; \ net zero \\ by "
                  rf"{St['zero_year']}, \ peak {St['peak_T']:.1f}\textdegree", font_size=18, color=STERN),
            label(r"same model, \ same damages, \\ same climate", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.3)
        tag = published_tag(tables.STERN_2006.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Two views of rho give two worlds. <bookmark mark='a'/> With a pure time preference of one and a half "
            "percent and an eta of 1.45, the discount rate is about "
            f"{100 * S['r_ramsey_n']:.0f} percent, close to what capital earns, a tonne costs {S['ramsey']:.0f} "
            "dollars, and the optimal path "
            f"lets warming peak at {O['peak_T']:.1f} degrees. <bookmark mark='b'/> In 2006 the Stern Review, "
            "written for Britain's Treasury by Nicholas Stern, argued that it is unethical to count future people "
            "less merely for being later. It set rho at 0.1 percent, allowing only for the chance that humanity "
            f"dies out, and eta at one. Then the discount rate is about {100 * S['r_ramsey_s']:.1f} percent, a tonne "
            f"costs {S['stern']:.0f} dollars in this model, emissions fall to zero by about {St['zero_year']}, and "
            f"warming peaks at {St['peak_T']:.1f} degrees. The Review itself, with its own model, put the social cost "
            "at over three hundred dollars a tonne of carbon, over eighty a tonne of carbon dioxide. <bookmark "
            "mark='c'/> The model, the damages and the climate are the same. Only the weight on the future "
            "changed."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(lo), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(ls), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def is_ought(self):
        card_ = is_ought_card(
            r"a dollar invested today returns several percent a year; \ the future will probably be richer; \ the "
            r"damage from a tonne lasts for centuries",
            r"the carbon price a government should set, \ and so how much the world should cut now",
            r"how much the well-being of people not yet born should count against ours, \ and whether the market's "
            r"return is the right guide for choices that span generations",
            width=12.0, font_size=23).move_to(DOWN * 0.1)
        tag = published_tag(r"Nordhaus (2007) and Weitzman (2007), \ JEL; \ Stern (2007)", corner=DR, font_size=11)
        with self.voiceover(
            "This is the clearest case in the course of a step from is to ought. <bookmark mark='a'/> What is: "
            "invested capital earns several percent a year; future people will probably be richer; a tonne does "
            "damage for centuries. <bookmark mark='b'/> What the step needs: a judgment about how much people not "
            "yet born should count against us, and whether the return on capital, which Nordhaus used to argue for "
            "a higher rate, is the right guide for choices that span generations. <bookmark mark='c'/> And what "
            "follows: the carbon price, and how much the world should cut now. Economists can make the "
            "consequences of each choice exact, as the model just did. They cannot make the choice for you."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(card_.card), FadeIn(card_.is_row))
            vo.wait_until("b")
            self.play(FadeIn(card_.judgment), FadeIn(card_[1][1]))
            vo.wait_until("c")
            self.play(FadeIn(card_.ought), FadeIn(card_[1][3]))
        self.clear_scene()

    def official(self):
        U = tables.SCC_US.data
        Dt = tables.DICE_2023.data
        S = load("scc")
        rows = [(r"Nordhaus, \ DICE-2016R \ (2010 \$, for 2015)", Dt["scc_2016"], GREY_B),
                (r"the US interim figure, \ 2021", U["iwg"], GREY_B),
                (r"Barrage and Nordhaus, \ DICE-2023", Dt["scc_base"], METAL),
                (r"this film, \ $\rho$ 1.5\%, \ $\eta$ 1.45", S["ramsey"], OPT),
                (r"Rennert et al., \ 2022: \ 2\% near-term", U["rennert"], COOL),
                (r"EPA, \ 2023: \ central estimate", U["epa"], COOL)]
        bars = VGroup()
        for i, (nm, v, col) in enumerate(rows):
            y = 2.0 - 0.78 * i
            w = v / 200 * 6.6
            r = Rectangle(width=w, height=0.5, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([-1.0 + w / 2, y, 0]))
            bars.add(VGroup(label(nm, font_size=18, color=col).next_to(np.array([-1.2, y, 0]), LEFT, buff=0.1), r,
                            label(rf"\${v:.0f}", font_size=20, color=WHITE).next_to(r, RIGHT, buff=0.15)))
        head = label(r"the social cost of carbon, \ official and academic", font_size=28, color=E.ACCENT).to_edge(
            UP, buff=0.45)
        foot = label(rf"Rennert et al.'s 5--95\% range: \ \${U['rennert_lo']} to \${U['rennert_hi']}; \ dollars of "
                     r"each study's year", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.55)
        tag = published_tag(tables.SCC_US.tag, corner=DR, font_size=11)
        with self.voiceover(
            "And the numbers governments have used? <bookmark mark='a'/> Nordhaus's 2016 model gave "
            f"{Dt['scc_2016']} dollars a tonne, in 2010 dollars. <bookmark mark='b'/> The United States' interim "
            f"interagency figure of 2021 was {U['iwg']}. <bookmark mark='c'/> DICE-2023, with damages nearly twice as "
            f"large as its predecessor's, {Dt['scc_base']}. <bookmark mark='d'/> This film's model, "
            f"{S['ramsey']:.0f}. <bookmark mark='e'/> In 2022 Kevin Rennert and colleagues, with newer evidence on "
            f"damages and a near-term discount rate of two percent, found {U['rennert']}, with a range from "
            f"{U['rennert_lo']} to {U['rennert_hi']}. <bookmark mark='f'/> And the Environmental Protection "
            f"Agency's 2023 estimate drew on that work: {U['epa']} dollars a tonne. Most of the gap between the "
            "low numbers and the high ones is the discount rate, as chapter six showed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(foot))
            for mk, b in zip("abcdef", bars):
                vo.wait_until(mk)
                self.play(FadeIn(b[0]), GrowFromEdge(b[1], LEFT), FadeIn(b[2]))
        self.clear_scene()
